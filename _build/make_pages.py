# -*- coding: utf-8 -*-
"""Generates every sub page from the shared shell in index.html.
Run after changing the header or footer:  python3 _build/make_pages.py
The generated .html files are what ships; this script is convenience only."""
import io, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_posts import RATGEBER, GEPLANT, META, TITEL, DATUM, THEMEN, THEMEN_NAMEN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
idx = io.open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

def block(start, end, s=idx):
    i = s.index(start); j = s.index(end, i) + len(end)
    return s[i:j]

HEADER = block('<header class="hdr">', '</header>')
MNAV   = block('<div class="mnav">', '</div>\n\n<!-- ============ HERO')[:-len('\n\n<!-- ============ HERO')]
FOOTER = block('<footer class="ftr">', '</footer>')
HEADER = HEADER.replace(' class="active"', '')   # only the homepage marks Start active

def depth_fix(html, d):
    if not d:
        return html
    up = "../" * d
    html = re.sub(r'(href|src)="(?!https?:|#|mailto:|tel:|/)', lambda m: '%s="%s' % (m.group(1), up), html)
    html = re.sub(r'href="#', 'href="%sindex.html#' % up, html)
    return html

SHELL = u"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="icon" href="{up}assets/img/icon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{up}assets/img/icon-180.png">
<link rel="preload" href="{up}assets/fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{up}assets/fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{up}assets/css/site.css">
<meta name="theme-color" content="#0B0B0C">
<noscript><style>.rv{{opacity:1;transform:none}}.serp-row{{opacity:1;transform:none}}</style></noscript>
</head>
<body>
{header}
{mnav}
<main class="page-top"{mainstyle}>
{body}
</main>
{footer}
<script src="{up}assets/js/site.js" defer></script>
</body>
</html>
"""

def page(path, title, desc, body, robots="index,follow", accent=None):
    d = path.count("/")
    up = "../" * d
    ms = u'' if accent is None else u' style="--c:var(--c%d);--c-soft:var(--c%d-soft)"' % (accent, accent)
    html = SHELL.format(title=title, desc=desc, robots=robots, up=up, mainstyle=ms,
                        header=depth_fix(HEADER, d), mnav=depth_fix(MNAV, d),
                        footer=depth_fix(FOOTER, d), body=body)
    out = os.path.join(ROOT, path)
    dirn = os.path.dirname(out)
    if dirn and not os.path.isdir(dirn):
        os.makedirs(dirn)
    io.open(out, "w", encoding="utf-8").write(html)
    print("wrote", path)

ARR = (u'<span class="arr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
       u'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>')

# Unterseiten-Kopf: Marker, zentrierte Zeile, optional eine Schaltflaeche.
HERO_T = u"""<section class="section page-hero" style="padding-top:0">
  <div class="wrap">
    <span class="pill">{kicker}</span>
    <h1 style="font-size:clamp(2rem,4.6vw,3.4rem);max-width:24ch;margin:0 auto">{h1}</h1>
    <p class="lede">{lede}</p>{cta}
  </div>
</section>"""

def hero(kicker, h1, lede, cta_up=None):
    btn = u""
    if cta_up is not None:
        btn = (u'\n    <div class="hero-cta"><a href="%sangebot.html#kontakt" class="btn btn-primary">'
               u'Gratismonat anfragen%s</a></div>' % (cta_up, ARR))
    return HERO_T.format(kicker=kicker, h1=h1, lede=lede, cta=btn)

def cta(up=""):
    return u"""<div class="band" style="margin-top:46px">
      <div class="band-in">
        <h2 style="margin:0 0 14px">Monat eins, 100 %% kostenlos.</h2>
        <p class="lede">Wir drehen, schneiden und veröffentlichen einen Monat lang. Ohne Rechnung, ohne Kündigungsfrist.</p>
        <div class="hero-cta"><a href="%sangebot.html#kontakt" class="btn btn-primary">Gratismonat anfragen<span class="arr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></a></div>
      </div>
    </div>""" % up

CHEV = (u'<span class="acc-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
        u'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></span>')

UMLAUTE = {u"\xe4": u"ae", u"\xf6": u"oe", u"\xfc": u"ue", u"\xdf": u"ss"}

def schlagwort(text):
    """Aus einer Ueberschrift eine Sprungmarke machen. Dieselbe Regel wie in
    site.js, damit Verweise von der Startseite auf die Felder zeigen koennen."""
    t = text.lower()
    for k, v in UMLAUTE.items():
        t = t.replace(k, v)
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:40]

def acc(items, hue=None):
    """items: (nr, titel, unterzeile, inhalt). Das erste Feld ist offen, damit
    die Seite nicht leer wirkt. <details> braucht kein JavaScript.
    hue: fester Farbton fuer alle Felder; ohne ihn traegt jedes seinen eigenen."""
    out = []
    for i, (nr, title, sub, body) in enumerate(items):
        n = hue if hue else ((int(nr) - 1) % 5) + 1
        out.append(u"""
      <details class="acc-item" id="%s"%s style="--c:var(--c%d);--c-soft:var(--c%d-soft)">
        <summary>
          <span class="acc-n">%s</span>
          <span><h2 class="acc-t">%s</h2><span class="acc-s">%s</span></span>
          %s
        </summary>
        <div class="acc-body">%s
        </div>
      </details>""" % (schlagwort(title), u" open" if i == 0 else u"", n, n, nr, title, sub, CHEV, body))
    return u'\n    <div class="acc">%s\n    </div>' % u"".join(out)

# Zwei Gruppen: Social Media zuerst, Suchmaschinenoptimierung dahinter.
# Jede Leistungsseite verweist nur innerhalb ihrer Gruppe weiter, sonst stehen
# auf jeder Seite sieben Querverweise und keiner wird mehr gelesen.
# Social Media ist bewusst EINE Seite, nicht drei: Der Kunde soll auf eine
# Schaltflaeche klicken und dort alles finden, statt sich durch Teilleistungen
# zu arbeiten. Deshalb ist die Liste leer, es gibt nichts zum Querverweisen.
SERVICES_SOCIAL = []
SERVICES_SEO = [
 (1, u"SEO", u"seo.html"),
 (2, u"OnPage und Webdesign", u"onpage-und-webdesign.html"),
 (3, u"Linkaufbau", u"linkaufbau.html"),
 (4, u"SEO Audit", u"seo-audit.html"),
 (5, u"Reporting", u"reporting.html"),
]
SERVICES = SERVICES_SEO   # Rueckwaertsname, falls noch jemand darauf zeigt

def other_services(n, group=None):
    """Querverweise auf die uebrigen Leistungen der Gruppe, je im eigenen Farbton."""
    group = SERVICES_SEO if group is None else group
    rows = u"".join(
        u'\n      <a class="xs-row" href="%s" style="--c:var(--c%d);--c-soft:var(--c%d-soft)">'
        u'<span class="xs-n">0%d</span><span class="xs-t">%s</span>'
        u'<span class="xs-a">%s</span></a>' % (href, i, i, i, name, ARR)
        for i, name, href in group if i != n)
    return u"""
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head" style="max-width:none;align-items:center;text-align:center">
      <h2>Weitere Leistungen</h2>
    </div>
    <div class="xs-list">%s
    </div>
  </div>
</section>""" % rows

def service(path, title, desc, kicker, h1, lede, sections, bullets_title, bullets,
            accent=None, vals_head=u"", vals=(), faq_head=u"", faq=(), subs=(),
            group=None):
    body = hero(kicker=kicker, h1=h1, lede=lede, cta_up="../")

    # Die drei Textbloecke als aufklappbare Felder, erstes offen.
    # Der Farbton kommt von der Seite, nicht vom Feld.
    blocks = acc([(u"%02d" % (i + 1), h, subs[i] if i < len(subs) else u"",
                   u"\n          <p>%s</p>" % t)
                  for i, (h, t) in enumerate(sections)], hue=accent)
    body += u"""
<section class="section" style="padding-top:0">
  <div class="wrap">%s
  </div>
</section>""" % blocks

    # Vier kurze Punkte, wie in der Vorlage unter der Ueberschrift.
    if vals:
        cells = u"".join(u"""
      <div class="val rv"><h3>%s</h3><p>%s</p></div>""" % (h, t) for h, t in vals)
        body += u"""
<section class="section" style="background:var(--bg-2);border-block:1px solid var(--line)">
  <div class="wrap">
    <div class="sec-head" style="max-width:none;align-items:center;text-align:center">
      <h2>%s</h2>
    </div>
    <div class="vals">%s
    </div>
  </div>
</section>""" % (vals_head, cells)

    lis = u"".join(u"\n        <li>%s</li>" % b for b in bullets)
    body += u"""
<section class="section">
  <div class="wrap">
    <div class="checks rv">
      <h2>%s</h2>
      <ul>%s
      </ul>
    </div>
  </div>
</section>""" % (bullets_title, lis)

    if faq:
        qs = u"".join(u"""
      <details class="q"><summary>%s <span class="ic"></span></summary><div class="a">%s</div></details>""" % (q, a)
                      for q, a in faq)
        body += u"""
<section class="section" style="background:var(--bg-2);border-block:1px solid var(--line);padding-bottom:clamp(44px,5vw,72px)">
  <div class="wrap">
    <div class="sec-head" style="max-width:none;align-items:center;text-align:center">
      <h2>%s</h2>
    </div>
    <div class="faq">%s
    </div>
  </div>
</section>""" % (faq_head, qs)

    body += other_services(accent, group)
    body += u"""
<section class="section" style="padding-top:0">
  <div class="wrap">%s
  </div>
