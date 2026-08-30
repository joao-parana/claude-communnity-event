# Handoff — Hackathon SME-Rio + Claude Impact Lab 2026

> Documento de continuidade. Todo o conteúdo abaixo foi discutido e validado em sessão de planejamento antes da fase de construção. Objetivo: retomar direto na implementação no Claude Code, sem precisar re-explicar contexto.

---

## 1. O desafio, em uma frase

A Inscrição Creche do Rio não sofre só de falta de vaga — sofre de **descompasso entre oferta e demanda por território/turno**, agravado por um fluxo de retaguarda manual (planejamento, classificação, convocação) que não acompanha a família nem sinaliza problemas pra equipe da SME/CRE em tempo real.

**Três eixos oficiais do desafio:**

1. **Planejamento** — vagas dimensionadas pela fila do ano anterior, sem sinal territorial preditivo real
2. **Classificação** — sistema classifica por *opção*, não por *CPF*: uma criança pode segurar até 5 vagas simultâneas, distorcendo a fila
3. **Convocação** — processo manual (ligação/e-mail/WhatsApp por 3 dias), sem forma da família corrigir contato desatualizado, gerando vagas ociosas por semanas

**Critério de julgamento dominante:** Impacto Real pesa 40 de 100 pontos (multiplicador x8). A pergunta central do júri é "a prefeitura usaria isso amanhã?" — mais importante que sofisticação técnica ou originalidade da ideia.

---

## 2. Estratégia de solução (fio condutor)

Em vez de 3 soluções soltas (uma por eixo), a decisão foi construir **um motor central de dados** que resolve os 3 eixos como consequência de uma mudança de modelo: **classificar e acompanhar por CPF único da criança, não por opção escolhida.**

- Resolve Classificação: dedup das 5 opções em 1 registro por criança
- Resolve Convocação: fila de contato única, rastreável, com contato sempre atualizável
- Resolve Planejamento: demanda real por território (sem inflar por múltiplas opções da mesma criança) cruzada com nascimentos históricos

**Dado de abertura forte pra apresentação:** 39% de todas as 837 mil linhas de inscrição têm situação `Cancelado pelo sistema` — mais que o volume de `Confirmado` (23%). É a evidência quantitativa da "fila fantasma" causada pela classificação por opção.

---

## 3. Dados — o que existe, validado linha a linha

Repositório: `dadoscreche-main.zip` (SME-Rio). Estrutura real confirmada:

### `Bases IC_ ClassificadoseFila/`

| Arquivo | Grão | Linhas | Observações críticas |
|---|---|---:|---|
| `01_QueryA_InscricoesPorAno.csv.gz` | 1 opção de creche escolhida | 837.179 | `aluno_anon` e `responsavel_anon` são **estáveis entre as 5 opções e entre os 5 anos (2021–2025)** — base do motor por CPF único. Traz `bairro`/`CEP` da família (nulo em 2,8%), `unidade`, `situacao`. **39% `Cancelado pelo sistema`**, 23% `Confirmado`, 21,3% `Lista de espera`. Atenção: grafia é `Cancelado na confirmacao`, sem cedilha/til. |
| `02_QueryB_RespostasSocioEconomicas.csv.gz` | 1 pergunta respondida | 4.357.119 | Formato longo. Junta com Query A por `(prm_id, plm_id, ipl_id)`. Não abre no Excel (limite de 1.048.576 linhas) — usar pandas em chunks ou DuckDB. |
| `03_QueryC_PerguntasComDescricao.csv` | 1 pergunta/processo/ano | 65 | **A régua de pontuação muda a cada ano.** Entre 2023→2024 só 3 das 13 perguntas sobreviveram; peso de "deficiência da criança" caiu de 100 para 25 pontos. Nunca comparar pontuação bruta entre anos sem normalizar pelo peso relativo daquele ano específico (usar `perg_id` para rastrear a mesma pergunta, `ich_perg_id` para juntar com Query B). |
| `04_UnidadesEscolaresComEndereco.csv` | 1 unidade | 2.188 | **Não confiar neste arquivo pra geolocalização** — 258 unidades sem endereço, sem cabeçalho (`header=None`). Usar o arquivo abaixo no lugar. |

### `OferecimentosEvagas/`

