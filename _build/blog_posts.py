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
    <p>Diese Frage steht am Anfang fast jedes Gesprächs. Die Website ist fertig, hat Geld gekostet, sieht ordentlich aus — und bringt keine einzige Anfrage. Dafür gibt es selten einen exotischen Grund. In den allermeisten Fällen ist es einer der folgenden fünf.</p>

    <h2>1. Die Seiten stehen gar nicht im Index</h2>
    <p>Bevor eine Seite eine Position haben kann, muss Google sie überhaupt kennen. Eine Seite, die nicht im Index ist, kann nicht auf Platz 50 stehen — sie existiert für die Suche nicht. Das passiert häufiger, als man denkt: ein <a href="noindex.html">noindex</a> aus der Entwicklungsphase, das nie entfernt wurde, eine blockierende <a href="robots-txt.html">robots.txt</a>, oder schlicht Seiten, auf die intern kein einziger Link zeigt.</p>
    <p>Prüfen lässt sich das in zwei Minuten: In die Google-Suche <code>site:ihre-domain.de</code> eingeben. Was dort nicht auftaucht, ist nicht im Index.</p>

    <h2>2. Es gibt keine Seite für den Suchbegriff</h2>
    <p>Google rankt keine Unternehmen, sondern einzelne Seiten. Wer fünf Leistungen anbietet, aber nur eine Seite hat, auf der alle fünf in Stichpunkten stehen, hat für keinen der fünf Begriffe eine Seite, die diese Frage vollständig beantwortet. Die häufigste Schwachstelle überhaupt ist die eine Leistungsseite, die alles gleichzeitig abdecken soll.</p>
    <p>Die Lösung ist unspektakulär: eine Seite je Begriff, der Anfragen bringt. Mehr dazu unter <a href="../leistungen/onpage-und-webdesign.html">OnPage und Webdesign</a>.</p>

    <h2>3. Die Begriffe sind zu groß gewählt</h2>
    <p>Wer bei „Rechtsanwalt“ auf Seite 1 will, tritt gegen Kanzleien an, die seit fünfzehn Jahren daran arbeiten. „Fachanwalt Arbeitsrecht Göppingen“ ist ein anderes Spiel — weniger Suchen, aber erreichbar, und dahinter steht jemand mit konkretem Bedarf. Das nennt sich <a href="long-tail-keyword.html">Long-Tail</a> und ist für kleine und mittlere Unternehmen fast immer der richtige Einstieg.</p>

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
 u"Der schnellste Hebel für Betriebe mit Kundschaft aus der Umgebung — und er kostet nichts.",
 u"""
    <p>Das Google Unternehmensprofil ist der Eintrag, der bei einer Suche mit Ortsbezug rechts oder oben mit Karte, Öffnungszeiten und Telefonnummer erscheint. Für viele Betriebe bringt er mehr Anrufe als die eigene Website, und er ist kostenlos. Trotzdem ist er bei den meisten halb ausgefüllt.</p>

    <h2>Die Felder, auf die es ankommt</h2>
    <p><strong>Kategorie.</strong> Das wichtigste Feld überhaupt. Die Hauptkategorie entscheidet, bei welchen Suchen Sie überhaupt infrage kommen. „Bäckerei“ und „Konditorei“ sind zwei verschiedene Türen. Nebenkategorien können ergänzt werden, aber die Hauptkategorie sollte das sein, womit Sie Ihr Geld verdienen.</p>
    <p><strong>Name, Adresse, Telefonnummer.</strong> Genau so, wie sie auch auf Ihrer Website und in Verzeichnissen stehen. Abweichungen sind einer der häufigsten Gründe, warum ein Profil schlechter läuft als es müsste.</p>
    <p><strong>Leistungen.</strong> Jede einzelne eintragen, nicht nur zwei Oberbegriffe. Diese Einträge tauchen in den Suchergebnissen auf und werden für die Zuordnung verwendet.</p>
    <p><strong>Öffnungszeiten, auch für Feiertage.</strong> Google weist Nutzer auf möglicherweise abweichende Zeiten hin. Ein gepflegter Kalender verhindert, dass jemand vor verschlossener Tür steht und eine schlechte Bewertung hinterlässt.</p>
    <p><strong>Fotos.</strong> Echte, eigene. Innen, außen, Team, Arbeit. Stockfotos erkennt man, und sie wirken genau so, wie sie sind.</p>

    <h2>Der Fehler, der am meisten kostet</h2>
    <p>Abweichende Angaben zwischen Profil, Website und Verzeichnissen. Wenn im Profil „Str.“ steht, auf der Website „Straße“ und im Branchenbuch noch die alte Telefonnummer, muss Google entscheiden, welche Angabe stimmt — und wird im Zweifel vorsichtig. Diese Einheitlichkeit heißt in der Branche NAP-Konsistenz, und sie ist stumpfe Fleißarbeit mit messbarem Ergebnis.</p>

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
 u"Eine ehrliche Antwort auf die Frage, auf die es keine Pauschalantwort gibt — aber eine klare Orientierung.",
 u"""
    <p>Auf diese Frage gibt es keine Zahl, die für alle stimmt, und jeder, der am Telefon sofort eine nennt, hat sich Ihre Seite nicht angesehen. Was es gibt, sind drei übliche Modelle, und die Frage, welches zu Ihnen passt, lässt sich beantworten.</p>

    <h2>Monatliche Betreuung</h2>
    <p>Ein fester Betrag pro Monat für laufende Arbeit: Inhalte, Technik, Berichte. Sinnvoll, wenn dauerhaft etwas passieren soll und Sie jemanden brauchen, der dranbleibt. Die Frage, die Sie stellen sollten: Was genau passiert in diesem Monat, und woran sehe ich, dass es passiert ist? Eine Pauschale ohne beschriebenen Umfang ist ein Abonnement, keine Leistung.</p>

    <h2>Festpreis je Projekt</h2>
    <p>Ein klar umrissenes Paket zu einem festen Preis: ein <a href="../leistungen/seo-audit.html">Audit</a>, der Aufbau von fünf Landingpages, die technische Überarbeitung. Der Vorteil liegt auf der Hand — Sie wissen vorher, was es kostet und was dabei herauskommt. So arbeiten wir, weil sich der Aufwand bei klar beschriebenem Umfang vorher einschätzen lässt.</p>

    <h2>Stundensatz</h2>
    <p>Üblich bei Beratung und kleinen Eingriffen. Für ein längeres Projekt ist es das unangenehmste Modell für den Kunden, weil das Risiko vollständig bei ihm liegt: Dauert es länger, zahlen Sie mehr, ohne dass das Ergebnis besser wird.</p>

    <h2>Woran Sie ein unseriöses Angebot erkennen</h2>
    <p>Es gibt drei zuverlässige Zeichen. <strong>Erstens:</strong> eine Garantie auf Platz 1. Niemand außer Google entscheidet über die Reihenfolge, und wer das zusagt, verkauft etwas, das er nicht halten kann. <strong>Zweitens:</strong> ein Preis ohne Blick auf die Seite. <strong>Drittens:</strong> eine feste Zahl an <a href="backlink.html">Backlinks</a> pro Monat. Diese Zusage lässt sich nur einhalten, indem man Links kauft, und gekaufte Links schaden der ganzen Domain.</p>

    <div class="cs-note">
      <h3>Kurz gesagt</h3>
      <p>Lassen Sie sich vor jedem Angebot zeigen, woran Sie heute stehen. Unsere <a href="../kontakt.html">kostenlose Analyse</a> ist genau dafür da: Sie sehen, wer vor Ihnen steht und warum — und entscheiden danach, ob und mit wem Sie arbeiten.</p>
    </div>
