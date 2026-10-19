# Paseo

Paseo 0.12.0 supports custom themes through the official `client.addTheme` plugin
API. This local plugin registers Wave and Lotus using eight palette colors.
It has no server entry, preparation commands, package dependencies, filesystem
operations or network calls. Paseo derives the remaining UI/terminal/diff colors;
this does not supply a separate syntax-highlighting theme or exact ANSI16 table.

## Install

1. From the repository root, regenerate with `python3 themes/scripts/generate.py`.
2. Review `paseo-plugin.json` and `index.client.ts`, then install the directory:

   ```sh
   paseo plugin add /absolute/path/to/dot-agents/themes/apps/paseo
   ```

3. If **Settings → Plugins → Enable plugins** is off, review the configured
   plugins before turning it on: the switch enables every individually enabled
   plugin on that host. This is required for the themes to appear.
4. In **Settings → Appearance → Theme**, select **Kanagawa Wave** or
   **Kanagawa Lotus**. If multiple hosts contribute these names, select the entry
   belonging to this plugin on the intended host.

Paseo runs client plugins as trusted code. The directory remains the source, so
keep it in place. After regenerating colors, run
`paseo plugin reload dot-agents-kanagawa`. Installation changes only plugin
registration; select a theme separately in each client.

## Appearance and rollback

Wave uses `#1f1f28` and Lotus uses `#f1e9d2`. Text, surfaces, borders, accent and
focus follow the shared palettes. Lotus secondary text uses normal foreground
for readable contrast on its raised surfaces.

In 0.12.0, **System** chooses built-in themes; a contributed theme is a separate,
single selection. This portable plugin provides manual Wave/Lotus choices.
For scheduled and manual Omarchy switching, install the separate
[Linux automatic adapter](../../platforms/linux-omarchy/README.md#paseo).

To undo, select the previous built-in theme (for example **System**), then run
`paseo plugin remove dot-agents-kanagawa`. Removal does not delete this directory.
If the global plugin switch was previously off and no other plugin needs it,
turn it off again in Settings → Plugins.
Do not commit daemon configuration, browser storage or private backups.

Linux desktop application is recorded in the verification guide. macOS, Windows
and mobile runtime application have not been checked here.

Source: [official 0.12.0 plugin API](https://github.com/getpaseo/paseo/blob/v0.12.0/public-docs/plugins/reference.md#contribute-a-theme).
