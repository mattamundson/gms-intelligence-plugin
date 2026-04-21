#!/usr/bin/env python3
"""
validate_pricing.py - GMS Pricing Validation Engine

Validates pricing consistency across product families against GMS pricing rules.
Detects gauge, length, and finish inconsistencies with configurable tolerances.

Usage:
    python validate_pricing.py products.csv --output json
    python validate_pricing.py products.json --output table --tolerance 0.07
    python validate_pricing.py data.csv --output csv > report.csv
"""

import argparse
import csv
import json
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ValidationIssue:
    """Represents a single validation issue."""
    severity: str  # ERROR, WARNING, INFO
    issue_type: str  # gauge, length, finish, margin
    product_id: str
    message: str
    expected: Optional[float] = None
    actual: Optional[float] = None


class PricingValidator:
    """Validates GMS pricing consistency across products."""

    # GMS pricing multipliers
    GAUGE_MULTIPLIERS = {
        "29ga": 1.0,
        "26ga": 1.2,
        "24ga": 1.44,
    }

    LENGTH_MULTIPLIERS = {
        "10": 1.0,
        "12": 1.2,
        "14": 1.4,
        "16": 1.6,
        "18": 1.8,
    }

    FINISH_MULTIPLIERS = {
        "standard": 1.0,
        "MCC": 1.08,
        "CR": 1.15,
        "ULG": 1.15,
    }

    # Target margins by category
    DEFAULT_TARGET_MARGINS = {
        "trim": 0.50,
        "ef_panel": 0.35,
        "hf_panel": 0.40,
        "coil": 0.35,
        "accessory": 0.40,
    }

    # Exposed fastener panels
    EF_PANEL_FAMILIES = {"A9", "A6", "PRO"}

    # Hidden fastener panels
    HF_PANEL_FAMILIES = {"SSQ550", "SSQ675", "FF100", "BBQ750"}

    def __init__(
        self,
        gauge_tolerance: float = 0.05,
        length_tolerance: float = 0.05,
        finish_tolerance: float = 0.03,
        target_margins: Optional[Dict[str, float]] = None,
    ):
        """
        Initialize the pricing validator.

        Args:
            gauge_tolerance: Tolerance for gauge ratio check (default 5%)
            length_tolerance: Tolerance for length ratio check (default 5%)
            finish_tolerance: Tolerance for finish ratio check (default 3%)
            target_margins: Override default target margins by category
        """
        self.gauge_tolerance = gauge_tolerance
        self.length_tolerance = length_tolerance
        self.finish_tolerance = finish_tolerance
        self.target_margins = self.DEFAULT_TARGET_MARGINS.copy()
        if target_margins:
            self.target_margins.update(target_margins)

        self.issues: List[ValidationIssue] = []
        self.products: Dict[str, Dict[str, Any]] = {}
        self.families: Dict[str, List[str]] = defaultdict(list)

    def load_data(self, filepath: str) -> None:
        """
        Load product data from CSV or JSON.

        Args:
            filepath: Path to CSV or JSON file

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        if path.suffix.lower() == ".json":
            self._load_json(path)
        elif path.suffix.lower() == ".csv":
            self._load_csv(path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")

    def _load_json(self, path: Path) -> None:
        """Load data from JSON file."""
        try:
            with open(path, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

        if not isinstance(data, list):
            raise ValueError("JSON must contain an array of objects")

        for item in data:
            if not isinstance(item, dict):
                raise ValueError("JSON items must be objects")
            self._add_product(item)

    def _load_csv(self, path: Path) -> None:
        """Load data from CSV file."""
        try:
            with open(path, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row:
                        self._add_product(row)
        except Exception as e:
            raise ValueError(f"Error reading CSV: {e}")

    def _add_product(self, row: Dict[str, Any]) -> None:
        """Add a product from a data row."""
        product_id = row.get("product_id", "").strip()
        if not product_id:
            return

        sell_price_str = row.get("sell_price", "")
        if not sell_price_str:
            return

        try:
            sell_price = float(sell_price_str)
        except ValueError:
            return

        product_data = {"product_id": product_id, "sell_price": sell_price}

        cost_str = row.get("cost", "")
        if cost_str:
            try:
                product_data["cost"] = float(cost_str)
            except ValueError:
                pass

        self.products[product_id] = product_data

        # Extract family from product ID (prefix before first digit or hyphen)
        family = self._extract_family(product_id)
        self.families[family].append(product_id)

    def _extract_family(self, product_id: str) -> str:
        """
        Extract product family from product ID.

        Examples:
            "CO4129ARW" -> "CO"
            "CRD10-12-MCC" -> "CRD"
            "A9-12-GRE" -> "A9"
        """
        # Remove hyphens temporarily to find the prefix
        clean_id = product_id.replace("-", "")

        # Find first digit
        for i, char in enumerate(clean_id):
            if char.isdigit():
                return product_id[: max(1, i)]  # Ensure at least 1 char

        # If no digits found, return first 2 chars or whole ID
        return product_id[:2] if len(product_id) >= 2 else product_id

    def _parse_product_attrs(self, product_id: str) -> Dict[str, Any]:
        """
        Parse product attributes from ID.

        Returns dict with: gauge, length, finish, category
        """
        attrs = {
            "gauge": None,
            "length": None,
            "finish": "standard",
            "category": self._classify_product(product_id),
        }

        # Extract gauge (29ga, 26ga, 24ga patterns)
        for gauge_key in ["29ga", "26ga", "24ga"]:
            if gauge_key in product_id.lower():
                attrs["gauge"] = gauge_key
                break

        # Extract length (10, 12, 14, 16, 18 followed by quote or hyphen or end)
        for length_key in ["10", "12", "14", "16", "18"]:
            if length_key in product_id:
                # Simple check: if the length appears, mark it
                # More sophisticated parsing would check context
                attrs["length"] = length_key
                break

        # Extract finish (MCC, CR, ULG in color portion after gauge digit)
        # Premium finishes appear after gauge digit in the color portion
        color_portion = product_id.split("-")[-1] if "-" in product_id else product_id

        # Check if premium finish markers appear in color portion
        # (not in profile prefix like CRDF, CRRC, CRD)
        if "MCC" in product_id and not product_id.startswith(("CRDF", "CRRC", "CRD")):
            attrs["finish"] = "MCC"
        elif "CR" in product_id and not product_id.startswith(("CRDF", "CRRC", "CRD")):
            # Need to check it's not part of profile prefix
            profile_prefixes = {"CRDF", "CRRC", "CRD"}
            is_profile = any(product_id.startswith(p) for p in profile_prefixes)
            if not is_profile:
                attrs["finish"] = "CR"
        elif "ULG" in product_id:
            attrs["finish"] = "ULG"

        return attrs

    def _classify_product(self, product_id: str) -> str:
        """Classify product category."""
        family = self._extract_family(product_id)

        if family.startswith("CO"):
            return "coil"
        elif family in self.EF_PANEL_FAMILIES:
            return "ef_panel"
        elif family in self.HF_PANEL_FAMILIES:
            return "hf_panel"
        elif any(x in product_id.upper() for x in ["TRIM", "TRM", "ED", "CLOSURE"]):
            return "trim"
        else:
            return "trim"  # Default to trim

    def validate(self) -> None:
        """Run all validation checks."""
        self.issues.clear()

        # Validate within families
        for family, product_ids in self.families.items():
            if len(product_ids) < 2:
                continue

            self._validate_family_gauge_consistency(family, product_ids)
            self._validate_family_length_consistency(family, product_ids)
            self._validate_family_finish_consistency(family, product_ids)

        # Validate margin health if cost is available
        self._validate_margin_health()

    def _validate_family_gauge_consistency(self, family: str, product_ids: List[str]) -> None:
        """Check gauge pricing consistency within a family."""
        gauge_groups: Dict[str, List[Tuple[str, float]]] = defaultdict(list)

        for product_id in product_ids:
            attrs = self._parse_product_attrs(product_id)
            gauge = attrs.get("gauge")
            if not gauge:
                continue

            sell_price = self.products[product_id]["sell_price"]
            gauge_groups[gauge].append((product_id, sell_price))

        # Compare gauges
        if "29ga" in gauge_groups and "26ga" in gauge_groups:
            base_prices = [p for _, p in gauge_groups["29ga"]]
            compare_prices = [p for _, p in gauge_groups["26ga"]]

            if base_prices and compare_prices:
                avg_base = sum(base_prices) / len(base_prices)
                avg_compare = sum(compare_prices) / len(compare_prices)

                if avg_base > 0:
                    ratio = avg_compare / avg_base
                    expected = 1.2
                    tolerance_margin = self.gauge_tolerance

                    if abs(ratio - expected) > tolerance_margin:
                        self.issues.append(
                            ValidationIssue(
                                severity="WARNING",
                                issue_type="gauge",
                                product_id=family,
                                message=(
                                    f"Family {family}: 26ga/29ga ratio is {ratio:.3f}, "
                                    f"expected {expected:.3f} (tolerance ±{tolerance_margin:.1%})"
                                ),
                                expected=expected,
                                actual=ratio,
                            )
                        )

    def _validate_family_length_consistency(self, family: str, product_ids: List[str]) -> None:
        """Check length pricing consistency within a family."""
        length_groups: Dict[str, List[Tuple[str, float]]] = defaultdict(list)

        for product_id in product_ids:
            attrs = self._parse_product_attrs(product_id)
            length = attrs.get("length")
            if not length:
                continue

            sell_price = self.products[product_id]["sell_price"]
            length_groups[length].append((product_id, sell_price))

        # Compare 10' vs 12'
        if "10" in length_groups and "12" in length_groups:
            base_prices = [p for _, p in length_groups["10"]]
            compare_prices = [p for _, p in length_groups["12"]]

            if base_prices and compare_prices:
                avg_base = sum(base_prices) / len(base_prices)
                avg_compare = sum(compare_prices) / len(compare_prices)

                if avg_base > 0:
                    ratio = avg_compare / avg_base
                    expected = 1.2
                    tolerance_margin = self.length_tolerance

                    if abs(ratio - expected) > tolerance_margin:
                        self.issues.append(
                            ValidationIssue(
                                severity="WARNING",
                                issue_type="length",
                                product_id=family,
                                message=(
                                    f"Family {family}: 12'/10' ratio is {ratio:.3f}, "
                                    f"expected {expected:.3f} (tolerance ±{tolerance_margin:.1%})"
                                ),
                                expected=expected,
                                actual=ratio,
                            )
                        )

    def _validate_family_finish_consistency(self, family: str, product_ids: List[str]) -> None:
        """Check finish pricing consistency within a family."""
        finish_groups: Dict[str, List[Tuple[str, float]]] = defaultdict(list)

        for product_id in product_ids:
            attrs = self._parse_product_attrs(product_id)
            finish = attrs.get("finish", "standard")
            sell_price = self.products[product_id]["sell_price"]
            finish_groups[finish].append((product_id, sell_price))

        # Compare finishes
        if "standard" in finish_groups:
            base_prices = [p for _, p in finish_groups["standard"]]
            if not base_prices:
                return

            avg_base = sum(base_prices) / len(base_prices)
            if avg_base <= 0:
                return

            for finish in ["MCC", "CR", "ULG"]:
                if finish in finish_groups:
                    compare_prices = [p for _, p in finish_groups[finish]]
                    avg_compare = sum(compare_prices) / len(compare_prices)

                    ratio = avg_compare / avg_base
                    expected = self.FINISH_MULTIPLIERS.get(finish, 1.0)
                    tolerance_margin = self.finish_tolerance

                    if abs(ratio - expected) > tolerance_margin:
                        self.issues.append(
                            ValidationIssue(
                                severity="WARNING",
                                issue_type="finish",
                                product_id=family,
                                message=(
                                    f"Family {family}: {finish}/standard ratio is {ratio:.3f}, "
                                    f"expected {expected:.3f} (tolerance ±{tolerance_margin:.1%})"
                                ),
                                expected=expected,
                                actual=ratio,
                            )
                        )

    def _validate_margin_health(self) -> None:
        """Check margin health for products with cost data."""
        for product_id, product_data in self.products.items():
            if "cost" not in product_data:
                continue

            sell_price = product_data["sell_price"]
            cost = product_data["cost"]

            if sell_price <= 0 or cost < 0:
                continue

            margin = (sell_price - cost) / sell_price if sell_price > 0 else 0
            attrs = self._parse_product_attrs(product_id)
            category = attrs["category"]
            target = self.target_margins.get(category, 0.35)

            if margin < 0.25:
                severity = "ERROR"
                message = (
                    f"{product_id}: margin {margin:.1%} is CRITICAL "
                    f"(target {target:.0%})"
                )
            elif margin < target:
                severity = "WARNING"
                message = (
                    f"{product_id}: margin {margin:.1%} below target "
                    f"{target:.0%} ({category})"
                )
            else:
                continue

            self.issues.append(
                ValidationIssue(
                    severity=severity,
                    issue_type="margin",
                    product_id=product_id,
                    message=message,
                    actual=margin,
                    expected=target,
                )
            )

    def get_summary(self) -> Dict[str, Any]:
        """Get validation summary."""
        issues_by_severity = defaultdict(int)
        issues_by_type = defaultdict(int)

        for issue in self.issues:
            issues_by_severity[issue.severity] += 1
            issues_by_type[issue.issue_type] += 1

        return {
            "total_products_checked": len(self.products),
            "total_families_checked": len(self.families),
            "total_issues_found": len(self.issues),
            "issues_by_severity": dict(issues_by_severity),
            "issues_by_type": dict(issues_by_type),
        }

    def get_family_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get summary by family."""
        family_issues = defaultdict(list)
        for issue in self.issues:
            family_issues[issue.product_id].append(issue)

        summary = {}
        for family, product_ids in self.families.items():
            family_issue_list = family_issues.get(family, [])
            summary[family] = {
                "product_count": len(product_ids),
                "issue_count": len(family_issue_list),
                "issues": [
                    {
                        "severity": i.severity,
                        "type": i.issue_type,
                        "message": i.message,
                    }
                    for i in family_issue_list
                ],
            }

        return summary


