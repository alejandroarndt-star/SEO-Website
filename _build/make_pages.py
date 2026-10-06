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
<link rel="preload" href="{up}assets/fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{up}assets/fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{up}assets/css/site.css">
<meta name="theme-color" content="#0B0B0C">
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
    html = SHELL.format(title=title, desc=desc, robots=robots, up=up,
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
    <h1 style="font-size:clamp(2rem,4.6vw,3.4rem);max-width:20ch;margin:14px 0 18px">{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>"""

def cta(up=""):
    return u"""<div class="band" style="margin-top:46px">
      <div class="band-in">
        <span class="kicker">Kostenlos und unverbindlich</span>
        <h2 style="margin:12px 0 14px">Wo steht Ihre Seite gerade?</h2>
        <p class="lede">Sie bekommen schriftlich, für welche Suchbegriffe Sie gefunden werden, wer vor Ihnen steht und woran es liegt.</p>
        <div class="hero-cta"><a href="%skontakt.html" class="btn btn-primary">Kostenlose SEO-Analyse<span class="arr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></a></div>
      </div>
    </div>""" % up

def service(path, title, desc, kicker, h1, lede, sections, bullets_title, bullets):
    body = HERO.format(kicker=kicker, h1=h1, lede=lede)
    inner = "".join(u"\n    <h2>%s</h2>\n    <p>%s</p>" % (h, t) for h, t in sections)
    lis = "".join(u"\n      <li>%s</li>" % b for b in bullets)
    body += u"""
<section class="section" style="padding-top:0">
  <div class="wrap prose">%s
    <h2>%s</h2>
    <ul>%s
    </ul>
    %s
  </div>
</section>""" % (inner, bullets_title, lis, cta("../"))
    page(path, title, desc, body)

# ---------------------------------------------------------------- Leistungen overview
page("leistungen/index.html",
 u"Leistungen | Markenname",
 u"SEO, OnPage und Webdesign, Linkaufbau, SEO Audit und Reporting. Festpreis, keine Mindestlaufzeit.",
 HERO.format(kicker=u"Leistungen",
   h1=u"Fünf Bereiche, die zusammen die Position ergeben.",
   lede=u"Je nach Ausgangslage liegt der Hebel woanders. Welcher es bei Ihnen ist, steht in der Analyse, bevor Sie etwas beauftragen.") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="index">
      <a class="index-row" href="seo.html"><span class="idx">01</span><h3>SEO</h3><p>Technik, Inhalte und lokale Sichtbarkeit als ein Paket.</p></a>
      <a class="index-row" href="onpage-und-webdesign.html"><span class="idx">02</span><h3>OnPage und Webdesign</h3><p>Aufbau, Gestaltung und Texte der Seiten, die ranken sollen.</p></a>
      <a class="index-row" href="linkaufbau.html"><span class="idx">03</span><h3>Linkaufbau</h3><p>Verlinkungen aus Quellen, die tatsächlich zählen.</p></a>
      <a class="index-row" href="seo-audit.html"><span class="idx">04</span><h3>SEO Audit</h3><p>Vollständige Bestandsaufnahme, auch einzeln beauftragbar.</p></a>
      <a class="index-row" href="reporting.html"><span class="idx">05</span><h3>Reporting</h3><p>Ein Bericht, wann immer Sie ihn brauchen.</p></a>
    </div>
    <div class="prose" style="max-width:none">%s</div>
  </div>
</section>""" % cta("../"))

service("leistungen/seo.html",
 u"SEO | Markenname",
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
  u"Ein Unternehmensprofil mit abweichender Adresse oder Telefonnummer"])

service("leistungen/onpage-und-webdesign.html",
 u"OnPage und Webdesign | Markenname",
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
  u"Gestaltung und Aufbau der Seiten, die Anfragen bringen sollen"])

service("leistungen/linkaufbau.html",
 u"Linkaufbau | Markenname",
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
  u"Fachbeiträge, bei denen die Verlinkung aus dem Inhalt folgt"])

service("leistungen/seo-audit.html",
 u"SEO Audit | Markenname",
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
  u"Priorisierte Maßnahmenliste mit Aufwandseinschätzung"])

service("leistungen/reporting.html",
 u"Reporting | Markenname",
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
  u"Erreichbar bei Fragen, ohne Ticketsystem"])

