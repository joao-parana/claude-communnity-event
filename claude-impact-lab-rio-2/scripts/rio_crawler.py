#!/usr/bin/env python3
"""CLI de coleta de dados públicos da Prefeitura do Rio (SME e SMDE).

Duas frentes independentes:

1. **ArcGIS REST** (`units`, `cres`) — dados estruturados e confiáveis do `data.rio`.
   Só depende de `httpx`. Use isto primeiro: é rápido e não precisa de navegador.

2. **Crawling** (`crawl`, `sitemap`, `pdfs`) — varre os portais da SME/SMDE com
   `crawl4ai` (Playwright), porque os sites são WordPress com conteúdo renderizado
   e paginação em JS. Requer instalação extra (ver README.md).

Toda resposta de rede é cacheada em disco (`.cache/`) — o Wi-Fi do evento é instável
e nenhuma demo pode depender de rede ao vivo.

Uso:
    python scripts/rio_crawler.py units --summary
    python scripts/rio_crawler.py units --out data/unidades.csv --format csv
    python scripts/rio_crawler.py cres --out data/cres.geojson
    python scripts/rio_crawler.py search "educação"
    python scripts/rio_crawler.py crawl sme --depth 2 --out data/crawl/sme
    python scripts/rio_crawler.py sitemap sme --out docs/sitemap-sme.md
    python scripts/rio_crawler.py pdfs sme --out data/pdfs
"""

from __future__ import annotations

import argparse
import asyncio
import collections
import csv
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urljoin, urlparse

try:
    import httpx
except ImportError:  # pragma: no cover
    sys.exit("Falta a dependência 'httpx'. Rode: pip install -r scripts/requirements.txt")

# --------------------------------------------------------------------------- #
# Configuração
# --------------------------------------------------------------------------- #

ARCGIS_SME = "https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Educacao/SME/MapServer"
ARCGIS_SME_VIEW = "https://pgeo3.rio.rj.gov.br/arcgis/rest/services/SME/SME_View/MapServer"
DATA_RIO_SEARCH = "https://www.data.rio/api/search/v1/collections/dataset/items"

LAYER_CRES = f"{ARCGIS_SME}/0"
LAYER_UNIDADES = f"{ARCGIS_SME}/1"
LAYER_MICROAREAS = f"{ARCGIS_SME}/2"
LAYER_CRECHES_CONVENIADAS = f"{ARCGIS_SME_VIEW}/2"

# Tipos que contam como unidade de ensino (exclui biblioteca, clube, núcleo de arte).
# A soma destes deve dar ~1.556, batendo com as "1.557 escolas" da comunicação oficial.
TIPOS_DE_ENSINO = {
    "Escola Municipal",
    "EDI",
    "Creche Municipal",
    "CIEP",
    "Escola Especial Municipal",
    "Escola Cívico Militar",
}

SITES = {
    "sme": {
        "url": "https://educacao.prefeitura.rio/",
        "nome": "Secretaria Municipal de Educação",
        "dominios": {"educacao.prefeitura.rio"},
    },
    "smde": {
        "url": "https://desenvolvimento.prefeitura.rio/",
        "nome": "Secretaria Municipal de Desenvolvimento Econômico",
        "dominios": {"desenvolvimento.prefeitura.rio", "smdeis.prefeitura.rio"},
    },
    "observatorio": {
        "url": "https://observatorioeconomico.rio/",
        "nome": "Observatório Econômico do Rio",
        "dominios": {"observatorioeconomico.rio"},
    },
}

CACHE_DIR = Path(".cache")
UA = "ClaudeImpactLabRio/1.0 (hackathon; contato via organizacao do evento)"

# --------------------------------------------------------------------------- #
# Cache em disco
# --------------------------------------------------------------------------- #


def _cache_path(key: str, suffix: str = ".json") -> Path:
    digest = hashlib.sha256(key.encode()).hexdigest()[:20]
    return CACHE_DIR / f"{digest}{suffix}"


def cached_get(url: str, params: dict[str, Any] | None = None, *, refresh: bool = False) -> str:
    """GET com cache em disco. Chave = URL + params serializados."""
    key = url + "?" + json.dumps(params or {}, sort_keys=True, ensure_ascii=False)
    path = _cache_path(key, ".txt")
    if path.exists() and not refresh:
        return path.read_text(encoding="utf-8")

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with httpx.Client(timeout=60.0, headers={"User-Agent": UA}, follow_redirects=True) as client:
        resp = client.get(url, params=params)
        resp.raise_for_status()
        body = resp.text
    path.write_text(body, encoding="utf-8")
    return body


