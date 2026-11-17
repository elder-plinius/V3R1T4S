#!/bin/bash
# Run LIRICAL 2.4.1 (benchmark --phenotype-only, cleaned data dir) over a case list in fixed-size chunks, one JVM at a
# time, resumable: a chunk whose <chunk>.log.summary already holds rc=0 is skipped. No chunk starts after CAP_EPOCH.
# usage: run_lirical_chunks.sh <caselist> <chunk_size> <outdir> <datadir> <phenopacket_dir> <pids.md> <cap_epoch_utc>
set -u
LIST="$1"; N="$2"; OUT="$3"; DD="$4"; PD="$5"; PIDS="$6"; CAP="$7"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$OUT/chunks"
echo "driver bash-pid $$ start $(date -u +%FT%TZ) list=$(basename "$LIST") chunk=$N cap_epoch=$CAP" >> "$PIDS"
split -l "$N" -d -a 3 "$LIST" "$OUT/chunks/c"
for f in $(ls "$OUT/chunks/" | sort); do
  base="$OUT/$f"
  if [ -f "$base.log.summary" ] && grep -q 'rc=0 ' "$base.log.summary"; then continue; fi
  if [ "$(date -u +%s)" -ge "$CAP" ]; then echo "CAP reached before $f at $(date -u +%FT%TZ)" | tee -a "$OUT/driver.log"; break; fi
  rm -f "$base.csv.gz"
  bash "$HERE/run_lirical_chunk.sh" "$DD" "$OUT/chunks/$f" "$PD" "$base.csv.gz" "$base.log" 4 "$PIDS" | tee -a "$OUT/driver.log"
done
echo "driver done $(date -u +%FT%TZ)" | tee -a "$OUT/driver.log"