def format_table_output(validator: PricingValidator) -> str:
    """Format validation results as ASCII table."""
    lines = []

    summary = validator.get_summary()
    lines.append("\n" + "=" * 80)
    lines.append("GMS PRICING VALIDATION REPORT")
    lines.append("=" * 80)
    lines.append(f"Products checked:  {summary['total_products_checked']}")
    lines.append(f"Families checked:  {summary['total_families_checked']}")
    lines.append(f"Total issues:      {summary['total_issues_found']}")

    if summary["total_issues_found"] > 0:
        lines.append("\nIssues by severity:")
        for severity, count in sorted(summary["issues_by_severity"].items()):
            lines.append(f"  {severity}: {count}")

        lines.append("\nIssues by type:")
        for issue_type, count in sorted(summary["issues_by_type"].items()):
            lines.append(f"  {issue_type}: {count}")

        lines.append("\n" + "-" * 80)
        lines.append("ISSUES BY FAMILY")
        lines.append("-" * 80)

        family_summary = validator.get_family_summary()
        for family in sorted(family_summary.keys()):
            info = family_summary[family]
            if info["issue_count"] > 0:
                lines.append(f"\n{family} ({info['product_count']} products)")
                for issue in info["issues"]:
                    lines.append(f"  [{issue['severity']}] {issue['type']}: {issue['message']}")

    lines.append("\n" + "=" * 80)
    return "\n".join(lines)


