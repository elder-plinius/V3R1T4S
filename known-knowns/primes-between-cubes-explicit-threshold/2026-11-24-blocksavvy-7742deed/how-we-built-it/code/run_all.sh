#!/bin/sh
# Reproduce every number in CLAIM.md / PROOF.md. Needs python3 with python-flint (arb) and mpmath.
set -e
cd "$(dirname "$0")"
PY=${PY:-python3}
$PY cert_arb.py --Y 29.735 --c 51.34 --dens thm11 --prec 128 > ../out/main_prec128.txt
$PY cert_arb.py --Y 29.735 --c 51.34 --dens thm11 --prec 256 > ../out/main_prec256.txt
if $PY cert_arb.py --Y 29.734 --c 51.34 --dens thm11 --prec 256 > ../out/main_29.734_expect_FAIL.txt; then echo "UNEXPECTED PASS"; exit 1; fi
$PY standalone_check.py 29.735 51.34 thm11 > ../out/standalone_main.txt
if $PY standalone_check.py 29.734 51.34 thm11 > ../out/standalone_29.734_expect_FAIL.txt; then echo "UNEXPECTED PASS"; exit 1; fi
$PY cert_arb.py --Y 29.907 --c 54.004 --dens thm11 --prec 256 > ../out/journal_zfr_54.004_prec256.txt
if $PY cert_arb.py --Y 29.906 --c 54.004 --dens thm11 --prec 256 > ../out/journal_zfr_54.004_29.906_expect_FAIL.txt; then echo "UNEXPECTED PASS"; exit 1; fi
$PY standalone_check.py 29.907 54.004 thm11 > ../out/standalone_journal_zfr_54.004.txt
$PY scan.py > ../out/scan_out.txt
$PY null_tests.py > ../out/null_tests_out.txt
$PY replay_ch.py > ../out/replay_ch_out.txt
$PY mutation.py cert_arb.py > ../out/mutation_out.txt
grep -h "^PASS\|^FAIL\|ALL_CONTROLS\|CONTROL_FAILURE\|MUTATION" ../out/*.txt
echo RUN_ALL_DONE
