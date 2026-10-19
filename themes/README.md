# Shared themes

Kanagawa Wave (dark) and the locally customized Kanagawa Lotus (light), extracted
from the working Linux desktop integration. App color files are usable separately
from Omarchy and from the browser automation.

| Palette | Background | Text |
| --- | --- | --- |
| Wave | `#1f1f28` | `#dcd7ba` |
| Lotus | `#f1e9d2` | `#545464` |

## Layout

- [`palettes/`](palettes/): the color source; edit these TOML files first.
- [`apps/chromium/`](apps/chromium/): explicit browser themes and their switcher.
- [`apps/darkreader/`](apps/darkreader/): color snippet, pinned source patch and public identity.
- [`apps/codex/appearance.toml`](apps/codex/appearance.toml): desktop appearance tables only.
- [`apps/terminals/`](apps/terminals/): Ghostty, Kitty and Alacritty color snippets.
- [`apps/neovim/`](apps/neovim/): LazyVim/kanagawa.nvim snippets.
- [`apps/obsidian/`](apps/obsidian/): portable Wave/Lotus theme and shared CSS source.
- [`apps/zeron/`](apps/zeron/): Wave/Lotus package for Zeron's built-in theme importer.
- [`apps/paseo/`](apps/paseo/): local color plugin for Paseo's official theme API.
- [`bridge/`](bridge/): native host source and machine-local registration preparation.
- [`platforms/`](platforms/): OS-specific application, hooks and policy handling.
- [`assets/`](assets/): image inventory, kept separate from color configuration.
- [`verification/`](verification/): what was actually verified and what remains platform-specific.
- [`PROVENANCE.md`](PROVENANCE.md): original sources and third-party license.

## Generate or check colors

Python 3.11 or newer is required; no Python packages are needed.

```sh
python3 themes/scripts/generate.py
python3 themes/scripts/generate.py --check
```

Run from the repository root. The first command updates only this tree's generated
color files; it does not install or activate anything. `--output <directory>` can
render an alternate tree. Changing a palette does not hot-reload an installed
browser theme: regenerate, update the selected app files, and reload them through
that app. Review changes to extension versions when distributing an update.

Generated browser manifests preserve the existing public keys/extension IDs.
No private signing keys are required for unpacked local use.

## Apply selected apps

- Browser appearance: load one generated theme folder in Developer mode, after
  checking browser policy. The frame and toolbar use the exact palette background,
  not a color-generation seed. See the Chromium guide for automatic switching.
- Web pages: enter the Dark Reader snippet's background/text colors in the
  extension's color controls, or use the separately built native-connected fork.
- Codex: merge the `desktop` appearance tables into the existing user config.
  Do not replace the complete config or create duplicate TOML tables. The snippet
  reflects the observed desktop schema; check it against the target app version.
- Terminals: include or import the desired color file using that terminal's
  configuration. Preserve existing fonts, shell commands, keybindings and paths.
- Neovim: use the snippets only if the existing setup uses LazyVim and kanagawa.nvim.
- Obsidian: install the two portable theme files in the intended vault and choose
  its base scheme, or use the existing Omarchy theme with the Linux user template.
- Zeron: import its theme package, select the light/dark variants, and follow System.
- Paseo: install the local color plugin and select Wave or Lotus in Appearance.
  On Omarchy, the optional Linux adapter adds an automatic current-palette theme.

## Platform status

| Area | Linux/Omarchy | macOS | Windows |
| --- | --- | --- | --- |
| Palette and app color data | Extracted/validated | Reusable data; app application not tested | Reusable data; app application not tested |
| Browser/native automatic switching | Previously verified in Helium | Registration guide; automatic mode source not implemented | Native host not supported by this POSIX implementation |
| Policy removal and Scheduler hooks | Linux-only adapter | Not installed or ported | Not installed or ported |

Read [Linux/Omarchy](platforms/linux-omarchy/README.md) or
[macOS](platforms/macos/README.md) before installing integration code.
No existing machine configuration is changed by checking out or generating this tree.

Personal site exceptions, browser profiles, Codex provider/trust/auth settings,
generated native registrations, copied initial user settings, build dependencies,
and private backups belong outside the repository. `local/` is ignored for any
temporary per-machine work under this directory.
