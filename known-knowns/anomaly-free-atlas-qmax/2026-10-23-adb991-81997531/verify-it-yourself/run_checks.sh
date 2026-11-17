#!/bin/sh
# Check this package's census rows. Run from the package folder:
#   sh verify-it-yourself/run_checks.sh              the default rows (DEFAULT_ROWS below)
#   sh verify-it-yourself/run_checks.sh --all        every row of object/counts.txt
#   sh verify-it-yourself/run_checks.sh --rows "SMnuR:12 SM:20"    chosen rows
#   add --both to run every lister object/counts.txt records for a row (default: one lister per row)
# Needs: a C compiler with OpenMP (gcc), python3 (standard library), sha256sum or shasum, and POSIX tools
# (tee, mkfifo, wc, awk, sed, xargs, gzip). Environment: THREADS (lister threads, default 3), JOBS (parallel
# counter processes, default 3), PYMAX (largest list also read by the Python checker, default 2000000 lines),
# KEEP=1 keeps the scratch folder. Nothing large is written to disk: each list is streamed once.
# What it does, in order (it stops at the first problem):
#   1. verify-it-yourself/rows.py reads object/counts.txt: exactly the claimed rows, count = lines + 1, valid hashes.
#   2. compiles the claim's sources (how-we-built-it/source/) and the C checker (verify-it-yourself/checklist.c).
#   3. stored lists in object/ (if any): sha256, line count, C checker and Python checker on the stored bytes.
#   4. recounts without listing (count.c + conventions.py): first reproduces the twenty published
#      Allanach-Davighi-Melville values (Q_max 1..10, both contents), then each selected row's count.
#   5. regenerates each selected row's list with its lister and streams the same bytes into sha256, wc -l and the
#      C checker (and the Python checker for small lists); all must equal object/counts.txt.
# Last line of output: PASS or FAIL (exit status 0 or 1).
TARGET="anomaly-free-atlas-qmax: SMnuR Q_max 12..16 and SM Q_max 12..31"
PKG_ROWS="SMnuR:12 SMnuR:13 SMnuR:14 SMnuR:15 SMnuR:16 SM:12 SM:13 SM:14 SM:15 SM:16 SM:17 SM:18 SM:19 SM:20 SM:21 SM:22 SM:23 SM:24 SM:25 SM:26 SM:27 SM:28 SM:29 SM:30 SM:31"
# default: a subset that runs in about 8 minutes on 3 cores (SMnuR 12, 13 and SM 12..20); --all adds SMnuR 14..16
# and SM 21..31 (about 2 to 3 hours on 3 cores)
DEFAULT_ROWS="SMnuR:12 SMnuR:13 SM:12 SM:13 SM:14 SM:15 SM:16 SM:17 SM:18 SM:19 SM:20"
PREF_SM="acclist csenum"; PREF_SMnuR="csenum acclist"


# ---------------------------------------------------------------------------------------------------------------
# Everything below is the same in the three census packages of this target; only the settings above differ.
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
    --rows) shift; [ $# -gt 0 ] || fail "--rows needs a value such as \"SM:12 SMnuR:13\""; SEL="$1"; MODE=chosen ;;
    --both) BOTH=1 ;;
    -h|--help) sed -n '2,40p' "$0"; exit 0 ;;
    *) fail "unknown option $1 (use --all, --rows \"CONTENT:QMAX ...\", --both)" ;;
  esac
  shift
done
for r in $SEL; do
  case " $PKG_ROWS " in *" $r "*) ;; *) fail "row $r is not part of this claim (rows: $PKG_ROWS)" ;; esac
done

THREADS=${THREADS:-3}; JOBS=${JOBS:-3}; PYMAX=${PYMAX:-2000000}; CC=${CC:-gcc}
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
say "threads per lister: $THREADS, parallel counter jobs: $JOBS, Python checker on lists up to $PYMAX lines"

# 1. the object file is internally consistent and holds exactly the claimed rows
python3 verify-it-yourself/rows.py object/counts.txt $PKG_ROWS > "$WORK/rows.txt" || { cat "$WORK/rows.txt"; fail "object/counts.txt"; }
say "step 1 counts file: $(wc -l < "$WORK/rows.txt" | tr -d ' ') rows, count = lines + 1 in every row: ok"

# 2. build (sources as shipped; sha256 printed so a reader can match them with SHA256SUMS)
mkdir "$WORK/src" "$WORK/bin" || fail "scratch folder"
cp how-we-built-it/source/count.c how-we-built-it/source/fix.py how-we-built-it/source/conventions.py "$WORK/src/" \
  || fail "missing source files in how-we-built-it/source/"
NEED=$(awk '{print $6}' "$WORK/rows.txt" | tr ',' '\n' | sort -u)
"$CC" -O2 -o "$WORK/bin/checklist" verify-it-yourself/checklist.c > "$WORK/cc.log" 2>&1 || { cat "$WORK/cc.log"; fail "checklist.c does not compile"; }
"$CC" -O2 -o "$WORK/bin/count" how-we-built-it/source/count.c > "$WORK/cc.log" 2>&1 || { cat "$WORK/cc.log"; fail "count.c does not compile"; }
for l in $NEED; do
  case "$l" in
    acclist) flags="-O2" ;;
    csenum|csenum2) flags="-O2 -fopenmp" ;;
    *) fail "unknown lister $l" ;;
  esac
  "$CC" $flags -o "$WORK/bin/$l" "how-we-built-it/source/$l.c" > "$WORK/cc.log" 2>&1 || { cat "$WORK/cc.log"; fail "$l.c does not compile (csenum needs OpenMP)"; }
