# Verification Receipts (`verify-it-yourself/RECEIPTS.md`)

Command executed:
```sh
sh verify-it-yourself/run_checks.sh
```

Output:
```text
== running check_lychrel.py on object/kuitche_2023_audit.json ==
=== V3R1T4S Mechanical Verifier: Kuitche (2023) Audit (p2, Bases 3..10) ===
[1/3] File integrity verified for object/kuitche_2023_audit.json.
[2/3] Baseline reproduction PASSED: David Seal Base 26 (Period 4, 8 symbolic blocks, brute-forced m=1..500).
[3/3] Kuitche (2023) mechanical audit PASSED across all bases b=3..10 (explicit failure instances verified for all b in {3,5,6,7,9,10}).
ALL CHECKS PASSED in 0.09s.
== negative control: a corrupted copy must FAIL ==
negative control rejected as expected (AssertionError: SHA-256 mismatch on kuitche_2023_audit.json: got 15dc4783b657d91efa19535a925647d4b43c5de9ca8e38c492d36dbfcfd64e14, expected 918d070676a95905173766663baef89c576b2f22d135cc7eacc7dd691f596736)
ALL CHECKS PASS
```
