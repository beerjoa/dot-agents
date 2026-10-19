# Native palette bridge

`host.py` is the existing POSIX Python host: it validates color input, atomically
exports a palette, and streams changes over Chromium's framed stdio protocol.
It accepts only the configured extension origin and a `subscribe` message.
It does not open a network server or execute shell commands.

Python 3.11+ is required. `configure.py` prepares two independent origin allowlists
and launchers using the exact interpreter running configuration. Select a stable
interpreter path without spaces and keep it available after setup.

```sh
python3 themes/bridge/configure.py \
  --source /absolute/path/to/current-colors.toml \
  --install-dir /absolute/path/to/private-theme-state \
  --native-host-dir /absolute/path/to/browser/NativeMessagingHosts
```

All three paths are per-machine inputs. Runtime config, state and initial settings
are written outside the repository with private file permissions. Re-running
configuration updates the two named native host registrations and launchers;
back up existing registrations first when migrating an installed integration.
The script does not edit browser flags, grant policy privileges, or launch apps.

On connection the host reads `--source` and emits the current palette. While
connected it watches the shared exported `palette.json` every 0.5 seconds.
After changing the source, run `<install-dir>/darkreader/host.py --export` to
notify both hosts. Linux's bundled theme-set hook does this automatically only
for the XDG install directory documented in the Linux guide. With another
`--install-dir`, set `root` in a machine-local hook copy to the same absolute
directory before installing it. A generic macOS system-appearance watcher is not
included.

For manual use, `--source` can point at one of the repository palettes. Changing
that file alone does not trigger export. To change modes, use a private current
palette file and export after updating it; do not edit installed Omarchy files.

This host uses POSIX pipe readiness through `select`; Windows needs a separate
transport adapter. Native registration directories vary by browser and OS.