done
for f in verify-it-yourself/checklist.c verify-it-yourself/check_list.py how-we-built-it/source/count.c \
         how-we-built-it/source/fix.py how-we-built-it/source/conventions.py; do
  say "  $(hash_of "$f")  $f"
done
for l in $NEED; do say "  $(hash_of "how-we-built-it/source/$l.c")  how-we-built-it/source/$l.c"; done
say "step 2 build: ok"

# stream_check LABEL Q NU LINES SHA256 COMMAND...: one stream of the list goes to sha256, wc -l, the C checker and
# (for small lists) the Python checker at the same time; nothing is written to disk.
stream_check() {
  sl=$1; sq=$2; snu=$3; slines=$4; ssha=$5; shift 5
  d="$WORK/stream"; rm -rf "$d"; mkdir "$d" || return 1
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
    csenum2:SMnuR:17) echo 16 ;; csenum2:SMnuR:18) echo 25 ;;
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

# 4. independent recount (no list): count.c gives the raw number of sorted-triple solutions for every bound,
#    conventions.py turns it into the published convention (1 + primitive nonzero classes modulo family
#    permutations within each species and overall sign; Burnside for the sign, Moebius for common factors).
recount() { # NU QMAX -> writes $WORK/conv_NU.txt
  rnu=$1; rq=$2
  cat > "$WORK/cnt1.sh" <<'EOF'
"$1" "$4" "$2" > "$3/N_$2_$4.txt"
EOF
  awk -v n="$rq" 'BEGIN { for (q = n; q >= 1; q--) print q }' | \
    xargs -n 1 -P "$JOBS" sh "$WORK/cnt1.sh" "$WORK/bin/count" "$rnu" "$WORK" || return 1
  : > "$WORK/N_$rnu.txt"
  q=1
  while [ $q -le "$rq" ]; do
    grep -q "^N $q $rnu [0-9][0-9]*\$" "$WORK/N_${rnu}_$q.txt" || return 1
    cat "$WORK/N_${rnu}_$q.txt" >> "$WORK/N_$rnu.txt"; q=$((q + 1))
  done
  (cd "$WORK/src" && python3 conventions.py "$WORK/N_$rnu.txt" "$rnu") > "$WORK/conv_$rnu.txt" || return 1
}
prim_of() { # NU Q -> count in the published convention
  awk -v q="$2" '$1 == q { if (match($0, /prim_incl0.: [0-9]+/)) { s = substr($0, RSTART, RLENGTH); sub(/.*: /, "", s); print s } }' "$WORK/conv_$1.txt"
}
SELROWS=""
for r in $SEL; do
  c=${r%%:*}; q=${r##*:}
  line=$(awk -v c="$c" -v q="$q" '$1 == c && $2 == q' "$WORK/rows.txt")
  [ -n "$line" ] || fail "row $r not found"
  SELROWS="$SELROWS$line
"
done
printf '%s' "$SELROWS" > "$WORK/sel.txt"
for c in SM SMnuR; do
  nu=0; adm=$ADM_SM; [ $c = SMnuR ] && { nu=1; adm=$ADM_SMNUR; }
  top=$(awk -v c=$c 'BEGIN { m = 10 } $1 == c && $2 > m { m = $2 } END { print m }' "$WORK/sel.txt")
  t0=$(date +%s)
  recount $nu "$top" || fail "the counter failed for $c"
  t1=$(date +%s)
  q=1; bad=""
  for v in $adm; do
    got=$(prim_of $nu $q); [ "$got" = "$v" ] || bad="$bad Q_max $q: $got vs published $v;"
    q=$((q + 1))
  done
  [ -z "$bad" ] || fail "calibration: $c counts differ from Allanach-Davighi-Melville:$bad"
  say "step 4 calibration $c: Q_max 1..10 = $(q=1; while [ $q -le 10 ]; do printf '%s ' "$(prim_of $nu $q)"; q=$((q + 1)); done)= published values: ok"
  while read -r rc rq rcnt rlines rsha rlisters rindep rshipped; do
    [ "$rc" = "$c" ] || continue
    got=$(prim_of $nu "$rq")
    [ "$got" = "$rcnt" ] || fail "recount $c Q_max $rq: counter gives $got, object/counts.txt says $rcnt"
    say "  recount $c Q_max $rq: $got = object/counts.txt count: ok"
  done < "$WORK/sel.txt"
  say "  ($c counter, Q_max 1..$top: $((t1 - t0)) s)"
done

# 5. regenerate every selected row's list, streamed, and check it
n=0
while read -r c q cnt lines sha listers indep shipped; do
  nu=0; [ "$c" = SMnuR ] && nu=1
  use=""
  if [ $BOTH = 1 ]; then use=$(printf '%s' "$listers" | tr ',' ' ')
  else
    eval "pref=\$PREF_$c"
    for l in $pref; do case ",$listers," in *",$l,"*) use=$l; break ;; esac; done
    [ -n "$use" ] || use=${listers%%,*}
  fi
  for l in $use; do
    case "$l" in
      acclist) set -- "$WORK/bin/acclist" "$q" "$nu" ;;
      *) set -- "$WORK/bin/$l" "$q" "$nu" "$(npass_of "$l" "$c" "$q")" "$THREADS" ;;
    esac
    stream_check "$c Q_max $q by $l" "$q" "$nu" "$lines" "$sha" "$@" || fail "$c Q_max $q ($l)"
    n=$((n + 1))
  done
done < "$WORK/sel.txt"
say "step 5 regenerated lists: $n streams, all equal to object/counts.txt"

say "rows checked: $(printf '%s' "$SEL" | wc -w | tr -d ' ') of $(printf '%s' "$PKG_ROWS" | wc -w | tr -d ' ') ($MODE)"
say PASS
exit 0
