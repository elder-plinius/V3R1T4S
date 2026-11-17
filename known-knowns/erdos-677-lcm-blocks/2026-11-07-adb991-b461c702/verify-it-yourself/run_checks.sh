#!/bin/sh
# Check this package: Erdos Problem 677 (Justin Sun Prize JSP-000550), no counterexample with 26 <= k <= 28,
# 0 <= n <= 10^494 and any m >= n + k. Run from the package folder:
#   sh verify-it-yourself/run_checks.sh          default checks, about 10 to 15 minutes
#   sh verify-it-yourself/run_checks.sh --all    also reruns the whole enumeration (4 shards, k = 26..28) and the
#                                                exact-rational margin checker per k (about 2 to 3 hours on 4 cores)
# Needs: Python 3 with gmpy2, mpmath and numpy (set PY to that interpreter; default python3), a C compiler (CC,
# default cc), sha256sum or shasum, and POSIX tools (cmp, sed, awk, grep, xargs, mktemp). Environment: PY,
# CC, JOBS (parallel Python jobs, default 4), PIDLOG (optional file: each job's start time, name and PID are
# appended to it). About 1 GB of memory per job. All jobs run at nice -n 10. Nothing is written into the package.
# What it does, in order (it stops at the first problem):
#   1. the files in object/ are the ones the panel read: their sha256 must equal the values recorded below
#      (and in README.md); object/ must hold no other file.
#   2. the saved outputs in object/out/ say what the claim says (0 exact-equal, 0 missing ratios for k = 26..28,
#      58926 margin pairs with 0 failures in both checkers, 4 enumeration shards whose ratio counts add up to
#      21262, 16402, 21262 with product_solutions=0 everywhere and 1455391 window candidates in all).
#   3. tools: PY imports gmpy2, mpmath and numpy; CC compiles C.
#   4. proof step 2 (small X): compiles object/search677b.c, reruns "search677b 1100000 20261106" and
#      object/verify_cands.py; the outputs must equal object/out/search_N1.1e6.txt and verify_N1.1e6.txt
#      (times stripped). The exact judge verify-it-yourself/check677.py must reject the two near-misses.
#   5. reruns, JOBS at a time: taskA_ratio_audit_k.py 400 26 28 (step 3; byte-identical output), rig_margin.py 26 28
#      1000000 1 1000 (step 4, interval arithmetic) and the enumeration (step 5; QEXP=495, 1040 digits, eta 0.001,
#      X0 1000000) of k = 27 on shard 0 of 4 (object/shard_rig.py), whose k = 27 line must equal the saved one.
#      With --all: all four shards for k = 26..28 (each whole output equal to its saved file, times stripped) and
#      rig_margin_exact.py per k (each equal to its saved output, time_s stripped).
# Last line of output: PASS or FAIL (exit status 0 or 1).
# What it cannot check: the hand proof of Lemma A and the argument that makes the enumeration complete
# (object/PROOF.md, to be read), and the float64 pre-filters and 1090-digit non-interval arithmetic inside
# deep_rig.py, which a rerun reproduces but does not prove correct.

