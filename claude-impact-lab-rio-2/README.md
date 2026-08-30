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

| Se você é…                             | Leia                                                                                        |
| -------------------------------------- | ------------------------------------------------------------------------------------------- |
| **qualquer pessoa do time**            | [`docs/desafio-inscricao-creche.md`](docs/desafio-inscricao-creche.md) — o briefing inteiro |
| **construindo o app**                  | [`docs/spec-app-fila-certa.md`](docs/spec-app-fila-certa.md) + o mockup                     |
| **produto / negócio / apresentação**   | o mesmo documento, §4 (os três eixos), §5 (pontos de quebra) e §7 (critérios de avaliação)  |
| **desenvolvedor**                      | [`CLAUDE.md`](CLAUDE.md) + [`scripts/README.md`](scripts/README.md)                         |
| **atrás de uma fonte de dado externa** | [`docs/mapa-sites-prefeitura.md`](docs/mapa-sites-prefeitura.md)                            |

---

## Estrutura

```
├── CLAUDE.md                         # contexto operacional (também lido pelo Claude Code)
├── app/                              # ⭐ Fila Certa (ver app/README.md)
│   ├── backend/                      #   FastAPI: painel de gestão (pronto) + API JSON
│   └── frontend/                     #   PWA do responsável (a fazer)
├── dadoscreche/                      # git clone https://github.com/CIT-SME-RJ/dadoscreche (não versionado)
├── docs/
│   ├── desafio-inscricao-creche.md   # ⭐ o briefing organizado — comece aqui
│   ├── spec-app-fila-certa.md        # especificação do app
│   ├── mockup_fila_certa_v1.html     # mockup das 6 telas
│   ├── Briefing_SME.docx.md          # briefing oficial da SME
│   ├── handoff_hackathon_sme.md      # handoff do outro dev (sessão de planejamento)
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

|                         |                                     |
| ----------------------- | ----------------------------------- |
| Alunos                  | **> 650.000**                       |
| Escolas                 | **1.557**                           |
| Professores             | **~42.900**                         |
| CREs                    | **11**                              |
| Refeições/dia           | **~1 milhão** (150 milhões em 2025) |
| Alimentos/dia           | **~55 toneladas**                   |
| Abandono no fundamental | **0,1%** — menor desde 2007         |

Composição: 911 Escolas Municipais, 286 EDIs, 247 Creches, 101 CIEPs, mais bibliotecas, clubes
escolares e núcleos de arte. Fontes e detalhamento em
[`docs/mapa-sites-prefeitura.md`](docs/mapa-sites-prefeitura.md) §4.

### O recorte do desafio — educação infantil, modalidade creche

|                                          |                                     |
| ---------------------------------------- | ----------------------------------- |
| Alunos                                   | **~89.000**                         |
| Unidades de creche                       | **~900**                            |
| Inscrições/ano (CPFs únicos)             | **~45.000**                         |
| Registros na base (por opção)            | **> 100.000** — cada CPF gera até 5 |
| Prazo para matricular após ser convocado | **3 dias**                          |

**O que mais chama atenção nos dados:** a desigualdade territorial da rede é de _densidade_, não de
contagem. A 7ª e a 10ª CRE somam 52% da área da cidade; a 4ª CRE tem 4,04 unidades/km² contra 0,59
da 7ª. Como a inscrição em creche **não tem nenhum critério territorial** — a família escolhe cinco
unidades em qualquer lugar da cidade — esse desbalanceamento entra direto no problema.

---

## Os dados: o que a análise exploratória mostrou

**Repositório oficial:** https://github.com/CIT-SME-RJ/dadoscreche/

```bash
git clone https://github.com/CIT-SME-RJ/dadoscreche.git
```

Cinco processos seletivos (2021–2025), **837 mil** opções de inscrição e **4,36 milhões** de
respostas de questionário. O `README.md` do próprio repositório é um dicionário de dados muito bom —
leia-o. O que segue são os achados de uma exploração feita com DuckDB sobre as bases.

> ⚠️ **Leia isto antes de citar qualquer número daqui.** O repositório avisa que _"indicadores
> gerados a partir dos dados NÃO representam a realidade"_ — a anonimização usou aleatorização,
> generalização e supressão. **Níveis absolutos são ilustrativos.** O que se sustenta são padrões
> relativos e a dinâmica do processo, que a SME declara ter preservado. Nunca apresente uma taxa
> destas como estatística oficial da cidade.

### Volume por ano

| Ano  |  Opções | Inscrições | Crianças | Opções/inscrição | Unidades |
| ---- | ------: | ---------: | -------: | ---------------: | -------: |
| 2021 | 198.498 |     73.283 |   57.690 |             2,71 |      514 |
| 2022 | 158.122 |     64.055 |   57.820 |             2,47 |      511 |
| 2023 | 123.174 |     51.331 |   45.918 |             2,40 |      496 |
| 2024 | 197.406 |     82.690 |   71.757 |             2,39 |  **844** |
| 2025 | 159.979 |     71.949 |   62.899 |             2,22 |      836 |

O salto de 496 → 844 unidades entre 2023 e 2024 é uma mudança estrutural na base, não crescimento
da rede. **Não trate a série como contínua sem entender esse corte.**

### 1. A perda na convocação está medida — e é grande

O problema que a Gabriela descreveu tem número. Entre as crianças que chegaram a ser chamadas,
a fatia que **nunca confirmou a matrícula**:

| Ano  | Confirmaram | Chamadas e perdidas | % perdido |
| ---- | ----------: | ------------------: | --------: |
| 2021 |      29.113 |              10.274 | **26,1%** |
| 2022 |      34.795 |              12.053 |     25,7% |
| 2023 |      28.199 |               8.460 |     23,1% |
| 2024 |      50.954 |               7.260 |     12,5% |
| 2025 |      48.680 |               5.994 | **11,0%** |

Caiu pela metade no período — mas ainda são **~6 mil crianças por ano** que foram chamadas e não
ocuparam a vaga. É a evidência quantitativa do gargalo do Eixo 3 e a métrica natural para provar
impacto: _quanto do 11% a solução recupera?_

O estado a filtrar é `Cancelado na confirmacao` — **sem cedilha e sem til**, como o próprio
dicionário avisa.

### 2. Escolher perto aumenta a chance de dar certo

A intuição da Gabriela sobre território se confirma nos dados (2025):

| Opção escolhida                 | Registros | % do total | Confirmaram |
| ------------------------------- | --------: | ---------: | ----------: |
| **Mesmo bairro** do responsável |    87.507 |      51,7% |   **33,9%** |
| Bairro diferente                |    81.860 |      48,3% |       26,4% |

Quase metade das escolhas é fora do bairro, e essas convertem **29% menos**. Reforça a hipótese de
inscrição referenciada por território — mas cuidado: correlação, não causalidade. Escolher longe
pode ser sintoma de não haver vaga perto, não a causa da desistência.

### 3. Usar mais opções quase não ajuda — o que é contraintuitivo

| Opções usadas | Inscrições | Taxa de confirmação |
| ------------- | ---------: | ------------------: |
| 1             |     68.544 |               65,4% |
| 2             |     27.705 |               62,9% |
| 3             |     23.046 |               63,9% |
| 4             |     12.427 |               62,9% |
| 5             |     22.917 |               67,1% |

**38,7% das famílias usam só uma opção** e se saem tão bem quanto quem usa cinco. Isso põe em
questão o próprio desenho das 5 opções: ele multiplica a base por 2,3, gera 5 filas paralelas por
criança e alimenta o efeito cascata dos 3 dias — em troca de quase nenhum ganho de acesso.

### 4. A comprovação presencial parece ser um funil severo

Declarações "Sim" nas perguntas socioeconômicas, e quantas foram validadas:

| Ano  | Disseram "Sim" | Validadas |         % |
| ---- | -------------: | --------: | --------: |
| 2021 |         43.833 |    38.947 | **88,9%** |
| 2022 |         39.099 |     4.214 |     10,8% |
| 2023 |         43.906 |     3.840 |      8,7% |
| 2024 |        152.366 |    12.098 |      7,9% |
| 2025 |        131.674 |    10.519 |  **8,0%** |

A queda de 89% para 11% entre 2021 e 2022 é abrupta demais para ser só comportamento — é quase
certamente **mudança na forma de registrar a validação**. Mas se os ~8% recentes refletirem a
realidade, significa que **9 em cada 10 famílias que declaram vulnerabilidade não conseguem
comprová-la** — coerente com a exigência de ir presencialmente a uma unidade no dia seguinte.
**Vale confirmar com a Gabriela antes de construir em cima disso.**

### 5. A régua de pontuação foi reescrita — não compare anos

| Critério (`perg_id`)                   | 2021 | 2022 | 2023 | 2024 |   2025 |
| -------------------------------------- | ---: | ---: | ---: | ---: | -----: |
| Deficiência da criança (2)             |  100 |  100 |  100 |   25 |      — |
| Bolsa Família (11)                     |  100 |  100 |  100 |    — |      — |
| Cartão Carioca (3)                     |  100 |  100 |  100 |    — |      — |
| Territórios Sociais (21)               |  100 |  100 |  100 |    — |      — |
| **CadÚnico (28)**                      |    — |    — |    — |   25 | **51** |
| Bolsa Família ou Cartão Carioca (6)    |    — |    — |    — |   15 |      2 |
| Público-alvo da educação especial (31) |    — |    — |    — |    — |     25 |

São 13 perguntas por ano, 24 distintas no período. O questionário foi **redesenhado entre 2023 e
2024** — das 13 de 2023, só 3 sobreviveram — e os pesos foram reescalonados. Em 2025 o CadÚnico
sozinho vale 51 dos ~100 pontos. Série temporal ingênua aqui produz conclusão falsa.

### 6. A concentração de demanda é extrema

Distribuição das 836 unidades em 2025:

| Faixa                  | Unidades | Inscritos | Confirmados |
| ---------------------- | -------: | --------: | ----------: |
| Zero confirmados       |        5 |       877 |           0 |
| < 50 inscritos         |       74 |     2.531 |       1.451 |
| 50–199                 |      455 |    54.169 |      22.096 |
| 200–499                |      273 |    82.487 |      22.196 |
| **500+ (fila enorme)** |       29 |    19.915 |       2.945 |

A razão inscritos/confirmados vai de **1,0 a 27,1**, mediana 2,8. É exatamente a coexistência de
ociosidade e fila que a SME descreveu — e está visível no dado.

### 7. Armadilhas que custam horas

- **`04_UnidadesEscolaresComEndereco.csv` não tem cabeçalho.** Leia com `header=None` ou perde a
  primeira unidade. A coluna que junta com a Query A é a **posição 1**, não a 0.
- **O campo `bairro` é texto livre digitado pela família.** 832 valores distintos em 2025, ainda 522
  depois de normalizar caixa e espaços. "Campo Grande" aparece em 7 grafias; há `REALEMGO`.
  **Use `CEP`** — 0% nulo, formato consistente de 8 dígitos, ~14 mil valores distintos.
- **Bairro declarado ≠ bairro oficial.** "Complexo do Alemão" tem **1** registro em 2025: as famílias
  declaram Olaria (1.090), Inhaúma, Ramos. Favelas que cruzam bairros formais somem da análise se
  você agrupar por nome. Eu caí nessa antes de conferir.
- **`Cancelado na confirmacao`** — sem cedilha, sem til. Com acento, retorna zero linhas.
- **`pergunta_legenda` é 100% nula** nas duas bases. Use `pergunta_texto`.
- **A QueryB não abre no Excel:** 4,36 milhões de linhas, acima do teto de 1.048.576 — abriria
  truncada sem aviso. Use DuckDB, pandas em blocos, ou R.
- **A base não vem filtrada por situação.** 39% é `Cancelado pelo sistema`. Decida o recorte antes
  de contar qualquer coisa.

### 8. Capacidade oficial: só a rede parceira declara vagas

`OferecimentosEvagas/Parceiras2025.xlsx`, aba `MAIO -2025`, traz por unidade e por grupamento
(Berçário I/II, Maternal I/II) as colunas `Meta`, `Aluno`, `Incluído` e `Vagas` — **capacidade
contratada**, não estimativa:

| | Maio/2025 |
| --- | ---: |
| Unidades parceiras | 347 |
| Meta total | 44.773 |
| Alunos matriculados | 42.108 |
| **Vagas abertas declaradas** | **2.723** |
| Unidades com pelo menos 1 vaga | **163** (47%) |

**2.723 vagas abertas convivendo com fila de espera** — a ociosidade que a SME descreveu, medida em
dado oficial. É o número mais forte para justificar a tela "Perto de você" do app.

⚠️ **`totalalunoscreche20XX.xlsx` (rede direta) não tem meta nem capacidade** — só matrícula atual.
Não dá para calcular vaga aberta ali. Toda sugestão de vaga na rede direta é **heurística e precisa
ser rotulada como tal na interface** — que é exatamente o que o mockup faz. Como a rede direta é a
maior parte das 872 unidades com inscrição, essa limitação vale para quase toda a rede.

Os relatórios de parceiras são mensais, com **defasagem de ~1 mês** entre coleta e envio.

### 9. O que ainda não explorei

- **`NascidosvivosRJ.xlsx`** — 169 bairros, **2016–2026** (não "desde 2006"). É a demanda potencial
  e a peça que falta para o Eixo 1. O cruzamento com inscrições esbarra na sujeira do campo
  `bairro`; via CEP → bairro oficial é o caminho.
- **Microáreas do IPP** (shapefile) + `Unidades_Unificadas_com_Localizacao.xlsx` (CRE + microárea +
  lat/lon das 1.942 unidades) permitem a análise territorial na granularidade que a SME usa.
  Requer `geopandas` ou `pyshp` — ainda não testado aqui.
- **Trajetória entre anos:** 13,3% das crianças reaparecem em mais de um processo, com
  `aluno_anon` estável. Dá para medir quanto tempo uma criança espera até conseguir vaga.

### 10. Para geolocalização, use o arquivo certo

**Não use `04_UnidadesEscolaresComEndereco.csv`** — 258 das 2.188 unidades estão sem endereço.
Use **`OferecimentosEvagas/Unidades_Unificadas_com_Localizacao.xlsx`**, que traz
`DESIGNACAO, CRE, microárea, DENOMINACAO, RUA, BAIRRO, LATITUDE, LONGITUDE, Tipo` para 1.942
unidades.

**Sobre "distância":** a anonimização suprimiu o endereço exato da família. O melhor alcançável é
**CEP do responsável → unidade**; se cair para bairro, vira centróide de bairro, não porta a porta.
Rotule como aproximação na interface.

### Como reproduzir

DuckDB lê os `.gz` direto, sem descompactar:

```python
import duckdb
c = duckdb.connect()
c.execute("""CREATE VIEW a AS SELECT * FROM read_csv_auto(
    'Bases IC_ ClassificadoseFila/01_QueryA_InscricoesPorAno.csv.gz',
    delim=';', header=true)""")