"""),

("wie-lange-dauert-seo",
 u"Wie lange dauert SEO?",
 u"Was nach Wochen passiert, was nach Monaten — und woran die Dauer wirklich hängt.",
 u"Eine realistische Zeitrechnung, aufgeteilt nach dem, was schnell geht, und dem, was dauert.",
 u"""
    <p>Die ehrliche Antwort lautet: Es kommt darauf an, woran gearbeitet wird. Manche Dinge wirken in Wochen, andere brauchen Monate, und beides im selben Projekt. Deshalb ist die Frage „wie lange dauert SEO“ ungefähr so präzise wie „wie lange dauert Renovieren“.</p>

    <h2>Wochen: Technik und lokale Präsenz</h2>
    <p>Blockierte Seiten freigeben, fehlende Titel ergänzen, ein unvollständiges <a href="google-unternehmensprofil-einrichten.html">Unternehmensprofil</a> ausfüllen, Ladezeit auf dem Handy reparieren. Solche Eingriffe sind oft innerhalb von zwei bis sechs Wochen sichtbar, weil sie keine neue Autorität aufbauen, sondern vorhandene freilegen. Das ist der Grund, warum wir damit anfangen.</p>

    <h2>Monate: Inhalte und Positionen</h2>
    <p>Eine neue Seite braucht Zeit, bis Google sie eingeordnet hat und bis sich zeigt, wie Nutzer darauf reagieren. Bei wenig umkämpften Begriffen sind zwei bis drei Monate realistisch, bei umkämpften sechs und mehr. Dazwischen passiert nichts Spektakuläres: Die Seite steht erst auf Position 60, dann auf 30, dann auf 12. Erst der letzte Schritt bringt spürbar Besucher.</p>

    <h2>Ein Jahr und länger: Autorität</h2>
    <p><a href="../leistungen/linkaufbau.html">Linkaufbau</a> und der Aufbau einer Inhaltssammlung wirken am langsamsten und am dauerhaftesten. Das ist der Teil, bei dem ein Wettbewerber, der zwei Jahre Vorsprung hat, schwer einzuholen ist — und der Grund, warum man am besten gestern angefangen hätte.</p>

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
    <p><strong>Texte über Ihre eigene Arbeit.</strong> Sie wissen besser als jede Agentur, welche Fragen Kunden am Telefon stellen. Diese Fragen aufzuschreiben, ist der Rohstoff für gute Inhalte — die Struktur drumherum kann jemand anderes bauen.</p>
    <p><strong>Fotos.</strong> Eigene Bilder von eigener Arbeit schlagen jede gekaufte Bildsammlung, und sie kosten nichts.</p>

    <h2>Wo es sich selten lohnt</h2>
    <p><strong>Keyword-Recherche.</strong> Nicht weil sie schwer wäre, sondern weil der häufigste Fehler darin besteht, auf die falschen Begriffe zu zielen — und das merkt man erst nach Monaten vergeblicher Arbeit. Ein Tag Recherche zu Beginn spart ein halbes Jahr.</p>
    <p><strong>Technik.</strong> <a href="indexierung.html">Indexierung</a>, <a href="canonical-tag.html">Canonical-Tags</a>, Weiterleitungen, Ladezeit. Hier richtet ein gut gemeinter Eingriff schnell Schaden an, den man selbst nicht sieht.</p>
    <p><strong>Linkaufbau.</strong> Der Bereich, in dem die meisten Anfänger Geld für Dinge ausgeben, die der Domain schaden.</p>

    <h2>Der dritte Weg</h2>
    <p>Häufig ist die sinnvollste Aufteilung: Ein <a href="../leistungen/seo-audit.html">Audit</a> einmal von außen, mit einer priorisierten Liste — und die Umsetzung danach intern, soweit Sie können. Das Audit gehört Ihnen, und es gibt keinen Grund, daraus einen Dauerauftrag zu machen, wenn Sie die Punkte selbst abarbeiten können.</p>

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
    <p>Zwölf Monate Bindung sind nicht per se unseriös — SEO dauert. Unseriös wird es, wenn die Laufzeit lang ist und die Beschreibung der Leistung kurz.</p>

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
    <p><strong>Wenn die Ladezeit baulich bedingt ist</strong> — zum Beispiel bei einer Seite, die komplett aus eingebetteten Fremdinhalten besteht.</p>

    <h2>Der teuerste Fehler beim Neubau</h2>
    <p>Alte URLs ersatzlos abschalten. Jede Seite, die rankte, verliert ihre Position, und die Besucher landen auf einer Fehlerseite. Wer neu baut, braucht eine vollständige Liste der alten Adressen und für jede eine <a href="301-weiterleitung.html">301-Weiterleitung</a> auf das passende neue Ziel. Ohne diese Liste kostet ein Neubau Sichtbarkeit, die vorher da war.</p>

    <div class="cs-note">
      <h3>Kurz gesagt</h3>
      <p>Lassen Sie prüfen, ob Ihre Seite die Grundlagen zulässt, bevor Sie über einen Neubau nachdenken. Wenn ein Neubau wirklich der günstigere Weg ist, sagen wir das offen — und wenn nicht, auch. Siehe <a href="../leistungen/onpage-und-webdesign.html">OnPage und Webdesign</a>.</p>
    </div>
