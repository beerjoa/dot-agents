# Portable themes implementation plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task by task.

**Goal:** Manage the existing Wave/Lotus app colors and browser integration in dot-agents on develop.

**Architecture:** TOML palettes are the color source. A standard-library generator emits app-specific color files; browser code and Dark Reader's pinned patch retain the working extension IDs. OS adapters contain policy and registration details. Existing installed settings remain in place.

**Tech Stack:** Python 3.11+, TOML, JSON, Chromium MV3, shell.

**Spec:** The user's approved common-theme inventory and `themes/README.md`.

## Constraints

- Start develop at freshly updated main; do not overwrite an existing branch.
- Export only colors and reviewed source, not profiles, site lists, credentials, absolute user paths, caches, upstream dependencies, or build output.
- Lotus background/text: #f1e9d2 / #545464. Wave: #1f1f28 / #dcd7ba.
- Keep browser frame and toolbar colors explicit; a generated policy seed is insufficient.
- Keep platform-dependent policy removal under Linux/Omarchy. macOS automation is not verified.
- Do not modify the currently installed integration during repository organization.
- Use static validation and source review; no test suites are requested for this organization task.

## Tasks

- [ ] Import the two palettes, reviewed extension sources, public identities, pinned patch and its license.
- [ ] Generate browser manifests, Dark Reader color snippets, Codex desktop appearance, terminal colors and Neovim color snippets from the palettes.
- [ ] Prepare native host registration with explicit per-machine paths; document Linux and macOS application separately.
- [ ] Add root README links, provenance, setup/rollback guidance, and verification limits.
- [ ] Check generated-file consistency, JSON/TOML parsing, syntax, privacy boundaries, diff whitespace, and obtain a final independent review.

## Review focus

- IDs must still match public keys and hardcoded switcher IDs.
- Reusing profiles or whole application configs must not expose private data.
- Native hosts must use an executable interpreter available on the target machine.
- Initial two-theme installation must explain the garbage-collection hazard.
- Linux's shared Chromium/Helium policy effects must remain explicit.
