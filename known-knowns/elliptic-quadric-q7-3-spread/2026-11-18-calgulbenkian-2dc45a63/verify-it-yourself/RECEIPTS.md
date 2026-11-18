# Verification Receipts

Real captured output from a clean run of `sh verify-it-yourself/run_checks.sh` (exit code `0`):

```text
[Python Checker] 1. Q^-(5,3) 28-line order-3 spread certificate verified.
[Python Checker] 2. All 5 Order-3 matrices, KM dimensions, and class sum (430,408,160) verified.
[Python Checker] 3. All 5 PO^-(8,3) involution classes and total count (41,398,479) verified.
[Python Checker] 4. All 4 odd prime Sylow-{5,7,13,41} exclusions verified by arithmetic & KM dimensions.
[Engine 2 C99] 1. Q^-(5,3) positive control (28-line spread invariant under order 3) -> PASS
[Engine 2 C99] 2. |Aut(Q^-(7,3))| = |PGO^-(8,3)| = 40,607,874,478,080 (frame stab = 64) -> PASS
[Engine 2 C99] 3. Constructive Order-3 completeness (59696+537264+42981120+193415040+193415040 = 430408160) -> PASS
[Engine 2 C99] 4. C3_94, C3_121, C3_4, C3_22 + all 5 PO^- involutions + all 4 Sylow-{5,7,13,41} -> ALL EXACT UNSAT
[Engine 2 C99] 5. C3_13 exhaustive Row-DLX -> EXACT UNSAT (143 tasks, 8776899 branches, 52.26s) -> PASS
ENGINE2_OK
[Verified in 56.51s] No spread of Q^-(7,3) admits an automorphism of order 3 (and Aut(S) cap PO^-(8,3) = {1}).
PASS
```
