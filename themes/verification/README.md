# Verification record and boundaries

## Previously verified original integration

The standalone `omarchy-helium-theme-bridge` work verified native roundtrips,
Dark Reader page recoloring, site-exception preservation, invalid-palette
handling, disconnect/reconnect, settings initialization and browser restart.
The explicit browser-theme work verified exact browser CSS colors
`#f1e9d2` / `#1f1f28`, native mode switching, two-theme garbage-collection
survival and restart behavior in isolated Helium profiles.

On 2026-10-19 the real Linux installation reported successful dark and light
selections after Omarchy theme changes, with the color seed policy absent.
These are original-installation results, not fresh macOS/Windows results or a
claim that every exported application was visually checked.

## This repository migration

The migration uses static checks: generated-file consistency, JSON/TOML parsing,
Python/JavaScript/shell syntax, identity correspondence, patch/source provenance,
personal-path filtering, and whitespace checks. It does not rerun the original
browser test suites or deploy this new repository layout over the working setup.
No private initial-settings files, native registrations or browser profiles are
copied into Git.

Regeneration consistency from the repository root:

```sh
python3 themes/scripts/generate.py --check
```

The native registration preparer and platform guides are new portable packaging.
Their end-to-end use on a new machine remains a separate installation check.

## Browser color roles, 2026-10-19

The version 1.0.1 browser manifests add explicit toolbar labels and inactive tab
surfaces/text, with stronger active tab/address text. Static inspection confirmed
all 17 color keys are in Chromium's exposed theme color table, both public keys
and all four base backgrounds are unchanged, and assigned small text/surface
pairs meet 4.5:1 contrast. Generated-file consistency, Python syntax and Git
whitespace checks passed. No automated browser test suites were run for this change.

Both installed Helium themes were updated after backing up their old manifests
and cached packs outside Git. Helium 0.19.4.1 (Chromium 155.0.8059.84) was restarted
with its browsing session restored. The active Lotus cache was rebuilt and
contained the new `#43436c` text color. A live Omarchy switch to Wave selected its
existing extension ID and rebuilt a cache containing the `#c8c093` inactive label
color; switching back selected Lotus. Both themes remained registered, with the
controller enabled. The original single browser window/page was restored after
closing a temporary blank window.

Cropped toolbar screenshots were inspected in both modes. Focused address
fields followed the light/dark palette; unfocused fields, hover/pressed states,
disabled glyphs and focus rings remain subject to Chromium's derived colors.
This was not an exhaustive visual audit of every control, extension icon or
platform. No screenshots, browser preferences or personal paths were committed.

## Obsidian, 2026-10-19

One CSS source now generates a portable two-mode theme and an Omarchy user
template; generated-file consistency covers 16 outputs. Python/JSON parsing,
CSS selector/placeholder/duplicate-variable checks, private-path filtering and
Git whitespace checks passed. The original 14 generated color files are unchanged.
No CSS parser dependency was added and no automated test suites were run.

On the installed Obsidian 1.14.4, the existing Omarchy vault theme was selected
with the base scheme set to system after backing up its appearance and CSS.
The user template was installed outside package directories. Omarchy's existing
synchronizer copied the generated CSS to the one registered vault without a new
plugin or hook. The installed CSS matched Omarchy's current rendered output and
contained no unresolved placeholders.

Live switches between Wave and Lotus updated Obsidian's visible controls and
its body class (`theme-dark` / `theme-light`), confirming system-mode adaptation.
Lotus was restored afterward. The editor/sidebar/input/selection/accent-button
text pairs checked from the palette have at least 4.5:1 contrast. Review found
low contrast in several small semantic/syntax colors; those text roles now mix
25% palette hue with 75% normal foreground. Their minimum contrast across the
editor and code/sidebar surfaces is 4.63:1 in Lotus and 8.27:1 in Wave.

Settings-window screenshots were inspected locally; no screenshots, vault names,
notes, account settings or machine-local appearance/workspace files are in Git.
This is not an exhaustive visual audit of every note, plugin or graph. Portable
theme runtime application on macOS/Windows remains unverified.

## Zeron, 2026-10-19

