#!/bin/sh
# Check this package: Erdos Problem 677 (Justin Sun Prize JSP-000550), no counterexample with 1 <= k <= 25,
# 0 <= n <= 10^494 and any m >= n + k. Run from the package folder:
#   sh verify-it-yourself/run_checks.sh          default checks, about 5 to 10 minutes with 3 parallel jobs
#   sh verify-it-yourself/run_checks.sh --all    also reruns k = 17..25 and the exact-rational margin checker
#                                                (several hours of CPU; about 1 to 2 hours with 3 jobs)
# Needs: Python 3 with gmpy2, mpmath and numpy (set PY to that interpreter; default python3), a C compiler (CC,
# default cc), sha256sum or shasum, and POSIX tools (cmp, sed, awk, grep, xargs, mktemp). Environment: PY,
# CC, JOBS (parallel Python jobs, default 3), PIDLOG (optional file: each job's start time, name and PID are
# appended to it). About 1 GB of memory per job. All jobs run at nice -n 10. Nothing is written into the package.
# What it does, in order (it stops at the first problem):
#   1. the 19 files in object/ are the ones the panel read: their sha256 must equal the values recorded below
#      (and in README.md); object/ must hold no other file.
#   2. the saved outputs in object/out/ say what the claim says (0 exact-equal, 0 missing ratios,
#      63041 margin pairs with 0 failures, product_solutions=0 for every k = 3..25, 1174616 window candidates).
#   3. tools: PY imports gmpy2, mpmath and numpy; CC compiles C.
#   4. proof step 2 (small X): compiles object/search677b.c, reruns "search677b 1100000 4242" and
#      object/verify_cands.py; the outputs must equal object/out/search_N1.1e6.txt and verify_N1.1e6.txt
#      (times stripped), with the COMPLETE line and "exact-equal: 0". The exact judge
#      verify-it-yourself/check677.py must reject the two near-misses it lists.
#   5. reruns, JOBS at a time: taskA_ratio_audit.py 3000 (proof step 3; byte-identical output, "TOTAL missing over
#      k=3..25: 0"), rig_margin.py 3 25 1000000 1 1000 (step 4, interval arithmetic; "TOTAL pairs=63041
#      failures=0 undecided=0"), and deep_rig.py (step 5; QEXP=495, 1040 digits, eta 0.001, X0 1000000) for
#      k = 3..16, whose per-k lines must equal those of object/out/deep_rig_final_k3-18_d1040.txt (times
#      stripped). With --all: deep_rig.py exactly as the five commands of how-we-built-it/claim/REPRODUCE.md
#      (k = 3..18, 19..22, 23, 24, 25), each output equal to its saved file (times stripped), and
#      rig_margin_exact.py 3 25 1000000 1 1000 (exact rationals), equal to its saved output (times stripped).
# Last line of output: PASS or FAIL (exit status 0 or 1).
# What it cannot check: the hand proof of Lemma A and the argument that makes the enumeration complete
# (object/PROOF.md, to be read), and the float64 pre-filters and 1090-digit non-interval arithmetic inside
# deep_rig.py, which a rerun reproduces but does not prove correct.

