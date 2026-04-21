#!/usr/bin/env python3
"""
GMS SKU Decoder - Decode Greenfield Metal Sales Product IDs into human-readable specifications.

This script decodes any GMS Product ID (PID/SKU) into complete product specifications
including family, gauge, color, length, finish type, and material sourcing.

No external dependencies required - runs standalone with Python 3.6+

Usage:
    python sku_decoder.py PCF9ARW10
    python sku_decoder.py PCF9ARW10 RC6CG12 SSQ6754AG
    python sku_decoder.py --batch products.txt
    python sku_decoder.py PCF9ARW10 --output json
    python sku_decoder.py --batch products.txt --output csv
"""

import argparse
import sys
import json
import csv
from io import StringIO
from typing import Dict, List, Optional, Tuple, Any


# ============================================================================
# COMPREHENSIVE FAMILY REGISTRY (211+ families)
# Sorted longest-first for greedy matching. Families with embedded numbers
# must appear before shorter prefixes (CRD810 before CRD81 before CRD).
# ============================================================================

FAMILY_REGISTRY = {
    # --- Panels (NO length code) ---
    "TRAPEZOID": ("Trapezoid Panel", "Panel", "exposed"),
    "BBQ750":    ("Board & Batten 750 Panel", "Panel", "hidden"),
    "SSQ675":    ("Standing Seam 675 Panel", "Panel", "hidden"),
    "SSQ550":    ("Standing Seam 550 Panel", "Panel", "hidden"),
    "FF100":     ("Flush Flat 100 Panel", "Panel", "hidden"),
    "PRO":       ("Pro Panel", "Panel", "exposed"),
    "A9":        ("Ag Panel 29ga", "Panel", "exposed"),
    "A6":        ("Greenfield Classic / Ag Panel 26ga", "Panel", "exposed"),

    # --- Coil / Flatsheet (raw material, NO length code) ---
    "CO":  ("Coil (raw material)", "Coil", "material"),
    "FS":  ("Flatsheet (raw material)", "Flatsheet", "material"),

    # --- Trim & Flashing (HAVE length code) ---
    # Crown family — longest first to avoid partial matches
    "CRD10110": ("Crown Drip 10x11 (10ft variant)", "Trim", "flashing"),
    "CRD1011":  ("Crown Drip 10x11", "Trim", "flashing"),
    "CRD810":   ("Crown Drip 8x10", "Trim", "flashing"),
    "CRD81":    ("Crown Drip 8x1", "Trim", "flashing"),
    "CRDD1011": ("Crown Drip Double 10x11", "Trim", "flashing"),
    "CRDD810":  ("Crown Drip Double 8x10", "Trim", "flashing"),
    "CRDD81":   ("Crown Drip Double 8x1", "Trim", "flashing"),
    "CRRC10":   ("Crown Ridge Cap 10in", "Trim", "flashing"),
    "CRRC":     ("Crown Ridge Cap", "Trim", "flashing"),
    "CRDF":     ("Crown Drip Flat", "Trim", "flashing"),
    "CRSF":     ("Crown Sidewall Flashing", "Trim", "flashing"),
    "CRJ":      ("Crown J-Trim", "Trim", "flashing"),
    "CRZ":      ("Crown Z-Flashing", "Trim", "flashing"),
    "CRB":      ("Commercial Rib", "Trim", "flashing"),

    # Ridge Cap family — longest first
    "RC24": ("Ridge Cap 24 inch", "Trim", "flashing"),
    "RC20": ("Ridge Cap 20 inch", "Trim", "flashing"),
    "RC14": ("Ridge Cap 14 inch", "Trim", "flashing"),
    "RC10": ("Ridge Cap 10 inch", "Trim", "flashing"),
    "RC":   ("Ridge Cap Standard", "Trim", "flashing"),

    # Angle family
    "ANG22": ("Angle 2x2", "Trim", "flashing"),
    "ANG11": ("Angle 1x1", "Trim", "flashing"),

    # CP family
    "CPFRC": ("CP Face Rail Cap", "Trim", "flashing"),
    "CPBR":  ("CP Board & Rail", "Trim", "flashing"),

    # RAC family
    "RAC16": ("Rake & Corner 16in", "Trim", "flashing"),
    "RAC":   ("Roofing Angle Channel", "Trim", "flashing"),

    # HF families (hidden fastener trim — uses 41" material)
    "HFBT": ("HF Base Trim", "Trim", "hidden_fastener"),
    "HFDF": ("HF Door Frame", "Trim", "hidden_fastener"),
    "HFJT": ("HF Jamb Trim", "Trim", "hidden_fastener"),
    "HFRG": ("HF Ridge Gap", "Trim", "hidden_fastener"),
    "HFSF": ("HF Side Flashing", "Trim", "hidden_fastener"),
    "HFTF": ("HF Top Flashing", "Trim", "hidden_fastener"),
    "HFVF": ("HF Valley Flashing", "Trim", "hidden_fastener"),

    # Side Door Trim
    "SDT9": ("Side Door Trim 9 inch", "Trim", "flashing"),
    "SDT7": ("Side Door Trim 7 inch", "Trim", "flashing"),

    # Edge Trim
    "ET5": ("Edge Trim 5 inch", "Trim", "flashing"),
    "ET4": ("Edge Trim 4 inch", "Trim", "flashing"),
    "ET":  ("Edge Trim", "Trim", "flashing"),

    # Face family
    "FAS1": ("Face Angle Stiffener 1", "Trim", "flashing"),
    "FCH":  ("Face Channel", "Trim", "flashing"),
    "FCJ":  ("Face Channel Jamb", "Trim", "flashing"),
    "FA":   ("Face Angle", "Trim", "flashing"),

    # Metal Stud
    "MET3": ("Metal Stud 3 inch", "Trim", "flashing"),

    # Water/Valley families
    "WV36": ("Water Valley 36 inch", "Trim", "flashing"),
    "WV24": ("Water Valley 24 inch", "Trim", "flashing"),
    "WV":   ("Water Valley", "Trim", "flashing"),
    "VV":   ("Valley Valley", "Trim", "flashing"),

    # Standard trim families (alphabetical)
    "BB":   ("Board & Batten Trim", "Trim", "panel_adjacent"),
    "BT":   ("Base Trim", "Trim", "flashing"),
    "CCF":  ("Corrugated Cap Flat", "Trim", "flashing"),
    "DE":   ("Drip Edge", "Trim", "flashing"),
    "DF":   ("Door Frame", "Trim", "flashing"),
    "DJT":  ("Door Jam Trim", "Trim", "flashing"),
    "EW":   ("Edge Weld", "Trim", "flashing"),
    "FSS":  ("Flatsheet Stiffener", "Trim", "flashing"),
    "GA":   ("Gable Angle", "Trim", "flashing"),
    "GF":   ("Gutter Flashing", "Trim", "flashing"),
    "GT":   ("Gutter Trim", "Trim", "flashing"),
    "HC":   ("Horizontal Channel", "Trim", "flashing"),
    "HT":   ("Header Trim", "Trim", "flashing"),
    "IC":   ("Inside Corner", "Trim", "flashing"),
    "JCH":  ("J Channel Heavy", "Trim", "flashing"),
    "JC":   ("J Channel", "Trim", "flashing"),
    "JT":   ("Jamb Trim", "Trim", "flashing"),
    "KOT":  ("Knock Out Trim", "Trim", "flashing"),
    "OC":   ("Outside Corner", "Trim", "flashing"),
    "ODHC": ("Overhead Door Header Channel", "Trim", "flashing"),
    "PCF":  ("Pitch Change Flashing", "Trim", "flashing"),
    "PT":   ("Pigeon Trim", "Trim", "flashing"),
    "RG":   ("Roofing Gauge", "Trim", "flashing"),
    "RT":   ("Rake Trim", "Trim", "flashing"),
    "SI":   ("Soffit Insert", "Trim", "flashing"),
    "SS":   ("Soffit Stiffener", "Trim", "flashing"),
    "TC":   ("Trim Channel", "Trim", "flashing"),
}

