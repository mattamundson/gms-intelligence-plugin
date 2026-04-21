---
name: gms-pricing-engine
description: "Calculate, validate, and analyze pricing for Greenfield Metal Sales trim, panel, and coil products. Use this skill whenever the user mentions pricing, quotes, margins, cost calculations, price sheets, markup, price updates, price validation, what-if pricing scenarios, or asks questions like 'how much does X cost', 'what's the margin on Y', 'generate a quote for Z', 'validate these prices', or 'what happens to margins if coil costs go up'. Also trigger when the user references stretchout calculations, gauge/length multipliers, premium finish markups, or coil-to-trim cost formulas. This is the authoritative pricing brain for GMS — use it even if the user doesn't explicitly say 'pricing' but is clearly working with product costs, sell prices, or margins."
---

# GMS Pricing Engine

The authoritative pricing calculation and analysis system for Greenfield Metal Sales. This skill encodes the complete pricing matrix, business rules, and validation logic so that every quote, price review, and margin analysis is accurate on the first pass.

## When to Use This Skill

- Calculating a price for any GMS product (trim, panel, coil, accessory)
- Generating customer quotes (inline, XLSX, PDF, or JSON)
- Validating existing pricing for consistency
- Analyzing margins across products, families, or categories
- Running "what-if" scenarios (e.g., coil cost changes, margin target adjustments)
- Performing bulk pricing updates or reviews
- Answering questions about how GMS pricing works

## Safety Rail

**NEVER auto-execute pricing changes to Paradigm.** Always generate a preview, show before/after, and require explicit "APPLY" or "CONFIRM" from Matt before writing any price data. This is non-negotiable — pricing errors affect live production data, customer quotes, and revenue.

---

## The Pricing Formula

Every GMS product's sell price derives from one core equation:

```
Sell Price = Base Price × Gauge Multiplier × Length Multiplier × Finish Multiplier
```

Where **Base Price** is the sell price of the simplest variant in a product family: 29ga, 10' length, standard (non-premium) finish.

### Gauge Multipliers

Metal thickness increases cost progressively. Each step up is +20% over the previous gauge:

| Gauge | Multiplier | Relationship |
|-------|-----------|--------------|
| 29ga  | 1.00      | Base         |
| 26ga  | 1.20      | +20% over 29ga |
| 24ga  | 1.44      | +20% over 26ga (= +44% over 29ga) |

The gauge digit in a product ID tells you the gauge: `9` = 29ga, `6` = 26ga, `4` = 24ga.

### Length Multipliers

Longer pieces cost proportionally more. Each ~2-foot increment adds +20%:

| Length         | Multiplier | Relationship |
|----------------|-----------|--------------|
| 10', 10'3", 10'6" | 1.00  | Base         |
| 12'3", 12'6"  | 1.20      | +20%         |
| 14'6"         | 1.40      | +40%         |
| 16'6"         | 1.60      | +60%         |
| 18'6"         | 1.80      | +80%         |

The length code appears at the end of the product ID: `10` = 10', `12` = 12', `14` = 14'6", `16` = 16'6", `18` = 18'6".

### Finish Multipliers (Premium Detection)

Most colors are standard finish (1.00 multiplier). Three premium finishes carry markups:

| Finish | Code | Multiplier | Notes |
|--------|------|-----------|-------|
| Standard | (any standard color) | 1.00 | No premium |
| Matte | MCC | 1.08 | +8% over standard |
| Crinkle | CR + color | 1.15 | +15% over standard |
| Ultra Low Gloss | ULG | 1.15 | +15% over standard |

**Critical: Detecting premium finishes in product IDs**

Premium finish codes appear AFTER the gauge digit in the color portion of the ID — not in the profile prefix. This distinction is essential because some profile prefixes contain "CR" (like CRD = Crown Drip, CRRC = Crown Ridge Cap) which are NOT premium finishes.

Detection logic:
1. Find the gauge digit (4, 6, or 9) in the product ID
2. Extract the color code that follows the gauge digit
3. Check if the color code starts with MCC, ULG, or CR followed by a color code

**Premium examples:**
- `PCF9MCC10` → gauge `9`, color starts with `MCC` → Matte premium (+8%)
- `PCF9CRBK10` → gauge `9`, color starts with `CR` + `BK` → Crinkle Black (+15%)
- `RAC169ULG` → gauge `9` (inside `169`), color `ULG` → Ultra Low Gloss (+15%)