| Arquivo | Conteúdo | Uso |
|---|---|---|
| `Unidades_Unificadas_com_Localizacao.xlsx` | `DESIGNACAO, CRE, microárea, DENOMINACAO, RUA, BAIRRO, LATITUDE, LONGITUDE, Tipo` | **Esta é a fonte de geolocalização real** (não a Query D). Base do mapa e do cálculo de distância. |
| `Parceiras20XX.xlsx` | 3 abas por arquivo: `Apoio` (ignorar), `Endereços`, e uma aba mensal (ex. `Maio-2024`) com `Meta`, `Total Alunos`, `Vagas`, `Excedentes` por unidade parceira | **Única fonte com capacidade oficial declarada.** Permite calcular vaga aberta real: `Vagas = Meta - Total Alunos` (ou usar a coluna `Excedentes` já calculada). |
| `totalalunoscreche20XX.xlsx` | Alunos matriculados por CRE/unidade/grupamento/turno (rede pública direta) | **Não tem capacidade/meta declarada.** Não dá pra calcular "vaga aberta" com certeza aqui — só matrícula atual. Qualquer sugestão de vaga pra rede direta é estimativa, precisa avisar isso na UI. |
| `LEIAME_OFERECIMENTOSPARCEIRASEPUBLICAS.txt` | Documentação dos arquivos acima | Confirma que os relatórios de parceiras são mensais, com defasagem de ~1 mês. |

### Outras bases

| Arquivo | Conteúdo | Uso |
|---|---|---|
| `NascidosvivosRJ.xlsx` | Nascidos vivos por bairro, por ano, desde 2006 | Sinal preditivo de demanda futura pro Eixo 1 (nascimento hoje = demanda de creche em ~1–3 anos). Não estava no briefing original, é uma descoberta útil. |
| `Microáreas_SME_revisãoIPP/` | Shapefile (`.shp`/`.dbf`/`.prj`) com organização territorial do IPP | Necessário `geopandas` ou `pyshp` para ler — **não testado no ambiente de validação por falta de acesso à rede**; testar localmente no Claude Code. |

### Limitações de anonimização a documentar no README do projeto

- Não há endereço exato da família — só bairro/CEP. Qualquer "distância" calculada é bairro→unidade (centróide), não porta a porta.
- Não há CPF real nos dados — `aluno_anon`/`responsavel_anon` são chaves derivadas. Login real por CPF no app dependeria de integração com o sistema vivo da SME, não com esta extração anonimizada.
- Rede direta (855 das 872 unidades) não tem capacidade oficial nos arquivos fornecidos — qualquer "vaga disponível" ali é heurística, não fato do sistema.

---

## 4. App do responsável — "Fila Certa" (mockup pronto)

Arquivo do mockup: `mockup_fila_certa.html` (entregue nesta sessão, 6 telas).

**Premissa confirmada com o time:** o app **não substitui** o matricula.rio. A inscrição continua sendo feita no site oficial; o app é uma camada de apoio vinculada por CPF ao que já existe lá. Login é uma consulta, não um cadastro novo.

### Telas construídas

