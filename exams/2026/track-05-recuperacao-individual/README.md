# Recuperação Individual · Track 05 — Conecta Comunidade

> No momento da aplicação, esta pasta virou o **seu repositório**. O enunciado,
> o contrato e a rubrica estão na raiz; o sistema de entrega e as regras comuns
> continuam no esqueleto do template.

Esta é uma avaliação **individual, online, com consulta permitida e janela de
sete dias**. Você vai pesquisar, especificar, implementar, testar, depurar,
integrar serviços e organizar o trabalho no GitHub. Não basta entregar uma API
funcionando: a correção acompanha também as decisões, os testes, as fontes e o
processo que levou até ela.

Leia o [`ENUNCIADO.md`](ENUNCIADO.md) **inteiro antes de criar o primeiro
branch**. O documento é longo de propósito: ele contém requisitos, missões de
pesquisa, casos de debugging, critérios de aceite e o checklist de entrega.

## Composição da avaliação

| Etapa | Valor | Peso na nota final |
| --- | ---: | ---: |
| Prova prática online — esta track | 0–100 | 50% |
| Entrevista presencial individual | 0–100 | 50% |
| **Nota final** | **0–100** | **100%** |

A entrevista terá até 60 minutos e usará o seu repositório como evidência. Você
precisará explicar, executar e modificar pequenas partes da própria solução.
Entregar algo que você não compreende compromete as duas etapas.

## Rubrica da prova prática

| Critério | O que será avaliado | Pontos |
| --- | --- | ---: |
| A — SDD e arquitetura | Especificação rastreável, contrato OpenAPI, ADRs, modelo de dados e planejamento | 15 |
| B — CRUD e regras de negócio | Recursos, relacionamentos, validações, transições, consultas e persistência | 20 |
| C — TDD e qualidade dos testes | Ciclos red–green–refactor, unidade, integração, bordas e regressão | 15 |
| D — Debugging | Diagnóstico e correção dos quatro casos, com testes que reproduzem os defeitos | 10 |
| E — Integrações e resiliência | ViaCEP, webhook, timeout, retentativa, idempotência, assinatura e concorrência | 15 |
| F — GitHub e SDLC | Issues, branches, PRs, revisões, commits, rastreabilidade e uso dos workflows existentes | 10 |
| G — Pesquisa aplicada | Qualidade, diversidade e rastreabilidade das fontes e das decisões investigadas | 5 |
| Containerfile | Build e execução reproduzíveis, sem ajustes manuais do corretor | 5 |
| README | Execução local/container, configuração, testes, arquitetura e guia de navegação | 5 |
| **Total** |  | **100** |

> A nota exibida pelo CI é **parcial**. O sistema verifica automaticamente a
> integridade da entrega, o Containerfile e o README. Os demais critérios são
> avaliados pelo professor a partir do repositório, dos testes e das evidências.
> A entrevista possui rubrica própria e não está incluída nesses 100 pontos.

## Janela de sete dias

- A janela é de **10.080 minutos (7 × 24 horas)**, iniciada no commit do bot
  `chore: aplicar prova …`.
- O comentário de aplicação na issue “🎯 Prova” informa o início e a variante.
- O último push dentro da janela conta. Commits posteriores entram em revisão.
- Planeje trabalho para **pelo menos três dias diferentes**. Isso também é um
  critério de processo: uma entrega comprimida em um único bloco não demonstra
  os ciclos de especificação, teste, revisão e refactor pedidos pela prova.
- Feche a issue somente depois de todo o trabalho estar na branch padrão e de
  executar `/auto-correcao` ao menos uma vez no estado final.

## Ferramentas do repositório

| Caminho/recurso | Uso |
| --- | --- |
| `ENUNCIADO.md` | Fonte completa dos requisitos e das tarefas |
| `contrato.json` | Versão máquina-legível do contrato funcional |
| `rubrica.json` | Pontuação e janela da prova prática |
| `variante/params.json` | Parâmetros individuais gerados na aplicação; somente leitura |
| `FONTES.md` | Declaração obrigatória de sites e IA consultados |
| `docs/REGRAS.md` | Regras comuns, integridade e causas de zeramento |
| issue “🎯 Prova” | Seleção, aplicação, auto-correção e encerramento |
| Actions existentes | Evidências de preparação, integridade, estrutura e README |

## Parâmetros da sua variante

Leia os valores reais em `variante/params.json`. Não execute o gerador, não
crie esse arquivo manualmente e não copie a variante de outro repositório.

| Parâmetro | Significado |
| --- | --- |
| `PORTA_API` | Porta do host usada pelo corretor; a aplicação escuta na 8080 dentro do container |
| `LIMITE_PAGINACAO` | Tamanho padrão de página quando `tamanho` não é informado |
| `HORAS_LIMITE_ATIVIDADE` | Limite de horas previstas/realizadas por atividade |
| `TENTATIVAS_WEBHOOK` | Número máximo de tentativas de entrega do webhook, incluindo a primeira |

