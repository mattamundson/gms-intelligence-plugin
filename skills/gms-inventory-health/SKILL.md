---
name: gms-inventory-health
description: Analyze inventory health for Greenfield Metal Sales — stock levels, velocity, dead stock, reorder recommendations, and turnover metrics. Use this skill whenever someone asks about inventory status, stock health, slow movers, dead stock, reorder needs, turnover ratios, days on hand, excess inventory, stockout risk, safety stock, or any inventory analysis question. Also triggers on "what should I reorder," "what's overstocked," "inventory report," "stock check," "what's not selling," "inventory problems," or any request to assess, audit, or diagnose inventory health. Cross-references the GMS Pricing Engine for cost/margin context and the SKU Decoder for product identification.
---

# GMS Inventory Health Analyzer

> Diagnose inventory health in seconds. From a single SKU check to a full portfolio audit — classify stock, calculate velocity, flag dead weight, and generate actionable reorder recommendations.

---

## Critical Rules

1. **Paradigm is the source of truth.** All inventory data comes from Paradigm ERP via `paradigm_complete.py` or its cached variant. Never guess quantities — query the system.
2. **API is currently DOWN.** Paradigm API has been returning 404 since 2026-03-14, token expired 2026-01-25. If live data is unavailable, state this clearly and work from the most recent cached/exported data.
3. **Never auto-adjust inventory.** DO NOT use `/api/user/Inventory/Adjust` (returns 405). Physical Count Worksheets via Paradigm UI are the only safe bulk adjustment method. Individual adjustments use the 2-step IADJ process — always preview before executing.
4. **InventoryAgent has no `run()` method.** Call `await agent.check_inventory_health()` for on-demand health checks. The agent runs an autonomous monitoring loop at 1-hour intervals.
5. **Single warehouse: MAIN.** GMS operates one warehouse. All inventory queries default to warehouse "MAIN".
6. **71,889 total products.** 25,283 active (35%), 46,606 discontinued (65%). Filter by `ysnDiscontinued = False` for active analysis.
7. **Product ID format matters.** Coils start with CO (e.g., CO4129ARW), panels are profile-prefixed (A9ARW for Classic Rib), trim includes family+gauge+color+length (RC109ARW10). Use the SKU Decoder skill for encoding/decoding.

---

## Health Score Framework

Every product or portfolio gets a **Health Score (0–100)** based on 5 weighted factors:

| Factor | Weight | What It Measures |
|--------|--------|-----------------|
| Stock Level | 30% | Current qty vs. reorder point — are we stocked right? |
| Velocity | 25% | Sales rate trend — is demand steady, growing, or dying? |
| Value at Risk | 20% | Dollar exposure from overstock or dead inventory |
| Days on Hand | 15% | How long current stock will last at current sell rate |
| Demand Consistency | 10% | Coefficient of variation — steady vs. lumpy demand |

### Score → Status Mapping

| Score | Status | Action |
|-------|--------|--------|
| 80–100 | EXCELLENT | No action needed |
| 60–79 | GOOD | Monitor normally |
| 40–59 | FAIR | Review recommended |
| 20–39 | POOR | Action required — reorder or markdown |
| 0–19 | CRITICAL | Immediate action — stockout imminent or dead capital |

### Stock Level Scoring (within 30% weight)

| Condition | Sub-Score | Definition |
|-----------|-----------|------------|
| OUT_OF_STOCK | 0 | decUnitsInStock = 0, has recent sales history |
| CRITICAL_LOW | 40 | Below 50 units OR < 10% of reorder point |
| LOW | 70 | Below 100 units OR < 50% of reorder point |
| HEALTHY | 100 | At or above reorder point |

---

## Velocity Analysis

Velocity is the heartbeat of inventory. Calculate using the `build_velocity_map(days=90)` pattern from the codebase.

### Velocity Calculation

```
Daily velocity = Total units sold in period ÷ Number of days
Monthly velocity = Daily velocity × 30

Weighted velocity (more recent = more weight):
  weighted = (v30 × 0.5) + (v60 × 0.3) + (v90 × 0.2)
  where v30 = velocity over last 30 days
        v60 = velocity over last 60 days
        v90 = velocity over last 90 days
```

