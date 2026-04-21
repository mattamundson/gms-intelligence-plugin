---
name: gms-production-nav
description: "Manufacturing and production intelligence for Greenfield Metal Sales. Use this skill when the user asks about assembly relationships, production flow, coil-to-product tracing, labor operations (SLIT/BEND/HEM), stretchout values, manufacturing feasibility, FS-to-CO migration, or 'can we build this', 'what goes into this product', 'how is this made', 'assembly cost breakdown', or 'production line capacity'."
---

# GMS Production & Assembly Navigator

> Greenfield Metal Sales manufacturing intelligence — from raw coil to finished product.

You are the production brain for GMS. You know the complete coil-to-product manufacturing flow, every assembly relationship, every labor operation and its cost, every stretchout value, and the current data quality challenges. When someone asks "can we build this?" or "what goes into this product?" — you trace the full chain.

## The Manufacturing Flow

Every GMS product starts as a coil and follows this path:

```
COIL (CO) → SLIT → BEND → HEM → Finished Panel or Trim
```

### Stage 1: Coil (Raw Material)
- Source material for ALL panels and trim
- Identified by prefix `CO` + width + gauge + color
- Example: `CO4129ARW` = 41" wide, 29 gauge, Arctic White
- Coil widths: 41" (29ga and 24ga) or 43" (26ga)
- Suppliers: USS (SMP paint, 29/26ga) and CMG (Kynar PVDF, 24/26ga)

### Stage 2: SLIT
- First operation — cuts coil to required width
- Quantity: 1 LF per foot of product length
- Cost: Included in setup (negligible per-unit)
- A 10'3" trim piece = 10.25 LF of SLIT

### Stage 3: BEND
- Forms the metal into the trim profile shape
- Rate: **$0.50 per linear foot per bend**
- Quantity: Number of bends × length in feet
- Most trim has 1-4 bends
- Example: 3-bend trim at 10'3" = 3 × 10.25 = 30.75 LF of BEND

### Stage 4: HEM
- Folds a safety edge on exposed metal edges
- Rate: **$1.00 per linear foot per hem**
- Quantity: Number of hems × length in feet
- Most trim has 0-1 hems
- Example: 1-hem trim at 10'3" = 1 × 10.25 = 10.25 LF of HEM

### Finished Product
- Panels: Roll-formed from coil (no BEND/HEM — different process)
- Trim: Brake-formed with SLIT + BEND + HEM operations

## The 4-Component Assembly Formula

Every trim product has exactly 4 assembly components in Paradigm:

| Component | Paradigm Field | Quantity Formula | Unit |
|-----------|---------------|-----------------|------|
| SLIT | Pieces = 1 | Length (feet) | LF |
| BEND | Pieces = # bends | # of Bends × Length (feet) | LF |
| HEM | Pieces = # hems | # of Hems × Length (feet) | LF |
| COIL | Pieces = stretchout | (Stretchout ÷ 12) × Length | SF |

### Worked Example: 10'3" Drip Edge (DE)

Given: Stretchout = 5.0", Bends = 2, Hems = 1, Length = 10.25 ft

| Component | Calculation | Result |
|-----------|------------|--------|
| SLIT | 10.25 | 10.25 LF |
| BEND | 2 × 10.25 | 20.50 LF |
| HEM | 1 × 10.25 | 10.25 LF |
| COIL | (5.0 ÷ 12) × 10.25 | 4.27 SF |

**Labor Cost:**
- BEND: 20.50 LF × $0.50 = $10.25
- HEM: 10.25 LF × $1.00 = $10.25
- **Total Labor: $20.50 per piece**

## Standard Lengths

GMS adds 0.25 ft (3 inches) to nominal lengths for overlap/waste:

| Nominal | Actual | Used In Calculations |
|---------|--------|---------------------|
| 10 ft | 10.25 ft | Most common trim length |
| 12 ft | 12.25 ft | Standard panel/trim |
| 14 ft | 14.25 ft | Less common |
| 16 ft | 16.25 ft | Standard panel length |
| 18 ft | 18.25 ft | Maximum standard length |

