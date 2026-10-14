#!/usr/bin/env bash
# Optional search replay, adapted from original to the standalone submission package.
# Not required to verify the 603-word mathematical witness.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROUNDS="${1:-50}"
SECONDS="${2:-150}"
OUTDIR="${OUTDIR:-$HERE/replay_run}"
mkdir -p "$OUTDIR"
g++ -O3 -march=native -std=c++17 "$HERE/engine.cpp" -o "$OUTDIR/engine"
set +e
"$OUTDIR/engine" "$HERE/A34_8_7_602.txt" 34 7 4 4 12 101 "$ROUNDS" "$SECONDS" "$OUTDIR/stage3"
RC=$?
set -e
if [ "$RC" -ne 0 ] && [ "$RC" -ne 2 ]; then
  echo "SEARCH_ERROR engine exit $RC" >&2
  exit "$RC"
fi
if [ -f "$OUTDIR/stage3_candidate.txt" ]; then
  python3 "$HERE/check_code.py" "$OUTDIR/stage3_candidate.txt" --minimum 603 --output "$OUTDIR/pairwise.json"
  python3 "$HERE/check_subsets.py" "$OUTDIR/stage3_candidate.txt" --minimum 603 --output "$OUTDIR/subsets.json"
  python3 - "$OUTDIR/stage3_candidate.txt" "$HERE/../object/A34_8_7_603.txt" <<'PYCODE'
from pathlib import Path
import hashlib,sys
x=Path(sys.argv[1]).read_bytes();target=Path(sys.argv[2]).read_bytes()
print('candidate_words:',len(x.splitlines()))
print('candidate_sha256:',hashlib.sha256(x).hexdigest())
print('matches_saved_witness:',x==target)
PYCODE
else
  echo "SEARCH_NO_GAIN: no 603-word candidate emerged within requested rounds/time. This does not invalidate the saved exact certificate."
fi