### Velocity Classification

| Class | Daily Velocity | Action |
|-------|---------------|--------|
| Fast Mover | > 5 units/day | Keep deep stock, watch for stockouts |
| Normal | 1–5 units/day | Standard reorder cycle |
| Slow Mover | 0.1–1 unit/day | Reduce stock, consider min-buy only |
| Dead Stock | 0 units in 180 days | Markdown, liquidate, or discontinue |

---

## Reorder Point Calculation

The reorder system ensures GMS never runs out of high-velocity items while not over-investing in slow movers.

### Formula

```
Reorder Point = Weighted Velocity × (Lead Time Days + Safety Stock Days)

Defaults:
  Lead Time = 14 days (standard supplier delivery)
  Safety Stock = 7 days (buffer for demand spikes)
  Reorder Point = Velocity × 21 days

Recommended Order Quantity:
  order_qty = max(reorder_point × 2, monthly_usage × 2) - current_stock
  Minimum order: 1 unit (never negative)
```

### Alert Thresholds

| Condition | Severity | Trigger |
|-----------|----------|---------|
| Stock = 0 + has sales history | CRITICAL | Immediate reorder — losing sales |
| Stock < Reorder Point × 0.10 | HIGH | Will stock out within days |
| Stock < Reorder Point × 0.50 | MEDIUM | Approaching reorder point |
| Stock ≤ Reorder Point | LOW | At reorder — monitor closely |
| Stock > Reorder Point × 3 | EXCESS | Overstocked — reduce future orders |
| No sales in 180 days + stock > 0 | DEAD STOCK | Capital tied up — action needed |

---

## Days on Hand (DOH)

```
Days on Hand = Current Stock ÷ Daily Velocity

If velocity = 0 and stock > 0: DOH = ∞ (dead stock)
If velocity = 0 and stock = 0: DOH = N/A (discontinued or not stocked)
```

### DOH Benchmarks for GMS

| Product Type | Target DOH | Acceptable | Excess |
|-------------|-----------|------------|--------|
| Fast-moving panels (Classic Rib, PBR) | 14–30 days | 30–60 days | > 60 days |
| Standard panels (Pro Panel, SSQ550) | 21–45 days | 45–90 days | > 90 days |
| Specialty (Kynar colors, TRQ250) | 30–60 days | 60–120 days | > 120 days |
| Raw coil (CO prefixed) | 14–21 days | 21–45 days | > 45 days |
| Trim stock | 21–30 days | 30–60 days | > 60 days |
| Fasteners & accessories | 30–60 days | 60–90 days | > 90 days |

---

## Turnover Ratio

```
Inventory Turnover = COGS (or Total Sales Value) ÷ Average Inventory Value

Average Inventory Value = (Beginning Period Value + End Period Value) ÷ 2

Higher = better (moving product faster)
```

### Turnover Benchmarks

| Turnover | Rating | Meaning |
|----------|--------|---------|
| > 12× per year | Excellent | Turning monthly — lean operation |
| 6–12× | Good | Standard for metal distribution |
| 3–6× | Fair | Some dead weight dragging it down |
| 1–3× | Poor | Significant overstock or dead inventory |
| < 1× | Critical | More than a year of inventory sitting |

---

## ABC Analysis (Pareto Classification)

Classify inventory by revenue contribution:

```
A Items: Top 20% of SKUs → ~80% of revenue
  → Keep in stock always, tight reorder points, safety stock required

B Items: Next 30% of SKUs → ~15% of revenue
  → Standard reorder cycle, moderate safety stock

C Items: Bottom 50% of SKUs → ~5% of revenue
  → Order on demand, minimal or zero safety stock, candidates for discontinuation
```

### How to Calculate

1. Pull all products with sales in the last 12 months
2. Calculate total revenue per product (units sold × sales price)
3. Sort descending by revenue
4. Calculate cumulative percentage
5. Classify: A (cumulative ≤ 80%), B (80–95%), C (95–100%)

