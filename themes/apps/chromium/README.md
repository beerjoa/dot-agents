# Explicit Chromium themes

`themes/kanagawa-wave` and `themes/kanagawa-lotus` are generated unpacked themes.
Their frame, toolbar, selected/unselected-tab and new-tab backgrounds all use
the palette background. Only the selected tab label uses the palette blue.
Address fields, buttons and icons use separate roles.
Both themes also include a generated 1×1 solid `frame.png`, referenced by
`theme_frame` and `theme_frame_inactive`. It uses the same palette background
and keeps Helium's vertical tab-strip surface from retaining a default gray fill
where color-only frame settings were insufficient on macOS.

There is deliberately no `theme_toolbar` image. Toolbar images are shared with
active tabs and can leak tab colors into macOS window controls. Coordinate-based
images cannot provide independent active-tab colors across window sizes/layouts.

## Color roles

| Role | Lotus | Wave |
| --- | --- | --- |
| Frame, toolbar, all tabs and new-tab page | `#f1e9d2` | `#1f1f28` |
| Selected tab text | `#4d699b` | `#7e9cd8` |
| Address text | `#43436c` | `#dcd7ba` |
| Inactive tab text, including unfocused windows | `#545464` | `#c8c093` |
| Toolbar labels, bookmarks and enabled icons | `#545464` | `#dcd7ba` |
| Address field background | `#faf4df` | `#17171e` |
| Control button background | `#e6dcc0` | `#223249` |
| New-tab links | `#4d699b` | `#7e9cd8` |

Toolbar labels and inactive-window tab colors are explicit so they do not fall
back to unrelated browser defaults. Small text retains at least 4.5:1 contrast
against its assigned surface. Lotus's lighter muted colors are not used for
small tab labels because their contrast is too low.

