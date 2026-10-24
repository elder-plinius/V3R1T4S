#!/bin/sh
_PKG=$(cd "$(dirname "$0")/.." && pwd)
if command -v shasum >/dev/null 2>&1; then _S="shasum -a 256"; else _S="sha256sum"; fi
( cd "$_PKG" && grep "  object/" SHA256SUMS > "${TMPDIR:-/tmp}/objsums.$$" && $_S -c "${TMPDIR:-/tmp}/objsums.$$" >/dev/null 2>&1 ) || { echo "object file sha256 MISMATCH against SHA256SUMS"; echo "FAIL"; exit 1; }
# Run from anywhere: sh verify-it-yourself/run_checks.sh
# python3 3.8+, standard library only. Uses 3 worker processes plus a mostly idle coordinating process.
# Needs about 6 GB of memory in the coordinating process and about 1 GB per worker, and about 150 MB of temporary disk.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3saw)
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
WHOLE_EXP=$(grep ' WHOLE ' "$HERE/object/SHA256_PARTS.txt" | cut -d' ' -f1)
echo "== reassemble object/vector_part_*.bin and check the whole first"
cat "$HERE"/object/vector_part_*.bin > "$TMP/vector.xz"
got=$($SHA "$TMP/vector.xz" | cut -d' ' -f1)
if [ "$got" = "$WHOLE_EXP" ]; then echo "whole object sha256 matches ($got)"; else echo "whole object sha256 MISMATCH (got $got)"; fail=1; fi
echo "== each part against object/SHA256_PARTS.txt"
bad=0
for f in "$HERE"/object/vector_part_*.bin; do
  b=$(basename "$f"); exp=$(grep " $b\$" "$HERE/object/SHA256_PARTS.txt" | cut -d' ' -f1)
  g=$($SHA "$f" | cut -d' ' -f1); [ "$g" = "$exp" ] || { echo "part $b MISMATCH"; bad=1; }
done
[ $bad -eq 0 ] && echo "all parts match" || fail=1
echo "== negative controls (first 3000 states only)"
python3 -I -c "
import sys, lzma
d = bytearray(lzma.decompress(open(sys.argv[1], 'rb').read())); N = int.from_bytes(d[0:8], 'big')
a = bytearray(d); a[9] = 0; a[9 + N] = 0; a[9 + 2 * N] = 1      # state 0: vector entry set to 1
open(sys.argv[2], 'wb').write(lzma.compress(bytes(a), preset=1))
a = bytearray(d); a[9] = 0; a[9 + N] = 0; a[9 + 2 * N] = 0      # state 0: vector entry set to 0
open(sys.argv[3], 'wb').write(lzma.compress(bytes(a), preset=1))
" "$TMP/vector.xz" "$TMP/neg1.xz" "$TMP/neg2.xz"
python3 -I "$HERE/verify-it-yourself/check_saw482_k34.py" "$TMP/neg1.xz" 34 --limit 3000 --workers 3 > "$TMP/neg1.txt" 2>&1
if grep -q '^FAIL bound' "$TMP/neg1.txt"; then echo "negative control 1 (a vector entry set to 1) rejected as expected"; else echo "negative control 1 NOT rejected"; fail=1; fi
python3 -I "$HERE/verify-it-yourself/check_saw482_k34.py" "$TMP/neg2.xz" 34 --limit 3000 --workers 3 > "$TMP/neg2.txt" 2>&1
if grep -q '^FAIL all' "$TMP/neg2.txt"; then echo "negative control 2 (a vector entry set to 0) rejected as expected"; else echo "negative control 2 NOT rejected"; fail=1; fi
echo "== full check: rebuild all states and transitions, pocket tests, ordered subset-inclusion, exact ratio (about 30 to 60 minutes)"
python3 -I "$HERE/verify-it-yourself/check_saw482_k34.py" "$TMP/vector.xz" 34 --workers 3 | tee "$TMP/full.txt"
[ "$(tail -n 1 "$TMP/full.txt")" = "PASS" ] || fail=1
rm -f "$TMP"/*.xz "$TMP"/*.txt; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