**NOT premium (profile prefix contains CR):**
- `CRD8109ARW10` → `CRD` is the profile name (Crown Drip), not a finish
- `CRRC109ARW10` → `CRRC` is the profile name (Crown Ridge Cap)
- `CRDF9ARW10` → `CRDF` is the profile name (Crown Drip Flat)

---

## Target Margins

GMS prices products to achieve specific margin targets by category:

| Category | Target Margin | Formula |
|----------|--------------|---------|
| Trim & Flashing | 50% | Sell Price = Cost ÷ 0.50 |
| Exposed Fastener Panels (Classic Rib, PBR, Pro Panel, Ag Panel) | 35% | Sell Price = Cost ÷ 0.65 |
| Hidden Fastener Panels (SSQ550, SSQ675, FF100, BBQ750) | 40% | Sell Price = Cost ÷ 0.60 |
| Fasteners & Accessories | 50%+ | Sell Price = Cost ÷ 0.50 |
| Coils (raw material resale) | 30-40% | Varies by volume |

**Margin formula:** `Margin % = (Sell Price - Cost) / Sell Price × 100`

**Margin health classification:**
- Red Flag: below 25%
- Low: 25-35%
- OK: 35-45%
- Good: above 45%

---

## Cost Formula (Trim Products)

Trim cost derives from the material consumed (coil) plus labor operations:

```
Material Cost = (Stretchout ÷ Coil Width) × Coil Cost per LF × Length
Labor Cost = (Bends × $0.50/LF + Hems × $1.00/LF) × Length
Total Cost = Material Cost + Labor Cost
```

Where:
- **Stretchout** = inches of flat metal needed to form one linear foot of the profile (each profile has a fixed stretchout value)
- **Coil Width** = width of the source coil in inches (typically 20.0" or 40.875")
- **Coil Cost per LF** = cost per linear foot of the source coil (varies by gauge, supplier, color)
- **Length** = piece length in feet
- **Bends** = number of brake bends in the profile (BEND operation = $0.50/LF)
- **Hems** = number of hems in the profile (HEM operation = $1.00/LF)

For detailed stretchout values, bend counts, and hem counts for all 211 trim families, read `references/trim-profiles.md`.

---

## Product Family Structure

Products are organized into families. All products in a family share the same profile — they differ only by gauge, color, and length. When pricing one product in a family, all related variants follow the multiplier rules.

**Family extraction from product ID:**
- `PCF9ARW10` → Family: `PCF` (matches PCF4*, PCF6*, PCF9*)
- `RC109ARW10` → Family: `RC10` (matches RC104*, RC106*, RC109*)
- `CRD8109ARW10` → Family: `CRD810` (matches CRD8104*, CRD8106*, CRD8109*)

The pattern: everything before the gauge digit + width code = the family identifier.

---

## The 8 Real Panels

GMS manufactures exactly 8 panel products. These are the only panels that exist:

| Panel | Type | Gauges | Coverage | Category |
|-------|------|--------|----------|----------|
| Classic Rib | Exposed Fastener | 29, 26, 24 | 36" | EF (35% margin) |
| PBR | Exposed Fastener | 29, 26 | 36" | EF (35% margin) |
| Pro Panel (R-Panel) | Exposed Fastener | 29, 26 | 36" | EF (35% margin) |
| Ag Panel | Exposed Fastener | 29, 26 | 36" | EF (35% margin) |
| SSQ550 | Hidden Fastener | 29, 26, 24 | — | HF (40% margin) |
| SSQ675 | Hidden Fastener | 29, 26, 24 | — | HF (40% margin) |
| FF100 (Flush Flat) | Hidden Fastener | 26, 24 | — | HF (40% margin) |
| BBQ750 (Board & Batten) | Hidden Fastener | 26, 24 | — | HF (40% margin) |

Panel pricing is per linear foot (LF) and varies by gauge and color/finish.

---

## Coil Reference Pricing

Coil costs fluctuate with steel markets. The skill includes a reference table of recent coil costs that serves as a reasonable default — but the user should always provide current costs when precision matters. If the user provides a coil cost, use it; otherwise, fall back to the reference table.

For the current reference coil pricing table, read `references/coil-pricing.md`.

---

## Suppliers

- **USS (United Steel Supply)** — SMP (standard paint) colors, 29ga and 26ga. WeatherXL 30-year warranty. ~120 colors.
- **CMG (Coated Metal Group)** — Kynar/PVDF premium paint, 24ga and 26ga. 40-year warranty. ~51 colors.

CMG coils cost more per foot than USS coils — this is baked into the coil cost, not a separate markup. When calculating cost, use the correct coil cost for the supplier/gauge combination.