"""),

("keyword-recherche-fuer-einsteiger",
 u"Keyword-Recherche für Einsteiger",
 u"Wie Sie in einer Stunde herausfinden, wonach Ihre Kundschaft wirklich sucht.",
 u"Der Schritt, der über alles andere entscheidet — und der ohne Werkzeug weiter kommt, als die meisten denken.",
 u"""
    <p>Jede Seite, jeder Text, jede Überschrift zielt auf einen Begriff. Wenn dieser Begriff falsch gewählt ist, war die gesamte Arbeit danach umsonst. Deshalb steht die Recherche am Anfang, nicht am Ende.</p>

    <h2>Schritt 1: aufschreiben, was Kunden sagen</h2>
    <p>Nicht, was Sie sagen. Ein Betrieb schreibt „Sanitärinstallation“, gesucht wird „Klempner in der Nähe“. Die beste Quelle sind Ihre eigenen Anfragen: Wie formulieren Leute es am Telefon, in E-Mails, im Kontaktformular? Diese Formulierungen sind die Begriffe, auf die es ankommt.</p>

    <h2>Schritt 2: Google selbst fragen</h2>
    <p>Tippen Sie Ihren Begriff in die Suche und sehen Sie sich die Vorschläge an, die beim Tippen erscheinen. Scrollen Sie zum Ende der Ergebnisseite zu den verwandten Suchanfragen. Öffnen Sie die Kästen „Ähnliche Fragen“. Das ist echte Suchdatenlage, kostenlos, und für den Einstieg reicht sie weit.</p>

    <h2>Schritt 3: die Absicht prüfen</h2>
    <p>Geben Sie den Begriff ein und sehen Sie sich an, was Google bereits auf Seite 1 zeigt. Stehen dort Shops, will der Suchende kaufen. Stehen dort Anleitungen, will er es selbst machen. Eine Verkaufsseite wird bei einem Begriff, hinter dem Anleitungen stehen, nicht ranken — egal wie gut sie ist. Mehr dazu unter <a href="suchintention.html">Suchintention</a>.</p>

    <h2>Schritt 4: aussortieren</h2>
    <p>Das ist die unsichtbare Hälfte. Streichen Sie alles, hinter dem keine Kundschaft steht, auch wenn es nach viel Volumen aussieht. Ein Begriff mit tausend Suchen, bei denen niemand kaufen will, ist wertlos. Ein Begriff mit dreißig Suchen und konkretem Bedarf bringt Aufträge.</p>

    <h2>Schritt 5: eine Seite je Begriff zuordnen</h2>
    <p>Legen Sie eine Tabelle an: Begriff, Suchabsicht, und welche Ihrer Seiten diesen Begriff bedient. Taucht eine Seite zweimal auf, haben Sie ein Problem — siehe <a href="keyword-kannibalisierung.html">Keyword-Kannibalisierung</a>. Fehlt zu einem guten Begriff eine Seite, haben Sie Ihre nächste Aufgabe.</p>

    <div class="cs-note">
      <h3>Kurz gesagt</h3>
      <p>Eine Stunde mit den Schritten 1 bis 3 bringt mehr als drei Monate Texte schreiben ins Blaue. Wie wir das in einem echten Projekt gemacht haben, steht in der <a href="../referenzen/poseypets.html">Fallstudie PoseyPets</a>.</p>
    </div>
