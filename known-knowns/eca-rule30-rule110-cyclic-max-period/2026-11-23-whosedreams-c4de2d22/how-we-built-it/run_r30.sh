#!/bin/bash
# Rule 30, cyclic width 37: A334497(37). One script, safe to re-run: finished stages are skipped.
#
#   ./run_r30.sh                 self-test, held-out check, n=37 impl1 then impl2, witness check, send-back
#   P1=1 ./run_r30.sh            also the OPTIONAL partial win p1 (A334497(31..36), both programs) after the main run
#   SMOKE=1 ./run_r30.sh         quick test of the whole pipeline at widths <= 20 (minutes, little memory)
#
# Everything goes to work/ (or work-smoke/ for SMOKE=1). Progress: ./status.sh
set -uo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
cd "$ROOT"
export TZ=America/Toronto
SMOKE=${SMOKE:-0}
P1=${P1:-0}
WIN_DL=${WIN_DL:-}   # optional: also copy the send-back archive to this folder (e.g. a Windows Downloads folder under WSL)
if [ "$SMOKE" = 1 ]; then
  WORK=${WORK:-$ROOT/work-smoke}; MAIN_N=20; ST_R30=20; ST_R110=20; REP_LO=0; REP_HI=-1; HELD_N=20; P1_LO=17; P1_HI=19
else
  WORK=${WORK:-$ROOT/work}; MAIN_N=37; ST_R30=24; ST_R110=30; REP_LO=25; REP_HI=30; HELD_N=31; P1_LO=31; P1_HI=36
fi
mkdir -p "$WORK"
if [ -f "$WORK/run.pid" ] && kill -0 "$(cat "$WORK/run.pid")" 2>/dev/null; then
  echo "run_r30.sh is already running (pid $(cat "$WORK/run.pid")). Use ./status.sh to watch it."; exit 0
fi
echo $$ > "$WORK/run.pid"
trap 'rm -f "$WORK/run.pid"' EXIT
LOG="$WORK/run.log"
STATUS="$WORK/STATUS.txt"
ts() { echo "$(date '+%Y-%m-%d %H:%M:%S ET') ($(date -u +%Y-%m-%dT%H:%M:%SZ))"; }
say() { echo "[$(ts)] $*" | tee -a "$LOG"; }
setstatus() { echo "[$(ts)] $*" > "$STATUS"; }

