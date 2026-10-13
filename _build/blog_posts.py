# -*- coding: utf-8 -*-
"""Die Blogbeitraege. Aufbau wie bei PoseyPets: zwei Formate mit zwei
Aufgaben. Ratgeber beantworten die ausfuehrlichen Fragen vor einer
Entscheidung, Lexikon-Eintraege die kurzen Begriffssuchen.

Jeder Beitrag: (slug, format, titel, teaser, lede, body).
Pro Beitrag gilt die 60/40-Regel fuer interne Links: die Mehrzahl zeigt
auf Leistungs- und Kontaktseiten, der Rest auf weitere Beitraege.
"""

import io as _io, os as _os
_DIR = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "artikel")

def _body(slug):
    """Beitragstext aus _build/artikel/<slug>.html."""
    with _io.open(_os.path.join(_DIR, slug + ".html"), encoding="utf-8") as f:
        return u"\n" + f.read()

# (slug, titel, teaser fuer die Karte, lede unter der Ueberschrift)
_RATGEBER = [
("warum-findet-mich-bei-google-niemand",
 u"Warum findet mich bei Google niemand?",
 u"Die fünf Ursachen, die in den meisten Fällen dahinterstecken.",
 u"Die Website ist online, sieht gut aus, und trotzdem kommt über Google niemand. Das hat fast immer eine von fünf Ursachen."),
("google-unternehmensprofil-einrichten",
 u"Google Unternehmensprofil richtig einrichten",
 u"Welche Felder zählen und welcher Fehler am meisten Sichtbarkeit kostet.",
 u"Der schnellste Hebel für Betriebe mit Kundschaft aus der Umgebung - und er kostet nichts."),
("was-kostet-seo",
 u"Was kostet SEO?",
 u"Die drei üblichen Abrechnungsmodelle und woran Sie unseriöse Angebote erkennen.",
 u"Eine ehrliche Antwort auf die Frage, auf die es keine Pauschalantwort gibt, aber eine klare Orientierung."),
("wie-lange-dauert-seo",
 u"Wie lange dauert SEO?",
 u"Was nach Wochen passiert, was nach Monaten und woran die Dauer wirklich hängt.",
 u"Eine realistische Zeitrechnung, aufgeteilt nach dem, was schnell geht, und dem, was dauert."),
("seo-agentur-oder-selbst-machen",
 u"SEO-Agentur oder selbst machen?",
 u"Was Sie ohne Vorkenntnisse selbst schaffen und wo es sich nicht lohnt.",
 u"Ein guter Teil der Arbeit lässt sich selbst erledigen. Bei welchem Teil das gilt und wo die Grenze liegt."),
("unserioese-seo-agentur-erkennen",
 u"Woran Sie eine unseriöse SEO-Agentur erkennen",
 u"Sieben Sätze, nach denen Sie das Gespräch beenden können.",
 u"SEO ist für Außenstehende schwer zu prüfen. Genau davon lebt ein Teil der Branche. Diese Zeichen sind eindeutig."),
("neue-website-fuer-seo",
 u"Brauche ich für SEO eine neue Website?",
 u"Meistens nicht. Wann ein Neubau trotzdem der günstigere Weg ist.",
 u"Die Frage kommt fast immer, und die Antwort ist seltener ja, als Agenturen behaupten."),
("keyword-recherche-fuer-einsteiger",
 u"Keyword-Recherche für Einsteiger",
 u"Wie Sie in einer Stunde herausfinden, wonach Ihre Kundschaft wirklich sucht.",
 u"Der Schritt, der über alles andere entscheidet, und der ohne Werkzeug weiter kommt, als die meisten denken."),
("core-web-vitals-erklaert",
 u"Core Web Vitals, kurz erklärt",
 u"Was Google misst und ab wann sich die Ladezeit auf die Position auswirkt.",
 u"Drei Messwerte, drei Alltagsfragen, ohne Fachchinesisch."),
("lokale-seo-handwerker-dienstleister",
 u"Lokale SEO für Handwerk und Dienstleistung",
 u"Wie Betriebe im Umkreis gefunden werden, bevor jemand die normalen Treffer ansieht.",
 u"Bei Suchen mit Ortsbezug entscheidet sich fast alles in den ersten drei Einträgen mit Karte."),
("keyword",
 u"Keywords richtig wählen: welcher Begriff auf welche Seite gehört",
 u"Ein Begriff, eine Seite. Was passiert, wenn diese Regel verletzt wird.",
 u"Ein Keyword ist der Satz, den jemand bei Google eingibt. Welche Ihrer Seiten dafür zuständig ist, muss vorher festgelegt sein, nicht hinterher."),
("suchintention",
 u"Suchintention verstehen: warum gute Seiten trotzdem nicht ranken",
 u"Die Erwartung hinter der Suche, und wie Sie sie in einer Minute ablesen.",
 u"Eine Seite kann gut geschrieben, schnell und technisch sauber sein und trotzdem nicht erscheinen. Dann liegt es meist an der Frage, die sie beantworten soll."),
("long-tail-keyword",
 u"Long-Tail-Keywords: weniger Suchen, mehr Aufträge",
 u"Warum dreißig Suchen im Monat mehr bringen können als dreitausend.",
 u"Lange, genaue Suchanfragen sind für Betriebe ohne großes Budget der einzige Weg, der von Anfang an funktioniert. Das hat drei Gründe."),
("meta-title",
 u"Meta-Title schreiben: die Überschrift, die über den Klick entscheidet",
 u"Ein Satz je Seite, und er bestimmt, ob überhaupt geklickt wird.",
 u"Der Meta-Title ist die Zeile, die im Suchergebnis als anklickbare Überschrift erscheint. Das Feld mit dem besten Verhältnis von Aufwand zu Wirkung."),
("meta-description",
 u"Meta-Description schreiben: der Text unter dem Treffer",
 u"Kein Rankingfaktor, aber entscheidend für die Zahl der Klicks.",
 u"Die Meta-Description steht im Suchergebnis unter dem Titel. Sie verändert Ihre Position nicht, wohl aber, wie viele Menschen sie nutzen."),
]

