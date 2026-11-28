# PREREG — 2026-10-29T21:11:15Z

## Target and Pre-Registration

- Target: `selection-min-comparisons-n16-n17`
- Frozen at: 2026-10-29T21:11:15Z

## Criteria Verbatim

### Full Win (CONFIRMED_SOLUTION)
Success means an explicit comparison-selection algorithm for one cell (n, i) in {(16, 8), (17, 6), (17, 7), (17, 8), (17, 9)} (1-based rank i; the mirror rank n+1-i is the same cell), written as a decision graph in the Rust certificate format of Cremer's repository and of the Dörrer et al. search code (functions that compare two arguments, discard arguments that cannot be the answer, call another function on the remaining arguments, or return an element), or in a format converted losslessly into it, whose worst-case number of comparisons is STRICTLY LESS (direction: min) than the best upper bound for that cell on the status sources re-fetched at verification time (on 2026-10-25: V8(16) <= 29, V6(17) <= 29, V7(17) <= 30, V8(17) <= 31, V9(17) <= 31, all from Cremer arXiv:2610.18740v1) and than any lower value in a newer arXiv version or in any paper citing it. The certificate must be accepted, with the claimed worst case, by (1) Cremer's static checker (python3 -I code/verifier/verify_rs_algorithm.py CERT.rs --expect-n N --expect-i I --expect-worst W, where --expect-i is 1-based) and (2) a second checker written from the definition without Cremer's code. A reported worst case below the proven lower bound (V8(16) >= 28; V6(17) >= 28; V7(17), V8(17), V9(17) >= 29) means a checker or parser bug, not a record. A 28-comparison certificate for the 8th smallest of 16 settles V8(16) = 28 and is the headline result; a certificate meeting the lower bound for an n = 17 cell settles that cell.

### Partial Wins
- **p1:** A raised lower bound for one of the open cells (V8(16) >= 29; V6(17) >= 29; V7(17), V8(17) or V9(17) >= 30) established either by a proof object accepted by a formally verified checker (for example a Lean 4 proof, or a DRAT/LRAT/VeriPB proof of an encoding whose correctness is argued in a short note), or by two independently written exhaustive searches (for example a forward minimax search and a backward search, as Dörrer et al. did) that complete with the same answer and whose runs a skeptic can repeat on comparable hardware; the second route is labelled computational, not certified.
- **p2:** An explicit certificate for a cell (18, i) with 5 <= i <= 9 whose worst case is strictly below the Hadian-Sobel bound n - i + (i - 1) * ceil(log2(n + 2 - i)) and below every value for that cell in Gasarch-Kelly-Pugh 1996 Table 3 and later sources (a claimant must locate and read that table), verified by the same two checkers.

## Verification Checkers and Thresholds
1. **Cremer Static Checker**:
   `python3 -I code/verifier/verify_rs_algorithm.py CERT.rs --expect-n N --expect-i I --expect-worst W`
   Must output `ACCEPT` and verify that no path exceeds $W$ comparisons, with 1-based rank $I$.
2. **Independent Path Checker**:
   `python3 -I code/independent_checks/checker/pathcheck.py CERT.rs`
   Must verify exact reachability, absence of cycles, and `exact_worst <= W`.

## Null Test Designation
null_test: not needed because explicit decision graphs checked by deterministic mathematical static verifiers against proven combinatorial bounds
