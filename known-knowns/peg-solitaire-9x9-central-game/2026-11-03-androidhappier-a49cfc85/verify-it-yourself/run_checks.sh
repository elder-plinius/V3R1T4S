#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh      (a few seconds; last line PASS or FAIL)
# Needs python3 (standard library only). If a C compiler (cc/gcc) is present, also builds and runs the
# independent C replay checker. Nothing is downloaded.
V=verify-it-yourself
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3chk)
trap 'rm -rf "$T"' EXIT
fail=0
PY=${PYTHON:-python3}

echo "== 1. object/sol31.txt sha256 vs INDEX.csv"
$PY - <<'PYEOF' || fail=1
import csv, hashlib, sys
rows = list(csv.reader(open("INDEX.csv")))
h = dict(zip(rows[0], rows[1]))
got = hashlib.sha256(open(h["file"], "rb").read()).hexdigest()
print("INDEX sha256 ", h["sha256"]); print("file sha256  ", got)
if got != h["sha256"]: print("sha256 MISMATCH"); sys.exit(1)
print("sha256 ok; INDEX value =", h["value"])
PYEOF

echo "== 2. Python checker (written from the definition) on the object: expect VALID, 31 moves, 79 jumps"
out=$($PY $V/check9.py object/sol31.txt --claim-max 33); echo "$out"
echo "$out" | grep -q "^jumps=79 moves=31 pegs_left=1 final=e5$" && echo "$out" | grep -q "^VALID central game e5->e5 in 31 moves$" \
  || { echo "object: unexpected result"; fail=1; }

echo "== 3. object/VALUE.txt agrees with the checker, and every file matches SHA256SUMS"
grep -q "^moves: 31$" object/VALUE.txt && grep -q "^jumps: 79$" object/VALUE.txt \
  && grep -q "^sha256: $(sed -n 2p INDEX.csv | awk -F, '{print $NF}')$" object/VALUE.txt || { echo "VALUE.txt mismatch"; fail=1; }
$PY - <<'PYEOF' || fail=1
import hashlib, sys
bad = 0; n = 0
for line in open("SHA256SUMS"):
    h, f = line.rstrip("\n").split(None, 1); f = f.lstrip("*")
    n += 1
    if hashlib.sha256(open(f, "rb").read()).hexdigest() != h: print("SHA256SUMS mismatch:", f); bad = 1
print("SHA256SUMS: %d files checked, %s" % (n, "MISMATCH" if bad else "all ok"))
sys.exit(bad)
PYEOF

echo "== 4. negative fixtures must be rejected"
for f in neg_diag neg_occupied neg_sol31_swapped neg_sol31_truncated neg_unfinished; do
  o=$($PY $V/check9.py $V/fixtures/$f.txt); rc=$?
  if [ $rc -ne 0 ] && ! echo "$o" | grep -q "^VALID"; then echo "$f: rejected ok ($(echo "$o" | tail -n 1))"
  else echo "$f: WRONGLY ACCEPTED"; fail=1; fi
done

echo "== 5. positive calibration fixture (34 moves, ties Maye; not a win) must be VALID 34"
o=$($PY $V/check9.py $V/fixtures/pos_beam_34.txt); echo "$o"
echo "$o" | grep -q "^VALID central game e5->e5 in 34 moves$" || { echo "pos_beam_34: unexpected"; fail=1; }

echo "== 6. independent C replay checker (optional)"
CC=${CC:-}
[ -z "$CC" ] && for c in cc gcc clang; do command -v $c >/dev/null 2>&1 && { CC=$c; break; }; done
if [ -n "$CC" ] && $CC -O2 -o "$T/replay9" $V/replay9.c 2>/dev/null; then
  o=$("$T/replay9" object/sol31.txt); echo "$o"
  echo "$o" | grep -q "jumps=79 moves=31 left=1 centre=1" && echo "$o" | grep -q "PASS" || { echo "replay9: unexpected"; fail=1; }
  o=$("$T/replay9" $V/fixtures/neg_diag.txt); echo "$o" | grep -q "PASS" && { echo "replay9 accepted neg_diag"; fail=1; } || echo "replay9 rejects neg_diag ok"
else echo "skip C part: no C compiler"; fi

echo "summary: 9x9 (81-hole square board) central game e5->e5, orthogonal jumps, 79 jumps / 31 moves"
if [ $fail -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
