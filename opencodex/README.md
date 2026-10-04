# OpenCodex public settings

[OpenCodex](https://github.com/lidge-jun/opencodex) is an MIT-licensed provider
proxy that connects Codex and Claude Code to multiple LLM providers.

## Included settings

[`config.public.json`](./config.public.json) contains a reviewed subset of the
source user's settings, not upstream factory defaults:

- Listener port, retained app-state memory budget, legacy usage-reader limit,
  model alias and fast service-tier preferences, WebSocket and proxy auto-start
  preferences, and multi-agent mode.
- Featured subagent, injection, web search, and vision model selections.
- The six `sp-*` failover combos, including target order, weights, reasoning
  effort, and sticky limits. These correspond to the `combo/...` selectors used
  by the [Codex agents](../codex/agents/) and the [OpenCode agents](../opencode/agents/).

Model and provider names in routing targets are included intentionally. Provider
connections and authentication modes are excluded.

## Applying the settings

This file is a **partial configuration**, not a replacement for
`~/.opencodex/config.json`. Set up OpenCodex and its providers first, then review
and apply selected top-level fields to your existing configuration. Preserve
the other fields, including your provider and account configuration. Merge
selected entries within `combos` to preserve any unrelated local combos. If you
use `OPENCODEX_HOME`, the active `config.json` is under that directory instead.

Configure the `openai`, `devin`, `opencode-go`, and `google-antigravity` providers
locally before using the corresponding combos. Verify that the target models
and reasoning efforts are available to your own accounts. The public subset
does not configure those connections or guarantee model availability.

The port must be available on the destination machine. Review auto-start and
multi-agent mode against your installed version before applying them. Follow
the upstream [configuration reference](https://opencodex.me/reference/configuration/)
for supported editing methods. This repository does not change your running
OpenCodex installation.

## Publication boundary

The public subset excludes:

- Provider connections and authentication modes, API keys and key pools, OAuth
  credentials, service/admin tokens, account IDs, emails, account namespaces,
  and account switching/pooling settings.
- Client integration settings and snapshots, machine paths, applied
  fingerprints, timestamps, and configuration migration/provenance records.
- Generated model catalogs, disabled-model lists, provider context caps, and
  interception settings.
- Request/response state, routing and spend records, usage logs, databases,
  replay data, caches, runtime state, certificates, private keys, and backups.

The repository's ignore rules allow only the reviewed files in this directory.
Recheck future additions before expanding that allowlist. The original local
configuration is preserved.