</section>""" % cta("../")
    page(path, title, desc, body, accent=accent)

# Die Leistungskarten stehen auf der Startseite und auf der Uebersicht. Hier
# relativ innerhalb von leistungen/, auf der Startseite mit dem Praefix.
SVC = [
 (u"01", u"Social Media Management", u"social-media-management.html",
  u"Dreh, Schnitt, Profil. Alles drin.",
  u"Wir kommen in den Betrieb, filmen einen halben Tag und machen daraus 10 bis 15 geschnittene Reels im Monat. Dazu Untertitel, Bewegtgrafik, Profilpflege und ein Plan, wann was erscheint.",
  u"Was das umfasst"),
 (u"02", u"SEO", u"seo.html",
  u"Gefunden werden, ohne zu zahlen.",
  u"Technik, Seitenstruktur und lokale Sichtbarkeit, damit Ihre Website bei Google auftaucht. Dazu Linkaufbau, Bestandsaufnahme und ein Bericht, der auf eine Seite passt.",
  u"Was das umfasst"),
]
# Die SEO-Leistungen stehen als ruhige Liste unter den Karten.
# seo.html ist selbst eine der zwei Karten, taucht hier also nicht noch einmal auf.
SEO_ROWS = u"".join(
    u'\n      <a class="xs-row" href="%s" style="--c:var(--c%d);--c-soft:var(--c%d-soft)">'
    u'<span class="xs-n">%02d</span><span class="xs-t">%s</span>'
    u'<span class="xs-a">%s</span></a>' % (href, i, i, i, name, ARR)
    for i, name, href in SERVICES_SEO if href != u"seo.html")

SVC_CARDS = u"".join(u"""
      <a class="svc-card" href="%s">
        <span class="svc-num">%s</span>
        <h3>%s</h3>
        <p class="svc-tag">%s</p>
        <p class="svc-txt">%s</p>
        <span class="svc-go">%s</span>
      </a>""" % (href, num, name, tag, txt, go) for num, name, href, tag, txt, go in SVC)

# ---------------------------------------------------------------- Probemonat

# ---------------------------------------------------------------- Kontakt
# EINE Stelle fuer die Buchungsseite. Der Link kommt aus Google Kalender,
# Terminplan -> Teilen. Solange hier der Platzhalter steht, zeigt die Seite
# statt des Kalenders den Hinweis, dass per Mail ein Termin vereinbart wird.
BOOKING_URL = u"BUCHUNGSSEITE_EINTRAGEN"
MAIL = u"alejandroarndt@kontor-seo.de"
TEL_LINK, TEL_TEXT = u"+491771885605", u"+49 177 188 5605"

if BOOKING_URL.startswith(u"http"):
    BOOKING_PANEL = u"""<div class="book" data-booking="%(url)s">
        <span class="kicker">Termin</span>
        <h2>Telefontermin buchen</h2>
        <p class="lede">Zwanzig Minuten, in denen wir uns Ihre Seite gemeinsam ansehen. <strong>Termine finden freitags statt.</strong></p>
        <button class="btn btn-primary book-go" type="button">Freien Freitagstermin wählen%(arr)s</button>
        <p class="book-hint">Mit dem Klick wird der Kalender von Google geladen. Dabei erhält Google Ihre IP-Adresse. Details in der <a href="datenschutz.html">Datenschutzerklärung</a>.</p>
        <p class="book-fallback" hidden>Der Kalender lädt nicht? <a href="%(url)s" target="_blank" rel="noopener">Buchungsseite direkt öffnen</a> oder einfach eine Mail an <a href="mailto:%(mail)s">%(mail)s</a>.</p>
      </div>""" % {"url": BOOKING_URL, "arr": ARR, "mail": MAIL}
else:
    BOOKING_PANEL = u"""<div class="book">
        <span class="kicker">Termin</span>
        <h2>Telefontermin</h2>
        <p class="lede">Zwanzig Minuten, in denen wir uns Ihre Seite gemeinsam ansehen. <strong>Termine finden freitags statt.</strong></p>
        <p class="book-hint">Die Online-Buchung wird gerade eingerichtet. Schreiben Sie uns bis dahin kurz an <a href="mailto:%(mail)s">%(mail)s</a>, wir schlagen Ihnen einen Freitagstermin vor.</p>
      </div>""" % {"mail": MAIL}

page("angebot.html",
 u"Erster Monat kostenlos | Kontor",
 u"Ein Monat Social Media ohne Rechnung: 10 bis 15 geschnittene Reels und Profilbetreuung. Keine Frist, keine stillschweigende Verlängerung.",
 hero(kicker=u"Zum Start",
   h1=u"Der erste Monat kostet nichts.",
   lede=u"Wir produzieren einen Monat lang Ihre Inhalte, Sie sehen am Ergebnis, ob es für Sie passt. Ohne Rechnung, ohne Anzahlung, ohne Kündigungsfrist.",
   cta_up="") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap offer">
    <div class="offer-art">
      <div class="phones" role="img" aria-label="Zwei Smartphones zeigen senkrechte Kurzvideos nebeneinander, links Instagram, rechts TikTok">
        <div class="phone phone-ig">
          <div class="phone-screen">
            <video autoplay muted loop playsinline preload="metadata" width="400" height="868"
                   poster="assets/video/reel-instagram.jpg">
              <source src="assets/video/reel-instagram.mp4" type="video/mp4">
              <source src="assets/video/reel-instagram.webm" type="video/webm">
            </video>
            <span class="phone-island"></span>
          </div>
        </div>
        <div class="phone phone-tt">
          <div class="phone-screen">
            <video autoplay muted loop playsinline preload="metadata" width="400" height="868"
                   poster="assets/video/reel-tiktok.jpg" data-versatz="2.4">
              <source src="assets/video/reel-tiktok.mp4" type="video/mp4">
              <source src="assets/video/reel-tiktok.webm" type="video/webm">
            </video>
            <span class="phone-island"></span>
          </div>
        </div>
      </div>
    </div>
    <div class="offer-txt">
      <h2 style="margin:0">Das ist enthalten</h2>
      <ul class="offer-list">
        <li><strong>Ein halber Drehtag bei Ihnen</strong><span>Vier bis fünf Stunden in Ihrem Betrieb. Wir filmen Ihre Arbeit, Ihre Räume und ein paar Sätze von Ihnen. Sie arbeiten dabei normal weiter.</span></li>
        <li><strong>10 bis 15 fertige Reels</strong><span>Geschnitten auf den Ton, mit von Hand geprüften Untertiteln und Bewegtgrafik, wo sie etwas erklärt. Im Hochformat, auf Wunsch zusätzlich quadratisch.</span></li>
        <li><strong>Profil eingerichtet und gepflegt</strong><span>Profiltext, Profilbild, Kontaktwege, Titelbilder und ein Plan, wann was erscheint. Falls noch kein Profil besteht, richten wir es ein.</span></li>
        <li><strong>Eine Korrekturschleife je Reel</strong><span>Sie sehen jedes Video, bevor es online geht, und sagen einmal, was anders soll.</span></li>
        <li><strong>Alle Dateien gehören Ihnen</strong><span>Fertige Videos und Rohaufnahmen bekommen Sie mitgeliefert, auch wenn wir danach nicht weiterarbeiten.</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="section" style="background:var(--bg-2);border-block:1px solid var(--line)">
  <div class="wrap">
    <div class="checks">
      <h2>Was danach passiert</h2>
      <ul>
        <li>Am Ende des Monats sehen wir uns gemeinsam die Zahlen aus Ihrem eigenen Konto an: Aufrufe, gespeicherte Videos, Profilaufrufe.</li>
        <li>Erst dann nennen wir einen Preis für die weitere Zusammenarbeit, weil erst dann beide wissen, wie viel Arbeit Ihr Betrieb tatsächlich macht.</li>
        <li>Es gibt keine stillschweigende Verlängerung. Melden Sie sich nicht, läuft das Angebot aus und es kommt keine Rechnung.</li>
        <li>Für den Probemonat entsteht keine Forderung, auch nicht rückwirkend, wenn Sie danach ablehnen.</li>
        <li>Ihre Zugänge bleiben bei Ihnen. Das Konto läuft auf Ihren Namen, nicht auf unseren.</li>
      </ul>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head" style="max-width:none;align-items:center;text-align:center">
      <h2>Warum wir das machen</h2>
    </div>
    <div class="prose" style="max-width:68ch;margin:0 auto">
      <p>Kontor ist als Social-Media-Dienstleister neu. Wir können Ihnen deshalb keine Arbeitsproben aus laufenden Kundenprojekten zeigen, und wir halten nichts davon, das mit Versprechen zu überdecken. Stattdessen liefern wir einen Monat und Sie entscheiden am Ergebnis.</p>
      <p>Für uns rechnet sich das, weil ein Betrieb, der vier Wochen lang gesehen hat, wie regelmäßige Videos wirken, in der Regel weitermacht. Für Sie rechnet es sich, weil Ihr Risiko bei null liegt: Sie investieren einen halben Tag Ihrer Zeit, sonst nichts.</p>
      <p>Ein Hinweis zur Ehrlichkeit: Wir können nicht versprechen, wie viele Aufrufe Ihre Videos bekommen. Über die Ausspielung entscheiden die Plattformen, nicht wir. Was wir zusagen können, ist die Arbeit: die Anzahl der Videos, die Qualität des Schnitts und dass wir den Monat durchhalten.</p>
    </div>
  </div>
</section>

<section class="section" style="background:var(--bg-2);border-block:1px solid var(--line)">
  <div class="wrap">
    <div class="sec-head" style="max-width:none;align-items:center;text-align:center">
      <h2>Für wen das passt</h2>
    </div>
    <div class="vals">
      <div class="val"><h3>Sichtbare Arbeit</h3><p>Handwerk, Praxen, Gastronomie, Studios: überall dort, wo sich das Ergebnis zeigen lässt, funktioniert das Format am schnellsten.</p></div>
      <div class="val"><h3>Festes Einzugsgebiet</h3><p>Die Plattformen spielen Inhalte bevorzugt in der Umgebung aus. Für Betriebe mit lokaler Kundschaft ist das genau die richtige Reichweite.</p></div>
      <div class="val"><h3>Profil vorhanden, aber still</h3><p>Am schnellsten geht es bei Betrieben, die schon ein Profil haben und dort wenig zurückbekommen. Die Hürde ist dann nur noch der Schnitt.</p></div>
      <div class="val"><h3>Ein halber Tag frei</h3><p>Mehr brauchen wir nicht. Aber den brauchen wir, und er sollte an einem Tag liegen, an dem ohnehin gearbeitet wird.</p></div>
    </div>
  </div>
</section>

<section class="section" style="padding-bottom:clamp(44px,5vw,72px)">
  <div class="wrap">
    <div class="sec-head" style="max-width:none;align-items:center;text-align:center">
      <h2>Häufige Fragen</h2>
    </div>
    <div class="faq">
      <details class="q"><summary>Wo ist der Haken? <span class="ic"></span></summary><div class="a">Es gibt keinen versteckten. Der offene ist: Wir hoffen, dass Sie danach weitermachen. Wenn nicht, behalten Sie trotzdem alle Videos und Rohaufnahmen, und es kommt keine Rechnung. Es gibt keine Klausel, die sich automatisch verlängert, und keine Anzahlung.</div></details>
      <details class="q"><summary>Wie viele Betriebe nehmen Sie gleichzeitig? <span class="ic"></span></summary><div class="a">Zwei bis drei Probemonate parallel, nicht mehr. Ein Probemonat ist ein voller Arbeitsmonat, und mehrere gleichzeitig ließen sich nicht in der Qualität liefern, auf die es gerade ankommt. Wenn gerade alle Plätze belegt sind, sagen wir das und melden uns, sobald einer frei wird.</div></details>
      <details class="q"><summary>Muss ich vor die Kamera? <span class="ic"></span></summary><div class="a">Nein. Es wirkt mit Ihnen im Bild meist besser, geht aber auch ohne: Hände bei der Arbeit, Räume, Abläufe, fertige Ergebnisse. Viele der erfolgreichsten Reels in Handwerk und Gastronomie zeigen überhaupt kein Gesicht.</div></details>
      <details class="q"><summary>Was muss ich liefern? <span class="ic"></span></summary><div class="a">Einen halben Tag Zugang zu Ihrem Betrieb und das Fachliche: was gemacht wird, was daran besonders ist, was Kunden immer wieder fragen. Texte, Schnitt und Planung kommen von uns.</div></details>
      <details class="q"><summary>Und wenn mir das Ergebnis nicht gefällt? <span class="ic"></span></summary><div class="a">Dann sagen Sie ab. Sie zahlen nichts und behalten die Dateien. Falls Ihnen während des Monats etwas nicht gefällt, sagen Sie es früh: Dafür ist die Korrekturschleife je Video da, und ein Probemonat ist genau der richtige Zeitpunkt, um Geschmack und Tonfall abzugleichen.</div></details>
      <details class="q"><summary>Machen Sie auch Suchmaschinenoptimierung? <span class="ic"></span></summary><div class="a">Ja, das war unser Ausgangspunkt und bleibt im Angebot. Beschrieben ist es unter <a href="leistungen/seo.html">SEO</a>, die Bestandsaufnahme davor unter <a href="leistungen/seo-audit.html">SEO Audit</a>.</div></details>
    </div>
  </div>
</section>
""" + u"""
<section class="section" id="kontakt" style="padding-top:0">
  <div class="wrap serp-grid">
    <div class="prose">
      <h2 style="margin-top:0">Direkt erreichbar</h2>
      <p><strong>E-Mail:</strong> <a href="mailto:%(mail)s">%(mail)s</a><br>
         <strong>Telefon:</strong> <a href="tel:%(tel_link)s">%(tel_text)s</a></p>
      <h3>Was wir dafür brauchen</h3>
      <ul>
        <li>Ihren Betrieb</li>
        <li>Ihr Ort oder Einzugsgebiet</li>
        <li>Die zwei bis drei Leistungen, die Sie zeigen wollen</li>
      </ul>
      <p>Antwort in der Regel innerhalb eines Werktags.</p>
    </div>
    <div>
      <!-- Der Kalender wird erst nach einem Klick geladen. Vorher geht keine
           Anfrage an Google, damit die Aussage in der Datenschutzerklaerung
           ("keine Inhalte Dritter") fuer alle gilt, die nicht buchen wollen. -->
      %(panel)s
    </div>
  </div>
</section>""" % {"mail": MAIL, "tel_link": TEL_LINK, "tel_text": TEL_TEXT, "panel": BOOKING_PANEL}, accent=1)

