#!/usr/bin/env python3
"""Bootstrap idempotente — roda no primeiro push apos "Use this template".

Nao existe evento "template usado" no GitHub Actions: a geracao do repo a
partir do template cria um commit inicial que dispara `push`. Este script se
reconhece pelo arquivo-sentinela `.prova/setup-done`.

Versao exam-escola-ti (template unico): NAO gera variante aqui — a prova
( pasta do ano com os parametros) so existe no dia da prova, aplicada por
`aplicar_prova.py`. O setup cria: identidade (.prova/id), ALUNO.md com o
botao "Iniciar a prova", README.md de primeiros passos (substituido pelo
overlay na aplicacao), a ISSUE UNICA da prova ("🎯 Prova", numero gravado em
`.prova/issue` — lock que todos os workflows usam para comentar na issue
certa) e o comentario de boas-vindas LISTANDO as provas disponiveis
(candidatas via scripts/selecao.py — fetch no template, publico sem PAT).

DRY_RUN=1 executa localmente sem API/push (para teste).
"""
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "scripts"))
import selecao  # noqa: E402

TOKEN = os.environ.get("GH_TOKEN", "")
REPO_FULL = os.environ.get("REPO_FULL", "")
OWNER = REPO_FULL.split("/")[0] if "/" in REPO_FULL else ""
REPO = os.environ.get("REPO_SLUG") or os.path.basename(BASE)
TEMPLATE_URL = os.environ.get(
    "TEMPLATE_URL", "https://github.com/endersonmenezes/exam-escola-ti.git")
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


def url_issue(numero_issue):
    return "https://github.com/%s/issues/%d" % (REPO_FULL, numero_issue)


def badge(numero_issue):
    return ("[![🎯 Iniciar a prova](https://img.shields.io/badge/"
            "🎯%20Iniciar%20a%20prova-clique%20aqui-2ea44f)]("
            + url_issue(numero_issue) + ")")


def readme_primeiros_passos(numero_issue):
    url = url_issue(numero_issue)
    return (badge(numero_issue) + "\n\n"
            "# Sua prova — primeiros passos\n\n"
            "1. **Edite `ALUNO.md`** com seu nome/RA (o workflow valida).\n"
            "2. **Abra a [issue 🎯 Prova]("+url+")** — é nela que tudo "
            "acontece.\n"
            "3. **Selecione sua prova** comentando `/track <nome>` na issue "
            "(a lista está no comentário de boas-vindas).\n"
            "4. A prova é aplicada no repo (overlay); desenvolva e dê push.\n"
            "5. **Feche a issue para encerrar** — o sistema gera o "
            "`teacher.json` de entrega.\n")


