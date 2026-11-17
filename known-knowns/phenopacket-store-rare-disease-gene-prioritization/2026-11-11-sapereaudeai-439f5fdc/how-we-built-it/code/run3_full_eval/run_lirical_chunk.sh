#!/bin/bash
# Run LIRICAL 2.4.1 benchmark (phenotype-only) on a list of phenopackets with one data dir; poll peak working set.
# (run 2's run_lirical_group.sh with the pids file as an argument.)
# usage: run_lirical_chunk.sh <datadir> <caselist> <phenopacket_dir> <out.csv.gz> <log> <threads> <pids.md>
J="${JAVA:-java}"   # Temurin JRE 21.0.13+9 was used (PACKAGE EDIT, see code/README.md)
LJ="${LIRICAL_JAR:-lirical-cli-2.4.1.jar}"   # PACKAGE EDIT
DD="$1"; LIST="$2"; PD="$3"; OUT="$4"; LOG="$5"; T="${6:-4}"; PIDS="$7"
mapfile -t P < <(sed "s#^#$PD/#; s#\$#.json#" "$LIST" | tr -d '\r' | grep -v '^$')
s=$(date +%s)
"$J" -Xmx1g -XX:ActiveProcessorCount=4 -jar "$LJ" benchmark --phenotype-only --parallelism "$T" -d "$DD" -o "$OUT" "${P[@]}" > "$LOG" 2>&1 &
jp=$!
wp=$(cat /proc/$jp/winpid 2>/dev/null)
echo "jvm bash-pid $jp winpid $wp start $(date -u +%FT%TZ) $DD $(basename $LIST)" >> "$PIDS"
peak=0
while kill -0 $jp 2>/dev/null; do
  ws=$(tasklist //FI "PID eq $wp" //FO CSV //NH 2>/dev/null | awk -F'","' '{print $5}' | tr -dc '0-9')
  [ -n "$ws" ] && [ "$ws" -gt "$peak" ] && peak=$ws
  sleep 2
done
wait $jp; rc=$?
e=$(date +%s)
echo "rc=$rc elapsed_s=$((e-s)) n_cases=${#P[@]} peak_ws_kb=$peak end=$(date -u +%FT%TZ)" | tee -a "$LOG.summary"