# Pre-sorted family list: longest prefix first for greedy matching
_SORTED_FAMILIES = sorted(FAMILY_REGISTRY.keys(), key=len, reverse=True)


# ============================================================================
# COMPREHENSIVE COLOR CODE REGISTRY
# Built from references/color-to-code.md (actual Paradigm data)
# Includes BOTH CM* (Paradigm native) and CMG* (SKILL.md alternate) codes
# ============================================================================

COLOR_REGISTRY = {
    # ── USS Standard Colors ──
    "AG":   "Ash Gray",
    "ALW":  "Alamo White",
    "ARW":  "Arctic White",
    "B":    "Brown",
    "BER":  "Berry",
    "BK":   "Black",
    "BOND": "Bonderized",
    "BP":   "Barnwood Plank",
    "BR":   "Brick Red",
    "BRI":  "Bright Red",
    "BS":   "Burnished Slate",
    "BSK":  "Buckskin",
    "BUR":  "Burgundy",
    "BW":   "Bright White",
    "BZ":   "Bronze",
    "CB":   "Cocoa Brown",
    "CG":   "Charcoal Gray",
    "CH":   "Charcoal",
    "CLR":  "Clear",
    "COP":  "Copper",
    "COPM": "Copper Metallic",
    "CW":   "Cedar Woodgrain",
    "DB":   "Desert Brown",
    "DG":   "Dark Gray",
    "DR":   "Dark Red",
    "EB":   "Evergreen",
    "G90":  "Galvanized G90",
    "GAL":  "Galvalume",
    "GB":   "Gallery Blue",
    "GN":   "Gunmetal",
    "GRN":  "Green",
    "GR":   "Green",
    "HB":   "Hawaiian Blue",
    "IG":   "Ivy Green",
    "IV":   "Ivory",
    "KB":   "Koko Brown",
    "LS":   "Light Stone",
    "MD":   "Midnight",
    "MG":   "Midnight Gray",
    "OB":   "Ocean Blue",
    "OTG":  "Old Town Gray",
    "OW":   "Oyster White",
    "PG":   "Pewter Gray",
    "PW":   "Polar White",
    "QQ":   "Quote Color",
    "RD":   "Red",
    "REB":  "Rough Edge Barnwood",
    "RR":   "Rural Red",
    "RRU":  "Rustic Red",
    "SL":   "Slate",
    "SN":   "Stone",
    "ST":   "Saddle Tan",
    "STW":  "Stone White",
    "TAN":  "Tan",
    "TB":   "Tan/Beige",
    "TN":   "Tan",
    "TP":   "Taupe",
    "TXB":  "Textured Black",
    "WH":   "White",
    "WN":   "Wine",
    "BBW":  "Brown Barn Wood",

    # ── USS Crinkle Colors (+15%) ──
    "AGC":  "Ash Gray Crinkle",
    "ARC":  "Arctic White Crinkle",
    "AWC":  "Alamo White Crinkle",
    "BKC":  "Black Crinkle",
    "BRC":  "Brown Crinkle",
    "BSC":  "Burnished Slate Crinkle",
    "BURC": "Burgundy Crinkle",
    "BZC":  "Bronze Crinkle",
    "CGC":  "Charcoal Gray Crinkle",
    "CHC":  "Charcoal Crinkle",
    "DBC":  "Dark Bronze Crinkle",
    "DGC":  "Dark Gray Crinkle",
    "EBC":  "Evergreen Crinkle",
    "GNC":  "Gunmetal Crinkle",
    "GRNC": "Green Crinkle",
    "KBC":  "Koko Brown Crinkle",
    "LSC":  "Light Stone Crinkle",
    "MDC":  "Midnight Crinkle",
    "MGC":  "Midnight Gray Crinkle",
    "OWC":  "Oyster White Crinkle",
    "RC":   "Red Crinkle",
    "RDC":  "Red Crinkle",
    "RRUC": "Rustic Red Crinkle",
    "RTC":  "Real Tree Camo",
    "RTCC": "Real Tree Crinkle",
    "SLC":  "Slate Crinkle",
    "SNC":  "Stone Crinkle",
    "TBC":  "Tan/Beige Crinkle",
    "TNC":  "Tan Crinkle",
    "TPC":  "Taupe Crinkle",
    "WHC":  "White Crinkle",
    "WNC":  "Wine Crinkle",

    # ── USS Crinkle Colors with CR prefix (+15%) ──
    "CRBK": "Crinkle Black",
    "CRAG": "Crinkle Ash Gray",
    "CRARW": "Crinkle Arctic White",
    "CRCH": "Crinkle Charcoal",
    "CRCG": "Crinkle Charcoal Gray",
    "CRDG": "Crinkle Dark Gray",
    "CRGN": "Crinkle Gunmetal",
    "CRBZ": "Crinkle Bronze",
    "CRRD": "Crinkle Red",
    "CRSL": "Crinkle Slate",
    "CRSN": "Crinkle Stone",
    "CRWH": "Crinkle White",
    "CRWN": "Crinkle Wine",
    "CRBR": "Crinkle Brown",
    "CREW": "Crinkle Oyster White",

    # ── USS Matte Colors (+8%) ──
    "MBB":  "Matte Black",
    "MBW":  "Matte Brown",
    "MBS":  "Matte Burnished Slate",
    "MBZ":  "Matte Bronze",
    "MCC":  "Matte Finish (generic)",
    "MCH":  "Matte Charcoal",
    "MDG":  "Matte Dark Gray",
    "MGN":  "Matte Gunmetal",
    "MKB":  "Matte Koko Brown",
    "MLS":  "Matte Light Stone",
    "MMG":  "Matte Moss Green",
    "MRD":  "Matte Red",
    "MT":   "Matte Tan",
    "MWH":  "Matte White",
    "BKM":  "Black Matte",
    "BWM":  "Bright White Matte",
    "CBM":  "Cocoa Brown Matte",
    "CGM":  "Charcoal Gray Matte",
    "LSM":  "Light Stone Matte",

    # ── CMG Standard Colors (Kynar, CM* Paradigm codes) ──
    "CMAC":   "CMG Aged Copper",
    "CMAG":   "CMG Almond",
    "CMAG2":  "CMG Ash Gray",
    "CMAI":   "CMG Antique Ivory",
    "CMBO":   "CMG Black Ore",
    "CMBW":   "CMG Bone White",
    "CMBRW":  "CMG Bright White",
    "CMBUR":  "CMG Burgundy",
    "CMBS":   "CMG Burnished Slate",
    "CMCG":   "CMG Charcoal Gray",
    "CMCHP":  "CMG Champagne",
    "CMCS":   "CMG Cityscape",
    "CMCRB":  "CMG Carbon",
    "CMCG2":  "CMG Classic Green",
    "CMCR":   "CMG Colonial Red",
    "CMCP":   "CMG Copper Penny",
    "CMDB":   "CMG Deep Black",
    "CMDBZ":  "CMG Dark Bronze",
    "CMEDG":  "CMG Extra Dark Bronze",
    "CMGP":   "CMG Galvalume Plus",
    "CMHG":   "CMG Hartford Green",
    "CMHG2":  "CMG Hemlock Green",
    "CMIO":   "CMG Iron Ore",
    "CMMB":   "CMG Mansard Brown",
    "CMMB2":  "CMG Medium Bronze",
    "CMMG":   "CMG Musket Gray",
    "CMPC":   "CMG Pebble Clay",
    "CMRR":   "CMG Regal Red",
    "CMRB":   "CMG Royal Blue",
    "CMRR2":  "CMG Rustic Rawhide",
    "CMSM":   "CMG Silver Metallic",
    "CMSND":  "CMG Sandstone",
    "CMST":   "CMG Sierra Tan",
    "CMSV":   "CMG Silver",
    "CMSB":   "CMG Slate Blue",
    "CMSG":   "CMG Slate Gray",
    "CMSW":   "CMG Stone White",
    "CMTL":   "CMG Teal",
    "CMTC":   "CMG Terra Cotta",
    "CMV":    "CMG Vintage",
    "CMWZ":   "CMG Weathered Zinc",
    "CMWR":   "CMG Western Rust",

    # ── CMG Crinkle Colors (CM* + C suffix, +15%) ──
    "CMBURC":  "CMG Burgundy Crinkle",
    "CMBSC":   "CMG Burnished Slate Crinkle",
    "CMCGC":   "CMG Classic Green Crinkle",
    "CMCRC":   "CMG Colonial Red Crinkle",
    "CMDBZC":  "CMG Dark Bronze Crinkle",
    "CMHGC":   "CMG Hartford Green Crinkle",
    "CMMEC":   "CMG Medium Bronze Crinkle",
    "CMMGC":   "CMG Musket Gray Crinkle",
    "CMSGC":   "CMG Slate Gray Crinkle",
    "CMSTC":   "CMG Sierra Tan Crinkle",
    "CMTCC":   "CMG Terra Cotta Crinkle",

    # ── CMG ULG Matte Colors (CM* + U suffix, +15%) ──
    "CMBK":   "CMG Black Matte (ULG)",
    "CMBKM":  "CMG Black Matte ULG",
    "CMBSU":  "CMG Burnished Slate Matte (ULG)",
    "CMCGU":  "CMG Charcoal Gray Matte (ULG)",
    "CMCAU":  "CMG Carbon Matte (ULG)",
    "CMIRU":  "CMG Iron Ore Matte (ULG)",
    "CMSGU":  "CMG Slate Gray Matte (ULG)",

    # ── CMG Colors: SKILL.md alternate codes (CMG* prefix) ──
    # These appear in some PIDs and documentation
    "CMGAC":   "CMG Aged Copper",
    "CMGALM":  "CMG Aluminum",
    "CMGAG":   "CMG Ash Gray",
    "CMGBK":   "CMG Black",
    "CMGBL":   "CMG Blue",
    "CMGBR":   "CMG Brown",
    "CMGCH":   "CMG Charcoal",
    "CMGCN":   "CMG Coral",
    "CMGCR":   "CMG Cherry Red",
    "CMGDB":   "CMG Dark Brown",
    "CMGDG":   "CMG Dark Gray",
    "CMGFR":   "CMG Forest Green",
    "CMGGG":   "CMG Graphite Gray",
    "CMGGN":   "CMG Green",
    "CMGGR":   "CMG Granite",
    "CMGGY":   "CMG Gray",
    "CMGLG":   "CMG Light Gray",
    "CMGMB":   "CMG Medium Bronze",
    "CMGMG":   "CMG Moss Green",
    "CMGOV":   "CMG Olive",
    "CMGPW":   "CMG Pearl White",
    "CMGRD":   "CMG Red",
    "CMGRT":   "CMG Rust",
    "CMGSN":   "CMG Stone",
    "CMGTB":   "CMG Tan",
    "CMGTN":   "CMG Tan/Buff",
    "CMGVG":   "CMG Vine Green",
    "CMGWH":   "CMG White",
    "CMGWR":   "CMG Wine Red",

    # ── CMG Crinkle: SKILL.md alternate codes (CMG* + C suffix) ──
    "CMGAGC":  "CMG Ash Gray Crinkle",
    "CMGBKC":  "CMG Black Crinkle",
    "CMGBRC":  "CMG Brown Crinkle",
    "CMGCHC":  "CMG Charcoal Crinkle",
    "CMGDGC":  "CMG Dark Gray Crinkle",
    "CMGGRC":  "CMG Green Crinkle",

    # ── CMG ULG: SKILL.md alternate codes (CMG* + M suffix) ──
    "CMGBURM": "CMG Burgundy ULG",
    "CMGBKM":  "CMG Black ULG",
    "CMGBRM":  "CMG Brown ULG",
    "CMGCHM":  "CMG Charcoal ULG",
    "CMGCRM":  "CMG Cherry Red ULG",
    "CMGDGM":  "CMG Dark Gray ULG",
    "CMGFRM":  "CMG Forest Green ULG",
    "CMGGYM":  "CMG Gray ULG",
    "CMGGRM":  "CMG Granite ULG",
    "CMGGM":   "CMG Green ULG",
    "CMGLGM":  "CMG Light Gray ULG",
    "CMGMBM":  "CMG Medium Bronze ULG",
    "CMGMGM":  "CMG Moss Green ULG",
    "CMGOVM":  "CMG Olive ULG",
    "CMGPWM":  "CMG Pearl White ULG",
    "CMGRDM":  "CMG Red ULG",
    "CMGRTM":  "CMG Rust ULG",
    "CMGSNM":  "CMG Stone ULG",
    "CMGTBM":  "CMG Tan ULG",
    "CMGTNM":  "CMG Tan Buff ULG",
    "CMGVGM":  "CMG Vine Green ULG",
    "CMGWHM":  "CMG White ULG",
    "CMGWRM":  "CMG Wine Red ULG",

    # ── Woodgrain / Specialty ──
    "BBW": "Brown Barn Wood",
    "RTC": "Real Tree Camo",
}