## Estrutura esperada da solução

Os nomes de módulos internos são livres. A organização abaixo deixa claro onde
o corretor procurará cada evidência:

```text
.
├── README.md
├── Containerfile
├── .dockerignore
├── src/                       # aplicação
├── tests/app/                 # testes da aplicação; não use tests/public/
├── debug/                     # correções e testes dos quatro casos
├── docs/
│   ├── constitution.md
│   ├── spec.md
│   ├── plan.md
│   ├── tasks.md
│   ├── tests.md
│   ├── pesquisa.md
│   ├── openapi.yaml
│   └── adr/
└── evidencias/
    ├── tdd/                   # registros enxutos dos ciclos red–green–refactor
    └── revisao/               # checklist de revisão e validação final
```

Você pode criar arquivos em `docs/`, mas **não altere** `docs/REGRAS.md` nem
`docs/TRACKS.md`. Não crie testes em `tests/public/`.

## Consulta, pesquisa e IA

- Consulta a sites, livros, documentação e IA **como conversa** é permitida.
- Toda fonte usada precisa estar em `FONTES.md`, no formato de linha numerada
  da tabela, com URL, conteúdo consultado e local de aplicação.
- Conversas de IA precisam ser compartilhadas por link público/acessível e
  registradas em `FONTES.md`.
- IA **como agente** — editando arquivos, executando comandos, criando commits,
  rodando testes ou operando o GitHub no seu lugar — é proibida e zera a prova.
- A pesquisa avaliada não é uma lista de links. Em `docs/pesquisa.md`, cada
  investigação precisa ligar pergunta → fonte → aprendizado → decisão →
  evidência no código/teste/documento.
- Você deve conseguir explicar qualquer trecho entregue, inclusive o que surgiu
  de uma consulta.

## Regras de integridade

- Trabalho individual. Não compartilhe implementação, testes ou diagnósticos.
- Não altere `scripts/`, `.github/`, `docs/REGRAS.md`, `docs/TRACKS.md`,
  `contrato.json`, `rubrica.json`, `track.json` ou `ENUNCIADO.md`.
- Não crie workflows próprios em `.github/`: além de não ser necessário, essa
  alteração viola a integridade do template. Use os Actions já fornecidos.
- Não altere nem apague commits para fabricar ciclos de TDD ou reescrever o
  histórico depois da entrega.
- Não versione tokens, senhas, chaves privadas, cookies ou dados pessoais reais.
- Não use dados de pessoas reais nos testes, exemplos, prints ou integrações.

## Sequência recomendada

1. Preencher identidade e selecionar `/track track-05-recuperacao-individual`.
2. Ler enunciado e contrato; registrar dúvidas e interpretações no próprio plano.
3. Criar o mapa de issues e o planejamento antes da implementação.
4. Pesquisar e escrever a primeira versão da especificação e dos ADRs.
5. Implementar por fatias verticais, usando PRs e ciclos de TDD.
6. Resolver os quatro casos de debugging com testes de regressão.
7. Testar as integrações exclusivamente com servidores simulados controlados.
8. Revisar segurança, concorrência, persistência, container e documentação.
9. Executar toda a validação no estado final e atualizar README/FONTES.
10. Rodar `/auto-correcao`, conferir o resultado e fechar a issue “🎯 Prova”.

## Antes de fechar a entrega

- [ ] Todo o trabalho foi integrado à branch padrão por pull request.
- [ ] O HEAD final tem testes verdes; commits vermelhos intermediários são
      evidência de TDD, não o estado da entrega.
- [ ] O container sobe em ambiente limpo usando apenas o README.
- [ ] Os testes não dependem de internet nem de serviços externos reais.
- [ ] `docs/openapi.yaml` corresponde ao comportamento implementado.
- [ ] As quatro correções de debugging têm diagnóstico e regressão.
- [ ] As missões de pesquisa têm aplicação localizável na entrega.
- [ ] `FONTES.md` está completo e sem placeholder.
- [ ] O README foi reescrito para a sua solução; não permaneceu igual à prova.
- [ ] `/auto-correcao` foi executado ao menos uma vez depois do último push.

---

## Este README passa a ser seu

Depois de ler o enunciado, substitua este texto por um README da **sua
solução**. O corretor precisa encontrar rapidamente: visão geral, arquitetura,
requisitos de ambiente, variáveis de configuração, comandos de execução local e
em container, comando dos testes, uso dos mocks, dados de exemplo, estrutura do
projeto, limitações conhecidas e links para a especificação e a pesquisa.

**Não edite nem crie arquivos dentro de:** `tests/public/`, `scripts/` e
`.github/`. Também não altere os arquivos protegidos do enunciado e das regras.

**Seu trabalho pode ficar em:** `src/`, `tests/app/`, `debug/`, `docs/` (exceto
os dois documentos protegidos), `evidencias/`, `Containerfile`, `.dockerignore`,
manifestos de dependências e demais arquivos necessários na raiz.
