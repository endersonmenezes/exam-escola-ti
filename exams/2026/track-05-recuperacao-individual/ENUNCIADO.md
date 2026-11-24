# ENUNCIADO — Recuperação Individual · Conecta Comunidade

- **Modalidade:** individual, online, com consulta e pesquisa rastreáveis
- **Janela:** 7 dias corridos (10.080 minutos), contados da aplicação da prova
- **Entrega:** repositório Git, aplicação executável, testes, documentação e evidências
- **Entrevista:** presencial, individual, até 60 minutos, depois da entrega
- **Peso:** prova prática 50% + entrevista 50%

> Esta avaliação foi desenhada para uma semana. O volume propositalmente exige
> pesquisa, planejamento e vários ciclos de trabalho. Não tente começar pela
> implementação: as primeiras decisões afetam banco, API, testes, integrações,
> container e entrevista.

## 1. Situação-problema

A iniciativa **Conecta Comunidade** aproxima projetos de extensão universitária
de organizações comunitárias. Hoje, o cadastro de parceiros, o acompanhamento
dos projetos e o registro das atividades são feitos em planilhas separadas. Os
problemas frequentes são:

- endereços digitados de forma inconsistente;
- parceiros desativados ainda vinculados a projetos ativos;
- projetos sem atividades planejadas apresentados como se estivessem em execução;
- horas calculadas com arredondamentos diferentes em cada planilha;
- atividades concluídas alteradas depois do fechamento;
- notificações de publicação duplicadas quando uma requisição é repetida;
- integrações externas tratadas como se nunca falhassem;
- ausência de histórico confiável das decisões técnicas.

Você foi responsável por construir a primeira versão da API e por demonstrar um
processo de engenharia reproduzível. A solução deve cadastrar parceiros com
consulta de CEP, administrar projetos e atividades, produzir relatórios e
publicar eventos em um webhook. Não é necessário criar frontend.

## 2. Competências demonstradas

Ao final, você deverá demonstrar que consegue:

1. transformar um problema em especificação rastreável antes de implementar;
2. pesquisar fontes primárias e usar o aprendizado em decisões concretas;
3. construir um CRUD com relacionamentos, validações e persistência;
4. praticar TDD e distinguir testes unitários, de integração e de regressão;
5. diagnosticar defeitos a partir de sintomas e testes que falham;
6. integrar serviços externos sem presumir rede perfeita;
7. tratar idempotência e concorrência sem depender apenas de sorte;
8. usar GitHub como registro de trabalho, revisão e tomada de decisão;
9. empacotar e documentar uma aplicação para outra pessoa executar;
10. explicar e defender a própria solução em uma entrevista técnica.

## 3. Regras de leitura e prioridade

1. O contrato funcional deste enunciado e o `contrato.json` são obrigatórios.
2. A stack é livre, desde que o README permita instalar e executar tudo em
   ambiente limpo. Escolha algo que você consiga explicar na entrevista.
3. Os valores individuais estão em `variante/params.json`. Eles não devem ser
   substituídos pelos valores dos exemplos.
4. Um exemplo marcado como inconsistente não altera o contrato.
5. Decisões não cobertas pelo enunciado devem ser registradas em ADR, com
   alternativas e consequências. “Sempre fiz assim” não é justificativa técnica.
6. Se identificar uma ambiguidade real, registre a interpretação antes de
   implementar e torne-a verificável por teste. Não altere o enunciado.

## 4. O que deve ser entregue

### 4.1 Aplicação

- código-fonte em `src/`;
- persistência real em banco relacional, com SQLite aceito;
- `Containerfile` funcional e `.dockerignore`;
- aplicação ouvindo na porta **8080 dentro do container**;
- configuração externa por variáveis de ambiente, sem segredos versionados;
- dados preservados ao recriar o processo/container com volume em `/data`;
- comando de migração/inicialização do banco documentado e reproduzível;
- endpoint de saúde e logs úteis, sem dados sensíveis.

### 4.2 Especificação e arquitetura

Crie, no mínimo:

- `docs/constitution.md`: regras invariantes do projeto;
- `docs/spec.md`: requisitos funcionais/não funcionais, casos de uso e aceite;
- `docs/plan.md`: arquitetura, modelo de dados e sequência técnica;
- `docs/tasks.md`: decomposição ligada a requisitos, issues e PRs;
- `docs/tests.md`: estratégia e matriz de testes;
- `docs/openapi.yaml`: contrato OpenAPI 3.1 dos endpoints;
- `docs/adr/`: pelo menos **cinco ADRs**;
- `docs/pesquisa.md`: investigações e aplicação das fontes;
- `debug/diagnostico.md`: diagnóstico dos quatro defeitos.

Os cinco ADRs devem cobrir, no mínimo: persistência e transações; estratégia de
testes; idempotência; retentativas do webhook; e formato/tratamento de erros.

### 4.3 Testes e evidências

- testes da aplicação em `tests/app/`;
- correções e testes de debugging em `debug/`;
- evidências enxutas dos ciclos de TDD em `evidencias/tdd/`;
- checklist de revisão em `evidencias/revisao/checklist-final.md`;
- comandos e resultados relevantes registrados sem despejar logs gigantes;
- histórico Git e PRs coerentes com a narrativa da entrega.

## 5. Planejamento sugerido para os sete dias

Este cronograma é uma recomendação, não uma sequência rígida. Ele ajuda a evitar
que toda a entrega aconteça no último dia.