c.execute("SELECT situacao, COUNT(*) FROM a WHERE ano=2025 GROUP BY 1").fetchall()
```

---

## A solução: app **Fila Certa**

📱 **Especificação:** [`docs/spec-app-fila-certa.md`](docs/spec-app-fila-certa.md)
🎨 **Mockup (6 telas):** [`docs/mockup_fila_certa_v1.html`](docs/mockup_fila_certa_v1.html) — abra no navegador

**PWA** para o **responsável** (pai/mãe) da criança inscrita na creche — roda em iOS e Android
sem passar por loja de aplicativos.

> **O app não reimplementa a inscrição** — ela continua no `matricula.rio`. O Fila Certa cobre a
> lacuna entre _inscrever-se_ e _ocupar a vaga_, que é exatamente onde o processo perde crianças.
> Entrada por **CPF do responsável**, sem cadastro novo.

> ✅ **Arquitetura decidida: PWA + notificação em cascata.**

```
Vaga aberta → 1. PUSH (quem instalou; não depende do telefone estar atualizado)
            → 2. WHATSAPP (todo mundo com número)
            → 3. SMS (aparelho sem internet)
            → 4. E-MAIL (registro formal)
                 ↓
            REGISTRO: canal · horário · entrega · houve resposta?
```

Escalonada, não simultânea — para de escalar assim que a família responde, respeitando a regra
oficial de 1 tentativa/dia por 3 dias em horários diferentes.

**O registro é o coração da proposta, porque hoje não existe.** Ninguém sabe se a escola ligou, se a
mensagem chegou, nem quando a opção virou "Selecionado" — e não há como provar que o protocolo dos
3 dias foi cumprido, o que importa porque a fila é auditada por órgãos reguladores. Com o registro,
a SME passa a distinguir **falha de contato** de **recusa real**, que exigem políticas opostas.

### As 6 telas

| #   | Tela                    | Resolve                                       | Como                                                                                                                            |
| --- | ----------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Consultar inscrição     | —                                             | CPF único, sem conta nova                                                                                                       |
| 2   | **Painel da inscrição** | contato desatualizado, escolha sem território | Alerta e edição de contato · selo de viabilidade por distância · oferta de vaga próxima com **"Tenho interesse" / "Agora não"** |
| 3   | Documentos              | comprovação presencial                        | Foto pelo celular · IA pré-checa, **unidade confirma**                                                                          |
| 4   | **Convocação**          | perda de vaga, cascata dos 3 dias             | Push · contagem regressiva · confirmar em um toque                                                                              |
| 5   | Perto de você           | ociosidade vs. fila                           | Unidades fora das 5 escolhas, por distância                                                                                     |
| 6   | Entenda sua pontuação   | opacidade da régua                            | Comparação com o mínimo confirmado · por que cada critério existe                                                               |

**A peça mais valiosa é o botão "Agora não".** Capturar a recusa em horas libera a vaga sem consumir
os 3 dias de convocação. Hoje só existe o silêncio — e cada silêncio custa 3 dias por elo da fila.

### O que a spec faz certo e vale preservar

- **Não promete o que não pode garantir.** Vaga em rede parceira aparece como `1 vaga` (meta
  contratada, dado firme); em rede direta, como `Provável vaga` com o aviso _"estimativa por baixa
  procura na região, não é capacidade oficial"_.
- **A IA pré-checa, a unidade decide.** Preserva a auditabilidade que os órgãos reguladores exigem —
  e torna a proposta aceitável para a SME.
- **A pontuação é explicada, não só exibida.** A tela 6 compara com o mínimo confirmado na unidade e
  registra que os pesos mudam a cada ano — coerente com a régua real extraída da `03_QueryC`.

### ⚠️ O app da SME não existe mais nas lojas

O briefing cita inscrição *"pelo portal matricula.rio ou pelo app Rioeduca em Casa"*, e a página da
SME ainda diz *"Baixe agora mesmo o aplicativo!"*. **Verifiquei em 30/08/2026: os dois links estão
mortos** — App Store 404 (e `resultCount: 0` na API da Apple), Google Play 404, busca "rioeduca" na
App Store BR com zero resultados. O app saiu do ar depois do ensino remoto de 2021; a documentação
da SME não acompanhou.

**Quem publica app municipal no Rio é a IPLANRIO**, não a SME: `MinhaSaúde.Rio` (ativo, atualizado
jun/2026), `1746 Rio` (dez/2023), `Zap Carioca` (2016, abandonado).

O que muda:

- ✅ **`MinhaSaúde.Rio` é o precedente que sustenta a proposta** — app municipal por domínio
  específico, de comunicação com o cidadão, vivo e mantido. É o análogo direto do Fila Certa.
- ⚠️ **App em loja depende da IPLANRIO e não estreia amanhã**, o que colide com o critério de maior
  peso. **PWA é a recomendação**: push sem loja, integrado ao `matricula.rio` que a família já
  acessa pelo celular.
- 💡 **A morte do Rioeduca em Casa joga a favor do argumento:** app que exige instalação para uma
  função sazonal é desinstalado; camada web vinculada ao portal existente, não.

### Três lacunas que o app expõe — e que são a proposta

Nem a base nem o sistema atual têm o que o app precisa:

1. **Contato editável do responsável** — não existe campo. É a causa-raiz da perda de vagas.
2. **Registro de quando a opção mudou de status** — sem isso, nem família nem equipe sabem o prazo
   restante.
3. **Registro de tentativas de contato** — canal, horário, entrega, resposta. Não existe em lugar
   nenhum; é o que a cascata cria.

Não escondam na apresentação: **são a proposta**, não falha dos dados. Mockar na demo e declarar
como requisito de integração.

### As três frentes do time

| Frente | Estado |
| --- | --- |
| **App do responsável (Fila Certa)** | ✅ mockup pronto, 6 telas · arquitetura decidida (PWA) |
| **Painel da prefeitura** | ⬜ conceito aprovado, aguarda mockup |
| **Mapa territorial** | ⬜ 5 camadas propostas |

O fio condutor das três é um **motor por CPF único da criança** em vez de por opção escolhida — o
que resolve os três eixos como consequência de uma só mudança de modelo. O painel consome o sinal
gerado quando uma família toca **"Tenho interesse"** no app: é a ponte direta entre o app e o
planejamento. Detalhes em [`CLAUDE.md`](CLAUDE.md) §3c e no
[`handoff`](docs/handoff_hackathon_sme.md).

### Por que PWA, e não app nativo

| | PWA | Nativo |
| --- | --- | --- |
| Estreia "amanhã" | ✅ é uma URL | ❌ depende da IPLANRIO publicar |
| Push Android | ✅ pleno, sem instalar nada | ✅ |
| Push iOS | ⚠️ exige "Adicionar à Tela de Início" | ✅ |
| **Demonstrar push hoje** | ✅ FCM grátis | ❌ **iOS exige conta paga de US$ 99** |
| Toolchain | Node, já instalado | Xcode + Android Studio, **ausentes na máquina** |

O único ganho do nativo seria push mais confiável no iOS — mas WhatsApp/SMS precisa existir em
qualquer arquitetura, inclusive na nativa. Não compensa toolchain, conta paga e duas bases de código
para melhorar só o primeiro degrau da cascata, na plataforma minoritária do público-alvo.

⚠️ **Na demo, só o push via FCM/Android roda ao vivo de graça.** WhatsApp e SMS devem ser simulados,
com a trilha de tentativas visível na tela — mostrar o registro vale mais que enviar a mensagem.

### Em aberto

- **Autenticação:** o mockup entra só com CPF, o que expõe dados de uma criança a quem souber o CPF
  do responsável. Serve para a demo; a proposta precisa de 2º fator ou gov.br.
- **Não há CPF real nos dados.** `aluno_anon` e `responsavel_anon` são chaves derivadas — o login
  por CPF só funciona contra o sistema vivo da SME, não contra esta extração.
- **Duas telas mencionadas e não desenhadas:** o fluxo de atualização de contato (o botão existe no
  alerta) e o *fallback* SMS/offline para a notificação de convocação.
- **O mockup carrega fontes e ícones de CDN.** Embuta os assets antes de publicar ou apresentar — a
  rede do evento é instável.

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

O critério de maior peso é **impacto real**: _"dá para colocar amanhã na prefeitura e gerar valor?"_

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
Atribuição obrigatória: _Prefeitura da Cidade do Rio de Janeiro_.

A camada geográfica de escolas tem última atualização em **junho/2023** — a rede mudou desde então.
Use-a para contexto e geolocalização, não como fonte de verdade sobre a rede atual.
