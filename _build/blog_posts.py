# -*- coding: utf-8 -*-
"""Die Blogbeitraege. Aufbau wie bei PoseyPets: zwei Formate mit zwei
Aufgaben. Ratgeber beantworten die ausfuehrlichen Fragen vor einer
Entscheidung, Lexikon-Eintraege die kurzen Begriffssuchen.

Jeder Beitrag: (slug, format, titel, teaser, lede, body).
Pro Beitrag gilt die 60/40-Regel fuer interne Links: die Mehrzahl zeigt
auf Leistungs- und Kontaktseiten, der Rest auf weitere Beitraege.
"""

RATGEBER = [

("warum-findet-mich-bei-google-niemand",
 u"Warum findet mich bei Google niemand?",
 u"Die fünf Ursachen, die in den meisten Fällen dahinterstecken.",
 u"Die Website ist online, sieht gut aus, und trotzdem kommt über Google niemand. Das hat fast immer eine von fünf Ursachen.",
 u"""
    <p>Diese Frage steht am Anfang fast jedes Gesprächs. Die Website ist fertig, hat Geld gekostet, sieht ordentlich aus - und bringt keine einzige Anfrage. Dafür gibt es selten einen exotischen Grund. In den allermeisten Fällen ist es einer der folgenden fünf.</p>

    <h2>1. Die Seiten stehen gar nicht im Index</h2>
    <p>Bevor eine Seite eine Position haben kann, muss Google sie überhaupt kennen. Eine Seite, die nicht im Index ist, kann nicht auf Platz 50 stehen - sie existiert für die Suche nicht. Das passiert häufiger, als man denkt: ein <a href="noindex.html">noindex</a> aus der Entwicklungsphase, das nie entfernt wurde, eine blockierende <a href="robots-txt.html">robots.txt</a>, oder schlicht Seiten, auf die intern kein einziger Link zeigt.</p>
    <p>Prüfen lässt sich das in zwei Minuten: In die Google-Suche <code>site:ihre-domain.de</code> eingeben. Was dort nicht auftaucht, ist nicht im Index.</p>

    <h2>2. Es gibt keine Seite für den Suchbegriff</h2>
    <p>Google rankt keine Unternehmen, sondern einzelne Seiten. Wer fünf Leistungen anbietet, aber nur eine Seite hat, auf der alle fünf in Stichpunkten stehen, hat für keinen der fünf Begriffe eine Seite, die diese Frage vollständig beantwortet. Die häufigste Schwachstelle überhaupt ist die eine Leistungsseite, die alles gleichzeitig abdecken soll.</p>
    <p>Die Lösung ist unspektakulär: eine Seite je Begriff, der Anfragen bringt. Mehr dazu unter <a href="../leistungen/onpage-und-webdesign.html">OnPage und Webdesign</a>.</p>

    <h2>3. Die Begriffe sind zu groß gewählt</h2>
    <p>Wer bei „Rechtsanwalt“ auf Seite 1 will, tritt gegen Kanzleien an, die seit fünfzehn Jahren daran arbeiten. „Fachanwalt Arbeitsrecht Göppingen“ ist ein anderes Spiel - weniger Suchen, aber erreichbar, und dahinter steht jemand mit konkretem Bedarf. Das nennt sich <a href="long-tail-keyword.html">Long-Tail</a> und ist für kleine und mittlere Unternehmen fast immer der richtige Einstieg.</p>

    <h2>4. Es fehlt die lokale Präsenz</h2>
    <p>Bei jeder Suche mit Ortsbezug zeigt Google zuerst drei Einträge mit Karte und Telefonnummer, das <a href="local-pack.html">Local Pack</a>. Darüber laufen viele Anrufe, bevor jemand die normalen Treffer überhaupt ansieht. Wer dort nicht steht, verliert die Kundschaft im Umkreis, egal wie gut die Website ist. Das <a href="google-unternehmensprofil-einrichten.html">Google Unternehmensprofil</a> kostet nichts und ist bei vielen Betrieben der schnellste Hebel.</p>

    <h2>5. Die Seite ist zu langsam oder auf dem Handy unbrauchbar</h2>
    <p>Der größte Teil der Suchen passiert heute mobil. Eine Seite, die auf dem Handy drei Sekunden braucht oder bei der man horizontal scrollen muss, verliert Besucher, bevor sie etwas gesehen haben. Diese Abbrüche sind für Google ein Signal, das auf die Position zurückwirkt. Was dabei genau gemessen wird, steht unter <a href="core-web-vitals-erklaert.html">Core Web Vitals</a>.</p>

    <div class="cs-note">
      <h3>Kurz gesagt</h3>
      <p>Gehen Sie die Liste von oben nach unten durch. Punkt 1 und 2 erklären die meisten Fälle, und beide lassen sich ohne großes Budget beheben. Erst wenn die ersten vier stehen und es trotzdem nicht reicht, wird <a href="../leistungen/linkaufbau.html">Linkaufbau</a> zum Thema.</p>
    </div>
"""),

("google-unternehmensprofil-einrichten",
 u"Google Unternehmensprofil richtig einrichten",
 u"Welche Felder zählen und welcher Fehler am meisten Sichtbarkeit kostet.",
 u"Der schnellste Hebel für Betriebe mit Kundschaft aus der Umgebung - und er kostet nichts.",
 u"""
    <p>Das Google Unternehmensprofil ist der Eintrag, der bei einer Suche mit Ortsbezug rechts oder oben mit Karte, Öffnungszeiten und Telefonnummer erscheint. Für viele Betriebe bringt er mehr Anrufe als die eigene Website, und er ist kostenlos. Trotzdem ist er bei den meisten halb ausgefüllt.</p>

    <h2>Die Felder, auf die es ankommt</h2>
    <p><strong>Kategorie.</strong> Das wichtigste Feld überhaupt. Die Hauptkategorie entscheidet, bei welchen Suchen Sie überhaupt infrage kommen. „Bäckerei“ und „Konditorei“ sind zwei verschiedene Türen. Nebenkategorien können ergänzt werden, aber die Hauptkategorie sollte das sein, womit Sie Ihr Geld verdienen.</p>
    <p><strong>Name, Adresse, Telefonnummer.</strong> Genau so, wie sie auch auf Ihrer Website und in Verzeichnissen stehen. Abweichungen sind einer der häufigsten Gründe, warum ein Profil schlechter läuft als es müsste.</p>
    <p><strong>Leistungen.</strong> Jede einzelne eintragen, nicht nur zwei Oberbegriffe. Diese Einträge tauchen in den Suchergebnissen auf und werden für die Zuordnung verwendet.</p>
    <p><strong>Öffnungszeiten, auch für Feiertage.</strong> Google weist Nutzer auf möglicherweise abweichende Zeiten hin. Ein gepflegter Kalender verhindert, dass jemand vor verschlossener Tür steht und eine schlechte Bewertung hinterlässt.</p>
    <p><strong>Fotos.</strong> Echte, eigene. Innen, außen, Team, Arbeit. Stockfotos erkennt man, und sie wirken genau so, wie sie sind.</p>

    <h2>Der Fehler, der am meisten kostet</h2>
    <p>Abweichende Angaben zwischen Profil, Website und Verzeichnissen. Wenn im Profil „Str.“ steht, auf der Website „Straße“ und im Branchenbuch noch die alte Telefonnummer, muss Google entscheiden, welche Angabe stimmt - und wird im Zweifel vorsichtig. Diese Einheitlichkeit heißt in der Branche NAP-Konsistenz, und sie ist stumpfe Fleißarbeit mit messbarem Ergebnis.</p>

    <h2>Bewertungen</h2>
    <p>Fragen Sie nach ihnen, und zwar am Tag, an dem jemand zufrieden war. Nicht kaufen, nicht erfinden: Google erkennt Muster, und gefälschte Bewertungen kosten im Zweifel den ganzen Eintrag. Antworten Sie auf jede Bewertung, auch auf die schlechten, sachlich und kurz. Das lesen nicht nur die Verfasser, sondern alle, die nach Ihnen kommen.</p>

    <div class="cs-note">
      <h3>Kurz gesagt</h3>
      <p>Ein vollständig gepflegtes Profil mit einheitlichen Angaben und echten Fotos ist die billigste Sichtbarkeit, die es gibt. Mehr zum Zusammenspiel mit der Website unter <a href="../leistungen/seo.html">SEO</a>, oder lassen Sie uns in der <a href="../kontakt.html">kostenlosen Analyse</a> draufschauen.</p>
    </div>
"""),

("was-kostet-seo",
 u"Was kostet SEO?",
 u"Die drei üblichen Abrechnungsmodelle und woran Sie unseriöse Angebote erkennen.",
 u"Eine ehrliche Antwort auf die Frage, auf die es keine Pauschalantwort gibt - aber eine klare Orientierung.",
 u"""
    <p>Auf diese Frage gibt es keine Zahl, die für alle stimmt, und jeder, der am Telefon sofort eine nennt, hat sich Ihre Seite nicht angesehen. Was es gibt, sind drei übliche Modelle, und die Frage, welches zu Ihnen passt, lässt sich beantworten.</p>

    <h2>Monatliche Betreuung</h2>
    <p>Ein fester Betrag pro Monat für laufende Arbeit: Inhalte, Technik, Berichte. Sinnvoll, wenn dauerhaft etwas passieren soll und Sie jemanden brauchen, der dranbleibt. Die Frage, die Sie stellen sollten: Was genau passiert in diesem Monat, und woran sehe ich, dass es passiert ist? Eine Pauschale ohne beschriebenen Umfang ist ein Abonnement, keine Leistung.</p>

    <h2>Festpreis je Projekt</h2>
    <p>Ein klar umrissenes Paket zu einem festen Preis: ein <a href="../leistungen/seo-audit.html">Audit</a>, der Aufbau von fünf Landingpages, die technische Überarbeitung. Der Vorteil liegt auf der Hand - Sie wissen vorher, was es kostet und was dabei herauskommt. So arbeiten wir, weil sich der Aufwand bei klar beschriebenem Umfang vorher einschätzen lässt.</p>

    <h2>Stundensatz</h2>
    <p>Üblich bei Beratung und kleinen Eingriffen. Für ein längeres Projekt ist es das unangenehmste Modell für den Kunden, weil das Risiko vollständig bei ihm liegt: Dauert es länger, zahlen Sie mehr, ohne dass das Ergebnis besser wird.</p>

    <h2>Woran Sie ein unseriöses Angebot erkennen</h2>
    <p>Es gibt drei zuverlässige Zeichen. <strong>Erstens:</strong> eine Garantie auf Platz 1. Niemand außer Google entscheidet über die Reihenfolge, und wer das zusagt, verkauft etwas, das er nicht halten kann. <strong>Zweitens:</strong> ein Preis ohne Blick auf die Seite. <strong>Drittens:</strong> eine feste Zahl an <a href="backlink.html">Backlinks</a> pro Monat. Diese Zusage lässt sich nur einhalten, indem man Links kauft, und gekaufte Links schaden der ganzen Domain.</p>

    <div class="cs-note">
      <h3>Kurz gesagt</h3>
      <p>Lassen Sie sich vor jedem Angebot zeigen, woran Sie heute stehen. Unsere <a href="../kontakt.html">kostenlose Analyse</a> ist genau dafür da: Sie sehen, wer vor Ihnen steht und warum - und entscheiden danach, ob und mit wem Sie arbeiten.</p>
    </div>
"""),

("wie-lange-dauert-seo",
 u"Wie lange dauert SEO?",
 u"Was nach Wochen passiert, was nach Monaten - und woran die Dauer wirklich hängt.",
 u"Eine realistische Zeitrechnung, aufgeteilt nach dem, was schnell geht, und dem, was dauert.",
 u"""
    <p>Die ehrliche Antwort lautet: Es kommt darauf an, woran gearbeitet wird. Manche Dinge wirken in Wochen, andere brauchen Monate, und beides im selben Projekt. Deshalb ist die Frage „wie lange dauert SEO“ ungefähr so präzise wie „wie lange dauert Renovieren“.</p>

    <h2>Wochen: Technik und lokale Präsenz</h2>
    <p>Blockierte Seiten freigeben, fehlende Titel ergänzen, ein unvollständiges <a href="google-unternehmensprofil-einrichten.html">Unternehmensprofil</a> ausfüllen, Ladezeit auf dem Handy reparieren. Solche Eingriffe sind oft innerhalb von zwei bis sechs Wochen sichtbar, weil sie keine neue Autorität aufbauen, sondern vorhandene freilegen. Das ist der Grund, warum wir damit anfangen.</p>

    <h2>Monate: Inhalte und Positionen</h2>
    <p>Eine neue Seite braucht Zeit, bis Google sie eingeordnet hat und bis sich zeigt, wie Nutzer darauf reagieren. Bei wenig umkämpften Begriffen sind zwei bis drei Monate realistisch, bei umkämpften sechs und mehr. Dazwischen passiert nichts Spektakuläres: Die Seite steht erst auf Position 60, dann auf 30, dann auf 12. Erst der letzte Schritt bringt spürbar Besucher.</p>

    <h2>Ein Jahr und länger: Autorität</h2>
    <p><a href="../leistungen/linkaufbau.html">Linkaufbau</a> und der Aufbau einer Inhaltssammlung wirken am langsamsten und am dauerhaftesten. Das ist der Teil, bei dem ein Wettbewerber, der zwei Jahre Vorsprung hat, schwer einzuholen ist - und der Grund, warum man am besten gestern angefangen hätte.</p>

    <h2>Wovon die Dauer tatsächlich abhängt</h2>
    <p>Drei Dinge: der Zustand der Seite zu Beginn, die Stärke des Wettbewerbs bei Ihren Begriffen, und wie schnell Änderungen tatsächlich umgesetzt werden. Der dritte Punkt wird unterschätzt. Projekte verzögern sich selten an der Suchmaschine, sondern daran, dass eine Freigabe drei Wochen liegen bleibt.</p>

    <div class="cs-note">
      <h3>Kurz gesagt</h3>
      <p>Rechnen Sie mit ersten Bewegungen nach vier bis sechs Wochen und mit belastbaren Ergebnissen nach drei bis sechs Monaten. Wer Ihnen Seite 1 in zwei Wochen verspricht, beschreibt nicht Ihre Branche, sondern sein Verkaufsgespräch. Siehe auch <a href="was-kostet-seo.html">Was kostet SEO?</a></p>
    </div>
"""),

("seo-agentur-oder-selbst-machen",
 u"SEO-Agentur oder selbst machen?",
 u"Was Sie ohne Vorkenntnisse selbst schaffen und wo es sich nicht lohnt.",
 u"Ein guter Teil der Arbeit lässt sich selbst erledigen. Bei welchem Teil das gilt und wo die Grenze liegt.",
 u"""
    <p>Nicht jeder Betrieb braucht eine Agentur. Ein Teil der Arbeit ist Fleiß und kein Fachwissen, und wer sich damit selbst befasst, versteht sein eigenes Geschäft hinterher besser. Die Frage ist, wo die Grenze liegt.</p>

    <h2>Was Sie gut selbst machen können</h2>
    <p><strong>Das Unternehmensprofil.</strong> Vollständig ausfüllen, echte Fotos hochladen, Bewertungen einsammeln und beantworten. Dafür braucht es niemanden, nur eine Stunde und etwas Regelmäßigkeit.</p>
    <p><strong>Texte über Ihre eigene Arbeit.</strong> Sie wissen besser als jede Agentur, welche Fragen Kunden am Telefon stellen. Diese Fragen aufzuschreiben, ist der Rohstoff für gute Inhalte - die Struktur drumherum kann jemand anderes bauen.</p>
    <p><strong>Fotos.</strong> Eigene Bilder von eigener Arbeit schlagen jede gekaufte Bildsammlung, und sie kosten nichts.</p>

    <h2>Wo es sich selten lohnt</h2>
    <p><strong>Keyword-Recherche.</strong> Nicht weil sie schwer wäre, sondern weil der häufigste Fehler darin besteht, auf die falschen Begriffe zu zielen - und das merkt man erst nach Monaten vergeblicher Arbeit. Ein Tag Recherche zu Beginn spart ein halbes Jahr.</p>
    <p><strong>Technik.</strong> <a href="indexierung.html">Indexierung</a>, <a href="canonical-tag.html">Canonical-Tags</a>, Weiterleitungen, Ladezeit. Hier richtet ein gut gemeinter Eingriff schnell Schaden an, den man selbst nicht sieht.</p>
    <p><strong>Linkaufbau.</strong> Der Bereich, in dem die meisten Anfänger Geld für Dinge ausgeben, die der Domain schaden.</p>

    <h2>Der dritte Weg</h2>
    <p>Häufig ist die sinnvollste Aufteilung: Ein <a href="../leistungen/seo-audit.html">Audit</a> einmal von außen, mit einer priorisierten Liste - und die Umsetzung danach intern, soweit Sie können. Das Audit gehört Ihnen, und es gibt keinen Grund, daraus einen Dauerauftrag zu machen, wenn Sie die Punkte selbst abarbeiten können.</p>

    <div class="cs-note">
      <h3>Kurz gesagt</h3>
      <p>Machen Sie alles selbst, was mit Ihrem eigenen Wissen zu tun hat. Holen Sie sich Hilfe bei allem, wo ein Fehler erst nach Monaten auffällt. Was bei Ihnen in welche Kategorie fällt, steht in der <a href="../kontakt.html">kostenlosen Analyse</a>.</p>
    </div>
"""),
]

