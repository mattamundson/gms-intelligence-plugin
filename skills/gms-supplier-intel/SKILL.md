---
name: gms-supplier-intel
description: "Supplier and purchasing intelligence for Greenfield Metal Sales coil procurement. Use this skill when the user asks about suppliers (USS, CMG), coil purchasing, reorder points, purchase orders, lead times, coil specifications, supplier routing, safety stock, or 'when should we reorder', 'who supplies this gauge', 'what's the lead time', 'PO workflow', or 'coil cost comparison'."
---

# GMS Supplier & Purchasing Intelligence

> Greenfield Metal Sales coil procurement — from reorder trigger to receiving dock.

You are the purchasing brain for GMS. You know every coil supplier, every specification, every lead time, every cost variable, and the complete PO workflow. When Inventory Health says "reorder," you know from whom, at what cost, and when it arrives.

## The Two Suppliers

GMS sources ALL coil from exactly two suppliers. There are no others.

### USS (United Steel Supply) — SMP Paint System

| Attribute | Value |
|-----------|-------|
| **Vendor ID** | MIDWES001 |
| **Paint System** | SMP (Sherwin-Williams Weather XL) |
| **Warranty** | Lifetime Paint & Fade |
| **Gauges** | 29ga, 26ga |
| **Lead Time** | 2-3 weeks |
| **Color Count** | ~70 (47 standard + 16 crinkle + 7 matte) |
| **Priority** | High |
| **Auto-Process Invoices** | Yes |

USS is the workhorse supplier. Their SMP-coated steel covers the vast majority of GMS orders — residential roofing, agricultural buildings, and most commercial projects. Shorter lead time means faster turnaround and lower safety stock requirements.

### CMG (Coated Metals Group) — Kynar PVDF System

| Attribute | Value |
|-----------|-------|
| **Vendor ID** | CMG001 |
| **Paint System** | Kynar 500 PVDF |
| **Warranty** | 40-Year Paint & Fade |
| **Gauges** | 24ga, 26ga |
| **Lead Time** | 4-6 weeks |
| **Color Count** | ~42 |
| **Priority** | High |
| **Auto-Process Invoices** | Yes |

CMG is the premium supplier. Kynar PVDF coating is significantly more durable and expensive. Used for commercial, architectural, and standing seam applications where the 40-year warranty matters.

## Coil Specifications

### 29 Gauge (USS Only)

| Spec | Value |
|------|-------|
| Grade | 80 (high-strength) |
| Width | 40.875" (called "41") |
| Thickness | 0.0153" |
| Base Cost/LF | $2.17 |
| Substrate | Galvalume AZ50 |
| Supplier | USS exclusively |

29ga is the thinnest, cheapest, and most common gauge. Used for exposed fastener panels (Classic Rib, PBR, Pro Panel, FF100) and standard trim. Cannot be sourced from CMG.

### 26 Gauge

**USS Version (SMP):**

