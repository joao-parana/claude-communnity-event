# CLAUDE.md — Claude Impact Lab Rio #2

Contexto operacional para o Claude Code neste repositório. Leia antes de qualquer tarefa.

---

## 1. O que é este projeto

Hackathon de **um dia** (30/08, 8h–20h, escritório da VTEX — R. Marquês de Olinda, 11, Botafogo),
segunda edição do **Claude Impact Lab Rio**, patrocinado pela Anthropic e realizado em parceria com a
**Prefeitura do Rio**, a **Secretaria Municipal de Educação (SME)** e a
**Secretaria Municipal de Desenvolvimento Econômico (SMDE)**.

**O briefing já aconteceu.** O desafio é o **acesso à creche para crianças de 0 a 3 anos e 11 meses**:
planejamento de vagas, lógica de inscrição/classificação e — o gargalo mais agudo — o processo de
**convocação**, hoje manual e que perde vagas por contato desatualizado.

📄 **Leia primeiro: [`docs/desafio-inscricao-creche.md`](docs/desafio-inscricao-creche.md)** —
briefing organizado da Gabriela (Gerente de Sistemas e Dados, Coordenadoria de Inovação e Tecnologia
da SME), com os três eixos, os oito pontos de quebra, os dados fornecidos e os critérios de avaliação.
A transcrição bruta está em [`docs/trancricao-gab.md`](docs/trancricao-gab.md).

As melhores soluções são **doadas para a cidade**. Isso é um requisito de projeto, não um detalhe:
o entregável precisa ser transferível (licença aberta, sem dependência de contas pessoais, documentado
em português).

### Cronograma que dita o ritmo de engenharia

| Hora | Evento | Implicação técnica |
| --- | --- | --- |
| ~~08h30~~ | ~~Briefing~~ | ✅ feito — ver `docs/desafio-inscricao-creche.md` |
| 09h00 | Início dos trabalhos | **7h30 líquidas de construção** |
| **16h30** | **GitHub público — último commit válido** | **Hard stop. Commit das 16h31 não conta.** |
| 16h30–17h30 | Jurados avaliam ~40 projetos | Entrega tem que ser entendível em minutos |
| 17h30 | Anúncio dos **5 finalistas** e apresentações | Todo time deve estar preparado |
| — | 6 min de pitch + 6 min de Q&A | Corte rígido aos 6:00 |
| 18h30 | Premiação | Plano Max (US$ 200) por 1 mês para o time vencedor |

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

## 3. O desafio: inscrição e acesso à creche

Resumo operacional. **O documento completo é [`docs/desafio-inscricao-creche.md`](docs/desafio-inscricao-creche.md)** —
consulte-o antes de propor qualquer solução.

### Escala do subdomínio

| Indicador | Valor |
| --- | --- |
| Alunos na educação infantil, modalidade creche | **~89.000** |
| Unidades de educação infantil (creche) | **~900** |
| Inscrições/ano (CPFs únicos) | **~45.000** |
| Registros na base (por opção) | **> 100.000** — cada CPF gera até 5 |
| RMI (Registro Municipal Integrado) | **> 12 milhões** de registros |
| Prazo para efetivar matrícula após convocação | **3 dias** (+1 excepcional) |

Creche **não é ensino obrigatório** — daí existir classificação por pontuação em vez de alocação
direta. A partir dos 4 anos a SME garante o bairro imediato.

### Os três eixos (divisão da própria SME)

1. **Planejamento de vagas** — começa em setembro para o ano seguinte, em três níveis: nível central
   → 11 CREs → microáreas (clusters do IPP). Ancorado quase só em **demanda histórica**. Sintoma do
   desalinhamento: vagas ociosas e filas gigantes **no mesmo território**.
2. **Inscrição e classificação** — até 5 unidades por CPF, **sem nenhum critério territorial**.
   A classificação é **por opção, não por criança**: uma criança existe em até 5 filas simultâneas.
3. **Convocação** ⚠️ **— o gargalo mais agudo.** Manual, a cargo do diretor.

### Os 8 pontos de quebra

