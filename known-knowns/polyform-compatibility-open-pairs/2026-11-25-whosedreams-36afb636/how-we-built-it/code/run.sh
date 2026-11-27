#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"

MODE=full
for a in "$@"; do
  case "$a" in
    --smoke) MODE=smoke ;;
    --estimate) MODE=estimate ;;
  esac
done

TABLE="${TABLE:-unrestricted}"
KMIN="${KMIN:-2}"
KMAX="${KMAX:-8}"
TIMEOUT="${TIMEOUT:-180}"
WORKDIR="${WORKDIR:-work/run_${TABLE}}"
mkdir -p "$WORKDIR"

# Build pair list
python3 - <<PY
import json
from pathlib import Path
t=json.loads(Path("data/tables.json").read_text())
table="$TABLE"
opens=t[table]["open"]
ge10=[x["pair"] for x in t[table]["min_ge10"]]
mode="$MODE"
if mode=="smoke":
    # 3 open pairs + 1 known calibration
    pairs=["A-B"] + opens[:3]
elif mode=="estimate":
    pairs=opens[:1] if opens else ["A-B"]
else:
    pairs=list(opens)
    # optional p2 attempts after opens — included as second phase flag
Path("$WORKDIR/pairs_open.json").write_text(json.dumps(pairs, indent=2))
Path("$WORKDIR/pairs_ge10.json").write_text(json.dumps(ge10, indent=2))
print(f"table={table} mode={mode} open_pairs={len(opens)} queued={len(pairs)} ge10={len(ge10)}")
PY

if [[ "$MODE" == "estimate" ]]; then
  echo "== timed sample =="
  t0=$(date +%s)
  nice -n 19 python3 -m py.worker \
    --pairs "$WORKDIR/pairs_open.json" --table "$TABLE" \
    --k-min "$KMIN" --k-max "$KMAX" --timeout "$TIMEOUT" \
    --out "$WORKDIR/estimate.jsonl" --work "$WORKDIR/est"
  t1=$(date +%s)
  echo "sample_seconds $((t1-t0))"
  n=$(python3 -c "import json;print(len(json.load(open('$WORKDIR/pairs_open.json'))))")
  # workers estimate
  eval "$(scripts/workers.sh | awk '/^(PEAK|MEM|WORKERS)/{print}')"
  # For estimate mode workers.sh ran a sample already; use WORKERS
  W=$(scripts/workers.sh 2>/dev/null | awk '/^WORKERS/{print $2}')
  echo "WORKERS $W"
  python3 - <<PY
sec=$((t1-t0))
# estimate used 1 pair; full open list:
import json
n=len(json.load(open("$WORKDIR/pairs_open.json")))
# Actually estimate mode rewrote pairs to 1; reload opens
import json
from pathlib import Path
t=json.loads(Path("data/tables.json").read_text())
n=len(t["$TABLE"]["open"])
W=max(1,int("$W" or 1))
eta=sec*n/W
print(f"open_pairs {n}")
print(f"sample_sec_per_pair {sec}")
print(f"workers {W}")
print(f"eta_seconds {eta:.0f}")
print(f"eta_hours {eta/3600:.2f}")
PY
  exit 0
fi

W="${WORKERS:-}"
if [[ -z "$W" ]]; then
  W=$(scripts/workers.sh | awk '/^WORKERS/{print $2}')
fi
NPAIRS=$(python3 -c 'import json,sys;print(len(json.load(open(sys.argv[1]))))' "$WORKDIR/pairs_open.json")
if (( W > NPAIRS )); then W=$NPAIRS; fi
echo "Using WORKERS=$W"

# shard pairs
python3 - <<PY
import json
from pathlib import Path
pairs=json.load(open("$WORKDIR/pairs_open.json"))
W=max(1,min(int("$W"),len(pairs)))
for i in range(W):
    shard=pairs[i::W]
    (Path("$WORKDIR")/f"shard_{i}.json").write_text(json.dumps(shard))
    print(f"shard {i}: {len(shard)} pairs")
PY

PIDS=()
cleanup() {
  for pid in "${PIDS[@]:-}"; do
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
    fi
  done
}
trap cleanup EXIT INT TERM

for i in $(seq 0 $((W-1))); do
  nice -n 19 python3 -m py.worker \
    --pairs "$WORKDIR/shard_${i}.json" --table "$TABLE" \
    --k-min "$KMIN" --k-max "$KMAX" --timeout "$TIMEOUT" \
    --out "$WORKDIR/results_${i}.jsonl" --work "$WORKDIR" &
  PIDS+=($!)
done

echo "launched ${#PIDS[@]} workers: ${PIDS[*]}"
echo "stop with: touch $WORKDIR/STOP"
fail=0
for pid in "${PIDS[@]}"; do
  if ! wait "$pid"; then fail=1; fi
done
trap - EXIT INT TERM
scripts/summary.sh "$WORKDIR" || true
exit $fail