# --------------------------------------------------------------------------- #
# ArcGIS REST
# --------------------------------------------------------------------------- #


def arcgis_query(
    layer: str,
    *,
    where: str = "1=1",
    out_fields: str = "*",
    geometry: bool = False,
    refresh: bool = False,
) -> dict[str, Any]:
    """Consulta uma camada ArcGIS. Pagina sozinho se o servidor truncar o resultado."""
    params = {
        "where": where,
        "outFields": out_fields,
        "returnGeometry": "true" if geometry else "false",
        "outSR": "4326" if geometry else "",
        "resultRecordCount": 2000,
        "f": "pjson",
    }
    payload = json.loads(cached_get(f"{layer}/query", params, refresh=refresh))
    if "error" in payload:
        raise RuntimeError(f"ArcGIS respondeu erro: {payload['error']}")

    features = payload.get("features", [])
    # O servidor sinaliza truncamento com exceededTransferLimit; pagina por offset.
    offset = len(features)
    while payload.get("exceededTransferLimit") and features:
        params_page = dict(params, resultOffset=offset)
        payload = json.loads(cached_get(f"{layer}/query", params_page, refresh=refresh))
        page = payload.get("features", [])
        if not page:
            break
        features.extend(page)
        offset += len(page)

    payload["features"] = features
    return payload


def arcgis_count(layer: str, *, refresh: bool = False) -> int:
    params = {"where": "1=1", "returnCountOnly": "true", "f": "pjson"}
    return int(json.loads(cached_get(f"{layer}/query", params, refresh=refresh))["count"])


def unidades(refresh: bool = False) -> list[dict[str, Any]]:
    """As 1.590 unidades/equipamentos da SME, com CRE, tipo e coordenadas."""
    payload = arcgis_query(
        LAYER_UNIDADES,
        out_fields="objectid,cre,designacao,denominacao,tipo,latitude,longitude",
        refresh=refresh,
    )
    linhas = []
    for feat in payload["features"]:
        attrs = dict(feat["attributes"])
        # cre vem como double (1.0, 2.0...); int é mais útil para join e ordenação.
        attrs["cre"] = int(attrs["cre"]) if attrs.get("cre") is not None else None
        attrs["eh_unidade_de_ensino"] = attrs.get("tipo") in TIPOS_DE_ENSINO
        linhas.append(attrs)
    return linhas


def resumo_unidades(linhas: list[dict[str, Any]]) -> str:
    por_tipo = collections.Counter(l["tipo"] for l in linhas)
    por_cre = collections.Counter(l["cre"] for l in linhas if l["cre"] is not None)
    ensino_por_cre = collections.Counter(
        l["cre"] for l in linhas if l["eh_unidade_de_ensino"] and l["cre"] is not None
    )

    out = [f"Total de equipamentos: {len(linhas)}", "", "-- Por tipo --"]
    out += [f"{qtd:5d}  {tipo}" for tipo, qtd in por_tipo.most_common()]
    out += ["", "-- Por CRE (todos os equipamentos) --"]
    out += [f"CRE {cre:2d}: {qtd:4d}" for cre, qtd in sorted(por_cre.items())]
    out += ["", "-- Por CRE (só unidades de ensino) --"]
    out += [f"CRE {cre:2d}: {qtd:4d}" for cre, qtd in sorted(ensino_por_cre.items())]
    out += ["", f"Unidades de ensino: {sum(ensino_por_cre.values())} (oficial SME: 1.557)"]
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# Busca no catálogo data.rio
# --------------------------------------------------------------------------- #


def buscar_datasets(termo: str, limite: int = 20, refresh: bool = False) -> list[dict[str, str]]:
    body = cached_get(DATA_RIO_SEARCH, {"q": termo, "limit": limite}, refresh=refresh)
    payload = json.loads(body)
    resultados = []
    for feat in payload.get("features", []):
        p = feat["properties"]
        resultados.append(
            {
                "titulo": p.get("title", ""),
                "tipo": p.get("type", ""),
                "url": p.get("url") or "",
                "resumo": (p.get("snippet") or "").strip(),
                "licenca": p.get("license") or "",
            }
        )
    return resultados


# --------------------------------------------------------------------------- #
# Crawling com crawl4ai
# --------------------------------------------------------------------------- #


@dataclass
class Pagina:
    url: str
    titulo: str
    markdown: str
    links_internos: list[str]
    pdfs: list[str]


def _importar_crawl4ai():
    try:
        from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
    except ImportError:
        sys.exit(
            "crawl4ai não instalado. Rode:\n"
            "    pip install -r scripts/requirements.txt\n"
            "    crawl4ai-setup\n"
            "Os comandos 'units', 'cres' e 'search' funcionam sem ele."
        )
    return AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig


