# -*- coding: utf-8 -*-
"""Generates every sub page from the shared shell in index.html.
Run after changing the header or footer:  python3 _build/make_pages.py
The generated .html files are what ships; this script is convenience only."""
import io, re, os

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
<noscript><style>.rv{{opacity:1;transform:none}}</style></noscript>
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
        btn = (u'\n    <div class="hero-cta"><a href="%skontakt.html" class="btn btn-primary">'
               u'Kostenlose SEO-Analyse%s</a></div>' % (cta_up, ARR))
    return HERO_T.format(kicker=kicker, h1=h1, lede=lede, cta=btn)

def cta(up=""):
    return u"""<div class="band" style="margin-top:46px">
      <div class="band-in">
        <h2 style="margin:0 0 14px">Wo steht Ihre Seite gerade?</h2>
        <p class="lede">Sie bekommen schriftlich, für welche Suchbegriffe Sie gefunden werden, wer vor Ihnen steht und woran es liegt.</p>
        <div class="hero-cta"><a href="%skontakt.html" class="btn btn-primary">Kostenlose SEO-Analyse<span class="arr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></a></div>
      </div>
    </div>""" % up

SERVICES = [
 (1, u"SEO", u"seo.html"),
 (2, u"OnPage und Webdesign", u"onpage-und-webdesign.html"),
 (3, u"Linkaufbau", u"linkaufbau.html"),
 (4, u"SEO Audit", u"seo-audit.html"),
 (5, u"Reporting", u"reporting.html"),
]

def other_services(n):
    """Querverweise auf die uebrigen vier Leistungen, je im eigenen Farbton."""
    rows = u"".join(
        u'\n      <a class="xs-row" href="%s" style="--c:var(--c%d);--c-soft:var(--c%d-soft)">'
        u'<span class="xs-n">0%d</span><span class="xs-t">%s</span>'
        u'<span class="xs-a">%s</span></a>' % (href, i, i, i, name, ARR)
        for i, name, href in SERVICES if i != n)
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
            accent=None, vals_head=u"", vals=(), faq_head=u"", faq=()):
    body = hero(kicker=kicker, h1=h1, lede=lede, cta_up="../")

    # Die drei Textbloecke als nummerierte Zeilen statt als Fliesstext.
    steps = u"".join(
        u"""
      <div class="step rv">
        <div class="step-k"><span class="step-n">%02d</span><h2>%s</h2></div>
        <p>%s</p>
      </div>""" % (i + 1, h, t) for i, (h, t) in enumerate(sections))
    body += u"""
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="steps">%s
    </div>
  </div>
</section>""" % steps

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

    body += other_services(accent)
    body += u"""
<section class="section" style="padding-top:0">
  <div class="wrap">%s
  </div>
</section>""" % cta("../")
    page(path, title, desc, body, accent=accent)

# Die Leistungskarten stehen auf der Startseite und auf der Uebersicht. Hier
# relativ innerhalb von leistungen/, auf der Startseite mit dem Praefix.
SVC = [
 (u"01", u"SEO", u"seo.html",
  u"Technik, Inhalte, lokale Sichtbarkeit.",
  u"Die drei Bereiche h\u00e4ngen zusammen. Wir trennen sie nicht in Pakete, sondern arbeiten an dem, was bei Ihnen den Unterschied macht.",
  u"Jetzt ranken"),
 (u"02", u"OnPage und Webdesign", u"onpage-und-webdesign.html",
  u"Struktur vor Gestaltung.",
  u"Wie eine Seite aufgebaut ist, entscheidet mehr \u00fcber die Position als ihr Aussehen. \u00dcberschriften, interne Links und Suchabsicht.",
  u"Jetzt umbauen"),
 (u"03", u"Linkaufbau", u"linkaufbau.html",
  u"Herkunft statt Anzahl.",
  u"Verlinkungen aus Quellen, bei denen eine Erw\u00e4hnung auch ohne SEO Sinn ergeben w\u00fcrde. Keine gekauften Netzwerke.",
  u"Jetzt verlinken"),
 (u"04", u"SEO Audit", u"seo-audit.html",
  u"Erst messen, dann entscheiden.",
  u"Vollst\u00e4ndige Bestandsaufnahme mit priorisierter Ma\u00dfnahmenliste. Auch einzeln beauftragbar, ohne Folgeauftrag.",
  u"Jetzt pr\u00fcfen"),
 (u"05", u"Reporting", u"reporting.html",
  u"Eine Seite, keine vierzig.",
  u"Positionen, Besucher aus der Suche und was umgesetzt wurde. Lesbar ohne Vorkenntnisse, wann immer Sie ihn brauchen.",
  u"Jetzt mitlesen"),
]
SVC_CARDS = u"".join(u"""
      <a class="svc-card" href="%s">
        <span class="svc-num">%s</span>
        <h3>%s</h3>
        <p class="svc-tag">%s</p>
        <p class="svc-txt">%s</p>
        <span class="svc-go">%s</span>
      </a>""" % (href, num, name, tag, txt, go) for num, name, href, tag, txt, go in SVC)