# Pre-sorted color codes longest-first for greedy matching
_SORTED_COLORS = sorted(COLOR_REGISTRY.keys(), key=len, reverse=True)


# ============================================================================
# KNOWN MATTE CODES — explicit set for reliable detection
# These are ALL the color codes that indicate Matte finish (+8%)
# ============================================================================

KNOWN_MATTE_CODES = {
    "MBB", "MBW", "MBS", "MBZ", "MCC", "MCH", "MDG", "MGN",
    "MKB", "MLS", "MMG", "MRD", "MT", "MWH",
    # Suffix-style matte codes
    "BKM", "BWM", "CBM", "CGM", "LSM",
}

# ============================================================================
# KNOWN CRINKLE CODES with CR prefix — explicit set
# These use CR + base color code instead of base + C suffix
# ============================================================================

KNOWN_CR_PREFIX_CRINKLE = {
    "CRBK", "CRAG", "CRARW", "CRCH", "CRCG", "CRDG", "CRGN",
    "CRBZ", "CRRD", "CRSL", "CRSN", "CRWH", "CRWN", "CRBR", "CREW",
}

# ============================================================================
# KNOWN CMG CRINKLE CODES — explicit set (both CM* and CMG* formats)
# ============================================================================

KNOWN_CMG_CRINKLE = {
    # Paradigm CM* format
    "CMBURC", "CMBSC", "CMCGC", "CMCG2C", "CMCRC", "CMDBZC",
    "CMHGC", "CMMEC", "CMMGC", "CMSGC", "CMSTC", "CMTCC",
    # SKILL.md CMG* format
    "CMGAGC", "CMGBKC", "CMGBRC", "CMGCHC", "CMGDGC", "CMGGRC",
}

