#!/usr/bin/env python3
"""
GMS SKU Encoder - Generate valid Greenfield Metal Sales Product IDs from plain English descriptions.

This script takes product descriptions like "Ridge Cap, 26ga, Charcoal Gray, 12ft"
and outputs a valid PID, with verification through decoding.

No external dependencies required - runs standalone with Python 3.6+

Usage:
    python sku_encoder.py "Ridge Cap, 26ga, Charcoal Gray, 12ft"
    python sku_encoder.py "SSQ 550 Panel, 29ga, Arctic White"
    python sku_encoder.py --batch descriptions.txt
    python sku_encoder.py --color-map (show all color mappings)
    python sku_encoder.py --families (show all product families)
"""

import argparse
import sys
import re
from typing import Dict, Optional, List, Tuple, Any


# ============================================================================
# COMPREHENSIVE FAMILY REGISTRY
# ============================================================================

FAMILY_REGISTRY = {
    # Product families with aliases for fuzzy matching
    "ANGLE": ("ANG11", "Angle 1x1"),
    "ANGLE11": ("ANG11", "Angle 1x1"),
    "ANGLE1X1": ("ANG11", "Angle 1x1"),
    "ANGLE22": ("ANG22", "Angle 2x2"),
    "ANGLE2X2": ("ANG22", "Angle 2x2"),

    "BASICTRIM": ("BT", "Base Trim"),
    "BASETRIM": ("BT", "Base Trim"),
    "BASE": ("BT", "Base Trim"),

    "BOARD": ("BB", "Board & Batten"),
    "BOARDBATTEN": ("BB", "Board & Batten"),
    "BOARDANDBATTEN": ("BB", "Board & Batten"),

    "BOARDBATTENPANEL": ("BBQ750", "Board & Batten Panel"),
    "BOARDBATTENPANEL750": ("BBQ750", "Board & Batten Panel"),
    "BBQ": ("BBQ750", "Board & Batten Panel"),
    "BBQ750": ("BBQ750", "Board & Batten Panel"),

    "CROWNDRIP": ("CRD81", "Crown Drip 8x1"),
    "CROWNDRIP81": ("CRD81", "Crown Drip 8x1"),
    "CRD81": ("CRD81", "Crown Drip 8x1"),
    "CROWNDRIP1011": ("CRD1011", "Crown Drip 10x11"),
    "CRD1011": ("CRD1011", "Crown Drip 10x11"),
    "CROWNDRIP10X11": ("CRD1011", "Crown Drip 10x11"),
    "CROWNDRIP8X1": ("CRD81", "Crown Drip 8x1"),

    "CROWNDRIPPFLAT": ("CRDF", "Crown Drip Flat"),
    "CRDF": ("CRDF", "Crown Drip Flat"),

    "CURVEDRIDGECAP": ("CRRC", "Curved Ridge Cap"),
    "CRRC": ("CRRC", "Curved Ridge Cap"),

    "CORRUGATED": ("CCF", "Corrugated Cap Flat"),
    "CORRUGATEDCAP": ("CCF", "Corrugated Cap Flat"),
    "CCF": ("CCF", "Corrugated Cap Flat"),

    "DOOREDGE": ("DE", "Door Edge Trim"),
    "DOOREDGETRIM": ("DE", "Door Edge Trim"),
    "DRIPEDGE": ("DE", "Drip Edge"),
    "DRIP": ("DE", "Drip Edge"),
    "DE": ("DE", "Drip Edge"),

    "DOORFRAME": ("DF", "Door Frame"),
    "DOORFRAMEMETAL": ("DF", "Door Frame"),

    "DOORJAM": ("DJT", "Door Jam Trim"),
    "DOORJAMTRIM": ("DJT", "Door Jam Trim"),

    "EDGETRIM": ("ET", "Edge Trim"),
    "ET": ("ET", "Edge Trim"),
    "EDGETRIM4": ("ET4", "Edge Trim 4 inch"),
    "ET4": ("ET4", "Edge Trim 4 inch"),
    "EDGETRIM5": ("ET5", "Edge Trim 5 inch"),
    "ET5": ("ET5", "Edge Trim 5 inch"),

    "EDGEWELD": ("EW", "Edge Weld"),

    "FACEANGLE": ("FA", "Face Angle"),

    "FACECHANNEL": ("FCH", "Face Channel"),
    "FACECHANNELJAMB": ("FCJ", "Face Channel Jamb"),

    "FLUSHFLAT": ("FF100", "Flush Flat Panel"),
    "FLUSHFLAT100": ("FF100", "Flush Flat Panel"),
    "FF100": ("FF100", "Flush Flat Panel"),

    "GABLEANGLE": ("GA", "Gable Angle"),

    "GUTTER": ("GT", "Gutter Trim"),
    "GUTTERFLASHING": ("GF", "Gutter Flashing"),
    "GUTTERCAP": ("GT", "Gutter Trim"),

    "HFBT": ("HFBT", "HF Base Trim"),
    "HIDDENFFASTENERBASETR": ("HFBT", "HF Base Trim"),
    "HF": ("HFBT", "HF Base Trim"),

    "HFDOORFRAME": ("HFDF", "HF Door Frame"),
    "HFDF": ("HFDF", "HF Door Frame"),

    "HFJAMB": ("HFJT", "HF Jamb Trim"),
    "HFJAMBTRIM": ("HFJT", "HF Jamb Trim"),
    "HFJT": ("HFJT", "HF Jamb Trim"),

    "HFRIDGE": ("HFRG", "HF Ridge Gap"),
    "HFRIDGEGAP": ("HFRG", "HF Ridge Gap"),
    "HFRG": ("HFRG", "HF Ridge Gap"),

    "HFSIDEFLASH": ("HFSF", "HF Side Flashing"),
    "HFSF": ("HFSF", "HF Side Flashing"),

    "HFTOPFLASH": ("HFTF", "HF Top Flashing"),
    "HFTF": ("HFTF", "HF Top Flashing"),

    "HFVALLEYFLASH": ("HFVF", "HF Valley Flashing"),
    "HFVF": ("HFVF", "HF Valley Flashing"),

    "JC": ("JC", "J Channel"),
    "JCHANNEL": ("JC", "J Channel"),

    "JCHEAVY": ("JCH", "J Channel Heavy"),
    "JCH": ("JCH", "J Channel Heavy"),

    "JAMB": ("JT", "Jamb Trim"),
    "JAMBTRIM": ("JT", "Jamb Trim"),

    "KNOCKOUTTRIM": ("KOT", "Knock Out Trim"),
    "KOT": ("KOT", "Knock Out Trim"),

    "METALSTUD": ("MET3", "Metal Stud 3 inch"),
    "MET3": ("MET3", "Metal Stud 3 inch"),

    "OUTSIDECORNER": ("OC", "Outside Corner"),
    "OUTERCORNER": ("OC", "Outside Corner"),

    "OVERHEADDOOR": ("ODHC", "Overhead Door Header Channel"),
    "ODHC": ("ODHC", "Overhead Door Header Channel"),

    "PITCHCHANGE": ("PCF", "Pitch Change Flashing"),
    "PITCHCHANGEFLASHING": ("PCF", "Pitch Change Flashing"),
    "PCF": ("PCF", "Pitch Change Flashing"),

    "PANEL": ("PRO", "Pro Panel"),
    "PROPANEL": ("PRO", "Pro Panel"),
    "PRO": ("PRO", "Pro Panel"),

    "PIGEONTREIM": ("PT", "Pigeon Trim"),
    "PT": ("PT", "Pigeon Trim"),

    "RIDGE": ("RC", "Ridge Cap Standard"),
    "RIDGECAP": ("RC", "Ridge Cap Standard"),
    "RIDGECAP10": ("RC10", "Ridge Cap 10 inch"),
    "RC10": ("RC10", "Ridge Cap 10 inch"),
    "RIDGECAP14": ("RC14", "Ridge Cap 14 inch"),
    "RC14": ("RC14", "Ridge Cap 14 inch"),
    "RIDGECAP20": ("RC20", "Ridge Cap 20 inch"),
    "RC20": ("RC20", "Ridge Cap 20 inch"),
    "RIDGECAP24": ("RC24", "Ridge Cap 24 inch"),
    "RC24": ("RC24", "Ridge Cap 24 inch"),

    "RAKETRIM": ("RT", "Rake Trim"),
    "RAKE": ("RT", "Rake Trim"),

    "SIDELOOR": ("SDT7", "Side Door Trim 7 inch"),
    "SDT7": ("SDT7", "Side Door Trim 7 inch"),
    "SDT9": ("SDT9", "Side Door Trim 9 inch"),

    "SOFFIT": ("SI", "Soffit Insert"),
    "SOFFITINSERT": ("SI", "Soffit Insert"),

    "STANDINGSEAM": ("SSQ550", "Standing Seam Panel"),
    "SSQ": ("SSQ550", "Standing Seam Panel"),
    "SSQ550": ("SSQ550", "Standing Seam 550 Panel"),
    "SSQ575": ("SSQ550", "Standing Seam 550 Panel"),  # Alias
    "SSQ675": ("SSQ675", "Standing Seam 675 Panel"),

    "TRAPEZOID": ("TRAPEZOID", "Trapezoid Panel"),
    "TRAPEZOIDPANEL": ("TRAPEZOID", "Trapezoid Panel"),

    "VALLEY": ("VV", "Valley Valley"),
    "VALLEYVALLEY": ("VV", "Valley Valley"),

    "WATERVALLEY": ("WV", "Water Valley"),
    "WV": ("WV", "Water Valley"),

    "AGPANEL": ("A9", "Ag Panel 29ga"),
    "AG": ("A9", "Ag Panel 29ga"),
    "A9": ("A9", "Ag Panel 29ga"),

    "GREENFIELDCLASSIC": ("A6", "Greenfield Classic"),
    "A6": ("A6", "Greenfield Classic"),
}