# ---------------------------------------------------------------- Leistungen overview
page("leistungen/index.html",
 u"Leistungen | Kontor",
 u"SEO, OnPage und Webdesign, Linkaufbau, SEO Audit und Reporting. Festpreis, keine Mindestlaufzeit.",
 hero(kicker=u"Leistungen",
   h1=u"Leistungen",
   lede=u"Je nach Ausgangslage liegt der Hebel woanders. Welcher es bei Ihnen ist, steht in der Analyse, bevor Sie etwas beauftragen.",
   cta_up="../") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="svc-grid">%s
    </div>
    <div class="prose" style="max-width:none">%s</div>
  </div>
</section>""" % (SVC_CARDS, cta("../")))

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
   u"Gekaufte Links aus Netzwerken, Verzeichnisse ohne eigenen Zweck und getauschte Links in großer Zahl. Das lässt sich erkennen, und der Schaden trifft die gesamte Domain. Wir machen das nicht, auch nicht auf Wunsch."),
  (u"Realistische Erwartung",
   u"Linkaufbau ist der langsamste Bereich. Vor den anderen lohnt er sich selten. Wenn Technik, Inhalte und lokale Präsenz stehen und es trotzdem nicht reicht, ist dies der nächste Schritt.")],
 u"Wie wir arbeiten", [
  u"Analyse, welche Quellen Ihre Wettbewerber verlinken",
  u"Erwähnungen Ihres Namens ohne Link finden und nachträglich verlinken lassen",
  u"Partner, Lieferanten und Verbände, bei denen ein Eintrag ohnehin naheliegt",
  u"Fachbeiträge, bei denen die Verlinkung aus dem Inhalt folgt"], accent=3,
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
      <button class="ref-filter" data-cat="ecommerce" aria-pressed="false">E-Commerce</button>
      <button class="ref-filter" data-cat="technik" aria-pressed="false">Technisches SEO</button>
      <button class="ref-filter" data-cat="content" aria-pressed="false">Content</button>
      <button class="ref-filter" data-cat="local" aria-pressed="false">Local SEO</button>
    </div>

    <div class="ref-grid" style="--case-accent:var(--c4)">
      <a class="ref-card" href="referenzen/poseypets.html" data-cats="ecommerce technik content local">
        <div class="ref-tile">
          <img src="assets/img/case/poseypets-napoleon.jpg" alt="Tierportrait auf Leinwand neben dem abgebildeten Dackel" loading="lazy" width="1200" height="1200">
          <div class="ref-tags"><span class="ref-tag">E-Commerce</span><span class="ref-tag">Organic</span><span class="ref-tag">Content</span></div>
          <span class="ref-go"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
        </div>
        <h3 class="ref-name">PoseyPets</h3>
        <p class="ref-desc">Onlineshop für Tierportraits, von Grund auf für die organische Suche aufgebaut. Keyword-Struktur, sechs Landingpages, zwei Inhaltsformate.</p>
      </a>
    </div>

    <p class="ref-empty" hidden>In dieser Kategorie liegt noch keine Fallstudie vor.</p>
  </div>
</section>""")

