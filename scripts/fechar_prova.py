#!/usr/bin/env python3
"""Fechamento da issue da prova -> teacher.json (handshake com o repo teacher).

Gatilho: issues closed. So age se a issue fechada for a do lock
(`.prova/issue` — ver scripts/prova_issue.py); issue de organizacao do aluno
-> no-op. Gera `teacher.json` (schema 1) na RAIZ, com commit do bot + push,
comenta a confirmacao na propria issue (comentario funciona em issue fechada)
e ainda escreve o JSON no Step Summary.

Se a prova nunca foi aplicada, gera o arquivo do mesmo jeito, com
`"aplicada": false` + motivo — fechar sem aplicar e caso real.

DRY_RUN=1 gera o arquivo local sem commit/push/comentario (para teste).
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "scripts"))
from variante import pasta_do_ano  # noqa: E402
import prova_issue  # noqa: E402

TOKEN = os.environ.get("GH_TOKEN", "")
REPO_FULL = os.environ.get("REPO_FULL", "")
REPO = os.environ.get("REPO_SLUG") or os.path.basename(BASE)
ISSUE_NUMBER = os.environ.get("ISSUE_NUMBER", "")
ISSUE_CLOSED_AT = os.environ.get("ISSUE_CLOSED_AT", "")
OWNER = os.environ.get("REPO_OWNER", "")
DRY_RUN = os.environ.get("DRY_RUN", "") == "1"


def sh(*args):
    return subprocess.run(list(args), capture_output=True, text=True,
                          cwd=BASE).stdout


def eh_bot(linha):
    alvo = linha.lower()
    return any(m in alvo for m in ("github-actions", "[bot]",
                                   "noreply@github", "dependabot"))


def iso_agora():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def main():
    if REPO_FULL == "endersonmenezes/exam-escola-ti":
        print("Repositorio-template — nao e uma prova; no-op.")
        return

    lock = prova_issue.numero()
    if not lock or not ISSUE_NUMBER:
        print("Sem lock (.prova/issue) ou sem ISSUE_NUMBER — no-op.")
        return
    try:
        if int(ISSUE_NUMBER) != lock:
            print("Issue fechada (#%s) nao e a da prova (lock #%s) — no-op."
                  % (ISSUE_NUMBER, lock))
            return
    except ValueError:
        print("ISSUE_NUMBER invalido (%s) — no-op." % ISSUE_NUMBER)
        return

    gerado_em = iso_agora()

    # ---- prova aplicada? ----
    pasta = pasta_do_ano(BASE)
    track = None
    track_path = os.path.join(BASE, "track.json")
    if os.path.exists(track_path):
        try:
            track = json.load(open(track_path, encoding="utf-8")).get("track")
        except ValueError:
            pass
    t0 = sh("git", "log", "--grep=aplicar prova", "--format=%ad",
            "--date=iso-strict", "-1").strip()
    aplicada = bool(pasta and t0)
    motivo = None
    if not aplicada:
        motivo = ("prova nunca aplicada neste repositorio (sem pasta do ano "
                  "ou sem commit 'aplicar prova')")

    # ---- aluno ----
    ra = None
    aluno_path = os.path.join(BASE, "ALUNO.md")
    if os.path.exists(aluno_path):
        m = re.search(r"RA\s*[:：]?\s*([0-9]{5,})",
                      open(aluno_path, encoding="utf-8", errors="replace").read())
        if m:
            ra = m.group(1)

    # ---- variante ----
    variante_d = None
    params_path = os.path.join(BASE, "variante", "params.json")
    if os.path.exists(params_path):
        try:
            variante_d = json.load(open(params_path, encoding="utf-8"))
        except ValueError:
            pass

    # ---- janela + commits (bot nao conta) ----
    minutos = 120
    rubrica_path = os.path.join(BASE, "rubrica.json")
    if os.path.exists(rubrica_path):
        try:
            minutos = int(json.load(open(rubrica_path, encoding="utf-8"))
                          .get("janela_minutos", 120))
        except Exception:
            pass
    log = sh("git", "log", "--format=%an|%ad", "--date=iso-strict")
    todos = [l for l in log.splitlines() if l.strip()]
    commits_aluno = [l for l in todos if not eh_bot(l)]
    datas = [l.split("|")[1] for l in commits_aluno if "|" in l]
    ultimo_push = datas[0] if datas else None
    primeiro = datas[-1] if datas else None
    autores = sorted({l.split("|")[0] for l in commits_aluno if "|" in l})
    fora = 0
    if t0:
        try:
            t0dt = datetime.fromisoformat(t0)
            fim = t0dt + timedelta(minutes=minutos)
            fora = sum(1 for d in datas
                       if not (t0dt <= datetime.fromisoformat(d) <= fim))
        except ValueError:
            fora = 0

    # ---- nota parcial (só existe na raiz se alguem a colocou; gitignored) ----
    valor, criterios = None, {}
    nota_path = os.path.join(BASE, "nota.json")
    if os.path.exists(nota_path):
        try:
            nd = json.load(open(nota_path, encoding="utf-8"))
            valor = nd.get("nota")
            criterios = {c.get("criterio", c.get("job", "?")): c.get("pontos", 0)
                         for c in nd.get("criterios", [])}
        except ValueError:
            pass
    if valor is None:
        import glob
        for path in sorted(glob.glob(os.path.join(BASE, "result-*.json"))):
            try:
                rd = json.load(open(path, encoding="utf-8"))
            except ValueError:
                continue
            if "pontos" in rd:
                criterios[rd.get("criterio", rd.get("job", "?"))] = rd.get("pontos", 0)
                valor = (valor or 0) + rd.get("pontos", 0)
            for c in rd.get("criterios", []):
                criterios[c.get("criterio", "?")] = c.get("pontos", 0)
                valor = (valor or 0) + c.get("pontos", 0)

    # ---- fontes ----
    presente = os.path.exists(os.path.join(BASE, "FONTES.md"))
    declarou_vazio, links = False, 0
    if presente:
        texto = open(os.path.join(BASE, "FONTES.md"), encoding="utf-8",
                     errors="replace").read()
        linhas = texto.splitlines()
        declarou_vazio = any(re.match(r"^\W{0,3}\s*Nenhum", l)
                             and ("utilizada" in l.lower()
                                  or "consultado" in l.lower()) for l in linhas)
        links = len(re.findall(r"https?://\S+", texto))

    teacher = {
        "schema": 1,
        "repo": REPO,
        "repo_url": "https://github.com/" + REPO_FULL if REPO_FULL else None,
        "exam_dir": pasta,
        "track": track,
        "issue": lock,
        "issue_url": ("https://github.com/%s/issues/%d" % (REPO_FULL, lock)
                      if REPO_FULL else None),
        "gerado_em": gerado_em,
        "fechada_em": ISSUE_CLOSED_AT or gerado_em,
        "aplicada": aplicada,
        "motivo": motivo,
        "aluno": {"login": OWNER or None, "ra": ra},
        "variante": variante_d,
        "janela": {"minutos": minutos, "t0": t0 or None, "ultimo_push": ultimo_push},
        "commits": {"total": len(commits_aluno), "autores": autores,
                    "primeiro": primeiro, "ultimo": ultimo_push,
                    "fora_da_janela": fora},
        "nota_parcial": {"valor": valor, "criterios": criterios},
        "fontes": {"presente": presente, "declarou_vazio": declarou_vazio,
                   "links": links},
    }

    with open(os.path.join(BASE, "teacher.json"), "w", encoding="utf-8") as f:
        json.dump(teacher, f, ensure_ascii=False, indent=2)
    print(json.dumps(teacher, ensure_ascii=False, indent=2))

    if DRY_RUN:
        print("DRY_RUN — teacher.json gerado local; sem commit/push/comentario.")
        return

    # commit do bot + push
    subprocess.run(["git", "config", "user.name", "github-actions[bot]"],
                   cwd=BASE, capture_output=True)
    subprocess.run(["git", "config", "user.email",
                    "41898282+github-actions[bot]@users.noreply.github.com"],
                   cwd=BASE, capture_output=True)
    subprocess.run(["git", "add", "teacher.json"], cwd=BASE, capture_output=True)
    subprocess.run(["git", "commit", "-m",
                    "chore: fechar prova (teacher.json)"], cwd=BASE,
                   capture_output=True)
    subprocess.run(["git", "pull", "--rebase"], cwd=BASE, capture_output=True)
    r = subprocess.run(["git", "push"], cwd=BASE, capture_output=True, text=True)
    if r.returncode != 0:
        print("push do teacher.json falhou:", r.stderr.strip())

    prova_issue.comentar(
        "🏁 **Prova encerrada.** `teacher.json` (schema 1) gerado e commitado "
        "neste repositorio — ele e o handshake de entrega para a correção. "
        "Obrigado!")

    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("## teacher.json\n\n```json\n" +
                    json.dumps(teacher, ensure_ascii=False, indent=2) +
                    "\n```\n")


if __name__ == "__main__":
    main()
