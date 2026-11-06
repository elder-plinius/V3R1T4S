#!/bin/sh
# Re-run one certification job and print one TSV result line:
# job, result, cake_lpr line, cnf_sha_match, drat_sha_match, lrat_bytes_match, wall_s
# result is PASS only if cake_lpr prints exactly "s VERIFIED UNSAT" and the CNF sha256 matches the ledger.
# Usage (from the workspace root): sh threads/schutte/rerun_one.sh <job id> <scratch parent dir>
J="$1"; W="$(pwd)"; T="$W/logs/certify-tools"; S=$(cd "$2" && pwd) || exit 1
ROW=$(awk -F'\t' -v j="$J" '$2==j' "$W/certify/ledger.tsv")
D=$(mktemp -d "$S/job.XXXXXX"); T0=$(date +%s)
cd "$D" || exit 1
OUT="no ledger row"
if [ -n "$ROW" ]; then
  "$W/venv-schutte/bin/python" -I "$W/certify/solve.py" "$J" "$D" > solve.json 2> solve.err
  [ -f proof.drat ] && "$T/drat-trim/drat-trim" f.cnf proof.drat -i -w -L proof.lrat > drat.out 2>&1
  OUT=$([ -f proof.lrat ] && "$T/cake_lpr/cake_lpr" --CML_HEAP_SIZE=4500 --CML_STACK_SIZE=1000 f.cnf proof.lrat 2>&1 | tail -1)
  [ -n "$OUT" ] || OUT="no proof"
fi
SHA=$( [ -f f.cnf ] && shasum -a 256 f.cnf | cut -c1-64)
DSHA=$( [ -f proof.drat ] && shasum -a 256 proof.drat | cut -c1-64)
LB=$( [ -f proof.lrat ] && wc -c < proof.lrat | tr -d ' ')
m() { [ -n "$1" ] && [ "$1" = "$2" ] && echo 1 || echo 0; }
C=$(m "$SHA" "$(echo "$ROW" | cut -f5)"); P=$(m "$DSHA" "$(echo "$ROW" | cut -f8)"); L=$(m "$LB" "$(echo "$ROW" | cut -f10)")
R=FAIL; [ "$OUT" = "s VERIFIED UNSAT" ] && [ "$C" = 1 ] && R=PASS
cd "$W"; rm -rf "$D"
printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$J" "$R" "$OUT" "$C" "$P" "$L" "$(( $(date +%s) - T0 ))"