The [Chromium theme color table](https://chromium.googlesource.com/chromium/src/+/main/chrome/browser/themes/browser_theme_pack.cc)
exposes these base roles. Hover, pressed and disabled variants are derived by
Chromium from the base colors, contrast and transparency rules. Themes do not
expose independent focus-ring, selection or accent overrides; an exact Lotus
blue focus ring cannot be guaranteed by these manifests. Extension-provided
icons and page controls also have their own rendering.

## Stable identities

| Component | Extension ID |
| --- | --- |
| Lotus | `ccehnmniielbahkigdnafcjlbodlnbin` |
| Wave | `kaajneiiilkiffigikfonphgemodkjah` |
| Switcher | `gbgidndeigddelpgmncjecnnfhihfhff` |

The keys in `theme-keys.json` and `switcher/manifest.json` are public identity
material, not private signing keys. Keep them stable to preserve the native host
allowlist and controller mapping.

## Manual use

After checking `chrome://policy`, open `chrome://extensions`, enable Developer
mode, and load the desired theme folder unpacked. A nonempty `BrowserThemeColor`
policy blocks these themes. Removing the policy must be handled for the actual OS
and browser; see the Linux adapter before changing a shared policy directory.

## Automatic use

The switcher uses `management`, `nativeMessaging`, `storage` and `alarms`. It has
no page content scripts or network/host permissions. Its implementation acts only
on the two IDs above, although the management permission itself is broader.
It subscribes to `dev.beerjoa.omarchy_browser_theme` and selects Wave for dark,
Lotus for light. The current mapping contains these two themes only.

### First installation matters

Chromium removes unused themes. Do not initially load both from command-line
flags at once: the first can disappear before the service worker starts.

1. Configure the native host and current mode source, then load the switcher.
2. Load the theme opposite to the current mode first: Wave if the source is light,
   Lotus if dark. Wait for the switcher to disable it. At this point an error
   about the still-missing desired theme is expected.
3. In the switcher's service-worker inspector, use
   `chrome.management.get('<opposite-theme-id>').then(console.log)` to confirm
   `enabled: false` before continuing.
4. Load the theme matching the current mode. The installation listener will select
   it. Inspect `chrome.storage.local.get('status').then(console.log)` and confirm
   the expected mode/ID with `error: null`.
5. Once both are registered and protected, subsequent restarts can load the
   switcher and both themes together. Explicitly disabling the other theme via
   the controller keeps Chromium's collector from deleting it.

Manual theme selection is enough if automatic mode switching is not needed.
Reload updated theme files through the browser; rewriting source files alone is
not an installation or activation mechanism.

## Updating another computer

Update this checkout with `git pull --ff-only`, then reload both already-loaded
theme folders through the browser's extension manager. Keep the existing theme
keys, IDs and switcher; do not remove and reinstall the themes. Wave 1.0.10 and
Lotus 1.0.8 restore matching toolbar, tab-strip and frame backgrounds and use
blue text to distinguish the selected tab. There is no selected-tab fill highlight. A uniform 1×1
frame resource keeps the macOS vertical strip from falling back to gray. No
position-dependent tab image or custom toolbar image is used.
The controller mapping and permissions are unchanged.
For a new installation, follow the installation order above.

The PNG files are committed and need no machine-specific paths or image tooling.
To regenerate or verify them, use Python 3.11+:

```sh
python3 themes/scripts/generate.py
python3 themes/scripts/generate.py --check
python3 -m unittest discover -s themes/scripts -p 'test_*.py' -v
```

Automatic switching still requires the existing native host and an OS-specific
mode source on each computer. Do not copy another computer's browser profile,
credentials or generated native registrations to set it up. See
[`../../platforms/macos/`](../../platforms/macos/) for macOS preparation and
[`../../platforms/linux-omarchy/`](../../platforms/linux-omarchy/) for Omarchy.

## Active-tab configuration limits (Helium 0.20.3.1)

Checked against Chromium 156.0.8078.79 and Helium tag 0.20.3:

- `colors.toolbar` also supplies the active-tab background. There is no separate
  active-tab fill in `kOverwritableColorTable`.
- `colors.background_tab` and `tints.background_tab` target inactive tabs;
  `tab_text` targets the active tab's text, not its background.
- RGBA is accepted by the parser, but frame, toolbar and tab-background colors
  are forced opaque in `BrowserThemePack::GetColor`. Alpha cannot separate them.
- The tint table supports buttons, frame variants and background tabs, but no
  active-tab-only tint. The property table only contains new-tab-page settings.
- Helium's built-in Material tab colors use the omnibox background, but the
  Material override function skips extension themes. Setting
  `colors.omnibox_background` does not enable that route for these themes.
- The experimental `helium-native-frame-materials` flag exposes a native-material
  appearance option. It replaces frame surfaces with macOS materials rather
  than providing an independent theme fill, changing the rendered palette with
  the background and focus state. It was tested and restored to its original
  disabled/default state; it is not enabled by these portable themes.

The selected tab uses `toolbar`; unselected tabs use `background_tab` (or the
uniform frame image in vertical layout). These are tab selection states, not
application-process states. The `_inactive` suffix on `background_tab_inactive`
means the window has lost focus. The current configuration deliberately matches
all tab backgrounds and the toolbar to the frame, and highlights only the
selected label through `tab_text`. Selected-label contrast is 4.55:1 in Lotus
and 5.94:1 in Wave. Pinned or collapsed tabs that show only icons do not gain a
text highlight. These color roles require no size-specific coordinates.

### Built-in color alternative

Helium's **Customize Helium → Appearance → Custom color** keeps its Material
selection rendering: inactive tabs are transparent and active tabs use the
location-bar background, independently of the toolbar. This was checked in the
installed browser in light and dark modes. It does not load these extension
themes.

The built-in picker accepts a hue, converts it to a seed color and generates a
Tonal Spot palette. It does not accept separate Wave/Lotus surface, foreground
or active-tab colors. Changing the seed changes the whole generated palette;
it is not a way to apply the original Kanagawa HEX palette while retaining
Material rendering. The stored user color is shared by light and dark modes.
The current extension switcher enables the two manifest themes and must be
turned off when testing this alternative, or it will restore an extension theme.

Sources: [picker seed handling](https://github.com/chromium/chromium/blob/156.0.8078.79/chrome/browser/ui/webui/cr_components/theme_color_picker/theme_color_picker_handler.cc),
[generated palette](https://github.com/chromium/chromium/blob/156.0.8078.79/ui/color/ref_color_mixer.cc),
[user color and scheme preferences](https://github.com/chromium/chromium/blob/156.0.8078.79/chrome/browser/themes/theme_service.cc).

References: [official theme documentation](https://developer.chrome.com/docs/extensions/develop/ui/themes),
[theme parser and opacity enforcement](https://github.com/chromium/chromium/blob/156.0.8078.79/chrome/browser/themes/browser_theme_pack.cc),
[tab color mapping](https://github.com/chromium/chromium/blob/156.0.8078.79/chrome/browser/ui/color/tab_strip_color_mixer.cc),
[Helium native materials implementation](https://github.com/imputnet/helium/blob/0.20.3/patches/helium/ui/native-frame-materials.patch).
