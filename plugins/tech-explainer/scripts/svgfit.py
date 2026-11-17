#!/usr/bin/env python3
"""Reports SVG diagram labels that run out of their box.

    python3 svgfit.py page.html [base=13,ttl=14,...]

For each <svg class="dg"> it predicts every <text>'s width in a 0.6em monospace font (Maple Mono and
JetBrains Mono are both 0.6em wide), finds the smallest rect or polygon that holds the label's anchor, and
prints labels that pass that box's edge minus 6px, or the viewBox for a free label. The sizes default to
base.css; pass name=px to override. Expect "labels over: 0".
"""
import re, sys, html
import xml.etree.ElementTree as ET
src = open(sys.argv[1], encoding='utf-8').read()
scale = dict(base=13, ttl=14, big=16, sub=11.5, mono=11.5, eb=11)
if len(sys.argv) > 2:
    for kv in sys.argv[2].split(','):
        k, v = kv.split('='); scale[k] = float(v)
ORDER = ['ttl', 'big', 'sub', 'mono', 'eb']   # later CSS rule wins
PAD = 6
ns = '{http://www.w3.org/2000/svg}'
bad = 0
for si, m in enumerate(re.finditer(r'<svg class="dg[^>]*>.*?</svg>', src, re.S)):
    s = m.group(0).replace('&nbsp;', ' ')
    s = re.sub(r'<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', s, count=1)
    root = ET.fromstring(s)
    vb = [float(v) for v in root.get('viewBox').split()]
    shapes = []
    for r in root.iter(ns + 'rect'):
        x, y, w, h = (float(r.get(k)) for k in 'x y width height'.split())
        shapes.append(('rect', x, y, w, h, r.get('class', '')))
    for p in root.iter(ns + 'polygon'):
        pts = [tuple(map(float, q.split(','))) for q in p.get('points').split()]
        xs = [a for a, b in pts]; ys = [b for a, b in pts]
        shapes.append(('dia', min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys), p.get('class', '')))
    for t in root.iter(ns + 'text'):
        if t.get('x') is None: continue
        cls = t.get('class', '').split()
        size = scale['base']
        for c in ORDER:
            if c in cls: size = scale[c]
        txt = ''.join(t.itertext())
        n = len(txt)
        w = n * 0.6 * size + (n * 0.08 * size if 'eb' in cls else 0)
        x, y = float(t.get('x')), float(t.get('y'))
        a = t.get('text-anchor', 'start')
        x0 = x - w / 2 if a == 'middle' else (x - w if a == 'end' else x)
        x1 = x0 + w
        cy = y - 0.35 * size
        inside = [sh for sh in shapes if sh[1] <= x <= sh[1] + sh[3] and sh[2] <= cy <= sh[2] + sh[4]]
        if inside:
            sh = min(inside, key=lambda q: q[3] * q[4])
            kind, bx, by, bw, bh, bc = sh
            if kind == 'dia':
                mid = by + bh / 2
                ww = bw * (1 - abs(cy - mid) / (bh / 2))
                lo, hi = bx + bw / 2 - ww / 2, bx + bw / 2 + ww / 2
            else:
                lo, hi = bx, bx + bw
            pad = PAD if kind == 'rect' else 2
            over = max(lo + pad - x0, x1 - (hi - pad))
            where = f'{kind} {bc or "plain"} [{lo:.0f},{hi:.0f}]'
        else:
            over = max(vb[0] - x0, x1 - (vb[0] + vb[2]))
            where = 'free (viewBox)'
        if over > 0:
            bad += 1
            print(f'svg{si+1}: over by {over:5.1f}px  size {size}  "{txt}"  in {where}')
print('labels over:', bad)
