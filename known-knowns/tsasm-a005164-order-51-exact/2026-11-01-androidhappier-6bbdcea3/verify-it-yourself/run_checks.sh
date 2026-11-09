#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# Checks that object/A005164_25.txt is the claimed file and that its value equals A005164(25), recomputed here
# from the definition by an exact big-integer height-function DP (tsasm_height_dp.py). The same DP must
# reproduce the published a(0..24), and a brute-force count straight from the ASM definition (tsasm_brute.py) must
# agree with it for n = 0..8. Needs python3 only (standard library). About 1-3 minutes on a laptop.
# The last output line is PASS or FAIL.
OBJ=object/A005164_25.txt
WANT=6bbdcea3372a91c60f07506f99ec6b9660bc885517e741f43460352421d6b745
ok=1
W=$(mktemp -d)

echo "== 1. sha256 of $OBJ"
GOT=$(python3 -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$OBJ")
echo "got  $GOT"
echo "want $WANT"
if [ "$GOT" = "$WANT" ]; then echo "sha256: match"; else echo "sha256: MISMATCH"; ok=0; fi

echo "== 2. brute force from the definition: fixtures, then a(0..8)"
python3 verify-it-yourself/tsasm_brute.py 8 > "$W/brute.txt" || ok=0
cat "$W/brute.txt"

echo "== 3. exact height-function DP, n = 0..25 (about 1-3 minutes)"
python3 verify-it-yourself/tsasm_height_dp.py 0 25 > "$W/dp.txt" || ok=0
cat "$W/dp.txt"

echo "== 4. compare: DP vs brute force (n<=8), DP vs published a(0..24), DP a(25) vs the object"
python3 - "$W/brute.txt" "$W/dp.txt" "$OBJ" <<'PY' || ok=0
import re, sys
# OEIS A005164 DATA a(0..24) (revision #41, unchanged since Sep 21 2022)
pub = [1, 1, 1, 2, 4, 13, 46, 248, 1516, 13654, 142873, 2156888, 38456356, 974936056, 29540545024,
       1259111024288, 64726478396896, 4641989615977216, 404396533544588344, 48825344233129714772,
       7202552030561982627472, 1464587581921220811285325, 365627222082497915618219716,
       125253905685915522767942493032, 52893528399758443649956432899616]
bad = 0
bt = open(sys.argv[1]).read()
fix = ("fixture pos (order-5 TSASM): True" in bt and "fixture neg1 (identity 3, ASM not TSASM): True False" in bt
       and "fixture neg2 (symmetric non-ASM): False" in bt)
print("brute-force fixtures behave as expected:", fix); bad += not fix
brute = {int(m[1]): int(m[2]) for m in re.finditer(r"a\((\d+)\) order \d+: (\d+)", bt)}
dp = {}
for l in open(sys.argv[2]):
    f = l.split()
    if len(f) == 2: dp[int(f[0])] = int(f[1])
if sorted(brute) != list(range(9)) or sorted(dp) != list(range(26)):
    print("missing output lines"); bad += 1
else:
    b_ok = all(brute[n] == dp[n] for n in range(9)); print("DP == brute force for n=0..8:", b_ok); bad += not b_ok
    p_ok = all(dp[n] == pub[n] for n in range(25)); print("DP == published a(0..24):", p_ok); bad += not p_ok
lines = [l.split() for l in open(sys.argv[3]) if l.strip()]
if len(lines) != 1 or len(lines[0]) != 2 or lines[0][0] != "25" or not lines[0][1].isdigit():
    print("object format: expected exactly one line '25 <a(25)>'"); bad += 1
else:
    v = int(lines[0][1]); o_ok = dp.get(25) == v
    print("object a(25) =", v); print("DP     a(25) =", dp.get(25)); print("object == DP a(25):", o_ok); bad += not o_ok
sys.exit(1 if bad else 0)
PY

rm -rf "$W"
if [ $ok -eq 1 ]; then echo PASS; exit 0; else echo FAIL; exit 1; fi
