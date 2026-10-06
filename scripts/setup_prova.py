#!/usr/bin/env python3
"""Bootstrap idempotente — roda no primeiro push apos "Use this template".

Nao existe evento "template usado" no GitHub Actions: a geracao do repo a
partir do template cria um commit inicial que dispara `push`. Este script se
reconhece pelo arquivo-sentinela `.prova/setup-done`.

Versao exam-escola-ti (template unico): NAO gera variante aqui — a prova
( pasta do ano com os parametros) so existe no dia da prova, aplicada por
`aplicar_prova.py`. O setup cria apenas identidade + ALUNO.md + issue.

DRY_RUN=1 executa localmente sem API/push (para teste).
"""
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TOKEN = os.environ.get("GH_TOKEN", "")
REPO_FULL = os.environ.get("REPO_FULL", "")
OWNER = REPO_FULL.split("/")[0] if "/" in REPO_FULL else ""
REPO = os.environ.get("REPO_SLUG") or os.path.basename(BASE)
DRY_RUN = os.environ.get("DRY_RUN", "") == "1"


def api(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request("https://api.github.com" + path,
                                 data=data, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Accept", "application/vnd.github+json")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, {}


def git(*args):
    return subprocess.run(["git"] + list(args), cwd=BASE,
                          capture_output=True, text=True)


def main():
    if os.environ.get("REPO_FULL", "") == "endersonmenezes/exam-escola-ti":
        print("Repositorio-template — nao e uma prova; no-op.")
        return

    sentinela = os.path.join(BASE, ".prova", "setup-done")
    if os.path.exists(sentinela):
        print("Setup ja realizado (.prova/setup-done existe) — no-op.")
        return

    # 1) identidade do repo (a variante so existe apos a aplicacao da prova)
    os.makedirs(os.path.join(BASE, ".prova"), exist_ok=True)
    with open(os.path.join(BASE, ".prova", "id"), "w", encoding="utf-8") as f:
        f.write(REPO + "\n")

    # 2) ALUNO.md pre-preenchido com a conta do dono do repo
    login = os.environ.get("REPO_OWNER_LOGIN", "")
    nome_conta = login
    if not DRY_RUN and TOKEN and REPO_FULL:
        status, repo = api("GET", "/repos/%s" % REPO_FULL)
        if status == 200:
            login = repo.get("owner", {}).get("login", login)
            status2, user = api("GET", "/users/%s" % login)
            if status2 == 200:
                nome_conta = user.get("name") or login
    aluno_path = os.path.join(BASE, "ALUNO.md")
    if not os.path.exists(aluno_path):
        with open(aluno_path, "w", encoding="utf-8") as f:
            f.write("# ALUNO\n\n"
                    "Nome: %s\n\n"
                    "RA: \x3e\x3e\x3e PREENCHER \x3c\x3c\x3c\n\n"
                    "Conta GitHub: @%s\n\n"
                    "\x3e Pre-preenchido pelo setup a partir da conta GitHub do "
                    "dono do repositorio. Confira o nome e complete o RA.\n"
                    % (nome_conta, login))

    # 3) sentinela
    with open(sentinela, "w", encoding="utf-8") as f:
        f.write("ok\n")

    # 4) commit + push como bot
    git("config", "user.name", "github-actions[bot]")
    git("config", "user.email",
        "41898282+github-actions[bot]@users.noreply.github.com")
    git("add", "-A")
    if git("diff", "--cached", "--quiet").returncode == 0:
        print("Nada a commitar.")
    else:
        git("commit", "-m", "chore: setup inicial da prova (bot)")
        if not DRY_RUN:
            git("pull", "--rebase")
            r = git("push")
            if r.returncode != 0:
                print("push falhou (continuando):", r.stderr)

    # 5) issue "Preparar entrega"
    if DRY_RUN or not TOKEN:
        print("DRY_RUN — issue nao criada.")
        return

    api("POST", "/repos/%s/labels" % REPO_FULL,
        {"name": "prova", "color": "1d76db", "description": "Issue oficial da prova"})
    corpo = """## Checklist do aluno

- [ ] Meu `ALUNO.md` esta com **Nome e RA** corretos (o bot preencheu o nome pela sua conta GitHub — confira!)
- [ ] Li as [regras comuns](docs/REGRAS.md) e sei o que precisa declarar em `FONTES.md`
- [ ] Sei que a **pasta da prova ainda nao foi publicada** — no dia da prova o bot puxa minha track (`exams/<ano>/<track>/`) e ela **vira meu repositorio** (README, contrato e testes novos); o relogio da janela comeca no commit de aplicacao
- [ ] Confirmo que vou entregar com commits **dentro da janela** contada a partir desse commit de aplicacao

Ao marcar as caixas (ou comentar aqui), o workflow **Preparar entrega** valida
e responde nesta mesma issue. Duvidas? Comente aqui.
"""
    status, issue = api("POST", "/repos/%s/issues" % REPO_FULL,
                        {"title": "🎯 Preparar entrega — prova",
                         "body": corpo, "labels": ["prova"]})
    if status == 201:
        api("POST", "/repos/%s/issues/%d/comments" % (REPO_FULL, issue["number"]),
            {"body": "⚙️ **Setup automatico concluido.** Repositorio: `%s`\n\n"
                     "A prova ainda **nao** foi publicada no template. Quando o "
                     "professor publicar a pasta do ano, o workflow *Aplicar "
                     "prova* puxa os arquivos para ca sozinho e abre a issue "
                     "da prova com seus parametros." % REPO})
        print("Issue #%d criada." % issue["number"])
    else:
        print("Falha ao criar issue (status %d)." % status)


if __name__ == "__main__":
    main()
