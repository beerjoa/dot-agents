# Herdr desktop app settings

This guide covers the native Herdr desktop app (GPUI), verified against macOS
build `20261028.1`. The sample is a partial configuration, not a backup of an
installed app. Its keyboard shortcuts target macOS; review or omit those tables
on other operating systems.

## Shared settings

[`config-gpui.local.toml`](config-gpui.local.toml) contains:

- The `normal` layout, high UI contrast, and background opacity `0.9`.
- Automatic Kanagawa Lotus light / Wave dark theme selection.
- Workspace selection with `Cmd+1` through `Cmd+9`, pane swapping with
  `Cmd+Shift+Arrow`, pane cycling with `Option+Tab` / `Option+Shift+Tab`
  or `Cmd+Option+]` / `Cmd+Option+[`, find with `Cmd+Shift+F`, and full screen
  with `Cmd+F` / `Ctrl+Cmd+F`.
- Removal of four default terminal key translations in `[pane_keys]`. This
  releases `Cmd+Left/Right` and `Option+Left/Right` for app navigation; it changes
  the default line/word movement behavior and should be reviewed before merging.
- Remote control disabled until explicitly configured on the destination machine.

This desktop sample does not require a terminal CLI keymap or shell wrapper.
It does not include the daemon's shared `[keys]` map, so it does not reproduce
additional shortcuts inherited from a locally customized daemon. Do not assume
the sample installs a Mod or a community Layout; this session did not install any.

## Apply on another machine

1. Run Herdr's `config` command to locate its configuration files. On the verified
   macOS installation, the executable is
   `/Applications/Herdr.app/Contents/MacOS/Herdr`, and the local override is
   `~/.config/herdr/config-gpui.local.toml`.
2. Back up the existing override outside this repository in a private location.
   Install the two shared color files using the
   [Ghostty theme installation guide](../themes/apps/terminals/ghostty/README.md#install-the-two-theme-files).
   Herdr loads those Ghostty theme names; a Ghostty shell wrapper is unnecessary.
3. Merge only the chosen top-level keys and table entries from the sample. Do not
   replace the entire file or append duplicate TOML tables. Preserve unrelated
   settings and existing remote configuration unless changing it deliberately.
4. Validate and reload with the installed executable. On macOS:

   ```sh
   /Applications/Herdr.app/Contents/MacOS/Herdr config check
   /Applications/Herdr.app/Contents/MacOS/Herdr config reload
   ```

5. Confirm the theme and shortcuts in the app. Static validation does not prove
   all shortcuts work on every platform. To undo, restore only the changed keys
   from the private backup and reload.

## Optional phone access over Tailscale

Phone pairing is local setup, not shared state. Keep it disabled in the public
sample. When enabling it on a destination machine:

1. Connect the Mac and phone to the same Tailscale network. Read that Mac's own
   Tailscale IP; never reuse an address from another machine.
2. In **Settings > Remote control**, select that address under **Listen on**
   before enabling remote control. The corresponding config key is `remote.bind`;
   `"all"` listens on every interface, rather than restricting access to Tailscale.
   Leave **Certificate** at the intended local choice and review **Keep running
   when Herdr UI quits** before enabling unattended access.
3. Open **Pair a phone** again. Check that its address is the intended Tailscale
   address and port, then scan the new QR and approve the intended device on the Mac.
4. Check the connected-device status in Herdr. Merely showing the correct QR
   address is not evidence of successful phone pairing.

Herdr's **Own CA** mode uses a locally created certificate authority. Tailscale
connectivity does not make Safari trust that authority. An iPhone certificate
warning was reported in this setup; its exact error and a successful certificate
trust procedure have not been verified. Diagnose the displayed certificate error
and verify the certificate identity before proceeding. Developer app-signing trust
under iOS device management is unrelated to browser HTTPS trust.

Do not publish or copy machine IPs, hostnames, tailnet domains, CA/key files,
certificate fingerprints from this machine, QR codes, pairing tokens, paired-device
records, agent sessions, or remote service state. Choose these on each device.

## Verification boundary

The local app accepted the appearance/keybinding configuration. After a local
`remote.bind` change, both **Addresses** and the newly opened pairing dialog showed
only the selected Tailscale IP. That machine-specific value is excluded here.
Actual iPhone pairing, HTTPS trust, and cross-platform shortcut behavior remain
unverified. This guide does not claim those issues were resolved.
