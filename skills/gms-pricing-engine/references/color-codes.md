# GMS Color Codes Reference

**Last Updated:** 2026-03-28
**Total Colors Cataloged:** 134 standard colors + specialty finishes
**Data Source:** analysis_color_results.json + CATALOG_TO_PARADIGM_MATCHED.csv

---

## Premium Finish Detection & Markup

### Detection Logic
Premium finishes are identified in product SKUs **immediately after the gauge digit** (29/26/24 or 9/6/4):
- Example: `CO4129MCC10` = 40.875" coil, 29ga, **Matte (MCC)**, 10'
- Example: `RC144CR10` = 14" Ridge Cap, 4ga (24), **Crinkle (CR)**, 10'
- Example: `ANG119ULG10` = 1.5" Angle, 29ga, **Ultra Low Gloss (ULG)**, 10'

### Finish Markup Rules
| Finish Code | Finish Type | Markup | Notes |
|-------------|-------------|--------|-------|
| MCC | Matte | +8% | Dull, non-reflective finish |
| CR | Crinkle | +15% | Textured, reduces gloss appearance |
| ULG | Ultra Low Gloss | +15% | Premium non-reflective coating |
| (none) | Standard Gloss | 0% | Base finish |

### Important Distinction
- **CR as finish:** `CO4126CR10` = Crinkle finish (+15%) ✓
- **CR as prefix:** `CRRC124AG10` = Commercial Rib Rake & Corner (NOT a finish) ✓

---

## USS Standard Paint Colors (~47 colors)

*SMP paint, 29/26ga coils, standard gloss finish*

| Code | Color Name | Use Cases |
|------|-----------|-----------|
| ARW | Arctic White | Most popular residential, neutral |
| BK | Black | High-contrast, commercial |
| BW | Bright White | Ultra white, premium residential |
| CH | Charcoal | Dark gray-black, modern |
| CG | Charcoal Gray | Medium-dark gray, commercial |
| AG | Ash Gray | Light gray, transitional |
| B / BR | Brown | Warm neutral, traditional |
| BUR | Burgundy | Deep red, premium |
| BER | Berry | Dark red-purple, specialty |
| BS | Burnished Slate | Blue-gray, modern |
| EB | Evergreen | Forest green, regional |
| ALW | Alamo White | Off-white, warm |
| BR | Brick Red | Rustic red, agricultural |
| BR-RT | Bright Red | Safety red, commercial |
| BK-TXT | Textured Black | Matte black (finish variant) |
| BSK | Buckskin | Tan-brown, rural |
| GRN | Green | Standard green (various shades) |
| COP | Copper | Metallic copper, specialty |
| CB | Charcoal Blue | Blue-gray, commercial |
| DB | Desert Brown | Warm brown, southwestern |
| DG | Dark Gray | Charcoal gray, modern |
| DR | Dark Red | Deep red, premium |
| GB | Gallery Blue | Steel blue, commercial |
| GAL | Galvalume | Bare metal-look, industrial |
| G90 | Galvanized G90 | Silver zinc, industrial |
| HB | Hawaiian Blue | Tropical blue, specialty |
| IV | Ivory | Off-white cream, residential |
| IG | Ivy Green | Deep forest, residential |
| KB | Koko Brown | Medium brown, warm |
| LS | Light Stone | Beige-white, residential |
| OB | Ocean Blue | Medium blue, contemporary |
| OTG | Old Town Gray | Weathered gray, rustic |
| PG | Pewter Gray | Silver-gray, modern |
| PW | Polar White | Cool white, premium |
| RTC | Real Tree Camo | Camouflage pattern, specialty |
| RR | Rural Red | Barn red, agricultural |
| RRU | Rustic Red | Weathered red, rustic |
| ST | Saddle Tan | Golden tan, southwestern |
| STW | Stone White | White with texture, residential |
| TAN | Tan | Light brown, residential |
| TP | Taupe | Gray-brown, contemporary |
| BP | Barnwood Plank | Wood grain finish (new Dec 2025) |
| REB | Rough Edge Barnwood | Wood texture variant |

---

## USS Crinkle Colors (~16 colors) — PREMIUM +15%

