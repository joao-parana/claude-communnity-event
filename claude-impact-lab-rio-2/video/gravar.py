"""Captura os quadros do roteiro em 2x e monta o vídeo com ffmpeg.

Não é screencast: é uma sequência determinística de estados reais da aplicação,
navegados de verdade (cliques, submit), capturados em alta resolução.
"""
import asyncio, sys
from pathlib import Path
from playwright.async_api import async_playwright

BASE = "http://127.0.0.1:8000"
OUT = Path(__file__).parent / "frames"
W, H = 1440, 900


async def main():
    OUT.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)

        async def shot(nome, espera=0.9):
            await asyncio.sleep(espera)
            await pg.screenshot(path=str(OUT / f"{nome}.png"))
            print("  ·", nome)

        print("cena 1 — cidade")
        await pg.goto(f"{BASE}/", wait_until="networkidle")
        await shot("01_cidade")
        await pg.hover("text=Bonsucesso >> nth=0")
        await shot("02_cidade_bonsucesso", 0.5)

        print("cena 2 — território")
        await pg.goto(f"{BASE}/cre/4", wait_until="networkidle")
        await shot("03_cre4")
        await pg.goto(f"{BASE}/cre/4?foco=430603", wait_until="networkidle")
        await shot("04_cre4_tiomario")
        # destaque na primeira vaga da lista
        await pg.hover("a[href='/realocar/430603/4016']")
        await shot("05_cre4_vaga", 0.5)

        print("cena 3 — decisão")
        await pg.goto(f"{BASE}/realocar/430603/4016", wait_until="networkidle")
        await shot("06_realocar")
        await pg.hover("text=A oferta é adicional, não substitui")
        await shot("07_realocar_aviso", 0.5)

        print("cena 4 — registro")
        await pg.click("button[type=submit]")
        await pg.wait_for_selector("text=registrada", timeout=8000)
        await shot("08_convocada", 1.2)
        await pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await shot("09_trilha", 0.8)

        await b.close()
    print(f"\n{len(list(OUT.glob('*.png')))} quadros em {OUT}")


asyncio.run(main())