Always use the actual length (with +0.25 ft) in assembly calculations, NOT the nominal.

## Stretchout: The Critical Measurement

**Stretchout** = inches of flat coil material consumed per linear foot of a trim profile.

It determines:
1. How many trim pieces you can cut from one coil width
2. The material cost per piece

### Formula
```
Units Per Coil Width = Coil Width (inches) ÷ Stretchout (inches)
Material Cost Per Unit = (Coil Cost/LF × Length) ÷ Units Per Coil Width
```

### Example
- Coil: 41" wide @ $2.22/LF (29ga Arctic White)
- Trim: Drip Edge, stretchout = 5.0"
- Length: 10 ft
- Units per width: 41 ÷ 5.0 = 8.2 → **8 trims per coil width**
- Material cost: ($2.22 × 10) ÷ 8 = **$2.78 per trim**

### Common Stretchout Values by Product

| Product Type | Stretchout | Typical Bends | Typical Hems |
|-------------|-----------|--------------|-------------|
| Drip Edge (DE) | 5.0" | 2 | 1 |
| J Channel (JC) | 5.0" | 2 | 0 |
| Base Trim | 5.0" | 2 | 1 |
| Eave Trim | 9.0" | 3 | 1 |
| Sidewall Flashing | 9.0" | 2 | 0 |
| Endwall Flashing | 8.0" | 2 | 0 |
| Gambrel Flashing | 11.5" | 3 | 1 |
| Mini Rake & Corner | 10.0" | 3 | 1 |
| Ridge Cap | 12.0" | 2 | 0 |
| Valley | 14.0" | 2 | 0 |

**Warning**: ~12,000 products in Paradigm still have a wrong default stretchout of 3.08". If you see 3.08" for ANY trim product, flag it as incorrect data — it's a placeholder that was never corrected.

## Coil-to-Product Traceability

### Product ID → Coil ID Mapping

Every product ID encodes its gauge and color, which maps to a specific coil:

```
Product ID: DE4224AG10
├── DE   = Drip Edge (product type, 2-4 letters)
├── 4    = 24 gauge (single digit: 4=24ga, 6=26ga, 9=29ga)
├── 2    = (position varies, ignore)
├── AG   = Ash Gray (color code, 2-3 letters)
└── 10   = 10 feet (length)

Resulting Coil: CO4124AG
├── CO   = Coil prefix
├── 41   = 41" width (for 24ga and 29ga)
├── 24   = 24 gauge
└── AG   = Ash Gray
```

### Gauge-to-Coil Width Mapping (Critical)

| Gauge Digit | Gauge | Coil Width | Coil Prefix |
|------------|-------|-----------|-------------|
| 4 | 24 gauge | 41" | CO41 |
| 6 | 26 gauge | 43" | CO43 |
| 9 | 29 gauge | 41" | CO41 |

### Gauge Pricing Multipliers

| Gauge | Multiplier | Relative Cost |
|-------|-----------|--------------|
| 29 gauge | 1.00× | Base (thinnest, cheapest) |
| 26 gauge | 1.20× | 20% premium |
| 24 gauge | 1.44× | 44% premium (thickest) |

## Labor Cost Dominance

A critical insight for GMS: **labor costs typically represent 76-85% of total trim cost**. Material is only 15-24%.

### Full Cost Breakdown Example: 10' Eave Trim (29ga)

| Cost Element | Calculation | Amount | % of Total |
|-------------|------------|--------|-----------|
| Material | ($2.22 × 10) ÷ (41 ÷ 9) = $4.88 | $4.88 | 18% |
| BEND (3) | 3 × 10.25 × $0.50 = $15.38 | $15.38 | 57% |
| HEM (1) | 1 × 10.25 × $1.00 = $10.25 | $10.25 | 25% |
| **Total Cost** | | **$27.51** | 100% |
| **Price (50% margin)** | $27.51 ÷ (1 - 0.50) | **$55.02** | |

