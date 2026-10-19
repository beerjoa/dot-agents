# Explicit Chromium themes

`themes/kanagawa-wave` and `themes/kanagawa-lotus` are generated unpacked themes.
Their `frame`, `frame_inactive`, `toolbar` and new-tab background use the palette
background directly. Address fields, buttons and icons use separate palette roles.

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