| Dia | Foco | Evidência esperada |
| --- | --- | --- |
| 1 | Leitura, pesquisa inicial, mapa de requisitos e riscos | Issues, `tasks.md`, primeiras fontes |
| 2 | SDD, OpenAPI, modelo de dados e ADRs | PR de especificação revisado |
| 3 | Parceiros + ViaCEP com TDD | Primeira fatia vertical e testes |
| 4 | Projetos, atividades, regras e concorrência | PRs de domínio e regressões |
| 5 | Webhook, idempotência, resiliência e debugging | Mocks, falhas simuladas, correções |
| 6 | Container, persistência, segurança, cobertura de bordas | Revisão e testes ponta a ponta |
| 7 | Validação limpa, documentação, fontes e preparação da entrevista | HEAD verde e entrega fechada |

Trabalhe em pelo menos **três dias diferentes**. Não crie commits artificiais
só para cumprir datas: o histórico precisa refletir trabalho real.

---

# PARTE I — PESQUISA APLICADA

## 6. Como registrar a pesquisa

Em `docs/pesquisa.md`, responda a pelo menos **12 das 14 missões** abaixo. Cada
missão deve conter:

1. pergunta investigada, escrita com suas palavras;
2. contexto do problema encontrado nesta prova;
3. pelo menos uma fonte localizada e data de acesso;
4. síntese do aprendizado, sem copiar parágrafos;
5. decisão tomada e alternativa rejeitada;
6. link para o arquivo, teste, ADR, commit ou PR onde a decisão aparece;
7. limitação ou dúvida que permaneceu.

Requisitos mínimos de fontes:

- **15 fontes distintas** no conjunto da pesquisa;
- pelo menos **8 fontes primárias/oficiais**: especificações, RFCs, documentação
  da linguagem/banco/framework ou documentação oficial da ferramenta;
- pelo menos **6 missões com duas fontes confrontadas**;
- pelo menos **10 aplicações práticas localizáveis** no entregável;
- todas as fontes também registradas em `FONTES.md`.

Quantidade não substitui qualidade. Quinze links sem aplicação valem menos que
uma investigação que mudou uma decisão e ganhou um teste. Responder “usei porque
a IA sugeriu” não fecha uma missão.

## 7. Missões de pesquisa

### P01 — Spec-Driven Development e rastreabilidade

Investigue como ligar requisito → caso de uso → critério de aceite → teste →
implementação. Proponha um esquema de identificadores para esta prova e explique
como ele evita que um requisito desapareça durante o desenvolvimento.

### P02 — Contract-first e OpenAPI 3.1

Pesquise a diferença entre documentar depois e usar o contrato como fonte de
projeto. Compare `nullable`, `required`, `oneOf` e tipos numéricos no contexto
das respostas desta API. Explique como manter `openapi.yaml` e implementação
sincronizados.

### P03 — Problem Details for HTTP APIs

Leia a RFC 9457 e identifique sua relação com a antiga RFC 7807. Justifique os
membros usados nas respostas de erro e a diferença entre `type`, `title`,
`detail`, `instance`, `status` e extensões.

### P04 — Semântica HTTP e idempotência

Pesquise os significados de 200, 201, 202, 204, 400, 404, 409, 422, 429, 500,
502 e 503 neste contexto. Explique por que método HTTP idempotente não elimina a
necessidade de uma chave de idempotência para operações de criação/publicação.

### P05 — Dinheiro, horas e arredondamento

Investigue problemas de ponto flutuante binário, representação decimal e
arredondamento half-up. Justifique os inteiros em centésimos de hora e o formato
do percentual do relatório. Inclua exemplos que falhariam com `float`/`round`.

### P06 — TDD e ciclo red–green–refactor

Pesquise o propósito de cada fase e por que escrever todos os testes depois não
comprova TDD. Explique o risco de um teste que nunca foi visto falhando e como
seus commits/evidências resolvem isso.

### P07 — Pirâmide de testes e duplas de teste

Compare testes unitários, integração e ponta a ponta; mocks, stubs, fakes e
servidores HTTP simulados. Decida o que deve ser testado sem rede e o que exige
banco real. Evite transformar todo teste em mock da própria implementação.

### P08 — Timeout, retentativa, backoff e jitter

Pesquise falhas transitórias, tempestade de retentativas, backoff exponencial,
jitter e `Retry-After`. Justifique quais operações podem ser repetidas e quais
códigos não devem gerar nova tentativa.

### P09 — Idempotency-Key e atomicidade

Investigue replay da mesma requisição, conflito de payload, expiração da chave,
escopo por rota e unicidade no banco. Explique por que verificar antes de inserir
não é suficiente sob concorrência.

### P10 — Assinatura de webhooks e segredos

Pesquise HMAC-SHA256, comparação de assinatura em tempo constante, replay,
timestamp e rotação de segredos. Explique o que a assinatura prova — e o que ela
não prova. Não coloque segredo real no repositório.

### P11 — Transações, constraints e concorrência

Pesquise transações, isolamento, constraints de unicidade e tratamento de erro de
integridade no banco escolhido. Compare lock de aplicação com garantia no banco e
explique qual protege múltiplas instâncias.

### P12 — GitHub Flow, pull requests e revisão

Pesquise branches curtos, PRs pequenos, revisão, vinculação de issues e histórico
útil. Explique como revisar o próprio PR sem fingir aprovação de outra pessoa e
como os Actions existentes entram nesse fluxo sem editar `.github/`.

### P13 — Containers reproduzíveis e segurança

Investigue builds reproduzíveis, cache de dependências, `.dockerignore`, usuário
não root, healthcheck e persistência em volume. Compare imagem de desenvolvimento
com imagem de execução e justifique sua escolha.

