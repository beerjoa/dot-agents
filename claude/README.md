# Claude Code public settings

Claude Code uses [pstack](https://github.com/cursor/plugins/tree/main/harness/pstack)
with three dedicated [Magpie groups](../magpie/pstack-groups.public.json).
Superpowers is disabled in this Claude Code configuration.

## Included settings

- [`settings.public.json`](./settings.public.json) is a partial settings file:
  pstack's marketplace and plugin switch, model aliases, and group compaction settings.
- [`rules/pstack-models.md`](./rules/pstack-models.md) assigns every pstack role to
  a Claude Code alias. Magpie chooses the actual model and reasoning effort.
- [`agents/Explore.md`](./agents/Explore.md) and [`agents/Plan.md`](./agents/Plan.md)
  override the built-in agents and use the dedicated exploration and reasoning groups.
- The other seven definitions in [`agents/`](./agents/) are retained for existing
  installations. They are not required by pstack and should not be installed for
  the pstack-only setup. Pstack supplies its own `pstack:poteto-agent` delegate.

| Claude Code alias | Magpie group | Purpose |
| --- | --- | --- |
| `haiku` | `group/pstack-explore` | Codex Luna and Antigravity Gemini Flash only; no Sol or OpenCode Go |
| `sonnet` | `group/pstack-code` | Sol, direct Grok, Claude Sonnet, and economical Go coding models |
| `opus` | `group/pstack-reasoning` | Sol for ordinary technical judgment, Muse for prose, selective premium escalation |

These aliases select groups, not actual Claude model families. The main session's
model is a separate choice and is not changed by the public subset.

## Applying the settings

Start with the [new-machine setup and safe-merge guide](../docs/SETUP.md).
Configure Magpie and provider authentication locally, then recreate the three
reviewed groups from [`pstack-groups.public.json`](../magpie/pstack-groups.public.json)
with `magpie group add`, `magpie group set`, and `magpie group rule add`.
Group members must be exposed before adding rules. In particular,
`opencode-go/mimo-v2.6-flash` may need to be enabled in the provider's model list.
Preserve all unrelated groups and provider settings.

Install pstack in Claude Code:

```text
/plugin marketplace add cursor/plugins
/plugin install pstack@cursor-plugins
```

Merge selected keys from `settings.public.json` into `~/.claude/settings.json`.
Do not replace that file. Preserve credentials, gateway address, hooks, permissions,
other plugins, and the main model. Merge `CLAUDE_CODE_MODEL_CAPABILITIES` as a
semicolon-separated map keyed by model ID, preserving other model entries; do not
replace the whole existing string with the three public entries. When Magpie manages the tier mappings, set them
through its CLI too, so a later sync retains the choices:

```sh
magpie claude haiku group/pstack-explore
magpie claude sonnet group/pstack-code
magpie claude opus group/pstack-reasoning
```

Copy `rules/pstack-models.md` to `~/.claude/rules/pstack-models.md`, and merge the
selected Explore and Plan definitions into `~/.claude/agents/`. Keep their names
unchanged to override the built-ins. Start a new Claude Code session to load the
role rule and disabled Superpowers setting, then use `/pstack:poteto-mode` for a task.

If rerunning `/pstack:setup-pstack`, preserve the alias mapping and Jev policy.
The standard setup command offers fixed starting budgets; this configuration
instead lets Jev decide actual effort. `high` in the role file merely keeps
reasoning enabled in requests. It is not a fixed effort for each served model.

## Routing and cost policy

All three groups use `classifier: typesafe/jev-latest`, `effort: auto`,
`routing: order`, and `affinity: turn`. Intent rules choose the first model to try;
other members remain fallback candidates. No member has a fixed effort suffix
or `use-effort` override. Jev selects actual effort within the model's support;
`max` is not automatically selected by the documented auto-effort ladder.

Sol is the default technical reasoner. Muse handles supplied-evidence prose and
ordinary synthesis. Opus and Astra are reserved for exceptional risk or demonstrated
difficulty. Direct Grok is included; Go Grok, Gemini Argon, Antigravity Opus,
expensive Go alternatives, and promotional free endpoints are excluded.

Go candidates favor DeepSeek Flash, GLM Flash, MiMo Flash/Pro, and Muse.
Check the current [Go prices, allowances, and Extra Usage setting](https://opencode.ai/v2/docs/console/go/).
Extra Usage can charge Console credits after a Go allowance is exhausted, so a
quota-based fallback is not a spending cap. DeepSeek requires an allowed Global
region; Muse Contributor requires consent to endpoints that can train on requests.
This repository does not change those account settings or grant that consent.

Different aliases do not guarantee different model families. A strict cross-family
Arena judge requires checking the actual served routes, not just their alias names.
Mixed-group fallback can eventually select Muse even after a technical request's
preferred candidates fail. Do not treat that as a high-risk review passing; inspect
the route and report unavailable capability when appropriate.

## Local dependencies and verification

Grok uses a Grok Build sign-in. Its auth plugin must also find the executable to
renew credentials. For a mise installation, one local option is a symlink from
`~/.grok/bin/grok` to the installed binary; keep it current after upgrades, or use
`GROK_BIN_DIR` in Magpie's launch environment. Never copy account tokens into Git.

Check saved groups with `magpie group <id>` and plugin activation with
`claude plugin list`. Short gateway requests should verify both the requested
group and actual served model/effort in Magpie's routing records. A provider
connection test alone does not exercise the intent classifier.

Groups advertise a 350k context. Their effective Claude Code compaction window is
also 350k; Magpie may inherit that from the global setting instead of keeping
identical per-group entries. This does not increase a member model's native window;
long requests can narrow the eligible models or require earlier compaction.

The full local `settings.json`, provider credentials, plugin caches, account
records, routing histories, and backups remain private. The installation and
configuration format was checked with Claude Code 2.1.318 and pstack 0.15.36;
availability of individual model routes depends on the local accounts.
