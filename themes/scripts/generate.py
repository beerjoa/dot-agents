#!/usr/bin/env python3
"""Render reviewed app color snippets from the two shared palettes (Python 3.11+)."""
import argparse
import json
from pathlib import Path
import re
import struct
import tomllib
import zlib

ROOT = Path(__file__).resolve().parents[1]
PALETTES = (('kanagawa-wave', 'Kanagawa Wave', 'dark'), ('kanagawa-lotus', 'Kanagawa Lotus', 'light'))
ANSI = ('background', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'foreground',
        'muted', 'bright_red', 'bright_green', 'bright_yellow', 'bright_blue',
        'bright_magenta', 'bright_cyan', 'bright_foreground')


def rgb(color):
    return [int(color[i:i + 2], 16) for i in (1, 3, 5)]


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def frame_png(color):
    def chunk(kind, data):
        return (struct.pack('>I', len(data)) + kind + data
                + struct.pack('>I', zlib.crc32(kind + data)))

    return (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(b'\x00' + bytes(rgb(color))))
            + chunk(b'IEND', b''))


def render():
    files = {}
    palettes = {}
    paseo = []
    keys = json.loads((ROOT / 'apps/chromium/theme-keys.json').read_text())
    obsidian_template = (ROOT / 'apps/obsidian/theme.css.tpl').read_text()
    obsidian = ['/* Generated Wave/Lotus theme; edit theme.css.tpl and the shared palettes. */']
    codex = ['# Generated color-only snippet; merge into existing config.toml.',
             '[desktop]', 'appearanceTheme = "system"']
    for slug, name, mode in PALETTES:
        p = tomllib.loads((ROOT / f'palettes/{slug}.toml').read_text())
        if p['mode'] != mode or any(not re.fullmatch(r'#[0-9a-fA-F]{6}', v) for k, v in p.items() if k != 'mode'):
            raise ValueError(f'Invalid palette: {slug}')
        palettes[mode] = p
        orca = [f'name: "{name}"', f'details: "{"darker" if mode == "dark" else "lighter"}"',
                f'background: "{p["background"]}"', f'foreground: "{p["foreground"]}"',
                f'cursor: "{p["bright_foreground"]}"', 'terminal_colors:']
        for section, roles in [('normal', ANSI[:8]), ('bright', ANSI[8:])]:
            orca.append(f'  {section}:')
            orca.extend(f'    {label}: "{p[role]}"' for label, role in
                        zip(('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'), roles))
        files[f'apps/orca/{slug}.yaml'] = '\n'.join(orca) + '\n'
        paseo.append({
            'id': slug, 'name': name, 'appearance': mode,
            'colors': {
                'background': p['background'], 'foreground': p['foreground'],
                'raised': p['dark_background'],
                'control': p['lighter_background'], 'border': p['muted'],
                'accent': p['blue'],
                'mutedForeground': p['light_foreground'] if mode == 'dark' else p['foreground'],
                'ring': p['blue'],
            },
        })
        zeron_colors = {}
        for role, tokens in {
            'dark_background': ('panel.background', 'list.hoverBackground', 'dropdown.background', 'menu.background', 'editorWidget.background'),
            'lighter_background': ('input.background',),
            'foreground': ('foreground', 'editor.foreground', 'input.foreground', 'terminal.foreground'),
            'light_foreground': ('descriptionForeground', 'tab.inactiveForeground'),
            'dark_foreground': ('disabledForeground', 'input.placeholderForeground'),
            'selection': ('list.activeSelectionBackground', 'list.inactiveSelectionBackground', 'terminal.selectionBackground'),
            'muted': ('panel.border', 'widget.border'),
            'blue': ('focusBorder', 'textLink.foreground', 'button.background'),
            'background': ('editor.background', 'sideBar.background', 'activityBar.background', 'terminal.background', 'button.foreground'),
            'bright_foreground': ('editorCursor.foreground',),
            'red': ('editorError.foreground',),
            'yellow': ('editorWarning.foreground',),
            'green': ('gitDecoration.addedResourceForeground',),
        }.items():
            zeron_colors.update({token: p[role] for token in tokens})
        zeron_colors.update({
            'diffEditor.insertedTextBackground': p['green'] + '30',
            'diffEditor.removedTextBackground': p['red'] + '30',
            'diffEditor.diagonalFill': p['blue'] + '20',
        })
        ansi_names = ('Black', 'Red', 'Green', 'Yellow', 'Blue', 'Magenta', 'Cyan', 'White')
        for bright, roles in [('', ANSI[:8]), ('Bright', ANSI[8:])]:
            zeron_colors.update({f'terminal.ansi{bright}{label}': p[role]
                                 for label, role in zip(ansi_names, roles)})
        files[f'apps/zeron/themes/{slug}.json'] = json_text({
            'name': name, 'type': mode, 'colors': zeron_colors,
            'tokenColors': [
                {'scope': scope, 'settings': {'foreground': p[role]}}
                for scope, role in [
                    ('comment', 'light_foreground'), ('keyword', 'magenta'),
                    ('keyword.operator', 'cyan'), ('string', 'green'),
                    ('constant.numeric', 'orange'), ('constant.language', 'orange'),
                    ('entity.name.function', 'blue'), ('support.function', 'blue'),
                    ('entity.name.type', 'yellow'), ('support.type', 'yellow'),
                    ('variable', 'foreground'), ('variable.parameter', 'foreground'),
                    ('variable.other.property', 'cyan'), ('entity.name.tag', 'red'),
                    ('entity.other.attribute', 'yellow'), ('punctuation', 'foreground'),
                ]
            ],
        })
        obsidian.append(re.sub(r'{{ (\w+) }}', lambda match: p[match[1]], obsidian_template)
                        .replace('.theme-dark, .theme-light', f'.theme-{mode}'))
        colors = {k: rgb(p['foreground']) for k in ('toolbar_text', 'bookmark_text', 'toolbar_button_icon', 'ntp_text')}
        colors.update({k: rgb(p['bright_foreground']) for k in ('tab_text', 'omnibox_text')})
        inactive_text = p['light_foreground'] if mode == 'dark' else p['foreground']
        colors.update({k: rgb(inactive_text) for k in ('tab_background_text', 'tab_background_text_inactive')})
        colors.update({k: rgb(p['dark_background']) for k in ('background_tab', 'background_tab_inactive')})
        colors.update({k: rgb(p['background']) for k in ('frame', 'frame_inactive', 'toolbar', 'ntp_background')})
        colors.update(button_background=rgb(p['lighter_background'] if mode == 'dark' else p['dark_background']),
                      omnibox_background=rgb(p['dark_background'] if mode == 'dark' else p['lighter_background']),
                      ntp_link=rgb(p['blue']))
        files[f'apps/chromium/themes/{slug}/manifest.json'] = json_text({
            'manifest_version': 3, 'name': f'Omarchy — {name}', 'version': '1.0.2',
            'key': keys[mode], 'theme': {
                'colors': colors,
                'images': {'theme_frame': 'frame.png', 'theme_frame_inactive': 'frame.png'},
            },
        })
        files[f'apps/chromium/themes/{slug}/frame.png'] = frame_png(p['background'])
        files[f'platforms/linux-omarchy/chromium/{slug}.theme'] = ','.join(map(str, rgb(p['background']))) + '\n'
        prefix = 'appearanceDarkChromeTheme' if mode == 'dark' else 'appearanceLightChromeTheme'
        codex.extend(['', f'[desktop.{prefix}]', f'accent = "{p["blue"]}"',
                      'accentSource = "custom"', 'contrast = 60',
                      f'ink = "{p["foreground"]}"', f'surface = "{p["background"]}"',
                      'opaqueWindows = true', '', f'[desktop.{prefix}.semanticColors]',
                      f'diffAdded = "{p["green"]}"', f'diffRemoved = "{p["red"]}"',
                      f'skill = "{p["magenta"] if mode == "dark" else p["bright_magenta"]}"'])
        ghostty = [f'background = {p["background"]}', f'foreground = {p["foreground"]}',
                   f'cursor-color = {p["bright_foreground"]}',
                   f'selection-background = {p["selection"]}', f'selection-foreground = {p["foreground"]}']
        ghostty.extend(f'palette = {i}={p[k]}' for i, k in enumerate(ANSI))
        files[f'apps/terminals/ghostty/{slug}.conf'] = '\n'.join(ghostty) + '\n'
        kitty = [f'background {p["background"]}', f'foreground {p["foreground"]}',
                 f'cursor {p["bright_foreground"]}', f'cursor_text_color {p["background"]}',
                 f'selection_background {p["selection"]}', f'selection_foreground {p["foreground"]}']
        kitty.extend(f'color{i} {p[k]}' for i, k in enumerate(ANSI))
        files[f'apps/terminals/kitty/{slug}.conf'] = '\n'.join(kitty) + '\n'
        alacritty = ['[colors.primary]', f'background = "{p["background"]}"', f'foreground = "{p["foreground"]}"',
                     '', '[colors.cursor]', f'text = "{p["background"]}"', f'cursor = "{p["bright_foreground"]}"',
                     '', '[colors.selection]', f'text = "{p["foreground"]}"', f'background = "{p["selection"]}"']
        for section, roles in [('normal', ANSI[:8]), ('bright', ANSI[8:])]:
            alacritty.extend(['', f'[colors.{section}]'])
            alacritty.extend(f'{label} = "{p[role]}"' for label, role in zip(
                ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'), roles))
        files[f'apps/terminals/alacritty/{slug}.toml'] = '\n'.join(alacritty) + '\n'
        variant = 'wave' if mode == 'dark' else 'lotus'
        files[f'apps/neovim/{slug}.lazyvim.lua'] = (
            '-- Generated LazyVim plugin snippet; merge with your existing plugin specs.\n'
            'return {\n'
            '    {\n'
            '        "rebelot/kanagawa.nvim",\n'
            f'        opts = {{ theme = "{variant}", colors = {{ theme = {{ {variant} = {{ ui = {{ bg = "{p["background"]}" }} }} }} }} }},\n'
            '    },\n'
            '    { "LazyVim/LazyVim", opts = { colorscheme = "kanagawa-' + variant + '" } },\n'
            '}\n')
    files['apps/codex/appearance.toml'] = '\n'.join(codex) + '\n'
    files['apps/paseo/index.client.ts'] = (
        '// Generated color-only plugin; edit the shared palettes and generator.\n'
        'import type { PluginClientContext } from "@getpaseo/plugin/client";\n\n'
        'export default function contribute(client: PluginClientContext) {\n'
        '  const themes = ' + json_text(paseo).rstrip() + ' as const;\n'
        '  for (const theme of themes) client.addTheme(theme);\n'
        '  return () => {};\n'
        '}\n')
    files['apps/zeron/package.json'] = json_text({
        'name': 'dot-agents-kanagawa', 'displayName': 'Dot Agents Kanagawa',
        'publisher': 'dot-agents', 'version': '1.0.0',
        'contributes': {'themes': [
            {'id': slug, 'label': name, 'uiTheme': 'vs-dark' if mode == 'dark' else 'vs',
             'path': f'./themes/{slug}.json'}
            for slug, name, mode in PALETTES
        ]},
    })
    files['apps/obsidian/theme.css'] = '\n'.join(obsidian)
    files['platforms/linux-omarchy/obsidian.css.tpl'] = obsidian_template
    theme = {'mode': 1, 'engine': 'dynamicTheme', 'darkColorScheme': 'Default', 'lightColorScheme': 'Default'}
    for mode, p in palettes.items():
        theme[f'{mode}SchemeBackgroundColor'] = p['background']
        theme[f'{mode}SchemeTextColor'] = p['foreground']
    files['apps/darkreader/presets/theme.json'] = json_text({'theme': theme})
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Report stale generated files without writing')
    parser.add_argument('--output', type=Path, default=ROOT, help='Output theme tree; defaults to this repository')
    args = parser.parse_args()
    stale = []
    files = render()
    for relative, content in files.items():
        target = args.output / relative
        data = content if isinstance(content, bytes) else content.encode('utf-8')
        if args.check:
            if not target.exists() or target.read_bytes() != data:
                stale.append(relative)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    if stale:
        parser.exit(1, 'Regenerate stale files:\n' + '\n'.join(stale) + '\n')
    print(f'{"Checked" if args.check else "Generated"} {len(files)} theme files')


if __name__ == '__main__':
    main()
