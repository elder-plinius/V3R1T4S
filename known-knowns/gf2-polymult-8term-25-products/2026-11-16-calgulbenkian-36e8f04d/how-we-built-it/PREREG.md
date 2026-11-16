# Pre-Registration: gf2-polymult-8term-25-products

frozen_utc: 2026-11-15T14:24:30Z
target_id: gf2-polymult-8term-25-products
null_test: not needed because exact algebraic/circuit certificate

## Exact Acceptance Rules Frozen Before Solver Execution
1. **Main Win (`solution_claim`)**:
   - Explicit binary `0/1` matrices `U (r x 8)`, `V (r x 8)`, `W (15 x r)` with `r <= 25` such that `sum_t U[t][i] V[t][j] W[k][t] mod 2 == [i + j == k]` for all `0 <= i, j <= 7` and `0 <= k <= 14` (all 960 tensor equations over `GF(2)`), AND verified end-to-end as a `{AND, XOR}` circuit on all `65536` pairs of 8-bit binary polynomials against schoolbook carry-less multiplication.
2. **Partial Win `p1` (`partial_win_claim`)**:
   - Explicit 2-input `{AND, XOR, XNOR}` straight-line circuit (no constants, no NOT, no wire used before definition or redefined) for multiplication in `GF(2^8)` modulo `x^8 + x^4 + x^3 + x + 1` (`0x11B`), standard polynomial basis in (`A0..A7`, `B0..B7`) and out (`C0..C7`), exhaustively verified on all `65536` input pairs, with **total gates <= 106** (strictly below NIST's 117 AND Swapnil Jain's Oct 2026 preprint record of 107).
3. **Partial Win `p2` (`partial_win_claim`)**:
   - Same exact `{AND, XOR, XNOR}` 2-input gate model and standard polynomial basis, exhaustively verified on all `2^(2m)` input pairs (`4096` for `m = 6`, `16384` for `m = 7`), achieving AT LEAST ONE of:
     - `GF(2^6)` modulo `x^6 + x^3 + 1` (`0x49`) with **total gates <= 56** (strictly below NIST's 57 AND Swapnil Jain's 57);
     - `GF(2^7)` modulo `x^7 + x^4 + 1` (`0x91`) with **total gates <= 83** (strictly below NIST's 84 AND Swapnil Jain's 87);
     - `GF(2^7)` modulo `x^7 + x^3 + 1` (`0x89`) with **total gates <= 82** (strictly below NIST's 85 AND Swapnil Jain's 83).
4. **Verification Gate**:
   - Standalone Python 3 stdlib checker calibrated on NIST's four `data/*.slp` circuits (`57, 84, 85, 117` gates), printing `PASS` as its exact final line on valid objects and `FAIL` (exit code 1) when 1 digit of the object is mutated.