RATGEBER = [(sl, ti, te, le, _body(sl)) for sl, ti, te, le in _RATGEBER]

# Geplante Ratgeber. Solange hier kein Text steht, wird keine Seite erzeugt
# und Verweise darauf erscheinen als normaler Text statt als toter Link.
GEPLANT = [
("h1-ueberschrift", u"Überschriftenstruktur: H1, H2 und warum sie keine Gestaltung sind"),
("alt-text", u"Alt-Texte richtig schreiben: Bildersuche und Barrierefreiheit"),
("backlink", u"Backlinks aufbauen: was zählt, was schadet, was Geld verbrennt"),
("interne-verlinkung", u"Interne Verlinkung: Kraft auf die richtigen Seiten lenken"),
("indexierung", u"Indexierung prüfen: stehen Ihre Seiten überhaupt im Index?"),
("noindex", u"noindex richtig einsetzen und der Fehler, der Websites unsichtbar macht"),
("robots-txt", u"robots.txt verstehen: was sie steuert und was nicht"),
("sitemap", u"XML-Sitemap anlegen und richtig nutzen"),
("canonical-tag", u"Canonical-Tags: doppelte Inhalte sauber auflösen"),
("301-weiterleitung", u"301-Weiterleitungen beim Relaunch: die Liste, die Sie brauchen"),
("keyword-kannibalisierung", u"Keyword-Kannibalisierung erkennen und auflösen"),
("local-pack", u"Ins Local Pack kommen: die drei Einträge mit Karte"),
("search-console", u"Google Search Console: der Einstieg in Ihre eigenen Suchdaten"),
("strukturierte-daten", u"Strukturierte Daten: mehr Platz im Suchergebnis"),
("sichtbarkeitsindex", u"Sichtbarkeitsindex richtig lesen"),
]