# ---------------------------------------------------------------- Social-Media-Leistungen

service("leistungen/social-media-management.html",
 u"Social Media Management | Kontor",
 u"Dreh vor Ort, Schnitt, Untertitel und Profilbetreuung aus einer Hand. 10 bis 15 Reels im Monat, erster Monat kostenlos.",
 u"Leistung 01", u"Social Media Management.",
 u"Ein halber Drehtag bei Ihnen, der Rest passiert bei uns: Schnitt, Untertitel, Grafik, Profilpflege und ein Plan, wann was erscheint. Sie müssen nichts können außer Ihren Beruf.",
 [(u"Dreh vor Ort",
   u"Wir kommen mit einer Kamera, einem Gimbal und einem Mikrofon, nicht mit einem Team und Scheinwerfern. Vier bis fünf Stunden genügen für das Material eines ganzen Monats, und Sie arbeiten dabei normal weiter. Aufgenommen wird dreierlei: Ihre Arbeit in Nahaufnahme, also Hände, Werkzeug und die Schritte eines Auftrags. Dann Sie selbst, wie Sie ein paar Sätze sagen, ohne Skript. Und Ihre Räume als ruhige Bilder zum Verbinden. Ihre Kundschaft wird nicht gefilmt, außer sie ist ausdrücklich einverstanden. Wer lieber selbst dreht, bekommt von uns eine Anleitung und spart den Drehtag."),
  (u"Schnitt",
   u"Jeder Schnitt sitzt auf einem Einsatz in der Tonspur. Das klingt nach Kleinigkeit und ist der Unterschied zwischen einem Video, das man zu Ende sieht, und einem, bei dem man wegwischt. Aus zwanzig Minuten Rohmaterial werden sechzig Sekunden, und das Weglassen ist die eigentliche Arbeit. Tempo, Reihenfolge und vor allem der Anfang entscheiden mehr als die Kameraqualität: Wer in den ersten zwei Sekunden erklärt, wer er ist, hat schon verloren."),
  (u"Untertitel und Grafik",
   u"Der größte Teil der Kurzvideos wird ohne Ton angesehen, im Zug, im Wartezimmer, nebenbei. Ohne Untertitel ist Ihr Video für diese Menschen stumm. Wir setzen sie Wort für Wort und prüfen jede Zeile von Hand nach, weil automatische Untertitel Fachbegriffe und Eigennamen zuverlässig falsch schreiben und nichts schneller unseriös wirkt als der eigene Firmenname in falscher Schreibweise. Bewegtgrafik kommt dort dazu, wo sie etwas erklärt: ein Arbeitsschritt, eine Zahl, ein Preis. Keine Effekte, die nur zeigen sollen, dass jemand ein Schnittprogramm bedienen kann."),
  (u"Profil und Plan",
   u"Gute Videos in einem ungepflegten Profil bringen wenig. Wer über ein Reel auf Ihr Profil kommt, entscheidet dort in Sekunden, ob er folgt oder anruft. Deshalb gehören Profilbild, Beschreibung, antippbare Telefonnummer, Adresse und Öffnungszeiten dazu, ebenso Titelbilder, damit der Feed als Ganzes lesbar bleibt. Und ein Plan für den ganzen Monat, was wann erscheint. Das ist weniger aufregend als spontane Einfälle und der einzige Grund, warum ein Profil nach drei Monaten noch lebt."),
  (u"Veröffentlichung und Zahlen",
   u"Sie bekommen die fertigen Dateien, auf Wunsch stellen wir selbst ein. Eine Korrekturschleife je Reel ist enthalten, bevor etwas online geht. Einmal im Monat sehen wir in die Statistiken Ihres eigenen Kontos: Aufrufe, gespeicherte Videos, Profilaufrufe. Gespeicherte Videos sind dabei aussagekräftiger als Aufrufe, weil Speichern eine Absicht zeigt. Daraus leiten wir ab, welche Art von Video bei Ihrer Kundschaft ankommt, und richten den Folgemonat danach aus."),
  (u"Was nicht enthalten ist",
   u"Damit es hinterher keinen Streit gibt, steht das hier und nicht im Kleingedruckten. Nicht enthalten sind: das Beantworten von Kommentaren und Nachrichten, weil das Kundenkontakt ist und fachlich von Ihnen kommen muss. Bezahlte Werbung. Das Betreuen von mehr als zwei bis drei Profilen gleichzeitig. Und alles, was wir nicht zusagen können: Wie oft ein Video ausgespielt wird, entscheidet die Plattform, nicht wir. Zusagen beziehen sich auf die Arbeit, also Anzahl, Schnitt und dass der Monat durchgehalten wird.")],
 u"Was Sie bekommen",
 [u"Ein halber Drehtag im Monat in Ihrem Betrieb, oder eine Anleitung, wenn Sie selbst drehen",
  u"10 bis 15 fertige Reels im Monat, im Hochformat, auf Wunsch zusätzlich quadratisch",
  u"Untertitel in jedem Video, von Hand nachgeprüft",
  u"Profil eingerichtet und gepflegt, dazu ein Monatsplan",
  u"Eine Korrekturschleife je Reel, bevor etwas online geht",
  u"Monatlicher Blick in die Statistiken Ihres eigenen Kontos",
  u"Fertige Videos und Rohaufnahmen gehören Ihnen, auch wenn wir danach nicht weiterarbeiten",
  u"Keine Mindestlaufzeit, keine stillschweigende Verlängerung"],
 accent=1,
 vals_head=u"Woran ein Reel scheitert",
 vals=[(u"Kein Anfang", u"Die ersten zwei Sekunden entscheiden. Wer dort erklärt, wer er ist, hat schon verloren."),
       (u"Kein Ton", u"Ohne Untertitel ist das Video für die Mehrheit stumm, egal wie gut der Inhalt ist."),
       (u"Kein Ende", u"Ein Video ohne nächsten Schritt bringt Aufrufe und keine Anfragen."),
       (u"Kein Durchhalten", u"Drei Wochen und dann Funkstille ist der Normalfall. Genau dagegen gibt es den Plan.")],
 faq_head=u"Häufige Fragen",
 faq=[(u"Was kostet das?",
       u"Der erste Monat nichts, siehe <a href=\"../angebot.html\">Probemonat</a>. Danach ein fester Monatsbetrag für einen klar beschriebenen Umfang, den wir am Ende des Probemonats nennen, wenn beide wissen, wie viel Arbeit Ihr Betrieb tatsächlich macht. Keine Mindestlaufzeit."),
      (u"Welche Plattformen?",
       u"In der Regel zwei: Instagram und TikTok. Beide spielen Kurzvideos auch an Menschen aus, die Ihnen nicht folgen, und beide bevorzugen Inhalte aus der Umgebung. Facebook kommt dazu, wenn Ihre Kundschaft dort ist. Mehr als zwei bis drei Profile gleichzeitig sind für einen Betrieb nicht sinnvoll zu pflegen."),
      (u"Muss ich vor die Kamera?",
       u"Nein. Mit Ihnen im Bild wirkt es meist besser, geht aber auch ohne: Hände bei der Arbeit, Räume, Abläufe, fertige Ergebnisse. Viele der erfolgreichsten Reels in Handwerk und Gastronomie zeigen überhaupt kein Gesicht."),
      (u"Brauche ich schon Follower?",
       u"Nein, und das ist der eigentliche Grund für dieses Format. Ein Betrieb mit zweihundert Followern kann ein Video mit zwanzigtausend Aufrufen haben. Bei Fotobeiträgen funktioniert das nicht."),
      (u"Wem gehören Konto und Videos?",
       u"Ihnen, beides. Das Konto läuft auf Ihren Namen, die Zugänge bleiben bei Ihnen, und die Dateien bekommen Sie mitgeliefert. Beim Wechsel oder beim Aufhören verlieren Sie nichts."),
      (u"Und wenn ich zusätzlich bei Google gefunden werden will?",
       u"Dann kommt <a href=\"seo.html\">SEO</a> dazu. Beides aus einer Hand ist möglich und sinnvoll, weil dieselben Aufnahmen auch auf der Website und im Google-Profil getragen werden.")],
 subs=[u"Vier bis fünf Stunden, Betrieb läuft weiter", u"Auswahl, Reihenfolge, Tempo",
       u"Wort für Wort, von Hand geprüft", u"Profil, Titelbilder, Monatsplan",
       u"Dateien, Korrekturschleife, Statistiken", u"Ausdrücklich draußen"],
 group=SERVICES_SOCIAL)

