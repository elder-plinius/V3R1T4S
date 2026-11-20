#!/bin/sh
set -u

CERT="object/d19_nonisometric_periodic_packing_certificate.json"
if [ ! -f "$CERT" ]; then
    echo "Missing $CERT (run from package root: sh verify-it-yourself/run_checks.sh)"
    echo "FAIL"
    exit 1
fi

TMPBIN="${TMPDIR:-/tmp}/verify_packing_c99_$$"
cleanup() {
    rm -f "$TMPBIN"
}
trap cleanup EXIT INT TERM

fail_check() {
    echo "$1"
    echo "FAIL"
    exit 1
}

echo "=== [1/4] Compiling strict ISO C99 zero-float verifier ==="
MGR_FLAG=""
if printf 'int main(void){return 0;}\n' | cc -std=c99 -mgeneral-regs-only -x c - -o "$TMPBIN" >/dev/null 2>&1; then
    MGR_FLAG="-mgeneral-regs-only"
    rm -f "$TMPBIN"
fi
cc -std=c99 -O2 -Wall -Wextra -Werror -Wpedantic $MGR_FLAG verify-it-yourself/verify_packing_c99.c -o "$TMPBIN" || fail_check "C99 compilation failed"

echo "=== [2/4] Running strict ISO C99 exact rational verifier ==="
"$TMPBIN" "$CERT" || fail_check "C99 verifier rejected certificate"

echo "=== [3/4] Running independent Python stdlib fractions.Fraction verifier ==="
python3 -B verify-it-yourself/verify_packing_py.py "$CERT" || fail_check "Python verifier rejected certificate"

echo "=== [4/4] Running negative-control corruption rejection checks ==="
if "$TMPBIN" "$CERT" --corrupt >/dev/null 2>&1; then
    fail_check "C99 verifier accepted corrupted certificate"
fi
if python3 -B verify-it-yourself/verify_packing_py.py "$CERT" --corrupt >/dev/null 2>&1; then
    fail_check "Python verifier accepted corrupted certificate"
fi
echo "[NEGATIVE CONTROLS] Both C99 and Python verifiers exited non-zero on corrupted input."
echo "PASS"
