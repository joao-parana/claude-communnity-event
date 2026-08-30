# Claude Impact Lab Rio #2 — base de trabalho

Repositório de preparação e desenvolvimento para o **Claude Impact Lab Rio #2**, hackathon de um dia
promovido pela Anthropic em parceria com a **Prefeitura do Rio**, a **Secretaria Municipal de
Educação (SME)** e a **Secretaria Municipal de Desenvolvimento Econômico (SMDE)**.

> 📅 **30/08, 8h–20h** · Escritório da VTEX, R. Marquês de Olinda, 11, Botafogo
> ⏱️ Briefing às **8h30** · Entrega às **16h30** — **7h30 líquidas de construção**

O desafio é um problema real da SME e **só é revelado no briefing**. Este repositório existe para que,
no momento em que isso acontecer, o time não gaste nenhum minuto pesquisando contexto: os números da
rede, o mapa das fontes de dados e o ferramental de coleta já estão prontos.

As melhores soluções são **doadas para a cidade** — o que torna documentação em português, licença
aberta e independência de contas pessoais requisitos de projeto, não capricho.

---

## Comece por aqui

| Se você é… | Leia |
| --- | --- |
| **qualquer pessoa do time** | esta página, depois a seção *Números* abaixo |
| **produto / negócio / apresentação** | [`CLAUDE.md`](CLAUDE.md) §3 (programas da SME) e §8 (perguntas para o briefing) |
| **desenvolvedor** | [`CLAUDE.md`](CLAUDE.md) inteiro + [`scripts/README.md`](scripts/README.md) |
| **atrás de uma fonte de dado específica** | [`docs/mapa-sites-prefeitura.md`](docs/mapa-sites-prefeitura.md) |

---

## Estrutura

```
├── CLAUDE.md                         # contexto operacional (também lido pelo Claude Code)
├── docs/
│   ├── luma-event-post.md            # post e comunicados originais do evento
│   └── mapa-sites-prefeitura.md      # sites, endpoints, datasets e números consolidados
└── scripts/
    ├── rio_crawler.py                # CLI de coleta: ArcGIS REST + crawling (crawl4ai)
    ├── requirements.txt
    └── README.md
```

`data/` e `.cache/` são criados na primeira execução e ficam fora do versionamento.

---

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
```

Isso já habilita os comandos de dados estruturados, que não precisam de navegador:

```bash
python scripts/rio_crawler.py units --summary
```

Saída esperada — contagem das 1.590 unidades da SME por tipo e por CRE, terminando em
`Unidades de ensino: 1556 (oficial SME: 1.557)`. Se esse número bater, sua conexão com o `data.rio`
está boa.

Exportando os dados:

```bash
python scripts/rio_crawler.py units --ensino --out data/escolas.csv   # 1.556 escolas com lat/lon
python scripts/rio_crawler.py cres --out data/cres.geojson            # limites das 11 CREs
python scripts/rio_crawler.py search "educação"                       # catálogo data.rio
```

Para varrer os portais da SME/SMDE (requer o navegador do Playwright):

```bash
crawl4ai-setup
python scripts/rio_crawler.py crawl sme --depth 2 --out data/crawl/sme
python scripts/rio_crawler.py pdfs sme --out data/pdfs    # relatórios de gestão, cardápios, PME
```

O `crawl4ai-setup` instala em três lugares — o pacote no `.venv`, os navegadores do Playwright em
`~/Library/Caches/ms-playwright/` (~555 MB) e o cache em `~/.crawl4ai/`. Se os comandos parecerem
ausentes, é o venv que não está ativado: os binários ficam em `.venv/bin`, não no sistema.

Detalhes de cada comando, e do que vai onde, em [`scripts/README.md`](scripts/README.md).

---

## Números da rede

Maior rede municipal de ensino fundamental da América Latina.

| | |
| --- | --- |
| Alunos | **> 650.000** |
| Escolas | **1.557** |
| Professores | **~42.900** |
| CREs | **11** |
| Refeições/dia | **~1 milhão** (150 milhões em 2025) |
| Alimentos/dia | **~55 toneladas** |
| Abandono no fundamental | **0,1%** — menor desde 2007 |

Composição: 911 Escolas Municipais, 286 EDIs, 247 Creches, 101 CIEPs, mais bibliotecas, clubes
escolares e núcleos de arte. Fontes e detalhamento em
[`docs/mapa-sites-prefeitura.md`](docs/mapa-sites-prefeitura.md) §4.

**O que mais chama atenção nos dados:** a desigualdade territorial da rede é de *densidade*, não de
contagem. A 7ª e a 10ª CRE somam 52% da área da cidade; a 4ª CRE tem 4,04 unidades/km² contra 0,59
da 7ª. Custo de rota, entrega e visita domiciliar não é comparável entre CREs — isso afeta qualquer
solução com componente logístico ou territorial.

---

## Quando o briefing sair

1. **Rode o checklist de perguntas** de [`CLAUDE.md`](CLAUDE.md) §8 durante a apresentação —
   as respostas mudam a arquitetura (formato dos dados, dados pessoais, usuário final, integração
   com sistemas existentes, critérios de avaliação).
2. **Valide o dataset recebido** contra as âncoras conhecidas: 1.557 unidades, 11 CREs, ~650 mil
   alunos. Divergência grande é sinal de recorte diferente — pergunte antes de modelar.
3. **Verifique se já existe solução.** A SME roda um *Preditor de Evasão Escolar* em produção e o
   programa *Bora pra Escola*; a alimentação escolar tem cardápio rotativo A/B/C/D e tabelas anuais
   de preços publicadas. Somar a algo existente rende mais que reconstruir.
4. **Só então escolha a stack.** A proposta em [`CLAUDE.md`](CLAUDE.md) §7 é ponto de partida,
   não compromisso.

---

## Regras de trabalho

- **Nada de credencial em código.** Chave da API em `.env` (já no `.gitignore`).
- **Não vaze dados de alunos.** Se o dataset do evento tiver informação nominal ou de menores,
  trate como sensível: anonimize antes de qualquer chamada à API, nunca em URL. Isso vale mesmo que
  seja dito que "pode".
- **Cacheie tudo que vier da rede.** O Wi-Fi do evento é instável e a demo das 17h30 não pode
  depender de rede ao vivo.
- **Documentação em português**, com acentuação correta. A solução vai ser lida por servidores da
  prefeitura.
- **Priorize demo funcionando** sobre arquitetura ideal. São 7h30.

---

## Dados e licenças

Os dados coletados por `rio_crawler.py` vêm do [`data.rio`](https://www.data.rio), portal da
Prefeitura do Rio gerido pelo Instituto Pereira Passos (IPP), sob licença **CC-BY 4.0**.
Atribuição obrigatória: *Prefeitura da Cidade do Rio de Janeiro*.

A camada geográfica de escolas tem última atualização em **junho/2023** — a rede mudou desde então.
Use-a para contexto e geolocalização, não como fonte de verdade sobre a rede atual.