SUMS='201bcc74dfe80bd57d43eb3f97330d8dc702623df9808c6ebc00f27b21b01e83 object/PROOF.md
dc74be2f2b68c5618437b9b972f7313621ab556360a33e7e784e5f0dc82e6b85 object/deep_cf.py
0e7d7d72f04e5076827c28afb1184f5ef3eb69c3a4be965a6c2e770cd6ad0341 object/deep_rig.py
2dbf20009051900358a3c77eb2ad221c8b877a065f97c75e5c3d795e33bcc4e9 object/out/deep_rig_final_k19-22_d1040.txt
03c6fb85078e5c6db93311814685693f94af87d0ff556a246e3205694ab58ec3 object/out/deep_rig_final_k23-23_d1040.txt
b508f922dc4f197bdb9af0b463ae1a7f3e3127c54161f3c90fda8897607c39e3 object/out/deep_rig_final_k24-24_d1040.txt
8e66ec2f182ba8bd9691520368726fe4b9ede8f2d97fc64923255ea7fcee4554 object/out/deep_rig_final_k25-25_d1040.txt
b77f25bee478df026ea2d1aa128cf436a44ce0e0f81df8994f41ff5674548f6f object/out/deep_rig_final_k3-18_d1040.txt
f1c60d38cbf1ca40895d596abac0bb17e3445a277cbeaeb56df877eb79201819 object/out/rig_margin_exact_k3-25_X1e6_eta1e-3.txt
a22430cbe811f6d31bc4a5dafe9a34dd3192993812ff83b28b50a12d1a4a1511 object/out/rig_margin_k3-25_X1e6_eta1e-3.txt
ff9851d66ae0c5a8169d75b39f9c6ea863e6fbb7e83b9d4a9c98623e7089fb31 object/out/search_N1.1e6.log
ce706f1126bfe0531ada631fdb98b3ef3897273f2409f9f1c8ed1a181036d38f object/out/search_N1.1e6.txt
2d57206bc9fd3d038e1843f80a9fb9a2c7e62e5631339df718beff620e3faa46 object/out/taskA_ratio_audit_NB3000.txt
23cf2e6066042259d2f128d7c74c29e07b95cb7f5e29e85a32f25352b997818f object/out/verify_N1.1e6.txt
3d1b50ab5f638def5d0dea18099a701c263d80caf8a4e1e3ea8db2dcde924e76 object/rig_margin.py
64328c1f47d3ef88418e8e77b462f6b70ea2aa3438e6249e1194b52e96d3f12b object/rig_margin_exact.py
d9c01611ba8e1fa5fff4a54c1c08b7a1d44689707fc98e8d60dfd054e460caa9 object/search677b.c
1b520c69a4ba5c757a8efd540284527f7bd99dfd9dc0bc0de44ceff9ea4ee152 object/taskA_ratio_audit.py
5e848cf39dd1b793e12a20cc3fae8ea8c2422e904e840ba0e29bb9ac418154d8 object/verify_cands.py'
TOTAL_LINE="TOTAL pairs=63041 failures=0 undecided=0"
DEEP_TAIL="product solutions=0 (X0=1000000, QMAX=10^495)"

say() { printf '%s\n' "$*"; }
WORK=""
cleanup() { if [ -n "$WORK" ]; then rm -rf "$WORK"; fi; }
fail() { say "problem: $*"; cleanup; say FAIL; exit 1; }
trap 'cleanup' EXIT
trap 'say "interrupted"; cleanup; say FAIL; exit 1' INT TERM

PY=${PY:-python3}; CC=${CC:-cc}; JOBS=${JOBS:-3}
case "$PY" in /*) ;; */*) PY="$(pwd)/$PY" ;; esac   # a relative PY is relative to where the script was started
cd "$(dirname "$0")/.." || { say "cannot enter the package folder"; say FAIL; exit 1; }
PKGDIR=$(pwd)

MODE=default
while [ $# -gt 0 ]; do
  case "$1" in
    --all) MODE=all ;;
    -h|--help) sed -n '2,31p' "$0"; exit 0 ;;
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

say "package check: erdos-677-lcm-blocks (Erdos 677 = JSP-000550), no counterexample with 1 <= k <= 25, 0 <= n <= 10^494, any m >= n + k"
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
grep -qx 'TOTAL missing over k=3..25: 0' "$O/taskA_ratio_audit_NB3000.txt" || fail "$O/taskA_ratio_audit_NB3000.txt does not report 0 missing ratios"
grep -q '; r outside sets: 0$' "$O/taskA_ratio_audit_NB3000.txt" || fail "$O/taskA_ratio_audit_NB3000.txt: brute-force ratios outside the sets"
for f in "$O/rig_margin_k3-25_X1e6_eta1e-3.txt" "$O/rig_margin_exact_k3-25_X1e6_eta1e-3.txt"; do
  [ "$(tail -n 1 "$f")" = "$TOTAL_LINE" ] || fail "$f does not end with '$TOTAL_LINE'"
done
cat "$O"/deep_rig_final_k3-18_d1040.txt "$O"/deep_rig_final_k19-22_d1040.txt "$O"/deep_rig_final_k23-23_d1040.txt \
    "$O"/deep_rig_final_k24-24_d1040.txt "$O"/deep_rig_final_k25-25_d1040.txt > "$WORK/deep_saved_all.txt"
