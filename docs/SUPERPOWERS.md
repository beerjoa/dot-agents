# Superpowers compatibility

Reviewed on 2026-10-04 against upstream **v6.4.2**, commit
[`8ca22dba9a94f28898bbce59f2537ff4d87c747d`](https://github.com/obra/superpowers/tree/8ca22dba9a94f28898bbce59f2537ff4d87c747d).
The installed skill files used for the comparison matched that commit.

## Workflow changes

The [SDD skill](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/subagent-driven-development/SKILL.md)
now uses one independent task reviewer for both spec compliance and code
quality. `sp-code-review` / `sp_code_review` implements this gate, scoped fix
re-review, and the final whole-branch review. `sp-spec-review` /
`sp_spec_review` remains available for design/plan review and explicit spec audits.

The controller creates a plan-scoped ledger, task briefs, and review packages
using the installed skill's `scripts/sdd-workspace`, `scripts/task-brief`, and
`scripts/review-package`. Run these from the target project worktree via their
resolved installed paths, not a hard-coded plugin version or a scripts path
relative to the project. Child context is bounded to the brief and relevant
interfaces/constraints; full reports stay in that plan's scratch workspace.

Implementers report `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED`.
They create verified task-scoped commits through `git-commit-from-instructions`
in `agent-only` mode, as delegated by the controller. This supplies a real
BASE..HEAD range for the review-package script. The controller's independent
review gates completion and the next task; creating a commit does not pass the
gate. Review fixes use new scoped commits rather than rewriting existing history.

Fix loops are bounded to five rounds, with scoped re-review and recorded
adjudication at the cap. Deferred Minor findings and parked rulings travel to
the final branch review. The final review has one fix wave and one scoped
re-review. Reports retain all rulings and remaining risks; merging or publishing
still requires the user's authorization.

The [writing-plans skill](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/writing-plans/SKILL.md)
uses a Spec reference, Global Constraints, Review Focus, and task Interfaces.
Plans pin exact values, signatures, tests, and verification outcomes; they do
not transcribe implementation bodies already determined by those decisions.

## OpenCodex routing

The routing source is [`opencodex/config.public.json`](../opencodex/config.public.json).
Both OpenCode and Codex agent definitions use the `combo/sp-*` model IDs directly.

| Role | OpenCode model | Codex model | Effort |
| --- | --- | --- | --- |
| Explorer | `combo/sp-explorer` | `combo/sp-explorer` | high |
| Worker | `combo/sp-worker` | `combo/sp-worker` | max |
| Worker Pro | `combo/sp-worker-pro` | `combo/sp-worker-pro` | max |
| Spec review | `combo/sp-spec-review` | `combo/sp-spec-review` | max |
| Task / final review | `combo/sp-code-review` | `combo/sp-code-review` | max |
| Debug | `combo/sp-debug` | `combo/sp-debug` | high |

The callable OpenCode `git-committer` also uses `sp-worker`, and
`project-docs-sync` uses `sp-worker-pro` while retaining its high-effort setting.
Primary agent models are configured separately.

Set up OpenCodex and its provider connections locally, then apply the reviewed
combo definitions. A role or combo name does not guarantee model capability:
the existing Worker Pro combo's target order is not a capability ladder.
Check the actual supported route before escalating rounds 4–5 or selecting a
whole-branch reviewer. If routing cannot provide the required capability, report
that blocker rather than repeating the same route or inheriting the parent model.

Codex dispatch must also respect the actual spawn allowlist and V1/V2 tools.
Unsupported combo presets need a compatible runtime configuration; naming a role
does not bypass the harness's model restrictions. Specify model and reasoning
effort explicitly when the dispatch interface supports them.

## Verification boundary

JSON, YAML frontmatter, and TOML can be checked locally, including every role's
combo reference and the mirrored OpenCode start-build command. These checks do
not prove account access, live failover, or a complete agent execution. Verify
those separately in the destination runtime.