# ---------------------------------------------------------------- Fallstudie PoseyPets
page("referenzen/poseypets.html",
 u"Fallstudie PoseyPets | Kontor",
 u"Wie der Onlineshop PoseyPets von Grund auf für die organische Suche aufgebaut wurde: Keyword-Recherche, Seitenstruktur, Inhalte und Technik.",
 u"""<section class="section cs" style="padding-top:0">
  <div class="wrap">
    <div class="cs-hero">
      <img src="../assets/img/case/poseypets-wohnzimmer.jpg" alt="Tierportraits als Wanddekoration im Wohnzimmer" width="1200" height="600">
    </div>
    <h1 style="font-size:clamp(2rem,4.6vw,3.4rem);margin:0 0 18px">PoseyPets</h1>
    <p class="lede">Ein deutscher Onlineshop für individuelle Tierportraits. Der Kunde lädt ein Foto hoch, und sein Tier wird als historische Figur gemalt. Die Aufgabe: gefunden werden, ohne jeden Besucher einkaufen zu müssen.</p>
    <div class="tags" style="margin-top:20px"><span class="tag accent">E-Commerce</span><span class="tag">Technisches SEO</span><span class="tag">Content</span><span class="tag">Keyword-Strategie</span></div>
  </div>
</section>

<section class="section cs" style="padding-top:0">
  <div class="wrap prose">
    <p><em>Offenlegung: PoseyPets ist ein eigenes Projekt. Wir zeigen es, weil wir dort jeden Schritt selbst gegangen sind und offen darüber schreiben können, auch über das, was nicht funktioniert hat.</em></p>

    <h2>Ausgangssituation</h2>
    <p>Ein neuer Shop ohne Domainhistorie, in einem Umfeld, in dem bereits internationale Anbieter stehen. Zum Start war der Shop bei Google für keinen einzigen relevanten Begriff zu finden.</p>
    <p>Die naheliegende Alternative wäre gewesen, jeden Besucher über bezahlte Anzeigen einzukaufen. Das funktioniert, solange Budget da ist, und endet an dem Tag, an dem es aufhört. Bei einem Produkt mit begrenztem Warenkorbwert frisst es außerdem die Marge. Also sollte die organische Suche die tragende Säule werden.</p>

    <div class="cs-split">
      <img src="../assets/img/case/poseypets-caesar.jpg" alt="Hundeportrait im Stil eines römischen Kaisers" loading="lazy" width="600" height="600">
      <img src="../assets/img/case/poseypets-mona.jpg" alt="Katzenportrait im Stil der Mona Lisa" loading="lazy" width="600" height="600">
    </div>

    <h2>Keyword-Recherche</h2>
    <p>Der wichtigste Fund kam ganz am Anfang und hat die gesamte Struktur bestimmt: bei diesen Begriffen entscheidet die <strong>Schreibweise</strong> über den Erfolg.</p>

    <div class="cs-quote">
      <p>„Haustier Portrait“ und „Haustierportrait“ sind für Google nicht dasselbe Wort. Der Unterschied im Suchvolumen liegt beim Zehnfachen.</p>
    </div>

    <p>Und es gibt keine Regel dafür. Bei einem Tier gewinnt die getrennte Schreibweise deutlich, beim nächsten die zusammengeschriebene. Das muss pro Begriff geprüft werden, bevor irgendetwas geschrieben wird, denn die Schreibweise steckt später in Titeln, Überschriften und URLs und lässt sich nicht beiläufig ändern.</p>
    <p>Genauso wichtig war, was <em>aussortiert</em> wurde. Ein ganzer Begriffscluster sah nach viel Volumen aus, bestand aber fast vollständig aus Leuten, die selbst malen lernen wollen. Ein zweiter war komplett wertlos, weil die Suchenden etwas ganz anderes meinten. Beide wurden gestrichen, bevor Arbeit hineinfloss.</p>

    <figure class="cs-figure">
      <img src="../assets/img/case/poseypets-pferd.jpg" alt="Pferdeportrait nach Foto" loading="lazy" width="1200" height="900">
      <figcaption>Eigene Landingpage je Hauptbegriff, hier das Pferdemotiv</figcaption>
    </figure>

    <h2>Seitenstruktur</h2>
    <p>Daraus wurden sechs eigene Landingpages gebaut, je eine pro Hauptbegriff, nach einer einzigen Regel: <strong>ein Suchbegriff, eine Seite.</strong> Keine zwei Seiten konkurrieren um denselben Begriff, weil sie sich sonst gegenseitig die Position wegnehmen.</p>
    <p>Diese Seiten sind keine Textwüsten, sondern echte Produktübersichten. Wer über die Suche kommt, sieht sofort Produkte und nicht erst 800 Wörter Einleitung. Jede Produktseite bekam zusätzlich einen eigenen Textblock, der auf ihren eigenen Begriff zugeschnitten ist.</p>

    <h2>Inhalte</h2>
    <p>Zwei bewusst unterschiedliche Formate statt eines Blogs, weil sie zwei verschiedene Aufgaben haben:</p>
    <ul>
      <li><strong>Ratgeber</strong> für die ausführlichen Fragen, die sich jemand vor dem Kauf stellt.</li>
      <li><strong>Lexikon</strong> von A bis Z für die vielen kurzen Begriffssuchen, mit eigener Filterung.</li>
    </ul>
    <p>Dazu eine feste Regel für die interne Verlinkung: etwa 60 Prozent der Links zeigen auf Seiten, die verkaufen, 40 Prozent auf weitere Inhalte.</p>

    <div class="cs-note">
      <h3>Warum diese Regel</h3>
      <p>Ohne sie verlinkt ein Blog nach einiger Zeit fast nur noch sich selbst. Die Artikel ranken dann vielleicht, schieben aber keine Kraft mehr auf die Seiten, an denen tatsächlich Geld verdient wird.</p>
    </div>

    <div class="cs-split">
      <img src="../assets/img/case/poseypets-tasse.jpg" alt="Personalisierte Tasse mit Tierportrait" loading="lazy" width="600" height="600">
      <img src="../assets/img/case/poseypets-unboxing.jpg" alt="Ausgepacktes Tierportrait" loading="lazy" width="600" height="600">
    </div>

    <h2>Technik</h2>
    <p>Vollständige Metadaten über alle Produkte und Kategorien, eine FAQ mit passender Auszeichnung für die Suchergebnisse, Ladezeit und mobile Darstellung, und eine saubere interne Verlinkung bis in den Footer.</p>
    <p>Eine Entscheidung dabei war, bestehende URLs <em>nicht</em> umzuziehen, obwohl eine andere Struktur auf dem Papier schöner gewesen wäre. Die Seiten rankten bereits.</p>

    <div class="cs-quote">
      <p>Einen vorhandenen Rankingaufbau für eine kosmetische Verbesserung wegzuwerfen, ist einer der teuersten Fehler überhaupt. Wir sehen ihn ständig.</p>
    </div>

    <h2>Stand heute</h2>
    <p>Der Shop ist live, verkauft und läuft geschäftlich gut. Die Sichtbarkeit baut sich weiter auf, die Landingpages ranken für ihre jeweiligen Begriffe, und es kommen laufend Inhalte dazu. SEO ist hier kein abgeschlossenes Projekt, sondern die Grundlage, auf der weitergearbeitet wird.</p>

    <figure class="cs-figure">
      <img src="../assets/img/case/poseypets-valentin.jpg" alt="Tierportrait als Geschenk" loading="lazy" width="1200" height="900">
      <figcaption>Saisonale Anlässe als eigene Einstiegspunkte in die Suche</figcaption>
    </figure>

    <h2>Was daraus für andere folgt</h2>
    <p><strong>Die Reihenfolge entscheidet.</strong> Zuerst prüfen, welche Suchbegriffe überhaupt zu Umsatz führen, dann die Seiten dafür bauen, erst danach Inhalte produzieren. Wer umgekehrt anfängt, schreibt Texte für Suchanfragen, die nie zu einer Anfrage führen, und merkt es erst nach Monaten.</p>
    <p><strong>Und die Schreibweise prüfen.</strong> Eine falsch gewählte Variante kostet dauerhaft den Großteil des möglichen Volumens, weil sie in Titeln, URLs und Überschriften steckt. Diese halbe Stunde am Anfang ist die billigste Stunde im ganzen Projekt.</p>
    """ + cta("../") + u"""
  </div>
</section>""")

