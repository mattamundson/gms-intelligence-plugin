#!/usr/bin/env python3
"""
GMS Pricing Calculator - Standalone Pricing Engine

A production-ready pricing calculator for Greenfield Metal Sales. Calculates sell prices
for trim, panels, and coils with support for gauge/length/finish multipliers, margin
analysis, batch processing, and what-if scenarios.

No external dependencies beyond Python standard library.

Usage:
    python calculate_quote.py --product PCF9ARW10 --base-price 28.50
    python calculate_quote.py --family PCF --base-price 28.50 --gauges 29,26,24 --lengths 10,12,14
    python calculate_quote.py --batch prices.csv --output json
    python calculate_quote.py --what-if --product PCF9ARW10 --base-price 28.50 --new-cost 15.00 --target-margin 50

Author: Matt Amundson
Version: 1.0.0
"""

import argparse
import csv
import json
import sys
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Tuple
from enum import Enum


class FinishType(Enum):
    """Premium finish types with multipliers."""
    STANDARD = (1.00, "standard")
    MATTE = (1.08, "matte")
    CRINKLE = (1.15, "crinkle")
    ULG = (1.15, "ulg")

    def __init__(self, multiplier: float, name: str):
        self.multiplier = multiplier
        self.display_name = name


class MarginHealth(Enum):
    """Margin health classification."""
    RED = ("RED", "<25%", "STOP — Do NOT quote; escalate")
    LOW = ("ORANGE", "25-35%", "Flag for review; do NOT quote")
    OK = ("YELLOW", "35-45%", "Acceptable; monitor")
    GOOD = ("GREEN", "45%+", "Standard pricing approved")

    def __init__(self, code: str, range_str: str, action: str):
        self.code = code
        self.range_str = range_str
        self.action = action


@dataclass
class PricingResult:
    """Result of a single product pricing calculation."""
    product_id: Optional[str] = None
    family: Optional[str] = None
    gauge: str = ""
    length_ft: int = 0
    finish_type: str = "standard"
    base_price: float = 0.0
    gauge_mult: float = 1.0
    length_mult: float = 1.0
    finish_mult: float = 1.0
    calculated_price: float = 0.0
    cost: Optional[float] = None
    margin_pct: Optional[float] = None
    margin_health: Optional[str] = None
    target_margin: Optional[float] = None

    def to_dict(self) -> dict:
        """Convert to dictionary, excluding None values from output."""
        result = asdict(self)
        return {k: v for k, v in result.items() if v is not None}


