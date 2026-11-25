# Pre-registration

UTC 2026-11-25T07:13:30Z

## Verbatim success criterion

CONFIRMED: both of Fraenkel's conjectures for N = 3 with smallest heap A1 = 11 (or any larger single value, once 11 is done). The proof gives explicit integers n2 < n1 and the derived constants (T, S, alpha, N1, N2, N3 and the set S1(n1) of Claim 3.3) satisfying every hypothesis of Sun and Zeilberger's Claims 3.4 and 3.5. Their Table 1 supplies T, S, alpha, N1 and N2 for the cases i < 11 but not N3, so the claim must also state N3^i and B^i_{N3^i} for every i < 11, recomputed. A program that shares no code with the claimant's must check this by recomputing the P-positions directly from the game rules. A general proof for all A1, formalised in Lean 4, Coq or Isabelle, also counts. The case must not be published as proved at verification time (GONC Unsolved Problems column, arXiv, journals citing Sun-Zeilberger).

## Verification specification and frozen thresholds

1. Reproduce all P-positions $(m, Y, Z)$ with $0 \le m \le Y \le Z \le 12000$ using two independent C++20 solvers (`reverse.cpp` predecessor marking and `direct.cpp` row-by-row gap evaluation), requiring byte-for-byte identity across all 59,483 positions.
2. Independently recompute P-positions from the literal move rules in pure Python (`verify_wythoff.py`) cross-checked against 3D brute-force search on $0 \le p_1 \le 12, p_3 \le 55$.
3. Verify exact agreement with all 11 rows ($m = 0..10$) of Sun & Zeilberger Table 1 (`T`, `S`, `alpha`, `N1`, `N2`) and recompute exact `N3^i`, `B^i_{N3^i}`, `B^i_{N3^i+1}` for all $0 \le i \le 11$.
4. For every layer $1 \le m \le 12$ (and specifically $m = 11$ with $n_2 = 1990, n_1 = 3249, \alpha = -61$ and target $m = 12$ with $n_2 = 601, n_1 = 1762, \alpha = -67$), verify:
   - All hypotheses of Claims 3.3 (modulo-$p(m)$ ray witnesses across $[Y_{n_1}, Y_{n_1} + p(m)]$), 3.4, and 3.5 (with $\alpha' = \lfloor (\max + \min)/2 \rfloor$).
   - All hypotheses of the self-contained direct induction proof (`PROOF.md`: Lemma 2.6 history/anchor bounds, `small_two_max` bounds, Beatty-floor `offset_slack` strict separation / adjacent-layer zero-slack guard, and full mex completeness).
   - Strict certificate integrity: every field of `wythoff_a1_12_certificate.json` matches recomputed values, and a 1-digit mutation causes `FAIL`.

null_test: not needed because an explicit finite certificate and P-position table are checked deterministically against exact game rules and algebraic induction inequalities
