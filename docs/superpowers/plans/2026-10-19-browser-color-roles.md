# Browser Color Roles Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this small change inline.

**Goal:** Match Lotus and Wave browser controls, labels and icons to their existing frame palettes.

**Architecture:** Extend the existing generator's supported Chromium theme colors. Keep extension IDs, native hosts and the two-mode switcher unchanged.

**Tech Stack:** Python 3.11+, Chromium theme manifests, installed Helium.

**Spec:** User-approved role mapping in this conversation: preserve the frame; distinguish controls and active/inactive text using the same palette; use supported theme properties and observe browser-derived states.

## Constraints and review focus

- Preserve Lotus `#f1e9d2` and Wave `#1f1f28` frames and toolbars.
- Keep small active and inactive text at contrast 4.5 or better on their assigned surfaces.
- Do not invent manifest keys for hover, pressed, disabled, selection or focus colors. Chromium derives these; exact focus/accent overrides are outside its exposed theme color table.
- Use the existing `develop` checkout. Do not push or change browser profiles, policy or site settings.
- Per session instructions, use static consistency/syntax/contrast checks and application observations; do not add or run test suites.

## Tasks

- [x] Extend `themes/scripts/generate.py` with explicit toolbar text and active/inactive tab colors; bump the two theme versions to `1.0.1` and regenerate their manifests.
- [x] Document the supported roles and derived-state limits in `themes/apps/chromium/README.md`.
- [x] Check generated consistency, supported keys, palette contrast and unchanged public identities; get a bounded independent code review (no findings).
- [x] Back up installed manifests and cached theme packs outside Git; deploy only the two theme manifests, rebuild caches and relaunch Helium with session restoration.
- [x] Record actual activation evidence and visual-verification limits in `themes/verification/README.md`.
- [x] Commit repository changes locally on `develop`.