SUMS='b461c7024f94a9487ab922b5558e017fcc747c56ce123b07d5083862307a2f81 object/PROOF.md
dc74be2f2b68c5618437b9b972f7313621ab556360a33e7e784e5f0dc82e6b85 object/deep_cf.py
0e7d7d72f04e5076827c28afb1184f5ef3eb69c3a4be965a6c2e770cd6ad0341 object/deep_rig.py
de27e17ffa4585c3511fb782af030b9570ab772d8b9ed707f00708b1950b1c13 object/out/deep_rig_shard0.txt
566af51ccbd48cafb54dccd6c03ec79becfc018a3ab8b85160d75c7ed4779555 object/out/deep_rig_shard1.txt
82de59df6124ce9853c51de197c101d20fe6c4780f388548be5a536e6f95a187 object/out/deep_rig_shard2.txt
481346c412fcf3d853ec98b87bc88d53f1c30a1b03c3412646c671f6cdbeca9a object/out/deep_rig_shard3.txt
0f5ad4e060971074a4378281d9696fcbe4917516987b3198ee37a2b6b55e75f0 object/out/rig_margin_exact_k26.txt
14226025f900d5353be52a4f8a7134d2737cfd299642ae434fcf7eb3988b6e60 object/out/rig_margin_exact_k27.txt
dfef8b097f9134b51f9330edb8e3c39d8725d25dac733c00175e20230f0c7cf8 object/out/rig_margin_exact_k28.txt
588060cf03232bb2e65289fc0bb6a4993aa79e9623e0bac05abcdf46f19bda02 object/out/rig_margin_k26-28.txt
20f5ee6956166e16f7b700e08cf47321d7adad0d45de0916ba9c42627afae052 object/out/search_N1.1e6.log
c3c75fb3fad9a5d125b3c9262df62a0b4524b6bcbf09e3aa28a7a3bcb487ee34 object/out/search_N1.1e6.txt
22c9f291140b5fa541674b2cbe41516be62fed6cabb4a81f36a0d3816bddc82e object/out/shard_sums.txt
124a8fc4605b695c56a627bd141e4f82c1da51d84770ae9a0e1c5301763084da object/out/taskA_ratio_audit_k26-28.txt
560873dc0712ddd08d822d18eb3f54097bc5a40c8274d33510c8729e1334ff84 object/out/verify_N1.1e6.txt
3d1b50ab5f638def5d0dea18099a701c263d80caf8a4e1e3ea8db2dcde924e76 object/rig_margin.py
64328c1f47d3ef88418e8e77b462f6b70ea2aa3438e6249e1194b52e96d3f12b object/rig_margin_exact.py
d9c01611ba8e1fa5fff4a54c1c08b7a1d44689707fc98e8d60dfd054e460caa9 object/search677b.c
41cdb740e45b1b9fd7ed219be63cfcc8f1916a3f1924d6522568287b1a90d130 object/shard_rig.py
bebff93f5e06f9cf019ae79cf7b41ccb7dfc8879631d05a5c62aac0e1c521642 object/sum_shards.py
ce6fa546045e398f00b5fd1980e74a04c5d59ffecea547fe25d7384f900871e5 object/taskA_ratio_audit_k.py
5e848cf39dd1b793e12a20cc3fae8ea8c2422e904e840ba0e29bb9ac418154d8 object/verify_cands.py'
TOTAL_LINE="TOTAL pairs=58926 failures=0 undecided=0"
DEEP_TAIL="product solutions=0 (X0=1000000, QMAX=10^495)"

say() { printf '%s\n' "$*"; }
WORK=""
cleanup() { if [ -n "$WORK" ]; then rm -rf "$WORK"; fi; }
fail() { say "problem: $*"; cleanup; say FAIL; exit 1; }
trap 'cleanup' EXIT
trap 'say "interrupted"; cleanup; say FAIL; exit 1' INT TERM

PY=${PY:-python3}; CC=${CC:-cc}; JOBS=${JOBS:-4}
case "$PY" in /*) ;; */*) PY="$(pwd)/$PY" ;; esac   # a relative PY is relative to where the script was started
cd "$(dirname "$0")/.." || { say "cannot enter the package folder"; say FAIL; exit 1; }
PKGDIR=$(pwd)

MODE=default
while [ $# -gt 0 ]; do
  case "$1" in
    --all) MODE=all ;;
    -h|--help) sed -n '2,32p' "$0"; exit 0 ;;
    *) fail "unknown option $1 (use --all, or --help)" ;;
  esac
  shift
done

case "$JOBS" in ''|*[!0-9]*|0) fail "JOBS must be a positive integer" ;; esac
for t in cmp comm sed awk grep xargs mktemp tail date wc sort find tr; do
  command -v "$t" >/dev/null 2>&1 || fail "needs $t on PATH"
done
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"
elif command -v shasum >/dev/null 2>&1; then SHA="shasum -a 256"
else fail "needs sha256sum or shasum"; fi
NICE=""; if command -v nice >/dev/null 2>&1; then NICE="nice -n 10"; fi
WORK=$(mktemp -d 2>/dev/null || mktemp -d -t v3r1t4s) || fail "cannot create a scratch folder"
hash_of() { $SHA < "$1" | awk '{print $1}'; }
T0=$(date +%s)

