# Magpie public settings

Magpie routes every agent's model through providers and routing groups.

## Included settings

[`providers.public.json`](./providers.public.json) contains a reviewed subset of
the source user's routing configuration, not upstream factory defaults:

- Ten routing groups: `jev-auto` plus nine subagent roles (`worker`,
  `sp-worker`, `sp-worker-pro`, `sp-code-review`, `sp-debug`, `sp-explorer`,
  `sp-spec-review`, `explore`, `plan`).
- For each group: member models in order, `routing`/`stays` behavior, routing
  rules (token thresholds and intent matchers), the `typesafe/jev-latest`
  classifier, and reasoning effort.
- `jev-auto` is the interactive main-session route. The other nine preserve
  separate Claude Code, Superpowers `sp-*`, and general worker entry points.
  Keep these group IDs even where their current routing definitions overlap.
  Pstack uses the separate groups below.

[`pstack-groups.public.json`](./pstack-groups.public.json) adds three independent
Jev-routed groups for [Claude Code with pstack](../claude/README.md):

- `pstack-explore`: Codex Luna for bounded lookup, Go Gemini Argon for broad
  evidence gathering with direct Grok as the next alternative, and Codex Terra
  at 250k tokens or more with Argon as its next alternative.
- `pstack-code`: Sol, Claude Sonnet/Haiku, direct Grok, Mistral DeepSeek Flash,
  and complementary Go/Mistral GLM and MiMo coding routes.
- `pstack-reasoning`: Sol for code analysis and diagnosis, Sonnet for ordinary
  design, planning and correctness review, Muse for prose, Grok for independent
  analysis, Argon for factual checking, and selective Opus/Astra escalation.

All three advertise a 350k context and use automatic Jev effort, ordered fallback,
and affinity within a turn.
No member effort is pinned. Antigravity, OpenCode Zen, Go Grok, and MiniMax
M3.1 Flash are excluded from the exported groups. Argon also handles broad
read-only discovery in `explore` and `sp-explorer`, with Grok as an alternative.

Sonnet handles standard spec/plan reviews, ordinary planning, and thorough code
review. Sol remains the primary for high-risk code review, diagnosis, long-context
work, and implementation. Opus remains an exceptional escalation. `jev-auto`
keeps Muse first for longer prose and summaries, with Haiku as an alternative;
short text transformations still use Mistral Large.

All DeepSeek Flash group members and rules use Mistral's dated DeepSeek Flash;
no group references the Go DeepSeek route. Go GLM Flash uses Mistral GLM Flash
and GLM-5.3; Mistral GLM-5.3 terminal-workflow rules use Go GLM Flash as their
next fallback. These ordered alternatives provide
coverage when a provider has no ready quota or fails; they do not configure a
proactive low-quota threshold. GLM Flash is a lower-capability alternative to
GLM-5.3, not the same model.

The configuration files are independent partial subsets; merge selected groups
by ID, never replace the local provider configuration with either file.

Model and provider names in routing targets are included intentionally.
Provider connections and authentication are excluded.

## Applying the settings

Start with the [new-machine setup and safe-merge guide](../docs/SETUP.md).
Magpie has no JSON import for groups: review the public file and recreate
selected groups with the CLI (`magpie group add`, `magpie group set`,
`magpie group rule add`; see `magpie group --help` and
`magpie group rule --help`).

This file is a **partial configuration**, not a replacement for
`~/.config/magpie/providers.json`. Set up Magpie and its providers first, then
recreate only the groups you need. Preserve your provider and account
configuration. Verify that the target models are available to your own
accounts; the public subset does not configure those connections or guarantee
model availability.

Recreate order matters: rules reference member models, so add members first,
then rules. A rule's `more` list contains its ordered alternatives; recreate it
with `use=<primary>,<fallback>,...` in `magpie group rule add`. Group ids referenced
by the Claude Code agents must match (`group/jev-auto`, `group/worker`, and so on;
see [claude](../claude/README.md)).

For the Go $10 plan, check current [model prices and allowances](https://opencode.ai/docs/console/go/).
Estimated request counts are workload examples, not fixed request quotas.
DeepSeek Flash runs through Mistral; Go's remaining allowance is directed toward
Argon discovery and Muse prose while retaining existing GLM/MiMo routes.
These Go priorities are temporary: before ending a Go subscription, replace its
explicit primary routes (for example, Argon discovery with Grok and Muse prose
with Claude) and remove unavailable members and rule alternatives. Provider
selection remains local: deselect Go DeepSeek Flash and MiniMax M3.1 Flash and
leave unused Zen routes off when following this configuration.

To exclude Go from automatically discovered groups while retaining it in all
explicitly configured groups:

```sh
magpie group auto skip opencode-go
```

This replaces the auto-group provider skip list; preserve any additional skips
already configured on the target machine. Account limits and Extra Usage settings
remain local and are not changed by these public files.

## Publication boundary

The public subset excludes:

- Provider connections, API keys and key pools, OAuth credentials, account
  state, provider catalogs, picked/disabled-model lists, and provider-level fallback settings.
- Machine state: applied fingerprints, timestamps, affinity, quotas and usage
  history, client shapes, routing logs, caches, backups, and runtime data.

The original local configuration is preserved. Recheck future additions before
expanding this directory.
