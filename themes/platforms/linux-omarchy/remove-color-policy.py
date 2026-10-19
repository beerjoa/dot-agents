#!/usr/bin/python
"""Remove only Chromium's generated theme seed so explicit themes can apply."""
import json
import os
from pathlib import Path
import sys
import tempfile


def remove_seed(path):
    if not path.exists():
        return
    if path.is_symlink() or not path.is_file():
        raise ValueError('Expected a regular browser color policy file')
    policy = json.loads(path.read_text())
    if not isinstance(policy, dict):
        raise ValueError('Expected a policy object')
    if 'BrowserThemeColor' not in policy:
        return
    del policy['BrowserThemeColor']
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(policy, stream)
            stream.write('\n')
        temporary.chmod(0o644)
        os.replace(temporary, path)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()


if __name__ == '__main__':
    if len(sys.argv) != 1 or os.geteuid() != 0:
        sys.exit('Run as root with no arguments')
    remove_seed(Path('/etc/chromium/policies/managed/color.json'))
