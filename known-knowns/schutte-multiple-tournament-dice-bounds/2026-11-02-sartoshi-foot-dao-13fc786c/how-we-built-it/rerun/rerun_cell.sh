#!/bin/sh
# Re-run every job of one cell, 3 at a time at nice 19, appending to threads/schutte/rerun/<cell>/results.tsv.
# Resumable: jobs already in results.tsv are skipped. To stop: touch threads/schutte/rerun/<cell>/STOP
# (running jobs finish; no new ones start). Usage (from the workspace root): sh threads/schutte/rerun_cell.sh m3k6n12
CELL="$1"; W="$(pwd)"; R="$W/threads/schutte/rerun/$CELL"
mkdir -p "$R/scratch"; touch "$R/results.tsv"
awk -F'\t' -v c="$CELL" 'NR>1 && index($1, c"/")==1 {print $1}' "$W/certify/jobs.tsv" > "$R/all.txt"
awk -F'\t' -v d="$R/results.tsv" 'BEGIN {while ((getline l < d) > 0) {split(l, a, "\t"); done[a[1]]=1}} !($1 in done)' "$R/all.txt" > "$R/todo.txt"
echo "start $(date -u +%FT%TZ) todo $(wc -l < "$R/todo.txt" | tr -d ' ') of $(wc -l < "$R/all.txt" | tr -d ' ')"
export R W
xargs -P 3 -n 1 sh -c '[ -e "$R/STOP" ] && exit 0; nice -n 19 sh "$W/threads/schutte/rerun_one.sh" "$1" "$R/scratch" >> "$R/results.tsv"' _ < "$R/todo.txt"
echo "end $(date -u +%FT%TZ) results $(wc -l < "$R/results.tsv" | tr -d ' ') pass $(awk -F'\t' '$2=="PASS"' "$R/results.tsv" | wc -l | tr -d ' ')"
