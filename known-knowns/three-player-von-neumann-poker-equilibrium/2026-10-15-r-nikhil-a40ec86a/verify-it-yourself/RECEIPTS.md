# RECEIPTS: real output of `sh verify-it-yourself/run_checks.sh` from this package folder

Output captured from a run that finished shortly before Thu Oct 15 19:54:02 UTC 2026 (file written then), with Python 3.9.6 (standard library only).

```
== exact_certificate (exit 0): PASS: exact b=2 equilibrium certificate; printed decimal criterion is FALSE
== universal_check (exit 0): PASS: universal exact polynomial certificate
== ordered_cone_check (exit 0): PASS: exact nonnegative-gap polynomial certificates for all 12 raw payoff regions
== finite_calibration (exit 0): PASS: exact finite calibrations and deliberately exploitable profile
== independent_check (exit 0): PASS
PASS
```

Corruption tests (one digit changed, then the script rerun from a copy of the package):
- object/universal.json, middle digit (the rule kit/check_run.py uses): FAIL, as it should.
- object/raw_payoffs.txt, middle digit: FAIL, as it should.
- object/equilibrium.json, first long integer, digit incremented: FAIL (checked while staging).
- object/equilibrium.json, middle digit: PASS. That digit sits in the upper endpoint of C's rational isolating
  interval; the change widens the interval from about 1e-65 to about 3.2e-59, which still isolates the same root, so
  the altered file is still a valid certificate. The checkers verify properties, not bytes.
- object/all_b_proof.md and object/proof.md are the written proofs; no program checks their prose. kit/check_run.py's
  one-digit test lands in all_b_proof.md (the first object file) and therefore reports a warning, not a failure.
