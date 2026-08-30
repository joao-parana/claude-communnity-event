# CLAUDE.md — Claude Impact Lab Rio #2

Contexto operacional para o Claude Code neste repositório. Leia antes de qualquer tarefa.

---

## 1. O que é este projeto

Hackathon de **um dia** (30/08, 8h–20h, escritório da VTEX — R. Marquês de Olinda, 11, Botafogo),
segunda edição do **Claude Impact Lab Rio**, patrocinado pela Anthropic e realizado em parceria com a
**Prefeitura do Rio**, a **Secretaria Municipal de Educação (SME)** e a
**Secretaria Municipal de Desenvolvimento Econômico (SMDE)**.

O desafio é **um problema concreto da SME**. O briefing, os *datasets* e os critérios de avaliação
**só são revelados às 8h30 do dia do evento** — este repositório existe para que, no momento em que o
briefing sair, o time já tenha contexto de domínio, mapa de fontes de dados e ferramental pronto.

As melhores soluções são **doadas para a cidade**. Isso é um requisito de projeto, não um detalhe:
o entregável precisa ser transferível (licença aberta, sem dependência de contas pessoais, documentado
em português).

### Cronograma que dita o ritmo de engenharia

| Hora | Evento | Implicação técnica |
| --- | --- | --- |
| 08h00 | Check-in | — |
| 08h30 | Briefing (desafio + dados + critérios) | Só aqui o escopo real aparece |
| 09h00 | Início dos trabalhos | **7h30 líquidas de construção** |
| 16h30 | **Deadline de entrega** | Hard stop |
| 17h30 | Apresentação dos finalistas | Demo precisa rodar sem internet confiável |
| 18h30 | Premiação | — |

**Consequência:** priorize *demo funcionando* sobre arquitetura ideal. Prefira caminho feliz robusto
a cobertura de casos de borda. Deixe *seed data* mockado pronto para quando a API cair no dia.

### Papel do usuário (João Parana)

Arquiteto de Software, Analista de Requisitos e Programador **Python**. Time de 4 pessoas,
multidisciplinar (a organização montou os times por perfil). Assuma que o usuário faz backend/dados
e que colegas cobrem produto, design e apresentação.

### Recursos disponíveis no dia

- **USD$ 100 em créditos** na API da Anthropic por participante (conta em `platform.claude.com`,
  separada da assinatura do Claude).
- Mentores presentes o dia todo.
- Wi-Fi do evento (**assuma instabilidade** — cacheie tudo que baixar).

---

## 2. Domínio: a rede municipal de educação do Rio

Maior rede municipal de ensino fundamental da **América Latina**. Números para dimensionar qualquer
solução proposta (fontes e datas em `docs/mapa-sites-prefeitura.md`):

### Escala

| Indicador | Valor | Referência |
| --- | --- | --- |
| Alunos matriculados | **> 650.000** | Ano letivo 2025 e 2026 |
| Unidades escolares | **1.557** | SME, 2026 |
| Professores | **~42.900** | Rede municipal |
| CREs (Coordenadorias Regionais de Educação) | **11** | +1 código residual (12) no dado geo |
| Refeições servidas/ano | **150 milhões** | 2025 |
| Refeições servidas/dia | **~1 milhão** | média |
| Alunos atendidos/dia pela alimentação | **469.818** | — |
| Alimentos/dia | **~55 toneladas** (≈25 contêineres) | — |
| Investimento uniforme + material | **R$ 83 milhões** (4,5 mi de itens) | 2026 |
| Taxa de abandono no fundamental | **0,1%** — menor desde 2007 | 2025 |

### Composição da rede (1.590 equipamentos georreferenciados, `data.rio`, jun/2023)

Contagem **verificada por consulta à API** (ver `scripts/rio_crawler.py units`):

| Tipo | Qtd |
| --- | --- |
| Escola Municipal | 911 |
| EDI (Espaço de Desenvolvimento Infantil) | 286 |
| Creche Municipal | 247 |
| CIEP | 101 |
| Biblioteca Escolar Municipal | 13 |
| Escola Especial Municipal | 10 |
| Núcleo de Arte | 9 |
| Clube Escolar | 7 |
| CEJA (Educação de Jovens e Adultos) | 2 |
| CDEI, Escola Cívico-Militar, Centro Ref. EJA, Polo de Educação pelo Trabalho | 1 cada |
| **Total** | **1.590** |

Somando apenas unidades de ensino (Escola Municipal + EDI + Creche + CIEP + Especial + Cívico-Militar)
chega-se a **1.556**, batendo com as "1.557 escolas" da comunicação oficial. Use esse número como
âncora de sanidade ao validar qualquer *dataset* recebido no evento.

### Distribuição por CRE (unidades de ensino)

```
CRE  1:  96   CRE  5: 130   CRE  9: 165
CRE  2: 153   CRE  6: 111   CRE 10: 193
CRE  3: 136   CRE  7: 174   CRE 11:  43
CRE  4: 162   CRE  8: 193
```

