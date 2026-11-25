#!/usr/bin/env bash
# Rule 10: peak RSS sample, total workers < half MemAvailable, cap 22.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CAP="${WORKER_CAP:-22}"
SAMPLE_PAIR="${SAMPLE_PAIR:-A-B}"
TABLE="${TABLE:-unrestricted}"

avail_kb=$(awk '/MemAvailable/{print $2}' /proc/meminfo)
half_kb=$((avail_kb / 2))

# measure one short job
tmp="$ROOT/work/_peak_sample"
rm -rf "$tmp"
mkdir -p "$tmp"
echo "[\"$SAMPLE_PAIR\"]" > "$tmp/pairs.json"
set +e
out=$(nice -n 19 python3 "$ROOT/scripts/measure_peak.py" \
  python3 -m py.worker --pairs "$tmp/pairs.json" --table "$TABLE" \
  --k-min 2 --k-max 2 --timeout 60 --out "$tmp/out.jsonl" --work "$tmp/w" 2>&1)
rc=$?
set -e
peak=$(echo "$out" | awk '/PEAK_RSS_KB/{print $2}' | tail -1)
if [[ -z "${peak:-}" || "$peak" -lt 1 ]]; then
  peak=500000  # 500 MB fallback
fi
# per-worker budget: peak * 1.3 headroom
budget=$((peak * 13 / 10))
n=$((half_kb / budget))
if [[ "$n" -lt 1 ]]; then n=1; fi
if [[ "$n" -gt "$CAP" ]]; then n=$CAP; fi
# also never exceed nproc-ish
cpus=$(nproc)
if [[ "$n" -gt $((cpus - 2)) ]]; then n=$((cpus - 2)); fi
if [[ "$n" -lt 1 ]]; then n=1; fi
echo "PEAK_RSS_KB $peak"
echo "MEM_AVAILABLE_KB $avail_kb"
echo "WORKERS $n"