"""),

("core-web-vitals-erklaert",
 u"Core Web Vitals, kurz erklärt",
 u"Was Google misst und ab wann sich die Ladezeit auf die Position auswirkt.",
 u"Drei Messwerte, drei Alltagsfragen — ohne Fachchinesisch.",
 u"""
    <p>Core Web Vitals sind drei Messwerte, mit denen Google beschreibt, wie sich eine Seite für den Besucher anfühlt. Sie sind kein Geheimnis und kein Hexenwerk, und man kann sie in Alltagssprache übersetzen.</p>

    <h2>LCP — wie schnell ist das Wesentliche da?</h2>
    <p>Gemessen wird, wann das größte sichtbare Element geladen ist, meist ein Bild oder eine Überschrift. Als gut gilt unter 2,5 Sekunden. Der häufigste Grund für schlechte Werte: Bilder, die in Originalgröße ausgeliefert werden, obwohl sie auf dem Handy auf Daumengröße schrumpfen.</p>

    <h2>INP — reagiert die Seite, wenn ich tippe?</h2>
    <p>Gemessen wird die Verzögerung zwischen einer Eingabe und der sichtbaren Reaktion. Als gut gilt unter 200 Millisekunden. Schlechte Werte kommen fast immer von zu vielen Skripten, die gleichzeitig arbeiten — Chat-Fenster, Tracking, Einwilligungsbanner, Schriftarten von fremden Servern.</p>

    <h2>CLS — springt das Layout?</h2>
    <p>Gemessen wird, wie stark sich Inhalte beim Laden noch verschieben. Jeder kennt das: Man will auf einen Link tippen, im selben Moment lädt oben ein Banner nach, und man trifft etwas anderes. Die häufigste Ursache sind Bilder ohne angegebene Größe und nachgeladene Werbeflächen.</p>

    <h2>Ab wann wirkt sich das auf die Position aus?</h2>
    <p>Hier ist Ehrlichkeit angebracht: Die Werte sind ein schwaches Signal im Vergleich zu Inhalt und Verlinkung. Eine schnelle Seite mit dem falschen Inhalt rankt nicht. Entscheidend wird die Geschwindigkeit dort, wo zwei Seiten inhaltlich gleichauf liegen — und in dem, was sie mit den Besuchern macht: Wer abbricht, kauft nicht, und das sieht Google an der Rückkehr zur Suche.</p>

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
    <p>Wer „Elektriker Göppingen“ sucht, bekommt zuerst eine Karte mit drei Einträgen, Telefonnummern und Bewertungen. Erst darunter beginnen die normalen Ergebnisse. Ein großer Teil der Anrufe entsteht in diesen drei Zeilen — das <a href="local-pack.html">Local Pack</a> ist für ortsgebundene Betriebe wichtiger als die eigene Startseite.</p>

    <h2>Was über die Platzierung entscheidet</h2>
    <p>Google nennt drei Faktoren: <strong>Relevanz</strong> (passt der Eintrag zur Suche?), <strong>Entfernung</strong> (wie weit ist es zum Suchenden?) und <strong>Bekanntheit</strong> (wie präsent ist der Betrieb im Netz?). Die Entfernung können Sie nicht ändern. Die anderen beiden schon.</p>

    <h2>Relevanz: Kategorie und Leistungen</h2>
    <p>Die Hauptkategorie im <a href="google-unternehmensprofil-einrichten.html">Unternehmensprofil</a> ist das stärkste Einzelsignal. Dazu jede Leistung einzeln eintragen. Ein Betrieb, der nur „Elektriker“ hinterlegt hat, erscheint seltener bei „Wallbox installieren“ als einer, der es ausdrücklich aufgeführt hat.</p>

    <h2>Bekanntheit: einheitliche Angaben und Bewertungen</h2>
    <p>Name, Adresse und Telefonnummer müssen überall identisch sein — Website, Profil, Branchenverzeichnisse, Handwerkskammer. Jede Abweichung schwächt den Eintrag. Dazu Bewertungen: regelmäßig, echt, beantwortet.</p>

    <h2>Und die Website?</h2>
    <p>Sie stützt den Eintrag. Eine eigene Seite je Leistung und, bei mehreren Einzugsgebieten, je Ort — mit echtem, unterschiedlichem Inhalt, nicht derselbe Text mit ausgetauschtem Ortsnamen. Diese Seiten geben Google den Zusammenhang zwischen Ihrem Betrieb, der Leistung und dem Gebiet.</p>

    <h2>Der häufigste Fehler</h2>
    <p>Eine Seite mit dreißig Ortsnamen in einer Liste am Seitenende. Das hat vor zehn Jahren funktioniert und wird heute als das erkannt, was es ist. Besser sind wenige echte Seiten für die Orte, aus denen tatsächlich Kundschaft kommt.</p>

    <div class="cs-note">
      <h3>Kurz gesagt</h3>
      <p>Profil vollständig, Angaben überall gleich, Bewertungen einsammeln, pro Leistung eine Seite. In dieser Reihenfolge. Was bei Ihnen fehlt, steht in der <a href="../kontakt.html">kostenlosen Analyse</a>.</p>
    </div>
"""),
]

LEXIKON = [

("keyword",
 u"Keyword",
 u"Der Begriff, den jemand bei Google eingibt — und auf den eine Seite ausgerichtet wird.",
 u"""
    <p>Ein Keyword ist nichts anderes als das, was ein Mensch in das Suchfeld tippt. „Schreiner Stuttgart“, „Fenster abdichten Kosten“, „Steuerberater für Kleinunternehmer“. In der Suchmaschinenoptimierung bezeichnet der Begriff den Suchausdruck, auf den eine einzelne Seite ausgerichtet wird.</p>
    <h2>Warum es darauf ankommt</h2>
    <p>Google ordnet Seiten einzelnen Suchanfragen zu, nicht ganzen Unternehmen. Jede Seite braucht deshalb einen Begriff, für den sie gebaut wurde. Fehlt diese Zuordnung, konkurrieren mehrere eigene Seiten um denselben Begriff und schwächen sich gegenseitig — siehe <a href="keyword-kannibalisierung.html">Keyword-Kannibalisierung</a>.</p>
    <h2>Häufiger Fehler</h2>
    <p>Begriffe wählen, die das Unternehmen benutzt, statt derer, die die Kundschaft benutzt. „Sanitärinstallation“ steht im Firmenprofil, gesucht wird „Klempner in der Nähe“.</p>
    <p>Wie man die richtigen findet, steht unter <a href="keyword-recherche-fuer-einsteiger.html">Keyword-Recherche für Einsteiger</a>, und was wir daraus bauen, unter <a href="../leistungen/seo.html">SEO</a>.</p>
"""),

("suchintention",
 u"Suchintention",
 u"Was jemand vorhat, der einen Begriff eingibt — kaufen, vergleichen oder nur nachschlagen.",
 u"""
    <p>Die Suchintention ist die Absicht hinter einer Suchanfrage. Üblicherweise unterscheidet man drei Arten: jemand will etwas <strong>wissen</strong> („wie funktioniert eine Wärmepumpe“), etwas <strong>finden</strong> („Stadtwerke Göppingen Login“) oder etwas <strong>tun bzw. kaufen</strong> („Wärmepumpe installieren lassen“).</p>
    <h2>Warum es darauf ankommt</h2>
    <p>Google zeigt für jede Anfrage den Seitentyp, der zur Absicht passt. Eine Verkaufsseite wird bei einem Begriff, hinter dem Wissensdurst steht, nicht ranken — unabhängig davon, wie gut sie gemacht ist. Umgekehrt bringt ein Ratgeber keine Aufträge, wenn der Suchende kaufen wollte.</p>
    <h2>Wie man sie prüft</h2>
    <p>Begriff eingeben und ansehen, was Google bereits auf Seite 1 zeigt. Stehen dort Shops, ist die Absicht kommerziell. Stehen dort Anleitungen und Videos, ist sie es nicht. Diese Prüfung dauert zehn Sekunden und erspart manchmal Wochen.</p>
    <p>Siehe auch <a href="keyword.html">Keyword</a> und <a href="long-tail-keyword.html">Long-Tail-Keyword</a>.</p>