# ============================================================================
# COLOR CODE REGISTRY - BIDIRECTIONAL
# ============================================================================

COLOR_NAME_TO_CODE = {
    # US Standard (29ga & 26ga)
    "ASH GRAY": "AG",
    "ASHGRAY": "AG",
    "ASH": "AG",
    "GRAY": "AG",
    "GREY": "AG",

    "ASH GRAY CRINKLE": "AGC",
    "ASHGRAYCRINKLE": "AGC",

    "ARCTIC WHITE": "ARW",
    "ARCTICWHITE": "ARW",
    "WHITE": "ARW",
    "ARCTIC": "ARW",

    "ARCTIC WHITE CRINKLE": "AWC",
    "ARCTICWHITECRINKLE": "AWC",

    "BLACK": "BK",
    "BK": "BK",

    "BLACK CRINKLE": "BKC",
    "BLACKCRINKLE": "BKC",

    "BLUE": "HB",  # Hawaiian Blue — B is Brown in GMS

    "BROWN": "BR",
    "BROWN CRINKLE": "BRC",
    "BROWNCRINKLE": "BRC",

    "CHARCOAL": "CH",
    "CHARCOALCRINKLE": "CHC",
    "CHARCOAL CRINKLE": "CHC",

    "CHARCOAL GRAY": "CG",
    "CHARCOALGRAY": "CG",

    "CHARCOAL GRAY CRINKLE": "CGC",
    "CHARCOALGRAYCRINKLE": "CGC",

    "DARK GRAY": "DG",
    "DARKGRAY": "DG",
    "DARK GREY": "DG",

    "DARK GRAY CRINKLE": "DGC",
    "DARKGRAYCRINKLE": "DGC",

    "DARK BRONZE": "DB",
    "DARKBRONZE": "DB",

    "DARK BRONZE CRINKLE": "DBC",
    "DARKBRONZECRINKLE": "DBC",

    "GREEN": "GR",

    "GREEN CRINKLE": "GRC",
    "GREENCRINKLE": "GRC",

    "GUNMETAL": "GN",

    "GUNMETAL CRINKLE": "GNC",
    "GUNMETALCRINKLE": "GNC",

    "MIDNIGHT": "MD",

    "MIDNIGHT CRINKLE": "MDC",
    "MIDNIGHTCRINKLE": "MDC",

    "MOSS GREEN": "MG",
    "MOSSGREEN": "MG",

    "MOSS GREEN CRINKLE": "MGC",
    "MOSSGREENCRINKLE": "MGC",

    "OYSTER WHITE": "OW",
    "OYSTERWHITE": "OW",

    "OYSTER WHITE CRINKLE": "OWC",
    "OYSTERWHITECRINKLE": "OWC",

    "RED": "RD",
    "RED CRINKLE": "RDC",

    "RUST": "RT",
    "RUST CRINKLE": "RTC",
    "RUSTCRINKLE": "RTC",

    "SLATE": "SL",
    "SLATE CRINKLE": "SLC",
    "SLATECRINKLE": "SLC",

    "STONE": "SN",
    "STONE CRINKLE": "SNC",
    "STONECRINKLE": "SNC",

    "TAN": "TN",
    "TAN CRINKLE": "TNC",
    "TANCRINKLE": "TNC",

    "MATTE BLACK": "MBB",
    "MATTEBLACK": "MBB",
    "MATTE CHARCOAL": "MCH",
    "MATTECHARCOAL": "MCH",
    "MATTE DARK GRAY": "MDG",
    "MATTEDARKGRAY": "MDG",
    "MATTE GUNMETAL": "MGN",
    "MATTEGUNMETAL": "MGN",
    "MATTE SLATE": "MBS",
    "MATTESLATE": "MBS",
    "MATTE BRONZE": "MBZ",
    "MATTEBRONZE": "MBZ",
    "MATTE WHITE": "MWH",
    "MATTEWHITE": "MWH",
    "MATTE MOSS GREEN": "MMG",
    "MATTMOSSGREEN": "MMG",
    "MATTE RED": "MRD",
    "MATTERD": "MRD",

    # CMG Standard (Kynar)
    "CMG ALUMINUM": "CMGALM",
    "CMG ASH GRAY": "CMGAG",
    "CMG ASH GREY": "CMGAG",
    "CMG BLACK": "CMGBK",
    "CMG BLUE": "CMGBL",
    "CMG BROWN": "CMGBR",
    "CMG CHARCOAL": "CMGCH",
    "CMG CORAL": "CMGCN",
    "CMG CHERRY RED": "CMGCR",
    "CMG DARK BROWN": "CMGDB",
    "CMG DARK GRAY": "CMGDG",
    "CMG DARK GREY": "CMGDG",
    "CMG FOREST GREEN": "CMGFR",
    "CMG GRAPHITE GRAY": "CMGGG",
    "CMG GREEN": "CMGGN",
    "CMG GRANITE": "CMGGR",
    "CMG GRAY": "CMGGY",
    "CMG GREY": "CMGGY",
    "CMG LIGHT GRAY": "CMGLG",
    "CMG LIGHT GREY": "CMGLG",
    "CMG MEDIUM BRONZE": "CMGMB",
    "CMG MOSS GREEN": "CMGMG",
    "CMG OLIVE": "CMGOV",
    "CMG PEARL WHITE": "CMGPW",
    "CMG RED": "CMGRD",
    "CMG RUST": "CMGRT",
    "CMG STONE": "CMGSN",
    "CMG TAN": "CMGTB",
    "CMG BUFF": "CMGTN",
    "CMG VINE GREEN": "CMGVG",
    "CMG WHITE": "CMGWH",
    "CMG WINE RED": "CMGWR",

    # CMG Crinkle
    "CMG CHARCOAL CRINKLE": "CMGCHC",
    "CMG BLACK CRINKLE": "CMGBKC",
    "CMG BROWN CRINKLE": "CMGBRC",

    # CMG ULG
    "CMG CHARCOAL ULG": "CMGCHM",
    "CMG BLACK ULG": "CMGBKM",
    "CMG BURGUNDY ULG": "CMGBURM",
}