RATGEBER += [

("unserioese-seo-agentur-erkennen",
 u"Woran Sie eine unseriöse SEO-Agentur erkennen",
 u"Sieben Sätze, nach denen Sie das Gespräch beenden können.",
 u"SEO ist für Außenstehende schwer zu prüfen. Genau davon lebt ein Teil der Branche. Diese Zeichen sind eindeutig.",
 u"""
    <p>Der Markt ist voll von Anbietern, deren Leistung sich für den Kunden kaum überprüfen lässt. Das ist das eigentliche Problem: Bei einem schlecht verlegten Boden sieht man es. Bei schlechter Suchmaschinenoptimierung merkt man nach einem Jahr, dass nichts passiert ist. Diese sieben Zeichen sparen Ihnen dieses Jahr.</p>

    <h2>1. „Wir garantieren Platz 1“</h2>
    <p>Über die Reihenfolge entscheidet allein Google, und das Verfahren ändert sich laufend. Eine Garantie ist entweder Unwissen oder Absicht. Beides ist ein Grund aufzulegen.</p>

    <h2>2. Ein Preis, ohne die Seite gesehen zu haben</h2>
    <p>Ob bei Ihnen zwanzig Stunden oder zweihundert nötig sind, hängt vom Zustand der Seite und vom Wettbewerb ab. Wer ohne Blick darauf eine Zahl nennt, verkauft ein Paket, keine Arbeit.</p>

    <h2>3. Eine feste Zahl an Backlinks pro Monat</h2>
    <p>„50 Backlinks monatlich“ ist nur einzuhalten, indem man sie kauft. Gekaufte Links aus Netzwerken lassen sich erkennen, und der Schaden trifft nicht eine Unterseite, sondern die ganze Domain. Was stattdessen zählt, steht unter <a href="backlink.html">Backlink</a>.</p>

    <h2>4. Berichte, die nur aus Diagrammen bestehen</h2>
    <p>Vierzig Seiten aus einem Tool, in denen keine einzige Zahl mit Ihrem Geschäft zu tun hat. Ein brauchbarer Bericht passt auf eine Seite und beantwortet: Welche Begriffe haben sich bewegt, wie viele Besucher kamen aus der Suche, was wurde gemacht, was kommt als Nächstes. Siehe <a href="../leistungen/reporting.html">Reporting</a>.</p>

    <h2>5. Lange Mindestlaufzeit bei kurzer Erklärung</h2>
    <p>Zwölf Monate Bindung sind nicht per se unseriös - SEO dauert. Unseriös wird es, wenn die Laufzeit lang ist und die Beschreibung der Leistung kurz.</p>

    <h2>6. Keine Zugänge, keine Einsicht</h2>
    <p>Search Console und Analysezugang gehören Ihnen. Eine Agentur, die darauf besteht, dass die Konten auf ihren Namen laufen, baut eine Abhängigkeit auf, die beim Wechsel teuer wird.</p>

    <h2>7. Druck im Erstgespräch</h2>
    <p>„Das Angebot gilt nur heute“ ist in einem Geschäft, das in Monaten rechnet, ein Widerspruch in sich.</p>

    <div class="cs-note">
      <h3>Kurz gesagt</h3>
      <p>Lassen Sie sich vor der Unterschrift zeigen, woran Sie stehen, und verlangen Sie eine Liste, was konkret gemacht wird. Beides bekommen Sie bei uns in der <a href="../kontakt.html">kostenlosen Analyse</a>, ohne Gegenleistung.</p>
    </div>
"""),

("neue-website-fuer-seo",
 u"Brauche ich für SEO eine neue Website?",
 u"Meistens nicht. Wann ein Neubau trotzdem der günstigere Weg ist.",
 u"Die Frage kommt fast immer, und die Antwort ist seltener „ja“, als Agenturen behaupten.",
 u"""
    <p>Ein Neubau ist der größte Posten, den eine Agentur verkaufen kann. Entsprechend oft wird er empfohlen. In den allermeisten Fällen lässt sich mit der vorhandenen Seite arbeiten.</p>

    <h2>Was auch auf einer alten Seite geht</h2>
    <p>Titel und Beschreibungen ändern, Überschriften ordnen, neue Unterseiten anlegen, interne Links setzen, Bilder verkleinern, <a href="alt-text.html">Alt-Texte</a> ergänzen, das Unternehmensprofil pflegen. Das ist der weit überwiegende Teil der Arbeit, und dafür muss niemand etwas neu bauen.</p>

    <h2>Wann ein Neubau wirklich günstiger ist</h2>
    <p><strong>Wenn das System keine eigenen Seiten zulässt.</strong> Manche Baukästen erlauben pro Seite keinen eigenen Titel oder keine saubere Überschriftenstruktur. Dann arbeitet man dauerhaft gegen das Werkzeug.</p>
    <p><strong>Wenn die Seite auf dem Handy unbrauchbar ist</strong> und sich das nicht nachrüsten lässt. Der Großteil der Suchen ist mobil; eine Seite, die dort nicht funktioniert, verliert Besucher unabhängig von der Position.</p>
    <p><strong>Wenn die Ladezeit baulich bedingt ist</strong> - zum Beispiel bei einer Seite, die komplett aus eingebetteten Fremdinhalten besteht.</p>

    <h2>Der teuerste Fehler beim Neubau</h2>
    <p>Alte URLs ersatzlos abschalten. Jede Seite, die rankte, verliert ihre Position, und die Besucher landen auf einer Fehlerseite. Wer neu baut, braucht eine vollständige Liste der alten Adressen und für jede eine <a href="301-weiterleitung.html">301-Weiterleitung</a> auf das passende neue Ziel. Ohne diese Liste kostet ein Neubau Sichtbarkeit, die vorher da war.</p>

    <div class="cs-note">
      <h3>Kurz gesagt</h3>
      <p>Lassen Sie prüfen, ob Ihre Seite die Grundlagen zulässt, bevor Sie über einen Neubau nachdenken. Wenn ein Neubau wirklich der günstigere Weg ist, sagen wir das offen - und wenn nicht, auch. Siehe <a href="../leistungen/onpage-und-webdesign.html">OnPage und Webdesign</a>.</p>
    </div>
"""),

("keyword-recherche-fuer-einsteiger",
 u"Keyword-Recherche für Einsteiger",
 u"Wie Sie in einer Stunde herausfinden, wonach Ihre Kundschaft wirklich sucht.",
 u"Der Schritt, der über alles andere entscheidet - und der ohne Werkzeug weiter kommt, als die meisten denken.",
 u"""
    <p>Jede Seite, jeder Text, jede Überschrift zielt auf einen Begriff. Wenn dieser Begriff falsch gewählt ist, war die gesamte Arbeit danach umsonst. Deshalb steht die Recherche am Anfang, nicht am Ende.</p>

    <h2>Schritt 1: aufschreiben, was Kunden sagen</h2>
    <p>Nicht, was Sie sagen. Ein Betrieb schreibt „Sanitärinstallation“, gesucht wird „Klempner in der Nähe“. Die beste Quelle sind Ihre eigenen Anfragen: Wie formulieren Leute es am Telefon, in E-Mails, im Kontaktformular? Diese Formulierungen sind die Begriffe, auf die es ankommt.</p>

    <h2>Schritt 2: Google selbst fragen</h2>
    <p>Tippen Sie Ihren Begriff in die Suche und sehen Sie sich die Vorschläge an, die beim Tippen erscheinen. Scrollen Sie zum Ende der Ergebnisseite zu den verwandten Suchanfragen. Öffnen Sie die Kästen „Ähnliche Fragen“. Das ist echte Suchdatenlage, kostenlos, und für den Einstieg reicht sie weit.</p>

    <h2>Schritt 3: die Absicht prüfen</h2>
    <p>Geben Sie den Begriff ein und sehen Sie sich an, was Google bereits auf Seite 1 zeigt. Stehen dort Shops, will der Suchende kaufen. Stehen dort Anleitungen, will er es selbst machen. Eine Verkaufsseite wird bei einem Begriff, hinter dem Anleitungen stehen, nicht ranken - egal wie gut sie ist. Mehr dazu unter <a href="suchintention.html">Suchintention</a>.</p>

    <h2>Schritt 4: aussortieren</h2>
    <p>Das ist die unsichtbare Hälfte. Streichen Sie alles, hinter dem keine Kundschaft steht, auch wenn es nach viel Volumen aussieht. Ein Begriff mit tausend Suchen, bei denen niemand kaufen will, ist wertlos. Ein Begriff mit dreißig Suchen und konkretem Bedarf bringt Aufträge.</p>

    <h2>Schritt 5: eine Seite je Begriff zuordnen</h2>
    <p>Legen Sie eine Tabelle an: Begriff, Suchabsicht, und welche Ihrer Seiten diesen Begriff bedient. Taucht eine Seite zweimal auf, haben Sie ein Problem - siehe <a href="keyword-kannibalisierung.html">Keyword-Kannibalisierung</a>. Fehlt zu einem guten Begriff eine Seite, haben Sie Ihre nächste Aufgabe.</p>

    <div class="cs-note">
      <h3>Kurz gesagt</h3>
      <p>Eine Stunde mit den Schritten 1 bis 3 bringt mehr als drei Monate Texte schreiben ins Blaue. Wie wir das in einem echten Projekt gemacht haben, steht in der <a href="../referenzen/poseypets.html">Fallstudie PoseyPets</a>.</p>
    </div>
"""),

("core-web-vitals-erklaert",
 u"Core Web Vitals, kurz erklärt",
 u"Was Google misst und ab wann sich die Ladezeit auf die Position auswirkt.",
 u"Drei Messwerte, drei Alltagsfragen - ohne Fachchinesisch.",
 u"""
    <p>Core Web Vitals sind drei Messwerte, mit denen Google beschreibt, wie sich eine Seite für den Besucher anfühlt. Sie sind kein Geheimnis und kein Hexenwerk, und man kann sie in Alltagssprache übersetzen.</p>

    <h2>LCP - wie schnell ist das Wesentliche da?</h2>
    <p>Gemessen wird, wann das größte sichtbare Element geladen ist, meist ein Bild oder eine Überschrift. Als gut gilt unter 2,5 Sekunden. Der häufigste Grund für schlechte Werte: Bilder, die in Originalgröße ausgeliefert werden, obwohl sie auf dem Handy auf Daumengröße schrumpfen.</p>

    <h2>INP - reagiert die Seite, wenn ich tippe?</h2>
    <p>Gemessen wird die Verzögerung zwischen einer Eingabe und der sichtbaren Reaktion. Als gut gilt unter 200 Millisekunden. Schlechte Werte kommen fast immer von zu vielen Skripten, die gleichzeitig arbeiten - Chat-Fenster, Tracking, Einwilligungsbanner, Schriftarten von fremden Servern.</p>

    <h2>CLS - springt das Layout?</h2>
    <p>Gemessen wird, wie stark sich Inhalte beim Laden noch verschieben. Jeder kennt das: Man will auf einen Link tippen, im selben Moment lädt oben ein Banner nach, und man trifft etwas anderes. Die häufigste Ursache sind Bilder ohne angegebene Größe und nachgeladene Werbeflächen.</p>

    <h2>Ab wann wirkt sich das auf die Position aus?</h2>
    <p>Hier ist Ehrlichkeit angebracht: Die Werte sind ein schwaches Signal im Vergleich zu Inhalt und Verlinkung. Eine schnelle Seite mit dem falschen Inhalt rankt nicht. Entscheidend wird die Geschwindigkeit dort, wo zwei Seiten inhaltlich gleichauf liegen - und in dem, was sie mit den Besuchern macht: Wer abbricht, kauft nicht, und das sieht Google an der Rückkehr zur Suche.</p>

    <div class="cs-note">
      <h3>Kurz gesagt</h3>
      <p>Prüfen Sie Ihre Seite einmal mit PageSpeed Insights von Google. Die größten Gewinne liegen fast immer bei Bildern und bei Skripten, die niemand vermisst. Siehe auch <a href="../leistungen/seo.html">SEO</a>.</p>
    </div>
"""),

("lokale-seo-handwerker-dienstleister",
 u"Lokale SEO für Handwerk und Dienstleistung",
 u"Wie Betriebe im Umkreis gefunden werden, bevor jemand die normalen Treffer ansieht.",
 u"Bei Suchen mit Ortsbezug entscheidet sich fast alles in den ersten drei Einträgen mit Karte.",
 u"""
    <p>Wer „Elektriker Göppingen“ sucht, bekommt zuerst eine Karte mit drei Einträgen, Telefonnummern und Bewertungen. Erst darunter beginnen die normalen Ergebnisse. Ein großer Teil der Anrufe entsteht in diesen drei Zeilen - das <a href="local-pack.html">Local Pack</a> ist für ortsgebundene Betriebe wichtiger als die eigene Startseite.</p>

    <h2>Was über die Platzierung entscheidet</h2>
    <p>Google nennt drei Faktoren: <strong>Relevanz</strong> (passt der Eintrag zur Suche?), <strong>Entfernung</strong> (wie weit ist es zum Suchenden?) und <strong>Bekanntheit</strong> (wie präsent ist der Betrieb im Netz?). Die Entfernung können Sie nicht ändern. Die anderen beiden schon.</p>

    <h2>Relevanz: Kategorie und Leistungen</h2>
    <p>Die Hauptkategorie im <a href="google-unternehmensprofil-einrichten.html">Unternehmensprofil</a> ist das stärkste Einzelsignal. Dazu jede Leistung einzeln eintragen. Ein Betrieb, der nur „Elektriker“ hinterlegt hat, erscheint seltener bei „Wallbox installieren“ als einer, der es ausdrücklich aufgeführt hat.</p>

    <h2>Bekanntheit: einheitliche Angaben und Bewertungen</h2>
    <p>Name, Adresse und Telefonnummer müssen überall identisch sein - Website, Profil, Branchenverzeichnisse, Handwerkskammer. Jede Abweichung schwächt den Eintrag. Dazu Bewertungen: regelmäßig, echt, beantwortet.</p>

    <h2>Und die Website?</h2>
    <p>Sie stützt den Eintrag. Eine eigene Seite je Leistung und, bei mehreren Einzugsgebieten, je Ort - mit echtem, unterschiedlichem Inhalt, nicht derselbe Text mit ausgetauschtem Ortsnamen. Diese Seiten geben Google den Zusammenhang zwischen Ihrem Betrieb, der Leistung und dem Gebiet.</p>

    <h2>Der häufigste Fehler</h2>
    <p>Eine Seite mit dreißig Ortsnamen in einer Liste am Seitenende. Das hat vor zehn Jahren funktioniert und wird heute als das erkannt, was es ist. Besser sind wenige echte Seiten für die Orte, aus denen tatsächlich Kundschaft kommt.</p>

    <div class="cs-note">
      <h3>Kurz gesagt</h3>
      <p>Profil vollständig, Angaben überall gleich, Bewertungen einsammeln, pro Leistung eine Seite. In dieser Reihenfolge. Was bei Ihnen fehlt, steht in der <a href="../kontakt.html">kostenlosen Analyse</a>.</p>
    </div>
"""),
]

# Geplante Ratgeber. Solange hier kein Text steht, wird keine Seite erzeugt
# und Verweise darauf erscheinen als normaler Text statt als toter Link.
GEPLANT = [
("keyword", u"Keywords richtig wählen: welcher Begriff auf welche Seite gehört"),
("suchintention", u"Suchintention verstehen: warum gute Seiten trotzdem nicht ranken"),
("long-tail-keyword", u"Long-Tail-Keywords: weniger Suchen, mehr Aufträge"),
("meta-title", u"Meta-Title schreiben: die Überschrift, die über den Klick entscheidet"),
("meta-description", u"Meta-Description schreiben: der Text unter dem Treffer"),
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
}
