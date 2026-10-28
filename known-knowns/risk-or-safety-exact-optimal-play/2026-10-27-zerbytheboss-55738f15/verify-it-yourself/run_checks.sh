#!/bin/sh
# Verify the object from a clean copy of this package. Run from the package folder:
#   sh verify-it-yourself/run_checks.sh
# Needs python3 (standard library only) and gzip. Last output line: PASS or FAIL.
set -u
W=verify-it-yourself/_work
rm -rf "$W"; mkdir -p "$W"

for k in $(seq 31 45); do
  if [ -f "object/n$k.json.gz" ]; then
    gzip -dc "object/n$k.json.gz" > "$W/n$k.json" || { echo "gunzip failed for object/n$k.json.gz"; echo FAIL; exit 1; }
  else
    cat object/n$k.json.gz.part* | gzip -dc > "$W/n$k.json" || { echo "gunzip failed for object/n$k.json.gz.part*"; echo FAIL; exit 1; }
  fi
done

CLAIM=""
for k in $(seq 31 45); do
  CLAIM="$CLAIM $W/n$k.json"
done

CAL=""
for k in $(seq 1 15); do
  CAL="$CAL verify-it-yourself/calibration/n$k.json"
done

# 1. The claim: every certificate n = 31..45 satisfies the Bellman optimality equations at every position (exact rationals).
python3 -I verify-it-yourself/ros_cert_check.py $CLAIM > "$W/check_claim.txt" 2>&1; r1=$?
tail -1 "$W/check_claim.txt"

# 2. Its P(0,0,0) values are the claimed terms in object/values.txt.
python3 -I verify-it-yourself/compare_values.py "$W/check_claim.txt" object/values.txt 31 45 > "$W/compare_values.txt" 2>&1; r2=$?
tail -1 "$W/compare_values.txt"

# 3. Calibration: the certificates for n = 1..15 pass and equal the published OEIS terms exactly.
python3 -I verify-it-yourself/ros_cert_check.py --oeis verify-it-yourself/published_terms $CAL > "$W/check_calibration.txt" 2>&1; r3=$?
tail -1 "$W/check_calibration.txt"
m=$(grep -c "oeis_match=yes PASS" "$W/check_calibration.txt")

# 4. A second verifier written independently (integer cross-multiplication, no Fraction) on all 30 certificates.
python3 -I verify-it-yourself/my_verify.py --oeis verify-it-yourself/published_terms $CAL $CLAIM > "$W/my_verify.txt" 2>&1; r4=$?
tail -1 "$W/my_verify.txt"

# 5. Calibration: reproduction of repository known-knowns (n = 16..30)
python3 -c '
from fractions import Fraction
exp = {int(l.split()[0]): Fraction(l.split()[1]) for l in open("verify-it-yourself/published_terms/values_16_30.txt") if "/" in l}
got = {int(l.split()[0]): Fraction(l.split()[1]) for l in open("object/values.txt") if "/" in l}
for n in range(16, 31):
    assert n in got and got[n] == exp[n], f"mismatch at {n}"
print("reproduced_known_knowns_16_30: ALL_EQUAL")
' > "$W/check_known_knowns.txt" 2>&1; r5=$?
tail -1 "$W/check_known_knowns.txt"

if [ "$r1" -eq 0 ] && [ "$r2" -eq 0 ] && [ "$r3" -eq 0 ] && [ "$r4" -eq 0 ] && [ "$r5" -eq 0 ] && [ "$m" -eq 15 ] \
   && grep -q "^ALL_PASS" "$W/check_claim.txt" && grep -q "^ALL_PASS" "$W/check_calibration.txt" \
   && grep -q "30 passed, 0 failed" "$W/my_verify.txt" \
   && grep -q "^reproduced_known_knowns_16_30: ALL_EQUAL" "$W/check_known_knowns.txt"; then
  echo "15 certificates n=31..45 verified; 15 calibration certificates n=1..15 equal published terms; repository terms n=16..30 reproduced; second verifier agrees"
  echo PASS
else
  echo "exit codes: checker $r1, values $r2, calibration $r3 (oeis matches $m/15), my_verify $r4, known_knowns $r5"
  echo FAIL
  exit 1
fi