### P14 — Logs, correlação e privacidade

Pesquise logs estruturados, correlation ID, níveis de log e minimização de dados.
Decida o que registrar nas falhas da ViaCEP/webhook sem expor endereço completo,
token, assinatura secreta ou payload sensível.

## 8. Pontos de partida para pesquisa

Estas fontes ajudam a começar, mas **não esgotam** as missões. Leia as seções
relevantes, não apenas o título. Acrescente documentação da stack escolhida.

- RFC 9457 — Problem Details: <https://www.rfc-editor.org/rfc/rfc9457>
- RFC 9110 — HTTP Semantics: <https://www.rfc-editor.org/rfc/rfc9110>
- OpenAPI Specification 3.1: <https://spec.openapis.org/oas/v3.1.0.html>
- OWASP API Security Top 10: <https://owasp.org/API-Security/editions/2023/en/0x11-t10/>
- Python `decimal` (se usar Python): <https://docs.python.org/3/library/decimal.html>
- SQLite transactions (se usar SQLite): <https://www.sqlite.org/lang_transaction.html>
- SQLite constraints: <https://www.sqlite.org/lang_createtable.html#constraints>
- GitHub Flow: <https://docs.github.com/en/get-started/using-github/github-flow>
- GitHub — linking PRs to issues: <https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue>
- GitHub Actions — understanding workflows: <https://docs.github.com/en/actions/about-github-actions/understanding-github-actions>
- Docker — building best practices: <https://docs.docker.com/build/building/best-practices/>
- Docker — volumes: <https://docs.docker.com/engine/storage/volumes/>
- AWS Builders’ Library — retries, backoff and jitter: <https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/>
- ViaCEP: <https://viacep.com.br/>
- Documentação oficial do framework, ORM, biblioteca HTTP e runner de testes da
  sua stack: localize e registre as URLs exatas.

---

# PARTE II — SDD E CONTRATO DA API

## 9. Convenções da especificação

Use identificadores consistentes em todos os artefatos:

- `RF-xx`: requisito funcional;
- `RNF-xx`: requisito não funcional;
- `RN-xx`: regra de negócio;
- `UC-xx`: caso de uso;
- `ADR-xx`: decisão arquitetural;
- `CT-xx`: caso de teste.

Cada requisito deve ter critério de aceite mensurável e pelo menos um teste ou
procedimento de verificação. Cada caso de teste deve apontar para o requisito
que protege. Cada PR deve indicar os identificadores implementados.

## 10. Convenções gerais da API

- Base URL na correção: `http://localhost:{PORTA_API}`
- Porta dentro do container: `8080`
- Content-Type principal: `application/json`

### 10.1 Identificadores e datas

- IDs são inteiros positivos gerados pela aplicação.
- Datas/horas com tempo usam ISO-8601 com offset explícito.
- Persista instantes em UTC e documente qualquer conversão.
- `criado_em` e `atualizado_em` são retornados nos recursos que os possuem.

### 10.2 Horas e percentuais

- Campos de horas na API usam **inteiros em centésimos de hora**.
- `100` = 1 hora; `125` = 1h15; `150` = 1h30.
- Valores de atividades devem ser múltiplos de 25 (15 minutos).
- O limite por atividade é `HORAS_LIMITE_ATIVIDADE × 100`.
- Percentuais do relatório são strings decimais com duas casas, arredondados
  half-up. Não use ponto flutuante para acumular horas.

### 10.3 Envelope de erro

Erros seguem `application/problem+json`:

```json
{
  "type": "https://example.test/problemas/recurso-nao-encontrado",
  "title": "Recurso não encontrado",
  "status": 404,
  "detail": "O projeto 42 não existe.",
  "instance": "/projetos/42",
  "code": "projeto_nao_encontrado",
  "correlation_id": "01J..."
}
```

Regras:

- `type`, `title`, `status`, `detail`, `instance`, `code` e `correlation_id`
  são obrigatórios;
- `title` é estável por tipo de erro; `detail` contextualiza a ocorrência;
- validações podem acrescentar `errors`, array com `field` e `message`;
- não devolva stack trace, SQL, segredo ou endereço completo em erro/log;
- toda resposta, inclusive sucesso, carrega `X-Correlation-ID`; o mesmo valor
  aparece em `correlation_id` dos erros e nos logs da requisição.

### 10.4 Paginação e ordenação

Listagens de parceiros, projetos e atividades usam:

- `pagina`: inteiro >= 1, padrão 1;
- `tamanho`: inteiro entre 1 e 50; padrão `LIMITE_PAGINACAO`;
- resposta:

```json
{
  "dados": [],
  "paginacao": {
    "pagina": 1,
    "tamanho": 10,
    "total": 0,
    "total_paginas": 0
  }
}
```

`total` é a quantidade após filtros, antes da paginação. Página além do final
retorna `dados: []` com metadados coerentes. Ordenação padrão é `id` crescente,
salvo quando outra for indicada.

### 10.5 Endpoint de saúde

`GET /saude` → **200**:

```json
{"status":"ok","versao":"1.0.0"}
```

A resposta de saúde não deve consultar ViaCEP ou webhook. O healthcheck do
container deve usar esse endpoint.

## 11. Recurso: parceiros

### 11.1 Modelo mínimo