class GMSPricingCalculator:
    """Main pricing calculator for GMS products."""

    # Gauge multipliers: 29ga is base (1.0), others calculated
    GAUGE_MULTIPLIERS = {
        "29": 1.00,
        "26": 1.20,
        "24": 1.44,
    }

    # Length multipliers: 10' is base
    LENGTH_MULTIPLIERS = {
        10: 1.00,
        12: 1.20,
        14: 1.40,
        16: 1.60,
        18: 1.80,
    }

    # Target margins by category (name, margin)
    MARGIN_TARGETS = {
        "trim": 0.50,
        "ef_panel": 0.35,  # Exposed Fastener
        "hf_panel": 0.40,  # Hidden Fastener
    }

    def __init__(self):
        """Initialize the calculator."""
        self.results: List[PricingResult] = []

    @staticmethod
    def extract_gauge_from_id(product_id: str) -> Optional[str]:
        """
        Extract gauge digit from product ID (4=24ga, 6=26ga, 9=29ga).

        Examples:
            PCF9ARW10 -> '9'
            RC109ARW10 -> '9'
            CRD8109ARW10 -> '9' (the first occurrence after profile)
        """
        # Look for gauge digits (4, 6, or 9) in the ID
        for char in product_id:
            if char in ["4", "6", "9"]:
                return char
        return None

    @staticmethod
    def extract_family_from_id(product_id: str) -> Optional[str]:
        """
        Extract family code from product ID (everything before gauge digit).

        Examples:
            PCF9ARW10 -> 'PCF'
            RC109ARW10 -> 'RC10'
            CRD8109ARW10 -> 'CRD810'
        """
        gauge_digit = None
        for i, char in enumerate(product_id):
            if char in ["4", "6", "9"]:
                gauge_digit = i
                break

        if gauge_digit is not None:
            return product_id[:gauge_digit]
        return None

    @staticmethod
    def extract_length_from_id(product_id: str) -> Optional[int]:
        """
        Extract length from product ID (10, 12, 14, 16, or 18).

        Examples:
            PCF9ARW10 -> 10
            RC109ARW12 -> 12
            CRD8109ARW14 -> 14
        """
        # Length is at the end; look for 2-digit numbers
        if len(product_id) >= 2:
            last_two = product_id[-2:]
            if last_two.isdigit():
                length = int(last_two)
                if length in GMSPricingCalculator.LENGTH_MULTIPLIERS:
                    return length
        return None

    @staticmethod
    def detect_finish_type(product_id: str) -> FinishType:
        """
        Detect premium finish from product ID.

        Premium finishes (MCC, ULG, CR + color) appear AFTER the gauge digit.
        NOT profile prefixes like CRD or CRRC.

        Examples:
            PCF9MCC10 -> Matte (MCC after gauge 9)
            PCF9CRBK10 -> Crinkle Black (CR after gauge 9)
            RAC169ULG -> ULG (after gauge 9)
            CRD8109ARW10 -> Standard (CRD is profile, not finish)
        """
        gauge_idx = None
        for i, char in enumerate(product_id):
            if char in ["4", "6", "9"]:
                gauge_idx = i
                break

        if gauge_idx is None or gauge_idx == len(product_id) - 1:
            return FinishType.STANDARD

        # Extract color code after gauge digit
        color_code = product_id[gauge_idx + 1:]

        # Check for premium finishes in color code
        if color_code.startswith("MCC"):
            return FinishType.MATTE
        elif color_code.startswith("ULG"):
            return FinishType.ULG
        elif color_code.startswith("CR"):
            # CR followed by color code = Crinkle
            return FinishType.CRINKLE

        return FinishType.STANDARD

    @staticmethod
    def gauge_digit_to_name(digit: str) -> str:
        """Convert gauge digit or string to gauge name."""
        mapping = {
            "4": "24ga", "6": "26ga", "9": "29ga",
            "24": "24ga", "26": "26ga", "29": "29ga",
        }
        return mapping.get(digit, "unknown")

    def calculate_price(
        self,
        base_price: float,
        gauge: Optional[str] = None,
        length_ft: Optional[int] = None,
        finish_type: Optional[FinishType] = None,
        product_id: Optional[str] = None,
        force_gauge: Optional[str] = None,
        force_length: Optional[int] = None,
    ) -> PricingResult:
        """
        Calculate sell price using multiplier formula.

        Sell Price = Base Price × Gauge Multiplier × Length Multiplier × Finish Multiplier

        Args:
            base_price: Base price (29ga, 10', standard finish)
            gauge: Gauge digit ('4', '6', '9') or explicit product_id for extraction
            length_ft: Length in feet (10, 12, 14, 16, 18)
            finish_type: FinishType enum
            product_id: Product ID for extraction (overrides explicit params)
            force_gauge: Force gauge value (used by family mode to override extraction)
            force_length: Force length value (used by family mode to override extraction)

        Returns:
            PricingResult with calculated price and multipliers
        """
        result = PricingResult(base_price=base_price)

        # If product_id provided, extract all info from it
        if product_id:
            result.product_id = product_id
            extracted_gauge = self.extract_gauge_from_id(product_id)
            extracted_length = self.extract_length_from_id(product_id)
            extracted_family = self.extract_family_from_id(product_id)
            extracted_finish = self.detect_finish_type(product_id)

            gauge = extracted_gauge or gauge
            length_ft = extracted_length or length_ft
            finish_type = extracted_finish or finish_type
            result.family = extracted_family

        # Apply force overrides for family mode
        if force_gauge is not None:
            gauge = force_gauge
        if force_length is not None:
            length_ft = force_length

        # Default to base case if not specified
        if gauge is None:
            gauge = "9"
        if length_ft is None:
            length_ft = 10
        if finish_type is None:
            finish_type = FinishType.STANDARD

        # Get multipliers
        gauge_mult = self.GAUGE_MULTIPLIERS.get(gauge, 1.0)
        length_mult = self.LENGTH_MULTIPLIERS.get(length_ft, 1.0)
        finish_mult = finish_type.multiplier

        # Store in result
        result.gauge = self.gauge_digit_to_name(gauge)
        result.length_ft = length_ft
        result.finish_type = finish_type.display_name
        result.gauge_mult = gauge_mult
        result.length_mult = length_mult
        result.finish_mult = finish_mult

        # Calculate price
        result.calculated_price = base_price * gauge_mult * length_mult * finish_mult

        return result

    def calculate_margin(
        self,
        sell_price: float,
        cost: float,
        target_margin: Optional[float] = None,
    ) -> Tuple[float, Optional[str]]:
        """
        Calculate margin percentage and health classification.

        Margin % = (Sell Price - Cost) / Sell Price × 100

        Args:
            sell_price: Sell price
            cost: Product cost
            target_margin: Target margin (0.0-1.0); used for health classification

        Returns:
            Tuple of (margin_pct, health_classification_str)
        """
        if sell_price == 0:
            return 0.0, None

        margin_pct = ((sell_price - cost) / sell_price) * 100

        # Classify health using fixed thresholds that match GMS business rules:
        # RED: below 25% — never quote at this margin
        # LOW/ORANGE: 25-35% — flag for review
        # OK/YELLOW: 35-45% — acceptable, monitor
        # GOOD/GREEN: above 45% — at or above target for most products
        health = None
        if target_margin:
            if margin_pct < 25:
                health = MarginHealth.RED.code
            elif margin_pct < 35:
                health = MarginHealth.LOW.code
            elif margin_pct < 45:
                health = MarginHealth.OK.code
            else:
                health = MarginHealth.GOOD.code

        return margin_pct, health

    def calculate_with_margin(
        self,
        base_price: float,
        cost: float,
        target_margin: float,
        gauge: Optional[str] = None,
        length_ft: Optional[int] = None,
        product_id: Optional[str] = None,
    ) -> PricingResult:
        """
        Calculate price based on cost and target margin.

        Sell Price = Cost ÷ (1 - Margin%)

        Args:
            base_price: Base price (for reference; actual sell price calculated from cost/margin)
            cost: Product cost
            target_margin: Target margin (0.0-1.0)
            gauge: Gauge digit
            length_ft: Length in feet
            product_id: Product ID for extraction

        Returns:
            PricingResult with cost-based pricing
        """
        # Initialize with product extraction
        result = PricingResult(base_price=base_price)

        if product_id:
            result.product_id = product_id
            extracted_gauge = self.extract_gauge_from_id(product_id)
            extracted_length = self.extract_length_from_id(product_id)
            extracted_family = self.extract_family_from_id(product_id)
            gauge = extracted_gauge or gauge
            length_ft = extracted_length or length_ft
            result.family = extracted_family

        if gauge is None:
            gauge = "9"
        if length_ft is None:
            length_ft = 10

        result.gauge = self.gauge_digit_to_name(gauge)
        result.length_ft = length_ft
        result.finish_type = "standard"

        # Safety check: margin must be < 1.0 (100%)
        if target_margin >= 1.0:
            target_margin = 0.99

        # Calculate sell price from cost and target margin
        sell_price = cost / (1 - target_margin)
        result.calculated_price = sell_price
        result.cost = cost
        result.target_margin = target_margin * 100
        margin_pct, health = self.calculate_margin(sell_price, cost, target_margin)
        result.margin_pct = round(margin_pct, 2)
        result.margin_health = health

        return result


