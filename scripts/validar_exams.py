#!/usr/bin/env python3
"""Valida as pastas de prova em exams/ — roda no CI do TEMPLATE (push na main).

Erros (exit 1): track.json invalido, contrato.json sem a secao variante com
as chaves exatas, rubrica.json sem nota_max/janela_minutos, item da pasta
colidindo com o esqueleto.
Avisos (exit 0): mais de uma track no mesmo ano, pasta com nome dummy.
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMS = os.path.join(BASE, "exams")
BLOQUEADOS = {"scripts", ".github", "docs", ".gitignore", ".prova", "tests"}
VARIANTE_OBRIGATORIAS = {"PREFIXOS": list, "RAZOES": list,
                         "PORTA_BASE": int, "FAIXA": int}

erros, avisos = [], []

if not os.path.isdir(EXAMS):
    print("exams/ ausente — nenhuma prova publicada.")
    sys.exit(0)

por_ano = {}
for ano in sorted(os.listdir(EXAMS)):
    dir_ano = os.path.join(EXAMS, ano)
    if not os.path.isdir(dir_ano) or not ano.isdigit():
        continue
    tracks = sorted(d for d in os.listdir(dir_ano)
                    if os.path.isdir(os.path.join(dir_ano, d)))
    por_ano[ano] = tracks
    if len(tracks) > 1:
        avisos.append("%s: %d tracks publicadas juntas (%s) — confirme a "
                      "selecao via /track na issue" % (ano, len(tracks), ", ".join(tracks)))
    for track in tracks:
        pasta = os.path.join(dir_ano, track)
        prefixo = "exams/%s/%s" % (ano, track)
        if "dummy" in track.lower():
            avisos.append("%s: pasta de teste (dummy) publicada na main — "
                          "OK para aula teste; remova para prova real" % prefixo)
        for item in os.listdir(pasta):
            if item in BLOQUEADOS:
                erros.append("%s: item '%s' colide com o esqueleto" % (prefixo, item))
        # track.json
        tj = os.path.join(pasta, "track.json")
        if not os.path.exists(tj):
            erros.append("%s: track.json ausente" % prefixo)
        else:
            try:
                lock = json.load(open(tj, encoding="utf-8"))
                assert isinstance(lock.get("track"), str)
                assert isinstance(lock.get("lockfile_version"), int)
                assert isinstance(lock.get("workflows"), dict)
            except Exception:
                erros.append("%s: track.json invalido (ver docs/TRACKS.md)" % prefixo)
        # contrato.json
        cj = os.path.join(pasta, "contrato.json")
        if not os.path.exists(cj):
            erros.append("%s: contrato.json ausente" % prefixo)
        else:
            try:
                contrato = json.load(open(cj, encoding="utf-8"))
                variante = contrato["variante"]
                for chave, tipo in VARIANTE_OBRIGATORIAS.items():
                    if not isinstance(variante.get(chave), tipo):
                        erros.append("%s: contrato.json variante.%s deve ser %s"
                                     % (prefixo, chave, tipo.__name__))
            except KeyError as e:
                erros.append("%s: contrato.json sem secao %s" % (prefixo, e))
            except ValueError:
                erros.append("%s: contrato.json nao e JSON valido" % prefixo)
        # rubrica.json
        rj = os.path.join(pasta, "rubrica.json")
        if not os.path.exists(rj):
            erros.append("%s: rubrica.json ausente" % prefixo)
        else:
            try:
                rubrica = json.load(open(rj, encoding="utf-8"))
                if "nota_max" not in rubrica or "janela_minutos" not in rubrica:
                    erros.append("%s: rubrica.json sem nota_max/janela_minutos" % prefixo)
            except ValueError:
                erros.append("%s: rubrica.json nao e JSON valido" % prefixo)

for a in avisos:
    print("AVISO:", a)
for e in erros:
    print("ERRO:", e)
print("exams validados: %d ano(s)" % len(por_ano))
sys.exit(1 if erros else 0)
