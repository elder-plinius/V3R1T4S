#!/bin/sh
# Run from the claim folder: sh verify-it-yourself/run_checks.sh        Last line: PASS or FAIL.
# Needs python3 (standard library) for check 1 and, for the faster check 2, numpy. No network.
# About 27 s wall for the whole script (check 1 about 25 s, check 2 about 2 s) on a laptop; peak memory about 0.9 GB resident (the stdlib checker; the numpy one needs less) (see README.md and RECEIPTS.md for the measured numbers).
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
want = {"u.txt": "b97796005813233f1938c3de171c7e6782b6d2da05830bfe1ef5c4c54685645e",
        "v.txt": "1d1d3f4fd9584afea8aed3c75ed028ecf03bc425f9f17f9ef0d6efc98b16e746",
        "w.txt": "b9b611abc1fd0048903f376452f96b2d09a6539329f6273588a4364e6ea4f330"}
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
