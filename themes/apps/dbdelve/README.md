# DBDelve Kanagawa themes

Native DBDelve themes matching the locally installed Zed **Dot Agents Kanagawa**
family, generated from this repository's shared palettes:

- [Wave](kanagawa-wave.json): dark, background `#1f1f28`, text `#dcd7ba`.
- [Lotus](kanagawa-lotus.json): light, customized background `#f1e9d2`, text `#545464`.
- [Wave Glass](kanagawa-wave-glass.json): dark with DBDelve's native glass effect.
- [Lotus Glass](kanagawa-lotus-glass.json): light with DBDelve's native glass effect.

Wave and Lotus are opaque (`glass: false`). The Glass variants use the same
source colors with `glass: true`; DBDelve applies its own translucent surfaces
and desktop blur when loading them, so their visible backgrounds depend on what
is behind the window. Editor, panel, chrome, hover, text, cursor,
accent and SQL syntax colors follow the Zed theme's roles. Wave retains Zed's
cream accent `#dcd7ba`; Lotus uses blue `#4d699b`. Chrome uses Zed's title-bar
color so the active editor tab remains distinguishable. Selection uses the
palette blue at approximately 38% opacity (`#7e9cd860` for Wave, `#4d699b60` for
Lotus), making selected text and result rows distinct from the neutral hover
surfaces. Edited-cell washes retain the importer's approximately 14% opacity.
`on_accent` uses the palette background.

## Install

Copy the desired JSON files into DBDelve's `themes` data folder. The commands
below copy all four variants. Back up any existing files with the same names
before replacing them. Run from the repository root.

Windows (PowerShell):

```powershell
$themeDir = Join-Path $env:APPDATA 'dbdelve\themes'
New-Item -ItemType Directory -Force -Path $themeDir | Out-Null
Copy-Item themes/apps/dbdelve/kanagawa-*.json $themeDir
```

Linux:

```sh
theme_dir="${XDG_DATA_HOME:-$HOME/.local/share}/dbdelve/themes"
mkdir -p "$theme_dir"
cp themes/apps/dbdelve/kanagawa-*.json "$theme_dir/"
```

macOS:

```sh
theme_dir="$HOME/Library/Application Support/dbdelve/themes"
mkdir -p "$theme_dir"
cp themes/apps/dbdelve/kanagawa-*.json "$theme_dir/"
```

Restart DBDelve: it reads user theme files at startup. Under **Settings →
Appearance**, choose **Dot Agents Kanagawa Wave** or **Dot Agents Kanagawa Lotus**,
including their **Glass** variants.
For automatic switching, enable **Match system appearance**, then set **Light
theme** to Lotus or Lotus Glass and **Dark theme** to Wave or Wave Glass. This
uses DBDelve's own system-mode support and needs no external hook.

To update, regenerate, copy the selected files again and restart DBDelve. To
remove them, select a built-in theme for each configured appearance, delete the
copied files and restart.

## Maintenance and verification

Edit `themes/palettes/*.toml` or the DBDelve mapping in
`themes/scripts/generate.py`, then run:

```sh
python3 themes/scripts/generate.py
python3 themes/scripts/generate.py --check
```

The native format and startup loading were checked against the
[official theme guide](https://github.com/ShayanAbbas1/dbdelve/blob/364fc969366750d8c4c0754d3369e92d1c47cfec/docs/themes.md)
and its matching loader source. Static validation checks generated-file
consistency, all 27 native color keys, hex formats, and color correspondence
with the installed Zed theme. Existing generator regression tests also pass.
Runtime selection, visual appearance and system switching in DBDelve have not
been verified. These files are not installed or activated by the generator.