# ============================================================================
# KNOWN CMG ULG CODES — explicit set (both CM* and CMG* formats)
# ============================================================================

KNOWN_CMG_ULG = {
    # Paradigm CM* format (ending in M or U)
    "CMBK", "CMBKM", "CMBSU", "CMCGU", "CMCAU", "CMIRU", "CMSGU",
    # SKILL.md CMG* format (ending in M)
    "CMGBURM", "CMGBKM", "CMGBRM", "CMGCHM", "CMGCRM", "CMGDGM",
    "CMGFRM", "CMGGYM", "CMGGRM", "CMGGM", "CMGLGM", "CMGMBM",
    "CMGMGM", "CMGOVM", "CMGPWM", "CMGRDM", "CMGRTM", "CMGSNM",
    "CMGTBM", "CMGTNM", "CMGVGM", "CMGWHM", "CMGWRM",
}


# ============================================================================
# GAUGE AND FINISH MAPPING
# ============================================================================

GAUGE_MAP = {
    "9": ("29ga", 0),
    "6": ("26ga", 1),
    "4": ("24ga", 2),
}

# Two-digit gauge for coils/flatsheets
GAUGE_2DIGIT_MAP = {
    "29": ("29ga", "9"),
    "26": ("26ga", "6"),
    "24": ("24ga", "4"),
}

