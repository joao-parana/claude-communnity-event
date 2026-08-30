# -*- coding: utf-8 -*-
"""Sintetiza a narração com a voz do macOS e mede a duração real de cada cena.

O vídeo é remontado a partir dessas durações — assim a imagem acompanha a voz,
e não o contrário.
"""
import subprocess, json, sys
from pathlib import Path

VOZ = sys.argv[1] if len(sys.argv) > 1 else "Reed"
VEL = "178"           # palavras por minuto
D = Path(__file__).parent / "audio"
D.mkdir(exist_ok=True)

CENAS = [
    ("01_cidade",
     "Painel de gestão da Inscrição Creche do Rio. Quinze mil e trezentas crianças esperam vaga "
     "a menos de três quilômetros de uma creche com vaga aberta."),
    ("02_cidade_bonsucesso",
     "Duas mil seiscentas e vinte cabem hoje em vagas já contratadas e ociosas. Sem obra, sem "
     "verba nova. A barra clara é a fila; a escura, quantas caberiam ao redor. Em Jacarepaguá, "
     "sete por cento: ali falta creche. Em Bonsucesso, sessenta e um."),
    ("03_cre4",
     "Um clique leva à quarta coordenadoria. A página não recarrega, mas cada tela continua sendo "
     "um endereço compartilhável."),
    ("04_cre4_tiomario",
     "Círculos vermelhos são unidades com fila, e o número é quantas crianças esperam. Verdes são "
     "creches parceiras com vaga ociosa. As posições são reais. Mais da metade desta fila caberia "
     "no que já existe."),
    ("05_cre4_vaga",
     "A Creche Tio Mário, em Bonsucesso, tem duzentas e quatorze na fila. E cento e vinte vagas em "
     "seis creches vizinhas. A mais próxima está a mil e duzentos metros: Lar Irmão Francisco."),
    ("06_realocar",
     "À esquerda, a fila na ordem publicada em Diário Oficial. Não é reordenável, porque é "
     "auditada. A primeira criança precisa de Maternal um; a creche de destino tem cinco vagas de "
     "Maternal um."),
    ("07_realocar_aviso",
     "E uma mudança de política: recusar esta vaga não retira a criança das outras filas. Hoje, "
     "aceitar encerra a inscrição inteira. Depende de validação jurídica da secretaria."),
    ("08_convocada",
     "A convocação sai por quatro canais em cascata: aplicativo, WhatsApp, mensagem de texto e "
     "ligação da unidade. É o protocolo oficial, automatizado e registrado."),
    ("09_trilha",
     "E este é o ponto: cada tentativa tem canal, horário e resultado. Isso não existe hoje. Sem "
     "esse registro, não se distingue quem recusou de quem nunca foi encontrado. E são problemas "
     "opostos."),
]

MARGEM = 0.9   # respiro depois de cada fala, em segundos
plano = []
for nome, texto in CENAS:
    aiff = D / f"{nome}.aiff"
    m4a = D / f"{nome}.m4a"
    subprocess.run(["say", "-v", VOZ, "-r", VEL, "-o", str(aiff), texto], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(aiff),
                    "-c:a", "aac", "-b:a", "160k", str(m4a)], check=True)
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(m4a)],
        capture_output=True, text=True).stdout.strip())
    aiff.unlink()
    plano.append({"cena": nome, "fala": round(dur, 2), "total": round(dur + MARGEM, 2)})
    print(f"  {nome:24} fala {dur:5.1f}s  cena {dur + MARGEM:5.1f}s")

(D / "plano.json").write_text(json.dumps(plano, ensure_ascii=False, indent=1))
t = sum(p["total"] for p in plano)
print(f"\nvoz: {VOZ} · {VEL} ppm")
print(f"duração total: {int(t // 60)}min{int(t % 60):02d}s")
