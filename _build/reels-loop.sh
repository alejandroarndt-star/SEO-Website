#!/usr/bin/env bash
# Baut aus einer Bildschirmaufnahme (Instagram oder TikTok) eine kurze,
# nahtlos laufende Schleife fuer die Handys auf der Startseite.
#
#   ./_build/reels-loop.sh EINGABE.mov AUSGABENAME [SEKUNDEN]
#   ./_build/reels-loop.sh ~/Downloads/instagram.mov instagram 26
#   ./_build/reels-loop.sh ~/Downloads/tiktok.mov    tiktok    22
#
# Was es macht:
#   1. schneidet die Aufnahme auf das Bildschirmverhaeltnis des iPhone 18 Pro
#      Max zu (1320:2868, also 19,5:9)
#   2. sucht die Stellen, an denen gewischt wurde, ueber Szenenerkennung
#   3. nimmt ab jeder dieser Stellen hoechstens MAX_CLIP Sekunden
#   4. haengt die Stuecke mit einem echten Hochwisch-Uebergang aneinander
#   5. schreibt mp4, webm und ein Standbild
#
# Ergebnis liegt in assets/video/.
#
# Hinweis zu bash: macOS liefert bash 3.2 aus. Deshalb kein mapfile, kein
# set -u, keine assoziativen Arrays. Nicht "modernisieren", sonst laeuft es
# auf Alejandros Rechner nicht mehr.
set -eo pipefail

EIN="${1:?Erstes Argument: die Bildschirmaufnahme}"
NAME="${2:?Zweites Argument: Ausgabename, z. B. instagram}"
ZIEL_LAENGE="${3:-26}"

MAX_CLIP="${MAX_CLIP:-4.5}"      # kein Reel laenger als das
MIN_CLIP="${MIN_CLIP:-1.8}"      # kuerzere Schnipsel fliegen raus
WISCH="${WISCH:-0.3}"            # Dauer des Hochwischers
SZENE="${SZENE:-0.30}"           # Empfindlichkeit der Szenenerkennung
TRIM_OBEN="${TRIM_OBEN:-0}"      # Anteil oben weg. Alejandros Aufnahmen sind
TRIM_UNTEN="${TRIM_UNTEN:-0}"    # bereits ohne Status- und Navigationsleiste.
X_ANTEIL="${X_ANTEIL:-1.0}"      # 0 = links beschneiden, 1 = rechts stehen
                                 # lassen. Muss 1 bleiben: dort sitzt die
                                 # Leiste mit Herz, Kommentar und Zaehlern.
                                 # Ohne sie erkennt niemand Instagram/TikTok.
A_BREITE="${A_BREITE:-1320}"     # Zielverhaeltnis, iPhone 18 Pro Max
A_HOEHE="${A_HOEHE:-2868}"
BREITE="${BREITE:-400}"          # Ausgabebreite. Das Handy ist auf der
                                 # Seite rund 240px breit, 400 reicht also
                                 # auch auf dichten Displays.
FPS="${FPS:-25}"                 # 25 statt 30: spart rund ein Sechstel
CRF="${CRF:-33}"                 # h264. Groesser = kleinere Datei.
CRF_WEBM="${CRF_WEBM:-46}"       # vp9, Skala laeuft anders als bei h264.

command -v ffmpeg >/dev/null || { echo "ffmpeg fehlt. Auf dem Mac: brew install ffmpeg"; exit 1; }
[ -f "$EIN" ] || { echo "Datei nicht gefunden: $EIN"; exit 1; }

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

lies() { ffprobe -v error -select_streams v:0 -show_entries "$1" -of csv=p=0 "$2" | head -1; }
BQ=$(lies stream=width "$EIN"); HQ=$(lies stream=height "$EIN")
DAUER=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$EIN")
echo "Quelle: ${BQ}x${HQ}, ${DAUER}s"

# --- 1. Zuschnitt auf das Handyverhaeltnis ------------------------------
read NUTZ_B NUTZ_H X OBEN HOEHE <<ENDE
$(python3 - "$BQ" "$HQ" "$TRIM_OBEN" "$TRIM_UNTEN" "$X_ANTEIL" "$A_BREITE" "$A_HOEHE" "$BREITE" <<'PY'
import sys
bq, hq = int(sys.argv[1]), int(sys.argv[2])
t_o, t_u, x_anteil = float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
a_b, a_h, breite = int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8])
gerade = lambda v: max(2, int(v) // 2 * 2)
oben, unten = gerade(hq * t_o), gerade(hq * t_u)
nutz_h = hq - oben - unten
nutz_b = gerade(min(bq, nutz_h * a_b / a_h))
nutz_h = gerade(min(nutz_h, nutz_b * a_h / a_b))
x = gerade((bq - nutz_b) * x_anteil)
print(nutz_b, nutz_h, x, oben, gerade(breite * a_h / a_b))
PY
)
ENDE
echo "Zuschnitt: ${NUTZ_B}x${NUTZ_H} ab x=${X} y=${OBEN}  ->  ${BREITE}x${HOEHE}"

