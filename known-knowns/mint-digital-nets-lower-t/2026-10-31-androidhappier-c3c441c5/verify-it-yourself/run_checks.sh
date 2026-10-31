#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# Checks object/net_F2_t11_m24_s17.txt is the claimed file and generates a digital (11,24,17)-net over F_2.
# Needs python3 (standard library only). If a C compiler (cc) is present, a second, independently written checker
# (netcheck_b.c) is also run. The last output line is PASS or FAIL.
OBJ=object/net_F2_t11_m24_s17.txt
OBJ13=object/net_F2_t11_m24_s17_first13rows.txt
WANT=c3c441c507605e64d545fb6c6ab57863c7306e8b29dc88bafca22577dfd54618
ok=1

echo "== 1. sha256 of $OBJ"
GOT=$(python3 -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$OBJ")
echo "got  $GOT"
echo "want $WANT"
if [ "$GOT" = "$WANT" ]; then echo "sha256: match"; else echo "sha256: MISMATCH"; ok=0; fi

echo "== 2. $OBJ13 equals rows 1..13 of each block of $OBJ"
python3 - "$OBJ" "$OBJ13" <<'PY'
import sys
def blocks(p):
    out, cur = [], []
    for l in open(p):
        l = l.strip()
        if l.startswith('#'):
            continue
        if not l:
            if cur: out.append(cur); cur = []
            continue
        cur.append(l)
    if cur: out.append(cur)
    return out
a, b = blocks(sys.argv[1]), blocks(sys.argv[2])
same = len(a) == len(b) == 17 and all(x[:13] == y for x, y in zip(a, b))
print("first13rows consistent:", same)
sys.exit(0 if same else 1)
PY
[ $? -eq 0 ] || ok=0

echo "== 3. Python checker (check_net.py), t=11: every composition of 13 into 17 parts (about 1-2 minutes)"
python3 verify-it-yourself/check_net.py "$OBJ" 24 17 11
[ $? -eq 0 ] || ok=0

echo "== 4. control: the same object at t=10 must FAIL (shows the checker can reject)"
python3 verify-it-yourself/check_net.py "$OBJ" 24 17 10 > control_out.txt 2>&1
rc=$?
cat control_out.txt; rm -f control_out.txt
if [ $rc -eq 0 ]; then echo "control: unexpected PASS at t=10"; ok=0; else echo "control: FAIL at t=10 as expected"; fi

echo "== 4b. control: a copy with row 1 of C_17 replaced by row 1 of C_16 must FAIL at t=11"
M=$(mktemp -d)
python3 - "$OBJ" "$M/mutated.txt" <<'PY'
import sys
lines = open(sys.argv[1]).read().split('\n')
rows = [i for i, l in enumerate(lines) if l and not l.startswith('#')]
# block i = data rows 24*(i-1) .. 24*i-1
lines[rows[24 * 16]] = lines[rows[24 * 15]]
open(sys.argv[2], 'w').write('\n'.join(lines))
PY
python3 verify-it-yourself/check_net.py "$M/mutated.txt" 24 17 11
rc=$?
rm -rf "$M"
if [ $rc -eq 0 ]; then echo "mutation control: unexpected PASS"; ok=0; else echo "mutation control: FAIL as expected"; fi

echo "== 5. second checker (netcheck_b.c, C, incremental echelon over F_q), t=11"
if command -v cc >/dev/null 2>&1; then
  W=$(mktemp -d)
  if cc -O2 -o "$W/netcheck_b" verify-it-yourself/netcheck_b.c; then
    "$W/netcheck_b" "$OBJ" 2 24 17 11
    [ $? -eq 0 ] || ok=0
  else
    echo "compile failed"; ok=0
  fi
  rm -rf "$W"
else
  echo "no C compiler found; second checker skipped (the Python checker alone decides)"
fi

if [ $ok -eq 1 ]; then echo PASS; exit 0; else echo FAIL; exit 1; fi