def _normalizar(url: str) -> str:
    """Remove fragmento e barra final para deduplicar URLs equivalentes."""
    parsed = urlparse(url)
    caminho = parsed.path.rstrip("/") or "/"
    base = f"{parsed.scheme}://{parsed.netloc}{caminho}"
    return f"{base}?{parsed.query}" if parsed.query else base


async def crawl_site(
    site: str, profundidade: int, max_paginas: int, out_dir: Path | None
) -> list[Pagina]:
    AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig = _importar_crawl4ai()

    cfg = SITES[site]
    dominios = cfg["dominios"]
    raiz = cfg["url"]

    browser = BrowserConfig(headless=True, user_agent=UA, verbose=False)
    run = CrawlerRunConfig(cache_mode=CacheMode.ENABLED, page_timeout=45_000, word_count_threshold=20)

    vistos: set[str] = set()
    fila: list[tuple[str, int]] = [(_normalizar(raiz), 0)]
    paginas: list[Pagina] = []

    async with AsyncWebCrawler(config=browser) as crawler:
        while fila and len(paginas) < max_paginas:
            url, nivel = fila.pop(0)
            if url in vistos or nivel > profundidade:
                continue
            vistos.add(url)

            try:
                res = await crawler.arun(url=url, config=run)
            except Exception as exc:  # rede de evento cai; segue em frente
                print(f"  ! falhou {url}: {exc}", file=sys.stderr)
                continue
            if not res.success:
                print(f"  ! sem sucesso {url}: {res.error_message}", file=sys.stderr)
                continue

            markdown = str(res.markdown or "")
            todos_links = [l.get("href", "") for l in (res.links or {}).get("internal", [])]
            externos = [l.get("href", "") for l in (res.links or {}).get("external", [])]

            internos, pdfs = [], []
            for href in todos_links + externos:
                if not href:
                    continue
                absoluto = _normalizar(urljoin(url, href))
                if absoluto.lower().endswith(".pdf"):
                    pdfs.append(urljoin(url, href))
                elif urlparse(absoluto).netloc in dominios:
                    internos.append(absoluto)

            pagina = Pagina(
                url=url,
                titulo=(res.metadata or {}).get("title", "").strip(),
                markdown=markdown,
                links_internos=sorted(set(internos)),
                pdfs=sorted(set(pdfs)),
            )
            paginas.append(pagina)
            print(f"  [{len(paginas):3d}] n{nivel} {pagina.titulo[:60] or url}")

            if out_dir:
                out_dir.mkdir(parents=True, exist_ok=True)
                nome = re.sub(r"[^a-z0-9]+", "-", urlparse(url).path.strip("/").lower()) or "index"
                (out_dir / f"{nome[:100]}.md").write_text(
                    f"<!-- {url} -->\n# {pagina.titulo}\n\n{markdown}", encoding="utf-8"
                )

            for link in pagina.links_internos:
                if link not in vistos:
                    fila.append((link, nivel + 1))

    return paginas


def gerar_sitemap(site: str, paginas: list[Pagina]) -> str:
    cfg = SITES[site]
    linhas = [
        f"# Sitemap — {cfg['nome']}",
        "",
        f"Raiz: {cfg['url']}",
        f"Páginas mapeadas: {len(paginas)}",
        "",
        "| Título | URL |",
        "| --- | --- |",
    ]
    for p in sorted(paginas, key=lambda x: x.url):
        titulo = (p.titulo or "(sem título)").replace("|", "\\|")
        linhas.append(f"| {titulo} | {p.url} |")

    pdfs = sorted({pdf for p in paginas for pdf in p.pdfs})
    if pdfs:
        linhas += ["", f"## PDFs encontrados ({len(pdfs)})", ""]
        linhas += [f"- {pdf}" for pdf in pdfs]
    return "\n".join(linhas) + "\n"


def baixar_pdfs(urls: Iterable[str], destino: Path) -> None:
    destino.mkdir(parents=True, exist_ok=True)
    with httpx.Client(timeout=120.0, headers={"User-Agent": UA}, follow_redirects=True) as client:
        for url in urls:
            nome = Path(urlparse(url).path).name or "documento.pdf"
            alvo = destino / nome
            if alvo.exists():
                print(f"  = já existe {nome}")
                continue
            try:
                resp = client.get(url)
                resp.raise_for_status()
            except Exception as exc:
                print(f"  ! falhou {url}: {exc}", file=sys.stderr)
                continue
            alvo.write_bytes(resp.content)
            print(f"  + {nome} ({len(resp.content) // 1024} KB)")