| # | Ponto de quebra | Efeito |
| --- | --- | --- |
| 1 | 5 unidades sem critério territorial | Opções inviáveis |
| 2 | Classificação por opção, não por CPF | 45 mil inscrições → 100 mil registros |
| 3 | Comprovação de vulnerabilidade **presencial** | Barreira para quem tem menos mobilidade |
| 4 | **Contato não editável no sistema** | **Vagas perdidas por falta de comunicação** |
| 5 | Convocação manual pelo diretor | Carga sobre quem já gere a unidade |
| 6 | 3 dias por convocação, em cascata entre 5 filas | > 1 semana para preencher uma vaga |
| 7 | Oferta única — recusou, sai de todas as filas | Reinscrição infla a demanda |
| 8 | Planejamento só por demanda histórica | Ociosidade e fila coexistindo |

**A causa-raiz do nº 4, dita textualmente:** o sistema **não permite editar o contato nem tem campo
de observação**. Quando a família aparece na creche com número novo, isso fica no *"caderninho"* do
diretor. Classificação roda em janeiro; em fevereiro/março o telefone já mudou.

### Restrições inegociáveis

- **A ordem da fila de espera é auditada por órgãos reguladores.** Qualquer solução precisa
  preservá-la e evidenciá-la.
- **Publicação da classificação em Diário Oficial** é obrigatória.
- **CPF da criança validado na Receita Federal**; uma inscrição ativa por CPF.

### Dados fornecidos

**Repositório oficial: https://github.com/CIT-SME-RJ/dadoscreche/**

```bash
git clone https://github.com/CIT-SME-RJ/dadoscreche.git
```

