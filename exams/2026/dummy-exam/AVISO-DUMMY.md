# ⚠️ AVISO — pasta DUMMY de teste

> [!WARNING]
> `exams/2026/dummy-exam/` **não é uma prova real** — existe para testar o
> ciclo de aplicação (fetch do template → overlay na raiz → commit do bot →
> issue da prova → auto-correção com janela ancorada).
>
> **Antes de liberar este repo como template para uma turma real, REMOVA a
> pasta `exams/2026/` da branch `main`** — senão todo aluno que gerar/clonar
> o repo recebe a prova "aplicada" na hora.
>
> Para testar: gere um repo de teste a partir do template **sem** esta pasta,
> e só depois faça o push dela para `main`, observando o workflow *Aplicar
> prova* disparar sozinho (ou comente "aplicar" na issue).

## Layout de uma pasta de prova real (`exams/<ano>/<track>/`)

A pasta **é o repositório do aluno**: cada item do topo vira um arquivo/pasta
na raiz do repo dele no momento da aplicação:

| Item | Vira no repo do aluno |
| --- | --- |
| `README.md` | README raiz (a visão da prova) |
| `contrato.json` | contrato raiz (endpoints, regras, frontend, variante) |
| `rubrica.json` | rubrica raiz (pesos, extras, janela) |
| `track.json` | **lockfile raiz** — liga/desliga os workflows (ver `docs/TRACKS.md`) |
| `tests_publicos.py` | `tests/public/test_publicos.py` |
| `Dockerfile`, `src/` | stubs de entrega na raiz |

O que **não** está na pasta (workflows, scripts base, trampas, nota) é o
esqueleto ano-agnóstico — protegido pelo tamper-check e mantido no template.