| Campo | Regra |
| --- | --- |
| `id` | Inteiro gerado |
| `nome` | String 3..100, sem apenas espaços |
| `email` | E-mail válido, único, normalizado para minúsculas |
| `cep` | Exatamente 8 dígitos, sem máscara na persistência |
| `logradouro`, `bairro`, `cidade`, `uf` | Dados normalizados retornados pela consulta de CEP |
| `complemento` | Opcional, até 120 caracteres |
| `ativo` | Boolean, padrão `true` |
| `criado_em`, `atualizado_em` | ISO-8601 com offset |

### 11.2 Endpoints

| Método e caminho | Sucesso | Regra |
| --- | ---: | --- |
| `POST /parceiros` | 201 | Consulta CEP e cria parceiro |
| `GET /parceiros` | 200 | Paginação + filtros `nome` e `ativo` |
| `GET /parceiros/{id}` | 200 | Detalhe |
| `PUT /parceiros/{id}` | 200 | Atualiza nome, e-mail, CEP e complemento; se CEP mudar, refaz consulta |
| `PATCH /parceiros/{id}` | 200 | Body `{"ativo": false}` ou `true` |
| `DELETE /parceiros/{id}` | 204 | Só sem projetos vinculados |

`nome` no filtro faz busca parcial sem distinção de maiúsculas/minúsculas.
`ativo` aceita somente `true` ou `false`. No PUT, todos os campos editáveis
(`nome`, `email`, `cep` e `complemento`) são obrigatórios; ausência gera 422
`validacao_falhou`. O PATCH aceita **somente** o campo `ativo`; campos ausentes
ou extras geram 422 `validacao_falhou`. Campos de leitura (`id`, endereço
resolvido e timestamps) não são aceitos como edição.

### 11.3 Regras de negócio

- **RN-P01:** e-mail duplicado → **409**, `email_em_uso`.
- **RN-P02:** CEP inexistente/inválido no provedor → **422**, `cep_invalido`.
- **RN-P03:** timeout, rede ou 5xx do provedor → **503**, `viacep_indisponivel`.
- **RN-P04:** parceiro com qualquer projeto não pode ser excluído → **409**,
  `parceiro_com_projetos`.
- **RN-P05:** parceiro com projeto `ativo` não pode ser desativado → **409**,
  `parceiro_com_projetos_ativos`.
- **RN-P06:** projeto `rascunho` ou `encerrado` não impede desativação.
- **RN-P07:** nenhuma alteração fica persistida se a consulta de CEP falhar.

## 12. Recurso: projetos

### 12.1 Modelo mínimo

| Campo | Regra |
| --- | --- |
| `id` | Inteiro gerado |
| `titulo` | String 3..120 |
| `descricao` | String 10..2000 |
| `parceiro_id` | Parceiro existente |
| `horas_previstas_centesimos` | Inteiro 100..1.000.000 |
| `status` | `rascunho`, `ativo`, `encerrado` |
| `criado_em`, `atualizado_em` | ISO-8601 com offset |

### 12.2 Endpoints

| Método e caminho | Sucesso | Regra |
| --- | ---: | --- |
| `POST /projetos` | 201 | Cria em `rascunho`; exige `Idempotency-Key` |
| `GET /projetos` | 200 | Paginação + filtros `status` e `parceiro_id` |
| `GET /projetos/{id}` | 200 | Detalhe |
| `PUT /projetos/{id}` | 200 | Só em `rascunho` |
| `PATCH /projetos/{id}/status` | 200 | Body com `status` |
| `DELETE /projetos/{id}` | 204 | Só `rascunho` sem atividades |
| `GET /projetos/{id}/relatorio` | 200 | Consolida atividades |
| `POST /projetos/{id}/publicacao` | 202 | Enfileira evento de webhook |

### 12.3 Regras de negócio

- **RN-J01:** parceiro inexistente → **404**, `parceiro_nao_encontrado`.
- **RN-J02:** parceiro inativo não aceita novo projeto → **409**,
  `parceiro_inativo`.
- **RN-J03:** transições permitidas: `rascunho → ativo → encerrado`; demais
  transições → **409**, `transicao_status_invalida`.
- **RN-J04:** ativar exige parceiro ativo e pelo menos uma atividade
  `planejada`; caso contrário → **409**, `projeto_sem_atividade_planejada`.
- **RN-J05:** encerrar exige que nenhuma atividade esteja `planejada`; caso
  contrário → **409**, `projeto_com_atividades_planejadas`.
- **RN-J06:** projeto ativo/encerrado não pode ser editado pelo PUT nem excluído
  → **409**, `projeto_nao_editavel`.
- **RN-J07:** rascunho com atividades não pode ser excluído → **409**,
  `projeto_com_atividades`.
- **RN-J08:** encerrado é terminal para edição, atividades e publicação.

## 13. Recurso: atividades

### 13.1 Modelo mínimo

| Campo | Regra |
| --- | --- |
| `id` | Inteiro gerado |
| `projeto_id` | Projeto existente |
| `titulo` | String 3..120 |
| `inicio` | ISO-8601 com offset |
| `voluntario` | Nome fictício 3..100; não use dados reais |
| `horas_previstas_centesimos` | Múltiplo de 25, entre 25 e o limite da variante |
| `horas_realizadas_centesimos` | Mesmas regras; obrigatório ao concluir |
| `status` | `planejada`, `concluida`, `cancelada` |
| `criado_em`, `atualizado_em` | ISO-8601 com offset |

### 13.2 Endpoints

| Método e caminho | Sucesso | Regra |
| --- | ---: | --- |
| `POST /projetos/{id}/atividades` | 201 | Cria em `planejada`; exige `Idempotency-Key` |
| `GET /atividades` | 200 | Paginação + filtros `projeto_id`, `status`, `de`, `ate` |
| `GET /atividades/{id}` | 200 | Detalhe |
| `PUT /atividades/{id}` | 200 | Só `planejada` |
| `PATCH /atividades/{id}/status` | 200 | Conclui ou cancela |
| `DELETE /atividades/{id}` | 204 | Só `planejada` |

