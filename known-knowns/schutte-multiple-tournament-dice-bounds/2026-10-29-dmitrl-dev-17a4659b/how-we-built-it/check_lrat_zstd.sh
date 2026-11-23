#!/bin/sh
# usage: check_lrat_zstd.sh <dir> <name> [heapMB]
# Streams <name>.lrat.zst through a FIFO into cake_lpr (checking <name>.cnf) and computes the sha256 of the
# uncompressed proof on the way. Last line of <name>.cake_lpr.out is cake_lpr's verdict.
set -u
DIR=$1; NAME=$2; HEAP=${3:-1500}
CODE=$(cd "$(dirname "$0")" && pwd)
cd "$DIR" || exit 3
rm -f "$NAME.chk.fifo"; mkfifo "$NAME.chk.fifo" || exit 4
( zstd -dc -q "$NAME.lrat.zst" | tee "$NAME.chk.fifo" | shasum -a 256 | sed "s/  -\$/  $NAME.lrat/" > "$NAME.lrat.sha256" ) &
SP=$!
perl -e 'alarm 3600; exec @ARGV' python3 "$CODE/rss_run.py" "${CAKE_LPR:-cake_lpr}" --CML_HEAP_SIZE="$HEAP" --CML_STACK_SIZE=512 "$NAME.cnf" "$NAME.chk.fifo" > "$NAME.cake_lpr.out" 2> "$NAME.cake_lpr.err"
echo "cake_lpr wrapper rc=$?"
# if cake_lpr gave no verdict (it may never have opened the FIFO), drain the FIFO so the writer side can finish
if ! grep -q '^s ' "$NAME.cake_lpr.out"; then
  perl -e 'alarm 600; open(my $f, "<", $ARGV[0]) or exit; while (read($f, my $b, 1<<20)) {}' "$NAME.chk.fifo" 2>/dev/null
fi
wait $SP; rm -f "$NAME.chk.fifo"
tail -n 1 "$NAME.cake_lpr.out"; cat "$NAME.cake_lpr.err"; cat "$NAME.lrat.sha256"