# ---------------------------------------------------------------- Kontakt
page("kontakt.html",
 u"Kontakt und kostenlose SEO-Analyse | Kontor",
 u"Fordern Sie die kostenlose SEO-Analyse für Ihre Website an.",
 hero(kicker=u"Kontakt",
   h1=u"Kostenlose SEO-Analyse.",
   lede=u"Schreiben Sie kurz, um welche Website es geht. Sie bekommen die Analyse schriftlich und unverbindlich.") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap serp-grid">
    <div class="prose">
      <h2 style="margin-top:0">Direkt erreichbar</h2>
      <!-- TODO: Adresse auf das neue Postfach umstellen, sobald die Domain steht -->
      <p><strong>E-Mail:</strong> <a href="mailto:kontakt@beispiel.de">kontakt@beispiel.de</a><br>
         <strong>Telefon:</strong> <a href="tel:+491771885605">+49 177 188 5605</a></p>
      <h3>Was wir für die Analyse brauchen</h3>
      <ul>
        <li>Ihre Website</li>
        <li>Ihr Ort oder Einzugsgebiet</li>
        <li>Die zwei bis drei Leistungen, über die Sie am liebsten Anfragen bekommen</li>
      </ul>
      <p>Antwort in der Regel innerhalb eines Werktags.</p>
    </div>
    <div>
      <!-- TODO: Terminbuchung einsetzen. GitHub Pages ist statisch, es gibt kein
           Backend. Also entweder die Google Buchungsseite (in Workspace Business
           Starter enthalten) oder eine Serverless Funktion. -->
      <div class="band ph">
        <div class="band-in">
          <span class="kicker">Platzhalter</span>
          <h2 style="font-size:clamp(1.4rem,2.6vw,2rem);margin:12px 0">Terminbuchung</h2>
          <p class="lede">Hier kommt der Buchungskalender hin.</p>
        </div>
      </div>
    </div>
  </div>
</section>""")

# ---------------------------------------------------------------- Blog
page("blog/index.html",
 u"Blog | Kontor",
 u"Artikel über Suchmaschinenoptimierung, ohne Fachchinesisch.",
 hero(kicker=u"Blog",
   h1=u"Blog",
   lede=u"Kurze Artikel zu den Fragen, die uns Kunden immer wieder stellen.") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap">
    <!-- TODO: Artikel als eigene Seiten anlegen und hier verlinken. -->
    <div class="posts">
      <article class="post"><span class="meta">Grundlagen</span><h3>Warum findet mich bei Google niemand?</h3><p>Die fünf Ursachen, die in den meisten Fällen dahinterstecken.</p><span class="more">Bald verfügbar</span></article>
      <article class="post"><span class="meta">Lokales SEO</span><h3>Google Unternehmensprofil richtig einrichten</h3><p>Welche Felder zählen und welcher Fehler am meisten Sichtbarkeit kostet.</p><span class="more">Bald verfügbar</span></article>
      <article class="post"><span class="meta">Technik</span><h3>Core Web Vitals, kurz erklärt</h3><p>Was Google misst und ab wann sich die Ladezeit auf die Position auswirkt.</p><span class="more">Bald verfügbar</span></article>
    </div>
  </div>
</section>""")