def comentario_boas_vindas(numero_issue, candidatas):
    linhas = ["⚙️ **Setup automático concluído.** Repositório: `%s`" % REPO,
              "",
              "Esta é a **issue única da sua prova**: preparação, seleção da "
              "track (`/track <nome-da-pasta>`), aplicação, nota parcial e "
              "fechamento acontecem aqui. O relógio da janela começa no "
              "commit de aplicação. Ao final, **você fecha esta issue** para "
              "encerrar a prova — o sistema gera o `teacher.json` de entrega.",
              "",
              "**Provas disponíveis:**"]
    for pasta in candidatas:
        nome = os.path.basename(pasta)
        if pasta == selecao.DUMMY:
            linhas.append("- `%s` — prova-teste (modo sandbox, para conhecer "
                          "o sistema)" % nome)
        else:
            linhas.append("- `%s`" % nome)
    linhas += ["", "Selecione comentando `/track <nome>` nesta issue."]
    return "\n".join(linhas)


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

    # 2) provas disponiveis (fetch no template; sem PAT). Se o fetch falhar,
    #    lista so o dummy permanente — conhecido de antemao.
    candidatas = [selecao.DUMMY]
    if selecao.fetch_template(TEMPLATE_URL):
        candidatas = selecao.candidatas(selecao.pastas_publicadas("FETCH_HEAD"))
        print("Provas disponiveis:", ", ".join(candidatas))
    else:
        print("Template indisponivel (%s) — listando so o dummy." % TEMPLATE_URL)

    # 3) ISSUE UNICA da prova — criada ANTES do commit para o lock
    #    .prova/issue entrar no mesmo commit do bot.
    numero_issue = None
    if DRY_RUN or not TOKEN:
        print("DRY_RUN — issue nao criada.")
    else:
        api("POST", "/repos/%s/labels" % REPO_FULL,
            {"name": "prova", "color": "1d76db", "description": "Issue oficial da prova"})
        corpo = """## Checklist do aluno

- [ ] Meu `ALUNO.md` esta com **Nome e RA** corretos (o bot preencheu o nome pela sua conta GitHub — confira!)
- [ ] Li as [regras comuns](docs/REGRAS.md) e sei o que precisa declarar em `FONTES.md`
- [ ] Sei que a pasta da prova ainda nao foi publicada — quando o professor publicar, o bot puxa a pasta escolhida (`exams/<ano>/<track>/`, ou a prova-teste `dummy-exam`) e ela **vira meu repositorio** (README, contrato e testes novos); o relogio da janela comeca no commit de aplicacao
- [ ] Confirmo que vou entregar com commits **dentro da janela** contada a partir desse commit de aplicacao

## Selecao da track (obrigatoria)

Comente `/track <nome-da-pasta>` **nesta issue** para escolher qual prova aplicar (a lista de disponiveis esta no comentario de boas-vindas). Para treinar o ciclo com a prova-teste: `/track dummy-exam` — a aplicacao acontece automaticamente em seguida.

Ao marcar as caixas (ou comentar), o workflow **Preparar entrega** valida e responde aqui. A prova se encerra quando **voce fechar esta issue** — nesse momento o sistema gera o `teacher.json` de entrega. Duvidas? Comente aqui.
"""
        status, issue = api("POST", "/repos/%s/issues" % REPO_FULL,
                            {"title": "🎯 Prova", "body": corpo,
                             "labels": ["prova"]})
        if status == 201:
            numero_issue = issue["number"]
            with open(os.path.join(BASE, ".prova", "issue"), "w",
                      encoding="utf-8") as f:
                f.write("%d\n" % numero_issue)
            print("Issue #%d criada (lock .prova/issue)." % numero_issue)
        else:
            print("Falha ao criar issue (status %d)." % status)

    # 4) ALUNO.md pre-preenchido com a conta do dono do repo + botao da issue
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
        topo = (badge(numero_issue) + "\n\n") if numero_issue else ""
        with open(aluno_path, "w", encoding="utf-8") as f:
            f.write(topo +
                    "# ALUNO\n\n"
                    "Nome: %s\n\n"
                    "RA: \x3e\x3e\x3e PREENCHER \x3c\x3c\x3c\n\n"
                    "Conta GitHub: @%s\n\n"
                    "\x3e Pre-preenchido pelo setup a partir da conta GitHub do "
                    "dono do repositorio. Confira o nome e complete o RA.\n"
                    % (nome_conta, login))

    # 5) README.md de primeiros passos (pre-aplicacao; o overlay substitui)
    if numero_issue:
        with open(os.path.join(BASE, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme_primeiros_passos(numero_issue))
        print("README.md de primeiros passos escrito (botao da issue #%d)."
              % numero_issue)

    # 6) sentinela
    with open(sentinela, "w", encoding="utf-8") as f:
        f.write("ok\n")

    # 7) commit + push como bot (inclui ALUNO.md, README.md, .prova/*)
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

    # 8) comentario de boas-vindas na issue da prova, LISTANDO as provas
    if numero_issue:
        api("POST", "/repos/%s/issues/%d/comments" % (REPO_FULL, numero_issue),
            {"body": comentario_boas_vindas(numero_issue, candidatas)})
        print("Comentario de boas-vindas postado na issue #%d." % numero_issue)


if __name__ == "__main__":
    main()
