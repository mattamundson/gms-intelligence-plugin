---
description: Decode a GMS product SKU into its components
argument-hint: [sku, e.g. "ANG114BK10" or multiple SKUs]
allowed-tools: Read, Glob, Grep
---

Decode the following GMS product SKU(s): $ARGUMENTS

Read the SKU decoder skill at `${CLAUDE_PLUGIN_ROOT}/skills/gms-sku-decoder/SKILL.md` and references in `${CLAUDE_PLUGIN_ROOT}/skills/gms-sku-decoder/references/`.

For each SKU provided:

1. **Parse structure** — Break down the product ID into family prefix, gauge digit, profile size, color code, and length.

2. **Identify product** — Map the family prefix to the product family (trim, panel, coil, flatsheet, accessory).

3. **Decode color** — Map the color code to the full color name and paint system. If the color code indicates a premium finish (MCC, CR/crinkle C-prefix, ULG), flag the +15% markup.

4. **Cross-reference** — Note the supplier (USS for 29/26ga SMP, CMG for 24/26ga Kynar), coil width, and availability status.

5. **Present clearly** — Show each decoded field in a clean format with the full human-readable product description.

If multiple SKUs are provided, present them in a comparison table.