"""),

("long-tail-keyword",
 u"Long-Tail-Keyword",
 u"Längere, genauere Suchanfragen mit weniger Volumen und deutlich mehr Kaufabsicht.",
 u"""
    <p>Als Long-Tail bezeichnet man längere, spezifische Suchanfragen: nicht „Anwalt“, sondern „Fachanwalt Arbeitsrecht Kündigung Göppingen“. Einzeln hat jede davon wenig Volumen. In der Summe machen sie den größten Teil aller Suchanfragen aus.</p>
    <h2>Warum es darauf ankommt</h2>
    <p>Zwei Gründe. Erstens ist der Wettbewerb deutlich geringer: Bei einem Wort treten Sie gegen Anbieter mit zwanzig Jahren Vorsprung an, bei fünf Wörtern oft gegen niemanden. Zweitens ist die Absicht klarer. Wer so genau sucht, weiß, was er will, und ist näher an der Anfrage.</p>
    <h2>Häufiger Fehler</h2>
    <p>Den großen Begriff anvisieren, weil die Zahl daneben größer aussieht. Hundert Besucher, die etwas Bestimmtes suchen, sind mehr wert als zehntausend, die sich umschauen.</p>
    <p>Siehe auch <a href="suchintention.html">Suchintention</a> und <a href="warum-findet-mich-bei-google-niemand.html">Warum findet mich bei Google niemand?</a></p>
"""),

("meta-title",
 u"Meta-Title",
 u"Die anklickbare Überschrift eines Treffers im Suchergebnis.",
 u"""
    <p>Der Meta-Title ist der blaue, anklickbare Text, den Google in der Ergebnisliste anzeigt. Er steht nicht sichtbar auf der Seite selbst, sondern im Quelltext, und er ist für jede Seite ein eigener.</p>
    <h2>Warum es darauf ankommt</h2>
    <p>Er wirkt zweifach: Google benutzt ihn für die Einordnung, und der Mensch entscheidet an ihm, ob er klickt. Die beste Position bringt nichts, wenn der Titel nicht erkennen lässt, dass hier die passende Antwort steht.</p>
    <h2>Was hineingehört</h2>
    <p>Der Begriff, für den die Seite gebaut wurde, möglichst weit vorn, dazu das Unterscheidbare: Ort, Leistung, Besonderheit. Rund 55 bis 60 Zeichen werden angezeigt, danach schneidet Google ab. Jede Seite braucht einen eigenen Titel — identische Titel über eine ganze Website sind eines der häufigsten Versäumnisse.</p>
    <p>Siehe auch <a href="meta-description.html">Meta-Description</a> und <a href="../leistungen/onpage-und-webdesign.html">OnPage und Webdesign</a>.</p>
"""),

("meta-description",
 u"Meta-Description",
 u"Der kurze Beschreibungstext unter dem Treffer. Kein Rankingfaktor, aber entscheidend für den Klick.",
 u"""
    <p>Die Meta-Description ist der graue Text unter dem Titel im Suchergebnis. Sie ist kein Rankingfaktor — Google verwendet sie nicht für die Einordnung. Sie entscheidet aber mit darüber, ob jemand Ihren Treffer anklickt oder den darunter.</p>
    <h2>Was hineingehört</h2>
    <p>Ein Satz, der die Frage des Suchenden aufgreift, und ein zweiter, der sagt, was er auf der Seite bekommt. Rund 150 bis 160 Zeichen werden angezeigt. Keine Aufzählung von Begriffen, sondern ein Text, den ein Mensch gern liest.</p>
    <h2>Gut zu wissen</h2>
    <p>Google ersetzt die Beschreibung häufig durch einen Ausschnitt aus der Seite, wenn dieser besser zur Anfrage passt. Das ist kein Fehler und kein Grund, keine zu schreiben: Eine gute Beschreibung wird oft genug übernommen, um den Aufwand zu lohnen.</p>
    <p>Siehe auch <a href="meta-title.html">Meta-Title</a>.</p>
"""),

("h1-ueberschrift",
 u"H1-Überschrift",
 u"Die Hauptüberschrift auf der Seite. Eine pro Seite, und sie sagt, worum es geht.",
 u"""
    <p>Die H1 ist die oberste Überschrift im Text einer Seite. Anders als der <a href="meta-title.html">Meta-Title</a> steht sie sichtbar auf der Seite. Darunter gliedern H2 und H3 den Inhalt weiter.</p>
    <h2>Warum es darauf ankommt</h2>
    <p>Sie ist für Google und für den Besucher das erste Signal, worum es auf dieser Seite geht. Eine Seite ohne H1 oder mit einer H1, in der nur der Firmenname steht, verschenkt diese Stelle.</p>
    <h2>Regeln, die wirklich gelten</h2>
    <p>Eine H1 pro Seite. Sie enthält den Begriff, für den die Seite gebaut wurde. Die Gliederung darunter folgt der Logik des Inhalts, nicht dem Aussehen: Überschriftenebenen sind kein Werkzeug, um Text größer zu machen. Dafür gibt es Gestaltung.</p>
    <p>Siehe auch <a href="../leistungen/onpage-und-webdesign.html">OnPage und Webdesign</a>.</p>
"""),

("alt-text",
 u"Alt-Text",
 u"Die Textbeschreibung eines Bildes — für Screenreader, für die Bildersuche und wenn das Bild nicht lädt.",
 u"""
    <p>Der Alt-Text ist eine kurze Beschreibung, die im Quelltext bei jedem Bild hinterlegt wird. Sichtbar wird er, wenn das Bild nicht lädt. Vorgelesen wird er von Screenreadern. Und er ist das Einzige, woran eine Suchmaschine erkennt, was auf dem Bild zu sehen ist.</p>
    <h2>Warum es darauf ankommt</h2>
    <p>Zum einen Barrierefreiheit: Für blinde Nutzer ist der Alt-Text das Bild. Zum anderen die Bildersuche, die in manchen Branchen ein eigener Einstieg ist — bei allem, wo Menschen zuerst sehen wollen, bevor sie lesen.</p>
    <h2>Wie er aussehen sollte</h2>
    <p>Beschreibend und knapp: „Monteur verlegt Fußbodenheizung in einem Neubau“. Nicht „bild1.jpg“, nicht eine Aneinanderreihung von Suchbegriffen. Rein dekorative Bilder bekommen einen leeren Alt-Text, damit Screenreader sie überspringen.</p>
    <p>Wie wir das in einem Projekt umgesetzt haben, steht in der <a href="../referenzen/poseypets.html">Fallstudie PoseyPets</a>.</p>
