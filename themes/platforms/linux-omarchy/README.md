# Linux / Omarchy adapter

The original integration was verified on Linux with Helium. These files are an
export for reuse, not an instruction to replace a working installation immediately.

## Palette placement

On a new machine, prepare the intended Omarchy themes first. To keep Omarchy's
active colors aligned with this repository, copy each shared palette to the
corresponding user theme's `colors.toml`: Wave to `kanagawa`, Lotus to
`kanagawa-lotus`, under `~/.config/omarchy/themes/`. Back up an existing file
before replacing it and retain the rest of that theme's assets. Reapply the
selected theme through Omarchy after changing its palette. Do not edit package
files under `/usr/share/omarchy` or the generated current-theme directory.

## 1. Register native hosts on a new machine

From the repository root, with Python 3.11+:

```sh
python3 themes/bridge/configure.py \
  --source "$HOME/.local/state/omarchy/current/theme/colors.toml" \
  --install-dir "${XDG_DATA_HOME:-$HOME/.local/share}/dot-agents-themes" \
  --native-host-dir "${XDG_CONFIG_HOME:-$HOME/.config}/net.imput.helium/NativeMessagingHosts"
```

This example is for Helium's observed Linux profile layout. Select the correct
registration directory if using another Chromium browser. Back up existing
registrations before migrating: the two host names are the same as the original
installation, so only one registration of each name should be active.

## 2. Palette export on theme changes

The bundled hook requires the `--install-dir` shown in step 1 and the same
`XDG_DATA_HOME` environment when the hook runs. If choosing another install
directory, copy the hook to a machine-local file and set its `root` to that exact
absolute directory before installing the local copy instead.

```sh
omarchy hook install theme-set themes/platforms/linux-omarchy/70-export-palette
```

The hook exports to the common local palette file consumed by both hosts. The
current source remains Omarchy's active theme, so Dark Reader follows its palette.
The browser switcher currently maps mode only to the two bundled browser themes.
If keeping the existing `70-helium-webpages` hook, migrate or replace it rather
than installing a duplicate exporter with a different runtime directory.

`scheduler.example.json` carries only reusable day/night preferences. Merge
selected fields in the plugin UI or its per-machine config. Keep location, runtime
boundary state and any existing overrides local. Palette generation does not
install or enable the Scheduler plugin.

## 3. Explicit themes and policy

**Helium and Chromium share `/etc/chromium/policies` on the observed system.**
Removing `BrowserThemeColor` unlocks theme selection for both. The helper preserves
every other key, including `BrowserColorScheme`; other browsers' policy files are
not edited by this helper. Omarchy recreates the color seed on each theme change,
so the root-owned helper runs after that write.

For a new installation, review the helper and make local backups of `color.json`,
the existing hook, and browser flags. Use administrator authentication in a visible
terminal to install the fixed-path helper:

```sh
sudo install -o root -g root -m 0755 \
  themes/platforms/linux-omarchy/remove-color-policy.py \
  /usr/local/bin/omarchy-helium-browser-theme-policy
sudo visudo -f /etc/sudoers.d/omarchy-helium-browser-theme
```

Use the `.sudoers.example` beside this guide, replacing `your_login` with the local
login. The `""` restricts the grant to **no arguments**. It is not a general shell
or file-write grant. The installed helper requires `/usr/bin/python` with Python
3.11+ on this Arch/Omarchy adapter; do not copy it unchanged to macOS.

```sh
omarchy hook install theme-set themes/platforms/linux-omarchy/60-helium-refresh
sudo -n /usr/local/bin/omarchy-helium-browser-theme-policy
```

## 4. Load browser extensions

Build the optional Dark Reader fork separately. Follow the
[first-install sequence](../../apps/chromium/README.md#first-installation-matters)
to load the switcher and both browser themes without losing the first theme.
After preparation, add the absolute local paths to the existing `--load-extension`
argument in Helium's user flags, preserving any other extension paths. Use one
comma-separated argument, and fully quit/reopen Helium to read it.

The legacy seed files under `chromium/` are generated for reverting to Omarchy's
older color-seed method. Wave maps to Omarchy's `kanagawa` directory; Lotus maps
to `kanagawa-lotus`. They do not provide exact frame/toolbar colors on their own.

## Rollback

Disable the switcher and native-connected Dark Reader if applicable, restore the
backed-up native registrations, flags and refresh/export hooks, and remove the
new helper/sudoers files through administrator authentication. Reapply the chosen
Omarchy theme to restore its generated color policy. Do not replace unrelated
browser policies or an existing full profile.

## Obsidian

Omarchy already renders `obsidian.css` and copies it to the **Omarchy** theme in
registered Obsidian vaults on system theme changes. No extra plugin or hook is
needed. To use the shared control/text roles, first back up an existing user
template and affected vault theme CSS, then install the generated override:

```sh
install -Dm644 themes/platforms/linux-omarchy/obsidian.css.tpl \
  "$HOME/.config/omarchy/themed/obsidian.css.tpl"
omarchy theme refresh
```

Select **Omarchy** in the intended vault's **Settings → Appearance → Themes**.
Set its base color scheme to **Adapt to system**. Omarchy's synchronization
copies the CSS but does not choose the theme in Obsidian for you. It updates
registered vaults, so review that list before refreshing. Backups, vault paths
and the vault's appearance/workspace files stay local.

The user template follows the current Omarchy palette for both scheme selectors;
it is not hardcoded to Kanagawa. To restore the stock styling, remove this user
override (or restore the prior one) and refresh the current theme again. Other
Obsidian themes and settings are not managed by this adapter. For portable
Wave/Lotus use, see the [Obsidian guide](../../apps/obsidian/README.md).