| Spec | Value |
|------|-------|
| Grade | 50 (standard) / 80 (heavy) |
| Widths | 20.0" (trim), 41.5625" (panels), 43.0" (Grade 80) |
| Thickness | 0.0185" |
| Base Cost/LF (20") | $1.37 |
| Base Cost/LF (41.5") | $2.59 |
| Base Cost/LF (43") | $2.65 |
| Substrate | Galvalume AZ50 |

**CMG Version (Kynar):**

| Spec | Value |
|------|-------|
| Grade | AZ50 (PVDF) |
| Widths | 43.0" (panels/trim), 48.375" (large panels) |
| Thickness | 0.0230" |
| Base Cost/LF (43") | $4.37 |
| Base Cost/LF (48.375") | $5.08 |
| Substrate | Galvalume AZ50 |

26ga is the crossover gauge — available from BOTH suppliers. USS 26ga SMP costs $2.59-2.65/LF vs CMG 26ga Kynar at $4.37/LF. The CMG version costs **65-69% more** for the same gauge because of the Kynar coating.

### 24 Gauge (CMG Only)

| Spec | Value |
|------|-------|
| Grade | AZ50 (PVDF premium) |
| Widths | 20.0" (trim), 43.0" (panels), 48.375" (large panels) |
| Thickness | 0.0230" |
| Base Cost/LF (20") | $2.19 |
| Base Cost/LF (43") | $4.37 |
| Base Cost/LF (48.375") | $5.08 |
| Substrate | Galvalume AZ50 |
| Liner discount | -$0.24/LF on 20" width |

24ga is the thickest and most expensive. Used for standing seam (SSQ550, SSQ675), architectural applications, and premium commercial projects. Cannot be sourced from USS.

## Gauge Routing Rules

This is the critical decision tree for which supplier to use:

```
Need 29ga? → USS (only option)
Need 24ga? → CMG (only option)
Need 26ga SMP? → USS
Need 26ga Kynar? → CMG
Need any Kynar/PVDF? → CMG (only option)
Need any crinkle/matte? → USS (only option)
```

**The 26ga decision**: When a customer orders 26ga, you MUST determine the paint system. If they want Kynar (40-year warranty, premium colors), route to CMG. If they want SMP (standard colors, lower cost), route to USS. This is the only gauge where supplier routing requires a paint system decision.

## Gauge Pricing Multipliers

| Gauge | Multiplier | Relative to 29ga |
|-------|-----------|-------------------|
| 29ga | 1.00× | Base |
| 26ga | 1.20× | +20% |
| 24ga | 1.44× | +44% |

These multipliers apply to finished product pricing, not just coil cost. A 24ga trim piece costs 44% more than the same profile in 29ga.

## Finish Premiums

### USS SMP Finish Surcharges (per LF, added to base cost)

| Finish | 29ga (40.875") | 26ga (41.5") | 26ga (43") |
|--------|---------------|--------------|------------|
| Standard SMP | +$0.00 | +$0.00 | +$0.00 |
| Galvalume (bare) | +$0.00 | +$0.00 | +$0.00 |
| ULG (Ultra Low Gloss) | +$0.04 | +$0.05 | +$0.06 |
| Gallery Blue | +$0.07 | +$0.10 | +$0.13 |
| Dark Red | +$0.07 | +$0.08 | +$0.10 |
| Textured/Crinkle | +$0.12 | +$0.18 | +$0.23 |
| Copper | +$0.14 | +$0.20 | +$0.26 |

### CMG Kynar Finish Surcharges (per LF, added to base cost)

| Finish | 24/26ga (20") | 24/26ga (43") | 24/26ga (48.375") |
|--------|--------------|--------------|-------------------|
| Smooth Kynar | +$0.00 | +$0.00 | +$0.00 |
| Regal | +$0.24 | +$0.46 | +$0.57 |
| Metallic | +$0.24 | +$0.46 | +$0.57 |
| Liner (20" only) | -$0.24 | N/A | N/A |
| Camo | — | +$1.96 | +$1.96 |
| Woodgrain | — | +$2.36 | +$2.36 |

**Premium finish markup**: MCC (Matt Color Coat), CR (Crinkle), and ULG (Ultra Low Gloss) finishes carry a **+15% retail markup** on top of the coil cost premium.

## Lead Time Management

### Safety Stock Calculation by Supplier

```
Reorder Point = Weighted Velocity × (Lead Time Days + Safety Stock Days)

USS:  Velocity × (14-21 days lead + 7 days safety) = Velocity × 21-28 days
CMG:  Velocity × (28-42 days lead + 7 days safety) = Velocity × 35-49 days
```

**Critical insight**: CMG coils need roughly **2× the safety stock** of USS coils due to the 2× longer lead time. This means more capital tied up in CMG inventory. Plan accordingly.

### Availability Statuses

| Status | Meaning | Lead Time Impact |
|--------|---------|-----------------|
| `stock` | Available for immediate shipment | Standard (2-3wk USS / 4-6wk CMG) |
| `slitting` | Coil must be slit to width | +1-2 days processing |
| `pto` | Purchase-to-order (mill run required) | Extends to 6-8 weeks for ANY supplier |

**Watch for PTO**: Even USS colors that are normally 2-3 weeks can jump to 6-8 weeks if the specific color/gauge combo is on PTO status. Always check availability before quoting lead times.

## Purchase Order Workflow

### Step 1: Reorder Trigger
- Inventory Health detects stock below reorder point
- Urgency assigned: CRITICAL / HIGH / MEDIUM / LOW

### Step 2: Recommendation Generation
```python
PurchaseRecommendation:
  product_id: str           # e.g., "CO4129ARW"
  supplier: str             # "USS" or "CMG"
  urgency: str              # CRITICAL/HIGH/MEDIUM/LOW
  current_stock: float
  reorder_point: float
  recommended_qty: float    # max(reorder_point × 2, monthly_usage × 2) - current_stock
  estimated_cost: float
  lead_time_days: int       # 14-21 (USS) or 28-42 (CMG)
```

### Step 3: PO Draft Creation
- Products grouped by supplier (all USS items on one PO, all CMG items on another)
- Auto-approve threshold: Configurable (default requires Matt's approval)
- PO sent to approver via Teams notification

### Step 4: Vendor Communication
- Approved POs emailed to supplier automatically
- Vendor confirmation tracked
- Three-way match on receipt: PO ↔ Invoice ↔ Receipt

### Step 5: Receiving
- Physical count verified against PO
- Price variance flagged if > 2.0% tolerance
- Inventory updated in Paradigm

### Urgency Levels

| Level | Condition | Action |
|-------|----------|--------|
| CRITICAL | Stock = 0 or < reorder point × 0.10 | Immediate PO, consider rush |
| HIGH | Stock < reorder point × 0.50 | Same-day PO |
| MEDIUM | Stock approaching reorder point | Standard PO within 48 hours |
| LOW | Stock at reorder point, excess | Monitor, no immediate action |

## Order Quantity Formula

```
Order Qty = max(Reorder Point × 2, Monthly Usage × 2) - Current Stock
Minimum: 1 unit (never order negative)
```

The 2× multiplier ensures you're ordering enough to cover the next reorder cycle, not just filling back to the reorder point.

## Coil ID Structure

Every coil follows this naming pattern:

```
CO{width}{gauge}{color}

CO4129ARW
├── CO    = Coil prefix
├── 41    = Width in inches (41" for 29ga/24ga, 43" for 26ga)
├── 29    = Gauge
└── ARW   = Arctic White (color code)
```

### Width-to-Gauge Mapping

| Width | Gauge | Supplier |
|-------|-------|---------|
| 41" (40.875") | 29ga | USS |
| 41" | 24ga | CMG |
| 43" | 26ga | USS or CMG |
| 48.375" | 24/26ga | CMG (large panels) |
| 20" | 26ga/24ga | USS (26) or CMG (24) trim coils |

## Supplier Performance Tracking

### Price Variance Monitoring
- Tolerance: 2.0% between PO price and invoice price
- Alerts generated for any variance exceeding threshold
- Three-way match required: PO ↔ Invoice ↔ Receipt

### Invoice Auto-Processing
- Both USS and CMG have auto-process enabled
- Trigger keywords: "invoice", "inv", "bill", "statement", "po#", "purchase order"
- Attachment type: PDF only
- Unknown vendors are flagged for manual review

## Days on Hand (DOH) Benchmarks for Coils

| Category | Target DOH | Excess Threshold |
|----------|-----------|-----------------|
| USS Coils (29ga, 26ga) | 14-21 days | > 45 days |
| CMG Coils (24ga, 26ga Kynar) | 21-35 days | > 60 days |

CMG coils justify higher DOH targets because of the longer replenishment lead time.

## Cost Comparison: USS vs CMG for Same Application

Example: 12' panel, 26 gauge

| Factor | USS (SMP) | CMG (Kynar) | Delta |
|--------|----------|------------|-------|
| Coil cost/LF (43") | $2.65 | $4.37 | +65% |
| Paint warranty | Lifetime | 40-Year | — |
| Lead time | 2-3 weeks | 4-6 weeks | +2-3 weeks |
| Safety stock days | 21-28 | 35-49 | +67-75% |
| Color options | ~70 | ~42 | -40% |
| Typical use | Residential, Ag | Commercial, Architectural | — |

**The pitch to customers**: USS SMP is the value choice — lower cost, faster delivery, more colors, with a lifetime warranty. CMG Kynar is the premium choice — superior fade resistance (PVDF coating), 40-year warranty, and the finish demanded by architects and commercial specs.

## Cross-References

- **Inventory Health Analyzer**: Triggers reorder recommendations. Lead time differentials (USS 14-21d vs CMG 28-42d) directly affect reorder point calculations and safety stock.
- **GMS Pricing Engine**: Coil costs from this skill are the raw material input to the pricing formula: `Material = (Stretchout / Coil Width) × Coil Price × Length + Labor`. Finish premiums layer on top.
- **SKU Decoder**: Product IDs encode gauge and color, which determine the supplier routing (gauge digit 4/9 → check paint system, 6 → check paint system for 26ga routing).
- **Production & Assembly Navigator**: Coils feed the CO→SLIT→BEND→HEM manufacturing flow. Assembly traceability maps every finished product back to a specific coil ID.
- **Material Estimator**: Project estimates generate coil demand that feeds purchasing recommendations.

## Common Mistakes

1. **Routing 29ga to CMG** — CMG does NOT make 29ga. Only USS.
2. **Routing 24ga to USS** — USS does NOT make 24ga. Only CMG.
3. **Assuming same lead time** — USS is 2-3 weeks, CMG is 4-6 weeks. Never quote CMG lead times at USS speed.
4. **Forgetting PTO status** — Even USS can go to 6-8 weeks on PTO colors. Always check.
5. **Using 41" width for 26ga** — 26ga coils are 43" (or 48.375"), NOT 41". Only 29ga and 24ga use 41".
6. **Ignoring finish premiums** — Crinkle, Woodgrain, and Camo finishes can add $0.23-$2.36/LF. This materially affects the quoted price.
7. **Same safety stock for both suppliers** — CMG needs ~2× the safety stock of USS. Under-stocking CMG coils causes production delays.
8. **Confusing warranty terms** — USS = "Lifetime Paint & Fade." CMG = "40-Year Paint & Fade." These are different programs with different claim processes.
