# Fila Certa — especificação do app (iOS e Android)

Especificação funcional do aplicativo para o **responsável** (pai/mãe) da criança inscrita na
Inscrição Creche da SME-Rio.

**Mockup de referência:** [`mockup_fila_certa_v1.html`](mockup_fila_certa_v1.html) — 6 telas, abrir
no navegador. O mockup é a definição visual e de conteúdo; este documento formaliza o
comportamento, as fontes de dado e as regras.

---

## 1. Posicionamento

> *"A inscrição continua sendo feita no site oficial matricula.rio — o app só acompanha e facilita o
> que vem depois: contato, documentos e convocação."*
> — subtítulo do próprio mockup

Isso é a decisão de produto mais importante da spec. O Fila Certa **não** reimplementa a inscrição.
Ele cobre a lacuna entre *inscrever-se* e *ocupar a vaga* — que é exatamente onde o processo perde
crianças.

**Vínculo por CPF do responsável, sem cadastro novo.** O mesmo CPF já validado na Receita Federal
durante a inscrição no `matricula.rio` é a chave de entrada. Nenhum dado é redigitado.

### ⚠️ Já existe um app oficial: `Rioeduca em Casa`

O briefing da SME diz, textualmente, que a inscrição pode ser feita *"pelo portal matricula.rio **ou
pelo app Rioeduca em Casa**"*. Esse app já está publicado nas duas lojas:

- **Android:** `tv.ip.rioeduca` — https://play.google.com/store/apps/details?id=tv.ip.rioeduca
- **iOS:** https://apps.apple.com/br/app/rioeduca-em-casa/id1554165839
- Gratuito e, segundo a prefeitura, **não consome o plano de dados** do usuário.

**Consequência para a arquitetura:** o Fila Certa tem muito mais chance de ser adotado como
**módulo dentro do Rioeduca em Casa** do que como app novo em loja separada. Isso elimina a fricção
de instalação — a maior objeção contra a hipótese de app — e conversa direto com o critério de
avaliação de maior peso (*"dá para colocar amanhã na prefeitura?"*). Trate o app autônomo do mockup
como **a vitrine da demo**, e o módulo integrado como **a proposta de adoção**.

---

## 2. As 6 telas e o que cada uma resolve

Cada tela é rastreada ao ponto de quebra que ataca (numeração de
[`desafio-inscricao-creche.md`](desafio-inscricao-creche.md) §5).

| # | Tela | Ataca | Como |
| --- | --- | --- | --- |
| 1 | **Consultar inscrição** | — | Entrada por CPF, sem conta nova. Reduz abandono no onboarding |
| 2 | **Painel da inscrição** | **4, 1, 7** | Alerta de contato desatualizado; selo de viabilidade por distância; oferta de vaga próxima fora das 5 escolhas |
| 3 | **Documentos** | **3** | Envio pelo celular substitui a ida presencial; pré-checagem por IA |
| 4 | **Convocação** | **4, 5, 6** | Push + prazo visível + confirmação em um toque |
| 5 | **Sugestões perto de você** | **1, 8** | Unidades fora das 5 escolhas, ordenadas por distância |
| 6 | **Entenda sua pontuação** | **2** | Transparência da régua e do porquê de cada critério |

### Tela 1 — Consultar inscrição

Campo único de CPF do responsável. Sem senha, sem cadastro. Link discreto para o `matricula.rio`
para quem ainda não se inscreveu. Aviso explícito de que o app **não substitui nem duplica** a
inscrição oficial.

> **Questão em aberto — autenticação.** O mockup mostra consulta só por CPF. Isso expõe dados de uma
> criança a quem souber o CPF do responsável. Antes de implementar de verdade: exigir segundo fator
> (data de nascimento da criança, ou OTP por SMS), ou integrar ao **gov.br** / Carioca Digital.
> Para a demo, CPF basta; para a proposta, não.

### Tela 2 — Painel da inscrição

O coração do app.

- **Cabeçalho da criança** — nome, idade, protocolo.
- **Alerta de contato desatualizado** — *"Seu telefone está desatualizado desde janeiro. Se sua vaga
  sair, é por aqui que avisamos."* Botão de atualização direta. **É a correção do ponto de quebra
  nº 4**, que hoje é impossível: o sistema não tem campo editável nem observação.
- **As 5 escolhas com selo de viabilidade** — `Alta viabilidade` / `Lista de espera` /
  `Risco de distância`, com a distância em km. O mockup é explícito: o selo é *"puxado do histórico
  do bairro, não uma opinião do app"*.
- **Oferta de vaga próxima fora das 5 escolhas** — *"Não era uma das suas 5 escolhas, mas fica mais
  perto e tem vaga agora."* Dois botões: **Tenho interesse** / **Agora não**.

> **O botão "Agora não" é a peça mais valiosa da spec.** Capturar declínio em horas é o que libera
> a vaga sem consumir os 3 dias de convocação — ataca o efeito cascata (nº 6). Hoje só existe o
> silêncio, e o silêncio custa 3 dias por elo da fila.

### Tela 3 — Documentos

Três estados por documento: `Confirmado` (validado automaticamente via Data Lake/RMI),
`Em análise` (enviado, aguardando a unidade), `Pendente`.

Upload por foto do celular. Selo *"Pré-checagem automática em minutos"*.

> **Limite deliberado, e correto:** a IA faz **pré-checagem**, a **unidade confirma no sistema, como
> já é hoje**. Não se propõe substituir a validação humana — o que preserva a auditabilidade exigida
> pelos órgãos reguladores e torna a proposta aceitável para a SME.

Justificativa nos dados: apenas ~8% das declarações "Sim" de vulnerabilidade aparecem validadas
(2022–2025), contra 89% em 2021 — ver [`README.md`](../README.md) §4. Se esse funil for real, é
onde mais se perde pontuação legítima.

