# Dark Reader

`presets/theme.json` is a **partial color snippet**, not a complete Dark Reader
settings backup or a file to import blindly. It records dynamic rendering and
both dark/light background and text colors. Enter these colors through Dark
Reader's controls or merge them into a separately reviewed full settings export.
Personal site lists and custom site themes are not included.

## Optional native-connected build

The pinned patch adds Native Messaging, the existing fixed public identity, and
live palette handling. It disables Dark Reader's separate automation, settings
sync, and browser-theme changes while the Omarchy palette controls the mode.
Site-specific themes can still override global page colors. This is a local
fork and does not receive Chrome Web Store updates.

Reproduce from the repository root:

```sh
git clone --no-checkout https://github.com/darkreader/darkreader.git themes/local/darkreader
cd themes/local/darkreader
git checkout --detach fd09b7a3980802600efc66bffe5a5f479a5bf803
git apply ../../apps/darkreader/patches/darkreader-omarchy.patch
npm ci --ignore-scripts --no-audit --no-fund
node tasks/cli.js build --release --chrome-mv3
```

The unpacked build is under `build/release/chrome-mv3`. Configure the native host
before loading it; disable the stock Dark Reader while using this fork to avoid
two page-color engines acting at once. The fork ID is
`ccdoogahbheenigeccaafmbcfaaiggkb`.

The host starts with an empty local `initial-settings.json`; no settings are
copied from a browser profile. If importing personal settings into that local
file, keep them outside Git. Updating that file does not re-import it after
the fork's first successful initialization.