---

## Output Formats

Adapt the output to the context:

### 1. Inline Calculation (for quick checks in conversation)
Show the math step by step:
```
Product: PCF6MCC10 (Profile, 26ga, Matte, 10')
Base Price (29ga/10'/std): $28.50
× Gauge (26ga): ×1.20 = $34.20
× Length (10'): ×1.00 = $34.20
× Finish (Matte): ×1.08 = $36.94
Sell Price: $36.94
```

### 2. XLSX/PDF (for customer-facing price sheets or internal reports)
Generate structured price sheets using the xlsx or pdf skills. Include:
- Product ID, description, gauge, length, color
- Cost, sell price, margin %
- Family groupings with subtotals
- Date generated and coil cost basis noted

### 3. JSON (for JARVIS API consumption)
Output structured data that JARVIS endpoints can consume:
```json
{
  "product_id": "PCF6MCC10",
  "family": "PCF",
  "profile": "Profile",
  "gauge": "26ga",
  "length_ft": 10,
  "color": "MCC",
  "finish_type": "matte",
  "base_price": 28.50,
  "gauge_mult": 1.20,
  "length_mult": 1.00,
  "finish_mult": 1.08,
  "sell_price": 36.94,
  "cost": null,
  "margin_pct": null,
  "target_margin": 50.0,
  "category": "trim"
}
```

---

## Pricing Update Workflow

When Matt asks to update pricing for a product or family:

1. **Identify the scope** — which product(s) or family/families are affected
2. **Calculate new prices** — apply the formula across all gauge/length/finish variants
3. **Generate a preview** — show a table of all changes: Product ID, Current Price, New Price, Change %, Margin %
4. **Save the preview** to a file (CSV or XLSX) for review
5. **STOP and wait** for Matt to say "APPLY" or "CONFIRM"
6. **Only then execute** the changes

Never skip the preview step. Never auto-apply.

---

## What-If Scenarios

When Matt asks "what happens if...":
- **Coil cost changes:** Recalculate cost for affected products using the new coil cost, show the impact on margins at current sell prices, and suggest new sell prices to maintain target margins.
- **Margin target changes:** Show what sell prices would need to be at the new target.
- **Competitor pricing:** Compare GMS pricing against competitor prices and show where margins are above/below target.

---

## Validation Checks

When validating pricing, check for:
1. **Gauge consistency** — 26ga should be ~1.20× the 29ga price in the same family/color/length
2. **Length consistency** — 12' should be ~1.20× the 10' price in the same family/color/gauge
3. **Finish consistency** — Matte should be ~1.08× standard, Crinkle/ULG ~1.15× standard
4. **Margin health** — Flag any product below 25% margin as a red flag
5. **Family coherence** — All products in a family should follow the same multiplier pattern
6. **Outliers** — Any price that deviates more than 5% from what the formula predicts

---

## Reference Files

Read these as needed for detailed data:

| File | Contents | When to Read |
|------|----------|--------------|
| `references/trim-profiles.md` | 131 active trim families with stretchout, bends, hems, material pattern | When calculating trim costs or looking up profile specs |
| `references/panel-specs.md` | 8 panel types with coverage, gauges, pricing per LF | When working with panel pricing |
| `references/color-codes.md` | All color codes with premium finish detection | When decoding a product ID or checking finish type |
| `references/coil-pricing.md` | Reference coil costs by gauge/width/supplier | When no user-provided coil cost is available |
| `references/margin-tables.md` | Target margins by category, health thresholds | When analyzing margin health |

---

## Helper Scripts

For complex calculations, use the bundled Python scripts:

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/calculate_quote.py` | Calculate prices for one or many products | `python scripts/calculate_quote.py --product PCF9ARW10 --base-price 28.50` |
| `scripts/validate_pricing.py` | Check pricing consistency across a family or dataset | `python scripts/validate_pricing.py --input prices.csv` |
| `scripts/margin_analyzer.py` | Analyze margin health across products | `python scripts/margin_analyzer.py --input products.json --target-margins trim=50,ef_panel=35,hf_panel=40` |

---

## Cross-References to Other GMS Skills

This pricing engine is designed to work with other GMS skills:

- **SKU Decoder** — decode product IDs before pricing them; encode product specs into IDs
- **Material Estimator** — estimate materials needed for a project, then price the material list using this engine
- **Sales Outreach** — reference accurate pricing when generating quotes in customer communications
- **Inventory Health** — combine pricing data with inventory levels to identify dead stock by dollar value
