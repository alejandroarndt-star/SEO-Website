#!/usr/bin/env bash
# Baut das Hintergrundvideo im Kopf der Startseite aus mehreren Clips.
#
#   ./_build/hero-montage.sh ORDNER
#
# ORDNER enthaelt die Rohclips. Reihenfolge und Einstiegspunkt stehen unten in
# CLIPS, je Zeile "Datei Startsekunde". Die Clips werden auf 1280x720
# zugeschnitten und mit einer weichen Blende aneinandergehaengt.
#
# Quelle des aktuellen Materials: pexels.com, Pexels-Lizenz, kostenlos auch
# kommerziell, keine Namensnennung noetig, kein Wasserzeichen.
#
# bash 3.2 tauglich, siehe Hinweis in reels-loop.sh.
set -eo pipefail

ORDNER="${1:?Erstes Argument: Ordner mit den Rohclips}"
BREITE="${BREITE:-1280}"
HOEHE="${HOEHE:-720}"
FPS="${FPS:-24}"
LAENGE="${LAENGE:-3.2}"     # Spieldauer je Clip
BLENDE="${BLENDE:-0.7}"     # Dauer der Ueberblendung
CRF="${CRF:-31}"
CRF_WEBM="${CRF_WEBM:-40}"

CLIPS="
p38492077.mp4 1.0
p36579141.mp4 0.5
p35184197.mp4 20.0
p8089525.mp4 3.0
p19598792.mp4 0.5
p2890196.mp4 2.0
"

command -v ffmpeg >/dev/null || { echo "ffmpeg fehlt. Auf dem Mac: brew install ffmpeg"; exit 1; }
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

EIN=""; FILTER=""; N=0
while read -r datei start; do
  [ -n "$datei" ] || continue
  [ -f "$ORDNER/$datei" ] || { echo "fehlt: $ORDNER/$datei"; exit 1; }
  EIN="$EIN -ss $start -t $LAENGE -i $ORDNER/$datei"
  FILTER="${FILTER}[${N}:v]scale=${BREITE}:${HOEHE}:force_original_aspect_ratio=increase:flags=lanczos,crop=${BREITE}:${HOEHE},fps=${FPS},setsar=1,format=yuv420p[v${N}];"
  N=$((N+1))
done <<ENDE
$CLIPS
ENDE

[ $N -ge 2 ] || { echo "Mindestens zwei Clips noetig"; exit 1; }

VOR="[v0]"; OFF=0; k=1
while [ $k -lt $N ]; do
  OFF=$(python3 -c "print(round($OFF + $LAENGE - $BLENDE, 3))")
  if [ $k -eq $((N-1)) ]; then AUS="[out]"; else AUS="[x$k]"; fi
  FILTER="${FILTER}${VOR}[v${k}]xfade=transition=fade:duration=${BLENDE}:offset=${OFF}${AUS};"
  VOR="[x$k]"
  k=$((k+1))
done

echo "Clips: $N"
ffmpeg -loglevel error -y $EIN -filter_complex "${FILTER%;}" -map "[out]" \
  -an -c:v libx264 -crf 18 -preset veryfast "$TMP/kette.mp4"

mkdir -p "$ROOT/assets/video"
ffmpeg -loglevel error -y -i "$TMP/kette.mp4" \
  -c:v libx264 -crf ${CRF} -preset slow -pix_fmt yuv420p -movflags +faststart -an \
  "$ROOT/assets/video/hero.mp4"
ffmpeg -loglevel error -y -i "$TMP/kette.mp4" \
  -c:v libvpx-vp9 -crf ${CRF_WEBM} -b:v 0 -row-mt 1 -deadline good -cpu-used 2 -an \
  "$ROOT/assets/video/hero.webm"
ffmpeg -loglevel error -y -ss 1.0 -i "$TMP/kette.mp4" -frames:v 1 -q:v 4 \
  "$ROOT/assets/video/hero-poster.jpg"

L=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$ROOT/assets/video/hero.mp4")
echo "Fertig: assets/video/hero.{mp4,webm,jpg}  (${L}s)"
ls -la "$ROOT/assets/video/hero".* | awk '{printf "   %7.0f KB  %s\n", $5/1024, $NF}'
