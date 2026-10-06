# Prova teste — Hello World

> Esta é a **sua prova-teste**: no momento da aplicação, esta pasta virou o
> seu repositório (contrato, rubrica e testes públicos estão na raiz). O
> esqueleto com os workflows de correção continua aqui, por trás. O objetivo
> é treinar o ciclo de entrega com o exercício mais simples possível: **um
> hello world em Python**.

Você implementa um servidor minúsculo (só stdlib, sem pip) que saúda quem
chama; a **suíte de testes define o contrato** (`contrato.json`) e confere a
saudação com os parâmetros **da sua variante** — derivados do nome do seu
repositório, então copiar de colega não funciona.

## O que vale nesta prova-teste

| Critério | Pontos |
| --- | --- |
| Testes públicos (5, em `tests/public/` — saudação da variante, defaults, validação, `src/`, `FONTES.md`) | 70 |
| Dockerfile funcional (suíte sobe sem ajustes — `EXPOSE 8080` + comando de execução) | 20 |
| README com instruções de subida (local e container) | 10 |
| **Total** | **100** |

> Sem pontos extras e sem suíte escondida nesta prova-teste — a nota do CI já
> é a nota desta prova-teste. Nas provas reais, a nota do CI é **parcial**: a
> suíte escondida não roda no CI do aluno e a nota definitiva é apurada pelo
> professor fora dele — correção manual ou via Actions do repo privado do
> professor, com a data de criação dos testes verificável pelos alunos.

## Suas ferramentas neste repo

- **Contrato**: `contrato.json` (endpoints, regras da saudação, variante)
- **Sua variante**: `variante/params.json` (gerada na aplicação; única do seu repo)
- **Testes públicos**: `bash scripts/rodar_testes.sh` (requer Docker)
- **Nota**: a cada push, no Summary do workflow *Auto-correção*
- **Regras e rastreabilidade**: `docs/REGRAS.md` e `FONTES.md`

## Regras da prova-teste

- **Janela**: 120 minutos (1h30), contados a partir do commit de aplicação
  ("chore: aplicar prova …", feito pelo bot). O relógio já está rodando —
  dê push antes do fim da janela.
- **Consulta é permitida — rastreabilidade obrigatória**: qualquer site ou IA
  usados vão para `FONTES.md` (URL/link + onde aparece no entregável). Se não
  usou nada, declare isso explicitamente lá.
- **IA como agente é proibida** (IA que edita arquivos ou executa comandos no
  seu lugar → nota 0, plágio). IA como consulta, com a conversa pública e
  registrada em `FONTES.md`, é permitida.
- **Não altere** `scripts/`, `.github/` ou `docs/` (conferido contra o
  template) nem `track.json`/`contrato.json`/`rubrica.json` depois da
  aplicação (conferido contra o commit de aplicação) — prova zerada.

## Agora

1. Leia `contrato.json` **inteiro** antes de codar (são dois endpoints).
2. Implemente em `src/app.py` (apague o `TODO`) + confira o `Dockerfile`.
3. Rode `bash scripts/rodar_testes.sh` localmente (requer Docker) e veja os
   5 testes passarem.
4. Commits pequenos, push antes do fim da janela. Boa prova! 🚀
