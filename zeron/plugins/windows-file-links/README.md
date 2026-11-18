# Windows File Links for Zeron

Personal plugin for Windows Zeron beta 0.3.7. It corrects existing Markdown file
links inside the current session's working folder and opens them in Zeron's
normal file viewer.

Supported targets include `C:/Work/repo/src/main.rs`, `C:\Work\repo\src\main.rs`,
and `file:///C:/Work/repo/src/main.rs`. Windows drive/folder ASCII case and path
separators are normalized for ownership checks; the relative file name keeps its
original spelling. Spaces, Korean names and percent-encoded UTF-8 are supported.
Line/column references (`:12`, `:12:5`, `#L12C5`) and line ranges are retained.

The plugin overrides only `@app/screens/chat/file_links`. Its only requested
permission is `ui.replace`. It has no command, network, service, message-writing
or custom viewer functionality. A screen replacement executes with the app's
own authority, so Zeron requires approval in its own interface.

## Enable on this PC

The plugin is registered under **Settings → Plugins → Windows File Links**.
Allow its screen-replacement permission there, then keep it enabled. Before that
approval, the files are installed but the resolver replacement is inactive.

The installation folder is `%LOCALAPPDATA%\Zeron\plugins\windows-file-links`.
Zeron creates and maintains its local signature. This repository's manifest has
no signature or device identity. To set up another device, create the plugin with
Zeron's `create_plugin` tool and copy the authored module, entry, README and license;
merge this manifest's `ui.replace` target into that device's generated manifest.

Existing messages use the corrected resolver when the plugin is active; they do
not need to be resent. To restore Zeron's original behavior, disable this plugin.
If a Zeron update changes the resolver contract, disable it and review the updated
upstream module before updating the plugin.

## Boundaries

- A Windows absolute target must be inside the current session's working folder.
  Other drives, sibling prefixes, missing roots, UNC paths, parent traversal and
  alternate data streams are refused.
- The plugin resolves links; it does not turn ordinary prose or inline-code paths
  into new links, and it does not make missing files exist.
- Relative and POSIX resolution, mentions, file chips and the exported module's
  existing contract are retained. The original POSIX `outside` result is retained;
  opening external files remains subject to Zeron's existing click handler.

## Verification

Run with the official [Luau CLI](https://github.com/luau-lang/luau/releases):

```sh
luau tests/paths.luau
luau-analyze windows_file_links.luau
```

The unmodified resolver failed 18 Windows cases. The corrected resolver passes
all 59 path cases plus mention round-trip and file-chip checks, and its Luau type
analysis passes. Plugin loading and live viewer clicks are separate runtime
checks; see the installed plugin's status in Zeron.

## Provenance

`windows_file_links.luau` adapts the MIT-licensed Zeron resolver at
[`f6a9bbfc29796cb90389ddd8e2e3bdcd8996829b`](https://github.com/zeronsh/zeron/blob/f6a9bbfc29796cb90389ddd8e2e3bdcd8996829b/apps/zgx/ui/screens/chat/file_links.luau),
matching this PC's beta 0.3.7 baseline. The original local module SHA-256 is
`44e028cfa4d8c8e36a5c21ea520654b304c9f70ccbfd9e5a7ec953cc8054aa65`.
The Windows ownership and resolution changes are authored here; the upstream
license is retained in `ZERON-LICENSE`.
