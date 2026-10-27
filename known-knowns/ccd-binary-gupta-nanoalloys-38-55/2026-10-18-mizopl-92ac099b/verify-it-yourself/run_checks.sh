#!/bin/sh
# Standalone check for object/Cu39Ag16_improved.txt and the 7 companion CuAg55 structures.
# Run from the package folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
OBJ="$HERE/object/Cu39Ag16_improved.txt"
CHK="$HERE/verify-it-yourself/check_bingupta.py"
PY="/opt/homebrew/bin/python3"
[ -x "$PY" ] || PY="python3"
fail=0
if [ ! -f "$OBJ" ]; then echo "FAIL missing object/Cu39Ag16_improved.txt"; exit 1; fi
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
# Check non-trivial content (55 atoms, 0=Cu and 1=Ag)
n_atoms=$(awk 'NF==4 && ($1=="0" || $1=="1") {c++} END {print c+0}' "$OBJ")
if [ "$n_atoms" -ne 55 ]; then echo "FAIL expected 55 atom rows in Cu39Ag16_improved.txt, got $n_atoms"; exit 1; fi
echo "== check_bingupta.py on object/"
"$PY" "$CHK" "$HERE/object" || fail=1
echo "== negative control: a corrupted copy must FAIL"
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
cp -R "$HERE/object" "$TMP/object"
rm -f "$TMP/object/cuag55_improvements_summary.tsv"
# Perturb first coordinate of Cu39Ag16_improved.txt by +0.05 Angstrom so gradient norm fails
awk 'NR==4 {$2 = $2 + 0.05} {print}' "$OBJ" > "$TMP/object/Cu39Ag16_improved.txt"
if "$PY" "$CHK" "$TMP/object" >"$TMP/neg.txt" 2>&1; then
    echo "negative control NOT rejected"; fail=1
else
    echo "negative control rejected as expected ($(tail -n 1 "$TMP/neg.txt"))"
fi
rm -rf "$TMP"
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