Materiais de apoio linkados no README do repo: [apresentação da
SME](https://rioeduca-my.sharepoint.com/:p:/g/personal/gabrielledomingues_rioeduca_net/IQAlvS8n9w7OQ6WcJK2T-wr6AVcXGJuT7MdyJ41qQtqlff0?e=xkQwfk)
e [briefing completo](https://docs.google.com/document/d/1jZenYEKR2hJOVrxLXWM0xjxmoiohAqEl/edit?usp=sharing).

| Pasta / arquivo | Conteúdo | Grão |
| --- | --- | --- |
| `Bases IC_ ClassificadoseFila/01_QueryA…csv.gz` | **837.179** linhas | uma opção de creche escolhida |
| `…/02_QueryB…csv.gz` | **4.357.119** linhas | uma pergunta respondida |
| `…/03_QueryC_PerguntasComDescricao.csv` | 65 linhas | uma pergunta por processo/ano — **a régua de pontuação** |
| `…/04_UnidadesEscolaresComEndereco.csv` | 2.188 linhas | uma unidade escolar — **sem cabeçalho** |
| `OferecimentosEvagas/` | XLSX por ano | vagas e matriculados, públicas e parceiras |
| `OferecimentosEvagas/Unidades_Unificadas_com_Localizacao.xlsx` | 1.942 unidades | **CRE + microárea + lat/lon** |
| `Microáreas_SME_revisãoIPP/` | shapefile | polígonos das microáreas |
| `NascidosvivosRJ.xlsx` | 169 bairros, 2016–2026 | **demanda potencial** |

Escopo: 5 processos — 179 (2021), 181 (2022), 184 (2023), 194 (2024), 195 (2025). **2026 não está
incluído.** Separador `;`, UTF-8 **com BOM**.

**A análise exploratória está resumida no [README.md](README.md).** Leia antes de modelar — há
armadilhas que custam horas.

Anonimização — **removido**: idade real, endereço exato (só bairro e CEP), data de nascimento (só ano
e mês). **Preservado**: sequência do processo, lógica da pontuação, relações entre as tabelas,
dinâmica real de transição de estados, e a **trajetória da mesma criança entre anos** (`aluno_anon`
é estável nos 5 processos).

> ⚠️ O próprio repositório avisa: **"indicadores gerados a partir dos dados NÃO representam a
> realidade"**. Trate níveis absolutos como ilustrativos; o que se sustenta são **padrões relativos**
> e a dinâmica do processo. Nunca apresente uma taxa dessas base como estatística oficial da cidade.

## 3b. A solução do time: **Fila Certa** (PWA)

📱 **Especificação: [`docs/spec-app-fila-certa.md`](docs/spec-app-fila-certa.md)**
🎨 **Mockup (6 telas): [`docs/mockup_fila_certa_v1.html`](docs/mockup_fila_certa_v1.html)**

> ✅ **Arquitetura decidida: PWA + camada de notificação em cascata.** Push para quem instalou,
> WhatsApp/SMS para todo mundo, e **registro de qual tentativa alcançou a família** — o que hoje não
> existe e torna o fluxo não-rastreável. Detalhes em [`spec`](docs/spec-app-fila-certa.md) §4.

App para o **responsável** (pai/mãe) da criança inscrita. Posicionamento decidido, e é o ponto mais
importante da spec:

> **O app não reimplementa a inscrição.** Ela continua no `matricula.rio`. O Fila Certa cobre a
> lacuna entre *inscrever-se* e *ocupar a vaga* — exatamente onde o processo perde crianças.
> Vínculo por **CPF do responsável**, sem cadastro novo.

### As 6 telas e o que cada uma ataca

| # | Tela | Ponto de quebra | Mecanismo |
| --- | --- | --- | --- |
| 1 | Consultar inscrição | — | Entrada por CPF, sem conta nova |
| 2 | **Painel da inscrição** | **4, 1, 7** | Alerta e edição de contato; selo de viabilidade por distância; oferta de vaga próxima com **"Tenho interesse" / "Agora não"** |
| 3 | Documentos | **3** | Upload por foto substitui ida presencial; IA faz pré-checagem, **unidade confirma** |
| 4 | **Convocação** | **4, 5, 6** | Push + contagem regressiva + confirmação em um toque |
| 5 | Sugestões perto de você | **1, 8** | Unidades fora das 5 escolhas, por distância |
| 6 | Entenda sua pontuação | **2** | Régua comparativa + por que cada critério existe |

**A peça mais valiosa é o botão "Agora não"** (tela 2): capturar declínio em horas libera a vaga sem
consumir os 3 dias, atacando o efeito cascata. Hoje só existe o silêncio, e o silêncio custa 3 dias
por elo da fila.

### ⚠️ Não existe app da SME nas lojas — verificado em 30/08/2026

O briefing menciona inscrição *"pelo app Rioeduca em Casa"* e a página da SME ainda o anuncia.
**Os dois links estão mortos:** App Store 404 e `resultCount: 0` na API da Apple; Google Play 404;
busca "rioeduca" na App Store BR retorna zero. O app saiu do ar depois do ensino remoto de 2021 e a
documentação da SME não acompanhou.

**Quem publica app municipal é a IPLANRIO**, não a SME — `MinhaSaúde.Rio` (ativo, atualizado
jun/2026), `1746 Rio` (dez/2023), `Zap Carioca` (2016, abandonado).

**Consequência para a proposta:**

- ❌ Não propor módulo no Rioeduca em Casa — ele não existe.
- ✅ **`MinhaSaúde.Rio` é o precedente institucional**: app municipal por domínio, de comunicação
  com o cidadão, vivo e mantido. É o análogo do Fila Certa e o melhor argumento de viabilidade.
- ⚠️ **App em loja depende da IPLANRIO e não estreia amanhã** — conflito direto com o critério de
  maior peso (Impacto Real ×8). **PWA é a recomendação**: push sem loja, integrado ao
  `matricula.rio`, que já é acessado majoritariamente por celular.
- 💡 A morte do Rioeduca em Casa é **argumento a favor**, não constrangimento: app que exige
  instalação para função sazonal é desinstalado; camada web vinculada ao portal que a família já
  usa, não.

### Lacunas que o app expõe — e que são a proposta

Três coisas que o app precisa **não existem na base nem no sistema atual**:

1. **Contato editável do responsável** — suprimido na anonimização, e no sistema real simplesmente
   não há campo. É a causa-raiz do ponto de quebra nº 4.
2. **Timestamp de mudança de status** — o briefing confirma que não há registro de quando uma opção
   virou "Selecionada"; nem família nem equipe sabem o prazo restante.
3. **Registro de tentativas de contato** — canal, horário, status de entrega, houve resposta.
   Não existe em lugar nenhum; é o que a cascata cria.

Não escondam isso na apresentação: **são a proposta**, não falha da base. Mockar na demo e declarar
como requisito de integração.

### A cascata de notificação — o coração da proposta

```
Vaga aberta → 1. PUSH (quem instalou o PWA; não depende do telefone estar atualizado)
            → 2. WHATSAPP (todo mundo com número)
            → 3. SMS (aparelho sem internet)
            → 4. E-MAIL (registro formal)
                 ↓
            REGISTRO: canal · timestamp · entrega · houve resposta?
```

Escalonada, não simultânea: para de escalar assim que a família responde, respeitando a regra
oficial de **1 tentativa/dia por 3 dias em horários diferentes**.

**O registro é o que não existe hoje.** Sem ele ninguém sabe se a escola ligou, se a mensagem foi
entregue, nem quando a opção virou "Selecionado" — e não há como provar que o protocolo dos 3 dias
foi cumprido, o que importa porque a fila é auditada por órgãos reguladores. Com ele, a SME passa a
distinguir **falha de contato** de **recusa real** — duas coisas que exigem políticas opostas.

### Por que PWA (decidido, não em aberto)

1. **Não existe app da SME nas lojas** — nada onde encaixar módulo; app novo põe a IPLANRIO no
   caminho crítico.
2. **Push no iOS exige conta paga de developer (US$ 99).** Com Apple ID gratuito a capability não
   fica disponível — demonstraríamos o app inteiro *exceto* a tela que é a proposta.
3. **Ambiente local não tem toolchain:** sem Xcode (só Command Line Tools), sem Android SDK, sem
   Flutter, e **12 GB livres em disco**. Instalar hoje custaria horas do orçamento de 7h30.
4. **Impacto Real ×8** pergunta *"usaria amanhã?"*. Uma URL, sim; um binário em fila de revisão, não.

O único ganho do nativo seria push mais confiável no iOS — mas WhatsApp/SMS precisa existir em
qualquer arquitetura, inclusive na nativa. O nativo custaria toolchain, conta paga e duas bases para
melhorar só o primeiro degrau da cascata, na plataforma minoritária do público-alvo.

### Limites do push por plataforma

| | Android | iOS |
| --- | --- | --- |
| Web Push | ✅ sem ressalvas, funciona em aba | ✅ desde 16.4, **só se instalado na tela de início** |
| Push silencioso | ✅ | ❌ não existe |

No iOS não há prompt automático de instalação, e dentro de *webview* (navegador do WhatsApp) a opção
some. Alcance estimado 10–15× menor que nativo. Como o parque do público-alvo é majoritariamente
Android, a maioria tem push pleno sem instalar nada — mas é exatamente por isso que a cascata existe.

⚠️ **Na demo:** só o **FCM/Android** é demonstrável ao vivo de graça. WhatsApp e SMS devem ser
simulados, com **a trilha de tentativas visível na tela** — mostrar o registro vale mais que enviar
a mensagem de verdade.

### Ainda em aberto

- **Autenticação.** O mockup entra só com CPF, o que expõe dados de uma criança a quem souber o CPF
  do responsável. Basta para a demo; para a proposta, exige 2º fator ou gov.br.
- **Provedor de WhatsApp.** A Business API exige *templates* aprovados e número oficial.
- **Assets do mockup vêm de CDN.** Embuta antes de publicar ou apresentar offline.

## 3c. Estratégia e frentes de trabalho

> Consolidado do [`docs/handoff_hackathon_sme.md`](docs/handoff_hackathon_sme.md), sessão de
> planejamento do outro desenvolvedor do time.

### Rubrica de avaliação — pesos reais

| Critério | Multiplicador | Pontos de 100 |
| --- | ---: | ---: |
| **Impacto Real** | **×8** | **40** |
| Produto | ×4 | 20 |
| Engenharia | ×4 | 20 |
| Ideia | ×2 | 10 |
| Apresentação | ×2 | 10 |

**Impacto Real sozinho vale 40% da nota.** A pergunta do júri é *"a prefeitura usaria isso amanhã?"*
— acima de sofisticação técnica ou originalidade. Quando houver conflito entre elegância e
adotabilidade, escolha adotabilidade.

### O fio condutor: um motor por CPF único

Decisão do time: **não** construir três soluções soltas (uma por eixo), e sim **um motor central de
dados** que troca o modelo — **classificar e acompanhar por CPF único da criança, não por opção
escolhida**. Os três eixos caem como consequência:

| Eixo | Como o motor resolve |
| --- | --- |
| Classificação | Deduplica as 5 opções em 1 registro por criança |
| Convocação | Fila de contato única, rastreável, com contato atualizável |
| Planejamento | Demanda real por território, sem inflar pelas múltiplas opções da mesma criança, cruzada com nascimentos |

**Dado de abertura da apresentação:** **39%** das 837 mil linhas são `Cancelado pelo sistema` —
mais que o volume de `Confirmado` (23%). É a evidência quantitativa da *fila fantasma* criada pela
classificação por opção.

### Três frentes

| Frente | Estado | Onde está |
| --- | --- | --- |
| **App do responsável (Fila Certa)** | ✅ mockup pronto, 6 telas | §3b + [`spec-app-fila-certa.md`](docs/spec-app-fila-certa.md) |
| **Painel da prefeitura** | ⬜ não iniciado | conceito aprovado, aguarda mockup |
| **Mapa territorial** | ⬜ não iniciado | 5 camadas propostas |

**Painel da prefeitura** — fila única por CPF; alerta de vaga ociosa *antes* de virar ociosidade,
por padrão histórico de tempo de resposta da unidade; score de risco de cancelamento por inscrição
(distância + histórico do território); comparativo entre as 11 CREs. Deve consumir o sinal gerado
quando uma família toca **"Tenho interesse"** no app — é a ponte direta entre app e planejamento.

**Mapa territorial** — 5 camadas: (1) demanda real por CPF único geolocalizada; (2) descompasso
oferta-demanda por unidade/microárea 2021–2025; (3) *"viagem inviável"* — territórios sem opção
viável perto; (4) camada preditiva com nascidos vivos; (5) linha do tempo 2021→2025.

### Decisões em aberto do time

- [ ] Sugestão de vaga na rede direta (estimativa) aparece com aviso, como no mockup, ou fica só nas parceiras?
- [ ] Métrica exata do score de viabilidade por distância — raio fixo ou percentil histórico de cancelamento por faixa?
- [ ] Painel da prefeitura: web funcional ou mockup estático?
- [ ] Ler o shapefile de microáreas (o outro dev não conseguiu instalar `geopandas` no ambiente dele)

### O que o outro dev ainda não sabe

Levar para ele na próxima sincronização:

1. **O `Rioeduca em Casa` saiu das lojas** (§3b) — App Store e Google Play retornam 404, apesar de
   o briefing e a página da SME ainda o citarem. Não dá para propor módulo nele. O precedente vivo é
   o `MinhaSaúde.Rio`, da IPLANRIO, e a recomendação de canal passa a ser **PWA**.
2. **A rede parceira declara 2.723 vagas abertas** em maio/2025 (§ no [README](README.md)) — dado
   oficial, não estimativa.
3. **`NascidosvivosRJ.xlsx` cobre 2016–2026**, não "desde 2006" como consta no handoff.
4. A análise quantitativa das bases (perda de 11% na convocação, efeito da distância) está no
   [README](README.md).


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

### Hierarquia das fontes

1. **As quatro tabelas entregues pela SME** — fonte de verdade. Tudo que importa para a avaliação sai
   daí.
2. **Microáreas do IPP** (também entregues) — a unidade territorial que a SME de fato usa para
   monitorar, mais fina que a CRE.
3. **`data.rio`** — *enriquecimento*. Útil para o que a base do desafio não tem: geometria das CREs
   para mapas, IDS por bairro/setor censitário (o mesmo critério socioeconômico que a prefeitura já
   usa), e conferência cruzada da rede física.

O *join* geográfico (unidade → microárea → CRE → bairro) é o eixo de quase toda análise territorial
aqui — a base de unidades entregue já traz **lat/lon**, e `rio_crawler.py cres` dá os polígonos das
CREs em GeoJSON para cruzar.

---

## 6. Ferramental deste repositório

```
.
├── CLAUDE.md                        # este arquivo
├── app/                             # ⭐ o PWA Fila Certa — ver app/README.md
│   ├── backend/                     #   FastAPI: api/ domain/ services/ adapters/ repositories/
│   ├── frontend/                    #   Vite + JS vanilla: pages/ components/ lib/ sw.js
│   └── .env.example
├── docs/
│   ├── desafio-inscricao-creche.md  # ⭐ o briefing organizado — leia primeiro
│   ├── trancricao-gab.md            # transcrição bruta do briefing
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
3. **Os dados são de crianças.** Já vêm anonimizados, mas a base preserva a dinâmica real do
   processo. Não reidentifique, não coloque em URL, não envie a serviço externo além da API da
   Anthropic, e minimize o que vai em prompt — mande agregados e amostras, não a base inteira.
4. **Escreva o código para quem vai herdá-lo.** O critério "engenharia" é julgado por banca técnica
   separada e mede explicitamente se **outra pessoa da secretaria consegue dar continuidade**.
   README em português, sem dependência de conta pessoal, licença aberta.
5. **Commit cedo, commit sempre** — mas só quando o usuário pedir.

### Requisitos de entrega (valem nota)

- **Repositório GitHub público.** Vale o **último commit até as 16h30**.
- **O GitHub não é a entrega.** É preciso **uma aplicação publicada e acessível** ou um **vídeo de
  até 5 minutos** com captura de tela. Jurados avaliam ~40 projetos em uma hora — se não der para
  entender em minutos, não é avaliado.
- **Todo time deve preparar o pitch**: 6 min + 6 min de Q&A, corte rígido. Os 5 finalistas só são
  anunciados às 17h30.
- **Créditos de API são finitos.** US$ 100 na conta `platform.claude.com` somem em um dia se usados
  sem critério no modelo mais caro. Use `claude-haiku-4-5-20251001` ou `claude-sonnet-5` para volume
  e tarefas simples; reserve `claude-opus-5` para onde raciocínio realmente importa.

### Sobre o ambiente local do usuário

`sed` neste Mac é **GNU** (`gsed` por alias); todo o resto (`awk`, `date`, `stat`, `grep`, `find`,
`xargs`, `tar`) é **BSD**. Ver `~/dev/CLAUDE.md` para a tabela completa. Em scripts não interativos o
alias não vale — chame `gsed` explicitamente.

---

## 8. Perguntas em aberto para mentores e para a SME

O briefing já passou, mas estas respostas mudam a arquitetura. Vale perguntar à Gabriela ou aos
mentores durante o dia:

- A convocação pode ser **automatizada de ponta a ponta**, ou o diretor precisa permanecer no fluxo
  por exigência normativa?
- Os **3 dias** são regra legal ou convenção operacional? Podem encurtar se a resposta for digital
  e registrada?
- Existe base legal para **recusar uma vaga sem sair de todas as filas**?
- O **RMI** tem telefone atualizado (assistência social / saúde) que possa complementar o cadastro
  educacional? — seria o caminho mais curto para o ponto de quebra nº 4.
- Classificar **por CPF em vez de por opção** esbarra em alguma exigência dos órgãos reguladores?
- Qual o volume real de **vagas perdidas por falha de contato**? Está mensurado na base entregue?

---

## 9. O aviso que mais importa

> *"Todo mundo aqui poderia pegar tudo que a Gabi preparou, jogar no Claude e falar: se vira. Se
> fizerem isso, todo mundo vem com uma solução igual — e para isso a Gabi podia ter feito dentro da
> secretaria, porque eles usam Claude pra caramba lá. A razão de estarmos aqui é que esses modelos
> ainda precisam da criatividade da galera. Pensem fora da caixa."*
>
> — organização, no briefing

Vale para mim também. Quando eu propuser uma solução aqui, o piso é o óbvio; o valor está no que
o time acrescenta em cima. O escopo foi declarado **deliberadamente aberto**: soluções "em torno do
problema" são bem-vindas.
