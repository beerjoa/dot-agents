<div align="center">
  <h1>dot-agents</h1>
  <p>A public collection of reusable settings, prompts, and tools for personal vibe coding workflows.</p>
  <p>English | <a href="./README.ko.md">한국어</a></p>
</div>

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
and six `sp-*` failover combos. Its
[`config.public.json`](./opencodex/config.public.json) is a partial configuration:
apply selected fields to an existing configuration after reviewing them.
Provider connections, authentication modes, credentials, account state, and
runtime data are excluded.