def format_csv_output(validator: PricingValidator) -> str:
    """Format validation results as CSV."""
    lines = []
    lines.append("severity,issue_type,product_id,message,expected,actual")

    for issue in validator.issues:
        expected_str = f"{issue.expected:.4f}" if issue.expected is not None else ""
        actual_str = f"{issue.actual:.4f}" if issue.actual is not None else ""

        # Escape quotes in message
        message = issue.message.replace('"', '""')

        lines.append(
            f'{issue.severity},{issue.issue_type},"{issue.product_id}",'
            f'"{message}",{expected_str},{actual_str}'
        )

    return "\n".join(lines)


def format_json_output(validator: PricingValidator) -> str:
    """Format validation results as JSON."""
    summary = validator.get_summary()
    family_summary = validator.get_family_summary()

    data = {
        "summary": summary,
        "families": family_summary,
        "issues": [
            {
                "severity": issue.severity,
                "type": issue.issue_type,
                "product_id": issue.product_id,
                "message": issue.message,
                "expected": issue.expected,
                "actual": issue.actual,
            }
            for issue in validator.issues
        ],
    }

    return json.dumps(data, indent=2)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate GMS pricing consistency across product families",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s products.csv
  %(prog)s products.json --output json
  %(prog)s data.csv --output csv > report.csv
  %(prog)s trim.json --gauge-tolerance 0.07 --length-tolerance 0.10
        """,
    )

    parser.add_argument("filepath", help="CSV or JSON file with product data")
    parser.add_argument(
        "--output",
        choices=["table", "csv", "json"],
        default="table",
        help="Output format (default: table)",
    )
    parser.add_argument(
        "--gauge-tolerance",
        type=float,
        default=0.05,
        help="Gauge ratio tolerance (default: 0.05)",
    )
    parser.add_argument(
        "--length-tolerance",
        type=float,
        default=0.05,
        help="Length ratio tolerance (default: 0.05)",
    )
    parser.add_argument(
        "--finish-tolerance",
        type=float,
        default=0.03,
        help="Finish ratio tolerance (default: 0.03)",
    )

    args = parser.parse_args()

    try:
        validator = PricingValidator(
            gauge_tolerance=args.gauge_tolerance,
            length_tolerance=args.length_tolerance,
            finish_tolerance=args.finish_tolerance,
        )

        validator.load_data(args.filepath)
        validator.validate()

        if args.output == "table":
            print(format_table_output(validator))
        elif args.output == "csv":
            print(format_csv_output(validator))
        elif args.output == "json":
            print(format_json_output(validator))

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