say "package check: erdos-677-lcm-blocks (Erdos 677 = JSP-000550), no counterexample with 26 <= k <= 28, 0 <= n <= 10^494, any m >= n + k"
say "mode: $MODE, parallel jobs: $JOBS"

# 1. object integrity ------------------------------------------------------------------------------------------
printf '%s\n' "$SUMS" > "$WORK/sums.txt"
while read -r want f; do
  [ -f "$f" ] || fail "$f is missing"
  got=$(hash_of "$f")
  [ "$got" = "$want" ] || fail "$f has sha256 $got, the package records $want (the file is not the one the panel read)"
done < "$WORK/sums.txt"
awk '{print $2}' "$WORK/sums.txt" | sort > "$WORK/listed.txt"
find object -type f | sort > "$WORK/present.txt"
extra=$(comm -13 "$WORK/listed.txt" "$WORK/present.txt" 2>/dev/null | tr '\n' ' ')
[ -z "$extra" ] || fail "object/ holds files that are not part of the claim: $extra"
say "step 1 object files: $(wc -l < "$WORK/sums.txt" | tr -d ' ') files, sha256 equal to the recorded values, no other file: ok"

# 2. the saved outputs ---------------------------------------------------------------------------------------
O=object/out
grep -q '^# COMPLETE kmin=3 kmax=147 total_candidates=2 ' "$O/search_N1.1e6.txt" || fail "$O/search_N1.1e6.txt has no COMPLETE line with 2 candidates"
grep -qx 'candidates: 2 exact-equal: 0 disjoint candidates: 2 disjoint exact-equal: 0' "$O/verify_N1.1e6.txt" || fail "$O/verify_N1.1e6.txt does not report 0 exact-equal"
grep -qx 'TOTAL missing over k=26..28: 0' "$O/taskA_ratio_audit_k26-28.txt" || fail "$O/taskA_ratio_audit_k26-28.txt does not report 0 missing ratios"
grep -q '; r outside sets: 0$' "$O/taskA_ratio_audit_k26-28.txt" || fail "$O/taskA_ratio_audit_k26-28.txt: brute-force ratios outside the sets"
[ "$(tail -n 1 "$O/rig_margin_k26-28.txt")" = "$TOTAL_LINE" ] || fail "$O/rig_margin_k26-28.txt does not end with '$TOTAL_LINE'"
for kn in "26 21262" "27 16402" "28 21262"; do
  set -- $kn
  [ "$(tail -n 1 "$O/rig_margin_exact_k$1.txt")" = "TOTAL pairs=$2 failures=0 undecided=0" ] || fail "$O/rig_margin_exact_k$1.txt does not end with 'TOTAL pairs=$2 failures=0 undecided=0'"
done
cat "$O"/deep_rig_shard0.txt "$O"/deep_rig_shard1.txt "$O"/deep_rig_shard2.txt "$O"/deep_rig_shard3.txt > "$WORK/deep_saved_all.txt"
grep '^k=' "$WORK/deep_saved_all.txt" | sed -E 's/ t=[0-9]+s$//' > "$WORK/deep_saved_k.txt"
for i in 0 1 2 3; do
  f="$O/deep_rig_shard$i.txt"
  [ "$(sed -n 1p "$f")" = "SHARD $i/4" ] || fail "$f does not start with 'SHARD $i/4'"
  ks=$(grep '^k=' "$f" | awk -F'[= ]' '{printf "%s ", $2}')
  [ "$ks" = "26 27 28 " ] || fail "$f does not hold exactly one line for each k = 26, 27, 28 (found: $ks)"
  last=$(tail -n 1 "$f")
  case "$last" in "TOTAL window candidates="*" $DEEP_TAIL") ;; *) fail "$f ends with '$last'" ;; esac
