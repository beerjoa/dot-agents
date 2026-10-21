# Orca ADE

These Warp-format YAML files target Orca's official **Import from YAML** terminal
theme importer. They provide the shared background, foreground, cursor and ANSI16
colors without installing a plugin or changing a shell/font/keybinding.
Wave uses `#1f1f28`; the customized Lotus uses `#f1e9d2`.

## Install and follow the system

1. Regenerate from the repository root with `python3 themes/scripts/generate.py`.
2. Back up the current Orca settings locally. In 1.4.230, open
   **Settings → Appearance → Terminal** (or search settings for `terminal theme`).
   Use **Import from YAML → Choose Folder** to select this directory, then import
   both variants. Some documentation/versions place these controls under Terminal.
3. Set the dark terminal theme to **Kanagawa Wave**, enable a separate light
   theme, and set that to **Kanagawa Lotus**.
4. Keep **Settings → Appearance → Theme** on **System**. Orca selects the dark
   or light terminal variant from its effective app mode. Omarchy's existing
   system-mode propagation also covers Theme Scheduler; no additional hook is
   needed for this pair.

Imports are snapshots. After changing the shared palettes, regenerate and
reimport the YAML files. Review existing color overrides: they can take priority
over imported theme colors. Do not replace a full profile to install colors.

## Boundaries and rollback

Installed Orca 1.4.230 exposes System/Dark/Light app modes and a sidebar tint,
but no custom full-app palette importer. These files theme terminals, not the
app frame, buttons or Monaco syntax. They do not patch package files or inject
styles. The YAML importer reads background, foreground, cursor and ANSI colors;
selection and other derived terminal colors remain Orca defaults.

To undo, select the previous dark/light terminal themes and remove the imported
entries if desired. Restore only the prior appearance choices or relevant color
overrides from a private backup; preserve other settings and live sessions.
Keep profiles, workspace/session data, authentication and backups outside Git.

Source: [official terminal import documentation](https://www.onorca.dev/docs/terminal).
