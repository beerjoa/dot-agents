# Obsidian

`theme.css.tpl` is the shared source for Obsidian color roles. The generator
produces `theme.css` with Wave under `.theme-dark` and Lotus under `.theme-light`,
and the Linux adapter's equivalent `obsidian.css.tpl` with Omarchy placeholders.
Edit the source template and shared palettes, then regenerate from the repo root.

The theme colors the editor, sidebars, tabs, title bar, buttons, inputs, focus,
icons, links, headings, selection, code, tags and graph. It does not install
plugins or change fonts, layout, notes, account settings or keyboard shortcuts.
Use a modern Obsidian installer/webview supporting CSS `color-mix()`; the theme
declares Obsidian 1.5.0 or newer.

Small semantic labels and code tokens mix their palette hue with normal text
to retain at least 4.5:1 contrast on the editor and code/sidebar surfaces in
both bundled palettes. Graph accents keep their original palette colors.

## Portable installation: macOS and other PCs

1. Back up the vault's current appearance configuration and any existing theme
   folder with the same name.
2. Create `.obsidian/themes/Dot Agents Kanagawa/` in the intended vault.
3. Copy **only** this folder's `manifest.json` and generated `theme.css` there.
4. In Obsidian **Settings → Appearance**, select **Dot Agents Kanagawa** and set
   the base color scheme to **Adapt to system** for system-driven dark/light.
   Manual **Dark** uses Wave; manual **Light** uses Lotus.

The folder name must match the manifest's `name`. Obsidian settings are per
vault; repeat intentionally for other vaults. A theme supplies colors, not an OS
appearance scheduler. System adaptation depends on the target platform signaling
its color scheme to Obsidian. macOS/Windows runtime application has not been
verified in this repository.

## Omarchy installation

Use the existing **Omarchy** theme in the vault, with the user template described
in the [Linux guide](../../platforms/linux-omarchy/README.md#obsidian). Omarchy
already regenerates and synchronizes that theme when the system theme changes.
The portable theme above stays fixed to Wave/Lotus and is a separate manual
choice; Omarchy's adapter follows the active Omarchy palette.

## Rollback

Choose the prior Obsidian theme/base scheme and restore any backed-up local
appearance fields or overwritten theme folder. For Omarchy, remove or restore
the user template and reapply the current system theme to regenerate its CSS.

References: [Build a theme](https://docs.obsidian.md/Themes/App+themes/Build+a+theme),
[CSS colors](https://docs.obsidian.md/Reference/CSS+variables/Foundations/Colors).
