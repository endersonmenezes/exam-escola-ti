#!/usr/bin/env python3
"""Reage a edicoes/comentarios na ISSUE UNICA da prova (lock .prova/issue).

Valida a preparacao (ALUNO.md com RA, identidade, FONTES.md) e — se a prova
ja foi aplicada — a variante, e responde NA PROPRIA ISSUE (upsert de estado
via comentario; NAO fecha: o fechamento encerra a prova — ver
scripts/fechar_prova.py). Mantem o parse de `/track <nome>` que grava
`.prova/track` (commit de bot).

No-op silencioso se a issue do evento nao for a da prova.
"""
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "scripts"))
from variante import slug_do_repo, pasta_do_ano, variante  # noqa: E402
import prova_issue  # noqa: E402

TOKEN = os.environ.get("GH_TOKEN", "")
REPO_FULL = os.environ.get("REPO_FULL", "")
NUMERO = os.environ.get("ISSUE_NUMBER", "")
REPO = os.environ.get("REPO_SLUG") or slug_do_repo()


def api(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request("https://api.github.com" + path,
                                 data=data, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Accept", "application/vnd.github+json")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError:
        return 0, {}


def main():
    if os.environ.get("REPO_FULL", "") == "endersonmenezes/exam-escola-ti":
        print("Repositorio-template — nao e uma prova; no-op.")
        return

    lock = prova_issue.numero()
    if lock is None:
        print("Lock .prova/issue ausente (setup nao rodou?) — no-op.")
        return
    if NUMERO:
        try:
            if int(NUMERO) != lock:
                print("Nao e a issue da prova (evento #%s != lock #%s) — no-op."
                      % (NUMERO, lock))
                return
        except ValueError:
            print("ISSUE_NUMBER invalido (%s) — no-op." % NUMERO)
            return

    ok = []

    # 0) Selecao de track (issueops): comentario "/track <nome>" grava .prova/track
    status_c, comentarios = api("GET", "/repos/%s/issues/%s/comments?per_page=100"
                                % (REPO_FULL, lock))
    track_escolhida = None
    if status_c == 200:
        for c in comentarios:
            m = re.search(r"(?im)^\s*/track\s+([\w-]+)", c.get("body", ""))
            if m:
                track_escolhida = m.group(1)
    if track_escolhida:
        track_path = os.path.join(BASE, ".prova", "track")
        atual = ""
        if os.path.exists(track_path):
            atual = open(track_path, encoding="utf-8").read().strip()
        if atual != track_escolhida:
            os.makedirs(os.path.dirname(track_path), exist_ok=True)
            with open(track_path, "w", encoding="utf-8") as f:
                f.write(track_escolhida + "\n")
            subprocess.run(["git", "config", "user.name", "github-actions[bot]"],
                           cwd=BASE, capture_output=True)
            subprocess.run(["git", "config", "user.email",
                            "41898282+github-actions[bot]@users.noreply.github.com"],
                           cwd=BASE, capture_output=True)
            subprocess.run(["git", "pull", "--rebase"], cwd=BASE, capture_output=True)
            subprocess.run(["git", "add", ".prova/track"], cwd=BASE, capture_output=True)
            subprocess.run(["git", "commit", "-m",
                            "chore: track selecionada via issue (%s)" % track_escolhida],
                           cwd=BASE, capture_output=True)
            subprocess.run(["git", "push"], cwd=BASE, capture_output=True)
        ok.append("✅ track `%s` gravada em `.prova/track`" % track_escolhida)

    # 1) ALUNO.md com RA
    aluno_path = os.path.join(BASE, "ALUNO.md")
    if not os.path.exists(aluno_path):
        ok.append("❌ `ALUNO.md` ausente — algo falhou no setup; comente aqui para o professor ver.")
    else:
        texto = open(aluno_path, encoding="utf-8", errors="replace").read()
        if re.search(r"RA\s*[:：]?\s*[0-9]{5,}", texto) and "PREENCHER" not in texto:
            ok.append("✅ `ALUNO.md` com RA válido")
        else:
            ok.append("❌ `ALUNO.md` sem RA válido — preencha e commite.")

    # 2) identidade
    id_path = os.path.join(BASE, ".prova", "id")
    if os.path.exists(id_path) and open(id_path, encoding="utf-8").read().strip() == REPO:
        ok.append("✅ identidade da prova confere com o repositório")
    else:
        ok.append("❌ `.prova/id` ausente ou divergente — rode `python scripts/variante.py`.")

    # 3) FONTES.md
    if os.path.exists(os.path.join(BASE, "FONTES.md")):
        ok.append("✅ `FONTES.md` presente")
    else:
        ok.append("❌ `FONTES.md` ausente — restaure o do template.")

    # 4) variante (só depois da aplicação)
    pasta = pasta_do_ano(BASE)
    if pasta:
        esperado = variante(REPO)
        params_path = os.path.join(BASE, "variante", "params.json")
        if os.path.exists(params_path):
            gravado = json.load(open(params_path, encoding="utf-8"))
            diffs = [k for k in esperado if gravado.get(k) != esperado[k]]
            ok.append("✅ variante coerente (pasta `%s`)" % pasta if not diffs
                      else "❌ `variante/params.json` diverge em: %s" % ", ".join(diffs))
        else:
            ok.append("❌ `variante/params.json` ausente — rode `python scripts/variante.py`.")
    else:
        ok.append("⏳ prova ainda não aplicada — a variante será validada no dia da prova")

    faltam = [l for l in ok if l.startswith("❌")]
    if faltam:
        corpo = ("🔎 **Preparação incompleta**:\n\n" + "\n".join(ok)
                 + "\n\nResolva os ❌ e marque os checkboxes de novo; eu revalido. 💪")
    else:
        corpo = ("✅ **Preparação em dia!**\n\n" + "\n".join(ok)
                 + "\n\nQuando a prova for aplicada (commit *aplicar prova*), a "
                   "janela definida na rubrica começa a contar. Para escolher a "
                   "track, comente `/track <nome>` aqui. Boa prova! 🚀")

    prova_issue.comentar(corpo)
    print("Respondido na issue #%s (%s)." % (lock, "ok" if not faltam else "pendencias"))


if __name__ == "__main__":
    main()