FINISH_MULTIPLIERS = {
    "matte": 1.08,      # US Matte: +8%
    "crinkle": 1.15,    # Crinkle (various patterns): +15%
    "ulg": 1.15,        # CMG ULG: +15%
    "standard": 1.0,    # Standard finish
}


# ============================================================================
# MATERIAL SOURCE MAPPING
# ============================================================================

MATERIAL_PATTERNS = {
    "20": {
        "29ga": "CO2029{color}",
        "26ga": "CO2026{color}",
        "24ga": "FS2024{color}",
    },
    "41": {
        "29ga": "CO4129{color}",
        "26ga": "CO4126{color}",
        "24ga": "FS4124{color}",
    },
    "43": {
        "29ga": "CO4329{color}",
        "26ga": "CO4326{color}",
        "24ga": None,
    },
}

PATTERN_B_FAMILIES = {"HFVF", "ODHC", "RC20", "RC24", "VV", "WV", "WV24", "WV36"}
HFRG_FAMILY = {"HFRG"}


# ============================================================================
# PRODUCT TYPE UTILITIES
# ============================================================================

def identify_product_type(pid: str) -> str:
    """Identify the product type from a PID."""
    if pid.startswith("CO"):
        return "Coil"
    elif pid.startswith("FS"):
        return "Flatsheet"
    elif pid.startswith(("PRO", "BBQ750", "SSQ550", "SSQ675", "FF100", "TRAPEZOID")):
        return "Panel"
    elif pid.startswith(("A9", "A6")):
        return "Panel"
    else:
        return "Trim/Flashing"


