#!/bin/sh
# Runs three exact programs on object/measure.json and compares with the pinned numbers. Last line PASS or FAIL.
D=$(cd "$(dirname "$0")" && pwd); ROOT=$D/..; O=$ROOT/object/measure.json; B=$D/.build; rm -rf "$B"; mkdir -p "$B"
EA=10845095970898536899315634; EM=5629639765; BAR=17027237336/10000000000
python3 -I - "$ROOT" "$D/object_hashes.txt" <<'H' || { echo "object file differs from verify-it-yourself/object_hashes.txt"; rm -rf "$B"; echo FAIL; exit 1; }
import sys,hashlib,os
r,f=sys.argv[1:3]
for l in open(f):
    h,p=l.split('  ');p=p.strip()
    if hashlib.sha256(open(os.path.join(r,p),'rb').read()).hexdigest()!=h: sys.exit(1)
H
cc -O2 -o "$B/check_b" "$D/check_b.c" 2>/dev/null || { echo "cc failed"; echo FAIL; exit 1; }
cc -O2 -o "$B/vsweep" "$D/third/vsweep.c" 2>/dev/null || { echo "cc failed"; echo FAIL; exit 1; }
python3 -I "$D/json2txt.py" "$O" > "$B/m.txt"
A=$(python3 -I "$D/check_a.py" "$O" 6 $BAR); echo "$A"
Bo=$("$B/check_b" "$B/m.txt" $((6<<30))); echo "$Bo"
"$B/vsweep" "$B/m.txt" 0 > "$B/sw.txt" 2>&1; python3 -I "$D/third/fmt.py" sweep "$B/sw.txt" | tee "$B/sw.fmt"
ok=1
echo "$A" | grep -q "area_num=$EA " || ok=0
echo "$A" | grep -q "mass_num=$EM " || ok=0
echo "$A" | grep -q "strictly_above_bar True" || ok=0
echo "$Bo" | grep -q "area_num=$EA " || ok=0
python3 -I - "$B/sw.fmt" "$BAR" <<'P' || ok=0
import sys,re
from fractions import Fraction as F
t=open(sys.argv[1]).read()
lo=F(re.search(r'V_lower ([0-9.]+)',t)[1]); hi=F(re.search(r'V_upper ([0-9.]+)',t)[1])
v=F(10845095970898536899315634,2**80)/F(5629639765,2**30)
sys.exit(0 if lo>F(sys.argv[2]) and v<=hi and hi-v<F(1,10**10) else 1)
P
rm -rf "$B"
[ $ok = 1 ] && { echo PASS; exit 0; }
echo FAIL
exit 1