CREs 7, 8, 9 e 10 (Zona Oeste / Norte) concentram ~46% da rede — **qualquer solução com componente
territorial precisa lidar com esse desbalanceamento**. Mais grave que a contagem é a **densidade**:
a 10ª CRE tem 316,7 km² e a 7ª tem 293,8 km² (juntas, 52% da área da cidade), contra 31,7 km² da 6ª.
A 4ª CRE tem 4,04 unidades/km²; a 7ª tem 0,59 — **sete vezes mais espalhada**. Custo de rota, entrega
e visita domiciliar não é comparável entre CREs. Tabela completa em `docs/mapa-sites-prefeitura.md` §3.5.

### Etapas e públicos atendidos

- **Educação Infantil**: 6 meses a 5 anos (creches e EDIs)
- **Ensino Fundamental**: 1º ao 9º ano (anos iniciais e finais)
- **EJA** — Educação de Jovens e Adultos
- **Educação Especial** — Instituto Municipal Helena Antipoff

---

## 3. Programas da SME que podem ser o desafio

Mapeados para reconhecer rapidamente o terreno quando o briefing sair:

| Programa | O que é | Ângulo de solução |
| --- | --- | --- |
| **Bora pra Escola / Busca Ativa** | Recondução de evadidos; 18 mil alunos em um ano; já existe um **"Preditor de Evasão Escolar"** interno que cruza variáveis de escola, turma, aluno e família | Cuidado: não reinvente o preditor — agregue interface, priorização de visitas, roteirização |
| **Alimentação escolar** | 4 cardápios rotativos (semanas A/B/C/D) por CRE; Rio foi o 1º município do Brasil a proibir ultraprocessados; regido pela Lei 11.947/2009 e Resolução CD/FNDE 06/2020 | Logística, previsão de demanda, desperdício, conformidade nutricional, alergias/restrições |
| **Matrícula Carioca** | Sistema de matrícula (`matricula.rio`) | Alocação de vagas, distância casa-escola, fila de creche |
| **GET** — Ginásio Experimental Tecnológico | Ensino com foco tecnológico | Currículo, trilhas |
| **EJA / ProJovem** | Fundamental + qualificação profissional, 18 a 29 anos | Ponte com empregabilidade (ver SMDE) |
| **Vacina na Escola** | Vacinação nas unidades | Cobertura, integração com saúde |
| **Trilhas Identitárias, Clubes Escolares, Núcleos de Arte** | Educação integral | Oferta vs. demanda territorial |
| **Escola de Férias** | Programação de recesso | Capacidade, inscrição |
| **Material RioEduca** | Plataforma de material didático | Conteúdo, IA generativa |

### Sinais fortes para o desafio

O briefing virá da SME, mas há apoio da SMDE. Temas com maior probabilidade, dada a materialidade dos
números e o discurso público da prefeitura: **alimentação escolar** (150 mi de refeições/ano, escala
brutal), **evasão/frequência**, **alocação de vagas em creche**, e **transição escola→trabalho**
(interseção SME × SMDE).

---

## 4. SMDE — Secretaria Municipal de Desenvolvimento Econômico

Parceira do evento. Relevante se o desafio tocar empregabilidade, formação técnica ou economia local.

- **Missão**: desenvolvimento sustentável, ambiente de negócios, segurança jurídica, inovação e
  atração de investimentos.
- **400 mil novos empregos formais** gerados desde 2021.
- **Programadores Cariocas** — *bootcamp* de ~6 meses para jovens em vulnerabilidade; prioriza
  egressos de escola pública, pessoas negras, mulheres, pessoas trans e refugiados; bolsa de R$ 500/mês
  + um computador ao concluir. Turma 2022: **750 formados** (70% negros, 40% mulheres, 45% de favelas).
  Motivação declarada: **24 mil vagas/ano não preenchidas** por falta de qualificação (2019–2024).
  → **Ponte natural com a rede da SME.**
- **Porto Maravalley** — hub de inovação.
- **Sandbox.rio** — ambiente regulatório experimental.
- **Observatório Econômico** (`observatorioeconomico.rio`) — boletins, notas técnicas, estudos;
  **IAE-Rio** (Indicador de Atividade Econômica) em Excel. Inflação 4,4% (12 meses até jun/2026);
  desemprego no menor patamar em mais de uma década.

---

## 5. Dados: onde buscar e como

Mapa completo em **[docs/mapa-sites-prefeitura.md](docs/mapa-sites-prefeitura.md)**.

### Fonte primária confirmada e funcional

`data.rio` expõe ArcGIS REST. Estes endpoints foram **testados e respondem**:

```
https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Educacao/SME/MapServer/0   # Limites das CREs
https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Educacao/SME/MapServer/1   # Escolas Municipais (1.590)
https://pgeo3.rio.rj.gov.br/arcgis/rest/services/Educacao/SME/MapServer/2   # Microáreas SME
https://pgeo3.rio.rj.gov.br/arcgis/rest/services/SME/SME_View/MapServer/2   # Creches Conveniadas
```

