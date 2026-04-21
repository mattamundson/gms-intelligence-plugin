---
name: gms-material-estimator
description: Estimate metal roofing and siding materials for buildings — panels, trim, fasteners, and accessories. Dual-mode estimator with quick sales-grade estimates and engineering-grade detailed takeoffs. Use this skill whenever someone asks to estimate, calculate, take off, or figure out materials for a building, roof, wall, pole barn, machine shed, garage, house, or any structure. Also triggers on "how much metal do I need," "material list for," "bill of materials," "takeoff," "estimate panels for," "how many panels," "quote a building," or any request to calculate construction materials for a metal building project. Cross-references the GMS Pricing Engine and SKU Decoder for accurate product codes and pricing.
---

# GMS Metal Building Material Estimator

> Two modes: **Quick** (sales-grade, 30-second ballpark for phone calls and quotes) and **Detailed** (engineering-grade takeoff with complete BOM). Start Quick unless they ask for precision.

---

## Critical Rules

1. **GMS is supply-only.** Never include labor, installation, or framing in estimates. Materials only.
2. **Only real products.** Use only the 8 actual panel profiles and 131 trim families. Never invent products.
3. **Always include waste factor.** 5% minimum on panels, 10% on trim (cut waste from odd lengths).
4. **Round UP.** Always round panel counts and trim lengths up to the next whole unit. Contractors can't buy 2.3 panels.
5. **Default to 10' trim lengths** unless the customer specifies otherwise.
6. **State assumptions.** Every estimate must explicitly list what was assumed (pitch, overhang, waste factor, etc.).
7. **Pricing is separate.** This skill estimates quantities. Use the GMS Pricing Engine skill for dollar amounts. Include product codes so pricing can be plugged in.

---

## Mode 1: Quick Estimate (Sales-Grade)

Use for: phone quotes, rough budgets, initial conversations. Takes building dimensions and spits out approximate panel and trim counts in 30 seconds.

### Input Required
- Building type (pole barn, garage, house re-roof, commercial, etc.)
- Building dimensions (width × length × eave height)
- Roof pitch (or "low slope" / "standard" / "steep")
- Panel profile preference (or "cheapest" / "best")
- Wall panels needed? (yes/no)

### Quick Calculation Formulas

**Roof Area:**
```
Roof pitch multipliers (applied to footprint area):
  2:12 = 1.03     4:12 = 1.05     6:12 = 1.12
  8:12 = 1.20    10:12 = 1.30    12:12 = 1.41

Gable roof: Footprint × Pitch Multiplier × 2 sides
Hip roof:   Footprint × Pitch Multiplier × 2 sides (then subtract gable triangles)
Shed roof:  Footprint × Pitch Multiplier × 1 side
```

