#!/usr/bin/env python3
"""Prepare local native hosts with explicit machine paths; does not launch browsers."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
HOSTS = {
    'darkreader': ('dev.beerjoa.omarchy_theme', 'ccdoogahbheenigeccaafmbcfaaiggkb'),
    'browser': ('dev.beerjoa.omarchy_browser_theme', 'gbgidndeigddelpgmncjecnnfhihfhff'),
}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')
    path.chmod(0o600)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path, help='Current palette TOML; hook must export after changes')
    parser.add_argument('--install-dir', required=True, type=Path, help='Private local native host/state directory')
    parser.add_argument('--native-host-dir', required=True, type=Path, help='NativeMessagingHosts directory for the browser')
    args = parser.parse_args()
    # Preserve the logical current-theme path if it contains a changing symlink.
    source = args.source.expanduser().absolute()
    if not source.is_file():
        parser.error('The palette source must be an existing TOML file')
    install = args.install_dir.expanduser().resolve()
    registration = args.native_host_dir.expanduser().resolve()
    repo = ROOT.parent
    if install == repo or repo in install.parents or registration == repo or repo in registration.parents:
        parser.error('Choose machine-local directories outside the repository')
    if any(c.isspace() for c in sys.executable):
        parser.error('Use a Python interpreter whose executable path contains no whitespace')
    install.mkdir(parents=True, exist_ok=True)
    install.chmod(0o700)
    initial = install / 'initial-settings.json'
    if not initial.exists():
        write_json(initial, {})
    for kind, (name, extension_id) in HOSTS.items():
        folder = install / kind
        folder.mkdir(exist_ok=True)
        executable = folder / 'host.py'
        lines = (ROOT / 'bridge/host.py').read_text().splitlines(keepends=True)
        executable.write_text(f'#!{sys.executable}\n' + ''.join(lines[1:]))
        executable.chmod(0o700)
        write_json(folder / 'bridge-config.json', {
            'extension_id': extension_id, 'source': str(source),
            'palette': str(install / 'palette.json'), 'initial_settings': str(initial),
        })
        write_json(registration / f'{name}.json', {
            'name': name, 'description': f'dot-agents {kind} theme bridge',
            'path': str(executable), 'type': 'stdio',
            'allowed_origins': [f'chrome-extension://{extension_id}/'],
        })
    print(f'Prepared native hosts in {install}; registrations in {registration}')
    print('Keep the interpreter at this path available; use --export after palette changes.')


if __name__ == '__main__':
    main()