# ---------------------------------------------------------------- Leistungen overview
page("leistungen/index.html",
 u"Leistungen | Kontor",
 u"Reels, Profilbetreuung und Dreh vor Ort f\u00fcr lokale Betriebe. Suchmaschinenoptimierung ebenfalls im Angebot.",
 hero(kicker=u"Leistungen",
   h1=u"Leistungen",
   lede=u"Der Schwerpunkt liegt auf Kurzvideos, weil sie auch Menschen erreichen, die Ihnen nicht folgen. Suchmaschinenoptimierung bleibt im Angebot f\u00fcr alle, die zus\u00e4tzlich \u00fcber Google gefunden werden wollen.",
   cta_up="../") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="svc-grid">%s
    </div>

    <div class="sec-head" style="max-width:none;align-items:center;text-align:center;margin-top:clamp(44px,6vw,76px)">
      <h2 style="margin:0">Im SEO-Paket enthalten</h2>
      <p class="lede" style="margin-top:12px">Die Teilbereiche im Einzelnen. Jeder davon ist auch allein beauftragbar.</p>
    </div>
    <div class="xs-list">%s
    </div>

    <div class="prose" style="max-width:none">%s</div>
  </div>
</section>""" % (SVC_CARDS, SEO_ROWS, cta("../")))

service("leistungen/seo.html",
 u"SEO | Kontor",
 u"Technik, Inhalte und lokale Sichtbarkeit als ein Paket. Die Grundlage für bessere Positionen bei Google.",
 u"Leistung 01", u"SEO.",
 u"Technik, Inhalte und lokale Sichtbarkeit hängen zusammen. Wir trennen sie nicht in Pakete, sondern arbeiten an dem, was bei Ihnen den Unterschied macht.",
 [(u"Technik",
   u"Ladezeit und Core Web Vitals, die Darstellung auf dem Handy, saubere Weiterleitungen, eine nachvollziehbare URL Struktur und eine Sitemap, die stimmt. Technische Fehler wirken wie eine Bremse auf alles andere: wer Inhalte produziert, während die Hälfte der Seiten nicht im Index ist, zahlt für Arbeit, die nicht ankommt."),
  (u"Inhalte",
   u"Google rankt keine Unternehmen, sondern einzelne Seiten. Für jeden Suchbegriff, der Anfragen bringt, braucht es eine Seite, die genau diese Frage beantwortet. Die häufigste Schwachstelle ist eine einzige Leistungsseite, auf der alles gleichzeitig steht."),
  (u"Lokale Sichtbarkeit",
   u"Bei jeder Suche mit Ortsbezug zeigt Google zuerst drei Einträge mit Karte und Telefonnummer. Darüber läuft ein großer Teil der Anrufe, bevor jemand die normalen Treffer sieht. Das Google Unternehmensprofil ist kostenlos und bei vielen Unternehmen der schnellste Hebel.")],
 u"Typische Funde", [
  u"Seiten, die durch robots.txt oder noindex versehentlich blockiert sind",
  u"Bilder in Originalgröße, die die Ladezeit auf dem Handy verdoppeln",
  u"Mehrere URLs mit demselben Inhalt, die sich gegenseitig Konkurrenz machen",
  u"Eine Leistungsseite, die zehn Themen gleichzeitig abdecken soll",
  u"Ein Unternehmensprofil mit abweichender Adresse oder Telefonnummer"], accent=1,
 subs=[u'Ladezeit, Indexierung, saubere Weiterleitungen', u'Eine Seite je Suchbegriff statt einer für alles', u'Das Unternehmensprofil, oft der schnellste Hebel'],
 vals_head=u'Was sich dadurch ändert',
 vals=[
   (u'Gefunden, wo gesucht wird', u'Nicht mehr Besucher irgendwoher, sondern die, die genau Ihre Leistung eingegeben haben.'),
   (u'Weniger Abhängigkeit von Anzeigen', u'Was organisch steht, bringt auch in einem Monat ohne Werbebudget Anfragen.'),
   (u'Eine Seite, die schneller lädt', u'Arbeit an Ladezeit und Darstellung auf dem Handy merkt jeder Besucher, nicht nur Google.'),
   (u'Nachvollziehbare Entwicklung', u'Positionen und Klicks stehen in der Search Console. Sie sehen, was passiert, nicht nur, dass gearbeitet wird.')],
 faq_head=u'Fragen zu SEO',
 faq=[
   (u'Wie lange dauert es, bis sich etwas zeigt?', u'Technische Verbesserungen und das Unternehmensprofil wirken oft innerhalb weniger Wochen. Bei umkämpften Suchbegriffen sind drei bis sechs Monate realistisch.'),
   (u'Können Sie Position 1 garantieren?', u'Nein. Niemand kann das, weil niemand außer Google über die Reihenfolge entscheidet. Wer es trotzdem zusagt, verkauft Ihnen etwas, das er nicht halten kann.'),
   (u'Muss ich dafür meine Website neu bauen?', u'Meistens nicht. In den allermeisten Fällen lässt sich mit der vorhandenen Seite arbeiten. Wenn ein Neubau wirklich der günstigere Weg ist, sagen wir das offen, bevor Sie Geld ausgeben.')])

service("leistungen/onpage-und-webdesign.html",
 u"OnPage und Webdesign | Kontor",
 u"Aufbau, Gestaltung und Texte der Seiten, die ranken sollen. Struktur, interne Verlinkung und Suchabsicht.",
 u"Leistung 02", u"OnPage und Webdesign.",
 u"Eine Seite muss zwei Dinge gleichzeitig können: von Google richtig eingeordnet werden und den Besucher zur Anfrage bringen. Das eine ohne das andere bringt nichts.",
 [(u"Struktur vor Gestaltung",
   u"Wie eine Seite aufgebaut ist, entscheidet mehr über die Position als ihr Aussehen. Überschriftenhierarchie, interne Verlinkung und eine Gliederung, die der Suchabsicht folgt, sind die Arbeit, die unter der Oberfläche passiert."),
  (u"Gestaltung, die zur Anfrage führt",
   u"Besucher auf der Seite zu haben, ist nur der halbe Weg. Telefonnummer sichtbar und antippbar, ein klarer nächster Schritt, kurze Formulare und Ladezeiten, die auf dem Handy keine Geduld verlangen."),
  (u"Suchabsicht vor Suchvolumen",
   u"Ein Begriff mit tausend Suchen im Monat ist wertlos, wenn die Leute dahinter nur vergleichen. Ein Begriff mit dreißig Suchen kann Aufträge bringen, wenn dahinter konkreter Bedarf steht. Wir sortieren nach dem, was Anfragen auslöst.")],
 u"Was Sie bekommen", [
  u"Eine Keyword Zuordnung: welcher Begriff auf welche Seite gehört",
  u"Titel und Beschreibungen, die auch angeklickt werden",
  u"Vorschläge für fehlende Seiten statt längerer Texte auf bestehenden",
  u"Interne Links von den starken auf die wichtigen Seiten",
  u"Gestaltung und Aufbau der Seiten, die Anfragen bringen sollen"], accent=2,
 subs=[u'Überschriften, interne Links, Gliederung', u'Ein sichtbarer nächster Schritt statt nur Besuch', u'Dreißig Suchen mit Bedarf schlagen tausend ohne'],
 vals_head=u'Was dabei entsteht',
 vals=[
   (u'Eine Seite je Suchabsicht', u'Statt einer Leistungsseite, auf der alles gleichzeitig steht, eine Seite pro Frage, die Anfragen bringt.'),
   (u'Titel, die angeklickt werden', u'Position allein reicht nicht. Titel und Beschreibung entscheiden, wer von den Suchenden tatsächlich klickt.'),
   (u'Interne Links mit Richtung', u'Die starken Seiten geben ihre Kraft an die wichtigen weiter, statt sie zufällig zu verteilen.'),
   (u'Ein sichtbarer nächster Schritt', u'Telefonnummer antippbar, kurzes Formular, klarer Abschluss. Besucher ohne Anfrage sind nur halb gewonnen.')],
 faq_head=u'Fragen zu OnPage und Webdesign',
 faq=[
   (u'Arbeiten Sie mit meinem bestehenden System?', u'Ja. WordPress, Shopify, Webflow, Typo3 oder eine selbst gebaute Seite – gearbeitet wird an dem, was da ist. Ein Systemwechsel ist nur dann ein Thema, wenn er sich unabhängig von SEO lohnt.'),
   (u'Schreiben Sie die Texte selbst?', u'Auf Wunsch ja. Häufiger ist der bessere Weg, dass Sie das Fachliche liefern und wir Struktur, Überschriften und Suchbegriffe einarbeiten. Sie kennen Ihr Geschäft besser.'),
   (u'Leidet das Design, wenn es für Google gebaut wird?', u'Nein. Die Arbeit liegt in Struktur, Reihenfolge und Technik, nicht darin, Text mit Suchbegriffen zu füllen. Eine Seite, die nach SEO aussieht, ist falsch gebaut.')])

service("leistungen/linkaufbau.html",
 u"Linkaufbau | Kontor",
 u"Erwähnungen und Verlinkungen aus Quellen, die tatsächlich zählen. Ohne gekaufte Linknetzwerke.",
 u"Leistung 03", u"Linkaufbau.",
 u"Links von anderen Seiten sind weiterhin einer der stärksten Faktoren. Entscheidend ist nicht die Anzahl, sondern woher sie kommen.",
 [(u"Was zählt",
   u"Ein Link aus einem regionalen Nachrichtenportal, einem Branchenverband, einem Partnerunternehmen oder einem Fachbeitrag. Also Quellen, bei denen eine Erwähnung auch ohne SEO Sinn ergeben würde."),
  (u"Was schadet",
   u"Gekaufte Links aus Netzwerken, Verzeichnisse ohne eigenen Zweck und maschinell verteilter Tausch in großer Zahl. Das lässt sich erkennen, und der Schaden trifft die gesamte Domain. Wir machen das nicht, auch nicht auf Wunsch. Ein einzelner Tausch mit einem Betrieb, dessen Thema tatsächlich zu Ihrem passt, ist etwas anderes: Dort ergibt die Erwähnung auch für dessen Leser Sinn."),
  (u"Realistische Erwartung",
   u"Linkaufbau ist der langsamste Bereich. Vor den anderen lohnt er sich selten. Wenn Technik, Inhalte und lokale Präsenz stehen und es trotzdem nicht reicht, ist dies der nächste Schritt.")],
 u"Wie wir arbeiten", [
  u"Analyse, welche Quellen Ihre Wettbewerber verlinken",
  u"Suche nach Betrieben, die thematisch passen und selbst eine sichtbare Seite haben",
  u"Persönliche Ansprache mit einem konkreten Vorschlag: Verlinkung untereinander oder ein Gastartikel, den wir schreiben",
  u"Erwähnungen Ihres Namens ohne Link finden und nachträglich verlinken lassen",
  u"Partner, Lieferanten und Verbände, bei denen ein Eintrag ohnehin naheliegt"], accent=3,
 subs=[u'Quellen, bei denen eine Erwähnung Sinn ergibt', u'Gekaufte Netzwerke treffen die ganze Domain', u'Der langsamste Bereich, deshalb zuletzt'],
 vals_head=u'Woran wir Qualität messen',
 vals=[
   (u'Themenbezug', u'Ein Link aus dem eigenen Umfeld zählt mehr als zehn aus einem beliebigen Verzeichnis.'),
   (u'Erreichbarkeit der Quelle', u'Seiten, die selbst Besucher haben. Über einen guten Link kommen auch Menschen, nicht nur Signale.'),
   (u'Dauerhaftigkeit', u'Ein Link, der in einem Jahr noch steht. Gemietete Links verschwinden, sobald nicht mehr gezahlt wird.'),
   (u'Natürliches Wachstum', u'Gleichmäßig statt in Schüben. Hundert Links in einer Woche sind ein Muster, das auffällt.')],
 faq_head=u'Fragen zum Linkaufbau',
 faq=[
   (u'Kaufen Sie Links?', u'Nein, auch nicht auf Wunsch. Gekaufte Links aus Netzwerken lassen sich erkennen, und der Schaden trifft die gesamte Domain, nicht nur die verlinkte Seite.'),
   (u'Wie viele Links pro Monat?', u'Keine feste Zahl. Eine Zusage über Stückzahlen lässt sich nur einhalten, indem man Links kauft. Gearbeitet wird an Gelegenheiten, die es tatsächlich gibt.'),
   (u'Wann lohnt sich Linkaufbau?', u'Zuletzt. Wenn Technik, Inhalte und lokale Präsenz stehen und es trotzdem nicht reicht. Davor ist der Hebel fast immer woanders größer.')])

service("leistungen/seo-audit.html",
 u"SEO Audit | Kontor",
 u"Vollständige Bestandsaufnahme Ihrer Website: was blockiert, was Potenzial hat, in welcher Reihenfolge.",
 u"Leistung 04", u"SEO Audit.",
 u"Eine vollständige Bestandsaufnahme, bevor irgendetwas umgesetzt wird. Auch einzeln beauftragbar, ohne laufende Betreuung und ohne Folgeauftrag.",
 [(u"Was drin steht",
   u"Technischer Zustand, Inhalte und Suchbegriffe, lokale Präsenz, Verlinkung und ein direkter Vergleich mit drei Wettbewerbern. Am Ende eine nach Wirkung sortierte Liste, keine Sammlung von Hinweisen."),
  (u"Für wen sich das lohnt",
   u"Für Unternehmen, die wissen wollen, woran sie sind, bevor sie ein Budget binden. Und für alle, die bereits mit einer Agentur arbeiten und eine unabhängige zweite Meinung möchten."),
  (u"Was danach passiert",
   u"Nichts, wenn Sie das so wollen. Das Audit gehört Ihnen, Sie können es intern oder mit einem anderen Dienstleister umsetzen.")],
 u"Umfang", [
  u"Vollständiger Crawl der Website",
  u"Auswertung von Search Console und Ladezeitdaten",
  u"Keyword Zuordnung und Lücken im Vergleich zum Wettbewerb",
  u"Prüfung des Google Unternehmensprofils und der Verzeichnisse",
  u"Priorisierte Maßnahmenliste mit Aufwandseinschätzung"], accent=4,
 subs=[u'Technik, Inhalte, lokal, Links, drei Wettbewerber', u'Bevor ein Budget gebunden wird', u'Nichts, wenn Sie das so wollen'],
 vals_head=u'Was Sie am Ende in der Hand haben',
 vals=[
   (u'Eine priorisierte Liste', u'Nach Wirkung sortiert, nicht nach Reihenfolge des Findens. Oben steht, was am meisten bringt.'),
   (u'Einen Wettbewerbsvergleich', u'Drei Wettbewerber, direkt gegenübergestellt: wofür sie gefunden werden und Sie nicht.'),
   (u'Eine Aufwandseinschätzung', u'Zu jedem Punkt, was er ungefähr kostet. Damit Sie entscheiden können, ohne nachzufragen.'),
   (u'Ein Dokument, das Ihnen gehört', u'Intern umsetzbar oder mit einem anderen Dienstleister. Ohne Folgeauftrag.')],
 faq_head=u'Fragen zum SEO Audit',
 faq=[
   (u'Was kostet das Audit?', u'Nach der kostenlosen Analyse bekommen Sie einen Festpreis für einen klar beschriebenen Umfang. Kein Stundensatz.'),
   (u'Wie lange dauert es?', u'In der Regel ein bis zwei Wochen, abhängig von der Größe der Website und davon, wie schnell die Zugänge zu Search Console und Unternehmensprofil vorliegen.'),
   (u'Muss ich danach mit Ihnen weiterarbeiten?', u'Nein. Das Audit ist einzeln beauftragbar und endet mit der Übergabe. Viele setzen es intern um, und das ist in Ordnung.')])

service("leistungen/reporting.html",
 u"Reporting | Kontor",
 u"SEO Bericht auf einer Seite: welche Suchbegriffe sich bewegt haben, woher die Besucher kamen, was ansteht.",
 u"Leistung 05", u"Reporting.",
 u"Ein Bericht, den man ohne Vorkenntnisse lesen kann. Eine Seite, in dem Rhythmus, der zu Ihnen passt, mit den Zahlen, die tatsächlich etwas über das Geschäft aussagen.",
 [(u"Was drin steht",
   u"Positionen für die vereinbarten Suchbegriffe und die Veränderung seit dem letzten Bericht, Besucher aus der Suche, Anfragen soweit messbar, und was umgesetzt wurde. Dazu der nächste Schritt."),
  (u"Was nicht drin steht",
   u"Keine 40 Seiten aus einem Tool, keine Kennzahlen ohne Bezug zum Geschäft, keine Diagramme, die gut aussehen und nichts aussagen. Wenn eine Phase schlecht lief, steht das so im Bericht."),
  (u"Messbar ohne Tracking auf Besucherebene",
   u"Die Daten stammen aus der Google Search Console und aus Ihrem Unternehmensprofil. Dafür ist kein Tracking Cookie und kein Banner auf Ihrer Seite nötig.")],
 u"Rhythmus", [
  u"Ein Bericht, wann immer Sie ihn brauchen",
  u"Auf Wunsch fest getaktet, sonst auf Zuruf",
  u"Immer eine Seite, per E-Mail",
  u"Erreichbar bei Fragen, ohne Ticketsystem"], accent=5,
 subs=[u'Positionen, Besucher, Umgesetztes, nächster Schritt', u'Keine vierzig Seiten aus einem Tool', u'Ohne Cookie und ohne Banner auf Ihrer Seite'],
 vals_head=u'Was im Bericht steht',
 vals=[
   (u'Positionen und Veränderung', u'Die vereinbarten Suchbegriffe und wie sie sich seit dem letzten Bericht bewegt haben.'),
   (u'Besucher aus der Suche', u'Wie viele über Google kamen und auf welchen Seiten sie gelandet sind.'),
   (u'Umgesetzte Maßnahmen', u'Was in diesem Zeitraum tatsächlich gemacht wurde, in einer Sprache ohne Fachbegriffe.'),
   (u'Der nächste Schritt', u'Woran als Nächstes gearbeitet wird und warum gerade daran.')],
 faq_head=u'Fragen zum Reporting',
 faq=[
   (u'Wie oft kommt der Bericht?', u'Wann immer Sie ihn brauchen. Auf Wunsch fest getaktet, sonst auf Zuruf. Immer eine Seite, immer per E-Mail.'),
   (u'Brauche ich dafür Tracking oder einen Cookie-Banner?', u'Nein. Die Daten stammen aus der Google Search Console und aus Ihrem Unternehmensprofil. Auf Ihrer Seite ist dafür nichts einzubauen.'),
   (u'Was steht drin, wenn eine Phase schlecht lief?', u'Dass sie schlecht lief, und woran es lag. Ein Bericht, der nur gute Nachrichten enthält, ist kein Bericht.')])

# ---------------------------------------------------------------- Referenzen (Übersicht)
# Weitere Fallstudie hinzufügen: einen .ref-card Block ergänzen, data-cats mit
# den passenden Kategorien füllen, und falls nötig oben einen Filter ergänzen.
page("referenzen.html",
 u"Referenzen | Kontor",
 u"Fallstudien: wie wir Projekte für die organische Suche aufbauen.",
 hero(kicker=u"Referenzen",
   h1=u"Referenzen",
   lede=u"Keine Logowand ohne Zusammenhang. Pro Projekt die Ausgangslage, das Vorgehen und was daraus zu lernen war.") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="ref-filters" role="group" aria-label="Nach Kategorie filtern">
      <button class="ref-filter" data-cat="alle" aria-pressed="true">Alle</button>
      <button class="ref-filter" data-cat="social" aria-pressed="false">Social Media</button>
      <button class="ref-filter" data-cat="ecommerce" aria-pressed="false">E-Commerce</button>
      <button class="ref-filter" data-cat="technik" aria-pressed="false">Technisches SEO</button>
      <button class="ref-filter" data-cat="content" aria-pressed="false">Content</button>
      <button class="ref-filter" data-cat="local" aria-pressed="false">Local SEO</button>
    </div>

    <div class="ref-grid" style="--case-accent:var(--c4)">
      <a class="ref-card" href="referenzen/alejandro-arndt.html" data-cats="social">
        <div class="ref-tile">
          <img src="assets/img/case/alejandro-arndt.jpg" alt="Alejandro Arndt vor einer Holzfassade" loading="lazy" width="1200" height="1200">
          <div class="ref-tags"><span class="ref-tag">Social Media</span><span class="ref-tag">Reels</span><span class="ref-tag">Schnitt</span></div>
          <span class="ref-go"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
        </div>
        <h3 class="ref-name">Alejandro Arndt</h3>
        <p class="ref-desc">Wer dreht und schneidet, mit welchem Ger\u00e4t und warum der erste Monat nichts kostet.</p>
      </a>
      <a class="ref-card" href="referenzen/poseypets.html" data-cats="ecommerce technik content local">
        <div class="ref-tile">
          <img src="assets/img/case/poseypets-napoleon.jpg" alt="Tierportrait auf Leinwand neben dem abgebildeten Dackel" loading="lazy" width="1200" height="1200">
          <div class="ref-tags"><span class="ref-tag">E-Commerce</span><span class="ref-tag">Organic</span><span class="ref-tag">Content</span></div>
          <span class="ref-go"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
        </div>
        <h3 class="ref-name">PoseyPets <span class="ref-kind">SEO-Referenz</span></h3>
        <p class="ref-desc">Onlineshop für Tierportraits, von Grund auf für die organische Suche aufgebaut. Keyword-Struktur, sechs Landingpages, zwei Inhaltsformate.</p>
      </a>
    </div>

    <p class="ref-empty" hidden>In dieser Kategorie liegt noch keine Fallstudie vor.</p>
  </div>
</section>""")

