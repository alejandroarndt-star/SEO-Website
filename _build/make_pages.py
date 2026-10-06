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
 u"Leistungen | SEO-Agentur",
 u"Technisches SEO, OnPage und Inhalte, lokales SEO, Linkaufbau, SEO Audit und Reporting. Festpreis, keine Mindestlaufzeit.",
 HERO.format(kicker=u"Leistungen",
   h1=u"Sechs Bereiche, die zusammen die Position ergeben.",
   lede=u"Je nach Ausgangslage liegt der Hebel woanders. Welcher es bei Ihnen ist, steht in der Analyse, bevor Sie etwas beauftragen.") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="index">
      <a class="index-row" href="technisches-seo.html"><span class="idx">01</span><h3>Technisches SEO</h3><p>Ladezeit, Core Web Vitals, Indexierung und Seitenstruktur. Die Grundlage, ohne die der Rest wenig bringt.</p></a>
      <a class="index-row" href="onpage-und-inhalte.html"><span class="idx">02</span><h3>OnPage und Inhalte</h3><p>Seitenstruktur, Überschriften, interne Verlinkung und Texte, die eine konkrete Suchabsicht beantworten.</p></a>
      <a class="index-row" href="lokales-seo.html"><span class="idx">03</span><h3>Lokales SEO</h3><p>Google Unternehmensprofil, Kartenbereich, Verzeichnisse und Bewertungen.</p></a>
      <a class="index-row" href="linkaufbau.html"><span class="idx">04</span><h3>Linkaufbau</h3><p>Erwähnungen und Verlinkungen aus Quellen, die tatsächlich etwas zählen.</p></a>
      <a class="index-row" href="seo-audit.html"><span class="idx">05</span><h3>SEO Audit</h3><p>Vollständige Bestandsaufnahme, auch einzeln beauftragbar.</p></a>
      <a class="index-row" href="reporting.html"><span class="idx">06</span><h3>Reporting</h3><p>Monatlich auf einer Seite, verständlich, ohne Fachchinesisch.</p></a>
    </div>
    <div class="prose" style="max-width:none">%s</div>
  </div>
