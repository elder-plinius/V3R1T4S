#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"

echo "== shapes: 24 pieces, aspects =="
python3 - <<'PY'
from py.shapes import letters, aspects_for, piece_cells
from py.grid import connected
assert len(letters())==24
for L in letters():
    assert len(piece_cells(L))==7 and connected(piece_cells(L))
    a=aspects_for(L)
    assert 1 <= len(a) <= 12, (L, len(a))
print("aspects", {L: len(aspects_for(L)) for L in letters()})
print("SHAPES OK")
PY

echo "== calibrate A-B listed k=2 =="
rm -rf work/selftest_AB
python3 - <<'PY'
from py.solve_pair import solve_pair
s=solve_pair('A','B', k_min=2, k_max=2, table='unrestricted',
             work_dir=__import__('pathlib').Path('work/selftest_AB'),
             timeout_per_k=90, prove_unsat=True)
assert s['found'], s
assert s['solution']['k']==2
assert s['solution']['checker']['ok'], s['solution']['checker']
print("A-B k=2 OK")
# UNSAT at k=1 impossible (area 7) — skip; check k=2 was listed
print("CALIBRATION OK")
PY

echo "== independent checker CLI =="
python3 py/check_independent.py work/selftest_AB/k2/solution.json

echo "== calibrate C-F listed k=2 =="
rm -rf work/selftest_CF
python3 - <<'PY'
from py.solve_pair import solve_pair
s=solve_pair('C','F', k_min=2, k_max=2, table='unrestricted',
             work_dir=__import__('pathlib').Path('work/selftest_CF'),
             timeout_per_k=90)
assert s['found'] and s['solution']['checker']['ok']
print("C-F k=2 OK")
PY

echo "SELFTEST PASS"
