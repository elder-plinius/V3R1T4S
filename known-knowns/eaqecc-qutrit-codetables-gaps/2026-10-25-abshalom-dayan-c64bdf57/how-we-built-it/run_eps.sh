#!/bin/sh
# constructor lens: exhaustive max Hermitian hull over all 2^(n-1) sign patterns
# (epsbig, eps_0 = +1) for every .code file named in the list file $1, $2 at a time, nice 10, each capped at $3 s.
# Results: one line per code in $4 (file name + epsbig output). Driver and children are logged with PIDs in $4.pids.
L="$1"; P="$2"; CAP="$3"; OUT="$4"
D="$(cd "$(dirname "$0")" && pwd)"
echo "driver $$ start $(date -u +%Y-%m-%dT%H:%M:%SZ) list=$L P=$P cap=$CAP" >> "$OUT.pids"
xargs -P "$P" -I{} sh -c 'r=$(nice -n 10 perl -e "alarm shift; exec @ARGV" '"$CAP"' '"$D"'/epsbig 0 0 < {} 2>&1); echo "$(basename {}) $r"' < "$L" >> "$OUT"
echo "driver $$ end $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$OUT.pids"