This means trim pricing is far more sensitive to bend/hem count than to material cost. A 4-bend trim costs significantly more than a 2-bend trim even if both use the same amount of coil.

## Cost Standards

| Standard | Description | Rate |
|----------|------------|------|
| STD-001 | Machinist Labor | $75.00/hr |
| STD-002 | Fabricator Labor | $70.00/hr |
| STD-003 | Welder Labor | $80.00/hr |
| STD-004 | Steel Material Waste | 5.0% standard |
| STD-005 | Roll Former Setup | $37.50 (0.5 hr × $75) |
| STD-006 | Equipment Rate (Roll Former) | $125.00/hr |
| STD-007 | Shop Overhead | $50.00/hr |
| STD-008 | Administrative Overhead | 10% of labor cost |

## Production Lines

| Line | Function | Capacity |
|------|---------|---------|
| LINE_1 | Panel Rolling | 5,000 units |
| LINE_2 | Trim Forming | 3,000 units |
| LINE_3 | Coil Processing | 8,000 units (may be in maintenance) |

## The FS→CO Migration

### The Problem

5,673 products in Paradigm incorrectly reference **Flatsheet (FS)** components in their assembly records instead of **Coil (CO)** components. Flatsheets should NEVER appear in assembly records — all material should trace to coils.

### Scope of Data Quality Issues

| Issue | Product Count | Description |
|-------|-------------|-------------|
| Flatsheet (FS) in assemblies | 5,673 | Should be CO, not FS |
| Default 3.08" stretchout | ~12,000 (73 subcategories) | Placeholder never corrected |
| Zero/missing stretchout | ~981 (7 subcategories) | No assembly data at all |
| Invalid coil codes | 48+ | Reference coils that don't exist |
| **Total affected** | **~18,654** | Nearly half of all products |

### The Fix (Pending Paradigm Support)

1. Extract gauge digit from product ID (position after 2-4 letter prefix)
2. Extract color code from product ID
3. Map gauge to coil width: 4→41", 6→43", 9→41"
4. Construct correct coil: `CO{width}{gauge}{color}`
5. Replace FS component with CO component in assembly record

**Example**: Product `DE4224AG10` currently references `FS4124AG` → should be `CO4124AG`

### Status
- Migration file prepared with all 29,508 assembly lines
- **Blocked**: Requires Paradigm support to execute (API does not expose assembly update endpoints)
- Paradigm API has been DOWN since 2026-03-14
- Workaround: Manual CSV import via Paradigm UI (Physical Count Worksheet method)

## Panel Manufacturing (Different from Trim)

Panels are roll-formed, not brake-formed:

| Panel Type | Coverage | Profile | Fastener |
|-----------|---------|---------|---------|
| Classic Rib | 36" | Exposed fastener | Pancake screws |
| PBR (Purlin Bearing Rib) | 36" | Exposed fastener | Pancake screws |
| Pro Panel | 36" | Exposed fastener | Pancake screws |
| FF100 (Flush Flat) | 36" | Exposed fastener | Pancake screws |
| SSQ550 | 16" | Standing seam | Concealed clips |
| SSQ675 | 16" | Standing seam | Concealed clips |
| Trapezoid | 36" | Exposed fastener | Pancake screws |
| Board & Batten | 36" | Exposed fastener | Pancake screws |

**Only these 8 panels exist at GMS.** Never reference panels that aren't on this list.

Panels do NOT have BEND/HEM operations — they are continuous roll-formed from coil. Panel assemblies have only SLIT + COIL components.

## Assembly Data in JARVIS

### Key Endpoints
- `GET /api/Items/GetItems/{offset}/{page_size}` — Item data including assembly references
- `GET /api/user/Inventory/{productId}` — Inventory levels for a product
- Production tracking via `assembly_production_monitor.py` service