# ---------------------------------------------------------------- Referenz Alejandro
# Die beiden Geraete sind aus CSS gebaut, nicht aus einem 3D-Modell: die Seite
# soll weiterhin ohne Bibliothek und ohne fremdes CDN auskommen. Die Masse
# stammen aus den technischen Daten von DJI, damit die Verhaeltnisse stimmen:
# Pocket 139,7 x 42,2 x 33,5 mm, Bildschirm 2 Zoll im Verhaeltnis 556:314.
PFEIL_L = (u'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
           u'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
           u'<path d="M19 12H5M11 18l-6-6 6-6"/></svg>')
PFEIL_R = (u'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
           u'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
           u'<path d="M5 12h14M13 6l6 6-6 6"/></svg>')

ICH_BILDER = [
 (u"alejandro-1.jpg", u"Alejandro Arndt vor einer Holzfassade"),
 (u"alejandro-2.jpg", u"Alejandro Arndt an einem gedeckten Tisch im Garten"),
 (u"alejandro-3.jpg", u"Alejandro Arndt auf einer Wiese"),
]
folien = u"".join(
 u'\n          <li class="gal-bild"><img src="../assets/img/case/%s" alt="%s" width="800" height="1000"%s></li>'
 % (d, a, u"" if i == 0 else u' loading="lazy"')
 for i, (d, a) in enumerate(ICH_BILDER))
punkte = u"".join(
 u'<button class="gal-punkt%s" type="button" aria-label="Bild %d"></button>'
 % (u" an" if i == 0 else u"", i + 1) for i in range(len(ICH_BILDER)))

def ich_galerie(up=u""):
    """Die Bildergalerie. up ist das Praefix zum Wurzelverzeichnis."""
    folien = u"".join(
     u'\n        <li class="gal-bild"><img src="%sassets/img/case/%s" alt="%s" width="800" height="1000"%s></li>'
     % (up, d, a, u"" if i == 0 else u' loading="lazy"')
     for i, (d, a) in enumerate(ICH_BILDER))
    punkte = u"".join(
     u'<button class="gal-punkt%s" type="button" aria-label="Bild %d"></button>'
     % (u" an" if i == 0 else u"", i + 1) for i in range(len(ICH_BILDER)))
    return u"""<div class="gal" data-gal>
      <ul class="gal-spur">%(folien)s
      </ul>
      <button class="gal-pfeil gal-zurueck" type="button" aria-label="Vorheriges Bild">%(l)s</button>
      <button class="gal-pfeil gal-vor" type="button" aria-label="N\u00e4chstes Bild">%(r)s</button>
    </div>
    <div class="gal-punkte">%(punkte)s</div>""" % {
      "folien": folien, "punkte": punkte, "l": PFEIL_L, "r": PFEIL_R}