1. **Consultar por CPF** — busca a inscrição já feita no site, sem duplicar cadastro
2. **Painel da inscrição** — as 5 escolhas com selo de viabilidade por distância (`Alta viabilidade` / `Em fila` / `Risco de distância`), alerta de contato desatualizado no topo (dor #1 do fluxo), card de sugestão de creche próxima com vaga aberta, link para tela de pontuação
3. **Documentos** — upload pelo celular em vez de ida presencial; pré-checagem por IA claramente rotulada como automática (não substitui validação da unidade); Cadastro Único mostrado como já validado via Data Lake (fluxo que já existe hoje)
4. **Convocação** — contador de prazo de confirmação (3 dias úteis), confirmação de vaga com um toque, linha do tempo da inscrição
5. **Perto de mim** — lista de unidades fora das 5 escolhas originais, ordenadas por distância. Parceiras aparecem com selo "vaga confirmada pela meta contratada" (dado real); rede direta aparece com selo "estimativa por baixa procura, não é capacidade oficial" (heurística, rotulada como tal)
6. **Entenda sua pontuação** — resolvida para ser didática: barra visual comparando a pontuação da família com o mínimo historicamente confirmado naquela unidade, explicação de por que os critérios existem (prioridade legal por vulnerabilidade social) antes de listar os pesos, e nota histórica de que a régua muda a cada processo

### Decisões de design (para manter consistência se o Claude Code recriar as telas)

- Nome do app: "Fila Certa" (pode trocar)
- Paleta: fundo areia suave, azul-atlântico profundo como cor institucional, âmbar como accent de CTA, verde para estados positivos/confirmados, terracota/vermelho para pendências e risco — evitando a paleta genérica de IA (creme + terracota `#D97757`)
- Tipografia: Archivo (display/headlines), Inter (corpo, legibilidade alta para usuários com literacia digital variada), IBM Plex Mono (protocolos, CPF, contadores)
- Linguagem: sempre nomear o que a pessoa controla, nunca jargão de sistema; toda estimativa/heurística é rotulada como tal na própria tela, nunca apresentada como fato

### Funcionalidades pendentes de mockup (mencionadas, não desenhadas ainda)

- Fluxo de atualização de contato (o botão existe no alerta, a tela em si não foi desenhada)
- Modo offline/SMS fallback para notificação crítica de convocação

---

## 5. Painel da prefeitura — ainda não iniciado (próximo passo)

Ideias já discutidas e aprovadas conceitualmente, aguardando mockup:

- **Fila única por CPF** (não por opção) — visão consolidada por criança
- **Alerta de vaga ociosa em risco** — antes de virar ociosidade, baseado em padrão histórico de tempo de resposta por unidade
- **Score de risco de cancelamento por inscrição** — combinando distância casa-unidade + padrão histórico do território
- **Dashboard comparativo entre as 11 CREs**
- Deve consumir o mesmo "sinal de demanda" gerado quando uma família toca "tenho interesse" numa sugestão de vaga próxima no app (ponte direta entre o app e o planejamento, Eixo 1)

---

## 6. Mapa territorial — camadas propostas (não iniciado)

1. **Demanda real por CPF único** geolocalizada por bairro/CEP (corrige a distorção de contar as 5 opções como 5 demandas)
2. **Descompasso oferta-demanda** por unidade/microárea ao longo de 2021–2025 (vagas ofertadas x confirmadas x canceladas)
3. **"Viagem inviável"** — distância das 5 escolhas de cada família, sinalizando territórios sem opção viável perto
4. **Camada preditiva** — nascidos vivos por bairro (`NascidosvivosRJ.xlsx`) cruzado com capacidade atual, projetando necessidade futura por microárea
5. **Linha do tempo interativa** (slider 2021→2025) mostrando evolução do descompasso por território

---

## 7. Gaps do briefing mapeados para features (tabela de rastreabilidade)

| Gap do briefing (SME) | Onde é resolvido |
|---|---|
| Fila sem visibilidade de prazo | App, tela 4 (contador de convocação) |
| Contato desatualizado não editável | App, alerta na tela 2 (fluxo de tela ainda não desenhado) |
| Vagas ociosas + fila represada por descompasso território/turno | App, tela 5 (sugestão de vaga próxima) + Mapa, camada 2 |
| Critérios de pontuação mudam a cada processo, família não entende | App, tela 6 (pontuação didática) |
| Estados transitórios não sinalizados entre as 5 opções do mesmo cadastro | Parcialmente no app (tela 2 mostra as 5 juntas); tratamento completo é tarefa do Painel da prefeitura |
| Colisão de identificação de criança sem CPF/DNV/NIS | Não resolvido pelo app diretamente; login por CPF real no sistema vivo reduziria o problema como efeito colateral, mas depende de integração fora do escopo desta extração anonimizada |
| Planejamento baseado só na fila do ano anterior | Mapa, camada 4 (nascidos vivos como sinal preditivo) |

---

## 8. Decisões em aberto para a equipe

- [ ] Confirmar se a sugestão de vaga na rede direta (estimativa, sem capacidade oficial) deve aparecer com aviso, como está no mockup, ou ser limitada só às parceiras
- [ ] Escolher a métrica exata do "score de viabilidade por distância" (raio fixo? percentil histórico de cancelamento por faixa de distância?)
- [ ] Decidir se o painel da prefeitura é web (mais rápido de prototipar) ou mockup estático como o app
- [ ] Testar a leitura do shapefile de microáreas localmente (ambiente de validação não tinha acesso à rede para instalar `geopandas`)

## 9. Arquivos entregues nesta sessão

- `mockup_fila_certa.html` — mockup interativo das 6 telas do app (abrir direto no navegador)
- Este documento (`handoff_hackathon_sme.md`)

## 10. Fontes originais do desafio

- Briefing completo: PDF "Hackathon SME-Rio" (Contexto, 3 eixos, fluxo, critérios de classificação, gaps, dados disponibilizados)
- Apresentação institucional: `Apresentação.pptx` (14 slides, mesmo conteúdo do briefing em formato visual)
- Regras e critérios de julgamento: PDF "Claude Impact Lab — Rio de Janeiro" (agenda, regras de submissão, rubrica de avaliação: Impacto Real x8, Produto x4, Engenharia x4, Ideia x2, Apresentação x2)
- Dados: `dadoscreche-main.zip`, repositório `CIT-SME-RJ/dadoscreche`
