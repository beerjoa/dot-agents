<div align="center">
  <h1>dot-agents</h1>
  <p>A public collection of reusable settings, prompts, and tools for personal vibe coding workflows.</p>
  <p>English | <a href="./README.ko.md">한국어</a></p>
</div>

## [New machine setup and safe merging](./docs/SETUP.md)

Agents applying these settings should start with this guide: it covers backups,
selective merging, provider login, environment variables, per-machine advisor
consent, native OpenCode free models, and verification before handoff.

## [OpenCode config](./opencode/opencode.json)

The sanitized `opencode.json` contains:

- **Plugins & MCP** — plugin and MCP server settings
- **Providers** — `commandcode` and `opencodex` configurations
- **Models** — model limits and runtime preferences
- **Credentials** — environment-variable references for sensitive values

## [Codex config](./codex/config.toml)

The `codex/` directory contains a public subset of user-level Codex settings:
`config.toml`, `keybindings.json`, `AGENTS.md`, its `RTK.md` reference,
the [custom agents](./codex/agents/), and the [Blastoise pet](./codex/pets/blastoise/).
The custom agents use local `combo/...` model selectors; choose available models
when using them on another machine. See the [plugin guide](./codex/PLUGINS.md)
for the selected installation list.
The [Superpowers compatibility notes](./docs/SUPERPOWERS.md) record the reviewed
workflow version and OpenCodex combo mapping for Codex and OpenCode agents.
The [prompts](./codex/prompts/) cover develop integration, planning, and task execution.
Use [start-build](./codex/prompts/start-build.md) for subagent implementation or
[start-build-native](./codex/prompts/start-build-native.md) to implement in the current session with one final branch review.
Planning and execution require Superpowers; execution uses `git-commit-from-instructions` and the custom agents for delegated implementation or final review.
Copy selected files to `~/.codex/` after reviewing them for your environment.
The original `config.toml` also contains machine paths, project trust entries,
provider and MCP connections, and authorization settings; those are omitted.

## [OpenCodex settings](./opencodex/README.md)

The `opencodex/` directory contains reviewed public
[OpenCodex](https://github.com/lidge-jun/opencodex) preferences, model selections,
and nine `jev` combos (`default`, `explorer`, `worker`, and the six `sp-*` roles). Its
[`config.public.json`](./opencodex/config.public.json) is a partial configuration:
apply selected fields to an existing configuration after reviewing them.
Provider connections, authentication modes, credentials, account state, and
runtime data are excluded.

## [Magpie routing](./magpie/README.md)

The `magpie/` directory contains a reviewed public subset,
[`providers.public.json`](./magpie/providers.public.json): ten routing groups
(`jev-auto` plus nine subagent roles) with member models, routing behavior,
token/intent rules, and the Jev classifier. Provider connections, credentials,
account state, and runtime data are excluded. Magpie has no JSON import, so
review the file and recreate selected groups with `magpie group add/set/rule`.

## [Claude Code agents](./claude/README.md)

The `claude/agents/` directory contains nine subagent definitions wired to the
Magpie groups via `model: group/<id>`, including `Explore` and `Plan` overrides
of the built-in agents. Copy selected files to `~/.claude/agents/` after
reviewing them. `settings.json` is excluded: it carries provider credentials
and machine state.

## [Shared themes](./themes/README.md)

`themes/` holds the Kanagawa Wave dark and customized Lotus light palettes,
generated browser/Dark Reader/Codex/terminal color files, the browser switcher,
and the pinned Dark Reader/native bridge source. Linux/Omarchy integration is
separated from macOS reuse guidance. Personal profiles, site lists and machine
registrations are excluded. Generate color files with Python 3.11+; installation
is explicit and does not happen when cloning this repository.
