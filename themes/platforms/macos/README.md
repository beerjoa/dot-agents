# macOS reuse

## Available now as app data

- Load either generated Chromium theme manually after checking that the browser
  permits custom themes. Theme colors and fixed public IDs are OS-independent;
  actual application in macOS Helium has not been verified.
- Apply the Dark Reader color values through its settings. No native host is
  needed for manual color selection.
- Merge the Codex desktop appearance tables if the target app uses that schema.
- Include the color snippet for Ghostty, Kitty or Alacritty if that application
  is already part of the Mac setup. Fonts and commands remain machine-local.
- Choose a LazyVim snippet only for a compatible existing Neovim setup.
- Install the [portable Obsidian theme](../../apps/obsidian/README.md) in each
  intended vault and select **Adapt to system** for OS-driven Wave/Lotus switching.
  Actual macOS application has not been verified.

## Optional native host preparation

Use Python 3.11+ from a stable executable path. The generated launchers pin that
interpreter; removing or moving its installation requires re-running setup.
The macOS system Python is not assumed to satisfy this requirement.

Use `bridge/configure.py` with explicit local paths and the native-host directory
documented by the selected browser. Google Chrome and Chromium use different
application-support directories. Do not assume Helium's registration directory
from Chrome's name or from the Linux example.

For a manual source, copy one shared palette to a private current-colors TOML
file, pass that file as `--source`, then run the generated Dark Reader host with
`--export` after replacing the file with the other palette. Register/load both
extensions only after reviewing their permissions and first-install sequence.

See the official [Native Messaging documentation](https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging)
for the selected browser's protocol and Chrome/Chromium directory conventions.

**Automatic macOS appearance/sunrise detection is not implemented or verified.**
The Linux Omarchy Scheduler, `/etc/chromium` policy helper and sudoers grant must
not be installed on a Mac. Supporting a native macOS mode source is a separate
adapter task; the palette and app data do not depend on it.