make_sendback() {   # $1 = OK, PARTIAL (stopped) or PROGRESS (quiet safety copy mid-run)
  local stamp out base
  stamp=$(date +%Y%m%d-%H%M)
  if [ "$1" = PROGRESS ]; then
    (cd "$ROOT" && sha256sum impl1/maxcycle.c impl2/maxcycle.c check_period.py run_r30.sh build.sh data/* 2>/dev/null) > "$WORK/kit_sha256.txt"
    tar -C "$(dirname "$WORK")" -czf "$HOME/send_back_r30_progress.tar.gz" --exclude='*.pid' "$(basename "$WORK")"
    say "safety copy updated: $HOME/send_back_r30_progress.tar.gz"
    return 0
  fi
  rm -f "$HOME/send_back_r30_progress.tar.gz"
  base="send_back_r30_${stamp}"
  [ "$SMOKE" = 1 ] && base="send_back_r30_SMOKE_${stamp}"
  [ "$1" = PARTIAL ] && base="${base}_PARTIAL"
  out="$HOME/${base}.tar.gz"
  (cd "$ROOT" && sha256sum impl1/maxcycle.c impl2/maxcycle.c impl1/maxcycle impl2/maxcycle check_period.py run_r30.sh build.sh data/* 2>/dev/null) > "$WORK/kit_sha256.txt"
  tar -C "$(dirname "$WORK")" -czf "$out" --exclude='*.pid' "$(basename "$WORK")"
  sha256sum "$out" | tee "$out.sha256" >> "$LOG"
  if [ -d "$WIN_DL" ]; then cp "$out" "$out.sha256" "$WIN_DL/" && say "copied to Windows Downloads: $WIN_DL/$(basename "$out")"; fi
  say "SEND-BACK FILE: $out"
  echo
  echo "=================================================================="
  echo " Send-back file: $out"
  [ -d "$WIN_DL" ] && echo " Also in Windows: Downloads\\$(basename "$out")"
  echo " sha256: $(cut -d' ' -f1 "$out.sha256")"
  echo "=================================================================="
}

fail() { say "STOPPED: $*"; setstatus "STOPPED: $*"; make_sendback PARTIAL; exit 1; }

oeis() { awk -v n="$2" '$1==n{print $2}' "$ROOT/data/$1"; }

# run one program; $1 impl, $2 rule, $3 n, $4 outdir. Writes result/witness/err/hwm files. Echoes max_period.
runone() {
  local impl=$1 rule=$2 n=$3 dir=$4 need head avail pid hwm line start
  mkdir -p "$dir"
  if [ "$impl" = 1 ]; then need=$(( (1<<n)/8 )); else need=$(( (1<<n)/4 )); fi
  head=$(( need/8 + (64<<20) ))   # room for the path stack: 2 GiB extra for impl1 at n=37, 4 GiB for impl2
  avail=$(awk '/MemAvailable/{print $2*1024}' /proc/meminfo)
  if [ $((need+head)) -gt "$avail" ]; then
    echo "impl$impl rule $rule n=$n needs about $(( (need+head)>>30 )) GiB free, only $(( avail>>30 )) GiB available. Close other programs and run ./run_r30.sh again." > "$WORK/.lastfail"
    return 1
  fi
  local tag="r${rule}_n${n}_impl${impl}"
  start=$(date +%s)
  nice -n 19 "$ROOT/impl$impl/maxcycle" --rule "$rule" --n "$n" --witness-out "$dir/witness_impl${impl}.txt" \
     > "$dir/result_impl${impl}.txt.tmp" 2> "$dir/err_impl${impl}.txt" &
  pid=$!
  echo "$pid" > "$dir/impl${impl}.pid"
  hwm=0; polls=0
  while kill -0 "$pid" 2>/dev/null; do
    h=$(awk '/VmHWM/{print $2}' /proc/$pid/status 2>/dev/null); [ -n "${h:-}" ] && hwm=$h
    echo "$hwm" > "$dir/peak_rss_kB_impl${impl}.txt"
    [ "$n" -ge 30 ] && setstatus "running $tag, pid $pid, elapsed $(( ($(date +%s)-start)/60 )) min, peak memory $((hwm/1024)) MiB"
    polls=$((polls+1)); if [ $polls -lt 40 ]; then sleep 0.05; else sleep 5; fi
  done
  wait "$pid"; local rc=$?
  rm -f "$dir/impl${impl}.pid"
  if [ $rc -ne 0 ]; then echo "$tag exited with code $rc (see $dir/err_impl${impl}.txt; code 137 usually means out of memory)" > "$WORK/.lastfail"; return 1; fi
  mv "$dir/result_impl${impl}.txt.tmp" "$dir/result_impl${impl}.txt"
  line=$(cat "$dir/result_impl${impl}.txt")
  echo "$line wall_sec=$(( $(date +%s)-start )) peak_rss_kB=$hwm" >> "$WORK/all_results.txt"
  echo "$line" | sed -n 's/.*max_period=\([0-9]*\).*/\1/p'
}

stage_done() { [ -f "$WORK/.done_$1" ]; }
mark_done() { touch "$WORK/.done_$1"; say "stage $1 done"; }

# ---------------- stage 0: environment, integrity, build ----------------
say "=== run_r30.sh start (SMOKE=$SMOKE P1=$P1) in $ROOT ==="
command -v cc >/dev/null || fail "no C compiler. Run: sudo apt update && sudo apt install -y build-essential"
command -v python3 >/dev/null || fail "no python3. Run: sudo apt update && sudo apt install -y python3"
if [ -f MANIFEST.sha256 ]; then
  sha256sum -c --quiet MANIFEST.sha256 >> "$LOG" 2>&1 || fail "kit files do not match MANIFEST.sha256 (damaged copy?)"
fi
{ echo "date: $(ts)"; uname -a; cat /proc/version; grep -m1 'model name' /proc/cpuinfo; echo "nproc: $(nproc)";
  free -b; cc --version | head -1; python3 --version; echo "SMOKE=$SMOKE P1=$P1"; } > "$WORK/sysinfo.txt" 2>&1
"$ROOT/build.sh" >> "$LOG" 2>&1 || fail "build failed (see $LOG)"
say "built programs"

# ---------------- stage 1: self-test ----------------
if ! stage_done selftest; then
  setstatus "self-test running"
  D="$WORK/selftest"; mkdir -p "$D"; : > "$D/selftest.log"
  for impl in 1 2; do
    for n in $(seq 1 "$ST_R30"); do
      got=$(runone $impl 30 $n "$D/r30_n$n") || fail "$(cat "$WORK/.lastfail")"; exp=$(oeis b334497.txt $n)
      if [ "$got" = "$exp" ]; then r=OK; elif [ "$got" -lt "$exp" ]; then r=BUG; else r=MISMATCH; fi
      echo "$r impl$impl rule30 n=$n got=$got oeis=$exp" | tee -a "$D/selftest.log"
    done
    for n in $(seq 1 "$ST_R110"); do
      got=$(runone $impl 110 $n "$D/r110_n$n") || fail "$(cat "$WORK/.lastfail")"; exp=$(oeis b204371.txt $n)
      if [ "$got" = "$exp" ]; then r=OK; elif [ "$got" -lt "$exp" ]; then r=BUG; else r=MISMATCH; fi
      echo "$r impl$impl rule110 n=$n got=$got oeis=$exp" | tee -a "$D/selftest.log"
    done
    for n in $(seq "$REP_LO" "$REP_HI"); do
      got=$(runone $impl 30 $n "$D/r30_n$n") || fail "$(cat "$WORK/.lastfail")"; exp=$(oeis b334497.txt $n)
      if [ "$got" = "$exp" ]; then r=REPORT_MATCHES_LISTED; elif [ "$got" -lt "$exp" ]; then r=BUG; else r=REPORT_ABOVE_LISTED; fi
      echo "$r impl$impl rule30 n=$n got=$got oeis=$exp" | tee -a "$D/selftest.log"
    done
  done
  cat "$D/selftest.log" >> "$LOG"
  if grep -qE '^(BUG|MISMATCH)' "$D/selftest.log"; then fail "self-test found BUG/MISMATCH lines (see $D/selftest.log). Do not start the big run."; fi
  say "SELFTEST: PASS ($(grep -c '^OK' "$D/selftest.log") OK lines)"
  mark_done selftest
fi

# ---------------- stage 2: held-out width ----------------
if ! stage_done heldout; then
  setstatus "held-out check running"
  D="$WORK/heldout"; mkdir -p "$D"; : > "$D/heldout.log"
  for impl in 1 2; do
    got=$(runone $impl 110 $HELD_N "$D/r110_n$HELD_N") || fail "$(cat "$WORK/.lastfail")"; exp=$(oeis b204371.txt $HELD_N)
    [ "$got" = "$exp" ] && r=OK || r=FAIL
    echo "$r impl$impl rule110 n=$HELD_N got=$got oeis=$exp" | tee -a "$D/heldout.log"
    got=$(runone $impl 30 $HELD_N "$D/r30_n$HELD_N") || fail "$(cat "$WORK/.lastfail")"; exp=$(oeis b334497.txt $HELD_N)
    if [ "$got" = "$exp" ]; then r=REPORT_MATCHES_LISTED; elif [ "$got" -lt "$exp" ]; then r=BUG; else r=REPORT_ABOVE_LISTED; fi
    echo "$r impl$impl rule30 n=$HELD_N got=$got oeis=$exp" | tee -a "$D/heldout.log"
  done
  cat "$D/heldout.log" >> "$LOG"
  grep -qE '^(FAIL|BUG)' "$D/heldout.log" && fail "held-out check failed (see $D/heldout.log)"
  mark_done heldout
fi

# ---------------- stage 3 and 4: main run, impl1 then impl2 (never together) ----------------
D="$WORK/main_r30_n$MAIN_N"
for impl in 1 2; do
  if ! stage_done main_impl$impl; then
    setstatus "main run impl$impl rule 30 n=$MAIN_N starting"
    say "main run impl$impl rule 30 n=$MAIN_N starting"
    got=$(runone $impl 30 $MAIN_N "$D") || fail "$(cat "$WORK/.lastfail")"
    say "main run impl$impl result: $(cat "$D/result_impl$impl.txt")"
    mark_done main_impl$impl
    make_sendback PROGRESS  # a copy after each big program, in case the PC restarts later
  fi
done

# ---------------- stage 5: compare, floor, independent witness check ----------------
if ! stage_done check; then
  setstatus "checking witnesses"
  p1v=$(sed -n 's/.*max_period=\([0-9]*\).*/\1/p' "$D/result_impl1.txt")
  p2v=$(sed -n 's/.*max_period=\([0-9]*\).*/\1/p' "$D/result_impl2.txt")
  floor=$(oeis a334496_data.txt $MAIN_N)
  {
    echo "impl1: $(cat "$D/result_impl1.txt")"
    echo "impl2: $(cat "$D/result_impl2.txt")"
    [ "$p1v" = "$p2v" ] && echo "AGREE max_period=$p1v" || echo "DISAGREE impl1=$p1v impl2=$p2v"
    if [ -n "$floor" ]; then [ "$p1v" -ge "$floor" ] && echo "FLOOR_OK A334496($MAIN_N)=$floor" || echo "FLOOR_BUG A334496($MAIN_N)=$floor"; fi
    listed=$(oeis b334497.txt $MAIN_N); [ -n "$listed" ] && echo "note: b-file in kit lists n=$MAIN_N as $listed"
  } | tee "$D/compare.txt" | tee -a "$LOG"
  for impl in 1 2; do
    python3 "$ROOT/check_period.py" --file "$D/witness_impl$impl.txt" > "$D/check_period_impl$impl.txt" 2>&1
    say "witness check impl$impl: $(tail -1 "$D/check_period_impl$impl.txt")"
  done
  for f in "$WORK"/heldout/r110_n$HELD_N/witness_impl1.txt; do
    python3 "$ROOT/check_period.py" --file "$f" > "$WORK/heldout/check_period_r110.txt" 2>&1
  done
  if grep -q DISAGREE "$D/compare.txt" || grep -q FLOOR_BUG "$D/compare.txt" \
     || ! tail -1 "$D/check_period_impl1.txt" | grep -qx PASS || ! tail -1 "$D/check_period_impl2.txt" | grep -qx PASS; then
    fail "checks did not all pass (see $D/compare.txt and check_period_impl*.txt)"
  fi
  say "MAIN RESULT: rule 30 n=$MAIN_N max_period=$p1v (both programs agree, witnesses verified)"
  mark_done check
fi

# ---------------- stage 6 (optional): partial win p1 ----------------
if [ "$P1" = 1 ] && ! stage_done p1; then
  setstatus "optional p1 running"
  P="$WORK/p1"; mkdir -p "$P"; : > "$P/p1.log"
  for n in $(seq "$P1_LO" "$P1_HI"); do
    for impl in 1 2; do
      got=$(runone $impl 30 $n "$P/r30_n$n") || fail "$(cat "$WORK/.lastfail")"; exp=$(oeis b334497.txt $n)
      if [ "$got" = "$exp" ]; then r=MATCHES_LISTED; elif [ "$got" -lt "$exp" ]; then r=BUG; else r=ABOVE_LISTED; fi
      echo "$r impl$impl rule30 n=$n got=$got oeis=$exp" | tee -a "$P/p1.log"
    done
    if grep -q "^ABOVE_LISTED impl[12] rule30 n=$n " "$P/p1.log"; then
      for impl in 1 2; do
        python3 "$ROOT/check_period.py" --file "$P/r30_n$n/witness_impl$impl.txt" > "$P/r30_n$n/check_period_impl$impl.txt" 2>&1
        echo "witness check n=$n impl$impl: $(tail -1 "$P/r30_n$n/check_period_impl$impl.txt")" | tee -a "$P/p1.log"
      done
    fi
  done
  cat "$P/p1.log" >> "$LOG"
  grep -q '^BUG' "$P/p1.log" && fail "p1 found a value below a listed term (bug)"
  mark_done p1
fi

setstatus "ALL DONE. Attach the send-back file in chat."
say "=== all stages done ==="
make_sendback OK
