# Sources

- Wave colors: the installed Omarchy `kanagawa/colors.toml`, based on
  [Omarchy](https://github.com/basecamp/omarchy) and
  [kanagawa.nvim](https://github.com/rebelot/kanagawa.nvim).
- Lotus colors: the current locally customized Omarchy Lotus palette. Its
  `#f1e9d2` background is intentional; do not replace it with the upstream Lotus
  default `#f2ecbc`. The Hyprland-only border setting was omitted.
- Browser theme public keys, the controller and native host: the local
  `omarchy-helium-theme-bridge` project built in this session. The controller
  includes the subsequent missing-theme/startup fix. No private keys are included.
- Dark Reader patch: official [darkreader/darkreader](https://github.com/darkreader/darkreader),
  commit `fd09b7a3980802600efc66bffe5a5f479a5bf803`, version 4.9.133.
  The matching [MIT license](vendor/DARKREADER-LICENSE) is retained.
- Codex appearance values: only the observed `desktop` appearance tables were
  extracted. The rest of the user's application config was not copied.
- Terminal roles follow Omarchy's color templates. The generated snippets carry
  only colors; they do not copy terminal programs, hardware settings or keybindings.
- Neovim snippets retain the existing LazyVim/kanagawa.nvim configuration shape
  and override only the palette background.
- Obsidian CSS is authored here from the shared palettes using
  [documented CSS variables](https://docs.obsidian.md/Reference/CSS+variables/Foundations/Colors).
  The Linux adapter uses Omarchy's existing user template and vault-theme sync.
- Zeron color data is authored here from the shared palettes, targeting the
  [official 0.2.113 theme importer](https://github.com/zeronsh/zeron/blob/6ac8859998909bc5afd55838afb0635c281f31c3/docs/theme-system.md).
  No Zeron implementation, built-in theme or device-local library is copied.
- Paseo color plugin is authored here from the shared palettes using the
  [official 0.12.0 theme API](https://github.com/getpaseo/paseo/blob/cafe4b01c8522ff39560241c5deb01427dc8dc5b/public-docs/plugins/reference.md#contribute-a-theme).
  Only the client registration pattern is used; no third-party plugin is installed.

Review upstream changes before rebasing the Dark Reader patch. The extension
build and its dependencies are deliberately not vendored here.
