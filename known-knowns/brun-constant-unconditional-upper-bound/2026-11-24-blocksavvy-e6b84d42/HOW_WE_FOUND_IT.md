# How we found it (contributor text, unverified)

- Starting point: our own earlier GRH package (2026-11-23-blocksavvy-a26bba47, B < 2.156967, draft PR #1231). In Dunn's
  sum, the dominant cost in most intervals is the sieve error term c_pi c2 r(z)^2, where r(z) ~ 0.405 z counts odd
  squarefree d <= z because Dunn (via Klyve Theorem 5.7) uses |lambda_d| <= 1.
- Prerun (frozen PREREG): does using the explicit Selberg weights instead of |lambda_d| <= 1 tighten the bound?
  Null test: Klyve's own weight formula ((5.24)-(5.26)) summed in exact rationals for z <= 2000 equals W(z)/V(z) exactly,
  which led to the identity sum |lambda_d| = W(z)/V(z) and to the W lemma W(z) <= z/(2 C2) + z^s S'(s).
- Result: exact fixed-point W tables to 1e10 (ceil, 2^40) next to the V tables (floor, 2^64), the W lemma beyond,
  re-optimised z_i, and arb balls give B <= 2.12698720 (program) / 2.12698717 (standalone checker).
  Controls: weights off reproduces the earlier 2.15696694; the weights on Dunn's original inputs give 2.1282623.
- What failed: an unconditional version of the same idea (float probe 2.3212 > 2.288513) is dead.
  A per-modulus combination rho_q = sum_{[d1,d2]=q} lambda lambda gives about 2.12574 rigorously in our code, but it has no
  standalone checker and was not panelled, so it is not in this package.
- Panel: three fresh subagent contexts saw only the claim folder. REPRODUCE rebuilt the tables and certificate and passed;
  NOVELTY found no GRH bound below 2.1594 and treats the |lambda| bound as classical (Vaughan's notes), applied here to
  Brun's constant for the first time as far as the sources opened show; CRITERION judged p1 met, conditional only.
  The panel's wording fixes are applied as documented errata (how-we-built-it/CLAIM_CHANGES.md); the checker was made
  two-sided and runs at 128 and 256 bits. One panel remark ((d), that the program value omits the pi_2(z) correction)
  was checked and does not hold: removing the addend lowers the sum by exactly the 3.509e-15 correction.
