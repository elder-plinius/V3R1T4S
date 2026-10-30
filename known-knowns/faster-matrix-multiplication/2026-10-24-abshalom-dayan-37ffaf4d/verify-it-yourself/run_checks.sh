#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs only python3 (standard library), no network. Last line: PASS or FAIL. About 1.5 minutes on a laptop.
# object/v.txt is stored as two parts (1 MB per-file limit); this script joins them, checks the sha256 of the three
# factor files against the values below, then runs two independent exact checkers.
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
PY=$(command -v python3 || command -v python)
[ -n "$PY" ] || { echo "no python3 found"; echo FAIL; exit 1; }
T=$(mktemp -d "${TMPDIR:-/tmp}/assembled.XXXXXX") || { echo FAIL; exit 1; }
cp object/u.txt object/w.txt "$T/" && cat object/v.part1.txt object/v.part2.txt > "$T/v.txt" || { echo FAIL; exit 1; }
"$PY" -I - "$T" <<'PYEOF'
import hashlib, sys
want = {"u.txt": "37ffaf4dc24686ccb944605fd965f8b981088a74cf5246a54d6bcf5a2b665eca",
        "v.txt": "5d15717baf763e44e9fb2808ff92335e66ec76f0940c0f75839a79a33ea4c5be",
        "w.txt": "0f0a3d5cffe4ba63b5aa9a464c87abe0c17a501028c2d7f0d02cc128ea4fd93a"}
ok = True
for f, h in want.items():
    got = hashlib.sha256(open(sys.argv[1] + "/" + f, "rb").read()).hexdigest()
    print(got, f, "(matches)" if got == h else "(MISMATCH, expected %s)" % h)
    ok &= got == h
sys.exit(0 if ok else 1)
PYEOF
s0=$?
echo "== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py)"
"$PY" -I verify-it-yourself/check_brent_stdlib.py "$T" --trials 3 --seed 20261024; s1=$?
echo "== check 2: second exact Brent-equation checker (check_scheme_second.py)"
"$PY" -I verify-it-yourself/check_scheme_second.py "$T"; s2=$?
rm -rf "$T"
if [ "$s0" -eq 0 ] && [ "$s1" -eq 0 ] && [ "$s2" -eq 0 ]; then echo PASS; exit 0; fi
echo FAIL; exit 1