class OutputFormatter:
    """Formats pricing results for console, CSV, and JSON output."""

    @staticmethod
    def format_console_table(results: List[PricingResult]) -> str:
        """Format results as a text table for console output."""
        if not results:
            return "No results to display."

        lines = []
        lines.append("")
        lines.append("=" * 120)
        lines.append("GMS PRICING CALCULATOR RESULTS")
        lines.append("=" * 120)

        # Header
        header = (
            f"{'Product ID':<20} {'Gauge':<8} {'Length':<8} {'Finish':<12} "
            f"{'Base Price':<12} {'Calc Price':<12} {'Margin %':<10} {'Health':<10}"
        )
        lines.append(header)
        lines.append("-" * 120)

        # Data rows
        for result in results:
            product_id = result.product_id or "(calc)"
            gauge = result.gauge or "—"
            length = str(result.length_ft) + "'" if result.length_ft else "—"
            finish = result.finish_type or "—"
            base_price = f"${result.base_price:.2f}"
            calc_price = f"${result.calculated_price:.2f}"
            margin = (
                f"{result.margin_pct:.1f}%"
                if result.margin_pct is not None
                else "—"
            )
            health = result.margin_health or "—"

            line = (
                f"{product_id:<20} {gauge:<8} {length:<8} {finish:<12} "
                f"{base_price:>11} {calc_price:>11} {margin:>9} {health:>9}"
            )
            lines.append(line)

        lines.append("-" * 120)
        lines.append("")

        return "\n".join(lines)

    @staticmethod
    def format_csv(results: List[PricingResult]) -> str:
        """Format results as CSV."""
        if not results:
            return ""

        output = []
        fieldnames = [
            "product_id",
            "family",
            "gauge",
            "length_ft",
            "finish_type",
            "base_price",
            "gauge_mult",
            "length_mult",
            "finish_mult",
            "calculated_price",
            "cost",
            "margin_pct",
            "margin_health",
            "target_margin",
        ]

        # Write header
        output.append(",".join(fieldnames))

        # Write data rows
        for result in results:
            row_dict = result.to_dict()
            row = [str(row_dict.get(field, "")) for field in fieldnames]
            output.append(",".join(row))

        return "\n".join(output)

    @staticmethod
    def format_json(results: List[PricingResult]) -> str:
        """Format results as JSON."""
        data = [result.to_dict() for result in results]
        return json.dumps(data, indent=2)


