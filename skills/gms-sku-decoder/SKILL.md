---
name: gms-sku-decoder
description: "Decode, encode, and look up Greenfield Metal Sales product IDs (PIDs/SKUs). Use this skill whenever the user mentions a product code like 'PCF9ARW10', asks 'what is this product', wants to generate a SKU from a description like '10\" Ridge Cap, 26ga, Charcoal, 12ft', needs to look up product specifications, or asks about product families, color codes, gauge options, or material sourcing. Also trigger when the user pastes a list of product IDs and wants them decoded, asks 'what coil does this trim come from', or needs to understand any GMS product identifier. This is the product intelligence brain for GMS — use it even for partial product questions like 'what gauge is this' or 'what color is ARW'."
---

# GMS SKU Decoder & Product Intelligence

The authoritative system for decoding, encoding, and understanding Greenfield Metal Sales product identifiers. Every product in Paradigm ERP has a structured Product ID (PID) that encodes the product family, gauge, color, and length. This skill knows how to read and write those codes fluently.

## Capabilities

1. **Decode** — Turn any PID into human-readable specs (`PCF9ARW10` → "Pitch Change Flashing, 29ga, Arctic White, 10ft")
2. **Encode** — Turn a description into a valid PID ("12\" Ridge Cap, 26ga, Matte Black, 14ft" → `RC6MBB14`)
3. **Look up** — Get full product specifications, material sources, available variants, and pricing category
4. **Batch decode** — Process lists of PIDs at once
5. **Validate** — Check if a PID follows valid encoding rules and whether the product likely exists

---

## PID Anatomy

Every GMS product ID follows this structure:

```
{FAMILY}{GAUGE_DIGIT}{COLOR_CODE}{LENGTH}
```

### Component Breakdown

| Component | Position | Format | Examples |
|-----------|----------|--------|----------|
| **Family** | Start | 1–11 chars | `PCF`, `RC`, `HFBT`, `CRD81`, `SSQ675` |
| **Gauge Digit** | After family | Single digit | `9`=29ga, `6`=26ga, `4`=24ga |
| **Color Code** | After gauge | 1–8 chars | `ARW`, `BK`, `CMGALM`, `MBB`, `AWC` |
| **Length** | End (trims only) | 2 digits | `10`=10ft, `12`=12ft, `14`=14'6" |

**Important exceptions:**
- **Panels** have NO length code (e.g., `PRO6AG`, `SSQ6754CMGAC`)
- **Coils** use format `CO{WIDTH}{GAUGE}{COLOR}` (e.g., `CO4129ARW`)
- **Flatsheets** use format `FS{WIDTH}{GAUGE}{COLOR}` (e.g., `FS2026AG`)
- **A9/A6 panels** embed gauge in the family name, not a digit (e.g., `A9AG` = Ag Panel 29ga)

---

## Decoding Rules

### Step 1: Identify the Product Type

| If PID starts with... | It's a... | Length code? |
|----------------------|-----------|-------------|
| `CO` | Coil (raw material) | No |
| `FS` | Flatsheet (raw material) | No |
| `PRO`, `BBQ750`, `SSQ550`, `SSQ675`, `FF100`, `TRAPEZOID` | Panel | No |
| `A9` | Ag Panel 29ga | No |
| `A6` | Ag Panel 26ga / Greenfield Classic | No |
| Everything else | Trim/Flashing | Yes (2 digits at end) |

### Step 2: Extract the Family Prefix

The family prefix is everything before the gauge digit. This requires knowing valid family prefixes because some families have numeric characters in them (like `CRD81`, `ANG11`, `RC10`).

**Parsing strategy:** Match against the known family registry (see `references/family-registry.md`). Start with the longest possible prefix and work backwards until you find a match followed by a valid gauge digit (4, 6, or 9).

**Tricky families with embedded numbers:**
- `CRD81` → Crown Drip 8×1 (not CRD + gauge 8)
- `CRD1011` → Crown Drip 10×11 (not CRD + gauge 1)
- `ANG11` → Angle 1×1 (not ANG + gauge 1)
- `ANG22` → Angle 2×2
- `RC10` → Ridge Cap 10" (not RC + gauge 1)
- `RC14` → Ridge Cap 14"
- `RC20`, `RC24` → Ridge Cap 20", 24"
- `BBQ750` → Board & Batten panel (not BB + Q)
- `SSQ550`, `SSQ675` → Standing Seam panels
- `FF100` → Flush Flat panel

### Step 3: Extract the Gauge

The gauge digit appears immediately after the family prefix:

| Digit | Gauge | Weight | Coil Cost Tier | Notes |
|-------|-------|--------|----------------|-------|
| `9` | 29ga | Lightest | Lowest | Most common for residential |
| `6` | 26ga | Medium | Middle | Standard commercial |
| `4` | 24ga | Heaviest | Highest | **CMG colors ONLY** — no US Standard in 24ga |

**Special cases:**
- `A9` and `A6` — gauge is in the family name, no separate digit
- `TRAPEZOIDT6` — includes a `T` before the gauge digit

### Step 4: Extract the Color Code

Everything between the gauge digit and the length code (or end of PID for panels/coils) is the color code.

**Color Code Categories:**

