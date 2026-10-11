# -*- coding: utf-8 -*-
"""Prueft alle internen Verweise und Bildpfade der ausgelieferten Seiten.
_build/ bleibt aussen vor: dort liegen Textbausteine, keine Seiten, und
ihre relativen Pfade gelten erst nach dem Einbau in blog/."""
import os, re, io, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages = []
for d, dirs, fs in os.walk(root):
    dirs[:] = [x for x in dirs if x not in ('.git', '_build')]
    for f in fs:
        if f.endswith('.html') and not f.startswith('_'):
            pages.append(os.path.relpath(os.path.join(d, f), root))
total, bad = 0, []
for pg in pages:
    s = io.open(os.path.join(root, pg), encoding='utf-8').read()
    base = os.path.dirname(pg)
    for m in re.finditer(r'(?:href|src)="([^"]+)"', s):
        u = m.group(1)
        if u.startswith(('http', 'mailto:', 'tel:', 'data:', '#')):
            continue
        total += 1
        path = u.split('#')[0].split('?')[0]
        if not path:
            continue
        t = os.path.normpath(os.path.join(root, base, path))
        if os.path.isdir(t):
            t = os.path.join(t, 'index.html')
        if not os.path.exists(t):
            bad.append((pg, u))
    for m in re.finditer(r'href="#([^"]+)"', s):
        if 'id="%s"' % m.group(1) not in s:
            bad.append((pg, '#' + m.group(1)))
print('Seiten %d | Verweise %d | defekt %d' % (len(pages), total, len(bad)))
for b in bad[:20]:
    print('   %s -> %s' % b)
sys.exit(1 if bad else 0)
