# `rio_crawler.py`

CLI para coletar dados públicos da **SME** e da **SMDE** da Prefeitura do Rio.

## Instalação

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
```

Os comandos `units`, `cres` e `search` só precisam de `httpx` — funcionam já.

Para os comandos de crawling (`crawl`, `sitemap`, `pdfs`), instale também o navegador do Playwright:

```bash
crawl4ai-setup
```

### Onde o `crawl4ai-setup` instala as coisas

Ele espalha os componentes por **três lugares distintos** — dois deles fora do projeto:

| O quê | Onde | Tamanho |
| --- | --- | --- |
| Pacote Python e executáveis (`crawl4ai-setup`, `crawl4ai-doctor`, `crwl`, `playwright`) | `.venv/lib/pythonX.Y/site-packages/crawl4ai/` e `.venv/bin/` | ~4 MB |
| Navegadores do Playwright (Chromium + *headless shell* + ffmpeg) | `~/Library/Caches/ms-playwright/` | **~555 MB** |
| Estado do crawl4ai: cache, banco SQLite, markdown e screenshots | `~/.crawl4ai/` | cresce com o uso |

**Se você não encontrou os binários,** provavelmente o venv não estava ativado — eles vivem em
`.venv/bin`, não no sistema. Sem `source .venv/bin/activate`, `which crawl4ai-setup` não retorna
nada e `import crawl4ai` falha.

Para conferir se está tudo de pé:

```bash
source .venv/bin/activate && crawl4ai-doctor
```

Dois detalhes que economizam dor de cabeça:

- Os navegadores ficam num cache **global do usuário**, fora do `.venv`. Se apagar o venv, eles
  ficam órfãos ocupando ~555 MB — rode `playwright uninstall --all` antes.
- `~/.crawl4ai/` acumula resultados a cada crawl. Se algum resultado vier estranho, limpar esse
  diretório é a primeira coisa a tentar.

## Comandos

### Dados estruturados (ArcGIS REST — rápido, sem navegador)

```bash
python scripts/rio_crawler.py units --summary
```
Contagens das 1.590 unidades da SME por tipo e por CRE. Boa checagem de sanidade:
a soma das unidades de ensino deve dar ~1.556, batendo com as "1.557 escolas" oficiais.

```bash
python scripts/rio_crawler.py units --out data/unidades.csv
python scripts/rio_crawler.py units --ensino --out data/escolas.csv
python scripts/rio_crawler.py units --out data/unidades.json --format json
```

```bash
python scripts/rio_crawler.py cres --out data/cres.geojson
```
Limites geográficos das 11 CREs em GeoJSON (WGS84), prontos para Leaflet/Folium.

```bash
python scripts/rio_crawler.py search "educação"
python scripts/rio_crawler.py search "desenvolvimento social"
```
Busca no catálogo do `data.rio` e imprime título, tipo e endpoint de cada dataset.

### Crawling dos portais

```bash
python scripts/rio_crawler.py crawl sme --depth 2 --out data/crawl/sme
python scripts/rio_crawler.py crawl smde --depth 2 --out data/crawl/smde
python scripts/rio_crawler.py crawl observatorio --depth 1 --out data/crawl/obs
```
Salva cada página como Markdown limpo — formato ideal para alimentar prompts.

```bash
python scripts/rio_crawler.py sitemap sme --depth 2 --out docs/sitemap-sme.md
```
Regenera o mapa do site. Use quando um link de `docs/mapa-sites-prefeitura.md` der 404.

```bash
python scripts/rio_crawler.py pdfs sme --depth 2 --out data/pdfs
```
Baixa todos os PDFs alcançáveis — inclui Relatórios Anuais de Gestão, Plano Municipal de
Educação, cardápios e guias alimentares. É onde estão os números densos da rede.

## Cache

Toda resposta HTTP vai para `.cache/`. Passe `--refresh` para forçar nova busca.
O cache existe porque o Wi-Fi do evento é instável e a demo não pode depender de rede ao vivo.

## Boas maneiras

Os sites são públicos e os dados são **CC-BY 4.0** ("Prefeitura da Cidade do Rio de Janeiro").
Mantenha `--max-pages` em valores razoáveis, não paralelize agressivamente e prefira o cache.
