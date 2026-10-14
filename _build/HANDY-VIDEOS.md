# Die zwei Handy-Videos auf der Startseite

Im Abschnitt „Der erste Monat kostet nichts" stehen zwei Handys nebeneinander,
links Instagram, rechts TikTok. Beide sind iPhone 18 Pro Max aus CSS, in jedem
läuft eine stumme Videoschleife.

**Stand: gebaut und auf der Seite.** Früher lag dort die flache Grafik
`assets/img/phones-feed.png`. Sie wird nicht mehr eingebunden.

---

## Was wo liegt

```
assets/video/reel-instagram.{mp4,webm,jpg}   19,2 s
assets/video/reel-tiktok.{mp4,webm,jpg}      16,2 s
_build/reels-loop.sh                         schneidet die Schleifen
```

Die Handyrahmen stehen in `assets/css/site.css` im Block „Gratismonat", die
Auszeichnung in `index.html` und in `_build/make_pages.py` (für `angebot.html`).

---

## Schleifen neu schneiden

Voraussetzung ist ffmpeg (`brew install ffmpeg`). So sind die aktuellen
Dateien entstanden:

```bash
CRF=37 CRF_WEBM=54 ./_build/reels-loop.sh ~/Downloads/instagram.mov instagram 18
CRF=37 CRF_WEBM=54 ./_build/reels-loop.sh ~/Downloads/tiktok.mov    tiktok    15
```

Das Skript schneidet auf 1320:2868 zu, sucht über Szenenerkennung die Wischer,
nimmt ab jeder Stelle höchstens 4,5 Sekunden und hängt die Stücke mit einem
echten Hochwischer aneinander.

| Variable | Standard | wofür |
|---|---|---|
| `SZENE` | `0.30` | Empfindlichkeit der Wischerkennung. Zu wenige Abschnitte: kleiner setzen, z. B. `0.15`. |
| `MAX_CLIP` | `4.5` | Länge je Reel |
| `MIN_CLIP` | `1.8` | kürzere Schnipsel fliegen raus |
| `X_ANTEIL` | `1.0` | **nicht ändern.** 1 heißt: rechts stehen lassen. Dort sitzt die Leiste mit Herz, Kommentar und Zählern. Mittig beschnitten fehlt sie, und dann erkennt niemand mehr Instagram oder TikTok. |
| `TRIM_OBEN` / `TRIM_UNTEN` | `0` | Alejandros Aufnahmen sind bereits ohne Status- und Navigationsleiste. Bei frischen Vollbildaufnahmen auf `0.055` und `0.045` setzen. |
| `CRF` / `CRF_WEBM` | `33` / `46` | größer = kleinere Datei. Für die Seite wurde 37/54 genommen. |

Zwei Dinge danach prüfen, nicht nur die Laufzeit:

- Ist von Status- oder Navigationsleiste ein Rest zu sehen? `TRIM_OBEN`
  oder `TRIM_UNTEN` erhöhen.
- **Die beiden Videos dürfen nicht gleich lang sein.** Gleichzeitig wischende
  Handys sehen sofort nach Attrappe aus. Deshalb 18 und 15 Sekunden, und
  deshalb startet das rechte über `data-versatz="2.4"` versetzt.

Zielwert je Datei: **unter 700 KB.** Reicht das nicht, in dieser Reihenfolge
nachbessern: `CRF` erhöhen, Laufzeit kürzen, `BREITE` von 400 auf 360.

---

## bash 3.2

macOS liefert bash 3.2 aus. Das Skript kommt deshalb ohne `mapfile`, ohne
`set -u` und ohne assoziative Arrays aus. Nicht „modernisieren", sonst läuft
es auf Alejandros Rechner nicht mehr.

---

## Rechte an den gezeigten Reels

Was in den Schleifen zu sehen ist, steht auf einer Verkaufsseite. In den
aktuellen Dateien laufen **fremde Reels mit erkennbaren Gesichtern und
sichtbaren Kontonamen**. Unproblematisch wäre: Alejandros eigenes Profil,
Inhalte von Kunden mit deren Einverständnis, oder Material, bei dem niemand
identifizierbar ist. Solange das nicht geklärt ist, gehören die Schleifen
ausgetauscht, nicht veröffentlicht.