GAUGE_NAME_TO_DIGIT = {
    "29GA": "9",
    "29": "9",
    "26GA": "6",
    "26": "6",
    "24GA": "4",
    "24": "4",
}

LENGTH_CODE_MAP = {
    "10": 10,
    "12": 12,
    "14": 14,
    "16": 16,
    "18": 18,
    "20": 20,
    "10FT": 10,
    "12FT": 12,
    "14FT": 14,
    "16FT": 16,
    "18FT": 18,
    "20FT": 20,
    "10FEET": 10,
    "12FEET": 12,
    "14FEET": 14,
    "16FEET": 16,
    "18FEET": 18,
    "20FEET": 20,
}


# ============================================================================
# FUZZY MATCHING
# ============================================================================

def fuzzy_match_family(description: str) -> Optional[Tuple[str, str]]:
    """
    Fuzzy match a family name from description.
    Returns: (family_code, family_name) or None
    """
    desc_clean = re.sub(r'\s+', '', description.upper())

    # Try exact match first
    if desc_clean in FAMILY_REGISTRY:
        code, name = FAMILY_REGISTRY[desc_clean]
        return code, name

    # Try substring matches (longest first)
    sorted_keys = sorted(FAMILY_REGISTRY.keys(), key=len, reverse=True)
    for key in sorted_keys:
        if key in desc_clean or desc_clean in key:
            code, name = FAMILY_REGISTRY[key]
            return code, name

    return None