def ich_geraete():
    """Osmo Pocket 4 und DJI Mic, zum Drehen und Durchblaettern."""
    return u"""<div class="geraete" data-geraete>
      <div class="geraet" data-name="DJI Osmo Pocket 4">
        <div class="pocket-stage">
          <div class="pocket" tabindex="0" role="img" aria-label="Dreidimensionale Darstellung einer DJI Osmo Pocket 4, mit Maus, Finger oder Pfeiltasten drehbar">
            <div class="pk-koerper">%(koerper)s
              <span class="pk-schirm"><span class="pk-schirm-bild"></span></span>
              <span class="pk-rad"></span>
              <span class="pk-knopf"></span>
              <span class="pk-marke">dji</span>
              <span class="pk-seitentext">POCKET 4</span>
            </div>
            <div class="pk-stiel">%(stiel)s</div>
            <div class="pk-motor">%(motor)s</div>
            <div class="pk-kopf">%(kopf)s
              <span class="pk-linse"><span class="pk-linse-glas"></span></span>
            </div>
          </div>
        </div>
      </div>
      <div class="geraet" data-name="DJI Mic" hidden>
        <div class="pocket-stage">
          <div class="pocket" tabindex="0" role="img" aria-label="Dreidimensionale Darstellung eines DJI Mic Senders, mit Maus, Finger oder Pfeiltasten drehbar">
            <div class="mic-koerper">%(mic)s
              <span class="mic-gitter"></span>
              <span class="mic-led"></span>
              <span class="mic-marke">dji</span>
            </div>
            <div class="mic-clip">%(clip)s</div>
          </div>
        </div>
      </div>
      <button class="geraet-pfeil geraet-zurueck" type="button" aria-label="Vorheriges Ger\u00e4t">%(l)s</button>
      <button class="geraet-pfeil geraet-vor" type="button" aria-label="N\u00e4chstes Ger\u00e4t">%(r)s</button>
    </div>
    <p class="geraet-name" data-geraet-name>DJI Osmo Pocket 4</p>""" % {
      "koerper": quader(), "stiel": quader(), "motor": quader(),
      "kopf": quader(), "mic": quader(), "clip": quader(),
      "l": PFEIL_L, "r": PFEIL_R}


def quader(k=None):
    """Die sechs Flaechen eines Quaders. Die Klassen sind fuer alle Quader
    gleich; Groesse, Tiefe und Farbe kommen ueber --w, --h, --d und --m von
    der Gruppe darueber. So braucht das Stylesheet nur einen Satz Regeln."""
    return u"".join(u'\n            <span class="pk-f pk-%s"></span>' % f
                    for f in (u"vo", u"hi", u"li", u"re", u"ob", u"un"))

page("referenzen/alejandro-arndt.html",
 u"Alejandro Arndt | Kontor",
 u"Wer dreht und schneidet: Alejandro Arndt aus Uhingen, mit DJI Osmo Pocket 4 und DJI Mic.",
 u"""<section class="section cs" style="padding-top:clamp(30px,5vw,56px)">
  <div class="wrap">
    <div class="me">
      <div class="me-foto">
        <h1 class="me-name">Alejandro Arndt</h1>
        %(galerie)s
        <div class="prose me-vorstellung">
          <p>Videografie ist meine Leidenschaft. Ich drehe und schneide, seit ich eine Kamera halten kann, und sitze jeden Tag mehrere Stunden im Schnitt. Genau das will ich zu meinem Beruf machen.</p>
          <p>Deshalb der Probemonat: einen Monat lang Reels, ohne Rechnung und ohne K\u00fcndigungsfrist. Ich arbeite von Uhingen aus und komme f\u00fcr den Dreh zu Ihnen.</p>
        </div>
      </div>
      <div class="me-txt">
        <h2 style="margin:0">Mein Equipment</h2>
        %(geraete)s
        <p class="pocket-hint">Ziehen zum Drehen, Pfeile f\u00fcr das n\u00e4chste Ger\u00e4t</p>
      </div>
    </div>
  </div>
</section>""" % {"galerie": ich_galerie(u"../"), "geraete": ich_geraete()} + cta("../"))