def main():
    """Main entry point with argparse CLI."""
    parser = argparse.ArgumentParser(
        description="GMS Pricing Calculator - Calculate, validate, and analyze product pricing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single product pricing
  python calculate_quote.py --product PCF9ARW10 --base-price 28.50

  # Family pricing (all gauge/length variants)
  python calculate_quote.py --family PCF --base-price 28.50 --gauges 29,26,24 --lengths 10,12,14

  # Batch CSV processing
  python calculate_quote.py --batch prices.csv --output json

  # What-if scenario (cost/margin sensitivity)
  python calculate_quote.py --what-if --product PCF9ARW10 --base-price 28.50 --new-cost 15.00 --target-margin 50

  # CSV output for spreadsheet
  python calculate_quote.py --product PCF9ARW10 --base-price 28.50 --output csv > output.csv
        """,
    )

    # Mode selection
    parser.add_argument(
        "--product",
        type=str,
        help="Single product ID (e.g., PCF9ARW10)",
    )
    parser.add_argument(
        "--family",
        type=str,
        help="Product family to price all variants (e.g., PCF)",
    )
    parser.add_argument(
        "--batch",
        type=str,
        help="CSV file with product IDs and base prices (columns: product_id, base_price)",
    )
    parser.add_argument(
        "--what-if",
        action="store_true",
        help="What-if scenario analysis (requires --product, --base-price, --new-cost, --target-margin)",
    )

    # Pricing parameters
    parser.add_argument(
        "--base-price",
        type=float,
        help="Base price (29ga/10'/standard finish) for calculation",
    )
    parser.add_argument(
        "--cost",
        type=float,
        help="Product cost (for margin calculation)",
    )
    parser.add_argument(
        "--target-margin",
        type=float,
        help="Target margin percentage (0-100, e.g., 50 for fifty)",
    )

    # Family-specific options
    parser.add_argument(
        "--gauges",
        type=str,
        default="29,26,24",
        help="Comma-separated gauge digits for family pricing (default: 29,26,24)",
    )
    parser.add_argument(
        "--lengths",
        type=str,
        default="10,12,14,16",
        help="Comma-separated lengths in feet for family pricing (default: 10,12,14,16)",
    )

    # What-if options
    parser.add_argument(
        "--new-cost",
        type=float,
        help="New cost for what-if scenario",
    )

    # Output format
    parser.add_argument(
        "--output",
        type=str,
        choices=["table", "csv", "json"],
        default="table",
        help="Output format: table, csv, or json (default: table)",
    )

    args = parser.parse_args()

    # Validate arguments and determine mode
    base_mode_count = sum([
        bool(args.product and not args.what_if),
        bool(args.family),
        bool(args.batch),
    ])

    if args.what_if:
        if not args.product or not args.base_price or not args.new_cost or not args.target_margin:
            parser.error(
                "--what-if requires --product, --base-price, --new-cost, and --target-margin"
            )
    else:
        if base_mode_count == 0:
            parser.error("One of --product, --family, or --batch is required")
        if base_mode_count > 1:
            parser.error("Only one of --product, --family, or --batch can be used")

        if args.product and not args.base_price:
            parser.error("--product mode requires --base-price")
        if args.family and not args.base_price:
            parser.error("--family mode requires --base-price")

    # Initialize calculator
    calc = GMSPricingCalculator()
    results = []

    try:
        # What-if scenario (requires product but in separate mode)
        if args.what_if:
            target_margin = args.target_margin / 100
            result = calc.calculate_with_margin(
                base_price=args.base_price,
                cost=args.new_cost,
                target_margin=target_margin,
                product_id=args.product,
            )
            results.append(result)

        # Single product pricing
        elif args.product:
            result = calc.calculate_price(
                base_price=args.base_price,
                product_id=args.product,
            )
            if args.cost:
                target_margin = (args.target_margin / 100) if args.target_margin else 0.5
                result.cost = args.cost
                margin_pct, health = calc.calculate_margin(
                    result.calculated_price,
                    args.cost,
                    target_margin,
                )
                result.margin_pct = round(margin_pct, 2)
                result.margin_health = health
                result.target_margin = args.target_margin
            results.append(result)

        # Family pricing (all variants)
        elif args.family:
            gauges = args.gauges.split(",")
            lengths = [int(x.strip()) for x in args.lengths.split(",")]

            for gauge in gauges:
                gauge = gauge.strip()
                for length in lengths:
                    result = calc.calculate_price(
                        base_price=args.base_price,
                        force_gauge=gauge,
                        force_length=length,
                    )
                    result.family = args.family
                    if args.cost:
                        target_margin = (
                            (args.target_margin / 100) if args.target_margin else 0.5
                        )
                        result.cost = args.cost
                        margin_pct, health = calc.calculate_margin(
                            result.calculated_price,
                            args.cost,
                            target_margin,
                        )
                        result.margin_pct = round(margin_pct, 2)
                        result.margin_health = health
                        result.target_margin = args.target_margin
                    results.append(result)

        # Batch CSV processing
        elif args.batch:
            try:
                with open(args.batch, "r") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        product_id = row.get("product_id", "").strip()
                        base_price_str = row.get("base_price", "").strip()
                        cost_str = row.get("cost", "").strip()

                        if not product_id or not base_price_str:
                            continue

                        base_price = float(base_price_str)
                        result = calc.calculate_price(
                            base_price=base_price,
                            product_id=product_id,
                        )

                        if cost_str:
                            cost = float(cost_str)
                            target_margin = 0.5  # Default to 50% for batch
                            result.cost = cost
                            margin_pct, health = calc.calculate_margin(
                                result.calculated_price,
                                cost,
                                target_margin,
                            )
                            result.margin_pct = round(margin_pct, 2)
                            result.margin_health = health
                            result.target_margin = target_margin * 100

                        results.append(result)
            except FileNotFoundError:
                print(f"Error: Batch file '{args.batch}' not found.", file=sys.stderr)
                sys.exit(1)
            except (ValueError, KeyError) as e:
                print(f"Error parsing batch file: {e}", file=sys.stderr)
                sys.exit(1)


        # Format output
        if args.output == "table":
            print(OutputFormatter.format_console_table(results))
        elif args.output == "csv":
            print(OutputFormatter.format_csv(results))
        elif args.output == "json":
            print(OutputFormatter.format_json(results))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