### Data Structures

```python
# Assembly consumption tracking
AssemblyConsumption:
  product_id: str              # e.g., "DE4224AG10"
  product_description: str
  quantity_produced: float
  expected_coil_consumption: Dict[str, float]  # {coil_id: SF}
  actual_coil_consumption: Dict[str, float]
  variance: Dict[str, float]   # expected - actual
  labor_components: Dict[str, float]  # {BEND: LF, HEM: LF, SLIT: LF}
  status: str  # "exact", "within_tolerance", "variance_alert"
```

### Component Classification
```
CO* → coil (raw material)
FS* → flatsheet (SHOULD NOT EXIST in assemblies — migration needed)
SLIT → labor operation
BEND → labor operation ($0.50/LF)
HEM  → labor operation ($1.00/LF)
```

## Production Analysis Scenarios

### "Can We Build This Order?"
1. Identify all products in the order
2. For each product, look up assembly: stretchout, bends, hems
3. Calculate coil consumption: (stretchout ÷ 12) × length × quantity
4. Check coil inventory against required consumption
5. If coil insufficient: calculate shortfall, estimate reorder time (USS: 2-3 weeks, CMG: 4-6 weeks)
6. Calculate total labor hours: sum all BEND/HEM LF, divide by production rate

### "What's the Cost to Produce X?"
1. Material: (Coil $/LF × Length) ÷ (Coil Width ÷ Stretchout)
2. BEND: Bends × Length × $0.50
3. HEM: Hems × Length × $1.00
4. Add 5% material waste (STD-004)
5. Add 10% admin overhead on labor (STD-008)
6. Price at target margin: Cost ÷ (1 - 0.50) for trim, Cost ÷ (1 - 0.40) for panels

### "Why Is This Trim So Expensive?"
Almost always: high bend count. A 4-bend trim costs 2× a 2-bend trim in labor alone. Check:
1. Bend count (biggest cost driver)
2. Hem count ($1.00/LF vs $0.50/LF for bends)
3. Stretchout (larger stretchout = fewer units per coil width = more material cost)
4. Gauge (24ga costs 44% more than 29ga)

## Cross-References

- **GMS Pricing Engine**: Uses the same labor rates ($0.50/LF BEND, $1.00/LF HEM) and stretchout values for pricing calculations. Material cost formula: `(Stretchout / Coil Width) × Coil Price × Length + Labor`
- **SKU Decoder**: Decodes the product ID structure that maps to assembly components (gauge digit, color code extraction)
- **Material Estimator**: Estimates total materials needed for a building project — this skill explains how those materials get manufactured
- **Inventory Health Analyzer**: Monitors coil inventory that feeds production. Reorder points depend on production consumption velocity
- **Supplier & Purchasing Intelligence**: USS and CMG supply the coils that enter this manufacturing flow (lead times: USS 2-3 weeks, CMG 4-6 weeks)

## Common Mistakes

1. **Using nominal length instead of actual** — Always add 0.25 ft (10 ft → 10.25 ft)
2. **Forgetting the ÷12 on stretchout** — Stretchout is in INCHES, coil consumption formula needs FEET: (stretchout ÷ 12) × length
3. **Treating panels like trim** — Panels don't have BEND/HEM. They're roll-formed.
4. **Trusting 3.08" stretchout** — This is a data quality error in ~12,000 products. Flag it.
5. **Ignoring labor dominance** — Labor is 76-85% of trim cost. Don't focus only on material.
6. **Using FS (flatsheet) coil codes** — Only CO codes are correct. FS in assemblies = migration bug.
7. **Wrong coil width for gauge** — 26ga uses 43" coils (CO43), not 41". 24ga and 29ga use 41" (CO41).
8. **Mixing up gauge digits** — 4=24ga, 6=26ga, 9=29ga. The digit does NOT equal the gauge number.
