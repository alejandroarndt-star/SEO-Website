#!/usr/bin/env bash
# Baut aus einer Bildschirmaufnahme (Instagram oder TikTok) eine kurze,
# nahtlos laufende Schleife fuer die Handys auf der Startseite.
#
#   ./_build/reels-loop.sh EINGABE.mov AUSGABENAME [SEKUNDEN]
#   ./_build/reels-loop.sh ~/Downloads/instagram.mov instagram
#   ./_build/reels-loop.sh ~/Downloads/tiktok.mov    tiktok 30
#
# Was es macht:
#   1. schneidet die Aufnahme auf 9:16 zu und entfernt Statusleiste oben und
#      Navigationsleiste unten (ueber TRIM_OBEN und TRIM_UNTEN einstellbar)
#   2. sucht die Stellen, an denen gewischt wurde, ueber Szenenerkennung
#   3. nimmt ab jeder dieser Stellen hoechstens MAX_CLIP Sekunden
#   4. haengt die Stuecke mit einem echten Hochwisch-Uebergang aneinander
#   5. schreibt mp4, webm und ein Standbild
#
# Ergebnis liegt in assets/video/.
set -euo pipefail

EIN="${1:?Erstes Argument: die Bildschirmaufnahme}"
NAME="${2:?Zweites Argument: Ausgabename, z. B. instagram}"
ZIEL_LAENGE="${3:-30}"

MAX_CLIP="${MAX_CLIP:-4.5}"      # kein Reel laenger als das
MIN_CLIP="${MIN_CLIP:-1.8}"      # kuerzere Schnipsel fliegen raus
WISCH="${WISCH:-0.3}"            # Dauer des Hochwischers
SZENE="${SZENE:-0.30}"           # Empfindlichkeit der Szenenerkennung
TRIM_OBEN="${TRIM_OBEN:-0.055}"  # Anteil oben weg (Statusleiste)
TRIM_UNTEN="${TRIM_UNTEN:-0.045}" # Anteil unten weg (Navigationsleiste)
BREITE="${BREITE:-540}"          # Ausgabebreite, 9:16

command -v ffmpeg >/dev/null || { echo "ffmpeg fehlt. Auf dem Mac: brew install ffmpeg"; exit 1; }
[ -f "$EIN" ] || { echo "Datei nicht gefunden: $EIN"; exit 1; }

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

lies() { ffprobe -v error -select_streams v:0 -show_entries "$1" -of csv=p=0 "$2" | head -1; }
BQ=$(lies stream=width "$EIN"); HQ=$(lies stream=height "$EIN")
DAUER=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$EIN")
echo "Quelle: ${BQ}x${HQ}, ${DAUER}s"

# --- 1. Zuschnitt auf 9:16 ohne Leisten ---------------------------------
OBEN=$(python3 -c "print(int($HQ*$TRIM_OBEN)//2*2)")
UNTEN=$(python3 -c "print(int($HQ*$TRIM_UNTEN)//2*2)")
NUTZ_H=$((HQ - OBEN - UNTEN))
NUTZ_B=$(python3 -c "print(min($BQ, int($NUTZ_H*9/16))//2*2)")
NUTZ_H=$(python3 -c "print(min($NUTZ_H, int($NUTZ_B*16/9))//2*2)")
X=$(( (BQ - NUTZ_B) / 2 ))
HOEHE=$(python3 -c "print(int($BREITE*16/9)//2*2)")
echo "Zuschnitt: ${NUTZ_B}x${NUTZ_H} ab x=${X} y=${OBEN}  ->  ${BREITE}x${HOEHE}"

ffmpeg -loglevel error -y -i "$EIN" \
  -vf "crop=${NUTZ_B}:${NUTZ_H}:${X}:${OBEN},scale=${BREITE}:${HOEHE}:flags=lanczos,fps=30" \
  -an -c:v libx264 -crf 17 -preset veryfast "$TMP/roh.mp4"

# --- 2. Wischstellen finden ---------------------------------------------
ffmpeg -loglevel error -y -i "$TMP/roh.mp4" \
  -vf "select='gt(scene,${SZENE})',metadata=print:file=$TMP/szenen.txt" \
  -an -f null - 2>/dev/null || true
