#!/bin/sh
# Verify this claim from the shipped files alone. No network, no drevalpy, no large dataset.
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# Override the interpreter with PYTHON=... if python3 lacks numpy/pandas.
# Last line is PASS or FAIL.
set -u
PY=${PYTHON:-python3}
FAILED=0

echo "interpreter: $($PY -c 'import sys; print(sys.version.split()[0])')  (standard library only -- no numpy, no pandas, no network)"
echo

$PY -I verify-it-yourself/check_claim.py || FAILED=1

# A checker that cannot fail proves nothing, so corrupt the object two ways and require the checker to
# RUN TO COMPLETION and report FAIL. A crash does not count as a rejection.
corrupt_must_fail() {
  label="$1"; mode="$2"
  TMP=.corrupt_check; rm -rf $TMP; mkdir -p $TMP
  cp -R object $TMP/object; cp -R verify-it-yourself $TMP/verify-it-yourself
  if ! $PY -I verify-it-yourself/corrupt.py "$mode" "$TMP/object" >/dev/null 2>&1; then
    echo "   -> FAILED: could not build the corrupted copy for '$label'"; FAILED=1; rm -rf $TMP; return
  fi
  out=$(cd $TMP && $PY -I verify-it-yourself/check_claim.py 2>&1)
  if printf '%s' "$out" | grep -q '^FAIL ('; then
    echo "   -> ok: '$label' rejected ($(printf '%s' "$out" | grep -c 'FAILED:') assertions fired)"
  elif printf '%s' "$out" | grep -q '^PASS$'; then
    echo "   -> FAILED: the checker PASSED a corrupted object ('$label')"; FAILED=1
  else
    echo "   -> FAILED: the checker crashed instead of reporting FAIL ('$label')"; FAILED=1
  fi
  rm -rf $TMP
}

echo
echo "=== corrupted objects must be rejected, and the checker must survive to say so ==="
corrupt_must_fail "model predictions replaced by the ruler's in ALL splits"        ruler_all
corrupt_must_fail "model predictions replaced by the ruler's in ONE split only"    ruler_one
corrupt_must_fail "ruler cell-line effects rescaled by 3x (model untouched)"       rescale
corrupt_must_fail "the 5 worst test drugs silently dropped from every split"       drop
corrupt_must_fail "a test drug also placed in training"                           leak
corrupt_must_fail "one digit of one prediction altered"                            digit

echo
if [ "$FAILED" -eq 0 ]; then echo PASS; exit 0; else echo FAIL; exit 1; fi
