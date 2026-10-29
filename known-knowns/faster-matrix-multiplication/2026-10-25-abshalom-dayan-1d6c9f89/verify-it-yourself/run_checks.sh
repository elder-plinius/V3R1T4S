#!/bin/sh
# Run from the claim folder: sh verify-it-yourself/run_checks.sh        Last line: PASS or FAIL.
# Needs python3 (standard library) for check 1 and, for the faster check 2, numpy. No network.
# About 120 s wall for the whole script (check 1 about 115 s, check 2 about 5 s) on a laptop; peak memory about 2.1 GB resident (the stdlib checker; the numpy one needs less) (see README.md and RECEIPTS.md for the measured numbers).
# object/ stores each factor file as parts of under 1 MB (u.txt, or u.part1.txt, u.part2.txt, ...). This script joins
# them, checks the sha256 of the joined u, v and w against the values below, then runs the exact checkers.
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
PY=$(command -v python3 || command -v python)
[ -n "$PY" ] || { echo "no python3 found"; echo FAIL; exit 1; }
T=$(mktemp -d "${TMPDIR:-/tmp}/assembled.XXXXXX") || { echo FAIL; exit 1; }
for w in u v w; do
  if [ -f "object/$w.txt" ]; then cat "object/$w.txt" > "$T/$w.txt"; else cat object/$w.part?.txt > "$T/$w.txt"; fi || { echo FAIL; exit 1; }
done
"$PY" -I - "$T" <<'PYEOF'
import hashlib, sys
want = {"u.txt": "1d6c9f89e17717b7236f9bbbf46d6903e95f66a3965445cd8194bc23bd065d58",
        "v.txt": "bdcfa626ff98644b132c75ac00deebb2b9cb922116b7b44e00e63d2238f5da5a",
        "w.txt": "9192310639d1141ba525574fac6735b5ce0507711ac0c8989a1f049b221aa48e"}
ok = True
for f, h in want.items():
    got = hashlib.sha256(open(sys.argv[1] + "/" + f, "rb").read()).hexdigest()
    print(got, f, "(matches)" if got == h else "(MISMATCH, expected %s)" % h)
    ok &= got == h
sys.exit(0 if ok else 1)
PYEOF
s0=$?
t0=$(date +%s)
echo "== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)"
"$PY" -I verify-it-yourself/check_brent_stdlib.py "$T" --trials 3 --seed 20261024; s1=$?
t1=$(date +%s); echo "check 1 took $((t1 - t0)) s"
echo "== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)"
if "$PY" -I -c "import numpy" 2>/dev/null; then
  "$PY" -I verify-it-yourself/check_exact_np.py "$T" --trials 3 --seed 20261024; s2=$?
  echo "check 2 took $(( $(date +%s) - t1 )) s"
else
  echo "numpy is not installed: check 2 SKIPPED (pip install numpy, then run this script again); the verdict below rests on check 1 alone"
  s2=0
fi
rm -rf "$T"
if [ "$s0" -eq 0 ] && [ "$s1" -eq 0 ] && [ "$s2" -eq 0 ]; then echo PASS; exit 0; fi
echo FAIL; exit 1
