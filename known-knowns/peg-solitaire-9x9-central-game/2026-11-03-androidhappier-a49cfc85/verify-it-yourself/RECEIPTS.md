# Receipts: real output of run_checks.sh

Command, from the package folder: `sh verify-it-yourself/run_checks.sh` (exit status 0).
Run on 2026-11-03 (Linux, python3 3.13.5, cc (Debian 14.2.0-19) 14.2.0).

```
== 1. object/sol31.txt sha256 vs INDEX.csv
INDEX sha256  a49cfc85ce7d20bd828fd9f168fd3beea6d4bfb0fbe90df350944a85bd60093a
file sha256   a49cfc85ce7d20bd828fd9f168fd3beea6d4bfb0fbe90df350944a85bd60093a
sha256 ok; INDEX value = 31
== 2. Python checker (written from the definition) on the object: expect VALID, 31 moves, 79 jumps
jumps=79 moves=31 pegs_left=1 final=e5
VALID central game e5->e5 in 31 moves
== 3. object/VALUE.txt agrees with the checker, and every file matches SHA256SUMS
SHA256SUMS: 26 files checked, all ok
== 4. negative fixtures must be rejected
neg_diag: rejected ok (ILLEGAL jump 1 (line 1) c3-e5: not an orthogonal distance-2 jump)
neg_occupied: rejected ok (ILLEGAL jump 2 e5-e3: no peg jumped over)
neg_sol31_swapped: rejected ok (ILLEGAL jump 4 e1-e3: no peg jumped over)
neg_sol31_truncated: rejected ok (INVALID: final position is not a single peg at e5)
neg_unfinished: rejected ok (INVALID: final position is not a single peg at e5)
== 5. positive calibration fixture (34 moves, ties Maye; not a win) must be VALID 34
jumps=79 moves=34 pegs_left=1 final=e5
VALID central game e5->e5 in 34 moves
== 6. independent C replay checker (optional)
jumps=79 moves=31 left=1 centre=1
PASS
replay9 rejects neg_diag ok
summary: 9x9 (81-hole square board) central game e5->e5, orthogonal jumps, 79 jumps / 31 moves
PASS
```