</section>""" % cta("../"))

service("leistungen/technisches-seo.html",
 u"Technisches SEO | Markenname",
 u"Ladezeit, Core Web Vitals, Indexierung und Seitenstruktur. Die technische Grundlage für bessere Positionen bei Google.",
 u"Leistung 01", u"Technisches SEO.",
 u"Eine Seite kann die besten Texte der Welt haben. Wenn Google sie nicht sauber lesen, einordnen und schnell ausliefern kann, bleibt sie unten.",
 [(u"Was dazugehört",
   u"Ladezeit und Core Web Vitals, die Darstellung auf dem Handy, saubere Weiterleitungen, eine nachvollziehbare URL Struktur, korrekte Canonicals und eine Sitemap, die auch stimmt. Dazu strukturierte Daten, damit Google versteht, worum es auf einer Seite geht."),
  (u"Warum das zuerst kommt",
   u"Technische Fehler wirken wie eine Bremse auf alles andere. Wer Inhalte produziert, während die Hälfte der Seiten gar nicht im Index ist, zahlt für Arbeit, die nicht ankommt. Deshalb steht dieser Bereich am Anfang und ist meist auch der, in dem am meisten liegen bleibt."),
  (u"Wie wir vorgehen",
   u"Zuerst eine Bestandsaufnahme mit Crawl und Search Console. Daraus entsteht eine Liste nach Wirkung sortiert, nicht nach Aufwand. Dann wird abgearbeitet, und Sie sehen im Bericht, welcher Punkt erledigt ist und was sich daraufhin bewegt hat.")],
 u"Typische Funde", [
  u"Seiten, die durch robots.txt oder noindex versehentlich blockiert sind",
  u"Bilder in Originalgröße, die die Ladezeit auf dem Handy verdoppeln",
  u"Mehrere URLs mit demselben Inhalt, die sich gegenseitig Konkurrenz machen",
  u"Weiterleitungsketten aus einem alten Relaunch",
  u"Fehlende oder doppelte Seitentitel über ganze Bereiche hinweg"])

service("leistungen/onpage-und-inhalte.html",
 u"OnPage und Inhalte | Markenname",
 u"Seitenstruktur, Überschriften, interne Verlinkung und Texte, die eine konkrete Suchabsicht beantworten.",
 u"Leistung 02", u"OnPage und Inhalte.",
 u"Google rankt keine Unternehmen, sondern einzelne Seiten. Für jeden Suchbegriff, der Ihnen etwas bringt, braucht es eine Seite, die genau diese Frage beantwortet.",
 [(u"Eine Seite, eine Suchabsicht",
   u"Die häufigste Schwachstelle ist eine einzige Leistungsseite, auf der alles gleichzeitig steht. Google kann daraus nicht ableiten, wofür Sie der beste Treffer sind. Besser ist eine eigene Seite je Leistung, die eine Frage vollständig beantwortet."),
  (u"Suchabsicht vor Suchvolumen",
   u"Ein Begriff mit tausend Suchen im Monat ist wertlos, wenn die Leute dahinter nur vergleichen. Ein Begriff mit dreißig Suchen kann jeden Monat Aufträge bringen, wenn dahinter jemand mit konkretem Bedarf sitzt. Wir sortieren nach dem, was Anfragen auslöst."),
  (u"Interne Verlinkung",
   u"Links innerhalb der eigenen Seite entscheiden mit, welche Seite Google für wichtig hält. Eine Seite, auf die von nirgendwo verlinkt wird, hat es schwer, egal wie gut der Text ist.")],
 u"Was Sie bekommen", [
  u"Eine Keyword Zuordnung: welcher Begriff auf welche Seite gehört",
  u"Titel und Beschreibungen, die auch angeklickt werden",
  u"Eine Gliederung pro Seite, die der Suchabsicht folgt",
  u"Vorschläge für fehlende Seiten statt längerer Texte auf bestehenden",
  u"Interne Links von den starken auf die wichtigen Seiten"])

service("leistungen/lokales-seo.html",
 u"Lokales SEO | Markenname",
 u"Google Unternehmensprofil, Kartenbereich, Branchenverzeichnisse und Bewertungen für Unternehmen mit Einzugsgebiet.",
 u"Leistung 03", u"Lokales SEO.",
 u"Bei fast jeder Suche mit Ortsbezug zeigt Google zuerst drei Einträge mit Karte, Telefonnummer und Bewertungen. Darüber läuft ein großer Teil der Anrufe, bevor jemand die normalen Treffer überhaupt sieht.",
 [(u"Der Kartenbereich steht über allem",
   u"Wer dort nicht auftaucht, verliert Anfragen an Wettbewerber, die weniger gut sind, aber besser gepflegt. Das Google Unternehmensprofil ist kostenlos und bei vielen Unternehmen der schnellste Hebel überhaupt."),
  (u"Einheitliche Daten",
   u"Name, Adresse und Telefonnummer müssen überall identisch sein, auf der Website, im Profil und in den Verzeichnissen. Abweichungen kosten Vertrauen bei Google und sind einer der häufigsten Gründe, warum ein Eintrag nicht nach oben kommt."),
  (u"Bewertungen",
   u"Bewertungen wirken auf die Position und noch stärker auf die Entscheidung, wer angerufen wird. Wir zeigen Ihnen, wie Sie seriös danach fragen. Gekaufte Bewertungen fliegen auf und schaden mehr, als sie je bringen.")],
 u"Besonders relevant für", [
  u"Unternehmen mit festem Standort und Laufkundschaft",
  u"Dienstleister mit Einzugsgebiet statt Ladenlokal",
  u"Betriebe mit mehreren Filialen oder Servicegebieten",
  u"Praxen, Kanzleien und Beratungen"])

service("leistungen/linkaufbau.html",
 u"Linkaufbau | Markenname",
 u"Erwähnungen und Verlinkungen aus Quellen, die tatsächlich zählen. Ohne gekaufte Linknetzwerke.",
 u"Leistung 04", u"Linkaufbau.",
 u"Links von anderen Seiten sind weiterhin einer der stärksten Faktoren. Entscheidend ist aber nicht die Anzahl, sondern woher sie kommen und ob sie plausibel sind.",
 [(u"Was zählt",
   u"Ein Link aus einem regionalen Nachrichtenportal, einem Branchenverband, einem Partnerunternehmen oder einem Fachbeitrag. Also Quellen, bei denen eine Erwähnung auch ohne SEO Sinn ergeben würde."),
  (u"Was schadet",
   u"Gekaufte Links aus Netzwerken, Verzeichnisse ohne eigenen Zweck und getauschte Links in großer Zahl. Das lässt sich erkennen, und der Schaden trifft die gesamte Domain, nicht nur die verlinkte Seite. Wir machen das nicht, auch nicht auf Wunsch."),
  (u"Realistische Erwartung",
   u"Linkaufbau ist der langsamste der sechs Bereiche. Vor den anderen fünf lohnt er sich selten. Wenn Technik, Inhalte und lokale Präsenz stehen und es trotzdem nicht reicht, ist dies der nächste Schritt.")],
 u"Wie wir arbeiten", [
  u"Analyse, welche Quellen Ihre Wettbewerber verlinken",
  u"Erwähnungen Ihres Namens ohne Link finden und nachträglich verlinken lassen",
  u"Partner, Lieferanten und Verbände, bei denen ein Eintrag ohnehin naheliegt",
  u"Fachbeiträge, bei denen die Verlinkung aus dem Inhalt folgt"])

service("leistungen/seo-audit.html",
 u"SEO Audit | Markenname",
 u"Vollständige Bestandsaufnahme Ihrer Website: was blockiert, was Potenzial hat, in welcher Reihenfolge. Auch einzeln beauftragbar.",
 u"Leistung 05", u"SEO Audit.",
 u"Eine vollständige Bestandsaufnahme, bevor irgendetwas umgesetzt wird. Auch einzeln beauftragbar, ohne laufende Betreuung und ohne Folgeauftrag.",
 [(u"Was drin steht",
   u"Technischer Zustand, Inhalte und Suchbegriffe, lokale Präsenz, Verlinkung und ein direkter Vergleich mit drei Wettbewerbern. Am Ende eine nach Wirkung sortierte Liste, keine Sammlung von Hinweisen."),
  (u"Für wen sich das lohnt",
   u"Für Unternehmen, die wissen wollen, woran sie sind, bevor sie ein Budget binden. Und für alle, die bereits mit einer Agentur arbeiten und eine unabhängige zweite Meinung möchten."),
  (u"Was danach passiert",
   u"Nichts, wenn Sie das so wollen. Das Audit gehört Ihnen, Sie können es intern oder mit einem anderen Dienstleister umsetzen. Wenn wir weitermachen sollen, bekommen Sie dafür einen Festpreis.")],
 u"Umfang", [
  u"Vollständiger Crawl der Website",
  u"Auswertung von Search Console und Ladezeitdaten",
  u"Keyword Zuordnung und Lücken im Vergleich zum Wettbewerb",
  u"Prüfung des Google Unternehmensprofils und der Verzeichnisse",
  u"Priorisierte Maßnahmenliste mit Aufwandseinschätzung"])

service("leistungen/reporting.html",
 u"Reporting | Markenname",
 u"Monatlicher SEO Bericht auf einer Seite: welche Suchbegriffe sich bewegt haben, woher die Besucher kamen, was als Nächstes ansteht.",
 u"Leistung 06", u"Reporting.",
 u"Ein Bericht, den man ohne Vorkenntnisse lesen kann. Eine Seite, jeden Monat, mit den Zahlen, die tatsächlich etwas über das Geschäft aussagen.",
 [(u"Was drin steht",
   u"Positionen für die vereinbarten Suchbegriffe und die Veränderung zum Vormonat, Besucher aus der Suche, Anrufe und Anfragen soweit messbar, und was im Monat umgesetzt wurde. Dazu der nächste Schritt."),
  (u"Was nicht drin steht",
   u"Keine 40 Seiten aus einem Tool, keine Kennzahlen ohne Bezug zum Geschäft, keine Diagramme, die gut aussehen und nichts aussagen. Wenn ein Monat schlecht lief, steht das so im Bericht."),
  (u"Messbar ohne Tracking auf Besucherebene",
   u"Die Daten stammen aus der Google Search Console und aus Ihrem Unternehmensprofil. Dafür ist kein Tracking Cookie und kein Banner auf Ihrer Seite nötig.")],
 u"Rhythmus", [
  u"Monatlicher Bericht per E-Mail, eine Seite",
  u"Quartalsgespräch, wenn Sie es möchten, sonst nicht",
  u"Jederzeit erreichbar bei Fragen, ohne Ticketsystem"])

# ---------------------------------------------------------------- Referenzen
page("referenzen.html",
 u"Referenzen | Markenname",
 u"Projekte und Ergebnisse.",
 HERO.format(kicker=u"Referenzen",
   h1=u"Projekte und Ergebnisse.",
   lede=u"Belegbare Zahlen aus echten Projekten statt Logos ohne Zusammenhang.") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap prose">
    <!-- ====================================================================
         PLATZHALTER. Hier kommt die PosyPets Referenz hin, mit echten,
         belegbaren Zahlen. Bis dahin steht hier bewusst KEINE erfundene
         Referenz: erfundene Ergebnisse auf einer SEO Seite sind
         wettbewerbsrechtlich angreifbar und zerstören genau das Vertrauen,
         das die Seite aufbauen soll.
         ==================================================================== -->
    <p style="color:var(--warn)"><strong>Platzhalter. Vor dem Start die PosyPets Referenz mit echten Zahlen einsetzen.</strong></p>
    <p>Diese Seite wird gerade aufgebaut. Wenn Sie vorab wissen möchten, wie wir arbeiten und was realistisch erreichbar ist, fordern Sie die kostenlose Analyse an. Darin sehen Sie am eigenen Beispiel, was möglich ist, statt an fremden Zahlen.</p>
    %s
  </div>
</section>""" % cta())