Filtros `de` e `ate` comparam `inicio`, são ISO-8601 e formam intervalo inclusivo.
Ordenação padrão: `inicio` crescente, depois `id` crescente.

### 13.3 Regras de negócio

- **RN-A01:** atividades só podem ser criadas em projeto `rascunho` ou `ativo`.
- **RN-A02:** concluir usa `{"status":"concluida","horas_realizadas_centesimos":125}`.
- **RN-A03:** cancelar usa `{"status":"cancelada"}` e não exige horas realizadas.
- **RN-A04:** somente `planejada → concluida|cancelada`; estado terminal é
  imutável e gera **409**, `atividade_finalizada`.
- **RN-A05:** atividade concluída não pode ser cancelada ou editada.
- **RN-A06:** atividade cancelada não conta horas previstas nem realizadas no
  relatório.
- **RN-A07:** horas realizadas não podem exceder `HORAS_LIMITE_ATIVIDADE`.

## 14. Relatório do projeto

`GET /projetos/{id}/relatorio` → **200**:

```json
{
  "projeto_id": 7,
  "status": "ativo",
  "atividades_planejadas": 1,
  "atividades_concluidas": 2,
  "atividades_canceladas": 1,
  "horas_previstas_centesimos": 600,
  "horas_realizadas_centesimos": 275,
  "percentual_conclusao": "45.83"
}
```

- Horas previstas somam atividades `planejada` e `concluida`.
- Horas realizadas somam somente `concluida`.
- Se horas previstas for zero, percentual é `"0.00"`.
- Percentual = realizadas ÷ previstas × 100, duas casas, half-up.
- Os valores acima são ilustrativos: verifique a fórmula, não copie resultados.

## 15. Erros mínimos esperados

| Código HTTP | `code` | Exemplo de situação |
| ---: | --- | --- |
| 400 | `json_invalido` | JSON malformado |
| 400 | `parametro_invalido` | Página, filtro ou data inválidos |
| 404 | `parceiro_nao_encontrado` | ID ausente |
| 404 | `projeto_nao_encontrado` | ID ausente |
| 404 | `atividade_nao_encontrada` | ID ausente |
| 409 | `email_em_uso` | E-mail duplicado, inclusive concorrente |
| 409 | `idempotencia_conflito` | Mesma chave com payload diferente |
| 409 | `transicao_status_invalida` | Retrocesso ou repetição inválida |
| 422 | `validacao_falhou` | Campos fora das regras |
| 422 | `cep_invalido` | CEP inexistente |
| 503 | `viacep_indisponivel` | Falha transitória do CEP |
| 503 | `webhook_nao_configurado` | URL/segredo não configurados |

Regra de precedência: JSON/formato → campos → existência do recurso → estado e
conflito de negócio. Documente exceções que fizerem sentido e cubra por testes.

## 16. Exemplo propositalmente inconsistente

> [!CAUTION]
> O trecho abaixo veio de uma planilha legada e **contradiz o contrato**. Ele
> serve para verificar se você priorizou a especificação, não o exemplo.

```json
{
  "horas_previstas": 1.3333333333,
  "percentual": 45.835,
  "erro": "Projeto inválido"
}
```

Não use floats acumulados para horas, não devolva o percentual com três casas e
não substitua Problem Details pelo campo `erro`.

---

# PARTE III — INTEGRAÇÕES E RESILIÊNCIA

## 17. Integração com ViaCEP

### 17.1 Comportamento

Na criação de parceiro e na mudança de CEP, o backend consulta:

```text
GET {VIACEP_BASE_URL}/{cep}/json/
```

Configuração:

- `VIACEP_BASE_URL`, padrão `https://viacep.com.br/ws`;
- `HTTP_TIMEOUT_MS`, com padrão documentado;
- a suíte local aponta `VIACEP_BASE_URL` para um servidor simulado.

Regras:

1. timeout explícito de conexão e leitura conforme suporte da biblioteca;
2. CEP com `erro: true` no provedor → 422 `cep_invalido`;
3. HTTP 400 do provedor → 422 `cep_invalido`;
4. timeout, conexão, resposta inválida ou HTTP 5xx → 503 `viacep_indisponivel`;
5. não repetir indefinidamente; para esta consulta, no máximo uma nova tentativa
   em falha de rede/5xx, com justificativa no ADR;
6. não persistir parceiro nem atualização parcial quando a integração falhar;
7. não incluir token ou endereço completo nos logs;
8. testes automatizados não podem acessar `viacep.com.br`.

### 17.2 Cenários obrigatórios com mock

- sucesso 200 com endereço completo;
- CEP inexistente;
- JSON inválido;
- timeout;
- falha de conexão;
- 500 seguido de sucesso quando houver retry;
- 500 persistente;
- mudança de CEP com falha sem alterar o endereço anterior.

## 18. Idempotência de criação

`POST /projetos` e `POST /projetos/{id}/atividades` exigem header
`Idempotency-Key` de 8..100 caracteres.

Comportamento persistido por pelo menos 24 horas:

1. ausência/formato inválido → 422 `idempotency_key_invalida`;
2. mesma rota + mesma chave + mesmo payload → retorna o mesmo status e corpo da
   primeira resposta, sem novo registro nem novo evento;
