# Brief & Preregistration (`three-heap-wythoff-fraenkel-a1-11`)

- Frozen UTC: `2026-11-16T02:56:00Z`
- `null_test: not needed because this is an explicit finite mathematical proof certificate checked deterministically from exact combinatorial game rules and published Table 1 values`

## Criterion (Verbatim)

CONFIRMED: both of Fraenkel's conjectures for N = 3 with smallest heap A1 = 11 (or any larger single value, once 11 is done). The proof gives explicit integers n2 < n1 and the derived constants (T, S, alpha, N1, N2, N3 and the set S1(n1) of Claim 3.3) satisfying every hypothesis of Sun and Zeilberger's Claims 3.4 and 3.5. Their Table 1 supplies T, S, alpha, N1 and N2 for the cases i < 11 but not N3, so the claim must also state N3^i and B^i_{N3^i} for every i < 11, recomputed. A program that shares no code with the claimant's must check this by recomputing the P-positions directly from the game rules. A general proof for all A1, formalised in Lean 4, Coq or Isabelle, also counts. The case must not be published as proved at verification time (GONC Unsolved Problems column, arXiv, journals citing Sun-Zeilberger).

## Deterministic Referee Gate

`verify-it-yourself/verify_wythoff.py` (stdlib Python, zero shared code with `code/fraenkel_wythoff.c`) must recompute `P^m` (`0 <= m <= 11`) from Fraenkel's move rules, cross-check against 3D brute-force move search, verify all 11 rows of Sun & Zeilberger Table 1 (`p1`), verify all hypotheses of Claims 3.3, 3.4, 3.5, and Lemma 2.4 for `m = 1..11`, and print `PASS` (while rejecting a digit-corrupted copy of `object/wythoff_a1_11_certificate.json` with `FAIL`).