done
grep -v ' product_solutions=0$' "$WORK/deep_saved_k.txt" > "$WORK/bad.txt" && fail "a saved shard line reports a product solution: $(head -n 1 "$WORK/bad.txt")"
grep -q 'PRODUCT SOLUTION' "$WORK/deep_saved_all.txt" && fail "a saved shard output reports a PRODUCT SOLUTION"
for kn in "26 21262" "27 16402" "28 21262"; do
  set -- $kn
  n=$(grep "^k=$1 " "$WORK/deep_saved_k.txt" | sed -n 's/.* admissible_r=\([0-9]*\) .*/\1/p' | awk '{s += $1} END {print s}')
  [ "$n" = "$2" ] || fail "the four shards' admissible_r counts for k=$1 add up to $n, expected $2 (len(admissible_r($1)))"
done
wsum=$(sed -n 's/.* window_candidates=\([0-9]*\) .*/\1/p' "$WORK/deep_saved_k.txt" | awk '{s += $1} END {print s}')
tsum=$(sed -n 's/^TOTAL window candidates=\([0-9]*\) .*/\1/p' "$WORK/deep_saved_all.txt" | awk '{s += $1} END {print s}')
[ "$wsum" = 1455391 ] && [ "$tsum" = 1455391 ] || fail "saved shard window candidates add up to $wsum (per k) and $tsum (TOTAL lines), expected 1455391"
say "step 2 saved outputs: search COMPLETE with 2 candidates, 0 exact-equal; 0 missing ratios for k = 26..28; both margin checkers 0 failures (58926 pairs); 4 shards, ratio counts 21262 + 16402 + 21262, product_solutions=0 everywhere, $wsum window candidates: ok"

# 3. tools ---------------------------------------------------------------------------------------------------
command -v "$PY" >/dev/null 2>&1 || fail "Python not found: PY=$PY (set PY to a Python 3 that has gmpy2, mpmath and numpy)"
missing=""
for mod in gmpy2 mpmath numpy; do
  $PY -I -B -c "import $mod" > /dev/null 2>&1 || missing="$missing $mod"
done
[ -z "$missing" ] || fail "the Python at PY=$PY lacks:$missing. Install them, for example: python3 -m venv v && v/bin/pip install gmpy2 mpmath numpy, then rerun with PY=v/bin/python3"
say "python: $($PY -I -B -c 'import sys, gmpy2, mpmath, numpy; print(sys.version.split()[0], "gmpy2", gmpy2.version(), "mpmath", mpmath.__version__, "numpy", numpy.__version__)')"
command -v "$CC" >/dev/null 2>&1 || fail "C compiler not found: CC=$CC"
say "step 3 tools: ok"