*Textured crinkle finish, SMP paint system, 29/26ga*

| Code | Color Name | Premium Notes |
|------|-----------|----------------|
| ALW-CR | Alamo White Crinkle | +15% markup, reduces gloss appearance |
| ARW-CR | Arctic White Crinkle | Popular crinkle variant, most common premium |
| AG-CR | Ash Gray Crinkle | Modern gray with texture |
| BK-CR | Black Crinkle | Matte black appearance, premium |
| BUR-CR | Burgundy Crinkle | Deep red texture, commercial grade |
| BS-CR | Burnished Slate Crinkle | Blue-gray texture, contemporary |
| CG-CR | Charcoal Gray Crinkle | Dark gray texture, durable |
| EB-CR | Evergreen Crinkle | Forest green texture, regional |
| GRN-CR | Green Crinkle | Standard green with crinkle |
| KB-CR | Koko Brown Crinkle | Warm brown texture |
| LS-CR | Light Stone Crinkle | Beige texture, residential |
| MG-CR | Midnight Gray Crinkle | Very dark gray, modern |
| RTC-CR | Real Tree Crinkle | Camouflage with crinkle texture |
| RD-CR | Red Crinkle | Medium red texture |
| RRU-CR | Rustic Red Crinkle | Weathered red texture, rustic |
| TP-CR | Taupe Crinkle | Gray-brown texture, contemporary |

---

## USS Matte Colors (~7 colors) — PREMIUM +8%

*Matte/flat finish, SMP paint system, 29/26ga*

| Code | Color Name | Premium Notes |
|------|-----------|----------------|
| BK-MCC | Matte Black | +8% markup, non-reflective |
| BW-MCC | Matte Bright White | +8% markup, ultra flat |
| BS-MCC | Matte Burnished Slate | +8% markup, blue-gray matte |
| CG-MCC | Matte Charcoal Gray | +8% markup, dark gray matte |
| CB-MCC | Matte Cocoa Brown | +8% markup, warm brown matte |
| LS-MCC | Matte Light Stone | +8% markup, beige matte |
| TP-MCC | Matte Taupe | +8% markup, gray-brown matte |

---

## CMG Standard Colors (~42 colors)

*Kynar/PVDF paint, 24/26ga coils, premium standard gloss finish (40-year warranty), 51 total color palette*

| Code | Color Name | Premium Notes |
|------|-----------|----------------|
| CMAG | CMG - ALMOND | Warm neutral, residential |
| CMAC | CMG - Aged Copper | Patina copper, specialty |
| CMAI | CMG - Antique Ivory | Off-white, classic |
| CMAG2 | CMG - Ash Gray | Light gray, modern |
| CMBO | CMG - Black Ore | Deep black, premium |
| CMBW | CMG - Bone White | Warm white, residential |
| CMBRW | CMG - Bright White | Cool white, premium |
| CMBUR | CMG - Burgundy | Deep red, premium commercial |
| CMBS | CMG - Burnished Slate | Blue-gray, contemporary |
| CMCG | CMG - CHARCOAL GRAY | Dark gray, commercial |
| CMCS | CMG - CITYSCAPE | Modern gray, contemporary |
| CMCRB | CMG - Carbon | Metallic carbon, specialty |
| CMCHP | CMG - Champagne | Gold-white, premium |
| CMCHP2 | CMG - Charcoal Gray – MATTE ULG | Matte variant, +15% |
| CMCG2 | CMG - Classic Green | Forest green, regional |
| CMCR | CMG - Colonial Red | Traditional red, residential |
| CMCP | CMG - Copper Penny | Metallic copper, specialty |
| CMDB | CMG - DEEP BLACK | Ultra black, premium |
| CMDBZ | CMG - Dark Bronze | Deep bronze, commercial |
| CMEDG | CMG - Extra Dark Bronze | Darkest bronze, specialty |
| CMGP | CMG - Galvalume Plus | Enhanced metal-look, industrial |
| CMHG | CMG - Hartford Green | Regional green, commercial |
| CMHG2 | CMG - Hemlock Green | Deep forest, residential |
| CMIO | CMG - Iron Ore | Dark metallic, industrial |
| CMMB | CMG - MANSARD BROWN | Dark brown, traditional |
| CMMB2 | CMG - Medium Bronze | Medium bronze, versatile |
| CMMG | CMG - Musket Gray | Cool gray, military-inspired |
| CMPC | CMG - Pebble Clay | Textured tan, contemporary |
| CMRR | CMG - Regal Red | Deep red, premium |
| CMRB | CMG - Royal Blue | Deep blue, commercial |
| CMRR2 | CMG - Rustic Rawhide® | Warm tan, southwestern |
| CMSM | CMG - SILVER Metallic | Bright silver, metallic |
| CMSND | CMG - Sandstone | Tan-gray, residential |
| CMST | CMG - Sierra Tan | Golden tan, southwestern |
| CMSV | CMG - Silver | Silver, industrial |
| CMSB | CMG - Slate Blue | Blue-gray, modern |
| CMSG | CMG - Slate Gray | Medium gray, versatile |
| CMSG2 | CMG - Slate Gray – MATTE ULG | Matte variant, +15% |
| CMSW | CMG - Stone White | White with warmth, residential |
| CMTL | CMG - Teal | Blue-green, contemporary |
| CMTC | CMG - Terra Cotta | Orange-red, southwestern |
| CMV | CMG - Vintage | Aged appearance, specialty |
| CMWZ | CMG - Weathered Zinc | Patina zinc, industrial |
| CMWR | CMG - Western Rust | Rust-orange, rustic |