3. mesma rota + mesma chave + payload diferente → 409 `idempotencia_conflito`;
4. chaves iguais em rotas diferentes são independentes;
5. payload deve ser comparado por hash canônico documentado;
6. duas requisições simultâneas com mesma chave/payload não podem criar dois
   registros: uma constraint/transação deve garantir a atomicidade;
7. respostas de validação anteriores à criação não precisam ser armazenadas;
   documente exatamente onde começa a operação idempotente.

Crie teste concorrente real com duas chamadas simultâneas, não apenas duas
chamadas sequenciais.

## 19. Publicação em webhook

`POST /projetos/{id}/publicacao` exige `Idempotency-Key` e projeto `ativo`.
A operação cria um evento persistido na **outbox** e responde **202**:

```json
{"evento_id":"01J...","projeto_id":7,"status":"pendente"}
```

Configuração:

- `WEBHOOK_URL`: endpoint do receptor;
- `WEBHOOK_SECRET`: segredo para HMAC;
- `WEBHOOK_TIMEOUT_MS`: timeout da entrega;
- `TENTATIVAS_WEBHOOK`: lido da variante, incluindo a primeira tentativa.

Evento entregue:

```json
{
  "id": "01J...",
  "tipo": "projeto.publicado",
  "ocorrido_em": "2026-11-24T15:00:00Z",
  "projeto": {
    "id": 7,
    "titulo": "Oficina comunitária",
    "parceiro_id": 3
  }
}
```

Headers obrigatórios:

- `Content-Type: application/json`;
- `X-Event-ID`: ID do evento;
- `X-Idempotency-Key`: mesmo ID do evento;
- `X-Webhook-Timestamp`: instante da tentativa;
- `X-Webhook-Signature`: `sha256=<hmac_hex>` calculado sobre o corpo bruto.

### 19.1 Worker e retentativas

Implemente um comando/worker documentado que processe a outbox. Ele deve:

- manter `pendente`, `enviado` ou `falhou`, tentativas e último erro sanitizado;
- usar timeout explícito;
- considerar sucesso somente HTTP 2xx;
- repetir somente rede/timeout, 429 e 5xx;
- não repetir demais 4xx;
- usar backoff exponencial com jitter e limites documentados;
- respeitar `Retry-After` em segundos quando presente, com teto configurável;
- nunca exceder `TENTATIVAS_WEBHOOK`;
- não enviar o mesmo evento novamente após `enviado`;
- registrar tentativas sem registrar `WEBHOOK_SECRET` nem assinatura completa;
- sobreviver a reinício sem perder eventos pendentes.

A API não precisa bloquear a requisição enquanto espera backoff. O comando pode
processar lote, agendar a próxima tentativa ou ser invocado novamente; explique
a escolha no ADR.

### 19.2 Consulta do evento

`GET /integracoes/eventos/{evento_id}` → **200** com ID, projeto, status,
quantidade de tentativas, timestamps e `proxima_tentativa_em` quando aplicável.
Não exponha URL com credenciais, segredo, assinatura ou corpo completo de erro.

### 19.3 Testes obrigatórios

Use um receptor HTTP local controlado para comprovar:

- assinatura válida e inválida;
- corpo e headers;
- sucesso no primeiro envio;
- 500 e depois 200;
- 429 com `Retry-After`;
- 400 sem retry;
- timeout;
- esgotamento das tentativas;
- reinício com evento pendente;
- replay da publicação sem duplicar evento.

## 20. Persistência e concorrência

Além dos testes de idempotência, demonstre:

- dados preservados após reiniciar a aplicação com o mesmo volume/banco;
- e-mail único garantido também pelo banco;
- duas criações concorrentes com o mesmo e-mail resultam em um 201 e um 409;
- nenhum estado parcial aparece quando uma operação falha no meio;
- tratamento de erro de constraint não vaza SQL nem derruba o processo.

Lock em memória pode complementar, mas não será aceito como única garantia de
unicidade/idempotência.

---

# PARTE IV — DEBUGGING

## 21. Regras dos quatro casos

Os trechos abaixo são Python deliberadamente defeituoso. Mesmo que sua aplicação
use outra stack, resolva estes casos em Python dentro de `debug/`, usando apenas
biblioteca padrão ou dependências de teste documentadas.

Para cada caso:

1. escreva primeiro um teste que reproduza o sintoma e veja a falha;
2. registre hipótese, evidência, causa raiz e correção em `debug/diagnostico.md`;
3. faça a menor correção coerente, sem reescrever tudo sem necessidade;
4. acrescente testes de borda e regressão;
5. indique commits/PR e comandos de execução.

Não basta apontar o bug em prosa. O código corrigido e os testes são entregáveis.

## 22. D01 — Arredondamento de horas

Sintoma: relatórios apresentam tipo/formato incorreto e divergências da
planilha em valores terminados em meio.

```python
def percentual(realizadas, previstas):
    if previstas == 0:
        return 0.0
    return round((realizadas / previstas) * 100, 2)


assert percentual(2675, 10000) == "26.75"
assert percentual(535, 10000) == "5.35"
assert percentual(1, 32) == "3.13"
```

Requisitos da correção: saída string com duas casas, half-up, zero tratado e
sem usar float para o cálculo. Acrescente casos adjacentes ao arredondamento.

## 23. D02 — Paginação que perde registros

Sintoma: o primeiro registro de cada página, incluindo a primeira, desaparece.

```python
def paginar(itens, pagina=1, tamanho=10):
    inicio = (pagina - 1) * tamanho + 1
    fim = inicio + tamanho
    return {
        "dados": itens[inicio:fim],
        "pagina": pagina,
        "tamanho": tamanho,
        "total": len(itens),
    }
```

