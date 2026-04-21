---
description: Quick-quote a GMS product with full cost breakdown
argument-hint: [product description, e.g. "100 LF Eave Trim 26ga Arctic White"]
allowed-tools: Read, Glob, Grep
---

Generate a quick quote for: $ARGUMENTS

Follow this process:

1. **Parse the request** — Extract product family, gauge, length, color, and quantity from the description. If anything is ambiguous, state assumptions clearly.

2. **Load pricing intelligence** — Read the gms-pricing-engine skill at `${CLAUDE_PLUGIN_ROOT}/skills/gms-pricing-engine/SKILL.md` and any relevant references in `${CLAUDE_PLUGIN_ROOT}/skills/gms-pricing-engine/references/`.

3. **Resolve color** — If a color is mentioned, read `${CLAUDE_PLUGIN_ROOT}/skills/gms-color-authority/SKILL.md` to identify the exact color name, code, paint system (SMP/Kynar), and any premium finish markup.

4. **Route supplier** — Read `${CLAUDE_PLUGIN_ROOT}/skills/gms-supplier-intel/SKILL.md` to determine the correct supplier (USS or CMG), coil specs, and lead time.

5. **Calculate cost** — Apply the GMS pricing formula:
   - Material = (Stretchout / Coil Width) x (Base Coil Cost + Finish Surcharge) x Length
   - Labor = SLIT + BEND + HEM costs per the assembly formula
   - Total Cost = Material + Labor
   - Sell Price = Cost / (1 - Target Margin)

6. **Present the quote** — Show a clean breakdown:
   - Product description with decoded SKU
   - Material cost per unit and total
   - Labor cost per unit and total
   - Sell price at target margin
   - Supplier, lead time, and availability
   - Any premium finish flags
