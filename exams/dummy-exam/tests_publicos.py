"""Testes PUBLICOS da prova-teste — Hello World (exams/dummy-exam).

Cada pasta do ano pode trazer seus proprios testes publicos; o workflow
*Aplicar prova* copia este arquivo para tests/public/ no repo do aluno.

A suíte sobe o container do aluno (scripts/rodar_testes.sh) e testa o
endpoint /saudar contra os parametros da SUA variante — derivados do nome
do repositorio pelas mesmas tabelas do contrato (mesmo mecanismo de
scripts/variante.py: hash sha256 do slug, módulo o tamanho de cada tabela).

Nao existe suíte escondida nesta prova-teste: a nota do CI ja e a nota —
trampas + entrega + estes testes publicos.
"""
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from variante import parametros_ano, pasta_do_ano, slug_do_repo, variante  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SLUG = os.environ.get("REPO_SLUG", slug_do_repo())
V = variante(SLUG)
BASE = os.environ.get("BASE_URL", "http://localhost:%d" % V["PORTA_API"])

# Parametros completos da variante: mesmo mecanismo de scripts/variante.py
# (sha256 do slug, indice = hash % len(tabela)) aplicado as tabelas extras.
_TABELAS = parametros_ano(pasta_do_ano())
_H = int(hashlib.sha256(SLUG.encode("utf-8")).hexdigest(), 16)
NOME = _TABELAS["PREFIXOS"][_H % len(_TABELAS["PREFIXOS"])]
REPETICOES = _TABELAS["RAZOES"][_H % len(_TABELAS["RAZOES"])]
SAUDACAO = _TABELAS["SAUDACOES"][_H % len(_TABELAS["SAUDACOES"])]
SUFIXO = _TABELAS["SUFIXOS"][_H % len(_TABELAS["SUFIXOS"])]


def req(metodo, caminho):
    r = urllib.request.Request(BASE + caminho, method=metodo)
    try:
        with urllib.request.urlopen(r, timeout=5) as resp:
            return resp.status, dict(resp.headers), resp.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        try:
            return e.code, dict(e.headers), e.read().decode(errors="replace")
        except Exception:
            return e.code, {}, ""
    except Exception as e:
        raise AssertionError("falha ao chamar %s%s: %s — o app esta no ar? "
                             "(bash scripts/rodar_testes.sh sobe o container)"
                             % (BASE, caminho, e))


def saudar(**params):
    return req("GET", "/saudar?" + urllib.parse.urlencode(params))


def test_01_healthz():
    """GET /healthz responde 200 com {"status": "ok"} (a suíte depende disso)."""
    status, _, corpo = req("GET", "/healthz")
    assert status == 200, "esperado 200, veio %d (%s)" % (status, corpo)
    assert json.loads(corpo).get("status") == "ok", "corpo esperado {'status': 'ok'}, veio %r" % corpo


def test_02_saudacao_da_variante():
    """A saudação com os parâmetros EXATOS da sua variante sai byte a byte."""
    status, headers, corpo = saudar(saudacao=SAUDACAO, nome=NOME,
                                    sufixo=SUFIXO, repeticoes=REPETICOES)
    assert status == 200, "esperado 200, veio %d (%s)" % (status, corpo)
    assert "text/plain" in headers.get("Content-Type", ""), \
        "Content-Type deve ser text/plain, veio %r" % headers.get("Content-Type")
    esperado = ["%s, %s%s" % (SAUDACAO, NOME, SUFIXO)] * REPETICOES
    linhas = [l for l in corpo.splitlines() if l]
    assert linhas == esperado, \
        "esperado %d linha(s) %r, veio %r — veja sua variante em variante/params.json" \
        % (REPETICOES, esperado, linhas)


def test_03_defaults_e_validacao():
    """Sem os opcionais vale Ola/{nome}! uma vez; parametros ruins dao 400."""
    status, _, corpo = saudar(nome="Teste")
    assert status == 200, "esperado 200, veio %d (%s)" % (status, corpo)
    assert corpo.splitlines() == ["Ola, Teste!"], \
        "default esperado 'Ola, Teste!', veio %r" % corpo

    status, _, corpo = req("GET", "/saudar")
    assert status == 400, "sem nome deve dar 400, veio %d" % status
    assert json.loads(corpo).get("erro") == "nome_ausente", "corpo veio %r" % corpo

    for ruim in ("0", "11", "abc"):
        status, _, corpo = saudar(nome="X", repeticoes=ruim)
        assert status == 400, "repeticoes=%s deve dar 400, veio %d" % (ruim, status)
        assert json.loads(corpo).get("erro") == "repeticoes_invalidas", "corpo veio %r" % corpo


def test_04_estrutura_src():
    """src/app.py existe, nao e o stub (sem TODO) e tem conteudo de verdade."""
    app = os.path.join(RAIZ, "src", "app.py")
    assert os.path.exists(app), "src/app.py ausente — implemente a solução em src/"
    texto = open(app, encoding="utf-8", errors="replace").read()
    assert "TODO" not in texto, "src/app.py ainda é o stub (contém TODO) — implemente o servidor"
    assert len(texto.strip()) > 100, "src/app.py muito pequeno (%d bytes) — solução vazia?" % len(texto)


def test_05_fontes():
    """FONTES.md preenchido (com link) OU declarado explicitamente vazio."""
    fontes = os.path.join(RAIZ, "FONTES.md")
    assert os.path.exists(fontes), "FONTES.md ausente — restaure o do template"
    linhas = open(fontes, encoding="utf-8", errors="replace").read().splitlines()
    tem_link = any(re.match(r"^\|\s*\d", l) and re.search(r"https?://\S+", l) for l in linhas)
    declarou_vazio = any(re.match(r"^\W{0,3}\s*Nenhum", l)
                         and ("utilizada" in l.lower() or "consultado" in l.lower())
                         for l in linhas)
    assert tem_link or declarou_vazio, \
        "FONTES.md ainda com placeholder — declare as fontes usadas OU escreva " \
        "explicitamente que nada foi consultado (ex.: 'Nenhum site consultado.')"
