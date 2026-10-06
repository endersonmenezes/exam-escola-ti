# Prova — Track CRUD fullstack

> Esta é a **sua prova**: no momento da aplicação, esta pasta virou o seu
> repositório (contrato, rubrica e testes públicos estão na raiz). O esqueleto
> com os workflows de correção continua aqui, por trás.

Estilo juiz online: a **suíte de testes define o contrato** (`contrato.json`).
Você implementa a **API + frontend** na stack de sua escolha; a correção sobe
seu código em container e executa testes contra ele.

## O que vale nesta prova

| Critério | Pontos |
| --- | --- |
| Testes públicos (3, em `tests/public/` — incluem o **frontend básico**) | 30 |
| Testes escondidos (proporção dos que passarem, rodam só na correção) | 55 |
| Dockerfile funcional (suíte sobe sem ajustes) | 10 |
| README com instruções de subida (local e container) | 5 |
| **Extras** — frontend avançado (estados, polling, responsivo, a11y, e2e) | **+10** |

A nota final é `min(100 + 10, base + extras)`. Frontend básico é obrigatório e
já é testado; avançar rende pontos. Veja `contrato.json → frontend`.

## Suas ferramentas neste repo

- **Contrato**: `contrato.json` (endpoints, regras, frontend, variante)
- **Sua variante**: `variante/params.json` (gerada na aplicação; única do seu repo)
- **Testes públicos**: `bash scripts/rodar_testes.sh` (requer Docker)
- **Nota parcial**: a cada push, no Summary do workflow *Auto-correção*
- **Regras e rastreabilidade**: `docs/REGRAS.md` e `FONTES.md`

## Agora

1. Leia `contrato.json` **inteiro** antes de codar.
2. Implemente em `src/` + complete o `Dockerfile` (API escuta na 8080; o
   frontend é servido em `GET /` pelo mesmo container).
3. Commits pequenos, push antes do fim da janela — o relógio começou no
   commit de aplicação da prova. Boa prova! 🚀
