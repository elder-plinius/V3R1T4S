#!/bin/sh
_PKG=$(cd "$(dirname "$0")/.." && pwd)
if command -v shasum >/dev/null 2>&1; then _S="shasum -a 256"; else _S="sha256sum"; fi
( cd "$_PKG" && grep "  object/" SHA256SUMS > "${TMPDIR:-/tmp}/objsums.$$" && $_S -c "${TMPDIR:-/tmp}/objsums.$$" >/dev/null 2>&1 ) || { echo "object file sha256 MISMATCH against SHA256SUMS"; echo "FAIL"; exit 1; }
# Standalone check for object/N53_S422_D19.txt. Run from this folder: sh verify-it-yourself/run_checks.sh
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
OBJ="$HERE/object/N53_S422_D19.txt"
CHK="$HERE/verify-it-yourself/check_sorter.py"
LIST="$HERE/the-record-we-beat/listed.json"
fail=0
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
exp_sha=$(tail -n 1 "$HERE/INDEX.csv" | awk -F, '{print $NF}')
got_sha=$($SHA "$OBJ" | cut -d' ' -f1)
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
echo "== check_sorter.py: exact 0-1 principle check, depth, comparison with the listed pairs"
python3 -I "$CHK" "$OBJ" 53 422 19 "$LIST" | tee "$TMP/out.json"
python3 -I -c "import json,sys; r=json.loads(open(sys.argv[1]).read().strip().splitlines()[-1]); ok=r.get('SORTS') is True and r.get('matches_stated_n_size_depth') is True and r.get('not_dominated_by_any_listed_pair') is True; print('checker verdict:', 'PASS' if ok else 'FAIL', '(SORTS=%s, n/size/depth match=%s, not dominated by a listed pair=%s)'%(r.get('SORTS'),r.get('matches_stated_n_size_depth'),r.get('not_dominated_by_any_listed_pair'))); sys.exit(0 if ok else 1)" "$TMP/out.json" || fail=1
echo "== negative control: the middle comparator deleted must NOT sort"
python3 -I "$CHK" "$OBJ" 53 422 19 "$LIST" --neg > "$TMP/neg.json"
if python3 -I -c "import json,sys; r=json.loads(open(sys.argv[1]).read().strip().splitlines()[-1]); sys.exit(0 if r.get('SORTS') is False else 1)" "$TMP/neg.json"; then echo "negative control rejected as expected (SORTS false)"; else echo "negative control NOT rejected"; fail=1; fi
rm -f "$TMP/out.json" "$TMP/neg.json"; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