"""),

("backlink",
 u"Backlink",
 u"Ein Link von einer fremden Seite auf Ihre. Nach wie vor einer der stärksten Faktoren.",
 u"""
    <p>Ein Backlink ist ein Link, der von einer anderen Website auf Ihre zeigt. Für Google ist er eine Empfehlung: Wer verlinkt wird, muss etwas haben, das verlinkenswert ist.</p>
    <h2>Worauf es ankommt</h2>
    <p>Nicht auf die Anzahl, sondern auf die Herkunft. Ein Link aus einem regionalen Nachrichtenportal, von einem Branchenverband oder aus einem Fachbeitrag wiegt mehr als hundert aus Verzeichnissen, die nur existieren, um Links zu verteilen. Die einfachste Prüfung: Würde diese Erwähnung auch Sinn ergeben, wenn es keine Suchmaschinen gäbe?</p>
    <h2>Was schadet</h2>
    <p>Gekaufte Links aus Netzwerken und maschinell verteilter Tausch in großer Zahl. Beides ist erkennbar, und der Schaden trifft nicht eine Unterseite, sondern die gesamte Domain. Deshalb ist jedes Angebot mit einer festen Zahl Links pro Monat ein Warnzeichen.</p>
    <p>Siehe <a href="../leistungen/linkaufbau.html">Linkaufbau</a> und <a href="unserioese-seo-agentur-erkennen.html">Woran Sie eine unseriöse SEO-Agentur erkennen</a>.</p>
"""),

("interne-verlinkung",
 u"Interne Verlinkung",
 u"Links innerhalb der eigenen Website. Sie verteilen Aufmerksamkeit und Kraft.",
 u"""
    <p>Interne Verlinkung bezeichnet alle Links, die von einer Seite Ihrer Website auf eine andere zeigen — aus dem Menü, aus dem Text, aus dem Fußbereich.</p>
    <h2>Warum es darauf ankommt</h2>
    <p>Sie hat zwei Aufgaben. Erstens findet Google über Links neue Seiten: Was nirgends verlinkt ist, wird schlecht oder gar nicht gefunden. Zweitens geben starke Seiten über Links einen Teil ihrer Kraft weiter. Welche Ihrer Seiten die wichtigste ist, teilen Sie Google unter anderem dadurch mit, wie oft und von wo Sie darauf verlinken.</p>
    <h2>Eine Regel aus der Praxis</h2>
    <p>Etwa 60 Prozent der Links in Inhalten sollten auf Seiten zeigen, die verkaufen, 40 Prozent auf weitere Inhalte. Ohne eine solche Quote verlinkt eine Inhaltssammlung nach einiger Zeit fast nur noch sich selbst — die Artikel ranken dann, bringen aber niemanden mehr dorthin, wo Geld verdient wird.</p>
    <p>Siehe <a href="../referenzen/poseypets.html">Fallstudie PoseyPets</a>.</p>
"""),

("indexierung",
 u"Indexierung",
 u"Die Aufnahme einer Seite in den Datenbestand von Google. Ohne sie gibt es keine Position.",
 u"""
    <p>Indexierung bezeichnet den Vorgang, bei dem Google eine Seite abruft, auswertet und in seinen Datenbestand aufnimmt. Erst danach kann sie überhaupt in den Ergebnissen erscheinen.</p>
    <h2>Warum es darauf ankommt</h2>
    <p>Eine nicht indexierte Seite steht nicht auf Position 90 — sie existiert für die Suche nicht. Das ist der erste Punkt, den man prüft, wenn eine Seite keine Besucher bringt, und überraschend oft auch schon der letzte.</p>
    <h2>Wie man es prüft</h2>
    <p>In der Google-Suche <code>site:ihre-domain.de</code> eingeben. Genauer geht es in der <a href="search-console.html">Search Console</a>, die für jede Seite ausweist, ob sie aufgenommen wurde und wenn nicht, warum.</p>
    <h2>Typische Ursachen für fehlende Indexierung</h2>
    <p>Ein vergessenes <a href="noindex.html">noindex</a> aus der Entwicklungsphase, eine blockierende <a href="robots-txt.html">robots.txt</a>, ein falsch gesetztes <a href="canonical-tag.html">Canonical-Tag</a> oder schlicht eine Seite, auf die intern kein Link zeigt.</p>
"""),
]

LEXIKON += [

("noindex",
 u"noindex",
 u"Eine Anweisung, eine Seite nicht in den Suchindex aufzunehmen. Nützlich — und gefährlich, wenn vergessen.",
 u"""
    <p><code>noindex</code> ist eine Anweisung im Quelltext einer Seite, die Suchmaschinen sagt: Diese Seite bitte nicht in die Ergebnisse aufnehmen. Die Seite bleibt für Besucher erreichbar, taucht aber in der Suche nicht auf.</p>
    <h2>Wofür man es braucht</h2>
    <p>Für Seiten, die niemand über die Suche finden soll: Dankeseiten nach einem Formular, interne Suchergebnisse, Testseiten, doppelte Druckansichten.</p>
    <h2>Warum es gefährlich ist</h2>
    <p>Während der Entwicklung wird eine Website meist komplett auf <code>noindex</code> gesetzt, damit die unfertige Fassung nicht in der Suche landet. Wird das beim Livegang vergessen, ist die fertige Seite monatelang unsichtbar — und niemand merkt es, weil die Seite ja aufrufbar ist. Das ist einer der häufigsten und teuersten Fehler überhaupt.</p>
    <p>Prüfen lässt sich das über die <a href="search-console.html">Search Console</a> oder mit <code>site:ihre-domain.de</code>. Siehe auch <a href="indexierung.html">Indexierung</a>.</p>