### Tela 4 — Convocação

- **Contagem regressiva** — *"2 dias e 14h restantes"*. Hoje o briefing registra que **não há
  visibilidade de prazo**: nem família nem equipe sabem há quanto tempo uma opção está "Selecionada".
- **Botão único: Confirmar vaga agora.**
- **Linha do tempo** do processo — inscrição registrada → CadÚnico confirmado → convocado.

**Regra oficial a respeitar** (do briefing): quando a vaga abre, a escola faz **no mínimo 1 tentativa
por dia, durante 3 dias consecutivos, em horários diferentes**, por telefone, e-mail, WhatsApp ou
SMS; a família tem **3 dias úteis** para comparecer. O app **não substitui** esse protocolo — ele o
complementa com um canal que não depende de número de telefone e **registra a tentativa e a
resposta**, tornando o fluxo rastreável.

### Tela 5 — Sugestões perto de você

Unidades fora das 5 escolhas, por distância. **A distinção de confiança do dado é exemplar e deve
ser preservada:**

| Origem | Rótulo | Base |
| --- | --- | --- |
| Rede parceira | `1 vaga` | *"vaga confirmada pela meta contratada"* — dado firme |
| Rede direta | `Provável vaga` | *"estimativa por baixa procura na região, **não é capacidade oficial**"* |
| Qualquer | `Lotada` | — |

Nunca prometa vaga que não se pode garantir. Um app da prefeitura que erra isso queima a confiança
da família e a credibilidade da SME.

### Tela 6 — Entenda sua pontuação

- **Pontuação com régua comparativa** — "76 pontos", com marcador do *"mínimo confirmado na CM Bento
  Ribeiro"* (60). Responde a pergunta que o número sozinho não responde: **isso é alto?**
- **Por que os critérios existem** — *"A lei municipal manda priorizar quem tem mais vulnerabilidade
  social, pra reduzir desigualdade no acesso à creche."*
- **Decomposição** — CadÚnico +51, Educação especial +25, Bolsa Família +0 (não informado).
- **Nota histórica** — *"Em 2024, Educação especial valia 25 pontos; até 2023 valia 100."*

Os pesos batem com a régua real de 2025 extraída da `03_QueryC` (ver [`README.md`](../README.md) §5).
**Ao implementar, leia a régua da tabela por ano — não a fixe em código.** Ela muda a cada processo.

---

## 3. Fontes de dado por tela

| Tela | Precisa de | Existe na base do desafio? |
| --- | --- | --- |
| 1 | CPF → inscrição | Sim (`prm_id`,`plm_id`,`ipl_id`; CPF é o `responsavel_anon`) |
| 2 | Situação por opção | Sim (`situacao`) |
| 2, 5 | Distância casa ↔ unidade | **Derivável**: `CEP` do responsável + lat/lon da unidade (`Unidades_Unificadas_com_Localizacao.xlsx`) |
| 2 | Selo de viabilidade | **Derivável** do histórico 2021–2025 por unidade |
| 2 | Contato do responsável | ❌ **Não está na base** (suprimido na anonimização) — mockar |
| 3 | Estado dos documentos | Parcial (`confirmado` na `02_QueryB`) |
| 4 | Prazo restante | ❌ **Não existe** — o briefing confirma que não há registro de mudança de status. **Mockar e propor** |
| 5 | Vagas abertas | Parcial (`OferecimentosEvagas/`, meta das parceiras) |
| 6 | Pontuação e régua | Sim (`03_QueryC` + `02_QueryB`) |

**Duas lacunas estruturais** — contato do responsável e *timestamp* de mudança de status — são
justamente o que o app precisa que o sistema passe a registrar. Não são falha da base: são **a
proposta**. Diga isso na apresentação em vez de escondê-las.

---

## 4. Decisões técnicas em aberto

| Decisão | Opções | Nota |
| --- | --- | --- |
| **Canal** | Módulo no `Rioeduca em Casa` · PWA · app nativo novo | Módulo tem a melhor história de adoção; PWA é o melhor meio-termo para a demo |
| **Autenticação** | CPF simples · CPF + 2º fator · gov.br | O mockup mostra o primeiro; a proposta precisa do segundo |
| **Push** | FCM/APNs · WhatsApp Business API · SMS | Não escolha um só — a família que não instala o app precisa continuar sendo alcançada |
| **Geocodificação** | CEP → lat/lon | `CEP` tem **0% de nulo** na base; `bairro` é texto livre e inútil. Ver [`README.md`](../README.md) §7 |

### Sobre o design do mockup

Paleta institucional sóbria (`--navy #153450`, papel `#EDEAE1`), Archivo + Inter + IBM Plex Mono,
ícones Tabler. Estados semânticos consistentes: âmbar = espera, verde = confirmado/viável,
vermelho = risco/lotada, tijolo = pendente. **Mantenha esse sistema** — ele passa credibilidade de
serviço público, e reescrevê-lo custa tempo que a demo não tem.

⚠️ O mockup carrega fontes e ícones de CDN. **Se for publicá-lo como artefato ou rodá-lo offline na
apresentação, embuta os assets** — a rede do evento é instável.

---

## 5. Como medir o impacto

A métrica está nos dados e é defensável perante a banca:

> **11,0% das crianças chamadas em 2025 nunca confirmaram a matrícula** — 5.994 crianças. Em 2021
> eram 26,1%.

O pitch fica direto: *quanto desses 11% o Fila Certa recupera?* Toda tela deve poder ser explicada
como uma redução desse número, ou como redução do tempo de ciclo da convocação (hoje > 1 semana por
vaga, pelo efeito cascata dos 3 dias).
