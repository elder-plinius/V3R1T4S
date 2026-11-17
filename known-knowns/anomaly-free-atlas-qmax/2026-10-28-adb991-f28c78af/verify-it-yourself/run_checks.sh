#!/bin/sh
# Check this package's census rows. Run from the package folder:
#   sh verify-it-yourself/run_checks.sh              the default rows (DEFAULT_ROWS below)
#   sh verify-it-yourself/run_checks.sh --all        every row of object/counts.txt
#   sh verify-it-yourself/run_checks.sh --rows "SM:34 SM:35"    chosen rows
#   add --both to run every lister object/counts.txt records for a row (default: one lister per row)
# Needs: a C compiler with OpenMP (gcc), python3 (standard library), sha256sum or shasum, and POSIX tools
# (tee, mkfifo, wc, awk, sed, xargs, gzip). Environment: THREADS (lister threads for csenum2, default 3), JOBS
# (parallel counter processes, default 3), PAR (single-threaded acclist streams run at the same time, default 2),
# PYMAX (largest list also read by the Python checker, default 2000000 lines), KEEP=1 keeps the scratch folder.
# Nothing large is written to disk: each list is streamed once.
# What it does, in order (it stops at the first problem):
#   1. verify-it-yourself/rows.py reads object/counts.txt: exactly the claimed rows, count = lines + 1, valid hashes.
#   2. compiles the claim's sources (how-we-built-it/source/) and the C checker (verify-it-yourself/checklist.c).
#   3. stored lists in object/ (if any): sha256, line count, C checker and Python checker on the stored bytes.
#   4. recounts without listing (mitm.c, a meet-in-the-middle counter that never lists): first reproduces the twenty
#      published Allanach-Davighi-Melville values (Q_max 1..10, both contents), then each selected row's count.
#   5. regenerates each selected row's list with its lister and streams the same bytes into sha256, wc -l and the
#      C checker (and the Python checker for small lists); all must equal object/counts.txt. The lister's own exit
#      status is captured and must be 0 (the same guard as `set -o pipefail`: a crashed lister cannot pass as a
#      short or empty list).
# Last line of output: PASS or FAIL (exit status 0 or 1).
TARGET="anomaly-free-atlas-qmax: SMnuR Q_max 19 and SM Q_max 32..35"
PKG_ROWS="SMnuR:19 SM:32 SM:33 SM:34 SM:35"
# default: a subset that runs in about 6 to 10 minutes on 3 cores (SM 32 and 33, their two lists streamed at the
# same time); --all adds SM 34, 35 (about 8 more minutes) and SMnuR 19 (about 90 minutes on 3 threads and about
# 4.4 GB of memory)
DEFAULT_ROWS="SM:32 SM:33"
PREF_SM="acclist"; PREF_SMnuR="csenum2"


# ---------------------------------------------------------------------------------------------------------------
# Below is the code of the earlier census packages of this target (2026-10-23-adb991-81997531 and
# 2026-10-23-adb991-0728c1c8) with three changes: step 4 recounts with mitm.c instead of count.c + conventions.py
# (count.c needs hours at SM 34, 35 and SMnuR 19), step 5 runs up to PAR single-threaded acclist streams at the same
# time, and rows.py accepts Q_max up to 40.
# ---------------------------------------------------------------------------------------------------------------
# Published Solutions column of Allanach-Davighi-Melville, arXiv:1812.04602v5 Table 2 (SM) and Table 3 (SMnuR),
# Q_max = 1..10 (copied from the-record-we-beat/STATUS_RECORD.md). The counter must reproduce all twenty.
ADM_SM="8 22 82 251 626 1983 3902 7068 14354 23800"
ADM_SMNUR="38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920"

say() { printf '%s\n' "$*"; }
WORK=""
cleanup() { if [ -n "$WORK" ] && [ -z "${KEEP:-}" ]; then rm -rf "$WORK"; fi; }
fail() { say "problem: $*"; cleanup; say FAIL; exit 1; }
trap 'cleanup' EXIT
trap 'say "interrupted"; cleanup; say FAIL; exit 1' INT TERM

cd "$(dirname "$0")/.." || { say "cannot enter the package folder"; say FAIL; exit 1; }

SEL="$DEFAULT_ROWS"; MODE=default; BOTH=0
while [ $# -gt 0 ]; do
  case "$1" in
    --all) SEL="$PKG_ROWS"; MODE=all ;;
    --rows) shift; [ $# -gt 0 ] || fail "--rows needs a value such as \"SM:34 SMnuR:19\""; SEL="$1"; MODE=chosen ;;
    --both) BOTH=1 ;;
    -h|--help) sed -n '2,40p' "$0"; exit 0 ;;
    *) fail "unknown option $1 (use --all, --rows \"CONTENT:QMAX ...\", --both)" ;;
  esac
  shift
