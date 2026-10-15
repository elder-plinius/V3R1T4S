# RECEIPTS: real output of `sh verify-it-yourself/run_checks.sh` from a clean copy of this package

Run at 2026-10-14T22:22:19Z (macOS, Python 3.9, curl); exit status follows the output.

```
breakdown: risk=58939, ret=-825237, trans=75179, cash=-1040, short=535, liq=0
feasible: True
objective = -691624 (expected -691624; bar -551385)
PASS
binary x variables set: 450
constraints c2/c3 hold in every period: True
objective (literal ZIMPL evaluation) = -691624
both evaluators: feasible, objective -691624 < bar -551385
PASS
exit status: 0
```

## Corrupted-object test (run by the claimant on a copy of this package, 2026-10-14T22:23:22Z)

kit/check_run.py skips this test because `.sol` is not in its text-extension list, so it was run by hand with
the same rule (change the middle digit of the object file):

```
changed one digit (the same rule check_run.py uses): line '4 RTX 3 0' -> '4 RTX 1 0'
objective (literal ZIMPL evaluation) = -659384
check_portfolio exit 1, literal evaluator exit 0 value -659384
FAIL
exit status: 1
```