Campos da camada 1: `objectid`, `cre`, `designacao`, `denominacao`, `tipo`, `latitude`, `longitude`.
Geometria em **EPSG:31983** (SIRGAS 2000 / UTM 23S) — converta para WGS84 antes de plotar em Leaflet,
ou use os campos `latitude`/`longitude`, que já vêm em graus decimais.

Licença: **CC-BY 4.0**. Atribuição obrigatória: "Prefeitura da Cidade do Rio de Janeiro".

Busca de datasets:
```bash
curl -s --get "https://www.data.rio/api/search/v1/collections/dataset/items" \
  --data-urlencode "q=educação" --data-urlencode "limit=20"
```

### Regra de ouro sobre dados no dia do evento

**Os dados oficiais do desafio vêm no briefing.** Tudo que está aqui é *contexto de enriquecimento*.
Não construa o núcleo da solução sobre `data.rio` antes de ver o que a SME entregar — mas tenha o
*join* geográfico (unidade → CRE → bairro) pronto, porque quase todo dataset da SME é chaveado por
CRE e por código/denominação de unidade.

---

## 6. Ferramental deste repositório

```
.
├── CLAUDE.md                        # este arquivo
├── docs/
│   ├── luma-event-post.md           # post e comunicados originais do evento
│   └── mapa-sites-prefeitura.md     # mapa de sites, endpoints e datasets
└── scripts/
    ├── rio_crawler.py               # CLI de crawling/scraping (crawl4ai) + cliente ArcGIS
    ├── requirements.txt
    └── README.md
```

### CLI `rio_crawler.py`

```bash
python scripts/rio_crawler.py units --out data/unidades.csv       # baixa as 1.590 unidades da SME
python scripts/rio_crawler.py units --summary                     # contagens por tipo e CRE
python scripts/rio_crawler.py cres --out data/cres.geojson        # limites das CREs
python scripts/rio_crawler.py crawl sme --depth 2                 # crawl do site da SME
python scripts/rio_crawler.py crawl smde --depth 2                # crawl do site da SMDE
python scripts/rio_crawler.py sitemap sme --out docs/sitemap-sme.md
python scripts/rio_crawler.py pdfs sme --out data/pdfs/           # baixa PDFs encontrados
```

Detalhes de instalação e opções em `scripts/README.md`.

---

## 7. Convenções de trabalho

### Idioma
Tudo em **português do Brasil**, com acentuação correta — documentação, comentários, mensagens de
commit, textos de UI. Identificadores de código em inglês (padrão usual de Python).

### Stack padrão (proposta, ajuste no dia)
- **Python 3.11+**, `uv` ou `venv` para ambiente
- Dados: `polars` ou `pandas`, `duckdb` para *joins* rápidos sem infra
- API: `FastAPI` + `uvicorn`
- IA: SDK `anthropic`, modelo **`claude-opus-5`** para raciocínio e **`claude-haiku-4-5-20251001`**
  para tarefas de alto volume e baixa latência
- Front: o que o time de produto dominar — não imponha

### Regras de engenharia para hackathon
1. **Cacheie toda chamada de rede em disco.** Wi-Fi de evento cai; demo não pode depender de rede.
2. **Nada de credencial em código.** Chave da API em `.env`, `.env` no `.gitignore`.
3. **Não vaze dados pessoais de alunos.** Se o dataset do evento contiver dados nominais ou de
   menores, trate como sensível: não envie a serviços externos, não coloque em URL, anonimize antes
   de qualquer prompt para a API. Isto vale mesmo que o organizador diga que "pode".
4. **Um README que qualquer pessoa da prefeitura consiga seguir.** A solução vai ser doada.
5. **Commit cedo, commit sempre** — mas só quando o usuário pedir.

### Sobre o ambiente local do usuário

`sed` neste Mac é **GNU** (`gsed` por alias); todo o resto (`awk`, `date`, `stat`, `grep`, `find`,
`xargs`, `tar`) é **BSD**. Ver `~/dev/CLAUDE.md` para a tabela completa. Em scripts não interativos o
alias não vale — chame `gsed` explicitamente.

---

## 8. Perguntas a fazer no briefing

Checklist para o usuário levar às 8h30. Respostas mudam a arquitetura:

- Qual o **formato e volume** dos dados entregues? (CSV, Excel, banco, API?)
- Os dados contêm **informação pessoal identificável** de alunos? Qual o regime de tratamento?
- A solução precisa **integrar com sistema existente** da SME? (ver lista de sistemas em
  `docs/mapa-sites-prefeitura.md` — há ~23 sistemas legados)
- Quem é o **usuário final**: gestor da SME, diretor de escola, CRE, professor, família?
- Os critérios de avaliação pesam mais **impacto**, **viabilidade de adoção** ou **inovação técnica**?
- Há **restrição de infraestrutura** do lado da prefeitura (nuvem permitida, on-premise, custo)?
- Existe **solução atual** para o problema? Qual e por que não basta?