done
for r in $SEL; do
  case " $PKG_ROWS " in *" $r "*) ;; *) fail "row $r is not part of this claim (rows: $PKG_ROWS)" ;; esac
done

THREADS=${THREADS:-3}; JOBS=${JOBS:-3}; PAR=${PAR:-2}; PYMAX=${PYMAX:-2000000}; CC=${CC:-gcc}
for t in "$CC" python3 tee mkfifo wc awk sed xargs gzip date; do
  command -v "$t" >/dev/null 2>&1 || fail "needs $t on PATH"
done
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"
elif command -v shasum >/dev/null 2>&1; then SHA="shasum -a 256"
else fail "needs sha256sum or shasum"; fi
WORK=$(mktemp -d 2>/dev/null || mktemp -d -t v3r1t4s) || fail "cannot create a scratch folder"

hash_of() { $SHA < "$1" | awk '{print $1}'; }
say "package check: $TARGET ($MODE rows: $SEL)"
say "object/counts.txt sha256: $(hash_of object/counts.txt)"
say "threads per csenum2 lister: $THREADS, parallel counter jobs: $JOBS, parallel acclist streams: $PAR, Python checker on lists up to $PYMAX lines"

# 1. the object file is internally consistent and holds exactly the claimed rows
python3 verify-it-yourself/rows.py object/counts.txt $PKG_ROWS > "$WORK/rows.txt" || { cat "$WORK/rows.txt"; fail "object/counts.txt"; }
say "step 1 counts file: $(wc -l < "$WORK/rows.txt" | tr -d ' ') rows, count = lines + 1 in every row: ok"

# 2. build (sources as shipped; sha256 printed so a reader can match them with SHA256SUMS)
mkdir "$WORK/bin" || fail "scratch folder"
NEED=$(awk '{print $6}' "$WORK/rows.txt" | tr ',' '\n' | sort -u)
"$CC" -O2 -o "$WORK/bin/checklist" verify-it-yourself/checklist.c > "$WORK/cc.log" 2>&1 || { cat "$WORK/cc.log"; fail "checklist.c does not compile"; }
"$CC" -O3 -o "$WORK/bin/mitm" how-we-built-it/source/mitm.c > "$WORK/cc.log" 2>&1 || { cat "$WORK/cc.log"; fail "mitm.c does not compile"; }
for l in $NEED; do
  case "$l" in
    acclist) flags="-O2" ;;
    csenum|csenum2) flags="-O2 -fopenmp" ;;
    *) fail "unknown lister $l" ;;
  esac
  "$CC" $flags -o "$WORK/bin/$l" "how-we-built-it/source/$l.c" > "$WORK/cc.log" 2>&1 || { cat "$WORK/cc.log"; fail "$l.c does not compile (csenum2 needs OpenMP)"; }
done
for f in verify-it-yourself/checklist.c verify-it-yourself/check_list.py how-we-built-it/source/mitm.c; do
  say "  $(hash_of "$f")  $f"
done
for l in $NEED; do say "  $(hash_of "how-we-built-it/source/$l.c")  how-we-built-it/source/$l.c"; done
say "step 2 build: ok"

