# Superpowers compatibility

Reviewed on 2026-10-14 against upstream **v7.0.0**, commit
[`bb92a77741419a4ab5f06e711a283343f1ada0c3`](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3).
The installed skill files used for the comparison matched that commit.

## Workflow changes

The [SDD skill](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/subagent-driven-development/SKILL.md)
now uses one independent task reviewer for both spec compliance and code
quality. `sp-code-review` / `sp_code_review` implements this gate, scoped fix
re-review, and the final whole-branch review. `sp-spec-review` /
`sp_spec_review` remains available for plan review and explicit spec audits.

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

The [writing-plans skill](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/writing-plans/SKILL.md)
uses a Spec reference, Global Constraints, Review Focus, and task Interfaces.
Plans pin exact values, signatures, tests, and verification outcomes; they do
not transcribe implementation bodies already determined by those decisions.

## Brainstorming

The v7.0.0 [brainstorming skill](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/brainstorming/SKILL.md)
draws out intent with open questions and playback, then sizes the work. A
quick task or small change agreed in chat gets no spec; only a project gets a
written design. The spec-document reviewer is replaced by a builder check: a
fresh subagent reads the design as its builder and lists remaining questions,
which `sp-spec` sorts into answered, its own marked calls, and one round of
user questions. `sp-spec` dispatches that check to OpenCode's `general`
subagent; `sp-spec-review` is no longer part of design review.

## Native execution

Use [`start-build-native`](../codex/prompts/start-build-native.md) for the
v7.0.0 [executing-plans skill](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/executing-plans/SKILL.md).
The current session implements tasks sequentially, verifies their planned
outcomes, and commits its own scoped changes. Native execution shares SDD's
plan workspace and ledger; `executing-plans/scripts/task-start` creates the
brief and returns BASE, and `scripts/task-done` runs the task's verification
command and records completion only on success.

There is one fresh whole-branch reviewer at the end, with explicit model and
effort, the plan/spec, Review Focus, and recorded rulings. If no subagent tool
exists, the executor performs a separate self-review and reports that limitation.
The executor handles Critical/Important findings in one fix pass with
RED-to-GREEN evidence and a passing full suite. Native mode does not dispatch
a fix worker or re-review. Deferred Minor findings and all rulings, including
the cost if wrong, reach the final report.

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
