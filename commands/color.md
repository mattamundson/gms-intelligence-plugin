---
description: Look up a GMS color by name, code, or contractor alias
argument-hint: [color name/code/alias, e.g. "CBK" or "dark gray crinkle"]
allowed-tools: Read, Glob, Grep
---

Look up color information for: $ARGUMENTS

Read the color authority skill at `${CLAUDE_PLUGIN_ROOT}/skills/gms-color-authority/SKILL.md`.

Determine whether the input is:
- A **color code** (1-4 characters like BK, ARW, CCH, MCC)
- An **official color name** (like "Arctic White", "Burnished Slate")
- A **contractor alias** (like "dark gray", "barn red", "just black")

Then provide:

1. **Official color name** and code
2. **Paint system** — SMP (USS) or Kynar (CMG), or both if the name exists in both systems (flag the cross-system warning)
3. **Finish type** — Standard, Crinkle, Matte, or ULG. If premium, note the +15% markup.
4. **Available gauges** — Which gauges carry this color, and the availability status (stock, slitting, PTO) for each
5. **Coil-level surcharge** — Any per-LF surcharge above base for this finish/color
6. **Lead time** — Based on supplier and availability status
7. **Color family** — Which family it belongs to (White, Black, Gray, Red, Blue, Green, Brown, Tan, Metallic, Specialty)

If the input is ambiguous (e.g., "tan" could be Tan, Saddle Tan, or Buckskin), list all matches and ask for clarification.
