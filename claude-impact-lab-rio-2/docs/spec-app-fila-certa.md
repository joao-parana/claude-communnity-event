# Fila Certa — especificação do app (PWA, iOS e Android)

Especificação funcional do aplicativo para o **responsável** (pai/mãe) da criança inscrita na
Inscrição Creche da SME-Rio.

> **Arquitetura decidida:** **PWA** com **camada de notificação de múltiplos canais em cascata** —
> push para quem instalou, WhatsApp/SMS para todo mundo, e **registro de qual tentativa alcançou a
> família**, que é o que hoje não existe e torna o fluxo não-rastreável. Ver **§4**.

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

### ⚠️ Não existe app da SME nas lojas — verificado

A página oficial da SME ([`/app-rioeduca/`](https://educacao.prefeitura.rio/app-rioeduca/)) ainda
anuncia *"Baixe agora mesmo o aplicativo!"* e o briefing menciona inscrição *"pelo app Rioeduca em
Casa"*. **Os dois links estão mortos** (verificado em 30/08/2026):

| Verificação | Resultado |
| --- | --- |
| `apps.apple.com/br/app/rioeduca-em-casa/id1554165839` | **HTTP 404** |
| iTunes Lookup API, id 1554165839 | `resultCount: 0` |
| Busca "rioeduca" na App Store BR | **0 resultados** |
| `play.google.com/store/apps/details?id=tv.ip.rioeduca` | **HTTP 404** |

O app foi lançado em 2021 para ensino remoto na pandemia e **removido de ambas as lojas** desde
então. A documentação da SME não acompanhou.

**Quem publica app municipal no Rio é a IPLANRIO**, não a SME. Apps ativos hoje:

| App | Autor | Última atualização |
| --- | --- | --- |
| **MinhaSaúde.Rio** | IPLANRIO | **jun/2026** — ativo |
| 1746 Rio | IPLANRIO | dez/2023 |
| Zap Carioca | IPLANRIO | 2016 — abandonado na prática |

**O que isso muda na proposta:**

- ❌ **Não dá para propor "módulo dentro do Rioeduca em Casa"** — o app não existe mais.
- ✅ **O precedente institucional é o `MinhaSaúde.Rio`**: app municipal, por domínio específico, de
  comunicação com o cidadão, mantido pela IPLANRIO e atualizado este ano. É o análogo exato do que
  o Fila Certa seria para creche — e o argumento mais forte de viabilidade na apresentação.
- ⚠️ **Publicar app novo depende da IPLANRIO, não da SME.** Isso reintroduz a objeção original com
  força: um app em loja **não estreia amanhã**, e o critério de maior peso é exatamente *"dá para
  colocar amanhã na prefeitura?"*. **PWA volta a ser a recomendação** — entrega push (Android bem;
  iOS 16.4+ via "adicionar à tela de início") sem depender de loja nem de terceiro para publicar,
  e integra ao `matricula.rio`, que já é acessado majoritariamente por celular.
- 💡 **Que o Rioeduca em Casa tenha morrido é argumento, não constrangimento.** Um app que exige
  instalação para uma função sazonal tende a ser desinstalado; uma camada web vinculada ao portal
  que a família já usa, não. Vale dizer isso na apresentação.
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
SMS; a família tem **3 dias úteis** para comparecer.

O app **não substitui** esse protocolo — ele o **automatiza e registra**, via a cascata de canais
descrita em **§4.3**. Esta tela é a ponta visível dela: o push é o primeiro degrau, e o único que
não depende de o telefone estar atualizado.

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

| 4 | **Registro de tentativas de contato** | ❌ **Não existe em lugar nenhum** — é o que a cascata (§4.3) cria |

**Três lacunas estruturais** — contato do responsável, *timestamp* de mudança de status e registro
de tentativas de contato — são justamente o que o app precisa que o sistema passe a registrar. Não
são falha da base: são **a proposta**. Diga isso na apresentação em vez de escondê-las.

---

## 4. Decisão de arquitetura: PWA + notificação em cascata

**Decidido.** O Fila Certa é um **PWA** (Progressive Web App), com uma **camada de notificação de
múltiplos canais em cascata**.

### 4.1 Por que PWA e não app nativo

| Critério | PWA | App nativo |
| --- | --- | --- |
| Estreia "amanhã" na prefeitura | ✅ é uma URL | ❌ depende da IPLANRIO publicar |
| Push em Android | ✅ pleno, sem instalar nada | ✅ |
| Push em iOS | ⚠️ exige "Adicionar à Tela de Início" | ✅ |
| **Demonstrar push no hackathon** | ✅ FCM grátis | ❌ **iOS exige conta paga (US$ 99)** |
| Toolchain necessária | Node, já instalado | Xcode + Android Studio, **ausentes** |
| Integra ao `matricula.rio` | ✅ mesmo domínio possível | ❌ |
| Custo de manutenção para a SME | uma base | duas + duas lojas |

Três fatos decidiram:

1. **Não existe app da SME nas lojas** (§1) — o `Rioeduca em Casa` saiu do ar. Não há onde encaixar
   um módulo, e publicar app novo põe a IPLANRIO no caminho crítico.
2. **Push no iOS exige conta paga de developer.** Com Apple ID gratuito a capability de Push
   Notifications não fica disponível — demonstraríamos o app inteiro *exceto* a tela que é a
   proposta.
3. **O critério de maior peso é Impacto Real (×8)**, e a pergunta é *"a prefeitura usaria isso
   amanhã?"*. Uma URL usa-se amanhã; um binário em fila de revisão, não.

### 4.2 O que o push entrega em cada plataforma

| | Android / Chrome | iOS / Safari |
| --- | --- | --- |
| Web Push | ✅ sem ressalvas | ✅ desde iOS 16.4 (mar/2023) |
| Exige instalação para receber push | ❌ funciona em aba | ⚠️ **sim — "Adicionar à Tela de Início"** |
| Push com o app fechado | ✅ | ✅ |
| Push silencioso / wake em background | ✅ | ❌ não existe |

No iOS uma aba do Safari **não recebe push**, não há prompt automático de instalação, e se o link
abrir dentro de um *webview* (o navegador interno do WhatsApp — justamente por onde a convocação
chegaria) a opção de instalar some ou degrada. O iOS 26 passou a abrir como web app todo site
adicionado à tela de início, e o Safari 18.4 trouxe Declarative Web Push; ainda assim, estima-se que
o alcance de push via PWA no iOS seja **10 a 15× menor** que o de app nativo, pelo funil de
instalação manual.

Como o parque brasileiro — e mais ainda o do público em vulnerabilidade social que a Inscrição
Creche prioriza — é majoritariamente Android, **a maior parte das famílias tem push pleno sem
instalar nada**. Mas isso não basta, e daí a cascata.

### 4.3 A camada de notificação em cascata

**Push nunca é o canal único.** O protocolo oficial da SME já obriga **no mínimo 1 tentativa por
dia, durante 3 dias consecutivos, em horários diferentes**, por telefone, e-mail, WhatsApp ou SMS.
A proposta não substitui isso — organiza, automatiza e **registra**.

```
Vaga aberta para a criança X
        │
        ├─ 1. PUSH        → quem instalou o PWA. Chega em segundos, custo zero.
        │                    Não depende de o telefone estar atualizado.  ◄── resolve a causa-raiz
        │
        ├─ 2. WHATSAPP    → todo mundo com número registrado. Canal que a família já usa.
        │
        ├─ 3. SMS         → alcança aparelho sem internet e sem WhatsApp.
        │
        └─ 4. E-MAIL      → registro formal, complementar.
                 │
                 ▼
        REGISTRO DE CADA TENTATIVA
        canal · timestamp · status de entrega · houve resposta?
```

**A cascata é escalonada, não simultânea.** Push primeiro (instantâneo e gratuito); se não houver
leitura nem resposta dentro da janela, escala para WhatsApp, depois SMS. Isso respeita a regra de
1 tentativa/dia por 3 dias e para de escalar assim que a família responde.

**O terceiro elemento é o que não existe hoje e é o coração da proposta:** o **registro de qual
tentativa alcançou a família**. Hoje a convocação é manual e não deixa rastro — ninguém sabe se a
escola ligou, se o número tocou, se a mensagem foi entregue, nem quando a opção mudou para
"Selecionado". O briefing confirma essa lacuna textualmente. Sem esse registro:

- a família não sabe seu prazo;
- a equipe da unidade não sabe o que já foi tentado;
- a CRE não consegue cobrar, só pedir relatório;
- **e ninguém consegue provar que o protocolo dos 3 dias foi cumprido** — o que importa porque a
  fila é auditada por órgãos reguladores.

Com o registro, cada convocação vira uma trilha auditável, o painel da prefeitura ganha o sinal
para alertar vaga ociosa em risco **antes** de virar ociosidade, e a métrica de impacto (§6) passa a
ser mensurável de verdade.

### 4.4 Por que isso enfraquece o argumento pró-nativo

O único ganho real do app nativo seria push mais confiável no iOS. Mas o canal que resolve o
problema para a maioria — **WhatsApp/SMS** — precisa existir em qualquer arquitetura, inclusive na
nativa. Ou seja: o nativo custa toolchain, conta paga, duas bases de código e a IPLANRIO no caminho
crítico, para melhorar apenas o primeiro degrau da cascata, na plataforma minoritária do público-alvo.

### 4.5 Demais decisões

| Decisão | Estado | Nota |
| --- | --- | --- |
| **Canal** | ✅ **decidido: PWA + cascata** | — |
| **Autenticação** | ⬜ aberta | O mockup entra só com CPF; a proposta precisa de 2º fator ou gov.br |
| **Geocodificação** | ✅ `CEP` → lat/lon | `CEP` tem 0% de nulo; `bairro` é texto livre e inútil. Ver [`README.md`](../README.md) §7 |
| **Provedor de WhatsApp** | ⬜ aberta | WhatsApp Business API exige *templates* aprovados e número oficial — na demo, mockar |

⚠️ **Para a demo:** push via **FCM no Android** funciona de graça e sem conta de developer — é o
único degrau da cascata demonstrável ao vivo hoje. WhatsApp e SMS devem ser **simulados**, com o
registro de tentativas visível na tela. Mostrar a trilha de auditoria vale mais que enviar a
mensagem de verdade.

### Sobre o design do mockup

Paleta institucional sóbria (`--navy #153450`, papel `#EDEAE1`), Archivo + Inter + IBM Plex Mono,
ícones Tabler. Estados semânticos consistentes: âmbar = espera, verde = confirmado/viável,
vermelho = risco/lotada, tijolo = pendente. **Mantenha esse sistema** — ele passa credibilidade de
serviço público, e reescrevê-lo custa tempo que a demo não tem.

⚠️ O mockup carrega fontes e ícones de CDN. **Se for publicá-lo como artefato ou rodá-lo offline na
apresentação, embuta os assets** — a rede do evento é instável.

---

## 5. Pendências do mockup

Mencionadas na sessão de planejamento, ainda **não desenhadas**:

- **Fluxo de atualização de contato.** O botão existe no alerta da tela 2; a tela em si não. É a
  correção do ponto de quebra nº 4 — a tela mais importante que falta.
- **Fallback SMS / offline** para a notificação de convocação. O protocolo oficial já obriga
  telefone, e-mail, WhatsApp ou SMS; o app não pode ser o único canal.

### O login por CPF não funciona contra esta base

`aluno_anon` e `responsavel_anon` são **chaves derivadas**, não CPFs. A anonimização suprimiu os
identificadores diretos. Consequência prática:

- **Na demo:** simule o vínculo CPF → inscrição com um mapeamento fixo sobre os códigos anonimizados.
- **Na proposta:** o login real exige integração com o sistema vivo da SME. Declare isso como
  requisito de integração, não o esconda.

---

## 6. Como medir o impacto

A métrica está nos dados e é defensável perante a banca:

> **11,0% das crianças chamadas em 2025 nunca confirmaram a matrícula** — 5.994 crianças. Em 2021
> eram 26,1%.

O pitch fica direto: *quanto desses 11% o Fila Certa recupera?* Toda tela deve poder ser explicada
como uma redução desse número, ou como redução do tempo de ciclo da convocação (hoje > 1 semana por
vaga, pelo efeito cascata dos 3 dias).

**A cascata torna isso mensurável pela primeira vez.** Hoje não se sabe *por que* uma família não
respondeu — se o telefone estava errado, se a mensagem não chegou, ou se ela desistiu. Com canal,
timestamp e status de entrega por tentativa, a SME passa a distinguir **falha de contato** de
**recusa real** — e essas duas exigem políticas opostas.
