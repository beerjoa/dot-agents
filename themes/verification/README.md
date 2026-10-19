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