grep '^k=' "$WORK/deep_saved_all.txt" | sed -E 's/ t=[0-9]+s$//' > "$WORK/deep_saved_k.txt"
ks=$(awk -F'[= ]' '{printf "%s ", $2}' "$WORK/deep_saved_k.txt")
[ "$ks" = "3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 " ] || fail "saved deep_rig outputs do not hold exactly one line for each k = 3..25 (found: $ks)"
grep -v ' product_solutions=0$' "$WORK/deep_saved_k.txt" > "$WORK/bad.txt" && fail "a saved deep_rig line reports a product solution: $(head -n 1 "$WORK/bad.txt")"
grep -q 'PRODUCT SOLUTION' "$WORK/deep_saved_all.txt" && fail "a saved deep_rig output reports a PRODUCT SOLUTION"
for f in "$O"/deep_rig_final_k*_d1040.txt; do
  last=$(tail -n 1 "$f")
  case "$last" in "TOTAL window candidates="*" $DEEP_TAIL") ;; *) fail "$f ends with '$last'" ;; esac
done
wsum=$(sed -n 's/.* window_candidates=\([0-9]*\) .*/\1/p' "$WORK/deep_saved_k.txt" | awk '{s += $1} END {print s}')
tsum=$(sed -n 's/^TOTAL window candidates=\([0-9]*\) .*/\1/p' "$WORK/deep_saved_all.txt" | awk '{s += $1} END {print s}')
[ "$wsum" = 1174616 ] && [ "$tsum" = 1174616 ] || fail "saved deep_rig window candidates add up to $wsum (per k) and $tsum (TOTAL lines), expected 1174616"
say "step 2 saved outputs: search COMPLETE with 2 candidates, 0 exact-equal; 0 missing ratios; both margin checkers '$TOTAL_LINE'; deep_rig k = 3..25 product_solutions=0, $wsum window candidates: ok"

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
$NICE "$WORK/search677b" 1100000 4242 "$WORK/search.txt" > "$WORK/search.err" 2>&1 &
pid=$!; [ -n "${PIDLOG:-}" ] && say "$(date -u +%Y-%m-%dT%H:%M:%SZ) search677b pid $pid" >> "$PIDLOG"
wait $pid; rc=$?
t1=$(date +%s)
[ "$rc" = 0 ] || { cat "$WORK/search.err"; fail "search677b 1100000 4242 exited with status $rc"; }
clast=$(tail -n 1 "$WORK/search.txt")
case "$clast" in "# COMPLETE kmin=3 kmax=147 total_candidates=2 "*) ;; *) fail "search677b: last line is '$clast'" ;; esac
strip_search "$WORK/search.txt" > "$WORK/a.txt"; strip_search "$O/search_N1.1e6.txt" > "$WORK/b.txt"
cmp "$WORK/a.txt" "$WORK/b.txt" > /dev/null 2>&1 || fail "search677b output differs from $O/search_N1.1e6.txt (times stripped)"
say "  search677b 1100000 4242: exit 0, $((t1 - t0)) s, '$clast'; equal to $O/search_N1.1e6.txt (times stripped)"
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
  taskA) set -- object/taskA_ratio_audit.py 3000 ;;
  rigm) set -- object/rig_margin.py 3 25 1000000 1 1000 ;;
  rigx) set -- object/rig_margin_exact.py 3 25 1000000 1 1000 ;;
  deep_*) a=${name#deep_}; set -- object/deep_rig.py "${a%-*}" "${a#*-}" 1040 0.001 1000000 ;;
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
  TASKS="deep_24-24 deep_19-22 rigx deep_25-25 deep_23-23 deep_3-18 rigm taskA"
else
  TASKS="rigm deep_15-16 deep_3-13 deep_14-14 taskA"
fi
say "step 5 reruns ($MODE): $TASKS"
printf '%s\n' $TASKS | xargs -n 1 -P "$JOBS" sh "$WORK/task.sh" || fail "could not run the jobs"
for n in $TASKS; do
  [ -f "$WORK/$n.rc" ] || fail "job $n did not run"
  rc=$(awk '{print $1}' "$WORK/$n.rc")
  [ "$rc" = 0 ] || { tail -n 20 "$WORK/$n.err"; fail "job $n exited with status $rc"; }
done

# taskA: byte-identical
cmp "$WORK/taskA.out" "$O/taskA_ratio_audit_NB3000.txt" > /dev/null 2>&1 || fail "taskA_ratio_audit.py 3000 output differs from $O/taskA_ratio_audit_NB3000.txt"
grep -qx 'TOTAL missing over k=3..25: 0' "$WORK/taskA.out" || fail "taskA_ratio_audit.py: no 'TOTAL missing over k=3..25: 0'"
say "  taskA_ratio_audit.py 3000: 'TOTAL missing over k=3..25: 0', $(sed -n 's/^brute force n<m<=3000: .*; \(total [0-9]*; r outside sets: [0-9]*\)$/\1/p' "$WORK/taskA.out"); byte-identical to $O/taskA_ratio_audit_NB3000.txt"

# margin checkers: identical with the time_s fields stripped
strip_margin() { sed -E 's/ time_s=[0-9.]+//' "$1"; }
check_margin() { # JOB SAVED LABEL
  [ "$(tail -n 1 "$WORK/$1.out")" = "$TOTAL_LINE" ] || fail "$3: last line is '$(tail -n 1 "$WORK/$1.out")'"
  strip_margin "$WORK/$1.out" > "$WORK/a.txt"; strip_margin "$2" > "$WORK/b.txt"
  cmp "$WORK/a.txt" "$WORK/b.txt" > /dev/null 2>&1 || fail "$3: output differs from $2 (time_s stripped)"
  say "  $3: '$TOTAL_LINE'; equal to $2 (time_s stripped)"
}
check_margin rigm "$O/rig_margin_k3-25_X1e6_eta1e-3.txt" "rig_margin.py 3 25 1000000 1 1000"
[ "$MODE" = all ] && check_margin rigx "$O/rig_margin_exact_k3-25_X1e6_eta1e-3.txt" "rig_margin_exact.py 3 25 1000000 1 1000"

# deep_rig: every per-k line equal to the saved one (times stripped), no product solution, TOTAL line
strip_deep() { sed -E 's/ t=[0-9]+s$//' "$1"; }
for n in $TASKS; do
  case "$n" in deep_*) ;; *) continue ;; esac
  a=${n#deep_}; lo=${a%-*}; hi=${a#*-}
  grep -q 'PRODUCT SOLUTION' "$WORK/$n.out" && fail "deep_rig.py $lo $hi reports: $(grep 'PRODUCT SOLUTION' "$WORK/$n.out" | head -n 1)"
  last=$(tail -n 1 "$WORK/$n.out")
  case "$last" in "TOTAL window candidates="*" $DEEP_TAIL") ;; *) fail "deep_rig.py $lo $hi: last line is '$last'" ;; esac
  k=$lo; wc_k=0
  while [ "$k" -le "$hi" ]; do
    line=$(grep "^k=$k " "$WORK/$n.out" | sed -E 's/ t=[0-9]+s$//')
    [ -n "$line" ] || fail "deep_rig.py $lo $hi printed no line for k=$k"
    grep -qxF "$line" "$WORK/deep_saved_k.txt" || fail "deep_rig.py k=$k: '$line' differs from the saved line '$(grep "^k=$k " "$WORK/deep_saved_k.txt")'"
    say "  k=$k: $(printf '%s' "$line" | sed 's/^k=[0-9]* //'): equal to the saved line"
    k=$((k + 1))
  done
  if [ "$MODE" = all ]; then
    saved="$O/deep_rig_final_k$lo-${hi}_d1040.txt"
    strip_deep "$WORK/$n.out" > "$WORK/a.txt"; strip_deep "$saved" > "$WORK/b.txt"
    cmp "$WORK/a.txt" "$WORK/b.txt" > /dev/null 2>&1 || fail "deep_rig.py $lo $hi: output differs from $saved (times stripped)"
    say "  deep_rig.py $lo $hi: '$last'; whole output equal to $saved (times stripped)"
  else
    say "  deep_rig.py $lo $hi: '$last'"
  fi
done
if [ "$MODE" = all ]; then
  say "step 5 reruns: ratio audit, both margin checkers and the enumeration for every k = 3..25 equal the saved outputs: ok"
else
  say "step 5 reruns: ratio audit, interval margin checker and the enumeration for k = 3..16 equal the saved outputs: ok"
  say "  (not rerun by default: deep_rig.py k = 17..25 and rig_margin_exact.py; use --all)"
fi
say "total time: $(( $(date +%s) - T0 )) s"
say PASS
exit 0
