#!/bin/bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
OUTDIR=${1:-$ROOT/results}
mkdir -p "$OUTDIR"
parse() { sed -n 's/.*max_period=\([0-9]*\).*/\1/p'; }
expect30() { awk -v n="$1" '$1==n{print $2; exit}' "$ROOT/data/b334497.txt"; }
expect110() { awk -v n="$1" '$1==n{print $2; exit}' "$ROOT/data/b204371.txt"; }

echo "=== A334497 Rule30 reproduce 1..24 + report 25..30 ===" | tee "$OUTDIR/selftest.log"
for n in $(seq 1 30); do
  exp=$(expect30 "$n")
  for impl in 1 2; do
    # skip if memory too high: impl2 needs 2 bits * 2^n; refuse if > 1.2GB
    # nbytes approx
    if [ "$impl" = 2 ]; then need=$(( (1<<n) / 4 )); else need=$(( (1<<n) / 8 )); fi
    avail_kb=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
    half=$(( avail_kb * 1024 / 2 ))
    if [ "$need" -gt "$half" ]; then
      echo "SKIP impl$impl rule=30 n=$n need=$need half_avail=$half" | tee -a "$OUTDIR/selftest.log"
      continue
    fi
    echo -n "impl$impl rule30 n=$n ... " | tee -a "$OUTDIR/selftest.log"
    w="$OUTDIR/wit_r30_n${n}_i${impl}.txt"
    line=$(nice -n 19 "$ROOT/impl$impl/maxcycle" --rule 30 --n "$n" --witness-out "$w" 2>"$OUTDIR/err_r30_n${n}_i${impl}.txt")
    got=$(echo "$line" | parse)
    echo "$line" >> "$OUTDIR/selftest.log"
    if [ -n "$exp" ]; then
      if [ "$got" = "$exp" ]; then
        echo "OK got=$got oeis=$exp" | tee -a "$OUTDIR/selftest.log"
      else
        # For n>=25, OEIS may be non-exhaustive: if we are HIGHER, note correction candidate;
        # if LOWER, BUG
        if [ "$n" -ge 25 ] && [ "$got" -gt "$exp" ]; then
          echo "NOTE got=$got oeis=$exp (exceeds listed; possible correction)" | tee -a "$OUTDIR/selftest.log"
        elif [ "$got" -lt "$exp" ]; then
          echo "BUG got=$got oeis=$exp (below listed => our bug)" | tee -a "$OUTDIR/selftest.log"
        else
          echo "MISMATCH got=$got oeis=$exp" | tee -a "$OUTDIR/selftest.log"
        fi
      fi
    else
      echo "NEW got=$got" | tee -a "$OUTDIR/selftest.log"
    fi
  done
done

echo "=== A204371 Rule110 reproduce 1..30 ===" | tee -a "$OUTDIR/selftest.log"
for n in $(seq 1 30); do
  exp=$(expect110 "$n")
  for impl in 1 2; do
    if [ "$impl" = 2 ]; then need=$(( (1<<n) / 4 )); else need=$(( (1<<n) / 8 )); fi
    avail_kb=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
    half=$(( avail_kb * 1024 / 2 ))
    if [ "$need" -gt "$half" ]; then
      echo "SKIP impl$impl rule=110 n=$n need=$need half_avail=$half" | tee -a "$OUTDIR/selftest.log"
      continue
    fi
    echo -n "impl$impl rule110 n=$n ... " | tee -a "$OUTDIR/selftest.log"
    w="$OUTDIR/wit_r110_n${n}_i${impl}.txt"
    line=$(nice -n 19 "$ROOT/impl$impl/maxcycle" --rule 110 --n "$n" --witness-out "$w" 2>"$OUTDIR/err_r110_n${n}_i${impl}.txt")
    got=$(echo "$line" | parse)
    echo "$line" >> "$OUTDIR/selftest.log"
    if [ "$got" = "$exp" ]; then
      echo "OK got=$got oeis=$exp" | tee -a "$OUTDIR/selftest.log"
    elif [ "$got" -lt "$exp" ]; then
      echo "BUG got=$got oeis=$exp" | tee -a "$OUTDIR/selftest.log"
    else
      echo "NOTE/MISMATCH got=$got oeis=$exp" | tee -a "$OUTDIR/selftest.log"
    fi
  done
done
echo DONE | tee -a "$OUTDIR/selftest.log"
