#!/bin/sh
# Standalone check. Run from the claim folder: sh verify-it-yourself/run_checks.sh
# Needs python3 (3.8 or later), standard library only.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
cd "$HERE" || exit 1
fail=0
exp_sha=$(tail -n 1 INDEX.csv | awk -F, '{print $NF}')
got_sha=$(python3 -I -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "object/WIN_scu_739.txt")
if [ "$got_sha" = "$exp_sha" ]; then echo "sha256 of object/WIN_scu_739.txt matches INDEX.csv ($got_sha)"; else echo "sha256 MISMATCH (got $got_sha, expected $exp_sha)"; fail=1; fi
echo "== packcheck.py: exact feasible radius of object/WIN_scu_739.txt"
python3 -I verify-it-yourself/packcheck.py --kind cube --dim 3 --object object/WIN_scu_739.txt --expect-n 739 --table-radius 0.058531064606 --margin 1e-11 | tee "$HERE/verify-it-yourself/.last_pack.txt"
tail -n 1 "$HERE/verify-it-yourself/.last_pack.txt" | grep -q "^RESULT PASS" || fail=1
RSTAR=$(grep '^r_star=' "$HERE/verify-it-yourself/.last_pack.txt" | cut -d= -f2)
rm -f "$HERE/verify-it-yourself/.last_pack.txt"
echo "== (the posted Packomania coordinate file is not shipped; see RUN_IT_YOURSELF.md for the non-isometry check)"
echo "== table_compare.py: facts against the saved table records"
python3 -I verify-it-yourself/table_compare.py --n 739 --rstar "$RSTAR" --radius the-record-we-beat/radius_rows_N739_to_1000.txt --mj the-record-we-beat/mj_rows_extract.csv --shelf scu || fail=1
echo "== negative control: the first point is moved onto the second; the check must FAIL"
TMP=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
python3 -I - "object/WIN_scu_739.txt" "$TMP/neg.txt" 3 <<'PYEOF'
import sys
src, dst, d = sys.argv[1], sys.argv[2], int(sys.argv[3])
lines = open(src).read().split('\n')
idx = [i for i, l in enumerate(lines) if l.strip() and not l.startswith('#') and len(l.split()) >= d]
a, b = idx[0], idx[1]
ta, tb = lines[a].split(), lines[b].split()
ta[-d:] = tb[-d:]
lines[a] = ' '.join(ta)
open(dst, 'w').write('\n'.join(lines))
PYEOF
if python3 -I verify-it-yourself/packcheck.py --kind cube --dim 3 --object "$TMP/neg.txt" --expect-n 739 --table-radius 0.058531064606 --margin 1e-11 >"$TMP/neg_out.txt" 2>&1; then echo "negative control NOT rejected"; fail=1; else echo "negative control rejected as expected ($(grep '^r_star=' "$TMP/neg_out.txt"))"; fi
rm -f "$TMP/neg.txt" "$TMP/neg_out.txt"; rmdir "$TMP" 2>/dev/null
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASS"; else echo "FAIL"; exit 1; fi
