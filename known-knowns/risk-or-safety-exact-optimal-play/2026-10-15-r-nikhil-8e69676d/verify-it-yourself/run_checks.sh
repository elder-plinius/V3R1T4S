#!/bin/sh
# Verify the object from a clean copy of this package. Run from the package folder:
#   sh verify-it-yourself/run_checks.sh
# Needs python3 (3.9 or newer, standard library only) and gzip. Last output line: PASS or FAIL. About 30 s on a laptop.
set -u
W=verify-it-yourself/_work
rm -rf "$W"; mkdir -p "$W"
for k in 27 28 29 30; do
  gzip -dc "object/n$k.json.gz" > "$W/n$k.json" || { echo "gunzip failed for object/n$k.json.gz"; echo FAIL; exit 1; }
done
for k in 16 17 18 19 20 21 22 23 24 25 26; do cp "object/n$k.json" "$W/n$k.json"; done
CLAIM="$W/n16.json $W/n17.json $W/n18.json $W/n19.json $W/n20.json $W/n21.json $W/n22.json $W/n23.json $W/n24.json $W/n25.json $W/n26.json $W/n27.json $W/n28.json $W/n29.json $W/n30.json"
CAL="verify-it-yourself/calibration/n1.json verify-it-yourself/calibration/n2.json verify-it-yourself/calibration/n3.json verify-it-yourself/calibration/n4.json verify-it-yourself/calibration/n5.json verify-it-yourself/calibration/n6.json verify-it-yourself/calibration/n7.json verify-it-yourself/calibration/n8.json verify-it-yourself/calibration/n9.json verify-it-yourself/calibration/n10.json verify-it-yourself/calibration/n11.json verify-it-yourself/calibration/n12.json verify-it-yourself/calibration/n13.json verify-it-yourself/calibration/n14.json verify-it-yourself/calibration/n15.json"
# 1. The claim: every certificate n = 16..30 satisfies the Bellman optimality equations at every position (exact rationals).
python3 -I verify-it-yourself/ros_cert_check.py $CLAIM > "$W/check_claim.txt" 2>&1; r1=$?
tail -1 "$W/check_claim.txt"
# 2. Its P(0,0,0) values are the claimed terms in object/values.txt.
python3 -I verify-it-yourself/compare_values.py "$W/check_claim.txt" object/values.txt 16 30 > "$W/compare_values.txt" 2>&1; r2=$?
tail -1 "$W/compare_values.txt"
# 3. Calibration: the same solver's certificates for n = 1..15 pass and equal the published OEIS terms exactly.
python3 -I verify-it-yourself/ros_cert_check.py --oeis verify-it-yourself/published_terms $CAL > "$W/check_calibration.txt" 2>&1; r3=$?
tail -1 "$W/check_calibration.txt"
m=$(grep -c "oeis_match=yes PASS" "$W/check_calibration.txt")
# 4. A second verifier written independently (integer cross-multiplication, no Fraction) on all 30 certificates.
python3 -I verify-it-yourself/my_verify.py --oeis verify-it-yourself/published_terms $CAL $CLAIM > "$W/my_verify.txt" 2>&1; r4=$?
tail -1 "$W/my_verify.txt"
if [ "$r1" -eq 0 ] && [ "$r2" -eq 0 ] && [ "$r3" -eq 0 ] && [ "$r4" -eq 0 ] && [ "$m" -eq 15 ] \
   && grep -q "^ALL_PASS" "$W/check_claim.txt" && grep -q "^ALL_PASS" "$W/check_calibration.txt" \
   && grep -q "30 passed, 0 failed" "$W/my_verify.txt"; then
  echo "15 certificates n=16..30 verified; 15 calibration certificates n=1..15 equal the published terms; second verifier agrees"
  echo PASS
else
  echo "exit codes: checker $r1, values $r2, calibration $r3 (oeis matches $m/15), my_verify $r4"
  echo FAIL
  exit 1
fi