def extract_family(pid: str) -> Tuple[Optional[str], str]:
    """
    Extract family prefix from PID.
    Returns: (family_prefix, remaining_pid)

    Coils: CO{WIDTH}{GAUGE}{COLOR}  (width=2-digit, gauge=2-digit)
    Flatsheets: FS{WIDTH}{GAUGE}{COLOR}
    """
    if pid.startswith("CO"):
        return "CO", pid[2:]
    elif pid.startswith("FS"):
        return "FS", pid[2:]

    # Try all families longest-first (greedy match)
    for family in _SORTED_FAMILIES:
        if family in ("CO", "FS"):
            continue  # Already handled above
        if not pid.startswith(family):
            continue

        remaining = pid[len(family):]

        # A9/A6: gauge is in the family name, no separate digit needed
        if family in ("A9", "A6"):
            return family, remaining

        # TRAPEZOID can have T before gauge digit
        if family == "TRAPEZOID":
            if remaining.startswith("T") and len(remaining) > 1 and remaining[1] in "469":
                return family, remaining
            if remaining and remaining[0] in "469":
                return family, remaining

        # Standard case: next char must be a gauge digit
        if remaining and remaining[0] in "469":
            return family, remaining

    return None, pid


def extract_gauge(remaining: str, family: str) -> Tuple[Optional[str], Optional[str], str]:
    """
    Extract gauge and return (gauge_name, gauge_digit, remaining_pid).

    Coil/Flatsheet: remaining = {WIDTH_2DIGIT}{GAUGE_2DIGIT}{COLOR}
      Examples: "4129ARW" (width=41, gauge=29, color=ARW)
                "2026AG"  (width=20, gauge=26, color=AG)

    Standard trim: remaining = {GAUGE_1DIGIT}{COLOR}{LENGTH}
      Examples: "9ARW10" (gauge=29ga, color=ARW, length=10)
    """
    if family in ("A9", "A6"):
        gauge = "29ga" if family == "A9" else "26ga"
        return gauge, None, remaining

    if family == "TRAPEZOID" and remaining.startswith("T"):
        remaining = remaining[1:]

    if family in ("CO", "FS"):
        # Coil/Flatsheet format: {WIDTH}{GAUGE}{COLOR}
        # Width: 2 digits (20, 41, 43, 48)
        # Gauge: 2 digits (29, 26, 24)
        # Color: everything else

        # Valid 2-digit widths
        valid_widths = ("20", "41", "43", "48")

        if len(remaining) >= 4:
            width_2 = remaining[0:2]
            gauge_2 = remaining[2:4]

            if width_2 in valid_widths and gauge_2 in GAUGE_2DIGIT_MAP:
                gauge_name, _ = GAUGE_2DIGIT_MAP[gauge_2]
                color_remainder = remaining[4:]
                return gauge_name, gauge_2, color_remainder

        # Fallback: return error
        return None, None, remaining

    # Standard single-digit gauge for trims and panels
    if remaining and remaining[0] in GAUGE_MAP:
        gauge_digit = remaining[0]
        gauge_name, _ = GAUGE_MAP[gauge_digit]
        return gauge_name, gauge_digit, remaining[1:]

    return None, None, remaining


def detect_finish(color_code: str) -> str:
    """
    Determine finish type from a color code.

    Detection priority (order matters):
    1. CMG/CM prefix codes: check for ULG (ends M/U), crinkle (ends C), or standard
    2. Known CR-prefix crinkle codes (CRBK, CRAG, etc.)
    3. Known M-prefix matte codes (MBB, MCH, MCC, etc.)
    4. Known suffix-style matte codes (BKM, BWM, CGM, LSM, CBM)
    5. Ends with C (and len > 1): crinkle
    6. Otherwise: standard
    """
    if not color_code:
        return "standard"

    # ── CMG codes (both CMG* and CM* prefixes) ──
    # Must use EXPLICIT known sets because some standard CMG codes end in C/M/U
    # Example: CMGAC = CMG Aged Copper (standard), NOT crinkle despite ending in C
    #          CMAC  = same in Paradigm format
    is_cmg = color_code.startswith("CMG") or (
        color_code.startswith("CM") and len(color_code) >= 4
        and not color_code.startswith("COP")  # not Copper
    )

    if is_cmg:
        # Check explicit known CMG crinkle codes
        if color_code in KNOWN_CMG_CRINKLE:
            return "crinkle"
        # Check explicit known CMG ULG codes
        if color_code in KNOWN_CMG_ULG:
            return "ulg"
        # Everything else is standard CMG
        return "standard"

    # ── CR-prefix crinkle (CRBK, CRAG, etc.) ──
    if color_code in KNOWN_CR_PREFIX_CRINKLE:
        return "crinkle"
    # Catch unknown CR-prefix codes too (CR + 2+ letter base)
    if color_code.startswith("CR") and len(color_code) >= 4:
        return "crinkle"

    # ── M-prefix matte (MBB, MCH, MCC, etc.) ──
    if color_code in KNOWN_MATTE_CODES:
        return "matte"
    # Catch unknown M-prefix codes (M + 1-2 letter base, NOT starting with CM)
    if color_code.startswith("M") and len(color_code) >= 2 and not color_code.startswith("CM"):
        return "matte"

    # ── Suffix-style matte (BKM, BWM, CGM, LSM, CBM) ──
    if color_code.endswith("M") and color_code in KNOWN_MATTE_CODES:
        return "matte"

    # ── Suffix C = crinkle (AGC, BKC, CHC, etc.) ──
    if color_code.endswith("C") and len(color_code) > 1:
        return "crinkle"

    return "standard"