def fuzzy_match_color(color_name: str) -> Optional[str]:
    """
    Fuzzy match a color name to color code.
    Returns: color_code or None
    """
    color_clean = re.sub(r'\s+', '', color_name.upper())

    # Try exact match
    if color_clean in COLOR_NAME_TO_CODE:
        return COLOR_NAME_TO_CODE[color_clean]

    # Try substring match (longest first)
    sorted_keys = sorted(COLOR_NAME_TO_CODE.keys(), key=len, reverse=True)
    for key in sorted_keys:
        if key in color_clean or color_clean in key:
            return COLOR_NAME_TO_CODE[key]

    return None


def fuzzy_match_gauge(gauge_str: str) -> Optional[str]:
    """
    Fuzzy match gauge string to digit.
    Returns: digit (9, 6, or 4) or None
    """
    gauge_clean = re.sub(r'\s+', '', gauge_str.upper())

    if gauge_clean in GAUGE_NAME_TO_DIGIT:
        return GAUGE_NAME_TO_DIGIT[gauge_clean]

    return None


# ============================================================================
# ENCODER
# ============================================================================

def encode_pid(description: str) -> Optional[Dict[str, Any]]:
    """
    Encode a description into a PID.
    Returns: dict with pid, valid, details, and error (if invalid)
    """
    # Parse the description (format: "Product, Gauge, Color, Length")
    parts = [p.strip() for p in description.split(",")]

    if not parts:
        return {
            "valid": False,
            "error": "Empty description",
        }

    # Extract components
    product_desc = parts[0] if len(parts) > 0 else ""
    gauge_str = parts[1] if len(parts) > 1 else ""
    color_str = parts[2] if len(parts) > 2 else ""
    length_str = parts[3] if len(parts) > 3 else ""

    # Fuzzy match family
    family_match = fuzzy_match_family(product_desc)
    if not family_match:
        return {
            "valid": False,
            "error": f"Could not identify product family: '{product_desc}'",
        }

    family_code, family_name = family_match

    # Fuzzy match gauge
    gauge_digit = fuzzy_match_gauge(gauge_str)
    if not gauge_digit:
        return {
            "valid": False,
            "error": f"Could not parse gauge: '{gauge_str}'",
        }

    # Fuzzy match color
    color_code = fuzzy_match_color(color_str)
    if not color_code:
        return {
            "valid": False,
            "error": f"Could not identify color: '{color_str}'",
        }

    # Check 24ga is CMG only
    if gauge_digit == "4" and not color_code.startswith("CMG"):
        return {
            "valid": False,
            "error": f"24ga (gauge digit 4) is only available with CMG colors. Got: {color_code}",
        }

    # Build PID
    pid = family_code + gauge_digit + color_code

    # Handle special cases
    if family_code == "TRAPEZOID":
        pid = family_code + "T" + gauge_digit + color_code
    elif family_code in ("A9", "A6"):
        # No gauge digit for A9/A6
        pid = family_code + color_code

    # Add length if provided and not a panel
    if length_str and family_code not in ("PRO", "A9", "A6", "BBQ750", "SSQ550", "SSQ675", "FF100") and not family_code.startswith("CO") and not family_code.startswith("FS"):
        # Extract numeric length
        length_match = re.search(r"(\d+)", length_str)
        if length_match:
            length_num = int(length_match.group(1))
            # Map to length code
            if length_num in (10, 12, 14, 16, 18, 20):
                pid += str(length_num).zfill(2)

    return {
        "valid": True,
        "pid": pid,
        "family_code": family_code,
        "family_name": family_name,
        "gauge_digit": gauge_digit,
        "color_code": color_code,
        "length": length_str if length_str else "N/A (Panel or Material)",
    }


