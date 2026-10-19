#!/usr/bin/env python3
"""Export an Omarchy palette or stream it to the authorized browser extension."""
import json
import os
from pathlib import Path
import re
import select
import struct
import sys
import tempfile
import tomllib


def parse_palette(value):
    colors = {}
    for key in ('background', 'foreground'):
        color = value.get(key)
        if not isinstance(color, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', color):
            raise ValueError(f'Invalid {key}')
        colors[key] = color.lower()
    mode = value.get('mode')
    if mode is None:
        def brightness(color):
            return sum(int(color[i:i + 2], 16) * weight for i, weight in [(1, 299), (3, 587), (5, 114)])
        mode = 'dark' if brightness(colors['background']) < brightness(colors['foreground']) else 'light'
    if mode not in ('light', 'dark'):
        raise ValueError('Invalid mode')
    return {'mode': mode, **colors}


def export_palette(source, target):
    palette = parse_palette(tomllib.loads(source.read_text()))
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', dir=target.parent, delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(palette, stream)
            stream.write('\n')
        os.replace(temporary, target)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()
    return palette


def read_message(stream):
    header = stream.read(4)
    if not header:
        return None
    if len(header) != 4:
        raise ValueError('Truncated message header')
    length = struct.unpack('=I', header)[0]
    if not 0 < length <= 65536:
        raise ValueError('Invalid message length')
    payload = stream.read(length)
    if len(payload) != length:
        raise ValueError('Truncated message payload')
    message = json.loads(payload)
    if not isinstance(message, dict):
        raise ValueError('Expected a message object')
    return message


def write_message(message, stream):
    payload = json.dumps(message, ensure_ascii=False).encode('utf-8')
    if len(payload) > 1024 * 1024:
        raise ValueError('Message exceeds browser limit')
    stream.write(struct.pack('=I', len(payload)) + payload)
    stream.flush()


def serve(config, origin):
    if origin != f"chrome-extension://{config['extension_id']}/":
        raise ValueError('Unauthorized extension origin')
    if read_message(sys.stdin.buffer) != {'type': 'subscribe'}:
        raise ValueError('Expected subscription')
    source = Path(config['source'])
    palette_file = Path(config['palette'])
    try:
        export_palette(source, palette_file)
    except (OSError, ValueError) as error:
        print(f'Cannot export current palette: {error}', file=sys.stderr)
    initial = json.loads(Path(config['initial_settings']).read_text())
    previous = None
    first = True
    while True:
        try:
            palette = parse_palette(json.loads(palette_file.read_text()))
            if palette != previous:
                message = {'type': 'palette', 'palette': palette}
                if first:
                    message['initialSettings'] = initial
                write_message(message, sys.stdout.buffer)
                previous = palette
                first = False
        except (OSError, ValueError) as error:
            # A missing/invalid palette must not replace a valid browser theme.
            if first:
                print(f'Waiting for a valid palette: {error}', file=sys.stderr)
        readable, _, _ = select.select([sys.stdin.buffer], [], [], 0.5)
        if readable:
            message = read_message(sys.stdin.buffer)
            if message is None:
                return
            raise ValueError('Unexpected message after subscription')


def main():
    config = json.loads(Path(__file__).with_name('bridge-config.json').read_text())
    if sys.argv[1:] == ['--export']:
        export_palette(Path(config['source']), Path(config['palette']))
    elif len(sys.argv) >= 2:
        serve(config, sys.argv[1])
    else:
        raise ValueError('Expected --export or a browser extension origin')


if __name__ == '__main__':
    try:
        main()
    except (BrokenPipeError, KeyboardInterrupt):
        sys.exit(0)
    except (OSError, ValueError, KeyError) as error:
        print(f'Omarchy theme bridge: {error}', file=sys.stderr)
        sys.exit(1)
