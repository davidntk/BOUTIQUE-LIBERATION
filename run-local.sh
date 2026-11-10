#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 est requis."
  exit 1
fi

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install -r requirements.txt
mkdir -p data

export FLASK_HOST="${FLASK_HOST:-0.0.0.0}"
export FLASK_PORT="${FLASK_PORT:-5001}"
export FLASK_DEBUG="${FLASK_DEBUG:-0}"
export SECRET_KEY="${SECRET_KEY:-local-development-change-this-secret}"
export DB_PATH="${DB_PATH:-$(pwd)/data/boutique_liberation.db}"

echo "Boutique : http://127.0.0.1:${FLASK_PORT}"
echo "Admin    : http://127.0.0.1:${FLASK_PORT}/admin"
echo "Sante    : http://127.0.0.1:${FLASK_PORT}/health"
exec python app.py