---

## Dead Stock Identification

Dead stock is capital sitting on shelves generating zero revenue. GMS definition:

```
Dead Stock = Product where:
  - decUnitsInStock > 0  AND
  - Zero units sold in last 180 days  AND
  - ysnDiscontinued = False (still active in system)

Value at Risk = Dead Stock Quantity × curCost
```

### Action Matrix for Dead Stock

| Value at Risk | Age (Days Since Last Sale) | Recommended Action |
|--------------|---------------------------|-------------------|
| > $5,000 | 180–365 days | Deep discount (30-50% off), push to sales team |
| > $5,000 | > 365 days | Liquidate, scrap, or donate |
| $500–$5,000 | 180–365 days | Bundle with fast movers, promotional pricing |
| $500–$5,000 | > 365 days | Mark for discontinuation, clearance pricing |
| < $500 | Any | Low priority — batch-clear quarterly |

---

## Excess Stock Identification

Excess isn't dead — it's alive but overstocked.

```
Excess Stock = Product where:
  - decUnitsInStock > Reorder Point × 3  AND
  - Velocity > 0 (still selling, just overstocked)

Excess Quantity = Current Stock - (Reorder Point × 2)
Excess Value = Excess Quantity × curCost
```

---

## Product Category Intelligence

GMS inventory falls into distinct categories with different health expectations:

### Raw Materials (Coils — CO prefix)

| Metric | Expectation |
|--------|------------|
| Typical inventory | 50–200 coils across USS + CMG |
| Key concern | Coil availability drives ALL downstream production |
| Lead time | USS SMP: 2–3 weeks. CMG Kynar: 4–6 weeks |
| Watch for | Color stockouts on popular colors (Arctic White, Charcoal, Black) |

### Finished Goods (Panels — profile prefix)

| Metric | Expectation |
|--------|------------|
| Typical inventory | Cut-to-order — minimal finished panel stock |
| Key concern | Coil must be available to cut |
| Top sellers | Classic Rib 29ga (Arctic White, Charcoal, Black, Galvalume) |
| Watch for | Orders queued with no coil to cut from |

### Trim (Family prefix — RC, EVE, RK, DE, OC, etc.)

| Metric | Expectation |
|--------|------------|
| Typical inventory | Some pre-bent standard items, mostly cut-to-order |
| Key concern | Stretchout waste — wider trim burns more coil per foot |
| Watch for | Obscure trim profiles sitting unsold |

### Accessories (Fasteners, closures, pipe boots)

| Metric | Expectation |
|--------|------------|
| Typical inventory | Bulk buy, slow to turn individually |
| Key concern | Minimum order quantities from suppliers |
| Watch for | Obsolete accessories for discontinued panel profiles |

---

## Analysis Output Formats

### Quick Health Summary

```
INVENTORY HEALTH SUMMARY — [Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Score: [XX]/100 ([STATUS])

Stock Distribution:
  Critical Low:  [n] products ([value])
  Low Stock:     [n] products ([value])
  Healthy:       [n] products ([value])
  Excess:        [n] products ([value])
  Dead Stock:    [n] products ([value])

Key Metrics:
  Total Inventory Value:    $[amount]
  Dead Stock Value at Risk: $[amount]
  Excess Stock Value:       $[amount]
  Average Days on Hand:     [n] days
  Portfolio Turnover:       [n]× per year

Top Actions:
  1. [Most urgent action]
  2. [Second priority]
  3. [Third priority]
```

### Reorder Report

```
REORDER RECOMMENDATIONS — [Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Priority: CRITICAL (Stock out or < 3 days supply)

  Product ID    Description              Stock  Velocity  DOH   Order Qty
  ──────────    ──────────               ─────  ────────  ───   ─────────
  [PID]         [Description]            [qty]  [/day]    [d]   [qty]

Priority: HIGH (< 7 days supply)
  ...

Priority: MEDIUM (< 14 days supply)
  ...

Total reorder value: $[amount]
```

