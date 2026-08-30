# Claude Impact Lab Rio #2 — base de trabalho

Repositório de preparação e desenvolvimento para o **Claude Impact Lab Rio #2**, hackathon de um dia
promovido pela Anthropic em parceria com a **Prefeitura do Rio**, a **Secretaria Municipal de
Educação (SME)** e a **Secretaria Municipal de Desenvolvimento Econômico (SMDE)**.

> 📅 **30/08, 8h–20h** · Escritório da VTEX, R. Marquês de Olinda, 11, Botafogo
> ⏱️ Briefing às **8h30** · Entrega às **16h30** — **7h30 líquidas de construção**

**O desafio é o acesso à creche** para crianças de 0 a 3 anos e 11 meses: como planejar as vagas,
como organizar a inscrição e a classificação, e — o gargalo mais agudo — como convocar as famílias
sem perder vagas por contato desatualizado.

📄 **[`docs/desafio-inscricao-creche.md`](docs/desafio-inscricao-creche.md)** tem o briefing
organizado: os três eixos, os oito pontos de quebra, os dados fornecidos e os critérios de avaliação.

As melhores soluções são **doadas para a cidade** — o que torna documentação em português, licença
aberta e independência de contas pessoais requisitos de projeto, não capricho.

---

## Comece por aqui

| Se você é… | Leia |
| --- | --- |
| **qualquer pessoa do time** | [`docs/desafio-inscricao-creche.md`](docs/desafio-inscricao-creche.md) — o briefing inteiro |
| **produto / negócio / apresentação** | o mesmo documento, §4 (os três eixos), §5 (pontos de quebra) e §7 (critérios de avaliação) |
| **desenvolvedor** | [`CLAUDE.md`](CLAUDE.md) + [`scripts/README.md`](scripts/README.md) |
| **atrás de uma fonte de dado externa** | [`docs/mapa-sites-prefeitura.md`](docs/mapa-sites-prefeitura.md) |

---

## Estrutura

```
├── CLAUDE.md                         # contexto operacional (também lido pelo Claude Code)
├── docs/
│   ├── desafio-inscricao-creche.md   # ⭐ o briefing organizado — comece aqui
│   ├── trancricao-gab.md             # transcrição bruta do briefing
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

### O recorte do desafio — educação infantil, modalidade creche

| | |
| --- | --- |
| Alunos | **~89.000** |
| Unidades de creche | **~900** |
| Inscrições/ano (CPFs únicos) | **~45.000** |
| Registros na base (por opção) | **> 100.000** — cada CPF gera até 5 |
| Prazo para matricular após ser convocado | **3 dias** |

**O que mais chama atenção nos dados:** a desigualdade territorial da rede é de *densidade*, não de
contagem. A 7ª e a 10ª CRE somam 52% da área da cidade; a 4ª CRE tem 4,04 unidades/km² contra 0,59
da 7ª. Como a inscrição em creche **não tem nenhum critério territorial** — a família escolhe cinco
unidades em qualquer lugar da cidade — esse desbalanceamento entra direto no problema.

---

## O que a entrega precisa ter

Vale nota — está tudo detalhado em
[`docs/desafio-inscricao-creche.md`](docs/desafio-inscricao-creche.md) §7.

1. **Repositório GitHub público**, com o **último commit até as 16h30**. Commit das 16h31 não conta.
2. **Uma aplicação publicada ou um vídeo de até 5 minutos.** O GitHub não é a entrega — os jurados
   avaliam ~40 projetos em uma hora. Se não der para entender em minutos, não é avaliado.
3. **Pitch preparado**: 6 min + 6 min de Q&A, corte rígido. Os 5 finalistas só saem às 17h30, então
   todo time precisa estar pronto.
4. **Código que outra pessoa da secretaria consiga continuar.** O critério "engenharia" é julgado por
   banca técnica separada e mede exatamente isso.

O critério de maior peso é **impacto real**: *"dá para colocar amanhã na prefeitura e gerar valor?"*

---

## Regras de trabalho

- **Nada de credencial em código.** Chave da API em `.env` (já no `.gitignore`).
- **Os dados são de crianças de 0 a 3 anos.** Já vêm anonimizados pela SME, mas preservam a dinâmica
  real do processo. Não tente reidentificar, nunca coloque em URL, e mande agregados e amostras para
  a API — não a base inteira.
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