# 4. proof step 2: small X ------------------------------------------------------------------------------------
strip_search() { sed -E 's/ t=[0-9]+s$//; s/ elapsed=[0-9]+s$//' "$1"; }
"$CC" -O2 -o "$WORK/search677b" object/search677b.c -lm > "$WORK/cc.log" 2>&1 || { cat "$WORK/cc.log"; fail "object/search677b.c does not compile"; }
t0=$(date +%s)
$NICE "$WORK/search677b" 1100000 20261106 "$WORK/search.txt" > "$WORK/search.err" 2>&1 &
pid=$!; [ -n "${PIDLOG:-}" ] && say "$(date -u +%Y-%m-%dT%H:%M:%SZ) search677b pid $pid" >> "$PIDLOG"
wait $pid; rc=$?
t1=$(date +%s)
[ "$rc" = 0 ] || { cat "$WORK/search.err"; fail "search677b 1100000 20261106 exited with status $rc"; }
clast=$(tail -n 1 "$WORK/search.txt")
case "$clast" in "# COMPLETE kmin=3 kmax=147 total_candidates=2 "*) ;; *) fail "search677b: last line is '$clast'" ;; esac
strip_search "$WORK/search.txt" > "$WORK/a.txt"; strip_search "$O/search_N1.1e6.txt" > "$WORK/b.txt"
cmp "$WORK/a.txt" "$WORK/b.txt" > /dev/null 2>&1 || fail "search677b output differs from $O/search_N1.1e6.txt (times stripped)"
say "  search677b 1100000 20261106: exit 0, $((t1 - t0)) s, '$clast'; equal to $O/search_N1.1e6.txt (times stripped)"
$NICE $PY -I -B object/verify_cands.py "$WORK/search.txt" > "$WORK/verify.txt" 2> "$WORK/verify.err" || { cat "$WORK/verify.err"; fail "verify_cands.py failed"; }
vline=$(grep "^candidates:" "$WORK/verify.txt")
grep -qx 'candidates: 2 exact-equal: 0 disjoint candidates: 2 disjoint exact-equal: 0' "$WORK/verify.txt" || fail "verify_cands.py: '$vline'"
strip_search "$WORK/verify.txt" > "$WORK/a.txt"; strip_search "$O/verify_N1.1e6.txt" > "$WORK/b.txt"
cmp "$WORK/a.txt" "$WORK/b.txt" > /dev/null 2>&1 || fail "verify_cands.py output differs from $O/verify_N1.1e6.txt (times stripped)"
say "  verify_cands.py: '$vline'; equal to $O/verify_N1.1e6.txt (times stripped)"
for t in "4 13 3" "18 53 4"; do
  # shellcheck disable=SC2086
  $PY -I -B verify-it-yourself/check677.py $t > "$WORK/j.txt" 2>&1
  jrc=$?
  if [ "$jrc" = 1 ] && [ "$(tail -n 1 "$WORK/j.txt")" = FAIL ] && grep -qx 'problem: lcms differ' "$WORK/j.txt"; then
    say "  exact judge check677.py $t (n m k): $(sed -n 1p "$WORK/j.txt"), $(sed -n 2p "$WORK/j.txt"): lcms differ, not a counterexample"
  else
    cat "$WORK/j.txt"; fail "check677.py $t should print 'problem: lcms differ' and FAIL"
  fi
done
say "step 4 small X (n + k <= 1100000, every k, every m): ok"

# 5. the Python reruns, JOBS at a time --------------------------------------------------------------------------
export PKGDIR WORK PY NICE
PIDLOG=${PIDLOG:-}; export PIDLOG
export QEXP=495
unset WINDOW_PREFILTER UMULT
cat > "$WORK/task.sh" <<'EOF'
name=$1
cd "$PKGDIR" || exit 0
case "$name" in
  taskA) set -- object/taskA_ratio_audit_k.py 400 26 28 ;;
  rigm) set -- object/rig_margin.py 26 28 1000000 1 1000 ;;
  rigx_*) k=${name#rigx_}; set -- object/rig_margin_exact.py "$k" "$k" 1000000 1 1000 ;;
  s27_0) export SHARD=0/4; set -- object/shard_rig.py 27 27 1040 0.001 1000000 ;;
  shard_*) export SHARD=${name#shard_}/4; set -- object/shard_rig.py 26 28 1040 0.001 1000000 ;;
  *) echo "127 0" > "$WORK/$name.rc"; exit 0 ;;
esac
t0=$(date +%s)
$NICE $PY -I -B "$@" > "$WORK/$name.out" 2> "$WORK/$name.err" &
pid=$!
[ -n "$PIDLOG" ] && echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $name pid $pid" >> "$PIDLOG"
wait $pid
rc=$?
echo "$rc $(( $(date +%s) - t0 ))" > "$WORK/$name.rc"
echo "  finished $name ($*): exit $rc, $(( $(date +%s) - t0 )) s"
exit 0
EOF
if [ "$MODE" = all ]; then
  TASKS="shard_0 shard_1 shard_2 shard_3 rigx_26 rigx_27 rigx_28 rigm taskA"
else
  TASKS="s27_0 rigm taskA"
fi
say "step 5 reruns ($MODE): $TASKS"
printf '%s\n' $TASKS | xargs -n 1 -P "$JOBS" sh "$WORK/task.sh" || fail "could not run the jobs"
for n in $TASKS; do
  [ -f "$WORK/$n.rc" ] || fail "job $n did not run"
  rc=$(awk '{print $1}' "$WORK/$n.rc")
  [ "$rc" = 0 ] || { tail -n 20 "$WORK/$n.err"; fail "job $n exited with status $rc"; }