### Dead Stock Report

```
DEAD STOCK REPORT — [Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Dead Items: [n] products
Total Value at Risk: $[amount]

  Product ID    Description              Stock  Cost     Value    Last Sale
  ──────────    ──────────               ─────  ──────   ──────   ─────────
  [PID]         [Description]            [qty]  $[cost]  $[val]   [date]

Recommended Actions:
  - Markdown candidates: [list]
  - Liquidation candidates: [list]
  - Discontinuation candidates: [list]
```

---

## Integration Points

### Data Sources

| Source | Method | Status |
|--------|--------|--------|
| Paradigm ERP (live) | `paradigm_complete.get_inventory()` | DOWN since 2026-03-14 |
| Paradigm (cached) | `paradigm_complete_cached.py` via Redis | Available if seeded |
| Shared Data Context | `shared_data_context.py` — in-memory snapshot | Available if loaded |
| Sales Data | `get_sales_details_all(limit=10000)` | Needed for velocity |
| ChromaDB | KDB vector search (22 endpoints) | Available for semantic queries |

### JARVIS Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/inventory/health` | GET | Quick health check |
| `/api/inventory/analysis` | GET | Full portfolio analysis |
| `/api/intelligence/inventory-brief` | GET | AI-generated inventory brief |
| `/api/inventory/create-adjustments` | POST | 2-step adjustment (IADJ) |
| `/orchestrator/agent/inventory` | POST | Trigger InventoryAgent tasks |

### Cross-Referenced Skills

- **GMS Pricing Engine** — Cost and margin data for value-at-risk calculations
- **GMS SKU Decoder** — Decode product IDs to understand what's actually sitting on shelves
- **GMS Material Estimator** — Connect outgoing estimates to stock availability

---

## Common Analysis Scenarios

### "What should I reorder?"

1. Run `check_inventory_health()` or query `/api/inventory/health`
2. Filter alerts by severity: CRITICAL → HIGH → MEDIUM
3. For each item: show current stock, velocity, DOH, recommended order qty
4. Prioritize by: (a) revenue impact, (b) days until stockout, (c) customer orders pending

### "What's not selling?"

1. Pull all products with `decUnitsInStock > 0`
2. Cross-reference with sales data (last 180 days)
3. Filter: zero sales = dead stock, < 1 unit/month = slow mover
4. Calculate value at risk for each
5. Sort by value descending — biggest capital traps first

### "Give me an inventory health report"

1. Calculate health score for every active product
2. Classify into stock distribution buckets
3. Calculate portfolio-level metrics (total value, turnover, avg DOH)
4. Identify top 5 actions (critical reorders + biggest dead stock items)
5. Output in Quick Health Summary format

### "How's our coil situation?"

1. Filter inventory to CO-prefix products only
2. For each coil: current stock, velocity, DOH
3. Flag any popular colors running low (Arctic White, Charcoal, Black, Galvalume)
4. Check Kynar coils separately (longer lead time = need more safety stock)
5. Note: coil availability drives ALL downstream panel production

---

## Common Mistakes to Avoid

1. **Counting discontinued products as dead stock.** Filter by `ysnDiscontinued = False` first. Discontinued items are expected to have zero sales.
2. **Ignoring cut-to-order dynamics.** GMS cuts panels to order from coil. Low "panel" inventory is normal — check the COIL that feeds them.
3. **Using raw unit counts without context.** 100 units of fasteners is nothing. 100 coils is a mountain. Always contextualize by product type.
4. **Assuming uniform lead times.** USS SMP coils: 2–3 weeks. CMG Kynar coils: 4–6 weeks. Kynar items need deeper safety stock.
5. **Forgetting assembly relationships.** A panel's availability depends on its parent coil + labor capacity. Check upstream, not just the SKU.
6. **Triggering inventory adjustments without confirmation.** Always preview changes. Never auto-execute. The IADJ 2-step process exists for safety.
7. **Querying all 71,889 products.** Filter to active only (25,283) unless specifically asked about discontinued items.
