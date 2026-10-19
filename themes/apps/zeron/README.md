# Zeron

Zeron 0.2.113 supports custom themes through its built-in VS Code theme importer.
These files are color data only; no extension code or external package is loaded.

## Install on Linux, macOS or Windows

1. Generate the shared color files from the repository root:
   `python3 themes/scripts/generate.py`.
2. In Zeron, open **Settings → Appearance → Theme library → Add theme**.
3. Enter the absolute path to this folder's `package.json`, then choose **Analyze theme**.
4. Keep both variants selected and choose **Import selected**. An imported copy
   remains available if the repository is moved. Alternatively, **Link to source**
   keeps a connection to these files; source changes require an explicit **Reload**.
5. Set **Light theme → Kanagawa Lotus**, **Dark theme → Kanagawa Wave**, and
   **Color scheme → System**. Keep **Accent color → Theme default** and
   **Match wallpaper colors → off** to preserve the palette. **Glass → Theme default**
   uses the imported theme's opaque recommendation.

On Omarchy, System follows the OS light/dark appearance set by the theme scheduler.
No extra theme-set hook is needed for this fixed Wave/Lotus pair. This does not
automatically import arbitrary new Omarchy palettes.

## Colors and updates

The generator maps backgrounds, borders, text, controls, focus/accent, code tokens,
diffs and terminal ANSI16 from the shared TOML palettes. The shell and editor use
the exact palette background, including Lotus `#f1e9d2`; cards and inputs use
neighboring surface colors. The interaction accent uses the palette's blue.

Zeron compiles source tokens into its own semantic roles and may adjust foreground
colors to meet its contrast checks. Derived interaction states are controlled by
Zeron; source colors are not a guarantee of identical pixels for every state.
The shared Lotus ANSI16 palette is retained, including bright green (slot 10),
which Zeron flags as below 3:1 against the terminal background.

After regenerating, reload a linked source or remove and reimport this package's
snapshot, then check the light/dark selections. Keep the existing theme available
until the replacement has imported successfully.

Do not commit `~/.zeron/ui-settings.json`, `theme-library.json`, or backups: these
are device-local settings and the library includes absolute source paths. To undo,
select the built-in Zeron Light/Dark themes and remove this library entry.

Linux runtime application is recorded in the verification guide. macOS and Windows
use the same documented importer but have not been exercised here.

Sources: [official theme documentation](https://github.com/zeronsh/zeron/blob/v0.2.113/docs/theme-system.md)
and [importer implementation](https://github.com/zeronsh/zeron/blob/v0.2.113/crates/theme/src/vscode.rs).
