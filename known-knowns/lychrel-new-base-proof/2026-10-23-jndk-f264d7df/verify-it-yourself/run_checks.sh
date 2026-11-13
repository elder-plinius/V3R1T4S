set -u
out=$("${PYTHON:-python3}" verify-it-yourself/check.py object/lychrel_base13.json 2>&1)
echo "$out"
case "$out" in *"CLAIM CHECK: PASS"*) echo PASS ;; *) echo FAIL; exit 1 ;; esac