Requisitos da correção: índices corretos, página além do fim, página/tamanho
inválidos e metadados coerentes. Explique a diferença entre validar parâmetros e
retornar uma página vazia válida.

## 24. D03 — Retry indiscriminado e resposta ambígua

Sintoma: cliente recebe sucesso vazio, erros 400 são repetidos e exceções somem.

```python
import time


def entregar(cliente, url, payload):
    for tentativa in range(3):
        try:
            resposta = cliente.post(url, json=payload, timeout=None)
            if resposta.status_code >= 400:
                time.sleep(1)
                continue
            return resposta
        except Exception:
            pass
    return None
```

Requisitos da correção: timeout explícito; retry apenas para falhas transitórias;
quantidade limitada; último erro propagado de forma útil; nenhum `except` mudo;
testes com cliente simulado para 400, 429, 500, timeout e sucesso após falha.

## 25. D04 — Check-then-act sob concorrência

Sintoma: duas requisições simultâneas conseguem reservar a mesma sala.

```python
import threading
import time


class Agenda:
    def __init__(self):
        self.reservas = []

    def reservar(self, sala, inicio, fim, usuario):
        for reserva in self.reservas:
            if (reserva["sala"] == sala and inicio < reserva["fim"]
                    and fim > reserva["inicio"]):
                raise ValueError("conflito")
        time.sleep(0.05)  # simula trabalho entre validar e gravar
        self.reservas.append({
            "sala": sala,
            "inicio": inicio,
            "fim": fim,
            "usuario": usuario,
        })


def executar_teste_concorrente(agenda):
    # Duas threads chamam reservar("Lab 1", 10, 11, ...) ao mesmo tempo.
    # O teste falha se ambas conseguirem reservar.
    ...
```

Requisitos da correção: teste determinístico com barreira/sincronização; proteção
da operação completa; preservação da regra de intervalos; testes para adjacência
(`fim == inicio` permitido), salas diferentes e exceção de conflito. Explique por
que essa solução local não substitui constraint no banco da API.

---

# PARTE V — TDD, GITHUB E QUALIDADE

## 26. TDD obrigatório

Implemente pelo menos **três ciclos red–green–refactor completos**, cobrindo:

1. uma regra de CRUD/transição;
2. uma integração ou idempotência;
3. uma regra de relatório ou concorrência.

Cada ciclo deve ter:

- issue e identificador do requisito;
- commit de teste com prefixo `test(red):` e falha esperada descrita;
- commit de implementação mínima com `feat(green):` ou `fix(green):`;
- commit separado de `refactor:` quando houver melhoria, mantendo testes verdes;
- pequeno registro em `evidencias/tdd/ciclo-XX.md` com comandos, falha inicial,
  motivo da falha e resultado final;
- PR que referencia os commits e explica o ciclo.

Não é necessário deixar o CI vermelho de propósito: os Actions do template não
executam sua suíte própria. A evidência red vem do teste local e do registro. O
**HEAD final deve estar totalmente verde**.

Quantidade mínima de testes da solução inteira: **30 casos automatizados**, com
no mínimo 8 testes de integração HTTP/banco e 10 cenários negativos/borda. Esse
número é piso, não garantia de pontuação: testes triviais ou que repetem o mesmo
caminho não substituem a matriz de riscos.

## 27. Estratégia de testes

`docs/tests.md` deve conter matriz com requisito, risco, nível, entrada, resultado
e arquivo do teste. Inclua:

- caminho feliz de todos os endpoints;
- limites imediatamente abaixo, no limite e acima;
- JSON inválido e campos ausentes;
- recursos inexistentes;
- transições inválidas;
- paginação vazia, exata e além do fim;
- filtros combinados;
- persistência após reinício;
- concorrência;
- integrações com falhas;
- regressões D01–D04.

Não use cobertura percentual como único argumento de qualidade. Se medir
cobertura, explique quais ramos importantes continuam descobertos.

## 28. GitHub como processo de engenharia

A entrega deve conter, no mínimo:

- **8 issues significativas**, com contexto, aceite e ligação a RF/RN;
- **6 pull requests integrados**, preferencialmente pequenos e por fatia;
- **18 commits significativos**, sem contar apenas commits do bot/merge;
- trabalho em **3 ou mais dias diferentes**;
- branches com nomes relacionados às issues;
- PRs ligados às issues por palavras-chave de fechamento;
- descrição de PR com escopo, requisitos, testes, riscos e evidências;
- checklist de autorrevisão preenchido em cada PR;
- pelo menos uma revisão de especificação antes do PR principal de código;
- uso de `/auto-correcao` no estado final;
- nenhuma alteração em `.github/` ou nos demais caminhos protegidos.

Você pode comentar no próprio PR para registrar autorrevisão, dúvidas resolvidas
e mudanças feitas. Não finja aprovação de outro revisor nem crie contas/bots para
simular trabalho em equipe.

### 28.1 Workflows existentes

Pesquise e utilize os workflows já presentes: preparação, aplicação, trampas,
estrutura, README e nota parcial. Como `.github/` é protegido, a criação de um
workflow personalizado não faz parte desta prova. Se quiser planejar um CI futuro,
documente-o em `docs/plan.md` sem criar o arquivo de workflow.

## 29. Container e reprodutibilidade

O corretor deve conseguir executar, a partir do README, equivalentes a:

```bash
docker build -f Containerfile -t conecta-comunidade .
docker run --rm -p 8080:8080 \
  -v conecta-data:/data \
  --env-file .env.example \
  conecta-comunidade
```