ffmpeg -loglevel error -y -i "$EIN" \
  -vf "crop=${NUTZ_B}:${NUTZ_H}:${X}:${OBEN},scale=${BREITE}:${HOEHE}:flags=lanczos,fps=${FPS}" \
  -an -c:v libx264 -crf 17 -preset veryfast "$TMP/roh.mp4"

# --- 2. Wischstellen finden ---------------------------------------------
ffmpeg -loglevel error -y -i "$TMP/roh.mp4" \
  -vf "select='gt(scene,${SZENE})',metadata=print:file=$TMP/szenen.txt" \
  -an -f null - 2>/dev/null || true
MARKEN=$(grep -o 'pts_time:[0-9.]*' "$TMP/szenen.txt" 2>/dev/null | cut -d: -f2 || true)

# --- 3. Abschnitte bilden ------------------------------------------------
STARTS=()
while IFS= read -r z; do
  [ -n "$z" ] && STARTS[${#STARTS[@]}]="$z"
done < <(printf '0\n%s\n' "$MARKEN" | awk 'NF' | sort -g -u)

SEGS=(); ANZ=0; SUMME=0; i=0
while [ $i -lt ${#STARTS[@]} ]; do
  A="${STARTS[$i]}"
  if [ $((i+1)) -lt ${#STARTS[@]} ]; then NAECHST="${STARTS[$((i+1))]}"; else NAECHST="$DAUER"; fi
  LAENGE=$(python3 -c "print(round(min(float('$NAECHST')-float('$A'), float('$MAX_CLIP')), 3))")
  OK=$(python3 -c "print(1 if $LAENGE >= $MIN_CLIP else 0)")
  if [ "$OK" = "1" ]; then
    ffmpeg -loglevel error -y -ss "$A" -t "$LAENGE" -i "$TMP/roh.mp4" \
      -an -c:v libx264 -crf 17 -preset veryfast "$TMP/seg${ANZ}.mp4"
    SEGS[$ANZ]="$TMP/seg${ANZ}.mp4"
    ANZ=$((ANZ+1))
    SUMME=$(python3 -c "print(round($SUMME + $LAENGE - $WISCH, 3))")
  fi
  ERREICHT=$(python3 -c "print(1 if $SUMME >= $ZIEL_LAENGE else 0)")
  [ "$ERREICHT" = "1" ] && break
  i=$((i+1))
done

[ $ANZ -ge 1 ] || { echo "Keine brauchbaren Abschnitte gefunden. SZENE kleiner setzen, z. B. SZENE=0.15"; exit 1; }
echo "Abschnitte: ${ANZ}, zusammen rund ${SUMME}s"

# --- 4. Mit Hochwischer verketten ---------------------------------------
if [ $ANZ -eq 1 ]; then
  cp "${SEGS[0]}" "$TMP/kette.mp4"
else
  EINGABEN=(); FILTER=""; VOR="[0:v]"; OFF=0
  n=0
  while [ $n -lt $ANZ ]; do EINGABEN[${#EINGABEN[@]}]="-i"; EINGABEN[${#EINGABEN[@]}]="${SEGS[$n]}"; n=$((n+1)); done
  k=1
  while [ $k -lt $ANZ ]; do
    LEN=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "${SEGS[$((k-1))]}")
    OFF=$(python3 -c "print(round($OFF + $LEN - $WISCH, 3))")
    if [ $k -eq $((ANZ-1)) ]; then AUS="[v]"; else AUS="[x$k]"; fi
    FILTER="${FILTER}${VOR}[${k}:v]xfade=transition=slideup:duration=${WISCH}:offset=${OFF}${AUS};"
    VOR="[x$k]"
    k=$((k+1))
  done
  ffmpeg -loglevel error -y "${EINGABEN[@]}" \
    -filter_complex "${FILTER%;}" -map "[v]" \
    -an -c:v libx264 -crf 18 -preset veryfast "$TMP/kette.mp4"
fi

# --- 5. Ausgabe ----------------------------------------------------------
mkdir -p "$ROOT/assets/video"
ffmpeg -loglevel error -y -i "$TMP/kette.mp4" \
  -c:v libx264 -crf ${CRF} -preset slow -pix_fmt yuv420p -movflags +faststart -an \
  "$ROOT/assets/video/reel-${NAME}.mp4"
ffmpeg -loglevel error -y -i "$TMP/kette.mp4" \
  -c:v libvpx-vp9 -crf ${CRF_WEBM} -b:v 0 -row-mt 1 -deadline good -cpu-used 2 -an \
  "$ROOT/assets/video/reel-${NAME}.webm"
ffmpeg -loglevel error -y -ss 0.4 -i "$TMP/kette.mp4" -frames:v 1 -q:v 4 \
  "$ROOT/assets/video/reel-${NAME}.jpg"

L=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$ROOT/assets/video/reel-${NAME}.mp4")
echo "Fertig: assets/video/reel-${NAME}.{mp4,webm,jpg}  (${L}s)"
ls -la "$ROOT/assets/video/reel-${NAME}".* | awk '{print "  ", $5, $9}'
