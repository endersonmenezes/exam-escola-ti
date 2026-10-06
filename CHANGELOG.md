# Changelog

Todas as mudanças notáveis do sistema de provas da Escola de TI
(`exam-escola-ti`). O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

> O versionamento começa em **1.0.0**: as versões anteriores (commits desde
> `da2c5f4`) foram ensaios com repos de teste e nunca foram usadas oficialmente
> em prova real. As turmas que exercitaram o sistema até aqui usaram-no como
> aula teste (prova dummy "Hello World").

## [1.0.0] — 2026-10-06

Primeira versão oficial do sistema de provas.

### Adicionado

- **Modelo de repositório único**: esqueleto ano-agnóstico (workflows + scripts)
  + pastas de prova (`exams/<ano>/<track>/`) aplicadas por *overlay* no repo do
  aluno no dia da prova, via issueops (`git fetch` no template — o repo gerado
  não é fork).
- **Prova-teste permanente "Hello World"** (`exams/dummy-exam/`, fora da
  hierarquia de ano): valida o sistema e treina o ciclo de entrega como
  *modo sandbox*; nunca é aplicada sem seleção explícita.
- **Issue única "🎯 Prova"** com lock em `.prova/issue`: preparação, seleção,
  aplicação, nota e fechamento acontecem na mesma issue (o aluno fica livre
  para usar os próprios issues). Setup com idempotência de **recurso** (adota
  issue existente, reconcilia duplicatas) e autocura do lock.
- **Comandos na issue**: `/track <nome>` (seleção, dispara a aplicação),
  `/aplicar` (força reaplicação), `/auto-correcao` (correção sob demanda),
  `/ajuda` / `--help` (lista de comandos).
- **Seleção sempre explícita do aluno** — fim da aplicação implícita; com mais
  de uma candidata publicada a aplicação trava de propósito até o `/track`.
- **Auto-correção sob demanda**: pushes não disparam correção (CI lenta ×
  incentivo a commits pequenos); correção completa (trampas + entrega + testes
  públicos + nota) roda via `/auto-correcao` ou dispatch, com gate no
  fechamento — fechar a issue sem correção **reabre** com aviso.
- **Nota em comentário único editado** (`<!-- nota-parcial -->`): `Última
  atualização` + `### Histórico` (uma entrada por disparo, até 10, com link da
  run). Linha `**Nota parcial:** N/100` parseável pelo fechamento.
- **Comentário de estado da preparação e ack de seleção como upsert**
  (`<!-- preparacao -->`, `<!-- track-ack -->`) — fim das duplicatas em
  rajadas de `issues: edited` (checkboxes).
- **Trampas**: variante por nome de repositório (T1), `.prova/id` canônico
  (T2), tamper-check contra o template (T3, opcional), janela auto-ancorada no
  commit de aplicação + `janela_minutos` da rubrica (T4 — só pega commits
  **depois** do fim; preparação entra como informativo), autoria por login do
  GitHub (T5).
- **Lockfile `track.json`** validado no CI do template (schema, `recursos`
  obrigatório, valores bool de workflows) e honrado pelos jobs da
  auto-correção.
- **`teacher.json` (schema 1)** — handshake de entrega na raiz do repo do
  aluno: aluno (login, RA, **nome**), variante, janela, commits
  (`commits_pre_aplicacao`, `fora_da_janela`), nota parcial,
  `auto_correcao.nota_ultima` e fontes.
- **Validação estrita de `FONTES.md`** (`scripts/fontes.py`, compartilhado com
  o teste público): só contam URLs em linha de tabela numerada, deduplicadas;
  URLs em texto corrido/exemplos não contam.
- **Suíte escondida fora do CI**: correção manual pelo professor ou Actions do
  repo privado do docente — aos alunos, cópia/relatório com a data de criação
  dos testes verificável (transparência sem entregar o ouro).
- **Docs**: README com sumário por persona (professor que replica / aluno que
  testa), ciclo de vida em mermaid, `docs/REGRAS.md`, `docs/TRACKS.md` e guia
  da prova-teste.

### Corrigido (ensaios com repos de teste)

- Corrida na geração do template (dois pushes) criando **issues duplicadas** →
  idempotência por recurso + reconciliador de duplicatas.
- Push do bot (GITHUB_TOKEN) não disparar workflows → aplicação passa a ser
  disparada pelo próprio comentário `/track` (schedule de 10 min como
  backstop).
- `git fetch --depth 1` deixando o repo do aluno *shallow* e quebrando o push
  do commit de aplicação ("shallow update not allowed").
- Tag inválida em `rodar_testes.sh` (`prova-<slug>-`) e porta não derivada da
  variante (`PORTA_API` do `variante/params.json`).
- Falsos positivos das trampas: commits de preparação contados como fora da
  janela; RA comparado a autor de commit (agora: login do GitHub); T3 desarmado
  tratado como suspeita (agora é observação de configuração).
- Contagem de fontes incluindo URLs de exemplo do template.
- Respostas do preparar fora de contexto (roteamento) e comentários duplicados
  (upsert).

[1.0.0]: https://github.com/endersonmenezes/exam-escola-ti/releases/tag/v1.0.0
