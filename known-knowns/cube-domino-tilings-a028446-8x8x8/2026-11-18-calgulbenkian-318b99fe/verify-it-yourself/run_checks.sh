#!/bin/sh
set -u

BIN="./verify-it-yourself/.verify_fresh_primes_bin_$$"
cleanup() {
    rm -f "$BIN"
}
trap cleanup EXIT INT TERM

if ! python3 verify-it-yourself/verify_a049507_7.py; then
    echo "FAIL"
    exit 1
fi

if ! cc -O3 -pthread verify-it-yourself/verify_fresh_primes.c -o "$BIN"; then
    echo "FAIL"
    exit 1
fi

if ! "$BIN"; then
    echo "FAIL"
    exit 1
fi

echo "PASS"
exit 0
