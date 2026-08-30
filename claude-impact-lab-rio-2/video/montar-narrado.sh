#!/usr/bin/env bash
# Monta o vídeo narrado: a duração de cada cena vem do áudio (audio/plano.json),
# então a imagem acompanha a voz — nunca o contrário.
set -euo pipefail
cd "$(dirname "$0")"
FPS=30; W=1920; H=1200
ZOOM=(1.00 1.05 1.00 1.04 1.07 1.00 1.05 1.03 1.04)

rm -rf .p && mkdir -p .p
i=0
while IFS=$'\t' read -r cena fala total; do
  n=$(printf "%02d" $i); z=${ZOOM[$i]}
  frames=$(python3 -c "print(int($total*$FPS))")
  # vídeo da cena, com zoom lento
  ffmpeg -nostdin -y -loglevel error -loop 1 -i "frames/${cena}.png" \
    -vf "scale=${W}:${H}:flags=lanczos,zoompan=z='min(zoom+((${z}-1)/${frames}),${z})':d=${frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=${W}x${H}:fps=${FPS},format=yuv420p" \
    -t "$total" -c:v libx264 -preset medium -crf 18 -an ".p/v${n}.mp4"
  # áudio da cena: fala + silêncio até fechar a duração
  ffmpeg -nostdin -y -loglevel error -i "audio/${cena}.m4a" \
    -af "adelay=250|250,apad" -t "$total" -c:a aac -b:a 160k -ar 48000 -ac 2 ".p/a${n}.m4a"
  ffmpeg -nostdin -y -loglevel error -i ".p/v${n}.mp4" -i ".p/a${n}.m4a" \
    -c:v copy -c:a copy -shortest ".p/${n}.mp4"
  echo "  ${n}  ${cena}  ${total}s"
  i=$((i+1))
done < <(python3 -c "
import json
for p in json.load(open('audio/plano.json')):
    print(p['cena'], p['fala'], p['total'], sep='\t')")

: > .p/lista.txt
for f in .p/[0-9][0-9].mp4; do echo "file '$(basename "$f")'" >> .p/lista.txt; done
ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i .p/lista.txt -c copy .p/bruto.mp4

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 .p/bruto.mp4)
FADE=$(python3 -c "print(round($DUR-1.4,2))")
ffmpeg -nostdin -y -loglevel error -i .p/bruto.mp4 \
  -vf "fade=t=in:st=0:d=0.6,fade=t=out:st=${FADE}:d=1.2" \
  -af "afade=t=in:st=0:d=0.5,afade=t=out:st=${FADE}:d=1.2" \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 160k -movflags +faststart \
  fila-certa-demo-narrado.mp4
rm -rf .p
echo
ffprobe -v error -show_entries format=duration,size -of default=nw=1 fila-certa-demo-narrado.mp4