# stream_check LABEL Q NU LINES SHA256 COMMAND...: one stream of the list goes to sha256, wc -l, the C checker and
# (for small lists) the Python checker at the same time; nothing is written to disk. SDIR names its scratch folder.
stream_check() {
  sl=$1; sq=$2; snu=$3; slines=$4; ssha=$5; shift 5
  d="$WORK/stream${SDIR:-}"; rm -rf "$d"; mkdir "$d" || return 1
  mkfifo "$d/a" "$d/b" || return 1
  py=0; if [ "$slines" -le "$PYMAX" ]; then py=1; mkfifo "$d/c" || return 1; fi
  $SHA < "$d/a" > "$d/sha" & pa=$!
  wc -l < "$d/b" > "$d/wc" & pb=$!
  if [ $py = 1 ]; then python3 verify-it-yourself/check_list.py "$sq" "$snu" "$d/c" > "$d/py" 2>&1 & pc=$!; fi
  t0=$(date +%s)
  if [ $py = 1 ]; then
    { "$@" < /dev/null 2> "$d/err"; echo $? > "$d/rc"; } | tee "$d/a" "$d/b" "$d/c" | "$WORK/bin/checklist" "$sq" "$snu" > "$d/chk" 2>&1
  else
    { "$@" < /dev/null 2> "$d/err"; echo $? > "$d/rc"; } | tee "$d/a" "$d/b" | "$WORK/bin/checklist" "$sq" "$snu" > "$d/chk" 2>&1
  fi
  crc=$?
  wait $pa; wait $pb; prc=0
  if [ $py = 1 ]; then wait $pc; prc=$?; fi
  t1=$(date +%s)
  grc=$(cat "$d/rc" 2>/dev/null || echo missing)
  gsha=$(awk '{print $1}' "$d/sha"); gwc=$(tr -d ' ' < "$d/wc")
  gchk=$(sed -n 's/^valid solutions: \([0-9][0-9]*\)$/\1/p' "$d/chk"); clast=$(tail -n 1 "$d/chk")
  ok=1; why=""
  [ "$grc" = 0 ] || { ok=0; why="$why; generator exit status $grc"; }
  [ "$gwc" = "$slines" ] || { ok=0; why="$why; wc -l $gwc, expected $slines"; }
  [ "$gsha" = "$ssha" ] || { ok=0; why="$why; sha256 $gsha, expected $ssha"; }
  if [ "$crc" = 0 ] && [ "$clast" = PASS ] && [ "$gchk" = "$slines" ]; then cres="PASS ($gchk valid)"
  else ok=0; cres="FAIL"; why="$why; C checker: $(head -n 1 "$d/chk")"; fi
  pres="not run (more than $PYMAX lines)"
  if [ $py = 1 ]; then
    pv=$(sed -n 's/^valid solutions: \([0-9][0-9]*\)$/\1/p' "$d/py")
    if [ "$prc" = 0 ] && [ "$(tail -n 1 "$d/py")" = PASS ] && [ "$pv" = "$slines" ]; then pres="PASS ($pv valid)"
    else ok=0; pres="FAIL"; why="$why; Python checker: $(head -n 1 "$d/py")"; fi
  fi
  say "  $sl: lines $gwc, sha256 $gsha, C checker $cres, Python checker $pres, $((t1 - t0)) s"
  if [ $ok = 1 ]; then say "  $sl: matches object/counts.txt"; return 0; fi
  say "  $sl: MISMATCH$why"; return 1
}

npass_of() { # LISTER CONTENT Q -> number of memory passes (the output bytes do not depend on it)
  case "$1:$2:$3" in
    csenum:SMnuR:13) echo 4 ;; csenum:SMnuR:14) echo 10 ;; csenum:SMnuR:15) echo 16 ;; csenum:SMnuR:16) echo 26 ;;
    csenum2:SMnuR:17) echo 16 ;; csenum2:SMnuR:18) echo 25 ;; csenum2:SMnuR:19) echo 40 ;;
    *) echo 2 ;;
  esac
}

# 3. lists stored in the package (if any): same checks on the stored bytes
n=0
while read -r c q cnt lines sha listers indep shipped; do
  [ "$shipped" = "-" ] && continue
  nu=0; [ "$c" = SMnuR ] && nu=1
  stream_check "stored list $shipped ($c Q_max $q)" "$q" "$nu" "$lines" "$sha" gzip -dc "$shipped" || fail "stored list $shipped"
  n=$((n + 1))
done < "$WORK/rows.txt"
say "step 3 stored lists: $n checked"

