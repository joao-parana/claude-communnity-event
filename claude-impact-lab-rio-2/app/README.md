# Fila Certa — PWA

Aplicação do responsável (pai/mãe) para a Inscrição Creche da SME-Rio.
Especificação em [`../docs/spec-app-fila-certa.md`](../docs/spec-app-fila-certa.md).

**Stack:** FastAPI (Python) + Vite com JS vanilla. Sem framework de UI — o
[mockup](../docs/mockup_fila_certa_v1.html) é HTML/CSS puro e entra quase direto.

---

## Estrutura

```
app/
├── backend/                          FastAPI
│   ├── pyproject.toml
│   ├── src/fila_certa/
│   │   ├── main.py                   cria o app, monta rotas, serve o front buildado
│   │   ├── config.py                 settings via env (pydantic-settings)
│   │   │
│   │   ├── api/v1/                   ── camada de interface ──
│   │   │                             rotas HTTP: validam entrada, chamam services,
│   │   │                             serializam saída. Nenhuma regra de negócio aqui.
│   │   │
│   │   ├── domain/                   ── regras de negócio, SEM I/O ──
│   │   │                             classificacao.py  régua de pontuação por ano
│   │   │                             cascata.py        política de escalonamento
│   │   │                             viabilidade.py    score de distância
│   │   │                             models.py         entidades (dataclasses)
│   │   │
│   │   ├── services/                 ── orquestração ──
│   │   │                             juntam domain + repositories + adapters
│   │   │
│   │   ├── adapters/                 ── canais de notificação (plugáveis) ──
│   │   │                             base.py  Protocol CanalNotificacao
│   │   │                             webpush.py · whatsapp.py · sms.py · email.py
│   │   │                             fake.py  registra sem enviar → demo sem credencial
│   │   │
│   │   ├── repositories/             ── acesso a dados ──
│   │   │                             duckdb_repo.py     lê as bases do desafio
│   │   │                             tentativas_repo.py grava o registro de contato
│   │   │
│   │   └── db/                       schema.sql + seed.py (dados para a demo)
│   └── tests/{unit,integration}/
│
├── frontend/                         Vite + JS vanilla
│   ├── index.html                    base derivada do mockup
│   ├── vite.config.js                vite-plugin-pwa (gera SW e manifest)
│   ├── public/
│   │   ├── manifest.webmanifest
│   │   └── icons/                    192/512 px — exigidos para instalar
│   └── src/
│       ├── main.js                   bootstrap, router simples
│       ├── sw.js                     service worker: push + cache offline
│       ├── pages/                    as 6 telas da spec
│       ├── components/               pedaços reutilizados (pill, card, timeline)
│       ├── styles/                   tokens do mockup (cores, tipografia)
│       └── lib/                      api.js · push.js · format.js
│
└── data/                             gerado em runtime — fora do versionamento
```

---

## Por que esta estrutura

### `domain/` não faz I/O

A régua de pontuação **muda a cada processo seletivo** (em 2025 o CadÚnico vale 51 pontos; até 2023
"deficiência da criança" valia 100 e hoje vale 25). Isso precisa ser **dado lido da `03_QueryC`**,
nunca constante em código. Isolar as regras num módulo sem I/O deixa isso testável sem banco e sem
rede — e é o que permite provar, na banca técnica, que o cálculo está certo.

### `adapters/` é o coração da proposta

A cascata de notificação (push → WhatsApp → SMS → e-mail) só funciona se cada canal for
intercambiável. Um `Protocol` em `base.py` e uma implementação por canal significa que:

- **`fake.py` permite demonstrar a cascata inteira sem nenhuma credencial** — registra a tentativa
  como se tivesse enviado. É assim que WhatsApp e SMS entram na apresentação.
- trocar provedor de SMS não toca em mais nada;
- a política de escalonamento (`domain/cascata.py`) não sabe qual canal está por baixo.

Na demo, só o **Web Push via FCM** roda de verdade — e de graça, sem conta de developer.

### `repositories/tentativas_repo.py` grava o que hoje não existe

Canal, horário, status de entrega, houve resposta. Essa tabela é a proposta: sem ela ninguém sabe se
a escola ligou, nem se prova que o protocolo dos 3 dias foi cumprido — e a fila é auditada por
órgãos reguladores.

