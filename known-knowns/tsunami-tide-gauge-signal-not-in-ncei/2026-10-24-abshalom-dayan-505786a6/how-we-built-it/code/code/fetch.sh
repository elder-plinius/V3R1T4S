#!/bin/sh
# One honest GET, logged: fetch.sh <url> <outfile>. Never retried. Appends url, UTC time, HTTP code, sha256, bytes to data/fetch_log.tsv.
D="$(cd "$(dirname "$0")/.." && pwd)/data"
t=$(date -u +%Y-%m-%dT%H:%M:%SZ)
code=$(curl -g -s -m 300 -A 'V3R1T4S-research (honest client)' -o "$2" -w '%{http_code}' "$1")
h=$(shasum -a 256 "$2" 2>/dev/null | cut -d' ' -f1); b=$(wc -c < "$2" 2>/dev/null | tr -d ' ')
printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$1" "$t" "$code" "$h" "$b" "$2" >> "$D/fetch_log.tsv"
printf '%s %s %s %s %s\n' "$code" "$t" "$h" "$b" "$2"
