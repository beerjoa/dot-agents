# Obsidian Themes Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans inline for this small integration.

**Goal:** Apply shared palette roles to Obsidian on this Omarchy installation and provide a portable Wave/Lotus app theme in dot-agents.

**Spec:** The user requested Obsidian theme application in both Omarchy OS and dot-agents after approving the browser's palette-based control/text roles.

**Architecture:** One CSS variable template feeds the generated portable two-mode theme and the Omarchy user template. Reuse Omarchy's existing Obsidian theme synchronization; select the existing Omarchy theme in the active vault. No plugin or new hook is needed.

## Constraints and review focus

- Use the existing develop branch, shared Wave/Lotus palettes and Obsidian's documented CSS variables.
- Keep machine-local vault paths and contents, account data, workspace files and backups outside Git.
- Modify only the active vault's appearance selection and Omarchy theme CSS; preserve notes, plugins and other preferences.
- Portable theme selection follows Obsidian's light/dark mode; system adaptation requires the target OS to signal its mode. Other platforms' runtime application remains unverified.
- Follow session instructions: static generation/CSS/contrast checks and application observations; no new tests or test-suite execution.

## Tasks

- [x] Add the shared CSS template, portable theme manifest and generator outputs; document installation and the Linux user override.
- [x] Check output consistency, CSS structure/variables, identity and private-path scope; perform a bounded independent review and fix its semantic-text contrast finding.
- [x] Back up the local appearance and Omarchy CSS files; install the user template, apply the existing Omarchy theme and enable it in the active vault with system appearance.
- [x] Observe light/dark application and restore Lotus; record limits in the verification README.
- [x] Commit locally on develop.
