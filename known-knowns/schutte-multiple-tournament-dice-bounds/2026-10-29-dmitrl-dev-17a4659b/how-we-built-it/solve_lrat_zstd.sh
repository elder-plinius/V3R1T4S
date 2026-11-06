#!/bin/sh
# usage: solve_lrat_zstd.sh <dir> <name> <seconds>
# Runs CaDiCaL with a text LRAT proof written into a FIFO that zstd compresses to <name>.lrat.zst (in <dir>).
set -u
DIR=$1; NAME=$2; SECS=$3
CODE=$(cd "$(dirname "$0")" && pwd)
cd "$DIR" || exit 3
rm -f "$NAME.fifo"; mkfifo "$NAME.fifo" || exit 4
zstd -3 -q -T1 -f < "$NAME.fifo" > "$NAME.lrat.zst" &
ZP=$!
perl -e "alarm $SECS + 300; exec @ARGV" python3 "$CODE/rss_run.py" "${CADICAL:-cadical}" --lrat --no-binary -t "$SECS" "$NAME.cnf" "$NAME.fifo" > "$NAME.cadical.log" 2> "$NAME.rss"
echo "cadical rc=$?"
# if cadical never opened the FIFO, give zstd an EOF
perl -e 'alarm 5; open(my $f, ">", $ARGV[0]); close($f)' "$NAME.fifo" 2>/dev/null
wait $ZP; echo "zstd rc=$?"
rm -f "$NAME.fifo"
grep -E "^s |total process time|maximum resident" "$NAME.cadical.log"; cat "$NAME.rss"; ls -la "$NAME".* | awk '{print $5, $9}'
