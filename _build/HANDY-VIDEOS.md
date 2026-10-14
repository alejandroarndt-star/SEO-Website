# Die zwei Handy-Videos auf der Startseite

Auf der Startseite stehen im Abschnitt „Der erste Monat kostet nichts" zwei
Handys nebeneinander. Links Instagram, rechts TikTok. Aktuell ist das eine
flache Grafik (`assets/img/phones-feed.png`). Sie soll durch zwei echte,
laufende Videoschleifen ersetzt werden.

Dieses Dokument beschreibt, was zu tun ist. Gedacht für eine Session, die
direkt auf Alejandros Rechner läuft und damit an die Aufnahmen kommt.

---

## Ausgangsmaterial

Zwei Bildschirmaufnahmen vom Handy, von Alejandro erstellt, liegen in seinem
Downloads-Ordner:

- eine Aufnahme beim Durchscrollen von **Instagram Reels**
- eine Aufnahme beim Durchscrollen von **TikTok**

**Vor der Verwendung prüfen:** Was in den Aufnahmen zu sehen ist, landet auf
einer Verkaufsseite. Fremde Reels bedeuten fremde Videos und fremde Gesichter
auf Alejandros Seite. Unproblematisch sind: sein eigenes Profil, Inhalte von
Kunden mit deren Einverständnis, oder Material, bei dem erkennbar niemand
identifizierbar ist. Im Zweifel neu aufnehmen, nicht veröffentlichen.

---

## Schritt 1: Schnitt

Dafür gibt es `_build/reels-loop.sh`. Es nimmt eine Aufnahme und macht daraus
eine Schleife. Voraussetzung ist ffmpeg (`brew install ffmpeg`).

```bash
./_build/reels-loop.sh ~/Downloads/instagram.mov instagram 30
./_build/reels-loop.sh ~/Downloads/tiktok.mov    tiktok    30
```

Was das Skript tut:

1. schneidet auf 9:16 zu und entfernt Statusleiste oben und Navigationsleiste
   unten
2. findet über Szenenerkennung die Stellen, an denen gewischt wurde
3. nimmt ab jeder Stelle höchstens 4,5 Sekunden, verwirft Schnipsel unter
   1,8 Sekunden
4. hängt die Stücke mit einem echten Hochwischer aneinander
   (`xfade=transition=slideup`), damit auch Reels, die in der Aufnahme nicht
   aufeinander folgen, wie ein durchgehendes Scrollen wirken
5. schreibt `assets/video/reel-<name>.mp4`, `.webm` und ein Standbild `.jpg`

**Das Skript ist noch nie mit echtem Material gelaufen.** Es ist auf Syntax
geprüft, mehr nicht. Rechne mit einer Runde Nachstellen über diese Variablen:

| Variable | Standard | wofür |
|---|---|---|
| `SZENE` | `0.30` | Empfindlichkeit der Wischerkennung. Werden zu wenige Abschnitte gefunden: kleiner setzen, z. B. `0.15`. Zu viele: größer. |
| `MAX_CLIP` | `4.5` | Länge je Reel. Alejandros Vorgabe: nicht länger als fünf Sekunden. |
| `MIN_CLIP` | `1.8` | kürzere Schnipsel fliegen raus |
| `TRIM_OBEN` | `0.055` | Anteil oben weg. Passt bei den meisten Handys, bei Dynamic Island eher `0.07`. |
| `TRIM_UNTEN` | `0.045` | Anteil unten weg |
| `WISCH` | `0.3` | Dauer des Hochwischers |

Beispiel mit Nachstellung:

```bash
SZENE=0.15 TRIM_OBEN=0.07 ./_build/reels-loop.sh ~/Downloads/instagram.mov instagram 30
```

**Danach ansehen, nicht nur die Laufzeit prüfen.** Drei Dinge:

- Ist von Statusleiste oder Navigationsleiste noch ein Rest zu sehen? Dann
  `TRIM_OBEN` oder `TRIM_UNTEN` erhöhen.
- Sitzen die Wischer mitten in einer Bewegung oder in einer Ruhepause? Mitten
  in der Bewegung wirkt gewollt, in der Ruhepause wie ein Fehler. Notfalls
  `SZENE` verändern, damit andere Stellen gefunden werden.
- Springt die Schleife am Ende hart zurück? Dann einen Abschnitt weniger
  nehmen (`ZIEL_LAENGE` kleiner) oder einen, der ähnlich anfängt wie der
  erste.

---

## Schritt 2: Einbau auf der Seite

Noch nicht gebaut, weil die tatsächlichen Seitenverhältnisse erst mit dem
Material feststehen. Zu tun:

1. In `index.html` und in `_build/make_pages.py` (Seite `angebot.html`) steht
   jeweils ein Block `<div class="offer-art">` mit einem einzelnen `<img>`.
   Dieser wird ersetzt durch zwei Handyrahmen mit je einem `<video>`:
   `autoplay muted loop playsinline preload="metadata"`, dazu `poster` auf das
   erzeugte `.jpg` und `width`/`height` gesetzt, damit beim Laden nichts
   springt.
2. Die Rahmen übernehmen die Geometrie aus `assets/img/phones-feed.png`:
   linkes Handy um 6 Grad gegen den Uhrzeigersinn gedreht, rechtes um 5 Grad
   im Uhrzeigersinn, rechtes etwas höher und hinter dem linken.
   Eckenradius 34px außen, 22px am Bildschirm, Rahmen `#141517` mit
   1,6px Kontur `#34373b`.
3. Die bestehende Grafik bleibt als Standbild darunter liegen, für den Moment
   vor dem Laden und für `prefers-reduced-motion`.
4. **Die zwei Videos dürfen nicht synchron wischen.** Synchron sieht sofort
   nach Attrappe aus. Das rechte Video per JavaScript um rund 1,5 Sekunden
   versetzt starten, oder beim Schneiden eine andere Zahl Abschnitte nehmen,
   damit die Längen nicht gleich sind.
5. Das CSS dazu steht in `assets/css/site.css` im Block „Gratismonat".
6. Danach `python3 _build/make_pages.py` und `python3 _build/linkcheck.py`
   laufen lassen, dann im Browser auf 390px Breite prüfen, dass nichts
   seitlich überläuft.

---

## Schritt 3: Gewicht im Auge behalten

Die Startseite trägt schon das Hero-Video (rund 900 KB). Zwei weitere
Schleifen kommen dazu. Zielwert: **je unter 700 KB**. Wenn das nicht reicht,
in dieser Reihenfolge nachbessern: Breite von 540 auf 440 reduzieren,
`-crf` erhöhen, Laufzeit kürzen. Zur Not die Videos erst laden, wenn der
Abschnitt in Sicht kommt.

---

## Stand

- `_build/reels-loop.sh` ist geschrieben und syntaktisch geprüft, aber noch
  nie mit echtem Material gelaufen.
- Die Aufnahmen liegen auf Alejandros Rechner. Die Cloud-Session, in der das
  hier entstanden ist, kommt nicht an sein Dateisystem: kein Zugriff auf den
  Downloads-Ordner, und `/mnt/user-data/uploads` war leer.
- Die Grafik `assets/img/phones-feed.png` bleibt bis dahin stehen und
  funktioniert.