# ---------------------------------------------------------------- Fallstudie PoseyPets
page("referenzen/poseypets.html",
 u"Fallstudie PoseyPets | Kontor",
 u"Wie der Onlineshop PoseyPets von Grund auf für die organische Suche aufgebaut wurde: Keyword-Recherche mit Sistrix, Seitenstruktur, täglicher Content, Technik und Linkaufbau.",
 u"""<section class="section cs" style="padding-top:0">
  <div class="wrap">
    <div class="cs-brand">
      <img src="../assets/img/case/posey-logo.png" alt="Logo von PoseyPets" width="500" height="268">
      <h1 style="font-size:clamp(2rem,4.6vw,3.4rem);margin:0">PoseyPets</h1>
      <p class="lede" style="margin:0 auto">Ein deutscher Onlineshop für individuelle Tierportraits. Der Kunde lädt ein Foto hoch, und sein Tier wird als historische Figur gemalt. Die Aufgabe: gefunden werden, ohne jeden Besucher einkaufen zu müssen.</p>
      <div class="tags"><span class="tag accent">E-Commerce</span><span class="tag">Technisches SEO</span><span class="tag">Content</span><span class="tag">Keyword-Strategie</span><span class="tag">Linkaufbau</span></div>
      <a class="cs-visit" href="https://poseypets.com" target="_blank" rel="noopener">poseypets.com ansehen</a>
      <!-- Die Offenlegung steht bewusst offen und nicht in einem Feld: ein
           Hinweis, den man erst aufklappen muss, ist keine Offenlegung. -->
      <p class="cs-disclosure">Offenlegung: PoseyPets ist ein eigenes Projekt. Wir zeigen es, weil wir dort jeden Schritt selbst gegangen sind und offen darüber schreiben können, auch über das, was nicht funktioniert hat.</p>
    </div>
    <div class="cs-hero" style="margin-bottom:0">
      <img src="../assets/img/case/poseypets-wohnzimmer.jpg" alt="Tierportraits als Wanddekoration im Wohnzimmer" width="1200" height="600">
    </div>
  </div>
</section>

<section class="section cs" style="padding-top:clamp(40px,5vw,72px)">
  <div class="wrap">""" + acc([

  (u"01", u"Ausgangssituation", u"Neuer Shop, keine Domainhistorie, null Sichtbarkeit", u"""
          <p>Ein neuer Shop ohne Domainhistorie, in einem Umfeld, in dem bereits internationale Anbieter stehen. Zum Start war der Shop bei Google für keinen einzigen relevanten Begriff zu finden. Es gab keine eingehenden Links, keine Historie, keine Seite, die irgendwo rankte.</p>
          <p>Die naheliegende Alternative wäre gewesen, jeden Besucher über bezahlte Anzeigen einzukaufen. Das funktioniert, solange Budget da ist, und endet an dem Tag, an dem es aufhört. Bei einem Produkt mit begrenztem Warenkorbwert frisst es außerdem die Marge: Wenn der Klickpreis steigt, steigt er für jede einzelne Bestellung mit, und die Rechnung geht irgendwann nicht mehr auf.</p>
          <p>Also sollte die organische Suche die tragende Säule werden, mit allem, was das bedeutet: langsamer Start, kein Ergebnis in den ersten Wochen, und eine Reihenfolge, von der nicht abgewichen wird. Die folgenden Bereiche beschreiben genau diese Reihenfolge.</p>
          <div class="cs-split">
            <img src="../assets/img/case/poseypets-caesar.jpg" alt="Hundeportrait im Stil eines römischen Kaisers" loading="lazy" width="600" height="600">
            <img src="../assets/img/case/poseypets-mona.jpg" alt="Katzenportrait im Stil der Mona Lisa" loading="lazy" width="600" height="600">
          </div>"""),

  (u"02", u"Keyword-Recherche", u"Der komplette erste Monat, bevor eine Zeile geschrieben wurde", u"""
          <p><strong>Der erste Monat ging vollständig in die Recherche.</strong> Keine Landingpage, kein Blogbeitrag, keine Produktbeschreibung, bevor die Begriffsliste stand. Das klingt nach verlorener Zeit und ist das Gegenteil davon: Jede Seite, die danach entstand, hatte einen Begriff, für den sie gebaut wurde, und jeder Artikel ein Thema, von dem vorher feststand, dass danach gesucht wird.</p>
          <p>Gearbeitet wurde mit <strong>Sistrix</strong>. Jeder einzelne Begriff wurde angesehen, nicht nur die offensichtlichen: Suchvolumen, Wettbewerb, und vor allem die Absicht dahinter. Wer „Hundeportrait malen lassen“ eingibt, will kaufen. Wer „Hundeportrait malen“ eingibt, will es selbst tun. Dazwischen liegt ein Buchstabe und der gesamte Unterschied zwischen einer Bestellung und einem Besucher, der nie etwas kauft.</p>
          <p>Der wichtigste Fund kam ganz am Anfang und hat danach die gesamte Struktur bestimmt: bei diesen Begriffen entscheidet die <strong>Schreibweise</strong> über den Erfolg.</p>
          <div class="cs-quote">
            <p>„Haustier Portrait“ und „Haustierportrait“ sind für Google nicht dasselbe Wort. Der Unterschied im Suchvolumen liegt beim Zehnfachen.</p>
          </div>
          <p>Und es gibt keine Regel dafür. Bei einem Tier gewinnt die getrennte Schreibweise deutlich, beim nächsten die zusammengeschriebene. Das muss pro Begriff geprüft werden, bevor irgendetwas geschrieben wird, denn die Schreibweise steckt später im Titel, in der Überschrift, in der URL und in jedem internen Link, der darauf zeigt. Sie lässt sich nicht beiläufig korrigieren.</p>
          <p>Genauso wichtig war, was <em>aussortiert</em> wurde. Ein ganzer Begriffscluster sah nach viel Volumen aus, bestand aber fast vollständig aus Leuten, die selbst malen lernen wollen. Ein zweiter war komplett wertlos, weil die Suchenden etwas ganz anderes meinten. Beide wurden gestrichen, bevor Arbeit hineinfloss. Das ist die unsichtbare Hälfte der Recherche: Nicht nur zu wissen, worauf man zielt, sondern worauf man bewusst nicht zielt.</p>
          <p>Am Ende des Monats stand eine sortierte Liste. Aus ihrem oberen Teil wurden die Landingpages, aus dem langen unteren Teil die Themen für Ratgeber und Lexikon. Beides kam aus derselben Datei, und keine Seite und kein Artikel entstand ohne Eintrag darin.</p>"""),

  (u"03", u"Seitenstruktur", u"Ein Suchbegriff, eine Seite. Sechs Landingpages als Einstiege.", u"""
          <p>Aus der Liste wurden sechs eigene Landingpages gebaut, je eine pro Hauptbegriff, nach einer einzigen Regel: <strong>ein Suchbegriff, eine Seite.</strong></p>
          <p>Der Grund dafür ist unspektakulär und wird trotzdem ständig übersehen. Google rankt keine Shops, sondern einzelne Seiten. Gibt es zwei Seiten, die dasselbe Thema behandeln, muss Google sich entscheiden, welche davon zum Suchbegriff passt, und beide verlieren: Jede bekommt einen Teil der Signale, keine bekommt genug, um vorn zu stehen. Im Fachjargon heißt das Keyword-Kannibalisierung, praktisch heißt es, dass man sich selbst Konkurrenz macht.</p>
          <p>Eine Landingpage ist hier keine Textseite, sondern eine vollwertige Produktübersicht zu genau einem Begriff. Die Überschrift trägt den Begriff in der Schreibweise, die vorher gewonnen hat. Darunter kommen ein kurzer Einstieg, die passenden Produkte, die wiederkehrenden Fragen zu genau diesem Motiv und Links zu den Artikeln, die dazu gehören. Wer über die Suche kommt, sieht sofort Produkte und nicht erst 800 Wörter Einleitung — die Reihenfolge auf der Seite folgt dem, was der Besucher in diesem Moment vorhat.</p>
          <p>Darunter liegt die zweite Ebene: die Produktseiten. Jede bekam einen eigenen Textblock, der auf ihren eigenen Begriff zugeschnitten ist, statt überall denselben Beschreibungstext zu wiederholen. Daneben, nicht darunter, stehen Ratgeber und Lexikon. So entsteht eine Struktur, in der jede Seite eine Aufgabe hat und keine zwei Seiten dieselbe.</p>"""),

  (u"04", u"Inhalte und Blog", u"Jeden Tag ein Beitrag, in zwei Formaten mit zwei Aufgaben", u"""
          <p><strong>Seit dem Start erscheint jeden Tag ein Beitrag.</strong> Nicht wöchentlich, nicht wenn gerade Zeit ist, sondern täglich. Das ist weniger eine kreative als eine rechnerische Entscheidung: Jeder Artikel ist ein eigener Einstiegspunkt in die Suche. Einer bringt fast nichts. Hundert bringen, nach einigen Monaten, einen Strom, der nicht von einzelnen Begriffen abhängt und den kein Wettbewerber mit einer einzelnen guten Seite einholt.</p>
          <p>Die Themen kommen nicht aus Einfällen, sondern aus dem unteren Teil der Keyword-Liste aus Bereich 02. Jeder Beitrag hat einen Begriff, für den er geschrieben wurde. Gibt es keinen, wird er nicht geschrieben.</p>
          <p>Dafür gibt es zwei bewusst unterschiedliche Formate statt eines Blogs, weil sie zwei verschiedene Aufgaben haben:</p>
          <ul>
            <li><strong>Ratgeber</strong> für die ausführlichen Fragen, die sich jemand vor dem Kauf stellt. Längere Stücke, die eine Entscheidung vorbereiten — welches Foto sich eignet, welcher Stil zu welchem Tier passt, wie lange es dauert.</li>
            <li><strong>Lexikon</strong> von A bis Z für die vielen kurzen Begriffssuchen, mit eigener Filterung. Kurze Einträge, die jeweils einen Begriff sauber erklären und von dort weiterführen.</li>
          </ul>
          <p>Dazu eine feste Regel für die interne Verlinkung: etwa <strong>60 Prozent der Links zeigen auf Seiten, die verkaufen, 40 Prozent auf weitere Inhalte.</strong> Diese Quote wird bei jedem Beitrag eingehalten, nicht im Nachhinein geprüft.</p>
          <div class="cs-note">
            <h3>Warum diese Regel</h3>
            <p>Ohne sie verlinkt ein Blog nach einiger Zeit fast nur noch sich selbst. Die Artikel ranken dann vielleicht, schieben aber keine Kraft mehr auf die Seiten, an denen tatsächlich Geld verdient wird. Man hat dann eine gut besuchte Inhaltssammlung gebaut und keinen Shop.</p>
          </div>
          <div class="cs-split">
            <img src="../assets/img/case/poseypets-tasse.jpg" alt="Personalisierte Tasse mit Tierportrait" loading="lazy" width="600" height="600">
            <img src="../assets/img/case/poseypets-unboxing.jpg" alt="Ausgepacktes Tierportrait" loading="lazy" width="600" height="600">
          </div>"""),

  (u"05", u"Technisches SEO", u"Metadaten, Alt-Texte, Auszeichnung, Ladezeit, interne Links", u"""
          <p>Technik bringt selten allein eine Position. Sie verhindert aber, dass alles andere wirkungslos bleibt. Deshalb lief sie parallel mit, von Anfang an und über den gesamten Shop, nicht als einmalige Aufräumaktion.</p>
          <ul>
            <li><strong>Metadaten über alle Produkte und Kategorien.</strong> Jede Seite hat einen eigenen Titel und eine eigene Beschreibung, beide mit dem Begriff, für den die Seite gebaut wurde. Kein generiertes Muster, das sich über hundert Seiten wiederholt. Der Titel entscheidet nicht nur über die Einordnung, sondern darüber, ob jemand im Suchergebnis überhaupt klickt.</li>
            <li><strong>Alt-Texte für jedes Bild.</strong> In einem Shop, der von Bildern lebt, ist das doppelt wichtig: Sie beschreiben Screenreadern, was zu sehen ist, und sie sind das Einzige, woran die Bildersuche ein Motiv erkennt. Bei „Tierportrait“ ist die Bildersuche ein eigener Einstieg, nicht ein Nebenschauplatz.</li>
            <li><strong>FAQ mit passender Auszeichnung.</strong> Die wiederkehrenden Fragen stehen strukturiert ausgezeichnet auf der Seite, sodass Google sie als Frage-Antwort-Paare erkennen und direkt im Suchergebnis anzeigen kann. Das vergrößert den eigenen Eintrag und nimmt Platz, den sonst jemand anderes bekommt.</li>
            <li><strong>Ladezeit und Darstellung auf dem Handy.</strong> Der größte Teil der Besucher kommt mobil. Eine Seite, die zu lange lädt, verliert Besucher, bevor sie etwas gesehen haben — und die abgebrochenen Aufrufe sind für Google ein Signal, das auf die Position zurückwirkt.</li>
            <li><strong>Interne Verlinkung bis in den Footer.</strong> Jede wichtige Seite ist von mehreren Stellen aus erreichbar, auch aus dem Fußbereich. Was nur über die Suche im Shop zu finden ist, findet Google schlecht und ein Besucher gar nicht.</li>
          </ul>
          <p>Eine Entscheidung fiel gegen den ersten Impuls: bestehende URLs wurden <em>nicht</em> umgezogen, obwohl eine andere Struktur auf dem Papier aufgeräumter gewesen wäre. Die Seiten rankten bereits.</p>
          <div class="cs-quote">
            <p>Einen vorhandenen Rankingaufbau für eine kosmetische Verbesserung wegzuwerfen, ist einer der teuersten Fehler überhaupt. Wir sehen ihn ständig.</p>
          </div>"""),

  (u"06", u"Linkaufbau", u"Gezielte Ansprache passender Unternehmen, rund 30 externe Links", u"""
          <p>Linkaufbau kam zuletzt, und das hat einen Grund: Solange Technik, Struktur und Inhalte nicht stehen, zeigen Links auf eine Seite, die die Aufmerksamkeit nicht halten kann. Erst als die sechs Landingpages standen und der tägliche Takt lief, ergab es Sinn, dass von außen jemand darauf zeigt.</p>
          <p>Das Vorgehen ist Handarbeit und sieht so aus: Wir suchen Unternehmen und Seiten, die inhaltlich zu PoseyPets passen — Tierbedarf, Geschenke, Fotografie, Tierblogs — und die selbst eine echte, sichtbare Seite betreiben. Wer selbst nicht gefunden wird, kann niemanden weiterempfehlen. Diese Betriebe werden angeschrieben, persönlich und mit einem konkreten Vorschlag.</p>
          <p>Angeboten wird eines von zwei Dingen:</p>
          <ul>
            <li>Ein <strong>Linktausch</strong>, bei dem beide Seiten voneinander profitieren, weil die Themen tatsächlich zusammenpassen und die Erwähnung für die Leser der anderen Seite Sinn ergibt.</li>
            <li>Ein <strong>Gastartikel</strong>, für den wir den Beitrag schreiben. Die andere Seite bekommt einen Inhalt, den sie sonst selbst erstellen müsste, und wir die Verlinkung aus dem Text heraus.</li>
          </ul>
          <p>Auf diesem Weg sind für PoseyPets <strong>rund 30 externe Links</strong> entstanden. Keiner davon gekauft, keiner aus einem Linknetzwerk, keiner aus einem Verzeichnis, das nur existiert, um Links zu verteilen. Das ist bewusst so: Gekaufte und maschinell verteilte Links lassen sich erkennen, und der Schaden trifft dann nicht eine Unterseite, sondern die gesamte Domain.</p>
          <p>Es ist der langsamste Bereich von allen. Dreißig gute Links brauchen deutlich mehr Zeit als dreihundert schlechte, und genau darin liegt ihr Wert.</p>"""),

  (u"07", u"Stand heute", u"Live, verkauft, und die Sichtbarkeit baut sich weiter auf", u"""
          <p>Der Shop ist live, verkauft und läuft geschäftlich gut. Die Sichtbarkeit baut sich weiter auf, die Landingpages ranken für ihre jeweiligen Begriffe, der tägliche Takt bei den Inhalten läuft unverändert weiter, und die Zahl der externen Erwähnungen wächst langsam mit.</p>
          <p>SEO ist hier kein abgeschlossenes Projekt, sondern die Grundlage, auf der weitergearbeitet wird. Das ist die ehrliche Beschreibung: Es gibt keinen Tag, an dem man fertig ist. Es gibt einen Punkt, ab dem die Arbeit der letzten Monate ohne weiteres Zutun Besucher bringt, und danach entscheidet man, wie viel man noch darauflegt.</p>
          <figure class="cs-figure">
            <img src="../assets/img/case/poseypets-valentin.jpg" alt="Tierportrait als Geschenk" loading="lazy" width="1200" height="900">
            <figcaption>Saisonale Anlässe als eigene Einstiegspunkte in die Suche</figcaption>
          </figure>"""),

  (u"08", u"Was daraus für andere folgt", u"Die Reihenfolge entscheidet, und die halbe Stunde am Anfang", u"""
          <p><strong>Die Reihenfolge entscheidet.</strong> Zuerst prüfen, welche Suchbegriffe überhaupt zu Umsatz führen, dann die Seiten dafür bauen, dann Inhalte produzieren, und erst ganz zum Schluss Links aufbauen. Wer umgekehrt anfängt, schreibt Texte für Suchanfragen, die nie zu einer Anfrage führen, und merkt es erst nach Monaten.</p>
          <p><strong>Und die Schreibweise prüfen.</strong> Eine falsch gewählte Variante kostet dauerhaft den Großteil des möglichen Volumens, weil sie in Titeln, URLs und Überschriften steckt. Diese halbe Stunde am Anfang ist die billigste Stunde im ganzen Projekt.</p>
          <p>Beides lässt sich auf fast jedes Geschäft übertragen, das über Google gefunden werden will. Nur die Begriffe sind andere.</p>"""),
 ]) + u"""
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">""" + cta("../") + u"""
  </div>
</section>""")

