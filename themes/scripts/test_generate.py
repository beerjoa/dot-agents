"""Regression checks for portable Chromium frame assets."""
import base64
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib

import generate


class ChromiumFrameTests(unittest.TestCase):
    def test_frame_images_match_palette_and_preserve_theme_ids(self):
        files = generate.render()
        for slug, color, extension_id in (
            ('kanagawa-lotus', b'\xf1\xe9\xd2', 'ccehnmniielbahkigdnafcjlbodlnbin'),
            ('kanagawa-wave', b'\x1f\x1f\x28', 'kaajneiiilkiffigikfonphgemodkjah'),
        ):
            with self.subTest(slug=slug):
                root = f'apps/chromium/themes/{slug}'
                manifest = json.loads(files[f'{root}/manifest.json'])
                self.assertEqual(manifest['theme'].get('images'), {
                    'theme_frame': 'frame.png', 'theme_frame_inactive': 'frame.png',
                })
                digest = hashlib.sha256(base64.b64decode(manifest['key'])).hexdigest()[:32]
                self.assertEqual(''.join(chr(ord('a') + int(c, 16)) for c in digest), extension_id)
                png = files[f'{root}/frame.png']
                self.assertEqual(png[:8], b'\x89PNG\r\n\x1a\n')
                offset, compressed = 8, b''
                while offset < len(png):
                    size = struct.unpack_from('>I', png, offset)[0]
                    kind = png[offset + 4:offset + 8]
                    data = png[offset + 8:offset + 8 + size]
                    crc = struct.unpack_from('>I', png, offset + 8 + size)[0]
                    self.assertEqual(crc, zlib.crc32(kind + data))
                    if kind == b'IHDR':
                        self.assertEqual(struct.unpack('>IIBBBBB', data), (1, 1, 8, 2, 0, 0, 0))
                    if kind == b'IDAT':
                        compressed += data
                    offset += size + 12
                self.assertEqual(zlib.decompress(compressed), b'\x00' + color)

    def test_check_detects_corrupt_and_missing_binary_asset(self):
        with tempfile.TemporaryDirectory() as directory:
            command = [sys.executable, str(Path(generate.__file__)), '--output', directory]
            subprocess.run(command, check=True, capture_output=True)
            subprocess.run(command + ['--check'], check=True, capture_output=True)
            frame = Path(directory) / 'apps/chromium/themes/kanagawa-lotus/frame.png'
            self.assertTrue(frame.exists(), 'Generator must emit frame PNGs')
            frame.write_bytes(frame.read_bytes()[:-1] + b'!')
            for missing in (False, True):
                with self.subTest(missing=missing):
                    if missing:
                        frame.unlink()
                    result = subprocess.run(command + ['--check'], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn('kanagawa-lotus/frame.png', result.stderr)


if __name__ == '__main__':
    unittest.main()
