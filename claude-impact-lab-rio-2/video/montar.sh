#!/usr/bin/env bash
# Monta o vídeo de 2 min a partir dos quadros, com os tempos do roteiro.
# Cada quadro ganha um zoom lento (Ken Burns) para a imagem não ficar parada.
set -euo pipefail
cd "$(dirname "$0")"
FPS=30; W=1920; H=1200

# quadro : segundos : zoom final
CENAS=(
  "01_cidade:11:1.00"
  "02_cidade_bonsucesso:13:1.06"
  "03_cre4:9:1.00"
  "04_cre4_tiomario:16:1.04"
  "05_cre4_vaga:11:1.08"
  "06_realocar:15:1.00"
  "07_realocar_aviso:13:1.06"
  "08_convocada:16:1.03"
  "09_trilha:16:1.05"
)

rm -rf .partes && mkdir -p .partes
i=0
for cena in "${CENAS[@]}"; do
  IFS=: read -r nome seg zoom <<< "$cena"
  n=$(printf "%02d" $i)
  frames=$(( seg * FPS ))
  ffmpeg -y -loglevel error -loop 1 -i "frames/${nome}.png" \
    -vf "scale=${W}:${H}:flags=lanczos,zoompan=z='min(zoom+((${zoom}-1)/${frames}),${zoom})':d=${frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=${W}x${H}:fps=${FPS},format=yuv420p" \
    -t "${seg}" -c:v libx264 -preset medium -crf 18 ".partes/${n}.mp4"
  echo "  ${n}  ${nome}  ${seg}s"
  i=$((i+1))
done

# concatena com fade de 0,4 s entre as cenas
: > .partes/lista.txt
for f in .partes/[0-9][0-9].mp4; do echo "file '$(basename "$f")'" >> .partes/lista.txt; done
ffmpeg -y -loglevel error -f concat -safe 0 -i .partes/lista.txt -c copy .partes/bruto.mp4
ffmpeg -y -loglevel error -i .partes/bruto.mp4 \
  -vf "fade=t=in:st=0:d=0.6,fade=t=out:st=$(python3 -c "print(sum(int(c.split(':')[1]) for c in '${CENAS[*]}'.split()) - 1.4)"):d=1.2" \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -movflags +faststart \
  fila-certa-demo.mp4
rm -rf .partes
echo
ffprobe -v error -show_entries format=duration,size -of default=nw=1 fila-certa-demo.mp4
