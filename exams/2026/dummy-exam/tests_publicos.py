"""Testes PUBLICOS da prova — versao DUMMY (2026/dummy-exam).

Cada pasta do ano pode trazer seus proprios testes publicos; o workflow
*Aplicar prova* copia este arquivo para tests/public/ no repo do aluno.

A suite escondida da correção segue o mesmo contrato (contrato.json), com
muito mais casos — incluindo avaliacao de frontend avancado (extras).
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from variante import slug_do_repo, variante  # noqa: E402

V = variante(os.environ.get("REPO_SLUG", slug_do_repo()))
BASE = os.environ.get("BASE_URL", "http://localhost:%d" % V["PORTA_API"])
PREFIXO = V["PREFIXO"]
RAZAO = V["RAZAO_PREFERENCIAL"]


def req(metodo, caminho, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + caminho, data=data, method=metodo)
    if data:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=5) as resp:
            return resp.status, dict(resp.headers), json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, dict(e.headers), json.loads(e.read().decode() or "{}")
        except ValueError:
            return e.code, {}, {}
    except Exception as e:
        raise AssertionError("falha ao chamar %s%s: %s" % (BASE, caminho, e))


def test_01_emissao_de_senha():
    """POST /senhas emite senha com o PREFIXO da variante e valida tipo."""
    status, _, corpo = req("POST", "/senhas", {"tipo": "normal"})
    assert status == 201, "esperado 201, veio %d (%s)" % (status, corpo)
    assert re.match(r"^%s\d{3}$" % PREFIXO, corpo.get("codigo", "")), \
        "codigo deve seguir %sNNN, veio %r" % (PREFIXO, corpo.get("codigo"))
    assert corpo.get("status") == "aguardando"

    status, _, corpo = req("POST", "/senhas", {"tipo": "vip"})
    assert status == 422, "tipo invalido deve dar 422, veio %d" % status
    assert corpo.get("erro") == "tipo_invalido"


def test_02_intercalacao_da_variante():
    """A prioridade chama RAZAO preferenciais antes de 1 normal (SUA razao)."""
    _, normal = req("POST", "/senhas", {"tipo": "normal"})
    for _ in range(RAZAO):
        req("POST", "/senhas", {"tipo": "preferencial"})

    chamadas = []
    for _ in range(RAZAO + 1):
        status, _, corpo = req("GET", "/senhas/proxima")
        assert status == 200, "esperado 200, veio %d (%s)" % (status, corpo)
        chamadas.append(corpo)

    tipos = [c.get("tipo") for c in chamadas]
    esperado = ["preferencial"] * RAZAO + ["normal"]
    assert tipos == esperado, "intercalacao deve ser %s, veio %s" % (esperado, tipos)
    assert chamadas[-1].get("codigo") == normal.get("codigo")


def test_03_frontend_basico():
    """GET / deve servir o frontend (200, text/html) pelo mesmo container."""
    r = urllib.request.Request(BASE + "/")
    try:
        with urllib.request.urlopen(r, timeout=5) as resp:
            html = resp.read().decode(errors="replace")
            assert resp.status == 200, "esperado 200, veio %d" % resp.status
            assert "text/html" in resp.headers.get("Content-Type", ""), \
                "Content-Type deve ser text/html, veio %r" % resp.headers.get("Content-Type")
            assert len(html) > 100, "pagina HTML muito pequena (%d bytes) — frontend ausente?" % len(html)
    except urllib.error.HTTPError as e:
        raise AssertionError("GET / retornou %d — o frontend deve ser servido pelo mesmo container" % e.code)
    except Exception as e:
        raise AssertionError("falha ao chamar %s/: %s" % (BASE, e))