---

## CMG Crinkle Colors (~10 colors) — PREMIUM +15%

*Kynar/PVDF with crinkle texture, 24/26ga, premium finish*

| Code | Color Name | Premium Notes |
|------|-----------|----------------|
| CMBUR-CR | CMG - Burgundy - Crinkle | +15% markup, deep red texture |
| CMBS-CR | CMG - Burnished Slate Crinkle | +15% markup, blue-gray texture |
| CMCG-CR | CMG - Classic Green - Crinkle | +15% markup, green texture |
| CMCR-CR | CMG - Colonial Red - Crinkle | +15% markup, red texture |
| CMDBZ-CR | CMG - Dark Bronze - Crinkle | +15% markup, bronze texture |
| CMHG-CR | CMG - Hartford Green - Crinkle | +15% markup, green texture |
| CMMG-CR | CMG - Musket Gray - Crinkle | +15% markup, gray texture |
| CMST-CR | CMG - Sierra Tan - Crinkle | +15% markup, tan texture |
| CMSG-CR | CMG - Slate Gray - Crinkle | +15% markup, gray texture |
| CMTC-CR | CMG - Terra Cotta - Crinkle | +15% markup, orange-red texture |

---

## CMG Matte/Ultra Low Gloss Colors (~4 colors) — PREMIUM +15%

*Kynar/PVDF with ultra low gloss (ULG) matte finish, 24/26ga, premium non-reflective*

| Code | Color Name | Premium Notes |
|------|-----------|----------------|
| CMBK-ULG | CMG - BLACK MATTE ULG | +15% markup, non-reflective black |
| CMBS-ULG | CMG - Burnished Slate – MATTE ULG | +15% markup, blue-gray matte |
| CMCG-ULG | CMG - Charcoal Gray – MATTE ULG | +15% markup, dark gray matte |
| CMSG-ULG | CMG - Slate Gray – MATTE ULG | +15% markup, gray matte |

---

## Hixwood Legacy Colors (5 colors)

*Older supplier, phased out. Maintained for legacy compatibility.*

| Code | Color Name | Status |
|------|-----------|--------|
| HIX-BS | Burnished Slate - Hixwood | Phased out |
| HIX-EB | Hixwood - Earth Brown | Phased out |
| HIX-FG | Hixwood - Forest Green | Phased out |
| HIX-W | Hixwood - White | Phased out |
| HIX-RC | Red Cedar - Hixwood | Phased out |

---

## Industrial/Specialty Colors (3 colors)

| Code | Color Name | Use Case |
|------|-----------|----------|
| BOND | BONDERIZED | Raw steel substrate (pre-paint) |
| CLR | CLEAR | Transparent/no finish |
| QQ | Quote Color | TBD in quoting system |

---

