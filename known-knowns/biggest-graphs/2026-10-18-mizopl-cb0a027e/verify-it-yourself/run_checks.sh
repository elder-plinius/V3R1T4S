#!/bin/sh
# Standalone check for object/G_14_3_N1118.edges and object/G_14_3_N1118.txt. Run from the package folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
OBJ="$HERE/object/G_14_3_N1118.edges"
OBJ_TXT="$HERE/object/G_14_3_N1118.txt"
CHK="$HERE/verify-it-yourself/check_dd.py"
PY="/opt/homebrew/bin/python3"
[ -x "$PY" ] || PY="python3"
fail=0
if [ ! -f "$OBJ" ]; then echo "FAIL missing object/G_14_3_N1118.edges"; exit 1; fi
if [ ! -f "$OBJ_TXT" ]; then echo "FAIL missing object/G_14_3_N1118.txt"; exit 1; fi
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
got_txt_sha=$($SHA "$OBJ_TXT" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ] && [ "$got_txt_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha / $got_txt_sha, expected $exp_sha)"; fail=1; fi
echo "== check_dd.py on object/G_14_3_N1118.edges"
"$PY" "$CHK" "$OBJ" --delta 14 --diameter 3 --expect-n 1118 --record 1117 || fail=1
echo "== check_dd.py on object/G_14_3_N1118.txt"
"$PY" "$CHK" "$OBJ_TXT" --delta 14 --diameter 3 --expect-n 1118 --record 1117 || fail=1
echo "== negative control: a corrupted copy must FAIL"
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
awk '$1 != 0 && $2 != 0' "$OBJ" > "$TMP/G_14_3_N1118.edges"
if "$PY" "$CHK" "$TMP/G_14_3_N1118.edges" --delta 14 --diameter 3 --expect-n 1118 >"$TMP/neg.txt" 2>&1; then echo "negative control NOT rejected"; fail=1; else echo "negative control rejected as expected ($(tail -n 1 "$TMP/neg.txt"))"; fi
rm -f "$TMP/G_14_3_N1118.edges" "$TMP/neg.txt"; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