"""),

("robots-txt",
 u"robots.txt",
 u"Eine Datei, die Suchmaschinen sagt, welche Bereiche sie nicht abrufen sollen.",
 u"""
    <p>Die <code>robots.txt</code> liegt im Hauptverzeichnis einer Website und enthält Regeln dafür, welche Bereiche Suchmaschinen abrufen dürfen. Sie ist das erste, was ein Crawler ansieht.</p>
    <h2>Ein wichtiger Unterschied</h2>
    <p>Die Datei steuert das <strong>Abrufen</strong>, nicht das <strong>Anzeigen</strong>. Eine über robots.txt gesperrte Seite kann trotzdem in den Ergebnissen erscheinen, wenn andere Seiten darauf verlinken — dann allerdings ohne Beschreibung. Wer eine Seite zuverlässig aus den Ergebnissen halten will, braucht <a href="noindex.html">noindex</a>, nicht robots.txt.</p>
    <h2>Häufiger Fehler</h2>
    <p>Ein <code>Disallow: /</code> aus der Entwicklungsphase, das live bleibt. Damit ist die gesamte Website gesperrt. Zweithäufigster Fehler: CSS- und Bildverzeichnisse sperren, wodurch Google die Seite nicht mehr so sieht wie ein Besucher und sie schlechter bewertet.</p>
    <p>Siehe auch <a href="sitemap.html">Sitemap</a> und <a href="indexierung.html">Indexierung</a>.</p>
"""),

("sitemap",
 u"Sitemap",
 u"Eine Liste aller Seiten einer Website für Suchmaschinen.",
 u"""
    <p>Eine XML-Sitemap ist eine Datei, die alle Adressen einer Website auflistet, die in der Suche erscheinen sollen, oft mit dem Datum der letzten Änderung. Sie wird in der <a href="search-console.html">Search Console</a> hinterlegt.</p>
    <h2>Was sie leistet — und was nicht</h2>
    <p>Sie hilft Google, Seiten zu finden, besonders bei großen Websites und bei Seiten, auf die wenig intern verlinkt wird. Sie ist aber keine Garantie für Aufnahme: Google entscheidet weiterhin selbst, was in den Index kommt. Eine Sitemap ersetzt deshalb keine gute <a href="interne-verlinkung.html">interne Verlinkung</a>.</p>
    <h2>Häufiger Fehler</h2>
    <p>Eine Sitemap, die Seiten enthält, die auf <a href="noindex.html">noindex</a> stehen, weitergeleitet werden oder nicht mehr existieren. Das sind widersprüchliche Angaben, und sie kosten Vertrauen in die gesamte Datei.</p>
"""),

("canonical-tag",
 u"Canonical-Tag",
 u"Ein Hinweis, welche von mehreren gleichen Seiten die maßgebliche ist.",
 u"""
    <p>Das Canonical-Tag ist eine Angabe im Quelltext, die sagt: Es gibt diese Seite unter mehreren Adressen, aber diese hier ist die richtige. Google soll die Signale aller Varianten auf dieser einen bündeln.</p>
    <h2>Wofür man es braucht</h2>
    <p>Dieselbe Seite ist oft über mehrere Adressen erreichbar — mit und ohne <code>www</code>, mit angehängten Parametern aus Werbekampagnen, in Shops über verschiedene Kategoriepfade. Ohne Canonical behandelt Google sie als mehrere Seiten, die sich gegenseitig Konkurrenz machen.</p>
    <h2>Häufiger Fehler</h2>
    <p>Ein Canonical, das auf jeder Seite auf die Startseite zeigt. Das kommt bei falsch konfigurierten Vorlagen vor und sorgt dafür, dass sämtliche Unterseiten aus dem Index verschwinden. Zweithäufigster Fehler: Canonical auf eine Seite, die ihrerseits auf <a href="noindex.html">noindex</a> steht.</p>
    <p>Siehe auch <a href="keyword-kannibalisierung.html">Keyword-Kannibalisierung</a>.</p>
"""),

("301-weiterleitung",
 u"301-Weiterleitung",
 u"Die dauerhafte Umleitung einer alten Adresse auf eine neue — der Rettungsanker bei jedem Umbau.",
 u"""
    <p>Eine 301-Weiterleitung sagt Browser und Suchmaschine: Diese Adresse gibt es nicht mehr, der Inhalt liegt dauerhaft dort. Im Unterschied zur 302, die nur eine vorübergehende Umleitung meldet, gibt die 301 den größten Teil der aufgebauten Signale an das neue Ziel weiter.</p>
    <h2>Wann man sie braucht</h2>
    <p>Bei jedem Umbau, der Adressen verändert: neues System, neue Struktur, Umzug auf eine andere Domain, Wechsel auf HTTPS. Ohne Weiterleitung verliert jede Seite, die rankte, ihre Position, und Besucher landen auf einer Fehlerseite.</p>
    <h2>So geht man vor</h2>
    <p>Vor dem Umbau eine vollständige Liste aller bestehenden Adressen ziehen. Nach dem Umbau für jede eine Weiterleitung auf die inhaltlich passende neue Seite setzen — nicht pauschal alles auf die Startseite. Eine pauschale Umleitung aller alten Adressen auf die Startseite wertet Google wie eine Fehlerseite.</p>
    <p>Siehe auch <a href="neue-website-fuer-seo.html">Brauche ich für SEO eine neue Website?</a></p>
"""),

("keyword-kannibalisierung",
 u"Keyword-Kannibalisierung",
 u"Wenn zwei eigene Seiten um denselben Suchbegriff konkurrieren und sich gegenseitig schwächen.",
 u"""
    <p>Von Kannibalisierung spricht man, wenn mehrere Seiten derselben Website auf denselben Suchbegriff ausgerichtet sind. Google muss sich dann entscheiden, welche davon angezeigt wird — und beide verlieren, weil sich Signale und Verlinkung auf zwei Seiten verteilen statt auf einer zu bündeln.</p>
    <h2>Woran man es erkennt</h2>
    <p>In der <a href="search-console.html">Search Console</a> eine Suchanfrage auswählen und ansehen, welche Seiten dafür angezeigt werden. Wechseln sich zwei Adressen ab oder stehen beide auf mittelmäßigen Plätzen, liegt der Fall vor.</p>
    <h2>Was man tut</h2>
    <p>Entscheiden, welche Seite die maßgebliche sein soll. Die andere entweder inhaltlich klar auf einen anderen Begriff ausrichten, in die erste zusammenführen und per <a href="301-weiterleitung.html">301</a> weiterleiten, oder per <a href="canonical-tag.html">Canonical</a> der ersten zuordnen.</p>
    <p>Vorbeugen ist einfacher: ein Suchbegriff, eine Seite. Siehe <a href="keyword-recherche-fuer-einsteiger.html">Keyword-Recherche für Einsteiger</a>.</p>
