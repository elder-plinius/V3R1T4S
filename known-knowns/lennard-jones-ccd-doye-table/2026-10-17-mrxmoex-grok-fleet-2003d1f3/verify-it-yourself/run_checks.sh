#!/bin/sh
# (A) Lennard-Jones table errata, then (B) Morse table erratum 63C. Last line is PASS only if both parts pass.
cd "$(dirname "$0")/.." || exit 1
echo "== (A) Lennard-Jones tables: N = 602, 486, 487, 813, 899"; python3 verify-it-yourself/repro_ccd_lj_errata.py "$@"; a=$?
echo "== (B) Morse table: 63C, rho0 = 3"; python3 verify-it-yourself/repro_ccd_morse_63c.py; b=$?
if [ "$a" -eq 0 ] && [ "$b" -eq 0 ]; then echo PASS; else echo "FAIL (A exit $a, B exit $b)"; exit 1; fi
