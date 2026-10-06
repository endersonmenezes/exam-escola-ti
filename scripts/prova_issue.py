#!/usr/bin/env python3
"""Issue unica da prova — helper compartilhado (lock em .prova/issue).

O setup cria UMA issue "🎯 Prova" que vive durante todo o ciclo (preparacao,
selecao, aplicacao, nota parcial e fechamento). O numero fica gravado em
`.prova/issue` (lockfile, commit do bot); se o lock sumir, ha fallback via API
(procura issue com titulo exato "🎯 Prova"). Motivo do lock: o aluno pode usar
os proprios issues do repo para se organizar — a nossa issue e identificavel
pelo lock, nao pelo titulo de evento.

    numero()                            -> int | None
    comentar(texto)                     -> cria comentario (one-shot)
    atualizar_comentario(marcador, txt) -> upsert: edita o comentario do bot
        que comeca com `<!-- marcador -->`, senao cria — para nao spammar a
        issue a cada push.

Usa GH_TOKEN e REPO_FULL do ambiente (mesmo contrato dos demais scripts).
"""
import json
import os
import urllib.error
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TOKEN = os.environ.get("GH_TOKEN", "")
REPO_FULL = os.environ.get("REPO_FULL", "")
TITULO = "🎯 Prova"


def _api(method, path, payload=None):
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


def numero(base: str = BASE):
    """Numero da issue da prova: lock .prova/issue, fallback via API."""
    lock = os.path.join(base, ".prova", "issue")
    if os.path.exists(lock):
        try:
            return int(open(lock, encoding="utf-8").read().strip())
        except ValueError:
            pass
    if TOKEN and REPO_FULL:
        status, dados = _api("GET", "/repos/%s/issues?state=all&per_page=100"
                             % REPO_FULL)
        if status == 200 and isinstance(dados, list):
            for issue in dados:
                if issue.get("title") == TITULO:
                    return issue.get("number")
    return None


def comentar(texto: str):
    """Cria comentario na issue da prova. Retorna id ou None."""
    n = numero()
    if not (n and TOKEN and REPO_FULL):
        return None
    status, dados = _api("POST", "/repos/%s/issues/%s/comments" % (REPO_FULL, n),
                         {"body": texto})
    return dados.get("id") if status == 201 else None


def atualizar_comentario(marcador: str, texto: str):
    """Upsert de comentario identificado por `<!-- marcador -->`."""
    n = numero()
    if not (n and TOKEN and REPO_FULL):
        return None
    marcacao = "<!-- %s -->" % marcador
    corpo = (marcacao + "\n" + texto).strip()
    status, comentarios = _api("GET", "/repos/%s/issues/%s/comments?per_page=100"
                               % (REPO_FULL, n))
    if status == 200 and isinstance(comentarios, list):
        for c in comentarios:
            if (c.get("body") or "").startswith(marcacao):
                _api("PATCH", "/repos/%s/issues/comments/%s"
                     % (REPO_FULL, c.get("id")), {"body": corpo})
                return c.get("id")
    status, dados = _api("POST", "/repos/%s/issues/%s/comments" % (REPO_FULL, n),
                         {"body": corpo})
    return dados.get("id") if status == 201 else None
