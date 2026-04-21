#!/usr/bin/env python3
"""
margin_analyzer.py - GMS Margin Analysis Engine

Analyzes margin health across product portfolio with category classification
and revenue-at-risk calculation.

Usage:
    python margin_analyzer.py products.csv
    python margin_analyzer.py products.json --output json
    python margin_analyzer.py data.csv --target-margins trim=0.50,ef_panel=0.35
"""

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, median, stdev
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ProductMargin:
    """Represents margin analysis for a product."""
    product_id: str
    sell_price: float
    cost: float
    margin: float
    margin_pct: float
    category: str
    volume: Optional[int] = None
    revenue: Optional[float] = None
    margin_dollars: Optional[float] = None


class MarginAnalyzer:
    """Analyzes margin health across products with category classification."""

    # GMS product categories
    EF_PANEL_FAMILIES = {"A9", "A6", "PRO"}  # Exposed fastener
    HF_PANEL_FAMILIES = {"SSQ550", "SSQ675", "FF100", "BBQ750"}  # Hidden fastener

    DEFAULT_TARGET_MARGINS = {
        "trim": 0.50,
        "ef_panel": 0.35,
        "hf_panel": 0.40,
        "coil": 0.35,
        "accessory": 0.40,
    }

    def __init__(self, target_margins: Optional[Dict[str, float]] = None):
        """
        Initialize the margin analyzer.

        Args:
            target_margins: Override default target margins by category
        """
        self.target_margins = self.DEFAULT_TARGET_MARGINS.copy()
        if target_margins:
            self.target_margins.update(target_margins)

        self.products: List[ProductMargin] = []
        self.categories: Dict[str, List[ProductMargin]] = defaultdict(list)

    def load_data(self, filepath: str) -> None:
        """
        Load product data from CSV or JSON.

        Args:
            filepath: Path to CSV or JSON file

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid or cost is missing
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

        if not self.products:
            raise ValueError("No valid products loaded from file")

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

        cost_str = row.get("cost", "")
        if not cost_str:
            return

        try:
            sell_price = float(sell_price_str)
            cost = float(cost_str)
        except ValueError:
            return

        # Basic validation
        if sell_price <= 0 or cost < 0:
            return

        if cost > sell_price:
            # Skip negative margin products
            return

        # Calculate margin
        margin = sell_price - cost
        margin_pct = margin / sell_price if sell_price > 0 else 0

        # Extract volume if provided
        volume = None
        volume_str = row.get("volume", "")
        if volume_str:
            try:
                volume = int(volume_str)
            except ValueError:
                pass

        # Calculate revenue and margin dollars
        revenue = sell_price * volume if volume else None
        margin_dollars = margin * volume if volume else None

        # Classify product
        category = self._classify_product(product_id)

        product = ProductMargin(
            product_id=product_id,
            sell_price=sell_price,
            cost=cost,
            margin=margin,
            margin_pct=margin_pct,
            category=category,
            volume=volume,
            revenue=revenue,
            margin_dollars=margin_dollars,
        )

        self.products.append(product)
        self.categories[category].append(product)

    def _extract_family(self, product_id: str) -> str:
        """
        Extract product family from product ID.

        Examples:
            "CO4129ARW" -> "CO"
            "CRD10-12-MCC" -> "CRD"
            "A9-12-GRE" -> "A9"
        """
        clean_id = product_id.replace("-", "")

        for i, char in enumerate(clean_id):
            if char.isdigit():
                return product_id[: max(1, i)]

        return product_id[:2] if len(product_id) >= 2 else product_id

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

    def get_overall_stats(self) -> Dict[str, Any]:
        """Calculate overall margin statistics."""
        if not self.products:
            return {}

        margins = [p.margin_pct for p in self.products]

        return {
            "total_products": len(self.products),
            "min_margin": min(margins),
            "max_margin": max(margins),
            "mean_margin": mean(margins),
            "median_margin": median(margins),
            "std_dev_margin": stdev(margins) if len(margins) > 1 else 0.0,
        }

    def get_category_stats(self) -> Dict[str, Dict[str, Any]]:
        """Calculate statistics by category."""
        stats = {}

        for category in sorted(self.categories.keys()):
            products = self.categories[category]
            if not products:
                continue

            margins = [p.margin_pct for p in products]
            target = self.target_margins.get(category, 0.35)

            revenue_sum = sum(p.revenue for p in products if p.revenue)
            margin_dollars_sum = sum(p.margin_dollars for p in products if p.margin_dollars)

            below_target = sum(1 for p in products if p.margin_pct < target)
            red_flag = sum(1 for p in products if p.margin_pct < 0.25)

            stats[category] = {
                "product_count": len(products),
                "min_margin": min(margins),
                "max_margin": max(margins),
                "mean_margin": mean(margins),
                "median_margin": median(margins),
                "std_dev_margin": stdev(margins) if len(margins) > 1 else 0.0,
                "target_margin": target,
                "below_target_count": below_target,
                "red_flag_count": red_flag,
                "total_revenue": revenue_sum if revenue_sum else None,
                "total_margin_dollars": margin_dollars_sum if margin_dollars_sum else None,
            }

        return stats

    def get_below_target(self) -> List[ProductMargin]:
        """Get products below target margin, sorted by dollar impact."""
        below_target = []

        for product in self.products:
            target = self.target_margins.get(product.category, 0.35)
            if product.margin_pct < target:
                below_target.append(product)

        # Sort by margin dollars (if available) then by product_id
        def sort_key(p: ProductMargin) -> Tuple[float, str]:
            margin_dollars = p.margin_dollars if p.margin_dollars else 0
            return (-margin_dollars, p.product_id)

        below_target.sort(key=sort_key)
        return below_target

    def get_red_flag_products(self) -> List[ProductMargin]:
        """Get products in critical margin territory (<25%), sorted by price."""
        red_flag = [p for p in self.products if p.margin_pct < 0.25]
        red_flag.sort(key=lambda p: -p.sell_price)
        return red_flag

    def get_highest_margin(self, count: int = 10) -> List[ProductMargin]:
        """Get top N highest-margin products."""
        sorted_products = sorted(self.products, key=lambda p: -p.margin_pct)
        return sorted_products[:count]

    def get_lowest_margin(self, count: int = 10) -> List[ProductMargin]:
        """Get top N lowest-margin products."""
        sorted_products = sorted(self.products, key=lambda p: p.margin_pct)
        return sorted_products[:count]

    def get_revenue_at_risk(self) -> Dict[str, Any]:
        """
        Calculate revenue-at-risk analysis.

        Revenue at risk = products below target margin × their volume.
        """
        below_target = self.get_below_target()

        total_revenue_at_risk = 0
        products_with_volume = 0

        for product in below_target:
            if product.revenue:
                total_revenue_at_risk += product.revenue
                products_with_volume += 1

        potential_margin_improvement = 0
        for product in below_target:
            target = self.target_margins.get(product.category, 0.35)
            if product.volume and product.margin_pct < target:
                # Calculate potential gain if margin reached target
                target_margin_dollars = product.sell_price * target * product.volume
                current_margin_dollars = product.margin_dollars if product.margin_dollars else 0
                potential_gain = target_margin_dollars - current_margin_dollars
                potential_margin_improvement += max(0, potential_gain)

        return {
            "products_below_target": len(below_target),
            "products_with_volume": products_with_volume,
            "total_revenue_at_risk": total_revenue_at_risk if total_revenue_at_risk else None,
            "potential_margin_improvement": (
                potential_margin_improvement if potential_margin_improvement else None
            ),
        }


def format_table_output(analyzer: MarginAnalyzer) -> str:
    """Format analysis results as ASCII table."""
    lines = []

    overall = analyzer.get_overall_stats()
    lines.append("\n" + "=" * 90)
    lines.append("GMS MARGIN ANALYSIS REPORT")
    lines.append("=" * 90)

    if overall:
        lines.append(f"\nOVERALL STATISTICS")
        lines.append("-" * 90)
        lines.append(f"  Total products:      {overall['total_products']}")
        lines.append(f"  Min margin:          {overall['min_margin']:>7.1%}")
        lines.append(f"  Max margin:          {overall['max_margin']:>7.1%}")
        lines.append(f"  Mean margin:         {overall['mean_margin']:>7.1%}")
        lines.append(f"  Median margin:       {overall['median_margin']:>7.1%}")
        lines.append(f"  Std Dev:             {overall['std_dev_margin']:>7.1%}")

    category_stats = analyzer.get_category_stats()
    if category_stats:
        lines.append(f"\nMARGIN BY CATEGORY")
        lines.append("-" * 90)
        lines.append(
            f"{'Category':<15} {'Count':>6} {'Min':>8} {'Mean':>8} {'Median':>8} "
            f"{'Target':>8} {'Below':>6} {'Red Flag':>9}"
        )
        lines.append("-" * 90)

        for category in sorted(category_stats.keys()):
            stats = category_stats[category]
            lines.append(
                f"{category:<15} {stats['product_count']:>6} "
                f"{stats['min_margin']:>7.1%} {stats['mean_margin']:>7.1%} "
                f"{stats['median_margin']:>7.1%} {stats['target_margin']:>7.1%} "
                f"{stats['below_target_count']:>6} {stats['red_flag_count']:>9}"
            )

    red_flag = analyzer.get_red_flag_products()
    if red_flag:
        lines.append(f"\nRED FLAG PRODUCTS (margin < 25%)")
        lines.append("-" * 90)
        lines.append(f"{'Product ID':<20} {'Price':>10} {'Cost':>10} {'Margin':>10} {'Category':<12}")
        lines.append("-" * 90)

        for product in red_flag[:20]:  # Limit to 20 for display
            lines.append(
                f"{product.product_id:<20} ${product.sell_price:>9.2f} "
                f"${product.cost:>9.2f} {product.margin_pct:>9.1%} {product.category:<12}"
            )

        if len(red_flag) > 20:
            lines.append(f"... and {len(red_flag) - 20} more")

    below_target = analyzer.get_below_target()
    if below_target:
        lines.append(f"\nBELOW TARGET PRODUCTS (sorted by revenue at risk)")
        lines.append("-" * 90)

        # Show products with volume first, then without
        with_volume = [p for p in below_target if p.volume]
        without_volume = [p for p in below_target if not p.volume]

        if with_volume:
            lines.append(f"{'Product ID':<20} {'Margin':>8} {'Target':>8} {'Volume':>8} "
                         f"{'Revenue':>12} {'At Risk':>12} {'Category':<12}")
            lines.append("-" * 90)

            for product in with_volume[:15]:
                target = analyzer.target_margins.get(product.category, 0.35)
                lines.append(
                    f"{product.product_id:<20} {product.margin_pct:>7.1%} "
                    f"{target:>7.1%} {product.volume:>8} "
                    f"${product.revenue:>11.2f} ${product.revenue:>11.2f} {product.category:<12}"
                )

            if len(with_volume) > 15:
                lines.append(f"... and {len(with_volume) - 15} more with volume data")

        if without_volume:
            lines.append(
                f"\nProducts below target WITHOUT volume data ({len(without_volume)} total):"
            )
            for product in without_volume[:10]:
                target = analyzer.target_margins.get(product.category, 0.35)
                lines.append(
                    f"  {product.product_id:<20} {product.margin_pct:>7.1%} "
                    f"(target {target:.0%}) - {product.category}"
                )

            if len(without_volume) > 10:
                lines.append(f"  ... and {len(without_volume) - 10} more")

    highest = analyzer.get_highest_margin(10)
    if highest:
        lines.append(f"\nTOP 10 HIGHEST MARGIN PRODUCTS")
        lines.append("-" * 90)
        lines.append(f"{'Product ID':<20} {'Margin':>8} {'Price':>10} {'Cost':>10} {'Category':<12}")
        lines.append("-" * 90)

        for product in highest:
            lines.append(
                f"{product.product_id:<20} {product.margin_pct:>7.1%} "
                f"${product.sell_price:>9.2f} ${product.cost:>9.2f} {product.category:<12}"
            )

    lowest = analyzer.get_lowest_margin(10)
    if lowest:
        lines.append(f"\nTOP 10 LOWEST MARGIN PRODUCTS")
        lines.append("-" * 90)
        lines.append(f"{'Product ID':<20} {'Margin':>8} {'Price':>10} {'Cost':>10} {'Category':<12}")
        lines.append("-" * 90)

        for product in lowest:
            lines.append(
                f"{product.product_id:<20} {product.margin_pct:>7.1%} "
                f"${product.sell_price:>9.2f} ${product.cost:>9.2f} {product.category:<12}"
            )

    revenue_at_risk = analyzer.get_revenue_at_risk()
    if revenue_at_risk["products_below_target"] > 0:
        lines.append(f"\nREVENUE-AT-RISK ANALYSIS")
        lines.append("-" * 90)
        lines.append(f"  Products below target:  {revenue_at_risk['products_below_target']}")
        lines.append(f"  With volume data:       {revenue_at_risk['products_with_volume']}")

        if revenue_at_risk["total_revenue_at_risk"]:
            lines.append(
                f"  Total revenue at risk:  ${revenue_at_risk['total_revenue_at_risk']:>10,.2f}"
            )

        if revenue_at_risk["potential_margin_improvement"]:
            lines.append(
                f"  Potential improvement: ${revenue_at_risk['potential_margin_improvement']:>10,.2f}"
            )

    lines.append("\n" + "=" * 90)
    return "\n".join(lines)


def format_csv_output(analyzer: MarginAnalyzer) -> str:
    """Format analysis results as CSV."""
    lines = []

    # Summary section as comments
    lines.append("# GMS Margin Analysis - Product Detail")
    lines.append("# " + "=" * 80)

    overall = analyzer.get_overall_stats()
    if overall:
        lines.append(f"# Total Products: {overall['total_products']}")
        lines.append(f"# Mean Margin: {overall['mean_margin']:.1%}")
        lines.append(f"# Median Margin: {overall['median_margin']:.1%}")

    lines.append("#")
    lines.append("product_id,category,sell_price,cost,margin_pct,volume,revenue,margin_dollars")

    for product in sorted(analyzer.products, key=lambda p: (-p.margin_pct, p.product_id)):
        volume_str = str(product.volume) if product.volume else ""
        revenue_str = f"{product.revenue:.2f}" if product.revenue else ""
        margin_dollars_str = f"{product.margin_dollars:.2f}" if product.margin_dollars else ""

        lines.append(
            f"{product.product_id},{product.category},{product.sell_price:.2f},"
            f"{product.cost:.2f},{product.margin_pct:.4f},{volume_str},{revenue_str},"
            f"{margin_dollars_str}"
        )

    return "\n".join(lines)


def format_json_output(analyzer: MarginAnalyzer) -> str:
    """Format analysis results as JSON."""
    overall = analyzer.get_overall_stats()
    category_stats = analyzer.get_category_stats()
    red_flag = analyzer.get_red_flag_products()
    below_target = analyzer.get_below_target()
    highest = analyzer.get_highest_margin(10)
    lowest = analyzer.get_lowest_margin(10)
    revenue_at_risk = analyzer.get_revenue_at_risk()

    def product_to_dict(p: ProductMargin) -> Dict[str, Any]:
        return {
            "product_id": p.product_id,
            "category": p.category,
            "sell_price": p.sell_price,
            "cost": p.cost,
            "margin_pct": p.margin_pct,
            "volume": p.volume,
            "revenue": p.revenue,
            "margin_dollars": p.margin_dollars,
        }

    data = {
        "overall_statistics": overall,
        "category_statistics": category_stats,
        "red_flag_products": [product_to_dict(p) for p in red_flag],
        "below_target_products": [product_to_dict(p) for p in below_target[:50]],
        "highest_margin_products": [product_to_dict(p) for p in highest],
        "lowest_margin_products": [product_to_dict(p) for p in lowest],
        "revenue_at_risk_analysis": revenue_at_risk,
    }

    return json.dumps(data, indent=2)


def parse_target_margins(margin_str: str) -> Dict[str, float]:
    """Parse target margins from command-line argument."""
    target_margins = {}

    if not margin_str:
        return target_margins

    pairs = margin_str.split(",")
    for pair in pairs:
        pair = pair.strip()
        if "=" not in pair:
            raise ValueError(f"Invalid margin format: {pair}")

        category, value = pair.split("=", 1)
        category = category.strip()
        value = value.strip()

        try:
            target_margins[category] = float(value)
        except ValueError:
            raise ValueError(f"Invalid margin value for {category}: {value}")

    return target_margins


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze GMS margin health with category classification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s products.csv
  %(prog)s products.json --output json
  %(prog)s data.csv --output csv > report.csv
  %(prog)s trim.json --target-margins trim=0.50,ef_panel=0.35,hf_panel=0.40

Required columns:
  product_id, sell_price, cost
  (optional: volume)
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
        "--target-margins",
        help=(
            "Override target margins (comma-separated key=value pairs). "
            "Example: trim=0.50,ef_panel=0.35,hf_panel=0.40"
        ),
    )

    args = parser.parse_args()

    try:
        # Parse target margins if provided
        target_margins = None
        if args.target_margins:
            target_margins = parse_target_margins(args.target_margins)

        analyzer = MarginAnalyzer(target_margins=target_margins)
        analyzer.load_data(args.filepath)

        if args.output == "table":
            print(format_table_output(analyzer))
        elif args.output == "csv":
            print(format_csv_output(analyzer))
        elif args.output == "json":
            print(format_json_output(analyzer))

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
