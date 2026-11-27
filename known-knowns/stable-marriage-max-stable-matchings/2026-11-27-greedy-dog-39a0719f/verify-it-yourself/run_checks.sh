#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
python3 verify-it-yourself/verify.py
command -v sha256sum >/dev/null 2>&1 && sha256sum -c SHA256SUMS --quiet
echo "PASS"
