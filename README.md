# Claude Community Events

Repositório guarda-chuva dos eventos da comunidade Claude no Brasil de que participo.
Cada evento vive em seu próprio diretório, autocontido.

## Eventos

| Diretório | Evento | Data | Tema |
| --- | --- | --- | --- |
| [`claude-impact-lab-rio-2/`](claude-impact-lab-rio-2/) | Claude Impact Lab Rio #2 | 30/08 | Hackathon com a Secretaria Municipal de Educação do Rio |

## Convenção para novos eventos

Um diretório por evento, nomeado em *kebab-case*, contendo pelo menos:

```
<nome-do-evento>/
├── README.md      # o que é o evento, como rodar o que está aqui
├── CLAUDE.md      # contexto operacional para o Claude Code
└── docs/          # material de origem (posts, briefings, comunicados)
```

Cada diretório é independente: ambiente virtual, dependências e dados próprios.
Nada de estado compartilhado entre eventos.

## Regras gerais

- Documentação em **português do Brasil**, com acentuação correta.
- Credenciais em `.env`, nunca versionadas.
- Dados de terceiros (prefeituras, órgãos públicos, parceiros) ficam fora do versionamento;
  guarde o *script* que os obtém, não o dado.
- Sobre a comunidade: https://www.claudecommunity.com.br/
