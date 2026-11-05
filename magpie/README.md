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
- `jev-auto` is the interactive main-session route. The other nine are retained
  for existing role-based installations. Claude Code's current pstack setup uses
  the separate groups below.

[`pstack-groups.public.json`](./pstack-groups.public.json) adds three independent
Jev-routed groups for [Claude Code with pstack](../claude/README.md):

- `pstack-explore`: Codex Luna and Antigravity Gemini Flash only.
- `pstack-code`: Sol, direct Grok, Claude Sonnet, and economical OpenCode Go coding models.
- `pstack-reasoning`: Sol as the technical default, Muse for prose, Grok/Sonnet
  for alternate analysis and synthesis, and selective Opus/Astra escalation.

All three advertise a 350k context and use automatic Jev effort, ordered fallback,
and affinity within a turn.
No member effort is pinned. Gemini Argon, Go Grok, and Antigravity Opus are excluded.
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
then rules. Group ids referenced by the Claude Code agents must match
(`group/jev-auto`, `group/worker`, and so on;
see [claude](../claude/README.md)).

## Publication boundary

The public subset excludes:

- Provider connections, API keys and key pools, OAuth credentials, account
  state, provider catalogs, picked/disabled-model lists, and fallback settings.
- Machine state: applied fingerprints, timestamps, affinity, quotas and usage
  history, client shapes, routing logs, caches, backups, and runtime data.

The original local configuration is preserved. Recheck future additions before
expanding this directory.