O `.env.example` deve conter apenas valores fictícios/seguros. Se sua aplicação
exigir configuração antes do build/run, documente. O exemplo acima não é contrato
rígido de porta externa: a correção pode usar `PORTA_API`.

Requisitos:

- build sem arquivos locais não declarados;
- dependências fixadas de forma reproduzível;
- processo sem root quando compatível com a stack;
- `.dockerignore` sem `.git`, `.env`, caches, banco local ou evidências grandes;
- volume `/data` documentado;
- healthcheck;
- comando de testes também executável fora do container;
- nenhuma dependência de internet durante os testes.

## 30. Segurança, logs e dados

- valide entrada no limite da aplicação;
- use queries parametrizadas/ORM seguro;
- não registre payloads inteiros de endereço ou segredos;
- proteja configuração de webhook e trate URL insegura conforme ADR;
- não exponha stack trace;
- não adicione autenticação fictícia apenas para parecer completa; se não houver
  autenticação, registre como limitação e risco da primeira versão;
- use somente pessoas, e-mails e organizações fictícios em fixtures/exemplos.

---

# PARTE VI — VALIDAÇÃO FINAL

## 31. Roteiro mínimo de aceite

Além dos testes automatizados, deixe um roteiro executável para estes cenários:

1. criar parceiro com mock de CEP e recuperá-lo após reinício;
2. rejeitar e-mail duplicado sequencial e concorrente;
3. criar projeto com chave de idempotência e repetir sem duplicar;
4. reutilizar a chave com payload diferente e receber 409;
5. tentar ativar projeto sem atividade e observar a regra;
6. planejar atividade, ativar, concluir e consultar relatório;
7. impedir edição/cancelamento de atividade concluída;
8. encerrar somente sem atividades planejadas;
9. desativar parceiro sem projeto ativo e impedir novo projeto;
10. publicar projeto, validar webhook assinado e consultar evento;
11. simular 500/429/timeout sem duplicar ou perder evento;
12. executar os quatro testes de regressão de debugging.

## 32. Checklist de entrega por critério

### A — SDD e arquitetura (15)

- [ ] Requisitos e regras têm IDs e critérios mensuráveis.
- [ ] Há rastreabilidade até testes, arquivos, issues e PRs.
- [ ] OpenAPI cobre endpoints, schemas, headers e Problem Details.
- [ ] Modelo de dados mostra relacionamentos e constraints.
- [ ] Cinco ADRs têm contexto, alternativas, decisão e consequências.
- [ ] Plano e tarefas correspondem ao que foi realmente executado.

### B — CRUD e regras (20)

- [ ] CRUDs e consultas estão completos.
- [ ] Todas as RN-P, RN-J e RN-A foram implementadas.
- [ ] Paginação, filtros e ordenação funcionam juntos.
- [ ] Relatório usa inteiros e arredondamento correto.
- [ ] Persistência sobrevive a reinício.

### C — TDD e testes (15)

- [ ] Três ciclos red–green–refactor são verificáveis.
- [ ] Há pelo menos 30 testes significativos.
- [ ] Integração, concorrência, negativos e bordas estão cobertos.
- [ ] Testes são independentes de internet e podem rodar em qualquer ordem.
- [ ] HEAD final está verde.

### D — Debugging (10)

- [ ] D01–D04 têm teste que falhava antes.
- [ ] Diagnóstico diferencia sintoma e causa raiz.
- [ ] Correções são mínimas e testadas.
- [ ] Regressões e bordas foram adicionadas.

### E — Integrações (15)

- [ ] ViaCEP tem mock, timeout, falhas e atomicidade.
- [ ] Idempotência é persistida e segura sob concorrência.
- [ ] Outbox sobrevive a reinício.
- [ ] Webhook tem HMAC, timeout e retentativas seletivas.
- [ ] Não há segredos ou dados sensíveis em logs.

### F — GitHub e SDLC (10)

- [ ] Issues, branches, PRs e commits contam uma história coerente.
- [ ] Há trabalho real em três ou mais dias.
- [ ] PRs têm revisão, testes e ligação aos requisitos.
- [ ] Nenhum caminho protegido foi alterado.
- [ ] `/auto-correcao` foi executado no estado final.

### G — Pesquisa (5)

- [ ] Pelo menos 12 missões foram investigadas.
- [ ] Há 15 fontes, 8 primárias e 6 comparações entre fontes.
- [ ] Dez aplicações práticas são localizáveis.
- [ ] FONTES.md está completo e no formato exigido.

### Containerfile e README (10)

- [ ] Build/run limpos, volume, healthcheck e não root quando aplicável.
- [ ] README contém execução, configuração, testes, mocks e limitações.
- [ ] `.env.example` não contém segredo real.
- [ ] O README não permaneceu igual ao texto da prova.

## 33. Preparação para a entrevista

Na entrevista, você poderá ser solicitado a:

- abrir um requisito e seguir seus links até teste, código e PR;
- explicar por que um teste falhava antes da correção;
- executar a suíte e o container;
- simular uma falha da ViaCEP ou do webhook;
- mostrar onde a atomicidade/idempotência é garantida;
- explicar um ADR e uma alternativa rejeitada;
- fazer uma pequena alteração com teste, sem agente de IA;
- analisar um trecho do próprio histórico e propor uma melhoria.

Leve ambiente local funcionando e dependências previamente instaladas. A
entrevista não é uma nova semana de desenvolvimento: ela verifica compreensão,
autoria, raciocínio e capacidade de trabalhar sobre o que foi entregue.