Zeron 0.2.113's official theme documentation and importer source were checked
before implementation. Three generated JSON files provide a VS Code theme
package with both Wave and Lotus. The existing 16 outputs are unchanged.
Generated-file consistency now covers 19 outputs; JSON/Python parsing and Git
whitespace checks passed. No automated test suites or new dependencies were used.

After backing up device-local settings outside Git, the installed app's own
Appearance importer analyzed and imported both variants as a snapshot. Both
compiled variants retained the exact editor/shell backgrounds and supplied all
mapped color roles; the only fallback record concerns the opaque surface
recommendation. The importer adjusted muted/faint text to its contrast targets.
Wave had no validation warnings. Lotus retained the shared ANSI16 bright green
at slot 10, for which the importer reports contrast below 3:1.

Light and dark selections were set to Lotus and Wave with System mode, theme
default accent/surface, and wallpaper-derived colors disabled. Live Omarchy
switches changed the visible Zeron controls to Wave and back to Lotus without
restarting the app or adding a hook. Local settings screenshots were inspected;
this is not an exhaustive check of agent sessions, code, terminal output or every
interaction state. No private settings, library source paths, screenshots or
backups are committed. macOS/Windows runtime application remains unverified.

## Paseo, 2026-10-20

The installed Paseo desktop 0.12.0 and its matching official plugin API/source
were inspected. A local client-only plugin registers the two eight-color
palettes through `client.addTheme`. It has no server entry, preparation command,
dependency installation, network call or filesystem operation. Generated-file
consistency covers 20 outputs; the previous 19 outputs are unchanged. Python
syntax, manifest/palette JSON, hex color/schema shape, private-path filtering
and Git whitespace checks passed. No automated test suites were run.

The daemon configuration was backed up outside Git. Official `paseo plugin add`
registered the local directory. Plugins were initially globally disabled; only
this new plugin was configured. Enabling the global switch in Settings allowed
the plugin to load. The final daemon-config differences were only `plugins` and
`pluginsEnabled`; other daemon configuration was preserved.

Both variants appeared in Appearance and were selected and visually inspected
on Linux. The app showed the Lotus surfaces and then Wave surfaces, text, input
fields and borders. Wave was left selected to match the current dark Omarchy
mode. Official plugin reload returned `running`. The source foreground/secondary
text contrast across background/raised/control surfaces is at least 7.05:1 in
Wave and 5.43:1 in Lotus. This is not an exhaustive audit of all derived states,
terminal ANSI colors, code or agent sessions.

Paseo 0.12.0 disables adaptive system theming when a contributed theme is
selected, so automatic Wave/Lotus switching is not implemented here. The
separate syntax theme was preserved. App restart persistence, additional hosts,
macOS, Windows and mobile runtime application remain unverified. Private daemon
settings, browser storage, screenshots and backups are not committed.

## Paseo automatic Omarchy adapter, 2026-10-20

A separate `dot-agents-omarchy` client-only plugin now contributes one stable
`current` theme. A user `theme-set.d/80-paseo-theme` hook renders its palette
outside Git from Omarchy's active colors and calls the official plugin reload
command. Theme Scheduler's source calls `omarchy theme set`, which runs this
hook; neither the scheduler nor package-owned Omarchy/Paseo files were modified.
The portable manual Wave/Lotus plugin and separate syntax theme are preserved.

After a private daemon-config backup, plugin installation and reload reported
`running`. **Omarchy (automatic)** was selected once through Appearance. A live
manual `omarchy theme set kanagawa` changed the selected theme's appearance and
visible background, text and controls to dark without another selection. A
subsequent `kanagawa-lotus` switch restored the initial light OS and app colors
while retaining the automatic selection. Screenshots were inspected locally.
This exercises the scheduler's command path, not a timed scheduler event.

Generated-file consistency still covers 20 unchanged outputs. Python and Bash
syntax, palette/manifest structure, installed-file correspondence and Git
whitespace checks passed. No automated test suites were run. Daemon restart,
stopped-daemon catch-up, multiple hosts, rapid concurrent switches and other
operating systems were not exercised. Runtime plugin source, configuration,
backups and screenshots remain outside Git.
