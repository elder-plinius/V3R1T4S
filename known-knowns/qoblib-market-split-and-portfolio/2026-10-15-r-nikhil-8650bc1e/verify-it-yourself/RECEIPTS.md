# RECEIPTS: real output of `sh verify-it-yourself/run_checks.sh` from a clean copy of this package

Run at 2026-10-15T09:12:13Z (macOS, Python 3.9, curl); output copied verbatim.

```
$ sh verify-it-yourself/run_checks.sh
(run 2026-10-15T09:12:13Z, from a clean copy of the package)
breakdown: risk=63057, ret=-784113, trans=76812, cash=-640, short=542, liq=0
feasible: True
objective = -644342 (expected -644342; bar -401535)
PASS
binary x variables set: 450
constraints c2/c3 hold in every period: True
objective (literal ZIMPL evaluation) = -644342
both evaluators: feasible, objective -644342 < bar -401535
PASS
```
