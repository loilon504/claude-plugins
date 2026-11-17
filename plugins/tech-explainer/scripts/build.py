#!/usr/bin/env python3
"""Builds a tech-explainer page into one self-contained HTML file.

    python3 build.py page.html out.html [--root DIR] [--lang vi|en]

In order:
  1. <!--@SBS old="..." new="..."@-->  becomes a side-by-side diff table (paths relative to --root,
                                        which defaults to the page's own folder)
  2. /*@BASE@*/                         becomes assets/base.css
  3. /*@FONTS@*/                        becomes the @font-face rules: Maple Mono NF (5 styles), JetBrains
                                        Mono NF (2), and an icon font holding the Nerd Font icons the page uses

Needs only Python 3. With fontTools (pip install fonttools; add brotli for smaller files) the icon font
holds exactly the page's icons. Without it, fonts/maple-icons-common.woff2 is embedded instead and any
icon the page uses that is not in that set is listed.
"""
import argparse
import base64
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
FONTS = os.path.join(SKILL, 'fonts')
sys.path.insert(0, HERE)
import sbs  # noqa: E402

TEXT_FACES = [
    ('Maple Mono NF', 'maple-regular.woff2', '400', 'normal'),
    ('Maple Mono NF', 'maple-medium.woff2', '500', 'normal'),
    ('Maple Mono NF', 'maple-semibold.woff2', '600', 'normal'),
    ('Maple Mono NF', 'maple-bold.woff2', '700', 'normal'),
    ('Maple Mono NF', 'maple-italic.woff2', '400', 'italic'),
    ('JetBrainsMono NF', 'jbmono-regular.woff2', '400', 'normal'),
    ('JetBrainsMono NF', 'jbmono-semibold.woff2', '600', 'normal'),
]
ICON_SOURCE = os.path.join(FONTS, 'maple-mono-nf-regular.ttf')
ICON_FALLBACK = os.path.join(FONTS, 'maple-icons-common.woff2')
VI_LETTERS = set('ăâđêôơưạảãáàặẳẵắằậẩẫấầẹẻẽéèệểễếềịỉĩíìọỏõóòộổỗốồợởỡớờụủũúùựửữứừỵỷỹýỳ')


def face(family, data, mime, fmt, weight, style):
    b = base64.b64encode(data).decode()
    return (f'@font-face {{ font-family: "{family}"; src: url(data:{mime};base64,{b}) format("{fmt}"); '
            f'font-weight: {weight}; font-style: {style}; font-display: swap; }}')


def icons_used(page):
    cps = set()
    for m in re.finditer(r'&#x([0-9A-Fa-f]+);', page):
        cps.add(int(m.group(1), 16))
    for m in re.finditer(r'&#(\d+);', page):
        cps.add(int(m.group(1)))
    cps.update(ord(ch) for ch in page)
    return sorted(c for c in cps if 0xE000 <= c <= 0xF8FF or 0xF0000 <= c <= 0xFFFFD)


def icon_font(cps):
    """Returns (bytes, mime, format, note)."""
    try:
        from fontTools import subset
        from fontTools.ttLib import TTFont
    except ImportError:
        data = open(ICON_FALLBACK, 'rb').read()
        with open(ICON_FALLBACK.replace('.woff2', '.txt'), encoding='utf-8') as f:
            have = {int(x, 16) for x in f.read().split()}
        missing = [f'{c:X}' for c in cps if c not in have]
        note = 'fontTools not installed (pip install fonttools): embedded the common icon set'
        if missing:
            note += f'; NOT in that set, will not show: {", ".join(missing)}'
        return data, 'font/woff2', 'woff2', note
    cmap = TTFont(ICON_SOURCE, lazy=True).getBestCmap()
    missing = [f'{c:X}' for c in cps if c not in cmap]
    opts = subset.Options()
    opts.layout_features = ['*']; opts.name_IDs = ['*']; opts.name_languages = ['*']
    opts.hinting = False; opts.notdef_outline = True; opts.glyph_names = False
    try:
        import brotli  # noqa: F401
        opts.flavor, mime, fmt = 'woff2', 'font/woff2', 'woff2'
    except ImportError:
        opts.flavor, mime, fmt = None, 'font/ttf', 'truetype'
    font = TTFont(ICON_SOURCE)
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=[c for c in cps if c in cmap] + [0x20])
    sub.subset(font)
    font.flavor = opts.flavor
    buf = io.BytesIO(); font.save(buf)
    note = f'icon font: {len(cps) - len(missing)} icons ({fmt})'
    if missing:
        note += f'; NOT in Maple Mono NF, will not show: {", ".join(missing)}'
    return buf.getvalue(), mime, fmt, note


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('page'); ap.add_argument('out')
    ap.add_argument('--root', help='folder the SBS paths are relative to (default: the page folder)')
    ap.add_argument('--lang', choices=['vi', 'en'], help='labels of the diff tables (default: guessed from the page)')
    a = ap.parse_args()

    page = open(a.page, encoding='utf-8').read()
    lang = a.lang or ('vi' if VI_LETTERS & set(page.lower()) else 'en')
    notes = []

    page, n = sbs.fill(page, a.root or os.path.dirname(os.path.abspath(a.page)), lang)
    if n:
        notes.append(f'{n} side-by-side tables ({lang})')

    if '/*@BASE@*/' in page:
        page = page.replace('/*@BASE@*/', open(os.path.join(SKILL, 'assets', 'base.css'), encoding='utf-8').read())
    else:
        notes.append('WARNING: no /*@BASE@*/ marker, base.css not included')

    if '/*@FONTS@*/' in page:
        rules = [face(fam, open(os.path.join(FONTS, f), 'rb').read(), 'font/woff2', 'woff2', w, s)
                 for fam, f, w, s in TEXT_FACES]
        cps = icons_used(page)
        if cps:
            data, mime, fmt, note = icon_font(cps)
            rules.append(face('Maple Mono NF Icons', data, mime, fmt, '100 900', 'normal'))
            notes.append(note)
        page = page.replace('/*@FONTS@*/', '\n'.join(rules))
    else:
        notes.append('WARNING: no /*@FONTS@*/ marker, fonts not embedded')

    if '<title>' not in page[:8192]:
        notes.append('WARNING: no <title> in the first 8 KB')

    with open(a.out, 'w', encoding='utf-8') as f:
        f.write(page)
    print(f'{a.out}: {os.path.getsize(a.out) / 1024:.0f} KB')
    for x in notes:
        print('  ' + x)


if __name__ == '__main__':
    main()