## Supplier Mapping & Paint Systems

### USS (SMP Paint)
- **Supplier:** USS Steel / SMP (Standard Metal Products)
- **Gauges:** 29ga, 26ga
- **Warranty:** 30 years
- **Colors:** ~70 total (47 standard + 16 crinkle + 7 matte)
- **Premium Finishes:** Crinkle (CR) = +15%, Matte (MCC) = +8%
- **Coil Width:** 29ga = 40.875", 26ga = 41.5625" (Grade 50) / 43" (Grade 80)
- **Application:** Primarily residential, commercial trim, flashing

### CMG (Kynar/PVDF)
- **Supplier:** CMG Coated Metals (or equivalent premium coil supplier)
- **Gauges:** 24ga, 26ga
- **Warranty:** 40 years (Kynar PVDF paint)
- **Colors:** ~56 total (42 standard + 10 crinkle + 4 matte)
- **Premium Finishes:** Crinkle (CR) = +15%, Matte/ULG = +15%
- **Coil Width:** 24ga = 20", 26ga = varies
- **Application:** Premium residential, panels, high-durability requirements
- **Note:** CMG is the Kynar premium paint supplier

### Hixwood (Discontinued)
- **Legacy colors** maintained for compatibility with older orders
- Phased out in favor of USS/CMG

---

## Color Code Extraction Examples

### Reading a Product SKU
```
CO4129ARW10
├─ CO = Coil prefix
├─ 41 = Width (40.875")
├─ 2 = Gauge shorthand (29ga)
├─ 9 = Color lookup → ARW = Arctic White
├─ (nothing) = No premium finish
└─ 10 = Length (10')

RC144CR10
├─ RC = Ridge Cap prefix
├─ 1 = Width identifier
├─ 4 = Gauge shorthand (24ga)
├─ CR = Premium finish (Crinkle, +15%)
└─ 10 = Length (10')
```

### Finish Detection Rules
1. **After gauge digit:** MCC, CR, ULG = premium finish
2. **In profile prefixes:** CR, RC, CRRC = NOT a finish code
3. **Examples:**
   - `ANG119CR10` → Angle, 29ga, **Crinkle finish** (+15%) ✓
   - `CRRC104BK10` → Commercial Rib Rake & Corner, 29ga, Black, (no premium) ✓

---

## Pricing Markup Summary

### Standard Finish
- No multiplier (×1.0)
- Base pricing

### Premium Finish
- **Crinkle (CR):** ×1.15 (+15%)
- **Matte (MCC):** ×1.08 (+8%)
- **Ultra Low Gloss (ULG):** ×1.15 (+15%)

### Example Calculation
```
Base Price: $100
Gauge 29ga: $100 × 1.0 = $100
Gauge 26ga: $100 × 1.2 = $120
Gauge 24ga: $100 × 1.44 = $144

Add Crinkle: $100 × 1.15 = $115 (standard + crinkle)
Add Matte: $100 × 1.08 = $108 (standard + matte)
```

---

## Historical Notes

**Paradigm Integration:** All color codes map via `CATALOG_TO_PARADIGM_MATCHED.csv` to Paradigm product records

**Analysis Date:** Based on 2026-03-28 inventory snapshot with 134 confirmed standard colors

**Rogue Colors Identified:**
- "Quote Color" (501 SKUs) — handled in quoting system separately
- "Matte Charcoal" (478 SKUs) — merged with standard Charcoal Gray variants
- "Hawaiian Blue" (339 SKUs) — legacy variant
- "Crinkle Charcoal" (339 SKUs) — mapped to Charcoal Gray Crinkle

---

## Quick Reference Cheat Sheet

| Supplier | Paint Type | Gauge | Warranty | Premium Finishes |
|----------|-----------|-------|----------|------------------|
| **USS** | SMP | 29, 26 | 30yr | CR (+15%), MCC (+8%) |
| **CMG** | Kynar | 24, 26 | 40yr | CR (+15%), ULG (+15%) |

**Detection:** If finish code (MCC/CR/ULG) appears **after gauge digit** → apply markup
**Most Popular:** Arctic White (ARW) — USS standard
**Premium Default:** Crinkle (CR) — +15% across both suppliers
