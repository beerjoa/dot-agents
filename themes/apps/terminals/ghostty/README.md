# Ghostty: Wave / Lotus

The existing generated `kanagawa-wave.conf` and `kanagawa-lotus.conf` contain
colors only: background, foreground, cursor, selection and ANSI palette.
Reuse these files on each computer; do not copy a complete Ghostty configuration
or another computer's accounts, shell commands, fonts or keybindings.

## Install the two theme files

From an up-to-date repository checkout, run these commands at the repository root
on macOS or Linux. Back up these destination theme files first if you customized
an earlier copy.

```sh
git pull --ff-only
ghostty_config_dir="${XDG_CONFIG_HOME:-$HOME/.config}/ghostty"
mkdir -p "$ghostty_config_dir/themes"
cp themes/apps/terminals/ghostty/kanagawa-lotus.conf \
  "$ghostty_config_dir/themes/dot-agents-kanagawa-lotus"
cp themes/apps/terminals/ghostty/kanagawa-wave.conf \
  "$ghostty_config_dir/themes/dot-agents-kanagawa-wave"
```

The installed names deliberately have a `dot-agents-` prefix so they do not
collide with Ghostty's bundled themes. Install both into the XDG theme directory
even when your main configuration uses the macOS-specific location.

## Merge the theme selection

Back up your existing configuration, then replace its existing `theme` setting
with this line, or add it if none exists. Keep other configuration entries.

```ini
theme = light:dot-agents-kanagawa-lotus,dark:dot-agents-kanagawa-wave
```

Ghostty selects the theme from the system appearance. This uses Ghostty's native
support; no browser extension, Native Messaging Host, LaunchAgent or Omarchy
Scheduler is required.

Current Ghostty uses `config.ghostty`; older versions also use `config`. It loads
these paths in order, with later conflicting values taking precedence:

1. `${XDG_CONFIG_HOME:-$HOME/.config}/ghostty/config.ghostty`
2. `${XDG_CONFIG_HOME:-$HOME/.config}/ghostty/config`
3. On macOS, `~/Library/Application Support/com.mitchellh.ghostty/config.ghostty`
4. On macOS, `~/Library/Application Support/com.mitchellh.ghostty/config`

Edit the file that controls your effective theme rather than creating duplicate
theme selections across locations. Follow any existing `config-file` includes
when checking overrides. Never replace a populated configuration with a sample.

Explicit `background`, `foreground`, `palette`, cursor or selection colors in
your own configuration override theme values. Preserve intentional overrides;
if exact Wave/Lotus colors are wanted, review only the conflicting color entries.
Fonts, keybindings, shell commands and account settings need no changes.

Keep the existing titlebar style. With separate light/dark themes, `window-theme`
in `auto` behaves as `system`; an explicit extra `window-theme` line is not needed.
On macOS the default transparent titlebar follows the terminal background.

## Validate and reload

Use the installed Ghostty executable:

```sh
ghostty +validate-config
```

On macOS, if `ghostty` is not in `PATH`, use
`/Applications/Ghostty.app/Contents/MacOS/ghostty +validate-config` instead.

Reload the configuration in Ghostty. On the verified macOS 1.3.1 installation,
the default shortcut is **Command+Shift+comma** (`reload_config`). Use your own
binding if customized; on other versions/platforms consult the app's bindings.

Check the terminal background and selection/cursor colors, then switch system
appearance to test both palettes. Lotus background is `#f1e9d2`; Wave background
is `#1f1f28`. Restore your original system appearance setting after checking.
Successful CLI validation confirms configuration parsing, not the appearance of
an already-running terminal window.

## Update or undo

After a repository update, repeat the two theme-file copies and reload Ghostty.
Regenerate repository color files only if editing the shared palettes; see
[`../../../README.md`](../../../README.md). The local installed copies do not
update merely because the repository was pulled.

To undo, restore the previous `theme` setting (or remove the added line when
there was none) and reload Ghostty. The two installed theme files can remain
unused. Do not overwrite unrelated settings while restoring.

## Verification boundary

On macOS with Ghostty 1.3.1, both files passed native configuration validation;
the effective configuration resolved Lotus colors, and fonts/keybindings were
unchanged. The user confirmed that reloading changed the running app's theme.
Live light/dark round-trip, restart persistence and Linux runtime application
were not separately verified. No private configuration or validation dump is
included in this repository.

References: [configuration locations](https://ghostty.org/docs/config),
[theme and window settings](https://ghostty.org/docs/config/reference),
[custom themes and automatic switching](https://ghostty.org/docs/features/theme).
