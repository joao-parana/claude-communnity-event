# Roteiro — vídeo de 2 minutos

**Projeto:** Fila Certa · Painel de Gestão — Inscrição Creche SME-Rio
**Percurso:** Cidade → 4ª CRE (Bonsucesso) → Realocar → Enviar convocação
**Duração alvo:** 2min00 · captura de tela com narração

---

## Antes de gravar

```bash
uvicorn fila_certa.main:app --port 8000
```

- Navegador em **1440×900**, sem barra de favoritos, aba única.
- Deixe as três URLs abertas em abas ocultas ou digite direto — o percurso é:
  1. `http://127.0.0.1:8000/`
  2. `http://127.0.0.1:8000/cre/4?foco=430603`
  3. `http://127.0.0.1:8000/realocar/430603/4016`
- **Zere o banco antes** para a convocação sair como `#1`:
  `rm -f /tmp/fila_certa.db` e reinicie o servidor.
- Navegue **clicando**, não digitando URL: o vídeo precisa mostrar que nada recarrega.

---

## Cena 1 — A cidade inteira (0:00 – 0:35)

**Tela:** `/` · página inicial

**Quem está olhando:** *Cláudia, gerente na Coordenadoria de Inovação e Tecnologia da SME.*
É ela quem responde, no nível central, por que existem filas e vagas ociosas ao mesmo tempo — e
quem precisa levar isso para as 11 coordenadorias no planejamento de setembro.

**Ação na tela:** abrir em `/`. Pausa de 2s na faixa escura. Depois passar o cursor devagar pela
lista de bairros, de cima para baixo.

> **Narração**
>
> "Este é o painel de gestão da Inscrição Creche do Rio. A primeira coisa que a gerente da SME vê
> não é uma lista de problemas — é uma oportunidade medida.
>
> Quinze mil e trezentas crianças estão numa fila de espera a menos de três quilômetros de uma
> creche com vaga aberta. Duas mil seiscentas e vinte delas cabem, hoje, nas vagas que já estão
> contratadas e ociosas. Sem obra, sem concurso, sem verba nova.
>
> A barra clara é a fila do bairro. A escura, quantas dessas crianças caberiam nas creches parceiras
> ao redor. Onde a barra escura quase some — Jacarepaguá, com dois mil e oitocentos esperando e
> cobertura de sete por cento — realocar não resolve: ali falta oferta de verdade.
>
> Mas olhe o quarto da lista."

**Ação:** cursor pousa na linha **Bonsucesso** (barra verde visivelmente longa, 61%).

> "Bonsucesso: setecentas e quatro crianças na fila, quatrocentas e trinta e uma vagas ao redor.
> Sessenta e um por cento de cobertura. Aqui a fila e a vaga estão a poucos quarteirões uma da outra."

---

## Cena 2 — O território (0:35 – 1:10)

**Tela:** `/cre/4?foco=430603` · chegando pelo clique em **4ª** na linha de Bonsucesso

**Quem está olhando:** *Marcelo, da equipe de matrícula da 4ª CRE.*
Ele conhece cada unidade pelo nome e é quem cobra as convocações das direções. O mapa é o
instrumento dele.

**Ação:** clicar no `4ª` ao lado de Bonsucesso. Enquanto a tela troca, apontar que a barra de
endereço mudou **sem recarregar**. Deixar o mapa respirar 3s.

> **Narração**
>
> "Um clique leva à 4ª CRE — e repare que a página não recarrega. Cada tela continua sendo um
> endereço que se compartilha por e-mail.
>
> Aqui o território aparece como ele é. Os círculos vermelhos são unidades com fila; o número dentro
> é quantas crianças esperam. Os verdes são creches parceiras com vaga ociosa. As posições são as
> coordenadas reais das unidades.
>
> Mil setecentas e oitenta e cinco crianças esperando nesta coordenadoria. Novecentas e setenta e
> cinco vagas ociosas a três quilômetros. Cobertura de cinquenta e cinco por cento — mais da metade
> da fila caberia no que já existe."

**Ação:** clicar no círculo vermelho maior (**214**, canto inferior direito do mapa). O painel à
direita troca.

> "A Creche Municipal Tio Mário, em Bonsucesso, tem duzentas e quatorze crianças na fila. E cento e
> vinte vagas ociosas em seis creches parceiras num raio de três quilômetros.
>
> A primeira da lista está a mil e duzentos metros: a Creche Lar Irmão Francisco, em Manguinhos,
> com oito vagas de Maternal — meta contratada com a prefeitura, não estimativa."

---

## Cena 3 — A decisão (1:10 – 1:45)

**Tela:** `/realocar/430603/4016`

**Quem está olhando:** *Marcelo ainda, agora decidindo. Do outro lado da mesa, a direção da unidade.*
Hoje esta etapa é o caderninho do diretor e três dias de ligações.

**Ação:** clicar em **Realocar →** na primeira linha. Pausar na coluna da esquerda.

> **Narração**
>
> "À esquerda, a fila na ordem da classificação publicada em Diário Oficial. Não é reordenável — a
> ordem é auditada por órgãos de controle, e o painel a preserva.
>
> A primeira criança tem setenta e seis pontos, CadÚnico confirmado, sete meses de espera, e precisa
> de Maternal I. A creche de destino tem cinco vagas de Maternal I. São compatíveis."

**Ação:** cursor desce até o aviso âmbar.

> "E aqui está uma mudança de política que o painel torna possível: recusar esta vaga não retira a
> criança das outras filas. Hoje, aceitar uma oferta encerra a inscrição inteira — por isso tantas
> famílias somem. Isso depende de validação jurídica da SME, e está marcado como tal."

**Ação:** cursor na faixa dos quatro canais.