**Panel Count (36" coverage panels):**
```
Panels per side = ceil(Building Length ÷ 3)
Panel length = Rafter length = sqrt((Run/2)² + Rise²) + Overhang
  where Run = Building Width, Rise = (Pitch/12) × (Width/2)
  Overhang: typically 12" (1') unless specified

Total roof panels = Panels per side × 2 (gable) or adjusted for hip

Wall panels (if needed):
  Front + back = 2 × ceil(Building Width ÷ 3) × Eave Height panels
  Sides = 2 × ceil(Building Length ÷ 3) × Eave Height panels
  (subtract for doors/windows)
```

**Quick Trim Estimate (standard building):**

| Trim | Where | How to Calculate | Pieces (10' lengths) |
|------|-------|------------------|----------------------|
| Ridge Cap (RC10 or RC14) | Roof peak | Building length | ceil(Length ÷ 10) |
| Eave Trim (EVE/EAV) | Bottom of roof | 2 × Building length | ceil(2 × Length ÷ 10) |
| Rake Trim (RK) | Gable edges | 4 × Rafter length | ceil(4 × Rafter ÷ 10) |
| Drip Edge (DE) | Roof edges | Perimeter of roof | ceil(Perimeter ÷ 10) |
| Peak Cap (PC/PCF) | Ridge ends | 2 pieces | 2 |
| Corner Trim (OC/IC) | Wall corners | 4 × Eave height | ceil(4 × Height ÷ 10) |
| J-Channel (JCH) | Doors/windows | Perimeter of openings | ceil(Perimeter ÷ 10) |

**Fasteners (Quick):**
```
Roof: 80 screws per 100 sq ft (exposed fastener) or 1 clip per 12" (standing seam)
Wall: 60 screws per 100 sq ft
Trim: 1 screw per 12" per flange (typically 2 flanges = 2 screws/LF)

Buy boxes of 250. Always round UP to next full box.
```

**Accessories:**
```
Closure strips: 1 per panel at eave and ridge (foam or vented)
Butyl tape: 1 roll per 50 LF of standing seam
Pipe boots: Count roof penetrations (vent pipes, exhaust fans)
```

### Quick Estimate Output Format

```
QUICK ESTIMATE — [Building Type]
Dimensions: [W] × [L] × [H] eave, [Pitch] roof
Panel: [Profile], [Gauge], [Color]
────────────────────────────────
ROOF PANELS
  [count] panels × [length]' = [total LF]
  Coverage: [sq ft]

WALL PANELS (if applicable)
  [count] panels × [height]' = [total LF]

TRIM (10' lengths)
  Ridge Cap (RC10):     [count]
  Eave Trim (EVE):      [count]
  Rake Trim (RK):       [count]
  Drip Edge (DE):       [count]
  Corner Trim (OC):     [count]
  J-Channel (JCH):      [count]

FASTENERS
  Roof screws:          [count] ([boxes] boxes of 250)
  Wall screws:          [count] ([boxes] boxes of 250)
  Trim screws:          [count]

ACCESSORIES
  Foam closures:        [count] pairs
  Pipe boots:           [count]

WASTE: 5% panels, 10% trim included above
────────────────────────────────
Assumptions: [list all assumptions]
```

---

## Mode 2: Detailed Estimate (Engineering-Grade)

Use for: formal quotes, large projects, architectural spec compliance. Produces a complete BOM with SKU codes.

### Additional Input Required (Beyond Quick)
- Exact roof pitch (X:12)
- Overhang dimensions (eave and gable)
- Number and sizes of doors/windows
- Number of roof penetrations
- Wall type (full metal, wainscot, partial)
- Wainscot height (if applicable)
- Soffit and fascia requirements
- Valley locations (if complex roof)
- Hip locations (if hip roof)
- Color specification
- Gauge specification

### Detailed Calculation: Trim Takeoff

For detailed mode, calculate EXACT trim quantities using stretchout for material cost:

**Common Trim Families for Buildings:**

| Application | Family | Stretchout | Bends | Hems | Notes |
|-------------|--------|------------|-------|------|-------|
| Ridge Cap 10" | RC10 | 12" | 2 | 0 | Standard residential/ag |
| Ridge Cap 14" | RC14 | 16" | 2 | 0 | Wide ridge |
| Eave Trim | EVE/EAV | 8" | 2 | 1 | Bottom of roof |
| Rake Trim | RK | 8" | 2 | 1 | Gable edge |
| Drip Edge | DE | 4" | 1 | 1 | Roof edge |
| J-Channel | JCH | 4" | 2 | 0 | Window/door trim |
| Outside Corner | OC | 6" | 1 | 2 | Wall corner (outside) |
| Inside Corner | IC | 6" | 1 | 2 | Wall corner (inside) |
| Fascia 3.5" | FAS13 | 7" | 2 | 1 | Standard fascia |
| Fascia 5.5" | FAS15 | 9" | 2 | 1 | Wide fascia |
| Base Angle | BA | 5" | 1 | 0 | Wall base |
| Rat Guard | RG | 6" | 2 | 0 | Bottom wall seal |
| Valley | VV | 18" | 1 | 2 | Valley flashing |
| Headwall | HWFR | 8" | 2 | 1 | Wall-to-roof |
| Sidewall | SWF | 8" | 2 | 1 | Wall-to-wall |
| Z-Flashing | ZF | 5" | 2 | 0 | Horizontal joint |

### Detailed BOM Output Format

```
DETAILED MATERIAL ESTIMATE
Project: [Name/Description]
Building: [W] × [L] × [H], [Pitch] roof
Date: [Date]
──────────────────────────────────────

PANELS
  SKU             Description              Qty    Length   Total LF
  ─────           ─────────               ────   ──────   ────────
  [PID]           [Panel, Gauge, Color]    [n]    [L]'     [LF]
  [PID]           [Wall panel if needed]   [n]    [L]'     [LF]

TRIM (10' lengths unless noted)
  SKU             Description              Qty
  ─────           ─────────               ────
  [PID]           Ridge Cap 10"            [n]
  [PID]           Eave Trim                [n]
  [PID]           Rake Trim                [n]
  ... (all trim items)

FASTENERS & ACCESSORIES
  Item                                     Qty
  ─────                                   ────
  #10 × 1" Pancake Screws (roof)          [n] ([boxes] boxes)
  #10 × 1" Pancake Screws (wall)          [n] ([boxes] boxes)
  #10 × 3/4" Stitch Screws (trim)         [n]
  Foam Closure Strips (pairs)              [n]
  Vented Closure Strips                    [n]
  Butyl Tape (rolls, 50'/roll)             [n]
  Pipe Boots                               [n]

WASTE ALLOWANCE
  Panels: +5% = [n] extra panels
  Trim: +10% = [n] extra pieces
──────────────────────────────────────
ASSUMPTIONS
  - [List every assumption explicitly]

NOTE: Quantities only. Use GMS Pricing Engine for dollar amounts.
```

---

## Building Type Templates

### Pole Barn / Machine Shed (Most Common)

**Typical spec:** 40' × 60' × 14' eave, 4:12 pitch, Classic Rib 29ga
- Gable roof with 12" overhangs
- No windows, 1 overhead door (12' × 14'), 1 walk door (3' × 7')
- Full metal walls on all 4 sides
- No soffit or fascia (open eave)

**Standard trim package:**
- Ridge cap, eave trim, rake trim, drip edge
- Corner trim (4 outside corners)
- J-channel around doors
- Rat guard at base

### Residential Re-Roof

**Typical spec:** 30' × 50' footprint, 6:12 pitch
- Existing structure — panels only (no wall metal)
- Need underlayment consideration (not GMS product)
- Pipe boots for plumbing vents (typically 2-4)
- Valley flashing if complex roof
- May need ice & water shield (not GMS product — note separately)

**Standard trim package:**
- Ridge cap (RC10), drip edge, rake trim
- Valley flashing if applicable
- Pipe boots

### Commercial / Warehouse

**Typical spec:** 60' × 100' × 20' eave, 2:12 pitch
- Low-slope standing seam (SSQ550 or SSQ675)
- Full wall panels (Pro Panel or PBR)
- Multiple doors, dock doors
- Parapet or mansard edge details
- May require Kynar/PVDF finish for warranty

### Garage / Shop

**Typical spec:** 24' × 30' × 10' eave, 4:12 pitch
- Classic Rib or Pro Panel
- 1-2 overhead doors, 1 walk door
- Full or partial metal walls
- Simple trim package

---

## Panel Selection Guide

| Building Type | Budget | Recommended | Gauge | Why |
|---------------|--------|-------------|-------|-----|
| Ag/Pole Barn | Economy | Classic Rib | 29ga | Lowest cost, proven performance |
| Ag/Pole Barn | Mid | Classic Rib | 26ga | Better hail resistance |
| Residential Roof | Standard | Pro Panel | 26ga | Better aesthetics than Classic Rib |
| Residential Roof | Premium | SSQ550 | 26ga | Hidden fastener, clean lines |
| Residential Walls | Accent | Board & Batten | 26ga | Modern vertical look |
| Commercial Roof | Standard | PBR | 26ga | Commercial-grade strength |
| Commercial Low-Slope | Required | SSQ675 | 26ga | Mechanical seam, 0.5:12 min |
| Industrial | Heavy | Trapezoid TRQ250 | 24ga | Maximum span capability |

---

## Fastener Guide

| Application | Fastener Type | Spacing | Per Sq Ft |
|-------------|---------------|---------|-----------|
| Exposed fastener roof | #10 × 1" pancake head | Every rib, 24" OC rows | 0.80 |
| Exposed fastener wall | #10 × 1" pancake head | Every rib, 24" OC rows | 0.60 |
| Standing seam clips | Hidden clip | 24" OC along panel | varies |
| Trim to panel | #10 × 3/4" stitch screw | 12" OC per flange | 2.0/LF |
| Metal-to-wood | #12 × 1.5" with washer | Varies by application | varies |
| Closure to purlin | Pop rivet or screw | 12" OC | varies |

**Screw packaging:** Boxes of 250. Always round up to full boxes.

---

## Common Mistakes to Avoid

1. **Forgetting waste.** 5% panels, 10% trim is the MINIMUM. Complex roofs may need 15% panel waste for cuts.
2. **Wrong coverage width.** Standing seam is 12" or 16" or 24", NOT 36". Big difference in panel count.
3. **Forgetting closures.** Every panel needs foam or vented closure at eave and ridge. Easy to miss, expensive to not have on site.
4. **Ignoring pitch.** A 12:12 pitch roof has 41% more area than the footprint. Huge impact on material quantity.
5. **Not accounting for doors/windows.** Subtract panel area, but ADD J-channel and flashing trim around every opening.
6. **Mixing gauges.** Don't mix 29ga and 26ga on the same building unless the customer specifically requests it (e.g., 26ga roof, 29ga walls).
7. **Forgetting pipe boots.** Every roof penetration needs one. Typical residential: 2-4. Typical commercial: 4-8.
8. **Not specifying color.** Every item in the BOM needs a color. Trim should match panels unless accent is specified.

---

## Cross-References

- **GMS Pricing Engine** — Use for dollar amounts after quantities are estimated
- **GMS SKU Decoder** — For encoding product IDs in the BOM
- **GMS Sales Outreach** — For turning estimates into quote emails

### Panel SKU Encoding Reference

Panel PIDs don't include length (panels are cut to order):
- Classic Rib 29ga Arctic White: `A9ARW`
- PBR 26ga Charcoal: `PBR6CH`
- Pro Panel 26ga Ash Gray: `PRO6AG`
- SSQ550 26ga Kynar Slate Gray: `SSQ5506CMGSG`

Trim PIDs include length code:
- Ridge Cap 10" 29ga Arctic White 10': `RC109ARW10`
- Eave Trim 26ga Charcoal 10': `EVE6CH10`
- Drip Edge 29ga Black 10': `DE9BK10`