"""),

("local-pack",
 u"Local Pack",
 u"Die Box mit Karte und drei Einträgen bei Suchen mit Ortsbezug.",
 u"""
    <p>Das Local Pack ist der Kasten mit Kartenausschnitt und drei Unternehmenseinträgen, den Google bei Suchen mit örtlichem Bezug über den normalen Ergebnissen zeigt — mit Bewertung, Öffnungszeiten, Telefonnummer und Route.</p>
    <h2>Warum es darauf ankommt</h2>
    <p>Für ortsgebundene Betriebe passiert hier ein großer Teil der Kontaktaufnahme, bevor jemand die normalen Treffer überhaupt ansieht. Viele Nutzer rufen direkt aus dem Eintrag an, ohne die Website zu besuchen.</p>
    <h2>Was über die Platzierung entscheidet</h2>
    <p>Relevanz, Entfernung und Bekanntheit. Die Entfernung lässt sich nicht beeinflussen, die anderen beiden schon: über Kategorie und Leistungen im <a href="google-unternehmensprofil-einrichten.html">Unternehmensprofil</a>, über einheitliche Angaben in allen Verzeichnissen und über Bewertungen.</p>
    <p>Mehr dazu unter <a href="lokale-seo-handwerker-dienstleister.html">Lokale SEO für Handwerk und Dienstleistung</a>.</p>
"""),

("search-console",
 u"Google Search Console",
 u"Das kostenlose Werkzeug von Google, das zeigt, wofür Sie gefunden werden.",
 u"""
    <p>Die Search Console ist ein kostenloser Dienst von Google für Websitebetreiber. Sie zeigt, bei welchen Suchanfragen Ihre Seiten erscheinen, wie oft sie angeklickt werden, auf welcher Position sie stehen und welche technischen Probleme Google feststellt.</p>
    <h2>Warum sie zuerst eingerichtet wird</h2>
    <p>Sie ist die einzige Quelle, die echte Suchdaten zu Ihrer eigenen Website liefert — keine Schätzung, sondern das, was Google tatsächlich gemessen hat. Jede Arbeit an der Sichtbarkeit beginnt sinnvollerweise damit, sie einzurichten und ein paar Wochen Daten zu sammeln.</p>
    <h2>Worauf man zuerst schaut</h2>
    <p>Auf den Bericht zur <a href="indexierung.html">Indexierung</a>: Welche Seiten sind aufgenommen, welche nicht und warum. Danach auf die Suchanfragen: Wofür werden Sie bereits gefunden, oft überraschenderweise für Begriffe, an die niemand gedacht hat.</p>
    <h2>Wichtig</h2>
    <p>Das Konto gehört Ihnen, nicht Ihrer Agentur. Siehe <a href="unserioese-seo-agentur-erkennen.html">Woran Sie eine unseriöse SEO-Agentur erkennen</a> und <a href="../leistungen/reporting.html">Reporting</a>.</p>
"""),

("strukturierte-daten",
 u"Strukturierte Daten",
 u"Zusätzliche Auszeichnung im Quelltext, mit der Google Inhalte eindeutig versteht.",
 u"""
    <p>Strukturierte Daten sind maschinenlesbare Angaben im Quelltext, die den Inhalt einer Seite eindeutig benennen: Das hier ist eine Adresse, das ein Preis, das eine Öffnungszeit, das eine Frage mit Antwort. Üblich ist das Format JSON-LD nach dem Vokabular von schema.org.</p>
    <h2>Was sie bringen</h2>
    <p>Google kann daraus erweiterte Darstellungen im Suchergebnis bauen — Sternebewertungen, Öffnungszeiten, aufklappbare Fragen, Preisangaben. Diese Einträge sind größer und auffälliger und bekommen mehr Klicks, auch bei gleicher Position.</p>
    <h2>Was sie nicht bringen</h2>
    <p>Sie sind kein direkter Rankingfaktor. Die Seite steigt nicht, weil sie ausgezeichnet ist. Sie fällt im Ergebnis nur mehr auf.</p>
    <h2>Häufiger Fehler</h2>
    <p>Auszeichnungen für Inhalte, die auf der Seite nicht sichtbar sind, etwa Bewertungen, die nirgends stehen. Das wertet Google als Täuschung und kann zu einer manuellen Maßnahme führen.</p>
"""),

("sichtbarkeitsindex",
 u"Sichtbarkeitsindex",
 u"Eine Kennzahl, die zeigt, wie präsent eine Domain in der Suche ist — nützlich als Verlauf, nicht als Ziel.",
 u"""
    <p>Der Sichtbarkeitsindex ist eine Kennzahl von Analyse-Anbietern wie Sistrix. Sie fasst zusammen, für wie viele Begriffe eine Domain rankt, auf welchen Positionen und wie häufig diese Begriffe gesucht werden.</p>
    <h2>Wofür er gut ist</h2>
    <p>Als Verlauf über Monate. Steigt die Kurve, geht etwas in die richtige Richtung; ein plötzlicher Einbruch ist ein verlässliches Alarmsignal, etwa nach einem Umbau ohne <a href="301-weiterleitung.html">Weiterleitungen</a>.</p>
    <h2>Wofür er nicht gut ist</h2>
    <p>Als Ziel. Der Index unterscheidet nicht, ob ein Begriff Umsatz bringt. Eine Domain kann an Sichtbarkeit gewinnen und gleichzeitig weniger Anfragen bekommen, wenn die neuen Begriffe nichts mit dem Geschäft zu tun haben. Umgekehrt kann eine kleine Verbesserung bei drei kaufnahen Begriffen die Kurve kaum bewegen und trotzdem Aufträge bringen.</p>
    <p>Deshalb steht in unseren Berichten, was sich bei den <em>vereinbarten</em> Begriffen bewegt hat. Siehe <a href="../leistungen/reporting.html">Reporting</a>.</p>
"""),
]