# Meta Description je Beitrag: 140-160 Zeichen, Fokus-Keyword drin,
# keine Pfeile, keine Emojis, keine Gedankenstriche (Regel 3).
META = {
"warum-findet-mich-bei-google-niemand": u"Bei Google nicht gefunden zu werden hat fast immer eine von fünf Ursachen. Woran es liegt, wie Sie es selbst prüfen und was Sie zuerst angehen sollten.",
"google-unternehmensprofil-einrichten": u"Das Google Unternehmensprofil richtig einrichten: welche Felder über die Platzierung entscheiden und welcher Fehler am meisten Sichtbarkeit kostet.",
"was-kostet-seo": u"Was kostet SEO? Die drei üblichen Abrechnungsmodelle im Vergleich und die drei Zeichen, an denen Sie ein unseriöses Angebot sicher erkennen.",
"wie-lange-dauert-seo": u"Wie lange dauert SEO? Was schon nach wenigen Wochen wirkt, was mehrere Monate braucht und wovon die Dauer bei Ihrem Projekt tatsächlich abhängt.",
"seo-agentur-oder-selbst-machen": u"SEO selbst machen oder eine Agentur beauftragen? Was Sie ohne Vorkenntnisse gut selbst erledigen und wo ein Fehler erst nach Monaten auffällt.",
"unserioese-seo-agentur-erkennen": u"Unseriöse SEO-Agentur erkennen: sieben Sätze und Versprechen, nach denen Sie das Gespräch beenden können, bevor Sie Geld und ein Jahr verlieren.",
"neue-website-fuer-seo": u"Brauche ich für SEO eine neue Website? Meistens nicht. Wann ein Neubau sich wirklich lohnt und welcher Fehler dabei am meisten Sichtbarkeit kostet.",
"keyword-recherche-fuer-einsteiger": u"Keyword-Recherche für Einsteiger: in fünf Schritten und ganz ohne Werkzeug herausfinden, wonach Ihre Kundschaft bei Google tatsächlich sucht.",
"core-web-vitals-erklaert": u"Core Web Vitals einfach erklärt: was LCP, INP und CLS messen, welche Werte gut sind und ab wann sich die Ladezeit auf die Position auswirkt.",
"lokale-seo-handwerker-dienstleister": u"Lokale SEO für Handwerk und Dienstleistung: wie Betriebe im Umkreis gefunden werden und was über die Platzierung im Local Pack von Google entscheidet.",
"keyword": u"Ein Keyword ist der Begriff, den jemand bei Google eingibt. Warum jede Seite genau einen braucht und welcher Fehler bei der Wahl am häufigsten ist.",
"suchintention": u"Die Suchintention ist die Absicht hinter einer Suchanfrage. Wie Sie in zehn Sekunden prüfen, ob jemand kaufen, vergleichen oder nachschlagen will.",
"long-tail-keyword": u"Long-Tail-Keywords sind längere, genauere Suchanfragen mit weniger Wettbewerb und mehr Kaufabsicht. Warum sie für kleine Betriebe der Einstieg sind.",
"meta-title": u"Der Meta-Title ist die anklickbare Überschrift im Suchergebnis. Was hineingehört, wie lang er sein darf und warum jede Seite einen eigenen braucht.",
"meta-description": u"Die Meta-Description ist der Beschreibungstext unter dem Treffer. Kein Rankingfaktor, aber entscheidend dafür, ob jemand Ihren Eintrag anklickt.",
"h1-ueberschrift": u"Die H1 ist die Hauptüberschrift einer Seite. Warum es genau eine pro Seite sein sollte und wieso Überschriftenebenen kein Gestaltungsmittel sind.",
"alt-text": u"Der Alt-Text beschreibt ein Bild für Screenreader und für die Bildersuche. Wie ein guter Alt-Text aussieht und wann er bewusst leer bleiben sollte.",
"backlink": u"Ein Backlink ist ein Link von einer fremden Seite auf Ihre. Warum die Herkunft zählt und nicht die Anzahl, und welche Links der Domain schaden.",
"interne-verlinkung": u"Interne Verlinkung verteilt Aufmerksamkeit und Kraft innerhalb Ihrer Website. Die 60/40-Regel und warum ein Blog sonst nur noch sich selbst verlinkt.",
"indexierung": u"Indexierung ist die Aufnahme einer Seite in den Datenbestand von Google. Wie Sie in zwei Minuten prüfen, ob Ihre Seiten überhaupt im Index stehen.",
"noindex": u"noindex hält eine Seite aus den Suchergebnissen heraus. Wofür man es braucht und warum ein vergessenes noindex zu den teuersten Fehlern gehört.",
"robots-txt": u"Die robots.txt steuert, welche Bereiche Suchmaschinen abrufen dürfen. Der wichtige Unterschied zu noindex und die zwei häufigsten Fehler darin.",
"sitemap": u"Eine XML-Sitemap listet alle Seiten einer Website für Suchmaschinen auf. Was sie leistet, was sie nicht leistet und welcher Fehler Vertrauen kostet.",
"canonical-tag": u"Das Canonical-Tag sagt Google, welche von mehreren gleichen Seiten die maßgebliche ist. Wofür man es braucht und wie ein Fehler ganze Shops kostet.",
"301-weiterleitung": u"Die 301-Weiterleitung leitet eine alte Adresse dauerhaft auf eine neue um. Warum sie bei jedem Umbau Pflicht ist und wie man dabei richtig vorgeht.",
"keyword-kannibalisierung": u"Keyword-Kannibalisierung bedeutet, dass zwei eigene Seiten um denselben Begriff konkurrieren. Wie Sie es erkennen und wie Sie es wieder auflösen.",
"local-pack": u"Das Local Pack ist die Box mit Karte und drei Einträgen bei Suchen mit Ortsbezug. Was über die Platzierung entscheidet und was Sie beeinflussen können.",
"search-console": u"Die Google Search Console zeigt, wofür Ihre Website gefunden wird. Warum sie zuerst eingerichtet wird und worauf Sie darin zuerst schauen sollten.",
"strukturierte-daten": u"Strukturierte Daten zeichnen Inhalte für Google eindeutig aus. Was sie im Suchergebnis bringen, was nicht, und welcher Fehler zur Abstrafung führt.",
"sichtbarkeitsindex": u"Der Sichtbarkeitsindex zeigt, wie präsent eine Domain in der Suche ist. Warum er als Verlauf nützlich ist und warum er als Ziel in die Irre führt.",
}
# Meta-Titel max. 60 Zeichen inklusive " | Kontor" (Regel 3).
TITEL = {
"warum-findet-mich-bei-google-niemand": u"Bei Google nicht gefunden",
"google-unternehmensprofil-einrichten": u"Google Unternehmensprofil einrichten",
"unserioese-seo-agentur-erkennen": u"Unseriöse SEO-Agentur erkennen",
"neue-website-fuer-seo": u"Neue Website für SEO nötig?",
"keyword-recherche-fuer-einsteiger": u"Keyword-Recherche für Einsteiger",
"core-web-vitals-erklaert": u"Core Web Vitals erklärt",
"lokale-seo-handwerker-dienstleister": u"Lokale SEO für Handwerk",
"seo-agentur-oder-selbst-machen": u"SEO-Agentur oder selbst machen",
"search-console": u"Google Search Console",
"keyword": u"Keywords richtig wählen",
"suchintention": u"Suchintention verstehen",
"long-tail-keyword": u"Long-Tail-Keywords",
"meta-title": u"Meta-Title schreiben",
"meta-description": u"Meta-Description schreiben",
}