> "A convocação não sai por um canal só. Push no aplicativo da família, imediato. WhatsApp em quatro
> horas se ninguém abrir. SMS no segundo dia. Ligação da unidade no terceiro. É o protocolo oficial
> da secretaria — um contato por dia, durante três dias — só que automatizado."

---

## Cena 4 — O registro (1:45 – 2:00)

**Tela:** mesma, após o envio

**Ação:** clicar em **Enviar convocação**. A trilha aparece **sem recarregar a página**. Segurar
3s no bloco verde.

> **Narração**
>
> "E este é o ponto. A convocação foi registrada, com prazo, e cada tentativa de contato tem canal,
> horário e resultado.
>
> Isso não existe hoje. Ninguém sabe se a escola ligou, se a mensagem chegou, nem quando a vaga foi
> oferecida. Sem esse registro, não se distingue uma família que recusou de uma família que nunca foi
> encontrada — e são problemas opostos.
>
> Com ele, a secretaria consegue provar que cumpriu o prazo de três dias. E uma criança de
> Bonsucesso entra numa creche a mil e duzentos metros de casa, numa vaga que já estava paga e vazia."

**Encerramento:** cortar direto no bloco verde. Sem cartela, sem logo animado.

---

## Números que aparecem na tela

| Onde | Valor | O que é |
| --- | ---: | --- |
| Cidade | 15.326 | crianças em fila com vaga a ≤ 3 km |
| Cidade | 3.346 | vagas ociosas ao alcance |
| Cidade | 2.620 | realocáveis sem repetir vaga |
| Bonsucesso | 704 / 431 · 61% | fila / vagas / cobertura |
| 4ª CRE | 1.785 / 975 · 55% | fila / vagas / cobertura |
| Tio Mário | 214 | crianças na fila |
| Lar Irmão Francisco | 8 vagas · 1,22 km | Maternal I (5) e II (3) |

---

## Cuidados de honestidade

Ditos ou visíveis no vídeo, para não prometer o que não existe:

- **A fila nominal é demonstração.** A extração é anonimizada e não traz pontuação individual por
  criança. Os códigos seguem o formato real da base. Se a narração ficar apertada, o rodapé da
  coluna já diz "códigos anonimizados".
- **Só o push sai de fato.** WhatsApp, SMS e ligação aparecem como `pendente` na trilha — exigem
  credencial de provedor. **Não afirme que as mensagens foram enviadas**; diga que a cascata foi
  registrada.
- **A recusa sem sair das filas muda a regra atual** e depende de validação jurídica. O aviso na
  tela diz isso; a narração repete.
- **Os dados são anonimizados por aleatorização, generalização e supressão.** A própria SME adverte
  que os indicadores não representam a realidade. Os padrões se sustentam; os absolutos são
  ilustrativos.

## Se sobrar tempo (versão de 3 min)

Inserir entre as cenas 2 e 3: voltar para `/`, abrir o menu **Coordenadorias** e mostrar as 11 CREs
com fila e vagas lado a lado — a 7ª com 3% de cobertura contra a 4ª com 55%. Deixa claro que o painel
separa "onde realocar resolve" de "onde falta creche", que são decisões orçamentárias diferentes.

---

## Vídeos gerados

| Arquivo | Duração | Áudio |
| --- | --- | --- |
| **`fila-certa-demo-narrado.mp4`** | 2min23 | ✅ narração sintetizada |
| `fila-certa-demo.mp4` | 2min00 | — mudo, para locutar por cima |

1920×1200, H.264. Nenhum dos dois é screencast: são sequências determinísticas de estados **reais**
da aplicação, navegados de verdade pelo Playwright (cliques e submit incluídos) e capturados em
retina. Não há cursor se movendo; cada cena tem um zoom lento para a imagem não ficar parada.

### A narração

Voz **Reed** (masculina, pt-BR, nativa do macOS) a 178 palavras por minuto, via `say`.
**A duração de cada cena vem do áudio, não o contrário** — `narracao.py` sintetiza, mede a fala com
`ffprobe` e grava `audio/plano.json`; `montar-narrado.sh` monta cada cena com o tempo exato da fala
mais 0,9 s de respiro. Trocar uma frase reajusta a imagem sozinho.

Outras vozes masculinas pt-BR disponíveis nesta máquina: `Eddy`, `Grandpa`, `Rocko`.
Para trocar: `python narracao.py Rocko && ./montar-narrado.sh`.

### Marcações

| Tempo | Cena |
| --- | --- |
| 0:00 | Cidade — a oportunidade medida |
| 0:11 | Bonsucesso — 61% de cobertura |
| 0:33 | 4ª CRE — chega sem recarregar |
| 0:44 | O território no mapa |
| 1:02 | Tio Mário e a vaga a 1,22 km |
| 1:17 | A fila e a compatibilidade |
| 1:34 | O aviso — não sai das outras filas |
| 1:49 | A cascata de quatro canais |
| 2:04 | A trilha registrada |

### Refazer

```bash
uvicorn fila_certa.main:app --port 8000   # servidor no ar
rm -f /tmp/fila_certa.db                  # convocação sai como #1
python video/gravar.py                    # captura os 9 quadros
python video/narracao.py Reed             # sintetiza e mede a narração
./video/montar-narrado.sh                 # monta o vídeo com voz
./video/montar.sh                         # (opcional) versão muda de 2min
```

Os textos da narração estão em `narracao.py`, um por cena — é lá que se edita a fala.

### Se quiser um screencast de verdade

Com cursor e cliques visíveis, grave você mesmo — **Cmd+Shift+5** no macOS, ou QuickTime →
*Gravar Tela*. Eu não consigo: o `screencapture` aqui está sem permissão de Gravação de Tela, e
mesmo com ela capturaria a janela do Claude Code em volta. As cenas acima já trazem as ações de
cursor.
