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
