# Herdr Omarchy-style macOS keymap

This repository had no Herdr-specific keymap before this folder was added.
Herdr has separate native GPUI and terminal CLI configurations. The daemon
`[keys]` map supplies shared prefix and direct bindings to both clients.

## Files

- `config-gpui.local.toml` contains native desktop shortcuts. Merge its
  remaining sections into `~/.config/herdr/config-gpui.local.toml`.
- `config.toml` contains CLI and shared daemon shortcuts. Merge it into
  `~/.config/herdr/config.toml`; preserve machine-specific settings.
- `ghostty.conf` defines the terminal `herdr` key table. Include it from the
  effective Ghostty config with `config-file = /absolute/path/to/dot-agents/herdr/ghostty.conf`.
- `zsh-integration.zsh` activates that table only while an interactive Herdr
  CLI attach is running, then deactivates it on exit or detach.

Add `source /absolute/path/to/dot-agents/herdr/zsh-integration.zsh` to
`~/.zshrc` and open a new shell. The wrapper checks `HERDR_ENV` to avoid
activating the outer key table from a Herdr-managed pane. `Cmd+Shift+H` is a
manual recovery toggle when Herdr starts without the wrapper.

## Shared Omarchy prefix map

The prefix is `Ctrl+Space`. The daemon keymap supplies Omarchy prefix actions to
both clients. The terminal CLI uses indexed tab shortcuts. GPUI lists
`Prefix+1…9`, but the installed desktop build did not switch tabs when tested;
use its verified `Cmd+Option+1…9` shortcuts instead.

| Herdr action | Shortcut |
| --- | --- |
| Reload / help / detach | `Prefix+Q` / `Prefix+?` / `Prefix+D` |
| New / rename / close tab | `Prefix+C` / `Prefix+R` / `Prefix+K` |
| Previous / next tab | `Prefix+P` / `Prefix+N` |
| Select tab 1–9 | CLI: `Prefix+1…9` or `Cmd+Option+1…9`; desktop: `Cmd+Option+1…9` |
| New / rename / close workspace | `Prefix+Shift+C` / `Prefix+Shift+R` / `Prefix+Shift+K` |
| Previous / next workspace | `Prefix+Shift+P` / `Prefix+Shift+N` |
| Split horizontal / vertical | `Prefix+H` / `Prefix+V` |
| Close / zoom / last pane | `Prefix+X` / `Prefix+Z` / `Prefix+;` |
| Rename pane | `Prefix+Shift+O` |
| Resize mode | `Prefix+Ctrl+Arrow` |

## Herdr GPUI desktop

The desktop app keeps the chosen macOS shortcuts and inherits the Omarchy
prefix/direct bindings while focused.

| Herdr action | Shortcut |
| --- | --- |
| Focus workspace 1–9 | `Cmd+1` … `Cmd+9` |
| Focus tab 1–9 | `Cmd+Option+1` … `Cmd+Option+9` |
| Focus pane | `Cmd+Arrow`, `Cmd+Option+Arrow`, or `Ctrl+Option+Arrow` |
| Swap pane | `Cmd+Shift+Arrow` |
| Previous / next tab | `Option+Left` / `Option+Right` (also `Cmd+Shift+[` / `Cmd+Shift+]`) |
| Move tab previous / next | `Option+Shift+Left` / `Option+Shift+Right` |
| Previous / next workspace | `Ctrl+Shift+Tab` / `Ctrl+Tab` (also `Option+Up` / `Option+Down`) |
| Next / previous pane | `Option+Tab` / `Option+Shift+Tab` |
| Split pane | `Cmd+D` / `Cmd+Shift+D`, or `Option+Shift+Enter` / `Option+Enter` |
| Close pane | `Cmd+W` / `Cmd+Q` or `Option+Escape` |
| Zoom pane | `Cmd+Option+F`, `Cmd+Shift+Enter`, or `Prefix+Z` |
| Full screen / find | `Cmd+F` or `Ctrl+Cmd+F` / `Cmd+Shift+F` |

The `pane_keys` entries release Herdr's default `Cmd+Left/Right` line movement
and `Option+Left/Right` word movement. This lets pane focus and tab navigation
claim those chords while the desktop app is active.

## Herdr terminal CLI in Ghostty

Ghostty routes the Omarchy and macOS chords to the terminal CLI only while the
shell wrapper has activated the `herdr` key table. Ghostty and macOS defaults
remain active outside that mode. While Herdr is active, `Option+Left/Right`
selects tabs and takes priority over Option-based word navigation.

macOS reserves `Cmd+Tab` and `Cmd+Shift+Tab` for app switching, so Herdr
workspace cycling uses `Ctrl+Tab` and `Ctrl+Shift+Tab`. Bare `Option+1…9` is not
used for tab selection on macOS because those keys can type symbols. Moving a
pane to another workspace and workspace 10 are not exposed by Herdr's indexed
key actions.