def extract_color_and_finish(remaining: str, product_type: str, family: str = "") -> Tuple[Optional[str], Optional[str], Optional[str], str]:
    """
    Extract color code and determine finish type.
    Returns: (color_code, color_name, finish_type, remaining_pid)

    For trim: last 2 digits are length, everything before is color.
    For panels/coils/flatsheets: everything is color (no length).
    """
    if product_type in ("Coil", "Flatsheet", "Panel"):
        color_code = remaining
        remaining_after = ""
    else:
        # Trim: last 2 chars are length code (if they're numeric)
        if len(remaining) >= 3 and remaining[-2:].isdigit():
            color_code = remaining[:-2]
            remaining_after = remaining[-2:]
        elif len(remaining) >= 2 and remaining[-2:].isdigit():
            color_code = ""
            remaining_after = remaining[-2:]
        else:
            color_code = remaining
            remaining_after = ""

    # Look up color name
    color_name = COLOR_REGISTRY.get(color_code)
    if color_name is None:
        color_name = f"Unknown ({color_code})"

    # Determine finish type using robust detection
    finish = detect_finish(color_code)

    return color_code, color_name, finish, remaining_after


def extract_length(remaining: str, product_type: str) -> Tuple[Optional[int], str]:
    """Extract length code (for trims only)."""
    if product_type != "Trim/Flashing":
        return None, remaining

    if remaining and len(remaining) >= 2:
        try:
            length = int(remaining[-2:])
            if length in (10, 12, 14, 16, 18, 20):
                return length, ""
        except ValueError:
            pass

    return None, remaining


def determine_material_source(family: str, gauge: str, color_code: str) -> str:
    """Determine which coil or flatsheet feeds this product."""
    if family in HFRG_FAMILY:
        pattern = "43"
    elif family in PATTERN_B_FAMILIES:
        pattern = "41"
    else:
        pattern = "20"

    patterns = MATERIAL_PATTERNS.get(pattern, {})
    template = patterns.get(gauge)

    if template:
        return template.format(color=color_code)
    return f"Unknown ({family}/{gauge}/{color_code})"


def categorize_product(family: str, product_type: str) -> Tuple[str, float]:
    """Return (category_name, target_margin_percent)."""
    if product_type == "Coil":
        return "Raw Material", 0.35
    elif product_type == "Flatsheet":
        return "Raw Material", 0.35
    elif family in ("PRO", "A9", "A6"):
        return "Exposed Fastener Panel", 0.35
    elif family in ("SSQ550", "SSQ675", "FF100", "BBQ750"):
        return "Hidden Fastener Panel", 0.40
    elif family == "TRAPEZOID":
        return "Exposed Fastener Panel", 0.35
    else:
        return "Trim & Flashing", 0.50


# ============================================================================
# MAIN DECODER FUNCTION
# ============================================================================

