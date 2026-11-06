#!/bin/sh
# Standalone check: no S_5 set of two tournaments on 13 vertices, so f(2,5) = 14 (arXiv:2604.08790, Definition 2.2).
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# Needs python3 (standard library), git, make and a C compiler, network access to github.com (to build the pinned
# CaDiCaL and cake_lpr), about 1.6 GB of free memory and 0.5 GB of free disk. About 5 minutes on an Apple M-series
# laptop. To skip the builds, set CADICAL=/path/to/cadical and CAKE_LPR=/path/to/cake_lpr (cake_lpr's own binary).
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd); V="$HERE/verify-it-yourself"; O="$HERE/object"
W=$(mktemp -d "${TMPDIR:-/tmp}/schutte_check.XXXXXX") || { echo "no temporary folder"; echo FAIL; exit 1; }
trap 'rm -rf "$W"' EXIT
fail() { echo "$1"; echo FAIL; exit 1; }
echo "== 1. regenerate the CNF named by object/cnf_spec.json (shipped encoder) and compare sha256 and header"
python3 "$V/spec_check.py" "$O/cnf_spec.json" "$V/encode_schutte.py" "$W/f.cnf" || fail "spec check failed"
echo "== 2. upper bound: object/upper_bound_m2k5n14.json is an S_5 set of two tournaments on 14 vertices"
python3 "$V/check_schutte.py" "$O/upper_bound_m2k5n14.json" || fail "upper bound object rejected"
echo "== 3. the base clauses of the CNF are exactly Definition 2.2 for (m,k,n) = (2,5,13) (cnf_audit.py)"
python3 "$V/cnf_audit.py" "$W/f.cnf" 2 5 13 > "$W/audit.txt"; cat "$W/audit.txt"
grep -q "^AUDIT OK" "$W/audit.txt" || fail "CNF audit failed"
echo "== 4. solver and verified checker"
CAD=${CADICAL:-}; CAKE=${CAKE_LPR:-}
if [ -z "$CAD" ]; then
  mkdir -p "$W/cadical" && git -C "$W/cadical" init -q && \
  git -C "$W/cadical" fetch -q --depth 1 https://github.com/arminbiere/cadical.git c60730422e758ef1cebe7aeddf2dda31c996bf04 && \
  git -C "$W/cadical" checkout -q FETCH_HEAD && (cd "$W/cadical" && ./configure > /dev/null 2>&1 && make > /dev/null 2>&1) \
  || fail "could not build CaDiCaL 3.0.1 (commit c60730422e758ef1cebe7aeddf2dda31c996bf04)"
  CAD="$W/cadical/build/cadical"
fi
if [ -z "$CAKE" ]; then
  mkdir -p "$W/cake_lpr" && git -C "$W/cake_lpr" init -q && \
  git -C "$W/cake_lpr" fetch -q --depth 1 https://github.com/tanyongkiam/cake_lpr.git a36874a8b750b43fe4b385b8ddbf5b033e46a3fa && \
  git -C "$W/cake_lpr" checkout -q FETCH_HEAD -- basis_ffi.c cake_lpr.S cake_lpr_arm8.S || fail "could not fetch cake_lpr (commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa)"
  case "$(uname -m)" in arm64|aarch64) S=cake_lpr_arm8.S ;; *) S=cake_lpr.S ;; esac
  (cd "$W/cake_lpr" && cc -O2 -o cake_lpr basis_ffi.c "$S") || fail "could not build cake_lpr"
  CAKE="$W/cake_lpr/cake_lpr"
fi
"$CAD" --version | sed 's/^/CaDiCaL /'
echo "== 5. CaDiCaL with a text LRAT proof, then cake_lpr on the formula and the proof"
"$CAD" -q --lrat --no-binary "$W/f.cnf" "$W/f.lrat" > "$W/cadical.out" 2>&1; rc=$?
grep "^s " "$W/cadical.out"
[ "$rc" -eq 20 ] || fail "CaDiCaL did not report UNSATISFIABLE (exit $rc)"
"$CAKE" --CML_HEAP_SIZE=1500 --CML_STACK_SIZE=512 "$W/f.cnf" "$W/f.lrat" > "$W/cake.out" 2>&1
tail -n 1 "$W/cake.out"
[ "$(tail -n 1 "$W/cake.out")" = "s VERIFIED UNSAT" ] || fail "cake_lpr did not verify the proof"
echo "no S_5 set of two tournaments on 13 vertices (so none on fewer, by adding a vertex that loses to all): f(2,5) >= 14;"
echo "with the 14-vertex object of step 2: f(2,5) = 14"
echo PASS
