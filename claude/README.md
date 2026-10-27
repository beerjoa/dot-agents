# Claude Code public settings

## Included settings

[`agents/`](./agents/) contains nine reviewed subagent definitions:

- `Explore.md` and `Plan.md` override the built-in Explore and Plan agents
  (same-name user files take precedence). Both are read-only and omit
  `CLAUDE.md` for focused, low-noise context gathering.
- `worker.md` plus six `sp-*` role workers (`sp-worker`, `sp-worker-pro`,
  `sp-code-review`, `sp-debug`, `sp-explorer`, `sp-spec-review`) for bounded
  implementation, review, debugging, exploration, and spec-compliance tasks.

Every agent pins `model: group/<id>`, selecting the matching
[Magpie routing group](../magpie/README.md) instead of inheriting the parent
session's route.

## Applying the settings

Start with the [new-machine setup and safe-merge guide](../docs/SETUP.md).
Copy selected files to `~/.claude/agents/` after reviewing them, then recreate
the referenced Magpie groups. Keep agent names unchanged: `Explore` and `Plan`
only override the built-ins under those exact names, and `model: group/<id>`
requires a group with the same id.

`settings.json` is intentionally excluded: it carries provider credentials,
local paths, hooks, and other machine state. Configure those locally.