# ============================================================================
# OUTPUT FORMATTERS
# ============================================================================

def format_result(result: Dict[str, Any]) -> str:
    """Format encoding result for display."""
    if not result["valid"]:
        return f"ERROR: {result['error']}"

    output = []
    output.append(f"PID: {result['pid']}")
    output.append(f"  Family:     {result['family_code']} ({result['family_name']})")
    output.append(f"  Gauge:      {result['gauge_digit']} (from '{result.get('gauge_str', 'N/A')}')")
    output.append(f"  Color Code: {result['color_code']}")
    output.append(f"  Length:     {result['length']}")
    output.append("")

    return "\n".join(output)


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Encode English product descriptions into Greenfield Metal Sales PIDs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sku_encoder.py "Ridge Cap, 26ga, Charcoal Gray, 12ft"
  python sku_encoder.py "SSQ 550 Panel, 29ga, Arctic White"
  python sku_encoder.py "Pitch Change Flashing, 26ga, Matte Black, 14ft"
  python sku_encoder.py --batch descriptions.txt
  python sku_encoder.py --color-map
  python sku_encoder.py --families

Format: Product Name, Gauge (24/26/29ga), Color Name, Length (trims only)
        """
    )

    parser.add_argument(
        "description",
        nargs="?",
        help="Product description to encode"
    )

    parser.add_argument(
        "--batch",
        type=str,
        help="Read descriptions from a file (one per line)"
    )

    parser.add_argument(
        "--color-map",
        action="store_true",
        help="Display all color name → code mappings"
    )

    parser.add_argument(
        "--families",
        action="store_true",
        help="Display all known product families"
    )

    args = parser.parse_args()

    # Display color map
    if args.color_map:
        print("COLOR NAME → CODE MAPPINGS")
        print("=" * 60)
        for color_name in sorted(COLOR_NAME_TO_CODE.keys()):
            code = COLOR_NAME_TO_CODE[color_name]
            print(f"  {color_name:30} → {code}")
        return

    # Display families
    if args.families:
        print("PRODUCT FAMILIES")
        print("=" * 60)
        seen = set()
        for alias in sorted(FAMILY_REGISTRY.keys()):
            code, name = FAMILY_REGISTRY[alias]
            if code not in seen:
                print(f"  {code:12} ({name})")
                seen.add(code)
        return

    # Encode descriptions
    descriptions = []

    if args.batch:
        try:
            with open(args.batch, 'r') as f:
                descriptions.extend(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            print(f"Error: File '{args.batch}' not found", file=sys.stderr)
            sys.exit(1)

    if args.description:
        descriptions.append(args.description)

    if not descriptions:
        parser.print_help()
        sys.exit(1)

    # Process each description
    for desc in descriptions:
        result = encode_pid(desc)

        if result["valid"]:
            print(f"✓ INPUT: {desc}")
            print(f"  PID: {result['pid']}")
            print(f"    Family:   {result['family_code']} ({result['family_name']})")
            print(f"    Gauge:    {result['gauge_digit']}")
            print(f"    Color:    {result['color_code']}")
            print(f"    Length:   {result['length']}")
            print()
        else:
            print(f"✗ INPUT: {desc}")
            print(f"  ERROR: {result['error']}")
            print()


if __name__ == "__main__":
    main()
