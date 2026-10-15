#!/bin/sh
# Verify the object from a clean copy of this package. Run from the package folder:
#   sh verify-it-yourself/run_checks.sh
# Third-party data is not copied into the package: the public QOBLIB instance po_a200_t10_orig is downloaded once from a
# pinned commit and checked by sha256. Then two independent exact evaluators, both written from the class's ZIMPL
# reference model, evaluate the object. Last line: PASS or FAIL.
set -u
BASE=https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/a6b69e46763f98997da11d9b6bf0bfd34a1d8271/06-portfolio/instances/po_a200_t10_orig
D=verify-it-yourself/_instance
OBJ=object/a200_t10_orig_b050_l1e-02_solution.sol
mkdir -p "$D"
for f in stock_prices.txt.gz covariance_matrices.txt.gz; do
  if [ ! -s "$D/$f" ]; then
    curl -sS -A "V3R1T4S-verify" -o "$D/$f" "$BASE/$f" || { echo "download failed: $f"; echo FAIL; exit 1; }
  fi
done
python3 -I verify-it-yourself/check_portfolio.py "$D" "$OBJ" -691624 -551385 > verify-it-yourself/_check1.txt 2>&1
r1=$?
tail -4 verify-it-yourself/_check1.txt
python3 -I verify-it-yourself/zimpl_literal_eval.py "$D" "$OBJ" 50 0.01 > verify-it-yourself/_check2.txt 2>&1
r2=$?
cat verify-it-yourself/_check2.txt
v2=$(awk '/literal ZIMPL evaluation/ {print $NF}' verify-it-yourself/_check2.txt)
if [ "$r1" -eq 0 ] && [ "$r2" -eq 0 ] && [ "$v2" = "-691624" ]; then
  echo "both evaluators: feasible, objective -691624 < bar -551385"
  echo PASS
else
  echo "check_portfolio exit $r1, literal evaluator exit $r2 value ${v2:-none}"
  echo FAIL
  exit 1
fi
