# CHANGES after the panel (wording only; no number changed)

Applied after panel/gate.md (2026-11-25T08:01:55Z), from panel/criterion.md fixes 1-6 and panel/novelty.md section 3:
1. CLAIM.md: same-Arb caveat (zeros and indexing from acb_dirichlet_zeta_zeros, as in the certificate), also in status_source.md.
2. CLAIM.md: E = 2.391e-11 cited as the certificate's own, unchecked value (bzyzz THEOREM.md); closing sentence now
   "confirms the certificate's K_2 inequality K2 > 1 + E at its stated E, and finds no error in the K_2 sum".
3. CLAIM.md: removed the unevidenced "J1..J6 numerically reproduced in an earlier run" remark.
4. CLAIM.md Files section and code/k2_chunks.py docstring: precision given by PREC (128 head128, 96 head/tail).
5. CLAIM.md: status label NUMERICAL.
6. code/aggregate_claim.py: adds "contained_in_bzyzz_K2" (arb containment); result JSONs regenerated; all other fields
   byte-identical to the panelled version. E line commented with its source.
7. CLAIM.md credits: Gallego wording (different k, y, T0; exponent 36,813.58 lower, per panel/novelty.md), links for
   Pintz (Numdam), Saouter-te Riele (Math. Comp. DOI), FLINT/Arb and python-flint, bzyzz THEOREM.md.
8. CLAIM.md: cites the REPRODUCE skeptic's zeta_nzeros count and its ball [1.00030525038651186516826 +- 3.73e-24] as panel evidence.
