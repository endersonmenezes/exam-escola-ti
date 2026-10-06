#!/usr/bin/env bash
# Roda os testes PUBLICOS contra o container do aluno.
# Uso: bash scripts/rodar_testes.sh   (requer Docker + python3 + pytest)
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v docker >/dev/null 2>&1; then
  echo "ERRO: docker nao encontrado." >&2
  exit 2
fi

python3 scripts/variante.py >/dev/null
PORTA=$(python3 -c "import json;print(json.load(open('variante/params.json'))['PORTA_API'])")
SLUG=$(python3 -c "import json;print(json.load(open('variante/params.json'))['slug'])")
IMAGEM="prova03-$(echo "$SLUG" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9' '-')"

echo "==> build $IMAGEM"
docker build -q -t "$IMAGEM" .

echo "==> subindo em localhost:$PORTA"
docker rm -f prova03-teste >/dev/null 2>&1 || true
docker run -d --name prova03-teste -p "$PORTA:8080" "$IMAGEM" >/dev/null

cleanup() { docker rm -f prova03-teste >/dev/null 2>&1 || true; }
trap cleanup EXIT

echo "==> aguardando /healthz"
for i in $(seq 1 40); do
  if curl -fsS "http://localhost:$PORTA/healthz" >/dev/null 2>&1; then
    break
  fi
  if [ "$i" = "40" ]; then
    echo "ERRO: API nao respondeu /healthz a tempo. Logs:" >&2
    docker logs prova03-teste >&2 || true
    exit 1
  fi
  sleep 2
done

echo "==> pytest (testes publicos)"
BASE_URL="http://localhost:$PORTA" REPO_SLUG="$SLUG" \
  python3 -m pytest tests/public -q --tb=short
