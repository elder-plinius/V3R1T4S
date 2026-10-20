#!/bin/sh
# Standalone verification for the N=3949 cci claim.
# Run from the package folder (or a clean copy of it):  sh verify-it-yourself/run_checks.sh
# Last output line is PASS or FAIL.
set -u
cd "$(dirname "$0")"
TMPFILE="./corrupted_check.tmp"

echo "== 1. clean object: 50-digit feasible radius vs table =="
python3 verify.py ../object/candidate_n3949.txt | tee check_clean.txt
tail -1 check_clean.txt | grep -qx 'PASS' || { echo 'FAIL'; exit 1; }

echo "== 2. corrupted copy (one center duplicated -> zero pair distance) must be rejected =="
python3 - <<'EOF'
lines = open('../object/candidate_n3949.txt').read().splitlines()
p = lines[0].split()
p[1] = p[2]  # move center 1 exactly onto center 2
lines[0] = ' '.join(p)
open('./corrupted_check.tmp', 'w').write('\n'.join(lines) + '\n')
print('corrupted copy written')
EOF
python3 verify.py "$TMPFILE" | tee check_corrupted.txt
tail -1 check_corrupted.txt | grep -qx 'FAIL' || { rm -f "$TMPFILE" check_clean.txt check_corrupted.txt; echo 'FAIL'; exit 1; }
rm -f "$TMPFILE" check_clean.txt check_corrupted.txt

echo 'PASS'
