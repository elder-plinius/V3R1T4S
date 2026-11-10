# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder on 2026-10-19 (python3, standard library only). Wall time 5 s on the packager's machine.

Differences from the copy of this folder that the panel ran: the table files are read from `the-record-we-beat/` (the panel folder called it `table-record/`), the last output line is `PASS` instead of `ALL CHECKS PASS`. The checkers themselves are unchanged.

```
sha256 of object matches INDEX.csv (686fb617c1dafe37759247e164ed246cd4ed1c572ea548b8dce8d8abbe450422)
== qecc_check.py (exact stabilizer-code check, d = 5, comparison with live bounds and neighbours)
A (weight distribution of S) = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 315, 0, 1980, 0, 4809, 0, 5937, 0, 3051, 0, 282, 0]
B_j - A_j for j <= d: [(1, 0), (2, 0), (3, 0), (4, 0), (5, 549)]
direct count of normalizer elements outside S by weight 1..d: {1: 0, 2: 0, 3: 0, 4: 0, 5: 549}
{"n": 23, "k": 9, "rank": 14, "self_orthogonal": true, "d": 5, "claimed_d": 5, "consistent": true, "VALID": true}
PASS exact d=5; live lower=4 (d > lower: True); live upper=6 (d <= upper: True); best lower bound implied by live neighbours = 4 (< claimed 5: True)
== negative control: one X bit of generator 1 flipped (must fail self-orthogonality or change the distance) (must be rejected)
PASS (negative control rejected)
PASS
```
