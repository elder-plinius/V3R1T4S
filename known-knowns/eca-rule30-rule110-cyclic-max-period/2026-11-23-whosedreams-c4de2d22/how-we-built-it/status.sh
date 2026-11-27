#!/bin/bash
# Show what run_r30.sh is doing. Usage: ./status.sh   (or SMOKE=1 ./status.sh)
ROOT=$(cd "$(dirname "$0")" && pwd)
W=$ROOT/work; [ "${SMOKE:-0}" = 1 ] && W=$ROOT/work-smoke
echo "--- status ---"; cat "$W/STATUS.txt" 2>/dev/null || echo "(not started yet)"
echo "--- finished stages ---"; for f in "$W"/.done_*; do [ -e "$f" ] && echo "  ${f##*/.done_}"; done
echo "--- last log lines ---"; tail -n 8 "$W/run.log" 2>/dev/null
echo "--- memory (GiB) ---"; free -g | head -2