# ---------------------------------------------------------------- Impressum
page("impressum.html", u"Impressum | Kontor", u"Impressum nach § 5 DDG.",
 hero(kicker=u"Pflichtangaben", h1=u"Impressum.", lede=u"Angaben gemäß § 5 DDG.") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap prose">
    <!-- Übernommen aus dem Impressum von poseypets.com, auf diese Tätigkeit
         angepasst. OFFEN: Marken- bzw. Firmierung und die E-Mail-Adresse auf
         der neuen Domain eintragen, sobald beides steht. -->
    <p style="color:var(--warn)"><strong>Offen: Firmierung und E-Mail-Adresse auf der neuen Domain eintragen.</strong></p>
    <h2>Diensteanbieter</h2>
    <p>Alejandro Arndt<br>Albstraße 54<br>73066 Uhingen<br>Deutschland</p>
    <h2>Kontakt</h2>
    <p>Telefon: +49 177 188 5605<br>E-Mail: kontakt@beispiel.de</p>
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
    <h2>Kontaktaufnahme</h2>
    <p>Wenn Sie uns per E-Mail oder Telefon kontaktieren, verarbeiten wir Ihre Angaben ausschließlich zur Bearbeitung Ihrer Anfrage. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO bei vorvertraglichen Maßnahmen, sonst Art. 6 Abs. 1 lit. f DSGVO. Die Daten werden gelöscht, sobald sie nicht mehr erforderlich sind und keine gesetzlichen Aufbewahrungsfristen entgegenstehen.</p>
    <h2>Ihre Rechte</h2>
    <p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch gegen die Verarbeitung. Außerdem steht Ihnen ein Beschwerderecht bei einer Datenschutzaufsichtsbehörde zu.</p>
  </div>
</section>""", robots="noindex,follow")

print("ok")