### Backend serve o frontend buildado

`vite build` gera `frontend/dist/`, que o FastAPI monta com `StaticFiles`. Um processo, uma porta,
um `docker run`. Isso responde direto ao critério de maior peso: *"dá para colocar amanhã?"*.

### `src/` layout no backend

`src/fila_certa/` em vez de `fila_certa/` na raiz evita que imports funcionem por acidente (o
diretório de trabalho entrando no `sys.path`) e força instalar o pacote — o que faz o teste rodar
contra o que será distribuído, não contra a árvore de código.

---

## Primeiros passos

Os diretórios estão vazios com `.gitkeep`. Ao começar a escrever código:

1. **Backend** — remova os `.gitkeep` conforme criar arquivos e adicione `__init__.py` em cada
   pacote de `src/fila_certa/` (são necessários; não os criei para manter os diretórios vazios como
   pedido).
2. **Frontend** — `npm create vite@latest . -- --template vanilla` dentro de `frontend/`, depois
   `npm i -D vite-plugin-pwa`.
3. **Ícones** — `public/icons/` precisa de 192×192 e 512×512 PNG, senão o navegador não oferece
   instalar o PWA. É o passo mais fácil de esquecer e o que quebra a demo de push no iOS.

---

## Publicação

**Alvo: [Hugging Face Spaces](https://huggingface.co/new-space)** — SDK `docker`, porta `7860`.

Escolhido porque o Space gratuito **só dorme após 48 h de inatividade** (o Render free dorme em
15 min, com 30–60 s de cold start — fatal na janela em que os jurados abrem ~40 projetos). Além
disso: 2 vCPU / 16 GB, HTTPS automático, sem cartão de crédito, deploy por `git push`.
Fly.io e Koyeb encerraram o free tier em 2026; Railway virou trial de US$ 5.

### Passos

```bash
# 1. crie o Space em huggingface.co/new-space  →  SDK: Docker
# 2. o README.md do Space precisa do bloco YAML de metadados:
cp app/README_HF.md /caminho/do/space/README.md

# 3. copie o app e publique
git clone https://huggingface.co/spaces/<user>/fila-certa
cp -r app/{Dockerfile,backend,frontend} /caminho/do/space/
cd /caminho/do/space && git add -A && git commit -m "deploy" && git push
```

O build roda no servidor (~3–5 min na primeira vez). A URL fica
`https://<user>-fila-certa.hf.space`.

### Segredos

As chaves VAPID vão em **Settings → Variables and secrets**, nunca no repositório. Em runtime
chegam como variáveis de ambiente comuns (`os.environ`).

### Três armadilhas

1. **Acesse o domínio direto (`*.hf.space`), não a página do HF.** O Space também é exibido dentro
   de um iframe em `huggingface.co/spaces/...`, e ali o navegador **não oferece instalar o PWA** nem
   registra push. Divulgue sempre a URL direta — inclusive no QR code da apresentação.
2. **O disco é efêmero:** o que for gravado se perde a cada rebuild. Por isso o `Dockerfile` aponta
   o DuckDB para `/tmp` e o banco é semeado no boot. Para a demo basta; persistência real exigiria
   o add-on de US$ 5/mês ou um Postgres externo (Supabase/Neon têm free tier).
3. **A imagem builda o frontend e serve tudo pelo FastAPI** — uma porta, um processo, sem CORS.
   Se separar front e back depois, lembre de configurar CORS.

### Plano B

Se o HF Spaces falhar na hora, **Render** funciona com o mesmo Dockerfile (mude a porta para
`$PORT`). Nesse caso, mantenha um ping externo (cron-job.org, UptimeRobot) batendo a cada 10 min
**durante a janela de avaliação** — é o que impede o spin down de matar a demo.

### Antes de divulgar a URL

- [ ] Abrir a URL direta no celular e confirmar que o navegador oferece instalar
- [ ] Ícones 192 e 512 px presentes em `public/icons/`
- [ ] Push testado no Android com o app fechado
- [ ] Seed carregado (a tela 2 mostra dados, não vazio)
- [ ] QR code apontando para a URL direta, testado por outra pessoa

---

## Painel de gestão — como executar

Aplicação web para **gestores e operação** (SME, CREs, direção de unidade). É a peça pronta;
o PWA do responsável (`frontend/`) entra depois no mesmo backend.

### Subir

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e app/backend
uvicorn fila_certa.main:app --port 8000 --reload --reload-dir app/backend/src
```

Abra **http://localhost:8000**. Não precisa de banco, de Node nem de build.

### As três telas — uma SPA, do panorama à ação

Navegação persistente no topo (Cidade · menu de Coordenadorias) e trilha
`Cidade › 7ª CRE › Realocar`. **Nada recarrega a página**, e cada rota continua sendo um deep-link
compartilhável.

| Rota | O que faz |
| --- | --- |
| `/` | **Cidade** — ranking de bairros por fila, vagas ao redor e cobertura de cada um |
| `/cre/{n}` | **CRE** — mapa dos focos; clicar num ponto troca o painel lateral (`?foco=<cod>`) |
| `/realocar/{origem}/{destino}` | **Realocação** — escolhe a criança e dispara a convocação |
| `/api/docs` | Documentação da API JSON (OpenAPI) |

**Como a SPA funciona sem router no cliente.** O `<body>` do shell carrega
`hx-boost="true" hx-target="#tela" hx-select="#tela"`: o htmx intercepta todo `<a>` e `<form>`,
busca a página inteira e troca apenas o `#tela`. Não há JavaScript de rota, o histórico e o botão
voltar funcionam nativamente, e **com JavaScript desligado tudo continua navegável** — cada
resposta é uma página completa e válida.

Uma consequência que vale conhecer: `hx-select` é herdado pelos filhos. Um formulário com
`hx-target` próprio ainda herda o `hx-select="#tela"` do shell e não acha o alvo num fragmento
parcial. Por isso o `POST /realocar/...` devolve a **tela inteira** com a convocação já registrada,
em vez de um fragmento — um contrato só para todas as respostas.

### API JSON

Mesma fonte do painel — é o que o PWA do responsável vai consumir:

```
GET /api/v1/totais            números agregados
GET /api/v1/cres              fila e vagas por coordenadoria
GET /api/v1/bairros?limite=40 ranking de bairros
GET /api/v1/focos?cre=7       unidades com fila e vaga vizinha
GET /api/v1/focos/{cod}       um foco com suas vagas alcançáveis
GET /api/v1/convocacoes       registro de tentativas de contato
```

### Regerar o dataset

O painel **não** lê as bases cruas: elas somam ~190 MB e demoram a agregar. O pré-processamento roda
offline e produz um JSON de 164 KB que carrega no boot.

```bash
git clone https://github.com/CIT-SME-RJ/dadoscreche.git   # na raiz do repositório
pip install duckdb openpyxl
python scripts/build_dataset.py app/backend/src/fila_certa/data/painel.json
```

Ele apura: fila por unidade (`Lista de espera`, processo 195/2025), vagas ociosas da rede parceira
(meta contratada menos matriculados, maio/2025), vizinhança até 3 km por distância entre coordenadas,
e os agregados por bairro e por CRE. **Uma creche alcançada por várias filas conta uma vez só** — somar
por foco infla o número; foi um erro que cometemos e corrigimos.

### Variáveis de ambiente

| Variável | Padrão | Para quê |
| --- | --- | --- |
| `FILA_CERTA_DATASET` | `src/fila_certa/data/painel.json` | dataset pré-agregado |
| `FILA_CERTA_DB_PATH` | `/tmp/fila_certa.db` | SQLite do registro de convocações |
| `FILA_CERTA_STATIC_DIR` | — | `dist/` do PWA, montado em `/app` |

### Arquitetura

```
api/v1/     → JSON (painel e PWA compartilham)
painel/     → views + templates Jinja2 + HTMX
domain/     → cascata.py (escalonamento) · viabilidade.py (cobertura, compatibilidade)
services/   → realocacao_service.py (orquestra a oferta)
repositories/
  painel_repo.py      lê o dataset
  tentativas_repo.py  grava convocações e tentativas  ← o que hoje não existe
```

**Um backend para as duas aplicações.** O painel dispara a convocação; o PWA a recebe. Se fossem dois
backends, o registro de tentativas se partiria em dois e a proposta perderia o sentido.

### O que é real e o que é demonstração

| | |
| --- | --- |
| ✅ Real | fila por unidade, vagas ociosas, distâncias, coordenadas, agregados |
| ⚠️ Demonstração | a **fila nominal** por unidade (`_fila_exemplo`) — a extração é anonimizada e não traz pontuação individual |
| ⚠️ Demonstração | só o **push** sai de fato; WhatsApp, SMS e ligação exigem credencial de provedor e ficam registrados como `pendente` |

O registro de tentativas é gravado de verdade, e é ele o entregável: consulte em
`/api/v1/convocacoes` depois de enviar uma convocação.

### Notas de implementação

- **HTMX vendorizado** em `painel/static/` — sem CDN, porque a rede do evento é instável.
- **Mapa em SVG**, não Leaflet: as coordenadas reais são projetadas linearmente no viewBox, e a página
  funciona sem rede. Tiles OSM ficam como evolução.

---

## Solução de problemas

### `ERROR: [Errno 48] Address already in use`

A porta 8000 já está ocupada — quase sempre por um `uvicorn` anterior que ficou pendurado.

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

A saída traz o PID na segunda coluna; `kill <PID>` libera a porta. Se insistir, `kill -9 <PID>`.
Alternativa sem matar nada: suba em outra porta com `--port 8001`.

> ⚠️ **`pkill -f "uvicorn fila_certa"` não resolve.** Com `--reload`, o uvicorn roda um processo pai
> e um filho, e **quem segura a porta é o filho** — cuja linha de comando é
> `python -c from multiprocessing.spawn ...`, sem o texto `uvicorn`. Por isso o `pkill` não encontra
> nada e a porta continua ocupada. Mate pelo PID que o `lsof` apontar.

### `TypeError: cannot use 'tuple' as a dict key (unhashable type: 'dict')`

Incompatibilidade do **cache de templates do Jinja2 com o Python 3.14**. Já está contornado —
`painel/views.py` desliga o cache (`templates.env.cache = None`), o que custa pouco com seis
templates. Se reaparecer após atualizar dependências, confirme que essa linha continua lá.

### `AttributeError: 'dict' object has no attribute 'split'` ao renderizar

Assinatura antiga do `TemplateResponse`. Nas versões recentes do Starlette a ordem é
**`TemplateResponse(request, nome, contexto)`** — o `request` vem primeiro. A forma antiga
`TemplateResponse(nome, {"request": request, ...})` faz o Starlette tratar o dicionário como nome
de template.

### O servidor responde 500, mas o mesmo código passa no teste

O `uvicorn` está rodando o código antigo em memória. Suba com `--reload --reload-dir app/backend/src`
ou reinicie o processo. Para conferir se o problema é do código ou do servidor:

```bash
python -c "
from fastapi.testclient import TestClient
import fila_certa.main as m
print(TestClient(m.app).get('/').status_code)"
```

### Uma ação HTMX apaga o bloco em vez de preenchê-lo

`hx-select` **é herdado** pelos elementos filhos. Como o shell declara `hx-select="#tela"` no
`<body>`, um formulário com `hx-target` próprio ainda procura `#tela` na resposta; se o endpoint
devolveu um fragmento parcial, não há o que selecionar e o alvo fica vazio. A convenção aqui é que
**todo endpoint devolve a página inteira** e o htmx extrai o `#tela` — foi assim que o
`POST /realocar/...` foi resolvido.

### O painel sobe mas as telas vêm vazias

Falta o dataset. Confirme que `src/fila_certa/data/painel.json` existe (164 KB) e regenere se
preciso — ver *Regerar o dataset* acima. Para checar rápido:

```bash
curl -s localhost:8000/api/v1/totais
```

### `ModuleNotFoundError: No module named 'fila_certa'`

O pacote não está instalado no ambiente ativo:

```bash
source .venv/bin/activate
pip install -e app/backend
```

O layout é `src/`, então rodar de dentro de `app/backend/src` **não** basta — o `pip install -e` é
o que registra o pacote.


## Convenções

- Código em **Python 3.11+**, identificadores em inglês, comentários e docs em português.
- Nada de credencial em código — tudo por env, `.env` fora do versionamento.
- Os dados são de crianças de 0 a 3 anos: não reidentificar, nunca em URL, e só agregados/amostras
  em prompt para a API.
