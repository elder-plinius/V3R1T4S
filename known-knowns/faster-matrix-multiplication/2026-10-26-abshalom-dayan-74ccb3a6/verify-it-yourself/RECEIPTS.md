# Receipts: real output of verify-it-yourself/run_checks.sh

Run on 2026-10-27 from a read-only copy of this package folder (copied, then chmod -R a-w; 8 s wall clock on the build
laptop), exit status 0. The script writes nothing inside the package folder. The output is the same as the run of
2026-10-26 (9 s) made with the earlier version of run_checks.sh, which wrote temporary files there:

    == exact Brent-equation check (check_scheme.py)
    format <14,15,15>, 1836 terms, every term with three nonzero factors, common denominator 54400, 9922500 Brent equations checked, 0 wrong
    rank 1836 scheme for <14,15,15> over Q verified exactly
    PASS
    == random exact evaluation against AB (check_random_eval.py)
    trial 1: 0 of 210 entries of C differ from AB
    trial 2: 0 of 210 entries of C differ from AB
    trial 3: 0 of 210 entries of C differ from AB
    PASS
    PASS
