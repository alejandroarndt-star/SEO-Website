# -*- coding: utf-8 -*-
"""Prueft jeden Artikelkoerper gegen die Regeln aus artikel-regeln.md."""
import io, os, re, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artikel")
bad = 0
for f in sorted(os.listdir(D)):
    if not f.endswith(".html"):
        continue
    s = io.open(os.path.join(D, f), encoding="utf-8").read()
    n = len(s)
    h2 = s.count("<h2>")
    img = s.count("<img")
    alt = len(re.findall(r'<img(?![^>]*\balt="[^"]{15,}")', s))
    links = re.findall(r'href="([^"]+)"', s)
    blog = [l for l in links if not l.startswith("../")]
    dash = len(re.findall(u"[–—]", s))
    h1 = s.count("<h1")
    probs = []
    if not (9500 <= n <= 10500): probs.append("Laenge %d" % n)
    if h2 != 6: probs.append("H2 %d" % h2)
    if img != 4: probs.append("Bilder %d" % img)
    if alt: probs.append("Alt fehlt %d" % alt)
    if not (3 <= len(links) <= 5): probs.append("Links %d" % len(links))
    if len(links) != len(set(links)): probs.append("Link doppelt")
    if len(blog) > 2: probs.append("zu viele Blog-Links %d" % len(blog))
    if dash: probs.append("Gedankenstrich %d" % dash)
    if h1: probs.append("h1 im Koerper")
    if probs:
        bad += 1
        print("%-42s %s" % (f[:-5], ", ".join(probs)))
print("geprueft %d Dateien, %d mit Befund" % (len(os.listdir(D)), bad))
sys.exit(1 if bad else 0)
