#!/bin/sh
# Verify the object from a clean copy of this package. Run from the package folder:
#   sh verify-it-yourself/run_checks.sh
# Two independently written exact-rational checkers (Python 3 standard library only) evaluate the lower bound LB(D)
# certified by object/mixture.json through Yao's principle; both must print exactly the expected fraction, and it must
# be strictly greater than 31/1326. A third script checks that the object's declared, informational fields (each
# environment's prior mean "mu" and the experts' "reports") agree with its structure. Last line: PASS or FAIL.
# Nothing is downloaded and nothing is written.
set -u
OBJ=object/mixture.json
EXPECTED=1652448303171916717080006468042849/70681471350112364987160770000000000
if [ ! -f "$OBJ" ]; then echo "missing $OBJ (run from the package folder)"; echo FAIL; exit 1; fi
out1=$(python3 -I verify-it-yourself/lb_check.py "$OBJ" 2>&1); r1=$?
echo "== lb_check.py (variance form and literal loss-difference definition), exit $r1"
echo "$out1"
out2=$(python3 -I verify-it-yourself/independent_recheck.py "$OBJ" 2>&1); r2=$?
echo "== independent_recheck.py (normalised-posterior route), exit $r2"
echo "$out2"
out3=$(python3 -I verify-it-yourself/check_declared_fields.py "$OBJ" 2>&1); r3=$?
echo "== check_declared_fields.py (declared mu and reports against the structure), exit $r3"
echo "$out3"
c3=$(echo "$out3" | awk -F': ' '/^declared fields consistent:/ {print $2}')
v1=$(echo "$out1" | awk -F': ' '/^LB_variance_form:/ {print $2}')
v1b=$(echo "$out1" | awk -F': ' '/^LB_literal_definition:/ {print $2}')
verdict=$(echo "$out1" | awk -F': ' '/^verdict:/ {print $2}')
v2=$(echo "$out2" | awk -F': ' '/^independent LB:/ {print $2}')
gt2=$(echo "$out2" | awk -F': ' '/^strictly greater than bar:/ {print $2}')
# exact check, independent of both scripts' own verdicts: 1326 * numerator > 31 * denominator
gt3=$(python3 -I -c "import sys; from fractions import Fraction as F; v = F(sys.argv[1]); print('yes' if v > F(31, 1326) else 'no')" "$EXPECTED" 2>&1)
if [ "$r1" -eq 0 ] && [ "$r2" -eq 0 ] && [ "$r3" -eq 0 ] && [ "$c3" = "yes" ] && [ "$v1" = "$EXPECTED" ] && [ "$v1b" = "$EXPECTED" ] && [ "$v2" = "$EXPECTED" ] \
   && [ "$verdict" = "LOWER_BOUND_BEATS_BAR" ] && [ "$gt2" = "yes" ] && [ "$gt3" = "yes" ]; then
  echo "three exact computations agree: LB = $EXPECTED > 31/1326; declared fields consistent"
  echo PASS
else
  echo "mismatch: lb_check exit $r1 (variance ${v1:-none}, literal ${v1b:-none}, verdict ${verdict:-none}); independent_recheck exit $r2 (${v2:-none}, greater ${gt2:-none}); declared fields exit $r3 (${c3:-none}); expected $EXPECTED"
  echo FAIL
  exit 1
fi
