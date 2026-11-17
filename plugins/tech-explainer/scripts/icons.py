#!/usr/bin/env python3
"""Finds Nerd Font icons by name, for use as <i class="nf">&#xF14DF;</i>.

    python3 icons.py rocket launch     names holding every word, Material Design (md-) first, outline first
    python3 icons.py --code f14df      the name of a codepoint
    python3 icons.py --all docker      every icon set, not only md-

Prefers the md- set (Material Design, outline style) so a page keeps one icon family. "common" marks icons
in fonts/maple-icons-common.woff2, the set used when fontTools is not installed.
"""
import argparse
import json
import os

FONTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fonts')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('words', nargs='*')
    ap.add_argument('--code', help='hex codepoint to name')
    ap.add_argument('--all', action='store_true', help='search every icon set, not only md-')
    ap.add_argument('-n', type=int, default=25, help='how many to show')
    a = ap.parse_args()

    names = json.load(open(os.path.join(FONTS, 'glyphnames.json'), encoding='utf-8'))
    names.pop('METADATA', None)
    with open(os.path.join(FONTS, 'maple-icons-common.txt'), encoding='utf-8') as f:
        common = {x.upper() for x in f.read().split()}

    if a.code:
        code = a.code.lower().lstrip('u+').lstrip('0x')
        hits = [k for k, v in names.items() if v.get('code', '').lower().lstrip('0') == code.lstrip('0')]
        print('\n'.join(hits) or 'no icon with that codepoint')
        return
    if not a.words:
        ap.error('give words to search, or --code')

    words = [w.lower() for w in a.words]
    hits = [(k, v['code']) for k, v in names.items()
            if all(w in k for w in words) and (a.all or k.startswith('md-'))]
    hits.sort(key=lambda kv: (not kv[0].startswith('md-'), '_outline' not in kv[0], len(kv[0]), kv[0]))
    for k, code in hits[:a.n]:
        mark = 'common' if code.upper() in common else ''
        print(f'{k:40s} &#x{code.upper()};  {mark}')
    if len(hits) > a.n:
        print(f'... {len(hits) - a.n} more (-n to show more)')
    if not hits:
        print('no match; try fewer or shorter words, or --all')


if __name__ == '__main__':
    main()
