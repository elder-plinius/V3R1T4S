#!/bin/bash
# Exhaustive max-cycle for Rule 30 / 110 at a given width (default 37).
# Designed for a high-RAM machine (n=37 needs ~16 GB for impl1 bitset, ~32 GB for impl2 colours).
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
"$ROOT/build.sh"

RULE=${RULE:-30}          # 30 or 110
N=${N:-37}
IMPL=${IMPL:-1}           # 1 (bitset+rotation) or 2 (3-colour, no rotation)
WORKERS=${WORKERS:-1}     # reserved; current builds are single-threaded
WORKDIR=${WORKDIR:-$ROOT/work/run_r${RULE}_n${N}}
mkdir -p "$WORKDIR"
WIT="$WORKDIR/witness_impl${IMPL}.txt"
LOG="$WORKDIR/run_impl${IMPL}.log"

# Memory gate
if [ "$IMPL" = 2 ]; then NEED=$(( (1<<N) / 4 )); else NEED=$(( (1<<N) / 8 )); fi
AVAIL=$(awk '/MemAvailable/{print $2*1024}' /proc/meminfo)
echo "need_bytes=$NEED avail_bytes=$AVAIL workers=$WORKERS" | tee -a "$LOG"
if [ "$NEED" -gt "$AVAIL" ]; then
  echo "ERROR: need $NEED bytes but only $AVAIL available" | tee -a "$LOG"
  exit 1
fi

echo "Starting IMPL=$IMPL RULE=$RULE N=$N at $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG"
nice -n 19 "$ROOT/impl$IMPL/maxcycle" --rule "$RULE" --n "$N" --witness-out "$WIT" \
  2>>"$LOG" | tee -a "$WORKDIR/result_impl${IMPL}.txt"
echo "Finished at $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG"
echo "Witness -> $WIT"
