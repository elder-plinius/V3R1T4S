#!/bin/bash
# Honest fetcher: one GET per file from raw.githubusercontent.com, V3R1T4S User-Agent, timeout, 200 MB cap,
# no retries; stops the whole list on 401/403/429/503. Logs UTC time, HTTP code, bytes, path.
# usage: fetch_list.sh <list.tsv (path \t size \t sha)> <dest dir> <log file> <sleep seconds> [ref]
LIST=$1; DEST=$2; LOG=$3; SLP=$4; REF=${5:-main}
UA="V3R1T4S-research-agent/1.0 (honest single request; open research notebook)"
while IFS=$'\t' read -r path size sha; do
  out="$DEST/$path"; mkdir -p "$(dirname "$out")"
  if [ -s "$out" ]; then continue; fi
  code=$(curl -sS -A "$UA" --max-time 300 --max-filesize 200000000 -o "$out.part" -w '%{http_code}' "https://raw.githubusercontent.com/HopkinsIDD/rsv-forecast-hub/$REF/$path")
  got=$(wc -c < "$out.part" 2>/dev/null || echo 0)
  echo -e "$(date -u +%Y-%m-%dT%H:%M:%SZ)\t$code\t$got\t$size\t$path" >> "$LOG"
  if [ "$code" = "200" ]; then mv "$out.part" "$out"; else rm -f "$out.part"; fi
  case "$code" in 401|403|429|503) echo "STOP on $code at $path" >> "$LOG"; exit 1;; esac
  sleep "$SLP"
done < "$LIST"
echo "DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