# ---------------------------------------------------------------- Referenzen
page("referenzen.html",
 u"Fallstudie PosyPets | Markenname",
 u"Wie der Onlineshop PosyPets von Grund auf für die organische Suche aufgebaut wurde: Keyword-Recherche, Seitenstruktur, Inhalte und Technik.",
 HERO.format(kicker=u"Fallstudie",
   h1=u"PosyPets.",
   lede=u"Ein deutscher Onlineshop für individuelle Tierportraits, aufgebaut mit dem Ziel, über die organische Suche gefunden zu werden statt über bezahlte Anzeigen.") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap prose">
    <p><em>Offenlegung: PosyPets ist ein eigenes Projekt. Wir zeigen es, weil wir dort jeden Schritt selbst gegangen sind und offen darüber schreiben können, auch über das, was nicht funktioniert hat.</em></p>

    <h2>Ausgangssituation</h2>
    <p>Ein neuer Shop ohne Domainhistorie in einem Umfeld, in dem bereits internationale Anbieter stehen. Bei Google war der Shop zum Start für keinen relevanten Begriff zu finden.</p>
    <p>Die Alternative wäre gewesen, jeden einzelnen Besucher über bezahlte Anzeigen einzukaufen. Bei einem Produkt mit begrenztem Warenkorbwert frisst das die Marge auf, und die Reichweite endet an dem Tag, an dem das Budget endet. Deshalb sollte die organische Suche die tragende Säule werden.</p>

    <h2>Keyword-Recherche</h2>
    <p>Der wichtigste Fund kam ganz am Anfang und hat die gesamte Struktur bestimmt: bei diesen Begriffen entscheidet die Schreibweise über den Erfolg. Getrennt oder zusammengeschrieben ist nicht dasselbe Wort, und der Unterschied im Suchvolumen liegt beim Zehnfachen. Bei einem Tier gewinnt die getrennte Schreibweise deutlich, beim nächsten die zusammengeschriebene. Es gibt keine Regel, das muss pro Begriff geprüft werden.</p>
    <p>Genauso wichtig war, was aussortiert wurde. Ein ganzer Begriffscluster sah nach viel Volumen aus, bestand aber fast vollständig aus Leuten, die selbst malen lernen wollen. Ein zweiter Cluster war komplett wertlos, weil die Suchenden etwas völlig anderes meinten. Beide wurden gestrichen, bevor Arbeit hineinfloss.</p>

    <h2>Seitenstruktur</h2>
    <p>Daraus wurden sechs eigene Landingpages gebaut, je eine pro Hauptbegriff, nach der Regel: ein Suchbegriff, eine Seite. Keine zwei Seiten konkurrieren um denselben Begriff.</p>
    <p>Diese Seiten sind keine Textwüsten, sondern echte Produktübersichten. Wer über die Suche kommt, sieht sofort Produkte und nicht erst 800 Wörter Einleitung. Jede Produktseite bekam zusätzlich einen eigenen Textblock, der auf ihren eigenen Begriff zugeschnitten ist.</p>

    <h2>Inhalte</h2>
    <p>Zwei bewusst unterschiedliche Formate statt eines Blogs:</p>
    <ul>
      <li><strong>Ratgeber</strong> für die ausführlichen Fragen, die sich jemand vor dem Kauf stellt.</li>
      <li><strong>Lexikon</strong> von A bis Z für die vielen kurzen Begriffssuchen, mit eigener Filterung.</li>
    </ul>
    <p>Dazu eine feste Regel für die interne Verlinkung: etwa 60 Prozent der Links zeigen auf Seiten, die verkaufen, 40 Prozent auf weitere Inhalte. Ohne so eine Regel verlinkt ein Blog irgendwann nur noch sich selbst und schiebt keine Kraft mehr auf die Seiten, die Umsatz bringen.</p>

    <h2>Technik</h2>
    <p>Vollständige Metadaten über alle Produkte und Kategorien, eine FAQ mit passender Auszeichnung für die Suchergebnisse, Ladezeit und mobile Darstellung, und eine saubere interne Verlinkung bis in den Footer.</p>
    <p>Eine Entscheidung dabei war, bestehende URLs <em>nicht</em> umzuziehen, obwohl eine andere Struktur auf dem Papier schöner gewesen wäre. Die Seiten rankten bereits. Einen Rankingaufbau für eine kosmetische Verbesserung wegzuwerfen, ist ein teurer Fehler, den wir oft genug bei anderen sehen.</p>

    <h2>Stand heute</h2>
    <p>Der Shop ist live, verkauft und entwickelt sich geschäftlich gut. Die Sichtbarkeit baut sich weiter auf, die Landingpages ranken für ihre jeweiligen Begriffe, und die Inhalte kommen laufend dazu. SEO ist an dieser Stelle kein abgeschlossenes Projekt, sondern die Grundlage, auf der weitergearbeitet wird.</p>

    <h2>Was daraus für andere folgt</h2>
    <p>Die Reihenfolge entscheidet. Zuerst prüfen, welche Suchbegriffe überhaupt zu Umsatz führen, dann die Seiten dafür bauen, erst danach Inhalte produzieren. Wer umgekehrt anfängt, schreibt Texte für Suchanfragen, die nie zu einer Anfrage führen, und merkt es erst nach Monaten.</p>
    <p>Der zweite Punkt: eine Schreibweise, die falsch gewählt ist, kostet den Großteil des möglichen Volumens, und zwar dauerhaft, weil sie in Titeln, URLs und Überschriften steckt. Diese halbe Stunde Prüfung am Anfang ist die billigste Stunde im ganzen Projekt.</p>
    %s
  </div>
</section>""" % cta())

# ---------------------------------------------------------------- Kontakt
page("kontakt.html",
 u"Kontakt und kostenlose SEO-Analyse | Markenname",
 u"Fordern Sie die kostenlose SEO-Analyse für Ihre Website an.",
 HERO.format(kicker=u"Kontakt",
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
 u"Blog | Markenname",
 u"Artikel über Suchmaschinenoptimierung, ohne Fachchinesisch.",
 HERO.format(kicker=u"Blog",
   h1=u"SEO, erklärt wie am Telefon.",
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
page("impressum.html", u"Impressum | Markenname", u"Impressum nach § 5 DDG.",
 HERO.format(kicker=u"Pflichtangaben", h1=u"Impressum.", lede=u"Angaben gemäß § 5 DDG.") + u"""
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
page("datenschutz.html", u"Datenschutzerklärung | Markenname",
 u"Informationen zur Verarbeitung personenbezogener Daten auf dieser Website.",
 HERO.format(kicker=u"Datenschutz", h1=u"Datenschutzerklärung.",
   lede=u"Diese Website kommt ohne Cookies, ohne Tracking und ohne eingebettete Inhalte Dritter aus.") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap prose">
    <!-- Verantwortlicher aus dem PosyPets Datenschutz übernommen. Der REST ist
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
