# GMS Coil Reference Pricing

## Important Note
These are reference prices as of 2026-03-28. Coil costs fluctuate with steel markets. Always use current costs when available — these serve as reasonable defaults for margin calculations and quoting.

**Source:** `coil_pricing_data.py` (Python service) and `coils.json` (calculator application)

---

## 29 Gauge Coils (USS/SMP)

### Grade 80 Coils
| Width | Thickness | Grade | Base Cost/LF | ULG | Textured | Gallery Blue | Dark Red | Copper | Notes |
|-------|-----------|-------|--------------|-----|----------|--------------|----------|--------|-------|
| 40.875" | 0.0153" | 80 | $2.17 | +$0.06 | +$0.18 | +$0.10 | +$0.10 | +$0.20 | Primary panel coil (41" actual) |

### Grade 80 Alternative (Acrylic Galvalume)
| Width | Thickness | Grade | Base Cost/LF | Acrylic | Notes |
|-------|-----------|-------|--------------|---------|-------|
| 40.875" | 0.0150" | 80 | $1.65 | $0.00 | Acrylic finish base |

---

## 26 Gauge Coils (USS/SMP)

### Grade 50 Coils (20" width)
| Width | Thickness | Grade | Base Cost/LF | ULG | Gallery Blue | Textured | Copper | Notes |
|-------|-----------|-------|--------------|-----|--------------|----------|--------|-------|
| 20.0" | 0.0185" | 50 | $1.37 | +$0.04 | +$0.07 | +$0.12 | +$0.14 | Pattern A trim coil |

### Grade 50 Coils (41.5625" width)
| Width | Thickness | Grade | Base Cost/LF | ULG | Gallery Blue | Textured | Copper | Notes |
|-------|-----------|-------|--------------|-----|--------------|----------|--------|-------|
| 41.5625" | 0.0185" | 50 | $2.59 | +$0.08 | +$0.13 | +$0.23 | +$0.26 | Standard panel coil |

### Grade 80 Coils (43" width)
| Width | Thickness | Grade | Base Cost/LF | Gallery Blue | Textured | Copper | Notes |
|-------|-----------|-------|--------------|--------------|----------|--------|-------|
| 43.0" | 0.0185" | 80 | $2.65 | +$0.13 | +$0.23 | +$0.26 | Alternate 26ga width |

---

## 24 Gauge Coils (CMG/Kynar — PVDF Premium)

### Grade 50 AZ50 PVDF (43" width)
| Width | Thickness | Grade | Base Cost/LF | Regal | Notes |
|-------|-----------|-------|--------------|-------|-------|
| 43.0" | 0.0230" | AZ50 | $4.37 | +$0.50 | CMG supplier — 24ga panels |

### Grade 50 AZ50 PVDF (48.375" width)
| Width | Thickness | Grade | Base Cost/LF | Regal | Notes |
|-------|-----------|-------|--------------|-------|-------|
| 48.375" | 0.0230" | AZ50 | $5.08 | +$0.57 | CMG supplier — largest 24ga panels |

### Grade 50 AZ50 PVDF (20" width)
| Width | Thickness | Grade | Base Cost/LF | Regal | Liner | Camo | Woodgrain | Notes |
|-------|-----------|-------|--------------|-------|-------|------|-----------|-------|
| 20.0" | 0.0230" | AZ50 | $2.19 | +$0.24 | -$0.24 | +$1.96 | +$2.36 | 24ga trim width; Liner is discount finish |

---

## Coil Width Mapping to Product Families

### Pattern A: 20" Coil Width
Used for **131 trim families** including:
- Flashings (FAS family)
- Trim pieces (trim width ~12-18")
- Special cuts

**Products sourced from:**
- 26GA-20-G50 (USS/SMP standard)
- PVDF-20-AZ50 (premium Kynar finishes)

### Pattern B: 40-43" Coil Width
Used for **8 core panel families** and most trims:

**26 Gauge panels (standard):**
- 26GA-41.5625-G50 (41.5625" width)
- 26GA-43-G80 (43" width)

**29 Gauge panels (exposed fastener):**
- 29GA-40.875-G80 (40.875" width)

**24 Gauge panels (premium Kynar):**
- PVDF-43-AZ50 (43" width)
- PVDF-48.375-AZ50 (48.375" wide — largest)

---

## 8 Real Panel Types (GMS Core Product Line)

All panels are sourced from the coil widths above:

| Panel | Gauge | Typical Coil | Width | Margin Target |
|-------|-------|--------------|-------|----------------|
| Classic Rib | 29, 26, 24 | 40.875" / 41.5625" | 36" | 35% (EF) / 40% (HF) |
| PBR (Pro Rib) | 29, 26, 24 | 40.875" / 41.5625" | 36" | 35% (EF) / 40% (HF) |
| Pro Panel | 29, 26, 24 | 40.875" / 41.5625" | 36" | 35% (EF) / 40% (HF) |
| FF100 | 29, 26, 24 | 40.875" / 41.5625" | 36" | 35% (EF) / 40% (HF) |
| SSQ550 (Standing Seam) | 26, 24 | 41.5625" / 43" | 24" | 40% (HF) |
| SSQ675 (Standing Seam) | 26, 24 | 41.5625" / 43" | 24" | 40% (HF) |
| Trapezoid | 26, 24 | 41.5625" / 43" | 30" | 40% (HF) |
| B&B (Box & Beam) | 26, 24 | 41.5625" / 43" | 24" | 40% (HF) |

**Legend:** EF = Exposed Fastener, HF = Hidden Fastener

---

## Pricing Methodology

### Base Cost Calculation
```
Adjusted Coil Cost/LF = Base Cost/LF + Finish Premium
```

Example:
- 26GA-20-G50 (base): $1.37/LF
- With ULG finish: $1.37 + $0.04 = $1.41/LF

### Trim/Panel Cost Calculation (Method A)
```
Material Cost = (Stretchout / Coil Width) × Adjusted Coil Cost × Length
Total Cost = Material Cost + Labor
```

### Coil Efficiency
- **20" coil:** Used for trim cuts (higher material waste)
- **40.875-48.375" coils:** Used for panels (optimized width = minimal waste)

---

## Key Coil Properties

### Gauge Thickness
- **29 GA:** 0.0153" (lightest)
- **26 GA:** 0.0185" (standard)
- **24 GA:** 0.0230" (heaviest — premium)

### Material Suppliers
- **USS:** United Steel Supply — SMP (Standard Metallic Paint) 29/26ga
- **CMG:** Coil Mills Group — Kynar 24/26ga PVDF

### Finish Categories
**Basic:** Galvalume, Acrylic (free)
**Standard Metallic:** ULG, Textured, Gallery Blue, Dark Red, Copper (+$0.06-$0.26)
**Premium PVDF:** Regal, Metallic, Camo, Woodgrain (+$0.24-$2.36)

---

## Common Questions

**Q: How does coil cost affect trim pricing?**
A: Trim cost is highly sensitive to coil cost (material is 60-70% of cost). A $0.10 increase per LF on the coil increases trim cost by ~$0.07-$0.10 depending on stretchout.

**Q: Why is 20" coil more expensive per LF than 40" coil?**
A: It isn't. The base cost is per LF. The 20" coil serves trim (which has higher stretchout), while 40"+ coils serve panels (optimized width).

**Q: When should I use 24GA over 26GA?**
A: Only for premium finishes (Kynar PVDF) or when customer specifies. 24GA adds ~$2-3/LF cost for minimal structural benefit on residential roofing.

**Q: Do finish premiums apply to all widths?**
A: Premiums are per-coil specific. Check the table for each coil ID. Some finishes may not be available on certain widths.
