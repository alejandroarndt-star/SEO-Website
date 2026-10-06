# -*- coding: utf-8 -*-
"""Generates the sub pages from the shared shell in index.html.
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

def depth_fix(html, d):
    """Rewrite root relative links for pages in a subdirectory."""
    if not d:
        return html
    up = "../" * d
    html = re.sub(r'(href|src)="(?!https?:|#|mailto:|tel:|/)', lambda m: '%s="%s' % (m.group(1), up), html)
    # bare in-page anchors must point back at the homepage from a subdirectory
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
<link rel="preload" href="{up}assets/fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{up}assets/fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{up}assets/css/site.css">
<meta name="theme-color" content="#09090B">
</head>
<body>
{header}
{mnav}
<main class="page-top">
{body}
</main>
{footer}
<script src="{up}assets/js/site.js" defer></script>
</body>
</html>
"""

def page(path, title, desc, body, robots="index,follow"):
    d = path.count("/")
    up = "../" * d
    html = SHELL.format(
        title=title, desc=desc, robots=robots, up=up,
        header=depth_fix(HEADER, d), mnav=depth_fix(MNAV, d),
        footer=depth_fix(FOOTER, d), body=body)
    out = os.path.join(ROOT, path)
    dirn = os.path.dirname(out)
    if dirn and not os.path.isdir(dirn):
        os.makedirs(dirn)
    io.open(out, "w", encoding="utf-8").write(html)
    print("wrote", path)

HERO = u"""<section class="section" style="padding-top:0">
  <div class="wrap">
    <span class="kicker">{kicker}</span>
    <h1 style="font-size:clamp(2.2rem,5.5vw,4rem);max-width:20ch;margin:16px 0 20px">{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>"""

# ---------------------------------------------------------------- Kontakt
page("kontakt.html",
 u"Kontakt und kostenloser Sichtbarkeits-Check",
 u"Fordern Sie den kostenlosen Sichtbarkeits-Check für Ihren Betrieb an oder vereinbaren Sie direkt einen Termin.",
 HERO.format(kicker=u"Kontakt",
   h1=u"Finden wir heraus, wo Sie stehen.",
   lede=u"Schreiben Sie mir kurz, welcher Betrieb Sie sind und in welcher Stadt Sie arbeiten. Sie bekommen den Sichtbarkeits-Check schriftlich, kostenlos und ohne Verpflichtung.") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap serp-grid">
    <div class="prose">
      <h2 style="margin-top:0">Direkt erreichbar</h2>
      <p>Am schnellsten geht es per E-Mail oder Telefon. Ich antworte in der Regel innerhalb eines Werktags.</p>
      <!-- TODO: echte Kontaktdaten eintragen, sobald Domain und Postfach stehen -->
      <p><strong>E-Mail:</strong> <a href="mailto:kontakt@beispiel.de">kontakt@beispiel.de</a><br>
         <strong>Telefon:</strong> <a href="tel:+491771885605">+49 177 188 5605</a></p>
      <h3>Was ich für den Check brauche</h3>
      <ul>
        <li>Name und Ort Ihres Betriebs</li>
        <li>Ihre Website, falls vorhanden</li>
        <li>Die zwei bis drei Leistungen, über die Sie am liebsten Aufträge bekommen</li>
      </ul>
      <p>Mehr nicht. Den Rest finde ich selbst heraus.</p>
    </div>
    <div>
      <!-- TODO: Terminbuchung einsetzen.
           Entweder die Buchungsseite aus Google Workspace Business Starter
           (dort bereits enthalten) oder die selbst gebaute Lösung.
           GitHub Pages ist statisch, eine eigene Buchung braucht einen
           externen Dienst oder eine Serverless Funktion. -->
      <div class="band ph">
        <div class="band-in">
          <span class="kicker">Platzhalter</span>
          <h2 style="font-size:clamp(1.4rem,2.6vw,2rem);margin:12px 0">Terminbuchung</h2>
          <p class="lede">Hier kommt der Buchungskalender hin. Bis dahin genügt eine E-Mail oder ein Anruf.</p>
        </div>
      </div>
    </div>
  </div>
</section>""")

# ---------------------------------------------------------------- Blog
page("blog/index.html",
 u"Blog, SEO verständlich erklärt",
 u"Artikel über Suchmaschinenoptimierung für Handwerksbetriebe und lokale Dienstleister, ohne Fachchinesisch.",
 HERO.format(kicker=u"Blog",
   h1=u"SEO, erklärt wie am Telefon.",
   lede=u"Kurze Artikel zu den Fragen, die Betriebe mir immer wieder stellen. Ohne Fachbegriffe, ohne Verkaufsgerede.") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap">
    <!-- TODO: Artikel als eigene Seiten anlegen und hier verlinken. -->
    <div class="posts">
      <article class="post"><span class="meta">Grundlagen</span><h3>Warum findet mich bei Google niemand?</h3><p>Die fünf Gründe, die bei kleinen Betrieben fast immer dahinterstecken.</p><span class="more">Bald verfügbar</span></article>
      <article class="post"><span class="meta">Lokales SEO</span><h3>Google Unternehmensprofil richtig einrichten</h3><p>Welche Felder wirklich zählen und welcher Fehler die meisten Betriebe Sichtbarkeit kostet.</p><span class="more">Bald verfügbar</span></article>
      <article class="post"><span class="meta">Bewertungen</span><h3>Wie viele Google Bewertungen brauchen Sie wirklich?</h3><p>Was Bewertungen für die Position bedeuten und wie Sie seriös danach fragen.</p><span class="more">Bald verfügbar</span></article>
    </div>
  </div>
</section>""")