done
cmp "$WORK/taskA.out" "$O/taskA_ratio_audit_k26-28.txt" > /dev/null 2>&1 || fail "taskA_ratio_audit_k.py 400 26 28 output differs from $O/taskA_ratio_audit_k26-28.txt"
say "  taskA_ratio_audit_k.py 400 26 28: 'TOTAL missing over k=26..28: 0'; byte-identical to $O/taskA_ratio_audit_k26-28.txt"
strip_margin() { sed -E 's/ time_s=[0-9.]+//' "$1"; }
check_margin() { # JOB SAVED LABEL TOTALLINE
  [ "$(tail -n 1 "$WORK/$1.out")" = "$4" ] || fail "$3: last line is '$(tail -n 1 "$WORK/$1.out")'"
  strip_margin "$WORK/$1.out" > "$WORK/a.txt"; strip_margin "$2" > "$WORK/b.txt"
  cmp "$WORK/a.txt" "$WORK/b.txt" > /dev/null 2>&1 || fail "$3: output differs from $2 (time_s stripped)"
  say "  $3: '$4'; equal to $2 (time_s stripped)"
}
check_margin rigm "$O/rig_margin_k26-28.txt" "rig_margin.py 26 28 1000000 1 1000" "$TOTAL_LINE"
if [ "$MODE" = all ]; then
  check_margin rigx_26 "$O/rig_margin_exact_k26.txt" "rig_margin_exact.py 26 26 1000000 1 1000" "TOTAL pairs=21262 failures=0 undecided=0"
  check_margin rigx_27 "$O/rig_margin_exact_k27.txt" "rig_margin_exact.py 27 27 1000000 1 1000" "TOTAL pairs=16402 failures=0 undecided=0"
  check_margin rigx_28 "$O/rig_margin_exact_k28.txt" "rig_margin_exact.py 28 28 1000000 1 1000" "TOTAL pairs=21262 failures=0 undecided=0"
fi
strip_deep() { sed -E 's/ t=[0-9]+s$//' "$1"; }
if [ "$MODE" = all ]; then
  for i in 0 1 2 3; do
    grep -q 'PRODUCT SOLUTION' "$WORK/shard_$i.out" && fail "shard $i reports: $(grep 'PRODUCT SOLUTION' "$WORK/shard_$i.out" | head -n 1)"
    strip_deep "$WORK/shard_$i.out" > "$WORK/a.txt"; strip_deep "$O/deep_rig_shard$i.txt" > "$WORK/b.txt"
    cmp "$WORK/a.txt" "$WORK/b.txt" > /dev/null 2>&1 || fail "shard $i: output differs from $O/deep_rig_shard$i.txt (times stripped)"
    say "  shard $i (k = 26..28): '$(tail -n 1 "$WORK/shard_$i.out")'; whole output equal to $O/deep_rig_shard$i.txt (times stripped)"
  done
  say "step 5 reruns: ratio audit, both margin checkers and the whole enumeration equal the saved outputs: ok"
else
  grep -q 'PRODUCT SOLUTION' "$WORK/s27_0.out" && fail "shard 0, k=27 reports a PRODUCT SOLUTION"
  line=$(grep '^k=27 ' "$WORK/s27_0.out" | sed -E 's/ t=[0-9]+s$//')
  want=$(grep '^k=27 ' "$O/deep_rig_shard0.txt" | sed -E 's/ t=[0-9]+s$//')
  [ -n "$line" ] && [ "$line" = "$want" ] || fail "shard 0, k=27: '$line' differs from the saved line '$want'"
  say "  shard 0 of 4, k=27: $(printf '%s' "$line" | sed 's/^k=27 //'): equal to the saved line"
  say "step 5 reruns: ratio audit, interval margin checker and the enumeration of k = 27 (shard 0 of 4) equal the saved outputs: ok"
  say "  (not rerun by default: the other shards and k values, and rig_margin_exact.py; use --all)"
fi
say "total time: $(( $(date +%s) - T0 )) s"
say PASS
exit 0