def decode_pid(pid: str) -> Optional[Dict[str, Any]]:
    """
    Decode a single PID into a dict of specifications.
    Returns None if PID is invalid.
    """
    pid = pid.strip().upper()

    if not pid:
        return None

    # Step 1: Identify product type
    product_type = identify_product_type(pid)

    # Step 2: Extract family
    family, remaining = extract_family(pid)

    if not family:
        return {
            "pid": pid,
            "valid": False,
            "error": "Could not identify product family",
        }

    # Step 3: Extract gauge
    gauge, gauge_raw, remaining = extract_gauge(remaining, family)

    if not gauge:
        return {
            "pid": pid,
            "valid": False,
            "error": "Could not identify gauge digit",
        }

    # Step 4: Extract color and finish
    color_code, color_name, finish, remaining = extract_color_and_finish(remaining, product_type, family)

    # Step 5: Extract length (if trim)
    length, _ = extract_length(remaining, product_type)

    # Validate 24ga is CMG only
    is_cmg_color = (
        color_code.startswith("CMG") or
        color_code.startswith("CM") and len(color_code) >= 4
        and not color_code.startswith("COP")
    )
    if gauge == "24ga" and not is_cmg_color:
        return {
            "pid": pid,
            "valid": False,
            "error": "24ga is only available with CMG (Kynar) colors",
        }

    # Determine material source
    material_source = determine_material_source(family, gauge, color_code)

    # Categorize product
    category, target_margin = categorize_product(family, product_type)

    # Get finish multiplier
    finish_multiplier = FINISH_MULTIPLIERS.get(finish, 1.0)

    # Get family info
    family_info = FAMILY_REGISTRY.get(family, ("Unknown", "Unknown", "Unknown"))
    family_name, fam_type, fam_subtype = family_info

    # Build coil width info for coils/flatsheets
    extra = {}
    if family in ("CO", "FS") and gauge_raw and len(gauge_raw) == 2:
        # We stored gauge_raw as the 2-digit gauge; width was already parsed
        # Reconstruct width from original PID
        after_prefix = pid[2:]  # everything after CO/FS
        width_code = after_prefix[:2]
        width_map = {"20": '20.0"', "41": '40.875"', "43": '~43"', "48": '48.375"'}
        extra["coil_width"] = width_map.get(width_code, f'{width_code}"')

    return {
        "pid": pid,
        "valid": True,
        "product_type": product_type,
        "family_prefix": family,
        "family_name": family_name,
        "gauge": gauge,
        "color_code": color_code,
        "color_name": color_name,
        "length_feet": length,
        "finish_type": finish,
        "finish_multiplier": finish_multiplier,
        "material_source": material_source,
        "category": category,
        "target_margin_percent": target_margin * 100,
        **extra,
    }


# ============================================================================
# OUTPUT FORMATTERS
# ============================================================================

def format_table(results: List[Dict[str, Any]]) -> str:
    """Format results as human-readable table."""
    output = []

    for result in results:
        if not result["valid"]:
            output.append(f"PID: {result['pid']}")
            output.append(f"  ERROR: {result['error']}")
            output.append("")
            continue

        output.append(f"PID: {result['pid']}")
        output.append(f"  Product Type:     {result['product_type']}")
        output.append(f"  Family:           {result['family_prefix']} ({result['family_name']})")
        output.append(f"  Gauge:            {result['gauge']}")
        output.append(f"  Color:            {result['color_code']} ({result['color_name']})")
        if result.get('coil_width'):
            output.append(f"  Coil Width:       {result['coil_width']}")
        if result['length_feet']:
            output.append(f"  Length:           {result['length_feet']} feet")
        output.append(f"  Finish:           {result['finish_type']} (x{result['finish_multiplier']:.2f})")
        output.append(f"  Material Source:  {result['material_source']}")
        output.append(f"  Category:         {result['category']}")
        output.append(f"  Target Margin:    {result['target_margin_percent']:.0f}%")
        output.append("")

    return "\n".join(output)


def format_json(results: List[Dict[str, Any]]) -> str:
    """Format results as JSON."""
    return json.dumps(results, indent=2)


def format_csv(results: List[Dict[str, Any]]) -> str:
    """Format results as CSV."""
    if not results:
        return ""

    output = StringIO()
    fieldnames = [
        "pid", "valid", "product_type", "family_prefix", "family_name",
        "gauge", "color_code", "color_name", "length_feet", "finish_type",
        "finish_multiplier", "material_source", "category", "target_margin_percent",
        "coil_width", "error"
    ]

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for result in results:
        row = {k: result.get(k, "") for k in fieldnames}
        writer.writerow(row)

    return output.getvalue()


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Decode Greenfield Metal Sales Product IDs (PIDs/SKUs)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sku_decoder.py PCF9ARW10
  python sku_decoder.py PCF9ARW10 RC6CG12 SSQ6754AG
  python sku_decoder.py CO4129ARW CO2026AG
  python sku_decoder.py --batch products.txt
  python sku_decoder.py PCF9ARW10 --output json
  python sku_decoder.py --batch products.txt --output csv > output.csv
        """
    )

    parser.add_argument(
        "pids",
        nargs="*",
        help="One or more product IDs to decode"
    )

    parser.add_argument(
        "--batch",
        type=str,
        help="Read PIDs from a file (one per line)"
    )

    parser.add_argument(
        "--output",
        choices=["table", "json", "csv"],
        default="table",
        help="Output format (default: table)"
    )

    args = parser.parse_args()

    pids_to_decode = []

    if args.batch:
        try:
            with open(args.batch, 'r') as f:
                pids_to_decode.extend(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            print(f"Error: File '{args.batch}' not found", file=sys.stderr)
            sys.exit(1)

    pids_to_decode.extend(args.pids)

    if not pids_to_decode:
        parser.print_help()
        sys.exit(1)

    results = [decode_pid(pid) for pid in pids_to_decode]

    if args.output == "json":
        print(format_json(results))
    elif args.output == "csv":
        print(format_csv(results))
    else:
        print(format_table(results))


if __name__ == "__main__":
    main()
