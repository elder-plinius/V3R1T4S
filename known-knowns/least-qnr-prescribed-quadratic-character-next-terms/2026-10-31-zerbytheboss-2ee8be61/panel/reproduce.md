# Skeptic 1: Reproducibility & Independent Computation Audit

context: independent clean-room verification process started from package directory only

## Audit Summary

1. Executed `sh verify-it-yourself/run_checks.sh` from a clean temporary directory copy.
2. Verified that `check_qnr.py` independently validates every prime in `object/a000229_qnr_census.json` via deterministic 64-bit Miller-Rabin primality testing, Euler criterion $p^{(q-1)/2} \bmod q$, Quadratic Reciprocity Legendre symbols, and `b000229.txt` SHA-256 reproduction.
3. Verified that `verify_qnr_sieve.c` executes Stage 1 ($M_1 = 892,371,480$ vs $M_2 = 25,878,772,920$ up to $317,398,900,373,231$) and Stage 2 ($M_2 = 25,878,772,920$ vs $M_3 = 802,241,960,520$ up to $1,463,971,373,078,639$), reproducing `A000229(30..38)`, `A002223(30..38)`, and `A002224(30..41)` from 1 and certifying `A000229(39..43)` with element-by-element agreement across enumerators.
4. Confirmed that mutating a single digit of `object/a000229_qnr_census.json` causes `run_checks.sh` to exit with code 1 and output `FAIL`.

pass: true
