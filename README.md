# design-to-code-reuse

A Comate / Claude Code skill that enforces **component reuse first** when implementing UI designs (Pencil / Figma / screenshots) into a mature frontend codebase, and learns from your corrections so reuse accuracy improves over time.

## Why

Mature projects already have a battle-tested component library and design tokens. Naive design-to-code tools tend to write fresh `<div>` soup that ignores those assets. This skill makes the AI:

1. **Inspect the repo first** — build / reuse a component inventory.
2. **Match before writing** — for every design module, decide `REUSE` / `EXTEND` / `NEW` and show you a table.
3. **Wait for confirmation** — never write code before you OK the matching plan.
4. **Learn from corrections** — when you change a decision or swap an import, the rule is appended to a project-level mapping file so the next match nails it.

## Install

### Comate (personal scope)

```bash
git clone git@github.com:xxylon111-sys/design-to-code-reuse.git ~/.comate/skills/design-to-code-reuse
```

### Claude Code

```bash
git clone git@github.com:xxylon111-sys/design-to-code-reuse.git ~/.claude/skills/design-to-code-reuse
```

### Codex CLI

```bash
git clone git@github.com:xxylon111-sys/design-to-code-reuse.git ~/.codex/skills/design-to-code-reuse
```

Restart your CLI / IDE after cloning.

## How to trigger

The skill auto-triggers when you, while in a project that has a component library, say things like:

- "按这个设计稿做一个页面" / "还原这个设计"
- "把 Pencil / Figma / 这张图写成代码"
- "implement this design into the project"

You can also force it: `用 design-to-code-reuse 实现这个设计`.

## Workflow (6 steps)

1. **First-time setup** — asks you to pick `on-demand` (recommended) or `full-scan` indexing strategy.
2. **Parse the design** — image / Pencil / Figma → module tree with visual features.
3. **Match against components** — checks `mapping rules → inventory → Explore subagent → cross-project heuristics → NEW`.
4. **Confirm** — shows a table; **does not write code until you approve**.
5. **Generate code** — `REUSE` imports existing; `EXTEND` patches a variant; `NEW` writes from scratch using design tokens.
6. **Learn** — your corrections become persistent rules in `<repo>/.comate/component-mapping.md`.

## Project-level artifacts

After first use, two files appear in your repo (commit them so the team shares the knowledge):

```
<repo>/.comate/
├── component-inventory.md   # what components exist
└── component-mapping.md     # design feature → component rules (learned from your edits)
```

## Layout

```
design-to-code-reuse/
├── SKILL.md                       # main workflow
├── references/
│   ├── inventory-schema.md
│   ├── mapping-schema.md
│   ├── heuristics.md              # cross-project rules
│   └── input-handlers.md
├── scripts/
│   ├── scan_components.py         # scans src/components, exports props
│   └── match_report.py            # renders the confirmation table
└── assets/
```

## Contributing

Issues and PRs welcome — especially additions to `references/heuristics.md` once you've seen a `design feature → component type` rule hold across multiple projects.

## License

MIT
