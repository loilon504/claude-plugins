"""Side-by-side file changes: old on the left, new on the right, line for line.

build.py replaces every placeholder of the form
    <!--@SBS old="path/to/old" new="path/to/new"@-->
with a table. A path is relative to the --root given to build.py (default: the page's folder).
Leave one side empty (old="") for a new file or (new="") for a deleted one. Optional: context="3".
"""
import difflib
import html
import os
import re

PLACEHOLDER = re.compile(r'<!--@SBS\s+([^@]*?)@-->')
ATTR = re.compile(r'(\w+)="([^"]*)"')
TOKEN = re.compile(r'\w+|\s+|[^\w\s]')
LABELS = {
    'vi': dict(old='Cũ', new='Mới', lines='dòng', none='không có', same='dòng giống nhau',
               added='Chưa có file này', removed='Xoá file này'),
    'en': dict(old='Old', new='New', lines='lines', none='none', same='unchanged lines',
               added='New file', removed='File removed'),
}


def esc(s):
    return html.escape(s, quote=False)


def _lines(root, path):
    if not path:
        return None
    with open(os.path.join(root, path), encoding='utf-8') as f:
        return f.read().splitlines()


def _cell(n, text, kind):
    # kind: '' same, 'd' removed, 'a' added, 'e' no line on this side
    if kind == 'e':
        return '<td class="n e"></td><td class="c e"></td>'
    k = f' {kind}' if kind else ''
    return f'<td class="n{k}">{n}</td><td class="c{k}">{text or " "}</td>'


def _similar(a, b):
    return difflib.SequenceMatcher(None, TOKEN.findall(a), TOKEN.findall(b), autojunk=False).ratio()


def _inline(a, b):
    # mark the changed words of a line pair; whole-line marks when they share little
    ta, tb = TOKEN.findall(a), TOKEN.findall(b)
    sm = difflib.SequenceMatcher(None, ta, tb, autojunk=False)
    if sm.ratio() < 0.5:
        return esc(a), esc(b)
    oa, ob = [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        sa, sb = esc(''.join(ta[i1:i2])), esc(''.join(tb[j1:j2]))
        if op == 'equal':
            oa.append(sa); ob.append(sb)
        else:
            if sa: oa.append(f'<span class="x">{sa}</span>')
            if sb: ob.append(f'<span class="x">{sb}</span>')
    return ''.join(oa), ''.join(ob)


def _align(old, new):
    # pair each removed line with the closest added line after the last pair, in order
    pairs, j = [], 0
    for i, line in enumerate(old):
        best = max(range(j, len(new)), key=lambda k: _similar(line, new[k]), default=None)
        if best is not None and _similar(line, new[best]) >= 0.5:
            pairs.append((i, best)); j = best + 1
    return pairs


def _fold(count, a_from, b_from, L):
    return (f'<tr class="fold"><td colspan="4"><span>{count} {L["same"]}'
            f' · {L["old"].lower()} {a_from}–{a_from + count - 1} · {L["new"].lower()} {b_from}–{b_from + count - 1}</span></td></tr>')


def _rows(a, b, context, L):
    rows, plus, minus = [], 0, 0
    if a is None or b is None:
        only, kind = (b, 'a') if a is None else (a, 'd')
        note = L['added'] if a is None else L['removed']
        for i, t in enumerate(only, 1):
            side = _cell(i, esc(t), kind)
            blank = (f'<td class="n e"></td><td class="c e none" rowspan="{len(only)}"><span>{note}</span></td>'
                     if i == 1 else '<td class="n e"></td>')
            rows.append(f'<tr>{blank}{side}</tr>' if a is None else f'<tr>{side}{blank}</tr>')
        return rows, (len(only) if a is None else 0), (len(only) if b is None else 0)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ai = bi = 0
    for g in sm.get_grouped_opcodes(context):
        if g[0][1] > ai:
            rows.append(_fold(g[0][1] - ai, ai + 1, bi + 1, L))
        for op, i1, i2, j1, j2 in g:
            if op == 'equal':
                for k in range(i2 - i1):
                    rows.append('<tr>' + _cell(i1 + k + 1, esc(a[i1 + k]), '') + _cell(j1 + k + 1, esc(b[j1 + k]), '') + '</tr>')
                continue
            na, nb = i2 - i1, j2 - j1
            minus += na; plus += nb
            x = y = 0
            for pi, pj in _align(a[i1:i2], b[j1:j2]) + [(na, nb)]:
                while x < pi or y < pj:
                    left = _cell(i1 + x + 1, esc(a[i1 + x]), 'd') if x < pi else _cell(0, '', 'e')
                    right = _cell(j1 + y + 1, esc(b[j1 + y]), 'a') if y < pj else _cell(0, '', 'e')
                    rows.append(f'<tr>{left}{right}</tr>')
                    x += x < pi; y += y < pj
                if pi < na:
                    ta, tb = _inline(a[i1 + pi], b[j1 + pj])
                    rows.append('<tr>' + _cell(i1 + pi + 1, ta, 'd') + _cell(j1 + pj + 1, tb, 'a') + '</tr>')
                    x, y = pi + 1, pj + 1
        ai, bi = g[-1][2], g[-1][4]
    if ai < len(a):
        rows.append(_fold(len(a) - ai, ai + 1, bi + 1, L))
    return rows, plus, minus


def render(root, old, new, context=3, lang='vi'):
    L = LABELS.get(lang, LABELS['en'])
    a, b = _lines(root, old), _lines(root, new)
    rows, plus, minus = _rows(a, b, context, L)
    la = f'{len(a)} {L["lines"]}' if a is not None else L['none']
    lb = f'{len(b)} {L["lines"]}' if b is not None else L['none']
    stat = f'<span class="stat"><span class="p">+{plus}</span> <span class="m">−{minus}</span></span>'
    return ('<div class="sbs-scroll"><table class="sbs">'
            '<colgroup><col class="cn"><col><col class="cn mid"><col></colgroup>'
            f'<thead><tr><th colspan="2">{L["old"]} · {la}</th><th colspan="2">{L["new"]} · {lb}{stat}</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


def fill(page, root, lang='vi'):
    """Replace every SBS placeholder in page; returns (page, count)."""
    count = 0

    def one(m):
        nonlocal count
        attrs = dict(ATTR.findall(m.group(1)))
        if 'old' not in attrs or 'new' not in attrs:
            raise SystemExit(f'SBS placeholder needs old="" and new="": {m.group(0)}')
        count += 1
        return render(root, attrs['old'], attrs['new'], int(attrs.get('context', 3)), lang)

    return PLACEHOLDER.sub(one, page), count