# --------------------------------------------------------------------------- #
# Saída
# --------------------------------------------------------------------------- #


def escrever(linhas: list[dict[str, Any]], destino: Path | None, formato: str) -> None:
    if destino is None:
        json.dump(linhas, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return

    destino.parent.mkdir(parents=True, exist_ok=True)
    if formato == "csv":
        with destino.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(linhas[0].keys()))
            writer.writeheader()
            writer.writerows(linhas)
    else:
        destino.write_text(json.dumps(linhas, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Gravado: {destino} ({len(linhas)} registros)")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="rio_crawler",
        description="Coleta dados públicos da SME e da SMDE (Prefeitura do Rio).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--refresh", action="store_true", help="ignora o cache em disco")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_units = sub.add_parser("units", help="unidades/equipamentos da SME (ArcGIS)")
    p_units.add_argument("--out", type=Path)
    p_units.add_argument("--format", choices=["json", "csv"], default="csv")
    p_units.add_argument("--summary", action="store_true", help="só imprime contagens")
    p_units.add_argument("--ensino", action="store_true", help="filtra só unidades de ensino")

    p_cres = sub.add_parser("cres", help="limites geográficos das CREs (GeoJSON)")
    p_cres.add_argument("--out", type=Path)

    p_search = sub.add_parser("search", help="busca datasets no catálogo data.rio")
    p_search.add_argument("termo")
    p_search.add_argument("--limit", type=int, default=20)

    p_crawl = sub.add_parser("crawl", help="varre um portal com crawl4ai")
    p_crawl.add_argument("site", choices=sorted(SITES))
    p_crawl.add_argument("--depth", type=int, default=1)
    p_crawl.add_argument("--max-pages", type=int, default=80)
    p_crawl.add_argument("--out", type=Path, help="diretório para os markdowns")

    p_map = sub.add_parser("sitemap", help="crawl + gera sitemap em markdown")
    p_map.add_argument("site", choices=sorted(SITES))
    p_map.add_argument("--depth", type=int, default=2)
    p_map.add_argument("--max-pages", type=int, default=200)
    p_map.add_argument("--out", type=Path, required=True)

    p_pdf = sub.add_parser("pdfs", help="crawl + baixa todos os PDFs encontrados")
    p_pdf.add_argument("site", choices=sorted(SITES))
    p_pdf.add_argument("--depth", type=int, default=2)
    p_pdf.add_argument("--max-pages", type=int, default=200)
    p_pdf.add_argument("--out", type=Path, default=Path("data/pdfs"))

    args = parser.parse_args()

    if args.cmd == "units":
        linhas = unidades(refresh=args.refresh)
        if args.ensino:
            linhas = [l for l in linhas if l["eh_unidade_de_ensino"]]
        if args.summary:
            print(resumo_unidades(linhas))
            return
        escrever(linhas, args.out, args.format)

    elif args.cmd == "cres":
        payload = arcgis_query(LAYER_CRES, geometry=True, refresh=args.refresh)
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": f["attributes"],
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": f.get("geometry", {}).get("rings", []),
                    },
                }
                for f in payload["features"]
            ],
        }
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(json.dumps(geojson, ensure_ascii=False), encoding="utf-8")
            print(f"Gravado: {args.out} ({len(geojson['features'])} CREs)")
        else:
            json.dump(geojson, sys.stdout, ensure_ascii=False, indent=2)

    elif args.cmd == "search":
        for r in buscar_datasets(args.termo, args.limit, refresh=args.refresh):
            print(f"- {r['titulo']}  [{r['tipo']}]")
            if r["url"]:
                print(f"    {r['url']}")
            if r["resumo"]:
                print(f"    {r['resumo'][:160]}")

    elif args.cmd == "crawl":
        paginas = asyncio.run(crawl_site(args.site, args.depth, args.max_pages, args.out))
        print(f"\n{len(paginas)} páginas coletadas.")

    elif args.cmd == "sitemap":
        paginas = asyncio.run(crawl_site(args.site, args.depth, args.max_pages, None))
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(gerar_sitemap(args.site, paginas), encoding="utf-8")
        print(f"\nGravado: {args.out} ({len(paginas)} páginas)")

    elif args.cmd == "pdfs":
        paginas = asyncio.run(crawl_site(args.site, args.depth, args.max_pages, None))
        pdfs = sorted({pdf for p in paginas for pdf in p.pdfs})
        print(f"\n{len(pdfs)} PDFs encontrados. Baixando para {args.out}/")
        baixar_pdfs(pdfs, args.out)


if __name__ == "__main__":
    main()
