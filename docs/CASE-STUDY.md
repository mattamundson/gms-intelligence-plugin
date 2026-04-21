# Case Study: GMS Intelligence Plugin

## Context

Greenfield Metal Sales (GMS) is a Midwest manufacturer of standing-seam roofing, exposed-fastener panels, and architectural trim. The product catalog is ~91,000 SKUs across multiple product families, gauges, lengths, colors, and finishes. Pricing, sourcing, production, and sales all depend on shared domain knowledge that was previously tribal — held in people's heads, in spreadsheets, and in a 20-year-old Paradigm ERP instance.

This plugin was built to make that domain knowledge **addressable by Claude Code** — installable, versionable, evalable, and (where safety rails allow) automatable.

## The 11-skill production system

The internal production plugin ships 11 skills. This public repo ships 7 of them. The other 4 are described here so a reader of this case study understands the full scope, even though the code isn't public.

### Skills in this repo (7)

| Skill | Core pattern |
|---|---|
| `gms-pricing-engine` | Formula-driven: encode `sell = base × gauge × length × finish` as a reusable calculator with preview-before-apply safety rails |
| `gms-sku-decoder` | Parser + encoder: round-trip between product IDs and human-readable descriptions; ships two Python scripts as tools |
| `gms-material-estimator` | Geometric: building dimensions → panel/trim takeoff with waste factors |
| `gms-color-authority` | Catalog lookup with fuzzy aliases: "dark gray crinkle" → `CCH` (Crinkle Charcoal Gray) |
| `gms-production-nav` | Graph traversal: product → assembly → coil → labor ops |
| `gms-supplier-intel` | Routing logic: color/gauge combo → supplier + lead time + reorder math |
| `gms-inventory-health` | Time-series heuristics: velocity × days-on-hand → stock status |

### Skills in the internal plugin, not in this repo (4)

Dropped from the public repo for specific reasons:

- **`gms-battlecard`** — A competitive-intelligence skill covering three named regional competitors with positioning, objection handling, and win/loss patterns. Dropped because publishing specific competitor weakness claims carries defamation risk and exposes Greenfield's competitive strategy. The skill architecture is identical to the public skills — the signal value is in the others.
- **`gms-sales-outreach`** — Cold-email and follow-up templates targeted at the same competitors. Same reason.
- **`gms-customer-intel`** — ICP (ideal-customer-profile) classification, MABC health metrics, and churn-risk scoring. Dropped because the segmentation logic is real proprietary go-to-market strategy, not generic.
- **`jarvis-dev-companion`** — An internal developer-assistance skill that referenced specific service endpoints, bearer-token env vars, and dashboard URLs on the GMS internal platform. Dropped because the infrastructure refs aren't useful without access to that platform and are a minor footprint leak.

Pattern-wise, the 4 dropped skills are identical to the 7 public ones: frontmatter description as the trigger, SKILL.md for the main content, references/ for long tables, evals.json for assertions. A reader who wants to build competitive or customer-facing skills for **their** domain has all the scaffolding they need from the 7 public examples.

## Build process

1. **Domain interview** — one to two hours per domain with the person who owns it (pricing, production, sales, etc.). Record the call. The questions are always the same: "walk me through a normal request," "what's a request that looks normal but is actually a trap," "what's the math," "what's the reference data."
2. **Skill draft** — `SKILL.md` + `references/*.md` written from the interview transcript. The SKILL.md is scannable (≤~15K tokens); reference docs are deep-link material.
3. **Eval set** — 3 to 5 prompts per skill, each with 5 to 10 assertions. Assertions tiered as `critical-correctness` (must pass) / `correctness` (should pass) / `depth` (nice to have).
4. **Executor + Grader loop** — Sonnet executes the prompt with the skill loaded; Opus grades each assertion. Fails surface as specific lines in the skill to fix.
5. **Iterate until green.** Usually two to four cycles per skill. The eval HTMLs in this repo are the final-pass output.
6. **Scripts where it matters.** Pricing and SKU decoding got real Python because (a) both have complex invariants that are easier to test programmatically and (b) both are call-site integrations for other skills in the system. Most skills don't need scripts — plain SKILL.md was sufficient.

## What I would do differently

- **Fewer, larger skills.** The original 11 included one skill per "role" (sales vs customer intel) even when the underlying domain was similar. Merging customer-intel + sales-outreach into one `customer-lifecycle` skill would have been cleaner.
- **Eval data alongside the skill, not in a separate eval harness.** This repo puts `evals/evals.json` inside each skill folder — that's the right call. Earlier versions had evals in a sibling directory and they rotted.
- **Ship one pattern-reference skill.** A `how-to-write-a-skill.skill` that demonstrates the skill pattern itself. Future-me would have been more productive with a self-documenting template.

## Reusing this for another domain

The pattern translates cleanly to any vertical with:
- A moderately large product/concept catalog (≥1K items)
- Formula-driven pricing or scoring
- A reference system that's already written down somewhere (even if it's PDFs and spreadsheets)
- A few recurring question shapes per domain

Verticals it would fit well: insurance underwriting, medical coding, legal contract review, supply chain routing, real estate comparables, commercial lending. Each of those has a "pricing-engine-shaped" skill, a "decoder-shaped" skill, and one or two catalog-lookup skills waiting to be written.