# ---------------------------------------------------------------- Kontakt
page("kontakt.html",
 u"Kontakt und kostenlose SEO-Analyse | Markenname",
 u"Fordern Sie die kostenlose SEO-Analyse für Ihre Website an oder vereinbaren Sie direkt einen Termin.",
 HERO.format(kicker=u"Kontakt",
   h1=u"Kostenlose SEO-Analyse.",
   lede=u"Schreiben Sie kurz, um welche Website es geht. Sie bekommen die Analyse schriftlich, kostenlos und ohne Verpflichtung.") + u"""
<section class="section" style="padding-top:0">
  <div class="wrap serp-grid">
    <div class="prose">
      <h2 style="margin-top:0">Direkt erreichbar</h2>
      <!-- TODO: echte Kontaktdaten eintragen, sobald Domain und Postfach stehen -->
      <p><strong>E-Mail:</strong> <a href="mailto:kontakt@beispiel.de">kontakt@beispiel.de</a><br>
         <strong>Telefon:</strong> <a href="tel:+491771885605">+49 177 188 5605</a></p>
      <h3>Was wir für die Analyse brauchen</h3>
      <ul>
        <li>Ihre Website</li>
        <li>Ihr Ort oder Einzugsgebiet</li>
        <li>Die zwei bis drei Leistungen, über die Sie am liebsten Anfragen bekommen</li>
      </ul>
      <p>Mehr nicht. Den Rest finden wir selbst heraus. Antwort in der Regel innerhalb eines Werktags.</p>
    </div>
    <div>
      <!-- TODO: Terminbuchung einsetzen. GitHub Pages ist statisch, es gibt kein
           Backend. Ein Formular braucht also entweder die Google Buchungsseite
           (in Workspace Business Starter enthalten) oder eine Serverless Funktion. -->
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
    <!-- ====================================================================
         PLATZHALTER. Vor dem Start vollständig ausfüllen. Pflicht sind unter
         anderem: voller Klarname, ladungsfähige Anschrift (kein Postfach),
         E-Mail-Adresse, Telefonnummer und, falls vorhanden, die
         Umsatzsteuer-Identifikationsnummer nach § 27a UStG.
         ==================================================================== -->
    <p style="color:var(--warn)"><strong>Platzhalter. Vor dem Start vollständig ausfüllen.</strong></p>
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
    <!-- PLATZHALTER, inhaltlich aber bereits auf DIESE Seite zugeschnitten.
         NICHT die Datenschutzerklärung von PosyPets übernehmen: dort steht ein
         anderer Hoster. Hier ist GitHub der Hoster, das muss drinstehen. -->
    <p style="color:var(--warn)"><strong>Platzhalter. Vor dem Start prüfen und die Verantwortlichen-Angaben ergänzen.</strong></p>
    <h2>Verantwortlicher</h2>
    <p>Vorname Nachname, Anschrift, E-Mail. Siehe <a href="impressum.html">Impressum</a>.</p>
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