# 4. independent recount (no list): mitm.c counts the solutions with every species sorted (meet in the middle on the
#    split (Q, L, nu) | (u, d, e)), removes common factors by Moebius inversion and the overall sign by Burnside, and
#    prints the count in the published convention (1 + primitive nonzero classes modulo family permutations within
#    each species and overall sign). Every call is independent; JOBS of them run at the same time.
SELROWS=""
for r in $SEL; do
  c=${r%%:*}; q=${r##*:}
  line=$(awk -v c="$c" -v q="$q" '$1 == c && $2 == q' "$WORK/rows.txt")
  [ -n "$line" ] || fail "row $r not found"
  SELROWS="$SELROWS$line
"
done
printf '%s' "$SELROWS" > "$WORK/sel.txt"
cat > "$WORK/cnt1.sh" <<'EOF'
"$1" "$3" "$4" > "$2/M_$3_$4.txt" 2>&1; echo "exit $?" >> "$2/M_$3_$4.txt"
EOF
mitm_of() { # CONTENT Q -> count printed by mitm (empty if it failed)
  grep -q '^exit 0$' "$WORK/M_$1_$2.txt" 2>/dev/null || return 0
  sed -n "s/^RESULT $1 Qmax $2: inequivalent = \([0-9][0-9]*\)\$/\1/p" "$WORK/M_$1_$2.txt"
}
t0=$(date +%s)
{ awk '$1 == "SMnuR" { print "SMnuR", $2 }' "$WORK/sel.txt"; awk '$1 == "SM" { print "SM", $2 }' "$WORK/sel.txt"
  q=1; while [ $q -le 10 ]; do say "SM $q"; say "SMnuR $q"; q=$((q + 1)); done; } | \
  xargs -n 2 -P "$JOBS" sh "$WORK/cnt1.sh" "$WORK/bin/mitm" "$WORK" || fail "the counter failed"
t1=$(date +%s)
for c in SM SMnuR; do
  adm=$ADM_SM; [ $c = SMnuR ] && adm=$ADM_SMNUR
  q=1; bad=""
  for v in $adm; do
    got=$(mitm_of $c $q); [ "$got" = "$v" ] || bad="$bad Q_max $q: $got vs published $v;"
    q=$((q + 1))
  done
  [ -z "$bad" ] || fail "calibration: $c counts differ from Allanach-Davighi-Melville:$bad"
  say "step 4 calibration $c: Q_max 1..10 = $(q=1; while [ $q -le 10 ]; do printf '%s ' "$(mitm_of $c $q)"; q=$((q + 1)); done)= published values: ok"
done
while read -r rc rq rcnt rlines rsha rlisters rindep rshipped; do
  got=$(mitm_of "$rc" "$rq")
  [ "$got" = "$rcnt" ] || fail "recount $rc Q_max $rq: counter gives $got, object/counts.txt says $rcnt"
  say "  recount $rc Q_max $rq: $got = object/counts.txt count: ok"
done < "$WORK/sel.txt"
say "  (mitm counter, 20 calibration values and $(wc -l < "$WORK/sel.txt" | tr -d ' ') rows: $((t1 - t0)) s)"

# 5. regenerate every selected row's list, streamed, and check it. Single-threaded acclist streams run PAR at a
#    time (each in its own scratch folder; their reports are printed in row order); csenum2 streams use THREADS
#    threads and run one at a time.
: > "$WORK/jobs.txt"
while read -r c q cnt lines sha listers indep shipped; do
  use=""
  if [ $BOTH = 1 ]; then use=$(printf '%s' "$listers" | tr ',' ' ')
  else
    eval "pref=\$PREF_$c"
    for l in $pref; do case ",$listers," in *",$l,"*) use=$l; break ;; esac; done
    [ -n "$use" ] || use=${listers%%,*}
  fi
  for l in $use; do say "$c $q $lines $sha $l" >> "$WORK/jobs.txt"; done
done < "$WORK/sel.txt"
run_job() { # CONTENT Q LINES SHA LISTER
  jc=$1; jq=$2; jl=$3; js=$4; jx=$5; jnu=0; [ "$jc" = SMnuR ] && jnu=1
  case "$jx" in
    acclist) set -- "$WORK/bin/acclist" "$jq" "$jnu" ;;
    *) set -- "$WORK/bin/$jx" "$jq" "$jnu" "$(npass_of "$jx" "$jc" "$jq")" "$THREADS" ;;
  esac
  stream_check "$jc Q_max $jq by $jx" "$jq" "$jnu" "$jl" "$js" "$@"
}
n=0
# acclist streams, PAR at a time
awk '$5 == "acclist"' "$WORK/jobs.txt" > "$WORK/jobs_a.txt"
total=$(wc -l < "$WORK/jobs_a.txt" | tr -d ' ')
i=0
while [ $i -lt "$total" ]; do
  pids=""; k=0
  while [ $k -lt "$PAR" ] && [ $i -lt "$total" ]; do
    i=$((i + 1)); k=$((k + 1))
    set -- $(sed -n "${i}p" "$WORK/jobs_a.txt")
    ( SDIR="_$i"; run_job "$@" ) > "$WORK/job_$i.out" 2>&1 &
    pids="$pids $!"
  done
  bad=0; j=$((i - k))
  for p in $pids; do
    j=$((j + 1))
    wait "$p" || bad=1
    cat "$WORK/job_$j.out"
    n=$((n + 1))
  done
  [ $bad = 0 ] || fail "a regenerated list differs from object/counts.txt (see above)"
done
# other listers (multi-threaded), one at a time
awk '$5 != "acclist"' "$WORK/jobs.txt" > "$WORK/jobs_b.txt"
while read -r jc jq jl js jx; do
  run_job "$jc" "$jq" "$jl" "$js" "$jx" || fail "$jc Q_max $jq ($jx)"
  n=$((n + 1))
done < "$WORK/jobs_b.txt"
say "step 5 regenerated lists: $n streams, all equal to object/counts.txt"

say "rows checked: $(printf '%s' "$SEL" | wc -w | tr -d ' ') of $(printf '%s' "$PKG_ROWS" | wc -w | tr -d ' ') ($MODE)"
say PASS
exit 0
