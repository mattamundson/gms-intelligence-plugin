# Install

## Requirements

- [Claude Code](https://claude.com/claude-code) 2.0+ installed and signed in
- macOS, Linux, or Windows (PowerShell or WSL)

## From a local clone

```bash
git clone https://github.com/mattamundson/gms-intelligence-plugin.git
cd gms-intelligence-plugin
claude plugin install ./
```

Verify the install:

```bash
claude plugin list
# should show: gms-intelligence 1.0.0
```

## From the Claude plugin marketplace (once published)

```bash
claude plugin marketplace add mattamundson/gms-intelligence-plugin
claude plugin install gms-intelligence
```

## What gets installed

After install, files live at:

```
~/.claude/plugins/gms-intelligence/
├── skills/            # 7 skills, auto-discovered by Claude Code
├── commands/          # 3 slash commands
└── .claude-plugin/plugin.json
```

## Verify skills are loading

Open a new Claude Code session and try:

```
/decode CRD8109BK10
```

You should get a full parse of the SKU — family (Crown Drip 8 × 10), gauge (29ga from the `9`), color (BK = Black), length (10 feet). If you get a generic response, the skill didn't load — check `claude plugin list`.

## Uninstall

```bash
claude plugin uninstall gms-intelligence
```

Or manually: `rm -rf ~/.claude/plugins/gms-intelligence/`.

## Requirements for the Python scripts

`skills/gms-pricing-engine/scripts/*.py` and `skills/gms-sku-decoder/scripts/*.py` are optional — the skills work without them. If Claude decides to run them for validation or bulk operations, it needs Python 3.10+. No third-party packages required; the scripts use only the Python standard library.

## Troubleshooting

**"Plugin not found" after install** — Claude Code caches the plugin list. Restart your Claude Code session.

**Skills don't trigger on natural language queries** — Check the `description` field in the skill's frontmatter. Skills load based on description match, not keywords. If your queries aren't activating the skill, either (a) your query isn't recognizably in the skill's domain or (b) the description is too narrow.

**Evals not running** — Eval HTMLs ship pre-rendered in `/evals/`. If you want to re-run them, you need Anthropic API access + a simple executor-grader harness (not included — this repo ships the skills, not the eval runner).
