#!/usr/bin/env python3
"""Publish Omarchy's active palette through Paseo's local theme plugin API."""

import argparse
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import tomllib


PLUGIN_ID = "dot-agents-omarchy"
ROOT = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share") / "omarchy-paseo-theme"
SOURCE = Path.home() / ".local/state/omarchy/current/theme/colors.toml"
PASEO_HOME = Path(os.environ.get("PASEO_HOME") or Path.home() / ".paseo")


def replace(path, content):
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(content)
            stream.close()
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)


def sync(prepare):
    palette = tomllib.loads(SOURCE.read_text())
    mode = palette["mode"]
    if mode not in ("dark", "light"):
        raise ValueError("Omarchy mode must be dark or light")
    roles = {
        "background": "background",
        "foreground": "foreground",
        "raised": "dark_background",
        "control": "lighter_background",
        "border": "muted",
        "accent": "blue",
        "mutedForeground": "light_foreground" if mode == "dark" else "foreground",
        "ring": "blue",
    }
    colors = {role: palette[key] for role, key in roles.items()}
    if any(not isinstance(color, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", color)
           for color in colors.values()):
        raise ValueError("Omarchy theme colors must be six-digit hex strings")
    theme = {"id": "current", "name": "Omarchy (automatic)", "appearance": mode, "colors": colors}
    manifest = {
        "id": PLUGIN_ID,
        "description": "Current Omarchy palette, updated by the local theme-set hook",
        "requirements": {"paseo": ">=0.12.0"},
    }
    entry = (
        '// Generated locally by paseo-theme-sync.py.\n'
        'import type { PluginClientContext } from "@getpaseo/plugin/client";\n\n'
        'export default function contribute(client: PluginClientContext) {\n'
        f'  client.addTheme({json.dumps(theme, indent=2)});\n'
        '  return () => {};\n}\n'
    )
    plugin = ROOT / "plugin"
    plugin.mkdir(exist_ok=True)
    replace(plugin / "paseo-plugin.json", json.dumps(manifest, indent=2) + "\n")
    replace(plugin / "index.client.ts", entry)
    if prepare:
        print(f"Prepared {PLUGIN_ID}: {mode}")
        return

    # Do not enable plugins, install anything, or start a stopped daemon in a hook.
    try:
        config = json.loads((PASEO_HOME / "config.json").read_text())
        pid = json.loads((PASEO_HOME / "paseo.pid").read_text())["pid"]
        os.kill(pid, 0)
    except (FileNotFoundError, ProcessLookupError):
        return
    registration = config.get("plugins", {}).get(PLUGIN_ID, {})
    if not config.get("pluginsEnabled") or not registration or not registration.get("enabled", True):
        return
    result = subprocess.run(
        ["paseo", "plugin", "reload", PLUGIN_ID, "--home", str(PASEO_HOME), "--json"],
        stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=20,
    )
    if result.returncode:
        raise RuntimeError(f"Paseo plugin reload failed: {result.stderr.strip() or result.stdout.strip()}")
    print(f"Updated {PLUGIN_ID}: {mode}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare", action="store_true", help="render the plugin without contacting Paseo")
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (ROOT / "sync.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        sync(args.prepare)


if __name__ == "__main__":
    main()