# Die frühere kontakt.html ist in angebot.html aufgegangen. Sie bleibt nur
# als Weiterleitung stehen, damit verschickte und indexierte Links nicht ins
# Leere laufen. GitHub Pages kann keine echte Weiterleitung, deshalb per
# Meta-Refresh und Canonical.
io.open(os.path.join(ROOT, "kontakt.html"), "w", encoding="utf-8").write(u"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=angebot.html">
<link rel="canonical" href="https://kontor-seo.de/angebot.html">
<meta name="robots" content="noindex,follow">
<title>Weitergeleitet | Kontor</title>
</head>
<body>
<p>Diese Seite ist umgezogen. Weiter zum <a href="angebot.html">Gratismonat</a>.</p>
</body>
</html>
""")
print("wrote kontakt.html (Weiterleitung)")

# ---------------------------------------------------------------- Blog
# Nur noch ein Format: Ratgeber. Jeder Beitrag eine eigene Seite unter blog/.
RAT_SLUGS = set(q[0] for q in RATGEBER)
PLAN_SLUGS = set(q[0] for q in GEPLANT)

def fix_links(html):
    """Verweise auf noch nicht geschriebene Beitraege werden zu normalem Text.
    So steht nie ein toter Link auf der Seite, und sobald der Beitrag da ist,
    wird aus demselben Text automatisch wieder ein Link."""
    def repl(m):
        slug = m.group(1)
        if slug in RAT_SLUGS:
            return m.group(0)
        if slug in PLAN_SLUGS:
            return u'<<STRIP>>'
        return m.group(0)
    html = re.sub(r'href="([a-z0-9][a-z0-9.-]*)\.html"', repl, html)
    # <a <<STRIP>> ...>Text</a>  ->  Text
    return re.sub(r'<a [^>]*<<STRIP>>[^>]*>(.*?)</a>', r'\1', html, flags=re.S)

def lesezeit(html):
    """Woerter geteilt durch 200, wie in blog-darstellung.md."""
    return max(1, int(round(len(re.sub(r'<[^>]+>', ' ', html).split()) / 200.0)))

POSTS = [(sl, ti, te, le, bo) for sl, ti, te, le, bo in RATGEBER]

NAME = dict(THEMEN_NAMEN)

def datum_de(iso):
    """2026-10-14 -> 14.10.2026"""
    j, m, t = iso.split("-")
    return u"%s.%s.%s" % (t, m, j)

def card(q, up=u""):
    """Karte wie im Posey-Magazin: Bild mit Lesezeit- und Datumsplakette,
    darunter die Schlagwoerter und der Titel. Kein Teaser, der steht dort
    auch nicht."""
    slug = q[0]
    themen = THEMEN.get(slug, ())
    pillen = u"".join(u'<span class="post-tag">%s</span>' % NAME.get(t, t) for t in themen)
    return u"""
      <a class="post" href="%(up)s%(slug)s.html" data-cats="%(cats)s">
        <span class="post-bild">
          <img src="%(up)s../assets/img/blog/%(slug)s-1.jpg" alt="" width="1200" height="900" loading="lazy">
          <span class="post-zeit">%(zeit)s min</span>
          <span class="post-datum">%(datum)s</span>
        </span>
        <span class="post-tags">%(pillen)s</span>
        <h3>%(titel)s</h3>
      </a>""" % {
        "up": up, "slug": slug, "cats": u" ".join(themen),
        "zeit": lesezeit(q[4]), "datum": datum_de(DATUM.get(slug, u"2026-10-14")),
        "pillen": pillen, "titel": q[1]}

def related(slug):
    rest = [q for q in POSTS if q[0] != slug]
    i = [q[0] for q in POSTS].index(slug)
    return u"".join(card(rest[(i + k) % len(rest)]) for k in (1, 2, 3))

SIDE = u"""
    <aside class="art-side">
      <div class="art-box">
        <a href="../index.html" class="logo">Kontor</a>
        <p class="art-sub">SEO-Agentur</p>
        <nav class="art-toc" aria-label="Kapitel" hidden>
          <span class="art-toc-h">Kapitel</span>
          <ol></ol>
        </nav>
        <a href="../angebot.html#kontakt" class="btn btn-primary btn-sm art-cta">Gratismonat anfragen</a>
      </div>
    </aside>"""

for slug, titel, teaser, lede, body in POSTS:
    page("blog/%s.html" % slug,
         u"%s | Kontor" % TITEL.get(slug, titel),
         META[slug],
         hero(kicker=u"Ratgeber &middot; %s min lesen" % lesezeit(body),
              h1=titel, lede=lede) + u"""
<section class="section" style="padding-top:0">
  <div class="wrap art-grid">%s
    <div class="prose art-body">%s
    </div>
  </div>
</section>

<section class="section" style="padding-top:clamp(30px,4vw,56px)">
  <div class="wrap">
    <div class="sec-head" style="max-width:none;align-items:center;text-align:center">
      <h2>Weiterlesen</h2>
    </div>
    <div class="posts">%s
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">%s
  </div>
</section>""" % (SIDE, fix_links(body), related(slug), cta("../")))

page("blog/index.html",
 u"Blog | Kontor",
 u"Ratgeber zu Social Media und Suchmaschinenoptimierung: verständlich erklärt, ohne Fachchinesisch und ohne Versprechen, die niemand halten kann.",
 hero(kicker=u"Blog",
   h1=u"Blog",
   lede=u"Die ausführlichen Antworten auf die Fragen, die uns Kunden immer wieder stellen.") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="ref-filters" role="group" aria-label="Nach Thema filtern">%(filter)s
    </div>
    <div class="posts">%(karten)s
    </div>
    <p class="ref-empty" hidden>Zu diesem Thema steht noch kein Beitrag bereit.</p>
  </div>
</section>""" % {
  "filter": u"".join(
    u'\n      <button class="ref-filter" data-cat="%s" aria-pressed="%s">%s</button>'
    % (k, u"true" if k == u"alle" else u"false", n) for k, n in THEMEN_NAMEN),
  "karten": u"".join(card(q) for q in POSTS)})

# ---------------------------------------------------------------- Impressum
page("impressum.html", u"Impressum | Kontor", u"Impressum nach § 5 DDG.",
 hero(kicker=u"Pflichtangaben", h1=u"Impressum.", lede=u"Angaben gemäß § 5 DDG.") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap prose">
    <!-- Übernommen aus dem Impressum von poseypets.com, auf diese Tätigkeit
         angepasst. Einzelunternehmen, daher nach § 5 DDG der bürgerliche Name
         und die ladungsfähige Anschrift; eine Firmierung ist nicht nötig. -->
    <h2>Diensteanbieter</h2>
    <p>Alejandro Arndt<br>Albstraße 54<br>73066 Uhingen<br>Deutschland</p>
    <h2>Kontakt</h2>
    <p>Telefon: +49 177 188 5605<br>E-Mail: <a href="mailto:alejandroarndt@kontor-seo.de">alejandroarndt@kontor-seo.de</a></p>
    <h2>Umsatzsteuer</h2>
    <p>Gemäß § 19 UStG wird keine Umsatzsteuer berechnet (Kleinunternehmerregelung).</p>
    <h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2>
    <p>Alejandro Arndt, Anschrift wie oben.</p>
    <h2>Streitbeilegung</h2>
    <p>Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
  </div>
</section>""", robots="noindex,follow")

# ---------------------------------------------------------------- Datenschutz
page("datenschutz.html", u"Datenschutzerklärung | Kontor",
 u"Informationen zur Verarbeitung personenbezogener Daten auf dieser Website.",
 hero(kicker=u"Datenschutz", h1=u"Datenschutzerklärung.",
   lede=u"Diese Website kommt ohne Cookies, ohne Tracking und ohne eingebettete Inhalte Dritter aus.") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap prose">
    <!-- Verantwortlicher aus dem PoseyPets Datenschutz übernommen. Der REST ist
         bewusst NICHT übernommen: dort stehen Shopify, Printify, Klarna und
         PayPal, die es hier alle nicht gibt. Hier ist GitHub der Hoster. -->
    <h2>Verantwortlicher</h2>
    <p>Alejandro Arndt, Albstraße 54, 73066 Uhingen, Deutschland. Siehe <a href="impressum.html">Impressum</a>.</p>
    <h2>Keine Cookies, kein Tracking</h2>
    <p>Diese Website setzt keine Cookies, verwendet keine Analyse- oder Trackingdienste und bindet keine Inhalte Dritter ein. Schriftarten und Videos werden vom eigenen Webspace ausgeliefert, es findet keine Verbindung zu Google Fonts oder zu einem Videoportal statt. Deshalb gibt es auch keinen Cookie-Banner.</p>
    <h2>Hosting durch GitHub Pages</h2>
    <p>Diese Website wird bei GitHub Pages gehostet, einem Dienst der GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA. Beim Aufruf verarbeitet GitHub technisch notwendige Zugriffsdaten, insbesondere die IP-Adresse, Datum und Uhrzeit des Zugriffs, die aufgerufene Seite, den verweisenden Link sowie Browser- und Betriebssystemangaben. Diese Verarbeitung ist für die Auslieferung und die Sicherheit der Website erforderlich.</p>
    <p>Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO, das berechtigte Interesse an einer sicheren und zuverlässigen Bereitstellung der Website. Da GitHub seinen Sitz in den USA hat, kann eine Übermittlung personenbezogener Daten in die USA nicht ausgeschlossen werden.</p>
    <h2>Terminbuchung über Google Kalender</h2>
    <p>Auf der Kontaktseite können Sie einen Telefontermin buchen. Der Kalender stammt von Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland. Er wird <strong>erst geladen, wenn Sie die Schaltfläche anklicken</strong>. Vorher wird keine Verbindung zu Google aufgebaut und es werden keine Daten übertragen.</p>
    <p>Mit dem Klick übermittelt Ihr Browser an Google insbesondere Ihre IP-Adresse sowie Browser- und Geräteangaben; Google kann dabei Cookies setzen. Rechtsgrundlage für das Laden ist Ihre Einwilligung nach Art. 6 Abs. 1 lit. a DSGVO, die Sie durch den Klick erteilen und für die Zukunft widerrufen können, indem Sie die Seite verlassen oder neu laden. Buchen Sie anschließend einen Termin, verarbeiten wir Ihre Angaben zur Durchführung des Termins auf Grundlage von Art. 6 Abs. 1 lit. b DSGVO.</p>
    <p>Sie können einen Termin auch ohne Google vereinbaren, indem Sie uns per <a href="mailto:alejandroarndt@kontor-seo.de">E-Mail</a> oder telefonisch schreiben.</p>

    <h2>Kontaktaufnahme</h2>
    <p>Wenn Sie uns per E-Mail oder Telefon kontaktieren, verarbeiten wir Ihre Angaben ausschließlich zur Bearbeitung Ihrer Anfrage. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO bei vorvertraglichen Maßnahmen, sonst Art. 6 Abs. 1 lit. f DSGVO. Die Daten werden gelöscht, sobald sie nicht mehr erforderlich sind und keine gesetzlichen Aufbewahrungsfristen entgegenstehen.</p>
    <h2>Ihre Rechte</h2>
    <p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch gegen die Verarbeitung. Außerdem steht Ihnen ein Beschwerderecht bei einer Datenschutzaufsichtsbehörde zu.</p>
  </div>
</section>""", robots="noindex,follow")

print("ok")