| Category | Pattern | Example Codes | Premium? |
|----------|---------|---------------|----------|
| US Standard | 1–3 letters | `ARW`, `BK`, `B`, `AG`, `CH` | No |
| US Crinkle | Standard + `C` | `AWC`, `AGC`, `BKC` | Yes (+15%) |
| US Matte | `M` + letters | `MBB`, `MBW`, `MBS`, `MCH` | Yes (+8%) |
| CMG Standard | `CMG` + abbrev | `CMGALM`, `CMGAG`, `CMGBK` | No (cost in coil) |
| CMG Crinkle | CMG + base + `C` | `CMGBRC`, `CMGCHC` | Yes (+15%) |
| CMG ULG | CMG + base + `M` | `CMGBURM`, `CMGBKM` | Yes (+15%) |
| Woodgrain | Unique 2–3 letters | `BP`, `BBW`, `BZ`, `CW` | Special pricing |

For the complete color code lookup table, read `references/color-to-code.md`.

### Step 5: Extract Length (Trims Only)

The last 2 digits of a trim PID indicate length in feet:

| Code | Actual Length | Pricing Multiplier |
|------|-------------|-------------------|
| `10` | 10ft (or 10'3", 10'6") | 1.00 (base) |
| `12` | 12ft (12'3" or 12'6") | 1.20 |
| `14` | 14'6" | 1.40 |
| `16` | 16'6" | 1.60 |
| `18` | 18'6" | 1.80 |
| `20` | 20ft | Special |

---

## Encoding Rules

To generate a PID from a description:

1. **Identify the product family** — match the description to a known family prefix
2. **Determine the gauge** — map to digit (29ga→9, 26ga→6, 24ga→4)
3. **Look up the color code** — find the correct abbreviation for the color name
4. **Add length** — if it's a trim product, append the 2-digit length code
5. **Validate** — check that the combination is valid (e.g., 24ga only exists with CMG colors)

**Encoding example:**
- Input: "12-inch Ridge Cap, 26ga, Charcoal Gray, 14 feet"
- Family: RC (Ridge Cap) → with 12" width modifier, need to check if RC or RC12 is the correct family
- Gauge: 26ga → `6`
- Color: Charcoal Gray → `CG`
- Length: 14ft → `14`
- Output: `RC6CG14` (or `RC126CG14` if the width is part of the family prefix)

**Validation rules:**
- 24ga gauge digit `4` requires CMG color code (starts with `CMG`)
- Panels never have length codes
- Coils use `CO{WIDTH}{GAUGE}{COLOR}` format
- All family prefixes must match the known registry

---

## Coil PID Format

Coils follow a different structure:

```
CO{WIDTH_DIGIT}{GAUGE_DIGIT}{COLOR_CODE}
```

| Width Digit | Actual Width | Primary Use |
|-------------|-------------|-------------|
| `20` or `2` | 20.0" | 131 trim families (Pattern A) |
| `41` or `4` | 40.875" | 8 trim families (Pattern B) + panels |
| `43` | ~43" | HFRG specialty |
| `48` | 48.375" | 24ga CMG panels |

**Examples:**
- `CO2026AG` → 20" coil, 26ga, Ash Gray
- `CO4129ARW` → 41" coil, 29ga, Arctic White
- `CO4326AG` → 43" coil, 26ga, Ash Gray (HFRG source)

---

## Material Source Mapping

Every trim product traces back to a coil or flatsheet:

**Pattern A — 20" Material (131 families):**
Most standard trim families use 20-inch coils.

| Gauge | Primary Source | Backup |
|-------|---------------|--------|
| 29ga | CO2029{color} | FS2029{color} |
| 26ga | CO2026{color} | FS2026{color} |
| 24ga | FS2024{color} | — |

**Pattern B — 41" Material (8 families: HFVF, ODHC, RC20, RC24, VV, WV, WV24, WV36):**

| Gauge | Primary Source | Backup |
|-------|---------------|--------|
| 29ga | CO4129{color} | FS4129{color} |
| 26ga | CO4126{color} | FS4126{color} |
| 24ga | FS4124{color} | — |

**HF Family Exception:**
HF trim families use 41" material despite most trims using 20":
- CMG colors → `FS4126CMG{abbrev}` (flatsheet, sold EA)
- US colors (HFBT/HFDF/HFJT) → `CO4129{color}` (coil, sold LF)
- US colors (HFRG) → `CO4326{color}` (43" coil)

---

## Product Categories

Understanding the category determines margin targets and pricing behavior:

| Category | Family Examples | Margin Target | Has Length? |
|----------|----------------|---------------|-------------|
| Trim & Flashing | PCF, RC, DE, GA, ANG, CRD, HFBT... | 50% | Yes |
| Exposed Fastener Panel | PRO, A9, A6 | 35% | No |
| Hidden Fastener Panel | SSQ550, SSQ675, FF100, BBQ750 | 40% | No |
| Coil | CO* | 30–40% | No |
| Flatsheet | FS* | 30–40% | No |

---

## Reference Files

| File | Contents | When to Read |
|------|----------|--------------|
| `references/family-registry.md` | All 211+ family prefixes with descriptions, stretchout, material pattern | When decoding a family prefix or looking up product specs |
| `references/color-to-code.md` | Complete bidirectional color name ↔ code mapping for all 166 colors | When encoding a color name to a code, or decoding a code to a name |

---

## Helper Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/sku_decoder.py` | Decode one or many PIDs | `python sku_decoder.py PCF9ARW10 RC6CMGALM12` |
| `scripts/sku_encoder.py` | Encode descriptions to PIDs | `python sku_encoder.py "Ridge Cap, 26ga, Ash Gray, 12ft"` |

---

## Cross-References to Other GMS Skills

- **Pricing Engine** — After decoding a PID, use the pricing engine to calculate its price. The decoder provides gauge, length, and finish type that feed directly into the pricing formula.
- **Material Estimator** — The decoder identifies which products are needed; the estimator calculates quantities.
- **Inventory Health** — Decode PIDs in inventory reports to understand what's in stock by family/gauge/color.
