# Website

Statische Website, ausgeliefert über GitHub Pages. Kein Build nötig, keine
Abhängigkeiten, kein Framework.

## Aufbau

```
index.html                         Startseite
kontakt.html                       Kontakt und Sichtbarkeits-Check
impressum.html                     PLATZHALTER, vor dem Start ausfüllen
datenschutz.html                   PLATZHALTER, vor dem Start prüfen
blog/index.html                    Blogübersicht
assets/css/site.css                Gesamtes Design, Tokens ganz oben
assets/js/site.js                  Vanilla JS, keine Bibliotheken
assets/fonts/*.woff2               Lokal eingebundene Schriften
assets/video/hero.*                Hero Video, lokal ausgeliefert
_build/make_pages.py               Erzeugt die Unterseiten aus der Hülle
_build/make_preview.py             Baut die Artifact Vorschau, nicht deployen
_artifact/page.html                Vorschau Variante, nicht deployen
```

## Datenschutz, bewusste Entscheidungen

- Schriften liegen lokal, keine Verbindung zu Google Fonts.
- Video liegt lokal, kein YouTube oder Vimeo Embed.
- Kein Analytics, kein Tracking, keine Cookies, deshalb kein Cookie Banner.
- Kein externes CDN. Alles kommt vom eigenen Webspace.

Diese Punkte beim Erweitern nicht aufgeben. Eine eingebundene Google Schrift
oder eine Kartenanzeige macht die Seite abmahnbar und erzwingt einen Banner.

## Unterseiten ändern

Header und Footer stehen in `index.html`. Nach einer Änderung dort:

```
python3 _build/make_pages.py
```

Das schreibt die Unterseiten neu. Die erzeugten HTML Dateien sind das, was
ausgeliefert wird, und gehören ins Repo.

## Vor dem Start

- [ ] Markenname festlegen und „Markenname" an drei Stellen in `index.html`
      ersetzen, dann `make_pages.py` laufen lassen
- [ ] `impressum.html` vollständig ausfüllen, Klarname und ladungsfähige Anschrift
- [ ] `datenschutz.html` prüfen, Verantwortlichen eintragen
- [ ] Abschnitt „Ergebnisse“ in `index.html`: echte Zahlen eintragen ODER den
      ganzen Abschnitt löschen. Die Platzhalter dürfen nicht online gehen.
- [ ] Echte Kontaktdaten in `kontakt.html`
- [ ] Repo auf öffentlich stellen, Pages aktivieren, Custom Domain eintragen
- [ ] `CNAME` Datei mit der Domain anlegen

## Lokal ansehen

```
python3 -m http.server 8777
```

Dann http://127.0.0.1:8777 öffnen.

## Lizenzen

- Schriften: Bricolage Grotesque, Archivo, JetBrains Mono, alle SIL Open Font License.
- Hero Video: Clips von mixkit.co, Mixkit Free License, kommerzielle Nutzung
  erlaubt, keine Namensnennung nötig. Die Clips dürfen nicht als Rohmaterial
  weitergegeben werden, die Verwendung als Hintergrund hier ist abgedeckt.