MARKEN=$(grep -o 'pts_time:[0-9.]*' "$TMP/szenen.txt" 2>/dev/null | cut -d: -f2 || true)

# --- 3. Abschnitte bilden ------------------------------------------------
mapfile -t STARTS < <(printf '0\n%s\n' "$MARKEN" | awk 'NF' | sort -g -u)
SEGS=(); SUMME=0; i=0
while [ $i -lt ${#STARTS[@]} ]; do
  A=${STARTS[$i]}
  NAECHST=${STARTS[$((i+1))]:-$DAUER}
  LAENGE=$(python3 -c "
a=float('$A'); n=float('$NAECHST'); m=float('$MAX_CLIP')
print(round(min(n-a, m), 3))")
  OK=$(python3 -c "print(1 if $LAENGE >= $MIN_CLIP else 0)")
  if [ "$OK" = "1" ]; then
    ffmpeg -loglevel error -y -ss "$A" -t "$LAENGE" -i "$TMP/roh.mp4" \
      -an -c:v libx264 -crf 17 -preset veryfast "$TMP/seg$((${#SEGS[@]})).mp4"
    SEGS+=("$TMP/seg$((${#SEGS[@]})).mp4")
    SUMME=$(python3 -c "print(round($SUMME + $LAENGE - $WISCH, 3))")
  fi
  ERREICHT=$(python3 -c "print(1 if $SUMME >= $ZIEL_LAENGE else 0)")
  [ "$ERREICHT" = "1" ] && break
  i=$((i+1))
done

[ ${#SEGS[@]} -ge 1 ] || { echo "Keine brauchbaren Abschnitte gefunden. SZENE kleiner setzen, z. B. SZENE=0.15"; exit 1; }
echo "Abschnitte: ${#SEGS[@]}, zusammen rund ${SUMME}s"

# --- 4. Mit Hochwischer verketten ---------------------------------------
if [ ${#SEGS[@]} -eq 1 ]; then
  cp "${SEGS[0]}" "$TMP/kette.mp4"
else
  EINGABEN=(); FILTER=""; VOR="[0:v]"; OFF=0
  for s in "${SEGS[@]}"; do EINGABEN+=(-i "$s"); done
  for ((k=1; k<${#SEGS[@]}; k++)); do
    LEN=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "${SEGS[$((k-1))]}")
    OFF=$(python3 -c "print(round($OFF + $LEN - $WISCH, 3))")
    AUS="[x$k]"; [ $k -eq $((${#SEGS[@]}-1)) ] && AUS="[v]"
    FILTER+="${VOR}[${k}:v]xfade=transition=slideup:duration=${WISCH}:offset=${OFF}${AUS};"
    VOR="[x$k]"
  done
  ffmpeg -loglevel error -y "${EINGABEN[@]}" \
    -filter_complex "${FILTER%;}" -map "[v]" \
    -an -c:v libx264 -crf 18 -preset veryfast "$TMP/kette.mp4"
fi

# --- 5. Ausgabe ----------------------------------------------------------
mkdir -p "$ROOT/assets/video"
ffmpeg -loglevel error -y -i "$TMP/kette.mp4" \
  -c:v libx264 -crf 28 -preset slow -pix_fmt yuv420p -movflags +faststart -an \
  "$ROOT/assets/video/reel-${NAME}.mp4"
ffmpeg -loglevel error -y -i "$TMP/kette.mp4" \
  -c:v libvpx-vp9 -crf 38 -b:v 0 -row-mt 1 -an \
  "$ROOT/assets/video/reel-${NAME}.webm"
ffmpeg -loglevel error -y -ss 0.4 -i "$TMP/kette.mp4" -frames:v 1 -q:v 4 \
  "$ROOT/assets/video/reel-${NAME}.jpg"

L=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$ROOT/assets/video/reel-${NAME}.mp4")
echo "Fertig: assets/video/reel-${NAME}.{mp4,webm,jpg}  (${L}s)"
ls -la "$ROOT/assets/video/reel-${NAME}".* | awk '{print "  ", $5, $9}'
