# Receipts (real output, 2026-11-24 ~06:20 UTC, Linux x86_64, 8 cores, python-flint 0.9.0 installed by run_checks.sh into a fresh venv)

Fresh copy of this package, `sh verify-it-yourself/run_checks.sh` (wrapped in `time`):

```
precision bits: 128
check 0: wvcount matches the definition at 2859 points <= 20000
check 1-2: 9906 intervals admissible; recomputed sups <= stated (max relative slack 5.0e-06)
check 3: A(1e10) <= 0.01070009059 <= 0.0107001
B <= 2.1269871669853558245 (sup of the ball, recomputed)
check 4: B < 2.126988
PASS
precision bits: 256
check 0: wvcount matches the definition at 2859 points <= 20000
check 1-2: 9906 intervals admissible; recomputed sups <= stated (max relative slack 5.0e-06)
check 3: A(1e10) <= 0.01070009059 <= 0.0107001
B <= 2.1269871669853558245 (sup of the ball, recomputed)
check 4: B < 2.126988
PASS
both precisions: PASS
PASS

real	1m10.066s
user	4m14.188s
sys	0m0.531s
```

Corrupted copies (interval 5000 (0-based), stated sup 8.9347734822299243470e-7), `check_selberg.py <copy> 128`, last two lines:

```
# lowered to 8.9e-7
FAIL reason: interval 5000: recomputed 8.9347734822299243470e-7 exceeds stated 8.9e-7
FAIL
# raised to 8.94e-7 (+0.06%)
FAIL reason: interval 5000: stated 8.94e-7 exceeds recomputed 8.9347734822299243470e-7 by more than 1e-5 relative (corrupted certificate?)
FAIL
```

Both corrupted runs exit with status 1.

Note on the kit's one-digit test. The kit's `check_run.py --package` changes the middle digit of the object, which here is
the 20th significant digit of interval 4945 (0-based)'s stated sup (9.1317875198497075085e-7 becomes ...0751e-7, a relative change of
about 8e-20). The checker still prints PASS, and that is correct: it sums its own recomputed sups, so the stated values
are not load-bearing, and the change is far inside the 1e-15 rounding allowance. The kit reports this as a warning.
Changes that matter are rejected, as shown above. The check is two-sided: a stated value below the recomputed sup, or more
than 1e-5 above it, fails. A z_i outside [1, m_i^(1/4)) also fails.
