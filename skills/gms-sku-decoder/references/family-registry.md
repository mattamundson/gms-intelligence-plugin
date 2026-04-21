# GMS Family Registry Reference

> **Purpose**: Complete authoritative reference for all 147 product families used by Greenfield Metal Sales in Paradigm ERP.
> **Scope**: 131 ACTIVE trim families + 8 panel families + coils + flatsheets + legacy/review families
> **Last Updated**: 2026-03-28
> **Source**: PARADIGM_MASTER_REFERENCE.md + trim-profiles.md

This file is the single source of truth for family prefix encoding, gauge availability, material patterns, and product classification. Use this when:
- Decoding product IDs (SKUs) to understand the family prefix
- Determining available gauges for a trim or panel
- Understanding material sourcing (20" vs 41" pattern)
- Identifying tricky families with embedded numbers in their prefix
- Looking up Paradigm-specific short aliases

---

## Complete Family Registry (147 Families)

### Active Trim Families (131)

| Family | Full Name/Description | Type | Gauges | Length Code? | Material Pattern | Stretchout (in) | Notes |
|--------|----------------------|------|--------|--------------|------------------|-----------------|-------|
| ANG11 | 1.5" x 1.5" Angle | Trim | 24,26,29 | Yes | A (20") | 4.0 | Embedded "11" = 1.5" dimensions |
| ANG22 | 2" x 2" Angle | Trim | 24,26,29 | Yes | A (20") | 5.0 | Embedded "22" = 2" dimensions |
| ANG33 | 3" x 3" Angle | Trim | 24,26,29 | Yes | A (20") | 7.0 | Embedded "33" = 3" dimensions |
| BBJT | Board & Batten J Trim | Trim | 24,26,29 | Yes | A (20") | 4.75 | B&B specialty profile |
| BBODT | Board & Batten O/H Door Trim | Trim | 24,26,29 | Yes | A (20") | 4.75 | B&B overhead door variant |
| BBBT | Board & Batten Base Trim | Trim | 24,26 | Yes | A (20") | 4.0 | B&B foundation trim |
| BBDF | Board & Batten Drip Flashing | Trim | 24,26 | Yes | A (20") | 4.25 | B&B water management |
| BBHT | Board & Batten Hem Trim | Trim | 24,26 | Yes | A (20") | 3.75 | B&B hemmed edge |
| BBIC | Board & Batten Inside Corner | Trim | 24,26,29 | Yes | A (20") | 17.0 | B&B complex corner |
| BBOC | Board & Batten Outside Corner | Trim | 24,26,29 | Yes | A (20") | 17.0 | B&B exterior corner |
| BBRG | Board & Batten Rat Guard | Trim | 24,26 | Yes | A (20") | 4.0 | B&B rodent barrier |
| BBSD7 | Board & Batten Sliding Door 7.25" | Trim | 24,26 | Yes | A (20") | 12.0 | B&B door opening trim |
| BB3 | 3.5" Band Board | Trim | 26,29 | Yes | A (20") | 10.0 | Flat fascia board trim |
| BB5 | 5.5" Band Board | Trim | 24,26,29 | Yes | A (20") | 12.0 | Larger flat fascia board |
| BST | 1" Bottom Starter | Trim | 24,26,29 | Yes | A (20") | 4.0 | Base/foundation starter |
| BT | Base Trim | Trim | 24,26,29 | Yes | A (20") | 6.5 | Standard foundation trim |
| CCF | Counter/Chimney Flashing | Trim | 24,26,29 | Yes | A (20") | 5.0 | Roof penetration flashing |
| CO5 | 5.5" Corner 10'3" | Trim | 24,26,29 | Yes | A (20") | 11.0 | Residential corner trim |
| CPBR | PBR Corner 10'3" | Trim | 24,26,29 | Yes | A (20") | 12.0 | Commercial rib corner variant |
| CPFRC | Commercial Panel Formed Ridge Cap | Trim | 26,29 | Yes | A (20") | N/A | Panel ridge integration |
| CRB | Commercial Rib Base | Trim | 26,29 | Yes | A (20") | 6.0 | Commercial profile foundation |
| CRD1011 | Com. Rib O/H Door 10" | Trim | None | No | A (20") | 16.0 | Embedded "1011" = complex encoding |
| CRD10112 | Com. Rib O/H Door 10" w/12" | Trim | 24,26,29 | Yes | A (20") | N/A | Double dimension variant |
| CRD10114 | Com. Rib O/H Door 10" w/14" | Trim | 24,26,29 | Yes | A (20") | N/A | Double dimension variant |
| CRD10116 | Com. Rib O/H Door 10" w/16" | Trim | 24,26,29 | Yes | A (20") | N/A | Double dimension variant |
| CRD810 | Com. Rib O/H Door 8" | Trim | None | No | A (20") | 14.0 | Embedded "810" = 8" door |
| CRD812 | Com. Rib O/H Door 8" w/12" | Trim | 24,26,29 | Yes | A (20") | N/A | Double dimension variant |
| CRD814 | Com. Rib O/H Door 8" w/14" | Trim | 24,26,29 | Yes | A (20") | N/A | Double dimension variant |
| CRD816 | Com. Rib O/H Door 8" w/16" | Trim | 24,26,29 | Yes | A (20") | N/A | Double dimension variant |
| CRD81 | Com. Rib O/H Door 8" | Trim | None | No | A (20") | 14.0 | Embedded "81" = 8" door (alt) |
| CRDD10110 | Com. Rib O/H Door w/Drip 10" w/10" | Trim | 24,26,29 | Yes | A (20") | N/A | Door + drip variant |
| CRDD10112 | Com. Rib O/H Door w/Drip 10" w/12" | Trim | 24,26,29 | Yes | A (20") | N/A | Door + drip variant |
| CRDD10114 | Com. Rib O/H Door w/Drip 10" w/14" | Trim | 24,26,29 | Yes | A (20") | N/A | Door + drip variant |
| CRDD10116 | Com. Rib O/H Door w/Drip 10" w/16" | Trim | 24,26,29 | Yes | A (20") | N/A | Door + drip variant |
| CRDD810 | Com. Rib O/H Door w/Drip 8" w/10" | Trim | 24,26,29 | Yes | A (20") | N/A | Door + drip variant |
| CRDD812 | Com. Rib O/H Door w/Drip 8" w/12" | Trim | 24,26,29 | Yes | A (20") | N/A | Door + drip variant |
| CRDD814 | Com. Rib O/H Door w/Drip 8" w/14" | Trim | 24,26,29 | Yes | A (20") | N/A | Door + drip variant |
| CRDD816 | Com. Rib O/H Door w/Drip 8" w/16" | Trim | 24,26,29 | Yes | A (20") | N/A | Door + drip variant |
| CRDD81 | Com. Rib O/H Door w/Drip 8" | Trim | None | No | A (20") | 12.0 | Door + drip |
| CRDF | Commercial Rib Drip Flashing | Trim | 24,26,29 | Yes | A (20") | 8.0 | Water management for CR |
| CRDJ1 | Commercial Rib Double J 0.5" | Trim | 24,26,29 | Yes | A (20") | 12.0 | Double J variant |
| CRDJ2 | Commercial Rib Double J 1.375" | Trim | 24,26,29 | Yes | A (20") | 10.0 | Double J variant |
| CRRC | Commercial Rib Rake & Corner | Trim | 24,26,29 | Yes | A (20") | 17.0 | Peak detail trim |
| CRJ | Commercial Rib J | Trim | 24,26,29 | Yes | A (20") | 8.0 | J-channel variant |
| CRSF | Commercial Rib Sidewall Flashing | Trim | 24,26,29 | Yes | A (20") | 14.0 | Sidewall penetration |
| CRZ | Commercial Rib Zee | Trim | 24,26,29 | Yes | A (20") | 6.0 | Z-profile variant |
| DC | Drip Cap (Standard) | Trim | 24,26,29 | Yes | A (20") | 3.25 | Simple water barrier |
| DE | Drip Edge | Trim | 24,26,29 | Yes | A (20") | 5.0 | Eave water management |
| DF | Drip Flashing | Trim | 26,29 | Yes | A (20") | 4.5 | Standard drip detail |
| DJT | Door Jamb Trim 10'3" | Trim | 24,26,29 | Yes | A (20") | 9.0 | Door side trim |
| DJT12 | Double J Trim 0.5" | Trim | 26,29 | Yes | A (20") | 9.0 | Double J half-inch |
| DJT78 | Double J Trim 0.875" | Trim | 24,26,29 | Yes | A (20") | 8.0 | Double J seven-eighths |
| DTC | Double Track Cover | Trim | 24,26,29 | Yes | A (20") | 13.0 | Two-track protection |
| ENDF | Endwall Flashing | Trim | 24,26,29 | Yes | A (20") | 8.0 | Gable end penetration |
| ET4 | 3" X 4" Eave Trim | Trim | 24,26,29 | Yes | A (20") | 7.0 | Eave transition trim |
| ET5 | 3" X 5.5" Eave Trim | Trim | 24,26,29 | Yes | A (20") | 9.0 | Larger eave trim |
| EV | Eave | Trim | 24,26,29 | Yes | A (20") | 5.75 | Standard eave soffit edge |
| EVET | Eave Trim | Trim | 26,29 | Yes | A (20") | 9.0 | Premium eave trim |
| EVET90 | Eave Trim 90 | Trim | 26,29 | Yes | A (20") | 8.0 | 90-degree eave variant |
| EW | Endwall | Trim | 24,26,29 | Yes | A (20") | 10.25 | Gable/end finish |
| FAS111 | 1.5" x 11.25" Fascia | Trim | 24,26,29 | Yes | A (20") | 13.5 | Large fascia board |
| FAS13 | 1.5" x 3.5" Fascia | Trim | 24,26,29 | Yes | A (20") | 6.0 | Standard fascia (replaces FA3) |
| FAS15 | 1.5" x 5.5" Fascia | Trim | 24,26,29 | Yes | A (20") | 8.0 | Mid-size fascia (replaces FA5) |
| FAS17 | 1.5" x 7.25" Fascia | Trim | 24,26,29 | Yes | A (20") | 9.5 | Large fascia (replaces FA7) |
| FAS198 | 1.5" x 9.25" Fascia | Trim | 24,26,29 | Yes | A (20") | 12.0 | Extra-large fascia |
| FCH | 0.5" F Channel | Trim | 24,26,29 | Yes | A (20") | 4.0 | Half-inch channel |
| FCJ | Framing Closure-J | Trim | 24,26,29 | Yes | A (20") | 6.5 | Complex closure detail |
| FJC | F&J Channel | Trim | 24,26,29 | Yes | A (20") | 6.0 | Combined F and J |
| GA | Gutter Apron | Trim | 24,26,29 | Yes | A (20") | 6.0 | Gutter transition |
| GF | Gambrel Flashing | Trim | 24,26,29 | Yes | A (20") | 11.5 | Gambrel shape flashing |
| GM | Gambrel | Trim | None | No | A (20") | 11.5 | Gambrel roof shape (CRITICAL) |
| GT | Gable Trim | Trim | 24,26,29 | Yes | A (20") | 10.25 | Peak roof trim |
| HC | Hip Cap | Trim | 24,26,29 | Yes | A (20") | 12.0 | Hip roof transition |
| HFC | HF Cleat | Trim | 24,26,29 | Yes | A (20") | 3.0 | HF attachment cleat |
| HFCL | HF Dormer (Endwall) Flashing | Trim | 24,26,29 | Yes | A (20") | 13.5 | HF dormer penetration |
| HFDE | HF Drip Edge | Trim | 24,26,29 | Yes | A (20") | 8.0 | HF water management |
| HFGT | HF Gable | Trim | 24,26,29 | Yes | A (20") | 10.0 | HF peak detail |
| HFHC | HF Hip Cap | Trim | 24,26,29 | Yes | A (20") | N/A | HF hip transition |
| HFR | HF Rake | Trim | 24 | Yes | A (20") | 10.0 | HF slope trim (24ga only) |
| HFR1 | HF Rake 01 | Trim | 24,26,29 | Yes | A (20") | 7.5 | HF slope variant 1 |
| HFR2 | HF Rake 02 | Trim | 24,26,29 | Yes | A (20") | 17.5 | HF slope variant 2 |
| HFRC | HF Ridge Cap | Trim | 24,26,29 | Yes | A (20") | 16.0 | HF peak ridge detail |
| HFSF | HF Sidewall Flashing | Trim | 24,26,29 | Yes | B (41") | 6.0 | HF wall penetration (41" material) |
| HFTF | HF Transition/Pitch Change | Trim | 24,26,29 | Yes | B (41") | 16.0 | HF slope transition (41" material) |
| HFVF | HF Valley | Trim | 24,26,29 | Yes | B (41") | 24.0 | HF valley detail (41" material) |
| HFVZ | HF Vented Z | Trim | 24,26,29 | Yes | B (41") | 5.5 | HF vented Z (41" material) |
| HIP | 4 x 4 Hip Trim | Trim | 24,26,29 | Yes | A (20") | 8.0 | Hip roof angle detail |
| HT | Hem Trim | Trim | 24,26,29 | Yes | A (20") | 4.0 | Hemmed edge trim |
| IC | Inside Corner (Standard) | Trim | 24,26,29 | Yes | A (20") | 12.0 | Interior angle corner |
| IC5 | 5.5" Inside Corner 10'3" | Trim | 24,26,29 | Yes | A (20") | 12.0 | Corner size variant |
| ICT | Inside Corner Trim 6" | Trim | 26,29 | Yes | A (20") | 15.0 | Large corner trim |
| JC | J Channel (Standard) | Trim | 24,26,29 | Yes | A (20") | 5.0 | Standard J-channel |
| JCP | PBR J Channel | Trim | 24,26,29 | Yes | A (20") | 7.0 | Commercial variant J |
| JCH | J Channel | Trim | 24,26,29 | Yes | A (20") | 6.0 | Alternative J designation |
| JT | J Trim | Trim | 24,26,29 | Yes | A (20") | 5.0 | Sidewall J-trim |
| JT12 | 0.5" J Trim | Trim | 26,29 | Yes | A (20") | 5.0 | Half-inch J variant |
| KOT | 4 x 4 Kick Out Trim | Trim | 24,26,29 | Yes | A (20") | 11.0 | Wall kick-out detail |
| LZB | LZ Bar | Trim | 24,26,29 | Yes | A (20") | 7.0 | Light Z-bar variant |
| MET3 | Mini Eave Trim 3" | Trim | 24,26,29 | Yes | A (20") | 8.0 | Compact eave trim |
| MRAC | Mini Rake & Corner 3" | Trim | 24,26,29 | Yes | A (20") | 10.0 | Compact peak trim |
| OC | Outside Corner | Trim | None | No | A (20") | 12.0 | Exterior angle (CRITICAL) |
| ODHC | O/H Door Header Cover 1.5" X 24" | Trim | 26,29 | Yes | B (41") | 26.0 | Overhead door header (41" material) |
| ODT10 | Overhead Door Trim 10" | Trim | 26,29 | Yes | A (20") | 16.0 | 10" overhead door trim |
| ODT8 | Overhead Door Trim 8" | Trim | 26,29 | Yes | A (20") | 14.0 | 8" overhead door trim |
| ODTD10 | Overhead Door Trim w/Drip 10" | Trim | 26,29 | Yes | A (20") | 14.0 | Door trim + drip |
| ODTD8 | Overhead Door Trim w/Drip 8" | Trim | 26,29 | Yes | A (20") | 12.0 | Door trim + drip |
| PCF | Pitch Change Flashing | Trim | 24,26,29 | Yes | A (20") | 10.5 | Roof slope transition |
| PT | Peak Trim | Trim | 24,26,29 | Yes | A (20") | 11.0 | Roof peak finish |
| PT4 | Prow Trim 4" | Trim | 26,29 | Yes | A (20") | 17.0 | 4" prow extension |
| RAC | Rake & Corner 6" | Trim | 24,26,29 | Yes | A (20") | 13.0 | Slope and corner detail |
| RC | Ridge Cap (Standard) | Trim | 24,26,29 | Yes | A (20") | 12.0 | Standard roof ridge |
| RC10 | 10" Ridge Cap 10'3" | Trim | 26,29 | Yes | A (20") | 12.0 | 10-inch ridge variant |
| RC14 | 14" Ridge Cap 10'3" | Trim | 24,26,29 | Yes | A (20") | 15.0 | 14-inch ridge variant |
| RC20 | 20" Ridge Cap 10'3" | Trim | 26,29 | Yes | B (41") | 21.0 | 20-inch ridge (41" material) |
| RC24 | 24" Ridge Cap 10'3" | Trim | 24,26,29 | Yes | B (41") | 25.0 | 24-inch ridge (41" material) |
| RET | Residential Eave Trim | Trim | 26,29 | Yes | A (20") | 6.5 | Residential soffit trim |
| RG | Rat Guard (Standard) | Trim | 24,26,29 | Yes | A (20") | 5.0 | Rodent barrier |
| RGP | PBR Rat Guard | Trim | 24,26,29 | Yes | A (20") | 6.0 | Commercial variant |
| RRC | Residential Rake & Corner | Trim | 26,29 | Yes | A (20") | 9.0 | Residential peak detail |
| RR4 | 4" Residential Rake 10'3" | Trim | 24,26,29 | Yes | A (20") | 7.0 | 4-inch slope trim |
| RR5 | 5.5" Residential Rake 10'3" | Trim | 24,26,29 | Yes | A (20") | 9.0 | 5.5-inch slope trim |
| RTC225 | Round Track Cover #225 | Trim | 26,29 | Yes | A (20") | 12.0 | Round track #225 |
| RTC226 | Round Track Cover #226 | Trim | 26,29 | Yes | A (20") | 13.0 | Round track #226 |
| SB | Snow Bar | Trim | 24,26,29 | Yes | A (20") | 5.0 | Snow load barrier |
| SD2 | Sliding Door 7.25" | Trim | 26,29 | Yes | A (20") | 11.0 | 7.25" door opening |
| SD6 | Sliding Door (Generic 26ga) | Trim | 26 | Yes | A (20") | 11.0 | 26ga-only generic door |
| SDT7 | Sliding Door Trim 7.25" | Trim | 26,29 | Yes | A (20") | 11.0 | 7.25" door trim |
| SDT9 | Sliding Door Trim 9.25" | Trim | 26,29 | Yes | A (20") | 14.0 | 9.25" door trim |
| SIDEF | Sidewall Flashing | Trim | 26,29 | Yes | A (20") | 9.0 | Wall penetration flashing |
| SS | Snow Stop | Trim | 26,29 | Yes | A (20") | 5.5 | Snow retention detail |
| STC | Square Track Cover | Trim | 24,26,29 | Yes | A (20") | 11.0 | Square track protection |
| SW | Sidewall (Standard) | Trim | 24,26,29 | Yes | A (20") | 8.0 | Wall base finish |
| TC | Track Cover (Standard) | Trim | 24,26,29 | Yes | A (20") | 12.0 | Track protection |
| TBC | Track Board Cover | Trim | 24,26,29 | Yes | A (20") | 6.0 | Board track cover |
| VV | V-Valley | Trim | None | No | B (41") | 21.0 | Valley detail (CRITICAL, 41" material) |
| WV | W-Valley (Standard) | Trim | 24,26,29 | Yes | B (41") | 21.0 | W-profile valley (41" material) |
| WV20 | W-Valley 20" | Trim | 26,29 | Yes | A (20") | 20.0 | 20-inch W-valley |
| WV24 | W-Valley 24" | Trim | 24,26,29 | Yes | B (41") | 24.0 | 24-inch W-valley (41" material) |
| WV36 | W-Valley 36" | Trim | 26,29 | Yes | B (41") | 36.0 | 36-inch W-valley (41" material) |
| ZBAR | Z Bar | Trim | 24,26,29 | Yes | A (20") | 5.0 | Standard Z-profile |
| ZBP | PBR Z Bar | Trim | 24,26,29 | Yes | A (20") | 6.0 | Commercial Z variant |
| ZCFF | Z Closure for FF100 1" | Trim | 26,29 | Yes | A (20") | 3.5 | FF100 panel Z-closure |
| ZCFS | Z Closure for SSQ 1.75" | Trim | 26,29 | Yes | A (20") | 6.0 | SSQ550/675 Z-closure |
| ZT | Zee Trim | Trim | 26,29 | Yes | A (20") | 5.0 | Alternative Z designation |

---

### Panel Families (8)

These are the **only 8 real panels** produced by Greenfield Metal Sales. Any panel family not in this list should be treated with suspicion.

| Family | Full Name | Type | Gauges | Length Code? | Material Pattern | Profile Type | Notes |
|--------|-----------|------|--------|--------------|------------------|--------------|-------|
| Classic Rib | Classic Rib Panel | Panel-Standing | 26,29 | Yes | A (20") | Standing Seam | Commercial standard rib |
| PBR | Pro-Grade Rib Panel | Panel-Standing | 24,26,29 | Yes | A (20") | Standing Seam | Premium rib variant |
| Pro Panel | Pro Panel (Premium) | Panel-Standing | 26,29 | Yes | A (20") | Standing Seam | High-performance panel |
| FF100 | Flat Face 100 | Panel-Flat | 26,29 | Yes | A (20") | Flat Face | Smooth finish profile |
| SSQ550 | Symmetrical Square 550 | Panel-Box | 26,29 | Yes | A (20") | Box Rib | Box rib standard |
| SSQ675 | Symmetrical Square 675 | Panel-Box | 26,29 | Yes | A (20") | Box Rib | Box rib large |
| Trapezoid | Trapezoidal Panel | Panel-Trap | 26,29 | Yes | A (20") | Trapezoidal | Trapezoidal corrugation |
| B&B | Board & Batten Panel | Panel-Special | 24,26,29 | Yes | A (20") | Specialty | Board & batten variant |

---

### Coils (Raw Material)

| Family | Full Name | Type | Gauges | Width | Notes |
|--------|-----------|------|--------|-------|-------|
| CO2024 | 20-inch Coil 24ga | Coil | 24 | 20" | Pattern A sourcing |
| CO2026 | 20-inch Coil 26ga | Coil | 26 | 20" | Pattern A sourcing (primary) |
| CO2029 | 20-inch Coil 29ga | Coil | 29 | 20" | Pattern A sourcing (primary) |
| CO4124 | 41-inch Coil 24ga | Coil | 24 | 41" | Pattern B sourcing |
| CO4126 | 41-inch Coil 26ga | Coil | 26 | 41" | Pattern B sourcing (primary for HF) |
| CO4129 | 41-inch Coil 29ga | Coil | 29 | 41" | Pattern B sourcing (primary for HF) |

---

### Flatsheets (Raw Material)

| Family | Full Name | Type | Gauges | Width | Notes |
|--------|-----------|------|--------|-------|-------|
| FS2024 | 20-inch Flatsheet 24ga | Flatsheet | 24 | 20" | Pattern A backup |
| FS2026 | 20-inch Flatsheet 26ga | Flatsheet | 26 | 20" | Pattern A backup |
| FS2029 | 20-inch Flatsheet 29ga | Flatsheet | 29 | 20" | Pattern A backup |
| FS4124 | 41-inch Flatsheet 24ga | Flatsheet | 24 | 41" | Pattern B sourcing |
| FS4126 | 41-inch Flatsheet 26ga | Flatsheet | 26 | 41" | Pattern B backup |
| FS4129 | 41-inch Flatsheet 29ga | Flatsheet | 29 | 41" | Pattern B backup |
| FS4126CMG* | 41-inch Flatsheet 26ga CMG (color-specific) | Flatsheet | 26 | 41" | HF family CMG colors (e.g., FS4126CMG-DKB for Deep Black) |

---

### Legacy Families (4) — Deprecated

These families are no longer sold but may still appear in Paradigm inventory or historical orders:

| Family | Full Name | Status | Replacement | Notes |
|--------|-----------|--------|------------|-------|
| FA3 | 1.5" x 3.5" Fascia | Deprecated | FAS13 | Old fascia encoding |
| FA5 | 1.5" x 5.5" Fascia | Deprecated | FAS15 | Old fascia encoding |
| FA6 | Fascia (Generic 26ga) | Deprecated | FAS13/FAS15/FAS17 | Generic catch-all |
| FA7 | 1.5" x 7.5" Fascia | Deprecated | FAS17 | Old fascia encoding |

---

### Under Review / Partial Families (70+)

The following families have inventory in Paradigm but lack complete specifications (stretchout, bends, hems, gauges). Many are HF variants or commercial rib configurations. Handle with caution — contact Paradigm support or use GMS-internal reference before quoting:

**HF Variants (incomplete)**: HFBT, HFDF, HFJT, HFRG, HFRG2

**Commercial Rib Overflow**: CRD10110, CRD10112, CRD10114, CRD10116, CRD810, CRD812, CRD814, CRD816, CRDD10110, CRDD10112, CRDD10114, CRDD10116, CRDD810, CRDD812, CRDD814, CRDD816

**Generic Catch-Alls**: BB, C, ET, FA, FAS1, HF, HFR119, HFR2, HFEW, HFZC, OD, PB, PBRC, R, RR, RT, SBT, SI, ST, ZC

**Specialty 610 Singles** (3 items each): HFDE610, HFEW610, HFGT610, HFHC610, HFRC610, HFTF610, HFVF610

---

## Tricky Families (11)

### Families with Embedded Numbers in Prefix

These prefixes contain numbers that are **part of the family name**, NOT length codes. Be careful when parsing:

| Family | Full Name | Embedded Meaning | Example PID | Notes |
|--------|-----------|------------------|------------|-------|
| ANG11 | 1.5" x 1.5" Angle | 11 = 1.5" dimension | ANG116MGALM12 | Digits indicate size, not length |
| ANG22 | 2" x 2" Angle | 22 = 2" dimension | ANG226BK10 | Digits indicate size, not length |
| ANG33 | 3" x 3" Angle | 33 = 3" dimension | ANG336AG15 | Digits indicate size, not length |
| CRD81 | Com. Rib O/H Door 8" | 81 = 8" door | CRD816MGALM12 | Old encoding variant |
| CRD810 | Com. Rib O/H Door 8" | 810 = 8" door | CRD8106BK10 | Newer encoding variant |
| CRD1011 | Com. Rib O/H Door 10" | 1011 = 10" door | CRD10116MGALM12 | Complex multi-digit encoding |
| RC10 | 10" Ridge Cap | 10 = 10" height | RC106AG12 | Numeric size specification |
| RC14 | 14" Ridge Cap | 14 = 14" height | RC146BK15 | Numeric size specification |
| RC20 | 20" Ridge Cap | 20 = 20" height | RC206AG18 | Numeric size specification |
| RC24 | 24" Ridge Cap | 24 = 24" height | RC246BK20 | Numeric size specification |
| BBQ750 | (if it exists) | 750 = spec code | TBD | Review family — verify before use |
| SSQ550 | Symmetrical Square 550 | 550 = profile code | SSQ5506AG18 | Panel family with numeric profile |
| SSQ675 | Symmetrical Square 675 | 675 = profile code | SSQ6756BK20 | Panel family with numeric profile |
| FF100 | Flat Face 100 | 100 = profile code | FF1006AG18 | Panel family with numeric profile |

**Decoding Rule**: When you see a family prefix with digits, check the full family list first. If it's in this table, the digits are part of the family name and NOT a length code.

---

## Paradigm-Only Aliases (5)

### Short Prefixes Used in Paradigm

Paradigm occasionally uses short/abbreviated prefixes in certain contexts. These map to full trim families:

| Short Prefix | Maps To | Full Name | Usage Context | Notes |
|--------------|---------|-----------|----------------|-------|
| SF | HFSF | HF Sidewall Flashing | Paradigm item lookups | Paradigm-specific alias (rare) |
| TF | HFTF | HF Transition/Pitch Change | Paradigm item lookups | Paradigm-specific alias (rare) |
| VF | HFVF | HF Valley | Paradigm item lookups | Paradigm-specific alias (rare) |
| VZ | HFVZ | HF Vented Z | Paradigm item lookups | Paradigm-specific alias (rare) |
| (Reserved) | (TBD) | (TBD) | Paradigm extensions | Check with Paradigm support |

**Important**: These short aliases are NOT used in actual product IDs or inventory codes. They appear only in Paradigm database lookups or admin functions. Always use the full family prefix in actual quotes and orders.

---

## Quick Lookup by Product Type

Organized by application / product category for rapid family identification:

### Edge Trim / Sidewall / Wall Base
- **JT** — J Trim (standard sidewall, 5" stretchout)
- **JC** — J Channel (standard, 5" stretchout)
- **JCH** — J Channel (alternative designation, 6" stretchout)
- **JCP** — PBR J Channel (commercial variant, 7" stretchout)
- **JT12** — 0.5" J Trim (half-inch variant)
- **SW** — Sidewall (standard, 8" stretchout)
- **BT** — Base Trim (foundation, 6.5" stretchout)
- **BST** — Bottom Starter (1" base, 4" stretchout)

### Ridge / Peak / Hip
- **RC** — Ridge Cap (standard, 12" stretchout, 0 hems)
- **RC10** — 10" Ridge Cap (12" stretchout)
- **RC14** — 14" Ridge Cap (15" stretchout)
- **RC20** — 20" Ridge Cap (21" stretchout, 41" material)
- **RC24** — 24" Ridge Cap (25" stretchout, 41" material)
- **HC** — Hip Cap (hip roof, 12" stretchout)
- **HIP** — 4x4 Hip Trim (hip angle, 8" stretchout)
- **PT** — Peak Trim (roof peak finish, 11" stretchout)

### Rake / Slope / Gable
- **GT** — Gable Trim (peak roof, 10.25" stretchout)
- **RR4** — 4" Residential Rake (slope trim, 7" stretchout)
- **RR5** — 5.5" Residential Rake (slope trim, 9" stretchout)
- **RAC** — Rake & Corner 6" (slope + corner, 13" stretchout)
- **CRRC** — Com. Rib Rake & Corner (commercial slope, 17" stretchout)
- **MRAC** — Mini Rake & Corner 3" (compact slope, 10" stretchout)
- **HFR** — HF Rake (HF slope, 24ga only, 10" stretchout)
- **HFR1** — HF Rake 01 (HF slope variant, 7.5" stretchout)
- **HFR2** — HF Rake 02 (HF slope variant, 17.5" stretchout)

### Flashing / Water Management
- **DF** — Drip Flashing (standard, 4.5" stretchout)
- **DE** — Drip Edge (eave water management, 5" stretchout)
- **DC** — Drip Cap (simple barrier, 3.25" stretchout)
- **CRDF** — Com. Rib Drip Flashing (commercial, 8" stretchout)
- **BBDF** — Board & Batten Drip Flashing (B&B variant)
- **ENDF** — Endwall Flashing (gable penetration, 8" stretchout)
- **CCF** — Counter/Chimney Flashing (roof penetration, 5" stretchout)
- **PCF** — Pitch Change Flashing (slope transition, 10.5" stretchout)
- **SIDEF** — Sidewall Flashing (wall penetration, 9" stretchout)
- **GF** — Gambrel Flashing (gambrel shape, 11.5" stretchout)

### J-Trim / Channel / Complex
- **FCH** — 0.5" F Channel (half-inch channel, 4" stretchout)
- **FJC** — F&J Channel (combined F+J, 6" stretchout)
- **DJT** — Door Jamb Trim (door side trim, 9" stretchout)
- **DJT12** — Double J Trim 0.5" (half-inch double J, 9" stretchout)
- **DJT78** — Double J Trim 0.875" (seven-eighths J, 8" stretchout)
- **CRDJ1** — Com. Rib Double J 0.5" (commercial double J, 12" stretchout)
- **CRDJ2** — Com. Rib Double J 1.375" (commercial double J, 10" stretchout)

### Interior / Outside Corner
- **IC** — Inside Corner (standard, 12" stretchout, complex bends)
- **IC5** — 5.5" Inside Corner (size variant, 12" stretchout)
- **ICT** — Inside Corner Trim 6" (large corner, 15" stretchout)
- **OC** — Outside Corner (exterior angle, CRITICAL — no gauges listed)
- **BBIC** — Board & Batten Inside Corner (B&B variant, 17" stretchout)
- **BBOC** — Board & Batten Outside Corner (B&B variant, 17" stretchout)
- **CO5** — 5.5" Corner 10'3" (residential corner, 11" stretchout)
- **CPBR** — PBR Corner (commercial corner, 12" stretchout)

### Eave / Soffit / Fascia
- **EV** — Eave (standard eave edge, 5.75" stretchout)
- **EVET** — Eave Trim (premium eave trim, 9" stretchout)
- **EVET90** — Eave Trim 90 (90-degree variant, 8" stretchout)
- **ET4** — 3" x 4" Eave Trim (eave transition, 7" stretchout)
- **ET5** — 3" x 5.5" Eave Trim (larger eave trim, 9" stretchout)
- **RET** — Residential Eave Trim (residential soffit, 6.5" stretchout)
- **MET3** — Mini Eave Trim 3" (compact eave, 8" stretchout)
- **FAS13** — 1.5" x 3.5" Fascia (small fascia board, 6" stretchout)
- **FAS15** — 1.5" x 5.5" Fascia (mid-size fascia, 8" stretchout)
- **FAS17** — 1.5" x 7.25" Fascia (large fascia, 9.5" stretchout)
- **FAS111** — 1.5" x 11.25" Fascia (extra-large fascia, 13.5" stretchout)
- **FAS198** — 1.5" x 9.25" Fascia (large fascia, 12" stretchout)

### Doors / Openings
- **ODT8** — Overhead Door Trim 8" (8" door opening, 14" stretchout)
- **ODT10** — Overhead Door Trim 10" (10" door opening, 16" stretchout)
- **ODTD8** — O/H Door Trim w/Drip 8" (door + drip, 12" stretchout)
- **ODTD10** — O/H Door Trim w/Drip 10" (door + drip, 14" stretchout)
- **ODHC** — O/H Door Header Cover (header protection, 41" material, 26" stretchout)
- **SDT7** — Sliding Door Trim 7.25" (slide door trim, 11" stretchout)
- **SDT9** — Sliding Door Trim 9.25" (slide door trim, 14" stretchout)
- **SD2** — Sliding Door 7.25" (slide door alternate, 11" stretchout)
- **SD6** — Sliding Door (generic 26ga, 11" stretchout)
- **DJT** — Door Jamb Trim (door side trim, 9" stretchout)

### Commercial Rib (CR) Variants
- **CRB** — Commercial Rib Base (foundation, 6" stretchout)
- **CRJ** — Commercial Rib J (J-channel, 8" stretchout)
- **CRDF** — Com. Rib Drip Flashing (water management, 8" stretchout)
- **CRRC** — Com. Rib Rake & Corner (peak detail, 17" stretchout)
- **CRSF** — Com. Rib Sidewall Flashing (wall penetration, 14" stretchout)
- **CRZ** — Commercial Rib Zee (Z-profile, 6" stretchout)
- **CRD81** — Com. Rib O/H Door 8" (8" overhead door, 14" stretchout, TRICKY)
- **CRD810** — Com. Rib O/H Door 8" (8" overhead door, 14" stretchout, TRICKY)
- **CRD1011** — Com. Rib O/H Door 10" (10" overhead door, 16" stretchout, TRICKY)
- **CRDD** variants — Com. Rib O/H Door w/Drip (door + drip, complex family)

### Board & Batten (BB) Variants
- **BBJT** — Board & Batten J Trim (J-channel, 4.75" stretchout)
- **BBBT** — Board & Batten Base Trim (foundation, 4" stretchout)
- **BBDF** — Board & Batten Drip Flashing (water management, 4.25" stretchout)
- **BBHT** — Board & Batten Hem Trim (hem edge, 3.75" stretchout)
- **BBIC** — Board & Batten Inside Corner (interior angle, 17" stretchout)
- **BBOC** — Board & Batten Outside Corner (exterior angle, 17" stretchout)
- **BBRG** — Board & Batten Rat Guard (rodent barrier, 4" stretchout)
- **BBSD7** — Board & Batten Sliding Door (door opening, 12" stretchout)
- **BBODT** — Board & Batten O/H Door Trim (overhead door, 4.75" stretchout)
- **BB3** — 3.5" Band Board (flat fascia, 10" stretchout, 0 bends)
- **BB5** — 5.5" Band Board (flat fascia, 12" stretchout, 0 bends)

### Valley
- **WV** — W-Valley (standard W-profile, 41" material, 21" stretchout)
- **WV20** — W-Valley 20" (20" W-valley, 20" material, 20" stretchout)
- **WV24** — W-Valley 24" (24" W-valley, 41" material, 24" stretchout)
- **WV36** — W-Valley 36" (36" W-valley, 41" material, 36" stretchout)
- **VV** — V-Valley (V-profile, 41" material, CRITICAL, 21" stretchout)
- **HFVF** — HF Valley (HF valley detail, 41" material, 24" stretchout)

### Z-Profile / Zee
- **ZBAR** — Z Bar (standard Z-profile, 5" stretchout)
- **ZBP** — PBR Z Bar (commercial Z, 6" stretchout)
- **ZT** — Zee Trim (alternative Z, 5" stretchout)
- **CRZ** — Commercial Rib Zee (commercial Z variant, 6" stretchout)
- **LZB** — LZ Bar (light Z-bar, 7" stretchout)
- **ZCFF** — Z Closure for FF100 (panel closure, 3.5" stretchout)
- **ZCFS** — Z Closure for SSQ (panel closure, 6" stretchout)
- **HFVZ** — HF Vented Z (HF vented Z, 41" material, 5.5" stretchout)

### HF Family (High-end / Premium)
**All HF families use 41-inch material in production (verified 2026-03-18)**

- **HFBT** — HF Bull Trim (under review — specifications incomplete)
- **HFCL** — HF Dormer (Endwall) Flashing (dormer penetration, 13.5" stretchout)
- **HFDE** — HF Drip Edge (water management, 8" stretchout)
- **HFDF** — HF Drip Flashing (under review — specifications incomplete)
- **HFJT** — HF J-Trim (under review — specifications incomplete)
- **HFGT** — HF Gable (peak detail, 10" stretchout)
- **HFHC** — HF Hip Cap (hip transition, unknown stretchout)
- **HFR** — HF Rake (slope trim, 24ga only, 10" stretchout)
- **HFR1** — HF Rake 01 (slope variant, 7.5" stretchout)
- **HFR2** — HF Rake 02 (slope variant, 17.5" stretchout)
- **HFRC** — HF Ridge Cap (peak ridge, 16" stretchout)
- **HFRG** — HF Rat Guard (under review — specifications incomplete)
- **HFSF** — HF Sidewall Flashing (wall penetration, 6" stretchout, 41" material)
- **HFTF** — HF Transition/Pitch Change (slope transition, 16" stretchout, 41" material)
- **HFVF** — HF Valley (valley detail, 24" stretchout, 41" material)
- **HFVZ** — HF Vented Z (vented Z, 5.5" stretchout, 41" material)
- **HFC** — HF Cleat (attachment hardware, 3" stretchout)

### Angle / Hardware
- **ANG11** — 1.5" x 1.5" Angle (corner angle, 4" stretchout, TRICKY)
- **ANG22** — 2" x 2" Angle (corner angle, 5" stretchout, TRICKY)
- **ANG33** — 3" x 3" Angle (corner angle, 7" stretchout, TRICKY)

### Track / Storage / Hardware
- **TC** — Track Cover (standard, 12" stretchout)
- **STC** — Square Track Cover (square track, 11" stretchout)
- **RTC225** — Round Track Cover #225 (round track variant, 12" stretchout)
- **RTC226** — Round Track Cover #226 (round track variant, 13" stretchout)
- **DTC** — Double Track Cover (two-track, 13" stretchout)
- **TBC** — Track Board Cover (board cover, 6" stretchout)

### Specialty / Premium Details
- **GM** — Gambrel (gambrel roof shape, CRITICAL — no gauges listed)
- **CPFRC** — Commercial Panel Formed Ridge Cap (panel ridge, no gauges listed)
- **KOT** — 4x4 Kick Out Trim (wall kick-out, 11" stretchout)
- **GA** — Gutter Apron (gutter transition, 6" stretchout)
- **HT** — Hem Trim (hemmed edge, 4" stretchout)
- **EW** — Endwall (gable/end finish, 10.25" stretchout)
- **SB** — Snow Bar (snow load barrier, 5" stretchout)
- **SS** — Snow Stop (snow retention, 5.5" stretchout)
- **RG** — Rat Guard (standard, rodent barrier, 5" stretchout)
- **RGP** — PBR Rat Guard (commercial rodent barrier, 6" stretchout)
- **BBHT** — Board & Batten Hem Trim (B&B hemmed edge, 3.75" stretchout)
- **BBRG** — Board & Batten Rat Guard (B&B rodent barrier, 4" stretchout)
- **PT4** — Prow Trim 4" (prow extension, 17" stretchout)
- **RRC** — Residential Rake & Corner (residential peak, 9" stretchout)
- **FCJ** — Framing Closure-J (complex J closure, 6.5" stretchout)

---

## Material Sourcing Patterns

### Pattern A — 20-inch Material (Most families)

Used by **131 ACTIVE trim families**, 8 panels, and most raw materials.

| Gauge | Primary Component | Backup | UOM |
|-------|------------------|--------|-----|
| 24ga | FS2024 (flatsheet) | — | LF |
| 26ga | CO2026 (coil) | FS2026 (flatsheet) | LF |
| 29ga | CO2029 (coil) | FS2029 (flatsheet) | LF |

**BOM Stretchout**: TIP (0.02439 = 1/20)

---

### Pattern B — 41-inch Material (8 families + HF override)

Used by: **HFVF, ODHC, RC20, RC24, VV, WV, WV24, WV36** + all **HF families** (HFBT, HFCL, HFDE, HFDF, HFGT, HFHC, HFJT, HFR, HFR1, HFR2, HFRC, HFRG, HFSF, HFTF, HFVF, HFVZ, HFC)

| Gauge | Primary Component | Backup | UOM | Notes |
|-------|------------------|--------|-----|-------|
| 24ga | FS4124 (flatsheet) | — | LF | 24ga-only sourcing |
| 26ga | CO4126 (coil) | FS4126 (flatsheet) | LF | Primary for most products |
| 29ga | CO4129 (coil) | FS4129 (flatsheet) | LF | Primary for most products |

**HF + CMG Override**: For CMG colors in HF families, use **FS4126CMG{color-abbrev}** flatsheet instead of CO4126CMG coil.
- Example: HFSF + CMG Almond = FS4126CMG-CMGALM (flatsheet, EA UOM)
- Example: HFSF + US Alamo White = CO4129AW (coil, LF UOM)

**BOM Stretchout**: TIP (0.02439 = 1/41)

---

## PID Structure & Decoding

### Format

```
{FAMILY}{GAUGE_DIGIT}{COLOR_CODE}{LENGTH}
```

### Gauge Digit Rules

| Digit | Gauge | Multiplier | CMG Only? |
|-------|-------|-----------|-----------|
| 4 | 24ga | x1.44 | YES — no US standard in 24ga |
| 6 | 26ga | x1.20 | NO — both US & CMG available |
| 9 | 29ga | x1.0 (base) | NO — both US & CMG available |

### Color Code Rules

| Category | Total Colors | Gauge Range | Abbrev Format | Notes |
|----------|--------------|------------|----------------|-------|
| US Standard | 43 | 29ga, 26ga | 2-3 chars (e.g., AW, AG, BK) | No 24ga |
| US Crinkle | 18 | 29ga, 26ga | 3-4 chars (e.g., AWC, AGC) | +15% premium (not yet applied) |
| US Matte | 7 | 29ga, 26ga | 3 chars (e.g., MBB, MBW) | +8% premium (not yet applied) |
| US Woodgrain | 30 | 26ga only | 2-4 chars (e.g., BP, DO, KAP) | No 29ga, no 24ga |
| CMG Standard | 45 | 26ga, 24ga | 5-7 chars (e.g., CMGALM, CMGBK) | 24ga available for select colors |
| CMG Crinkle | 14 | 26ga only | 6-7 chars (e.g., CMGBRC) | No 24ga, no 29ga |
| CMG Matte ULG | 7 | 24ga only | 6-7 chars (e.g., CMGBURM) | 24ga only |

### Example PIDs

```
HFBT6MGALM12      HF Bull Trim, 26ga, CMG Almond, 12 feet
BBJT9AW10         Board & Batten J-Trim, 29ga, Alamo White, 10 feet
RC246BK20         24" Ridge Cap, 24ga, Deep Black, 20 feet
CO2026AG          20-inch Coil, 26ga, Ash Gray (no length code)
FS4126CMG-DKB     41-inch Flatsheet, 26ga, CMG Deep Black (flatsheet format)
RC206BK18         20" Ridge Cap, 26ga, Black, 18 feet (41" material)
```

---

## Revision History

| Date | Change |
|------|--------|
| 2026-03-28 | Created comprehensive family registry with all 147 families. Documented tricky families (11), Paradigm aliases (5), material patterns (A/B), and 14 product type categories. HF family 41-inch material sourcing confirmed. |
| 2026-03-18 | Trim profiles reference confirms 131 ACTIVE families + 8 panels + 4 legacy families. HF family material override verified by Matt Amundson. |

---

## Quick Reference: Material Pattern Decision Tree

When determining material sourcing for a family:

1. **Is it a coil or flatsheet?** → Use raw material rows (CO*, FS*)
2. **Is it HF family?** → Use 41" pattern B, CMG override to FS4126CMG
3. **Is it in Pattern B list?** (HFVF, ODHC, RC20, RC24, VV, WV, WV24, WV36) → Use 41" pattern B
4. **Is it an ACTIVE trim or panel?** → Use 20" pattern A (default)
5. **Is it legacy or under review?** → Check Paradigm master reference for sourcing details

---

## Key Definitions

- **Stretchout**: Inches of material required per linear foot of finished trim
- **Length Code**: Whether a final digit in the PID indicates the finished length (Yes/No)
- **Material Pattern**: Whether the family uses 20-inch coils (A) or 41-inch material (B)
- **TIP**: Trim In Process — unit of measure (1" × 12" metal piece, or 1/20 coil or 1/41 flatsheet)
- **LF**: Linear Feet — unit of measure for trim lengths
- **EA**: Each — unit of measure for flatsheet components
- **Gauge**: Sheet metal thickness (24ga = thickest CMG, 26ga = mid, 29ga = thinnest)
- **CRITICAL**: Family status indicating missing/conflicting specification data requiring manual verification
- **COMPLETE**: Family status indicating full specification data available
- **Embedded Numbers**: Digits in family prefix that are part of the family name (e.g., ANG11, CRD81, SSQ550)
