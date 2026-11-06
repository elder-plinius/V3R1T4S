#!/bin/sh
# Standalone check: no S_6 set of three tournaments on 12 vertices, so f(3,6) = 13 (arXiv:2604.08790, Definitions 2.1, 2.2).
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# Default (about 5 minutes on an Apple M-series laptop): checks the object's integrity, the 13-vertex upper-bound object,
# the job list against the cover tree, 40 rebuilt CNFs, and re-proves 6 jobs end to end (the root cover lemma and 5 seeded
# small jobs) with CaDiCaL 1.9.5, drat-trim and the verified checker cake_lpr. FULL=1 re-proves all 2,871 jobs instead
# (about 27 CPU-hours; peak 4.5 GB per job).
# Needs python3 (3.10-3.12), git, a C compiler, network access to pypi.org (python-sat 1.9.dev17 in a temporary venv) and
# github.com (pinned drat-trim and cake_lpr), about 5 GB of free memory and 3 GB of disk. To skip downloads and builds, set
# CHECK_PYTHON (a python with python-sat 1.9.dev17), DRAT_TRIM and CAKE_LPR (binaries).
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd); V="$HERE/verify-it-yourself"; O="$HERE/object"
W=$(mktemp -d "${TMPDIR:-/tmp}/schutte36_check.XXXXXX") || { echo "no temporary folder"; echo FAIL; exit 1; }
trap 'rm -rf "$W"' EXIT
fail() { echo "$1"; echo FAIL; exit 1; }
cd "$HERE" || fail "no package folder"

echo "== 0. object files match SHA256SUMS"
python3 -I -c '
import hashlib, sys
want = dict(reversed(l.split(None, 1)) for l in open("SHA256SUMS").read().splitlines() if l.strip())
want = {k.strip().lstrip("*"): v for k, v in want.items()}
for f in ("object/certificate_m3k6n12.tsv", "object/witness_m3k6n13.json"):
    got = hashlib.sha256(open(f, "rb").read()).hexdigest()
    print(f, "ok" if want.get(f) == got else "MISMATCH"); assert want.get(f) == got
' || fail "an object file does not match SHA256SUMS"

echo "== 1. upper bound: object/witness_m3k6n13.json is an S_6 set of three tournaments on 13 vertices (Definition 2.1)"
python3 -I "$V/check_witness.py" "$O/witness_m3k6n13.json" 6 > "$W/w.out" 2>&1; cat "$W/w.out"
[ "$(tail -n 1 "$W/w.out")" = PASS ] || fail "upper-bound object rejected"

echo "== 2. python with python-sat 1.9.dev17"
PY=${CHECK_PYTHON:-}
if [ -z "$PY" ]; then
  python3 -m venv "$W/venv" && "$W/venv/bin/python" -m pip install -q --disable-pip-version-check python-sat==1.9.dev17 \
    || fail "could not install python-sat 1.9.dev17 into a temporary venv"
  PY="$W/venv/bin/python"
fi
"$PY" -I -c 'import importlib.metadata as m; print("python-sat", m.version("python-sat"))'

echo "== 3. job list = cover tree, and rebuilt CNFs match the object"
N=40; [ "${FULL:-0}" = 1 ] && N=all
"$PY" -I "$V/check_cert.py" "$N" > "$W/c.out" 2>&1; cat "$W/c.out"
[ "$(tail -n 1 "$W/c.out")" = PASS ] || fail "certificate list check failed"

echo "== 4. drat-trim and cake_lpr at pinned commits"
DT=${DRAT_TRIM:-}; CAKE=${CAKE_LPR:-}
if [ -z "$DT" ]; then
  mkdir -p "$W/drat-trim" && git -C "$W/drat-trim" init -q && \
  git -C "$W/drat-trim" fetch -q --depth 1 https://github.com/marijnheule/drat-trim.git 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 && \
  git -C "$W/drat-trim" checkout -q FETCH_HEAD -- drat-trim.c && (cd "$W/drat-trim" && cc -std=c99 -O2 -o drat-trim drat-trim.c 2>/dev/null) \
  || fail "could not build drat-trim (commit 2e3b2dc0ecf938addbd779d42877b6ed69d9a985)"
  DT="$W/drat-trim/drat-trim"