# ---------------------------------------------------------------- Impressum
page("impressum.html", u"Impressum", u"Impressum nach § 5 DDG.",
 HERO.format(kicker=u"Pflichtangaben", h1=u"Impressum.", lede=u"Angaben gemäß § 5 DDG.") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap prose">
    <!-- ====================================================================
         PLATZHALTER. Vor dem Start vollständig ausfüllen.
         Pflicht sind unter anderem: voller Klarname, ladungsfähige Anschrift
         (kein Postfach), E-Mail-Adresse, Telefonnummer, und falls vorhanden
         Umsatzsteuer-Identifikationsnummer nach § 27a UStG.
         Die Angaben von PosyPets können als Vorlage dienen, müssen aber auf
         die neue Tätigkeit und die neue Firmierung angepasst werden.
         ==================================================================== -->
    <p style="color:var(--accent)"><strong>Platzhalter. Vor dem Start vollständig ausfüllen.</strong></p>
    <h2>Diensteanbieter</h2>
    <p>Vorname Nachname<br>Straße und Hausnummer<br>PLZ Ort<br>Deutschland</p>
    <h2>Kontakt</h2>
    <p>Telefon: +49 ...<br>E-Mail: kontakt@beispiel.de</p>
    <h2>Umsatzsteuer</h2>
    <p>Umsatzsteuer-Identifikationsnummer gemäß § 27a Umsatzsteuergesetz: DE ...<br>
       Alternativ, falls Kleinunternehmerregelung nach § 19 UStG: entsprechenden Hinweis ergänzen.</p>
    <h2>Verantwortlich für den Inhalt</h2>
    <p>Vorname Nachname, Anschrift wie oben.</p>
    <h2>Streitbeilegung</h2>
    <p>Ich bin nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
  </div>
</section>""", robots="noindex,follow")

# ---------------------------------------------------------------- Datenschutz
page("datenschutz.html", u"Datenschutzerklärung", u"Informationen zur Verarbeitung personenbezogener Daten auf dieser Website.",
 HERO.format(kicker=u"Datenschutz", h1=u"Datenschutzerklärung.", lede=u"Diese Website kommt ohne Cookies, ohne Tracking und ohne eingebettete Inhalte Dritter aus.") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap prose">
    <!-- ====================================================================
         PLATZHALTER, aber inhaltlich bereits auf DIESE Seite zugeschnitten.
         NICHT die Datenschutzerklärung von PosyPets übernehmen: dort steht
         ein anderer Hoster. Hier ist GitHub der Hoster, das muss drinstehen.
         Vor dem Start von einer fachkundigen Person prüfen lassen.
         ==================================================================== -->
    <p style="color:var(--accent)"><strong>Platzhalter. Vor dem Start prüfen und die Verantwortlichen-Angaben ergänzen.</strong></p>

    <h2>Verantwortlicher</h2>
    <p>Vorname Nachname, Anschrift, E-Mail. Siehe <a href="impressum.html">Impressum</a>.</p>

    <h2>Keine Cookies, kein Tracking</h2>
    <p>Diese Website setzt keine Cookies, verwendet keine Analyse- oder Trackingdienste und bindet keine Inhalte Dritter ein. Schriftarten und Videos werden vom eigenen Webspace ausgeliefert, es findet keine Verbindung zu Google Fonts oder zu einem Videoportal statt. Deshalb gibt es auch keinen Cookie-Banner.</p>

    <h2>Hosting durch GitHub Pages</h2>
    <p>Diese Website wird bei GitHub Pages gehostet, einem Dienst der GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA. Beim Aufruf der Seite verarbeitet GitHub technisch notwendige Zugriffsdaten, insbesondere die IP-Adresse, Datum und Uhrzeit des Zugriffs, die aufgerufene Seite, den verweisenden Link sowie Browser- und Betriebssystemangaben. Diese Verarbeitung ist für die Auslieferung und die Sicherheit der Website erforderlich.</p>
    <p>Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO, das berechtigte Interesse an einer sicheren und zuverlässigen Bereitstellung der Website. Da GitHub seinen Sitz in den USA hat, kann eine Übermittlung personenbezogener Daten in die USA nicht ausgeschlossen werden.</p>

    <h2>Kontaktaufnahme</h2>
    <p>Wenn Sie mich per E-Mail oder Telefon kontaktieren, verarbeite ich Ihre Angaben ausschließlich zur Bearbeitung Ihrer Anfrage. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO bei vorvertraglichen Maßnahmen, sonst Art. 6 Abs. 1 lit. f DSGVO. Die Daten werden gelöscht, sobald sie nicht mehr erforderlich sind und keine gesetzlichen Aufbewahrungsfristen entgegenstehen.</p>

    <h2>Ihre Rechte</h2>
    <p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch gegen die Verarbeitung. Außerdem steht Ihnen ein Beschwerderecht bei einer Datenschutzaufsichtsbehörde zu.</p>
  </div>
</section>""", robots="noindex,follow")

print("ok")
