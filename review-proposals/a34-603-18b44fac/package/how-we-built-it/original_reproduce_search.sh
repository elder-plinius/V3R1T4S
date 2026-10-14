#!/usr/bin/env bash
# Optional deterministic search replay on the same standard-library implementation.
# Validation of the explicit witness does not require compiling or running the search.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p replay
g++ -O3 -march=native -std=c++17 scan.cpp -o replay/scan
g++ -O3 -march=native -std=c++17 engine.cpp -o replay/engine
replay/engine sources/A34_8_7_602.txt 34 7 4 4 12 101 50 150 replay/stage3
python3 check_code.py replay/stage3_candidate.txt --output replay/pairwise.json
python3 check_subsets.py replay/stage3_candidate.txt --output replay/subsets.json
python3 - <<'PY'
from pathlib import Path
import hashlib
p=Path('replay/stage3_candidate.txt'); expected=Path('candidates/A34_8_7_603.txt')
print('Exact published-witness match:',p.read_bytes()==expected.read_bytes())
print('SHA256:',hashlib.sha256(p.read_bytes()).hexdigest())
PY
