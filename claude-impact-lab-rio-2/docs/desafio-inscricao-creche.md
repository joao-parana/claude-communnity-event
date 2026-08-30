# Desafio — Inscrição e acesso à creche (SME/Rio)

Transcrição organizada do briefing do **Claude Impact Lab Rio #2**, 30/08, 8h30–9h20.

- **Gabriela** (Speaker A) — Gerente de Sistemas e Dados, **Coordenadoria de Inovação e Tecnologia**,
  Secretaria Municipal de Educação do Rio de Janeiro. Apresenta o problema.
- **Speaker B** (organização/Anthropic) — critérios de avaliação e regras de entrega.

> **Sobre este documento.** É uma reorganização da transcrição bruta
> ([`trancricao-gab.md`](trancricao-gab.md)), com correções de erros evidentes de transcrição
> automática (ex.: "data label" → *Data Lake*, "Cade Lônico" → *CadÚnico*, "fila de pedra" →
> *fila de espera*, "modalidade crédito" → *modalidade creche*). O conteúdo e a ordem das ideias são
> da Gabriela. A **§8 é análise nossa**, não fala dela — está marcada como tal.

---

## 1. O problema em uma frase

O acesso à creche para crianças de **0 a 3 anos e 11 meses** no município do Rio: como planejar as
vagas, como organizar a inscrição e a classificação, e como convocar as famílias sem perder vagas
por falta de contato.

Creche **não é ensino obrigatório** — a partir dos 4 anos a SME garante o bairro imediato. É
justamente na creche que está a maior demanda reprimida, e por isso existe um processo de
**inscrição e classificação por pontuação**, e não alocação direta.

---

## 2. Escala

| Indicador | Valor |
| --- | --- |
| Alunos na educação infantil, modalidade creche | **~89.000** |
| Unidades de educação infantil (modalidade creche) | **~900** |
| Inscrições por ano (CPFs únicos) | **~45.000** |
| Registros na base de inscrição (por opção) | **> 100.000** — cada CPF gera até 5 |
| Coordenadorias Regionais de Educação (CREs) | **11** |
| Registro Municipal Integrado (RMI) | **> 12 milhões** de registros |
| Opções de unidade por inscrição | **1 a 5** (não obrigatórias) |
| Prazo para efetivar a matrícula após convocação | **3 dias** (+1 em caso atípico) |

---

## 3. A jornada atual do cidadão

