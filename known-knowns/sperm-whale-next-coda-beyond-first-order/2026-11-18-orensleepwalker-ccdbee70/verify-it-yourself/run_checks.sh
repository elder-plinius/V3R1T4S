#!/bin/sh
set -eu
failure() { printf '%s\n' FAIL; exit 1; }
sha256sum --check --quiet SHA256SUMS || failure
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir "$tmp/data"
curl -fsSL --max-time 30 -o "$tmp/data/sperm-whale-dialogues.csv" 'https://raw.githubusercontent.com/pratyushasharma/sw-combinatoriality/7228c8eed2cc27ddd23b74c51aeccec9d762389e/data/sperm-whale-dialogues.csv' || failure
printf '%s  %s\n' '1856c8bf915cc5ae6f928aaa2036cbbc6ad8840bb6e4f6a96aaeb96953215da2' "$tmp/data/sperm-whale-dialogues.csv" | sha256sum --check --quiet || failure
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 verify-it-yourself/verify.py . "$tmp" || failure
printf '%s\n' PASS
