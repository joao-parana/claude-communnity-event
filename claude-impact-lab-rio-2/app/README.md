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

## Convenções

- Código em **Python 3.11+**, identificadores em inglês, comentários e docs em português.
- Nada de credencial em código — tudo por env, `.env` fora do versionamento.
- Os dados são de crianças de 0 a 3 anos: não reidentificar, nunca em URL, e só agregados/amostras
  em prompt para a API.
