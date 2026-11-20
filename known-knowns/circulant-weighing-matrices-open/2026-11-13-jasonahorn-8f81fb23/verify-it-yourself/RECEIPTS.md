# Verification receipts — repaired package, 2026-11-14

The original panel/preregistration files remain historical records. These receipts describe the repaired verification code. No submission is implied.

Environment: Python 3.14.9; NumPy 2.5.4; GCC 13.3.0; Linux. C source SHA256:
17290fe19200b4d6894a6c500673d06a5e6d9aee7376d447ed14df0008a8d5b7

## Clean-copy entrypoint

Command: sh verify-it-yourself/run_checks.sh
Executed in a newly copied package with a 300-second outer timeout and 24 GiB memory cap. Exit 0. All file bytes in that copy were unchanged after execution.

    Ran 18 tests
    OK
    CONTRACTIONS PASS: object = Python = C (25 distinct rows)
    ORBITS 35 TARGETS 25
    SELFTEST target0 brute=0 join=0 rejected=32 identity=ok
    SELFTEST synthetic-cancel-not-CW20881 brute=16 join=16 rejected=16 identity=ok
    SELFTEST synthetic-reject-not-CW20881 brute=8 join=8 rejected=24 identity=ok
    SELFTEST autocorrelation positive_weight4=ok negative=ok weight81_gate=ok
    SELFTEST dense_nonzero=0 status=ok
    END nodes=43196762 hits=0 capped=0 elapsed=30 targets=25 matches=5519232 completed=25
    RESULT n=91 contractions=48 lookups=3604 hash_matches=9720 exact_matches=9720 hits=48 proper_hits=48 elapsed=0s
    RESULT n=104 contractions=48 lookups=426864 hash_matches=0 exact_matches=0 hits=0 proper_hits=0 elapsed=0s
    RESULT n=208 contractions=50 lookups=112960308 hash_matches=1499136 exact_matches=1499136 hits=0 proper_hits=0 elapsed=2s
    INDEPENDENT PASS: positive control, negative control, target
    PASS

Positive control validation additionally checks 48 distinct proper rows, 24 of each sign, closure under negation, and exact scalar autocorrelations of all 48 rows at every lag. The independent checker binds contraction and exact-match counts for each run, not only the final hit count.

## Sanitizers

The original repair worker's UndefinedBehaviorSanitizer run completed all 25 targets with no diagnostics, elapsed=89.

The parent independently compiled the assembled package source with:

    cc -std=c11 -O1 -g -Wall -Wextra -Wpedantic -Werror -fsanitize=address,undefined -fno-sanitize-recover=all

The AddressSanitizer + UndefinedBehaviorSanitizer executable completed `all 180` with exit 0, no sanitizer diagnostics, and the same self-tests above:

    END nodes=43196762 hits=0 capped=0 elapsed=120 targets=25 matches=5519232 completed=25

## Negative-path verification

- Changed digit in object, duplicate contraction row, missing object: shell entrypoint rejected each with exit 1 and final FAIL.
- Three deliberate C regressions, each compiled separately in scratch storage and run with --selftest:
  - Restore stale dense buffer: exit 2, selftest reconstructed candidate.
  - Reverse required join sign: exit 2, selftest join identity/count.
  - Disable weight gate: exit 2, selftest inflated CW4 positive/weight.
- 24 malformed CLI argument cases: each exited 2.
- Real single-target search reported completed=1 and was rejected by the full-run summary validator.
- The 18 Python tests include each orchestration stage failing, timeout, cap, incomplete coverage, missing independent completion, bad contraction output, malformed/duplicate summary fields, process failure despite good-looking output, and actual shell-wrapper success/failure propagation in disposable fixtures.

Mock outputs inside regression tests are explicitly fixtures, not search evidence. The real search results above were obtained from executed C/Python enumerations.