1. **Inscrição** em [`matricula.rio`](https://matricula.rio) — site acessível por celular ou
   computador. **Há muito acesso por celular.**
2. **CPF da criança é obrigatório e validado na Receita Federal.** Garante qualidade do dado e
   impede duplicidade — só **uma inscrição ativa por CPF**. Inscrição errada só se corrige indo
   presencialmente a um polo de atendimento para excluir e refazer.
3. **Escolha de até 5 unidades.** O responsável digita o bairro e o sistema mostra as creches
   compatíveis com a **idade da criança** (os agrupamentos variam entre 0 e 3a11m).
4. **Comprovação de vulnerabilidade social — presencial, no dia seguinte.** O responsável leva
   documentação física (laudos, comprovantes) a **uma das cinco unidades escolhidas**. Três critérios
   pontuam hoje: **CadÚnico**, **Bolsa Família** e **Pequenos Cariocas**. Também pontuam deficiência
   e situação de violência.
5. **Dupla validação:** o **diretor confere manualmente** a documentação e registra sim/não no
   sistema; em paralelo, a SME cruza o CPF no **Data Lake** com a base da assistência social
   (**RMI** — o primeiro *data lake* público do mundo, da Prefeitura do Rio) e valida
   automaticamente CadÚnico, Bolsa Família e Pequenos Cariocas.
6. **Classificação**, com **publicação obrigatória em Diário Oficial**. A data é divulgada e
   responsáveis podem acompanhar presencialmente.
7. **Resultado no site.** Quem foi selecionado vai à unidade com a documentação de matrícula
   (identidade, CPF, caderneta de vacinação). Quem não foi entra na **fila de espera** e acompanha
   pelo site durante o ano inteiro.
8. **Convocação**, que corre o ano todo conforme vagas se abrem.

---

## 4. Os três eixos do desafio

A própria Gabriela dividiu o problema assim.

### Eixo 1 — Planejamento de vagas e oferta

Começa em **setembro**, para o ano seguinte, em três níveis: **nível central** (diretrizes e estudos)
→ **11 CREs** (territórios) → **microáreas** (clusters de unidades dentro de cada CRE, definidos com
o Instituto Pereira Passos).

Hoje o planejamento se ancora sobretudo na **demanda histórica da fila do ano anterior**, mais alunos
ativos e saídas. É uma capital com gente entrando e saindo o tempo todo, e cada território tem
desafios próprios.

> **Pergunta da Gabriela:** *"Será que a gente consegue antecipar de alguma forma algum dado, talvez,
> que a gente não esteja olhando, para estabelecer melhores métricas para esse planejamento?"*

O sintoma do desalinhamento: **o ano começa com vagas ociosas em algumas unidades e filas de espera
gigantes em outras — às vezes no mesmo território.**

### Eixo 2 — Inscrição e classificação

A regra estrutural: **a classificação é por opção, não por criança.**

Cada CPF vira até 5 registros na base, um por unidade escolhida. Uma mesma criança pode ser
classificada e convocada em até **5 filas simultâneas** — mas só pode ocupar uma vaga.

Não há **nenhum critério territorial** na escolha. Quem mora em Bangu pode escolher Campo Grande
(um parente) ou o Centro (o trabalho) — o que é legítimo, mas gera opções que podem se tornar
inviáveis quando a vida muda.

> **Pergunta da Gabriela:** *"Será que a gente consegue mudar um pouco essa lógica da inscrição e da
> classificação?"* E sugere um caminho: *"talvez já o referenciado, bairro versus [endereço do]
> responsável, oferecer talvez prioridade dessas inscrições."*

**A armadilha da oferta única.** Se a família recebe uma vaga que não quer mais — *"não consegui
aquele emprego"* — ela é obrigada a aceitar ou perde tudo: **sai de todas as filas de espera porque
já teve um oferecimento**. O resultado é perverso: o responsável se reinscreve, gerando ainda mais
demanda artificial na fila.

### Eixo 3 — Convocação  ⚠️ *o gargalo mais agudo*

**Manual, lento e oneroso.** Rodada a classificação, o **diretor** precisa: ver se há vaga, identificar
o próximo da fila, e convocar o responsável — por e-mail, telefone e WhatsApp — durante os 3 dias de
prazo. Tudo isso somado à gestão administrativa e pedagógica da unidade.

**O ponto de falha central — o contato desatualizado:**

> *"A gente tem um sistema em que esse telefone não se atualiza, o WhatsApp não atualiza. E uma coisa
> que a gente sofre muito é que as pessoas trocam de contato o tempo todo. A partir do momento que a
> gente roda uma classificação em janeiro, às vezes em fevereiro e março esse responsável já trocou
> de contato. E a gente não consegue [contato]."*

O sistema **não permite editar o contato nem tem campo de observação**. Quando o responsável aparece
na creche e dá um número novo, isso vive no *"caderninho"* do diretor — e depende de ele lembrar.

**Consequência direta: a criança perde a vaga.** *"Uma frustração gigante. Perdeu essa vaga, perde o
direito, e entra para o próximo da fila de espera."*

**O efeito cascata dos 3 dias.** Como a mesma criança pode estar em 5 filas, ao escolher uma unidade
as outras 4 ficam **bloqueadas esperando os 3 dias** correrem. Chama-se então o próximo — que pode
estar exatamente na mesma situação, somando mais 3 dias.

> *"Às vezes a gente demora mais de uma semana para conseguir alocar uma criança em uma vaga. Enquanto
> isso, a gente tem uma vaga ociosa sem uma criança para atender."*

**Restrição inegociável:** a ordem da fila de espera **tem que ser seguida e auditável** — há órgãos
reguladores acompanhando as bases de dados. Qualquer solução precisa preservar e evidenciar essa
ordem.

**Monitoramento hoje:** consultas manuais à base, relatórios consolidados enviados a diretores e CREs
para cobrar convocações pendentes.

---

## 5. Onde a lógica quebra — resumo

| # | Ponto de quebra | Efeito |
| --- | --- | --- |
| 1 | Escolha de 5 unidades **sem critério territorial** | Opções inviáveis; deslocamento irreal |
| 2 | Classificação **por opção, não por CPF** | 45 mil inscrições viram 100 mil registros; 5 filas por criança |
| 3 | Comprovação de vulnerabilidade **presencial** | Barreira justamente para quem tem menos mobilidade |
| 4 | **Contato desatualizado e não editável** | Vagas perdidas por falta de comunicação |
| 5 | Convocação **manual pelo diretor** | Carga sobre quem já gere a unidade |
| 6 | **3 dias por convocação**, em cascata entre 5 filas | > 1 semana para preencher uma vaga |
| 7 | **Oferta única** — recusou, sai de todas as filas | Reinscrição, demanda artificial inflada |
| 8 | Planejamento ancorado só em **demanda histórica** | Vagas ociosas e filas gigantes coexistindo |

---

## 6. Dados fornecidos

Base **real e anonimizada**, com dicionário de dados. Quatro tabelas principais:

| Conjunto | Conteúdo |
| --- | --- |
| **Inscrições por opção**, 2021–2025 | Um registro por opção de unidade, com situação: `confirmado`, `selecionado`, `cancelado` |
| **Respostas socioeconômicas** | Questionário sim/não, por ano. **O questionário mudou entre 2021 e 2025** |
| **Matriculados totais**, 2021–2025 | Unidades públicas e unidades parceiras |
| **Unidades escolares** | Repositório da rede com **latitude e longitude** — pronto para mapa |
| **Microáreas (IPP)** | Clusters territoriais dentro de cada CRE, produzidos pelo Instituto Pereira Passos |

### Anonimização — o que foi alterado e o que foi preservado

| Removido / generalizado | Preservado |
| --- | --- |
| Idade real das crianças e dos responsáveis | Sequência do processo |
| Endereço exato (só **bairro** e **CEP**) | Lógica da pontuação |
| Data de nascimento (só **ano** e **mês**) | Relações entre as quatro tabelas |
| | Dinâmica real de transição de estados |

> **Aviso do Speaker B:** *"São dados reais. Dados reais podem ter ruído."* Inspecione e limpe antes
> de concluir qualquer coisa.

---

## 7. Critérios de avaliação e regras de entrega

### Pontuação

| Peso | Critério | O que se avalia |
| --- | --- | --- |
| **🥇 Maior** | **Impacto real** | *"Dá para colocar amanhã na prefeitura e gerar valor?"* |
| | Produto | Experiência para o usuário final |
| | **Engenharia** | Facilidade de integrar aos sistemas atuais da prefeitura e de **outra pessoa da secretaria dar continuidade ao código**. Avaliado por banca técnica separada |
| | Ideia | Inovação pontua **mesmo sem execução perfeita** |
| | Apresentação | Como o time contou a história |

### Regras duras

- **GitHub público obrigatório.** Vale o **último commit até as 16h30** — commit das 16h31 não conta.
- **O GitHub não é a entrega.** A entrega é uma **aplicação publicada e acessível** ou um **vídeo de
  até 5 minutos** com captura de tela. (O README do desafio diz 60s; foi estendido para 5 min.)
- **~40 times competindo, apenas 5 apresentam.** Os finalistas só são anunciados às **17h30** —
  todo time deve estar preparado.
- **6 minutos de apresentação + 6 de Q&A**, corte rígido aos 6:00.
- Prêmio: **plano Max (US$ 200) por um mês** para cada membro do time vencedor.

### Avisos sobre os créditos

US$ 100 na conta da **API** (`platform.claude.com`), separada da assinatura. *"Parece muito. Não é."*
A conta de API consome rápido: usados de forma indiscriminada com o modelo mais caro, os créditos vão
embora em um dia. Use **Sonnet** para tarefas mais simples e reserve o modelo mais capaz para onde
raciocínio importa.

### O aviso mais importante

> *"Todo mundo aqui poderia pegar tudo que a Gabi preparou, jogar no Claude e falar: se vira. Se
> fizerem isso, todo mundo vem com uma solução igual — e para isso a Gabi podia ter feito dentro da
> secretaria, porque eles usam Claude pra caramba lá. A razão de estarmos aqui é que esses modelos
> ainda precisam da criatividade da galera. Pensem fora da caixa."*

O escopo é **deliberadamente aberto**: soluções "em torno do problema" são bem-vindas.

---

## 8. Análise: onde entra um app móvel

> ⚠️ **Esta seção é análise do time, não fala da Gabriela.** Ela não pediu um aplicativo. O que ela
> descreveu foi o *problema*; a escolha de resolvê-lo com app iOS/Android é decisão nossa e precisa
> se sustentar sozinha.

### O que sustenta a hipótese

O **Eixo 3** é o gargalo mais agudo e é, na raiz, um **problema de canal de comunicação com o
responsável**. Um app no celular do pai/mãe endereçaria diretamente:

- **Contato sempre atual** — o vínculo passa a ser a conta/dispositivo, não um número digitado uma vez
  em janeiro. Resolve a quebra nº 4.
- **Notificação push da convocação** — chega sem depender de o diretor ligar. Alivia a quebra nº 5.
- **Resposta imediata "aceito / não tenho mais interesse"** — se a família declina em horas, a vaga
  libera sem consumir os 3 dias. Ataca frontalmente a quebra nº 6.
- **Autoatualização de dados e interesse** ao longo do ano — reduz a demanda artificial da quebra nº 7.
- **Transparência da posição na fila**, com o registro de ordem preservado e auditável.

### O que precisa ser respondido antes de assumir o app como solução

1. **Fricção de instalação.** O público é justamente o de maior vulnerabilidade social. Baixar app,
   criar conta e manter espaço no aparelho é barreira real. **WhatsApp e SMS já estão no celular** —
   e a Gabriela citou os dois como canais já tentados. A pergunta honesta: *o problema é a ausência
   de um app, ou o fato de o cadastro de contato ser imutável?*
2. **A SME já tem canal digital.** `matricula.rio` é acessado por celular ("a gente tem muito acesso
   pelo celular") e já publica o resultado e a fila. Um app precisa entregar o que o site **não pode**
   — essencialmente, o **push** e a **resposta ativa**.
3. **Critério "engenharia" pesa integração.** Um app nativo iOS+Android exige contas nas lojas,
   ciclo de revisão, pipeline de build e manutenção de duas bases — tudo do lado da prefeitura,
   depois. Um **PWA** entrega push (Android bem; iOS 16.4+ com "adicionar à tela de início") sem loja
   nem instalação, e integra ao `matricula.rio` existente.
4. **"Colocar amanhã na prefeitura"** é o critério de maior peso. Um app em loja **não estreia
   amanhã**; uma camada de notificação sobre o fluxo atual, sim.

### Recomendação para a discussão do time

Trate o **canal** como decisão de arquitetura separada do **produto**. O núcleo de valor — detectar a
vaga, alcançar a família certa, capturar a resposta em horas e devolver a vaga ao fluxo — é o mesmo
seja o canal WhatsApp, SMS, PWA ou app nativo. Construa esse núcleo primeiro, com o canal atrás de
uma interface, e escolha a vitrine pela demo. Se o app for o rosto da solução, considere **PWA**:
mesma experiência mobile, zero fricção de instalação, e uma história de adoção muito mais crível
diante do critério de impacto real.

---

## 9. Perguntas em aberto para mentores/Gabriela

- A convocação pode ser **automatizada de ponta a ponta**, ou o diretor precisa permanecer no fluxo
  por exigência normativa?
- Os **3 dias** são regra legal ou convenção operacional? Podem ser reduzidos se a resposta for
  digital e registrada?
- Existe base legal para **recusar uma vaga sem sair de todas as filas**?
- O **RMI** tem telefone atualizado da assistência social/saúde que possa complementar o cadastro
  educacional?
- A classificação **por CPF em vez de por opção** esbarra em alguma exigência dos órgãos reguladores?
- Qual o volume real de **vagas perdidas por falha de contato**? Está mensurado na base?