fi
if [ -z "$CAKE" ]; then
  mkdir -p "$W/cake_lpr" && git -C "$W/cake_lpr" init -q && \
  git -C "$W/cake_lpr" fetch -q --depth 1 https://github.com/tanyongkiam/cake_lpr.git a36874a8b750b43fe4b385b8ddbf5b033e46a3fa && \
  git -C "$W/cake_lpr" checkout -q FETCH_HEAD -- basis_ffi.c cake_lpr.S cake_lpr_arm8.S || fail "could not fetch cake_lpr (commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa)"
  case "$(uname -m)" in arm64|aarch64) S=cake_lpr_arm8.S ;; *) S=cake_lpr.S ;; esac
  (cd "$W/cake_lpr" && cc -std=c99 -O2 -o cake_lpr basis_ffi.c "$S" 2>/dev/null) || fail "could not build cake_lpr"
  CAKE="$W/cake_lpr/cake_lpr"
fi

echo "== 5. re-prove jobs: CaDiCaL 1.9.5 writes a DRAT proof, drat-trim turns it into LRAT, cake_lpr checks it"
"$PY" -I -c '
import sys, random
rows = [l.rstrip("\n").split("\t") for l in open("object/certificate_m3k6n12.tsv")][1:]
if sys.argv[1] == "1": pick = [r[0] for r in rows]
else:
    small = [r[0] for r in rows if float(r[7]) + float(r[8]) + float(r[9]) < 10 and r[0] != "m3k6n12/COVER1"]
    pick = ["m3k6n12/COVER1"] + random.Random(20261101).sample(small, 5)
print("\n".join(pick))' "${FULL:-0}" > "$W/pick.txt" || fail "could not pick jobs"
ok=0; tot=$(wc -l < "$W/pick.txt" | tr -d ' ')
while read -r J; do
  D="$W/job"; rm -rf "$D"; mkdir -p "$D"
  ROW=$(awk -F'\t' -v j="$J" '$1==j' "$O/certificate_m3k6n12.tsv")
  "$PY" -I "$HERE/how-we-built-it/certify/solve.py" "$J" "$D" > "$D/solve.json" 2> "$D/solve.err" || fail "$J: solver step failed"
  grep -q '"result": "UNSAT"' "$D/solve.json" || fail "$J: solver did not report UNSAT"
  SHA=$( (shasum -a 256 "$D/f.cnf" 2>/dev/null || sha256sum "$D/f.cnf") | cut -c1-64)
  [ "$SHA" = "$(echo "$ROW" | cut -f2)" ] || fail "$J: CNF sha256 differs from the object"
  "$DT" "$D/f.cnf" "$D/proof.drat" -i -w -L "$D/proof.lrat" > "$D/drat.out" 2>&1
  OUT=$("$CAKE" --CML_HEAP_SIZE=4500 --CML_STACK_SIZE=1000 "$D/f.cnf" "$D/proof.lrat" 2>&1 | tail -n 1)
  echo "$J: $OUT"
  [ "$OUT" = "s VERIFIED UNSAT" ] || fail "$J: cake_lpr did not verify the proof"
  ok=$((ok + 1))
done < "$W/pick.txt"
echo "$ok of $tot jobs re-proved and verified by cake_lpr (of 2,871 in the certificate)"
echo "no S_6 set of three tournaments on 12 vertices (all 2,871 cubes of the cover are UNSAT, as listed in the object);"
echo "an S_6 triple on fewer vertices would extend to 12 (add vertices that lose to all), so none exists: f(3,6) >= 13; with step 1, f(3,6) = 13"
echo PASS
