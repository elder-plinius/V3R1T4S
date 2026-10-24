# MOONSHOT - 4x4 matrices with 47 multiplications in characteristic 0, or 3x3 matrices with 22

⚡ **Algorithms** · moonshot (famous, long odds) · tractability ★☆☆☆☆ · compute: laptop-hours · open as of 2026-10-08

## The problem

Two headline open problems of small-format fast matrix multiplication. (a) <4,4,4>: AlphaTensor (2022) found rank 47 over GF(2) only; AlphaEvolve (May 2025) found 48 over C; Dumas-Pernet-Sedoglavic (2025, arXiv:2506.13242) gave 48 over any ring with 1/2, with a 'more accurate' rational variant in March 2026 (arXiv:2603.18699); the Lille catalogue lists 48 and matmulcatalog lists F2 47 / Z 49 / C 48. No rank-47 scheme is known in characteristic 0 (or in any characteristic other than 2), and no integer rank-48 scheme is known. (b) <3,3,3>: Laderman's 23 (1976) is unbeaten; the general lower bound is 19, and Sep 2026 preprints prove 21 over GF(2) (arXiv:2609.06725, arXiv:2609.18722); a 2026 Zenodo note (record 18514533, 'On the Tensor Rank of 3x3 Matrix Multiplication: Barriers and Open Problems') surveys the barriers. Epoch AI lists the rank of the 4x4 tensor as a FrontierMath open problem. Any rank-47 scheme for 4x4 valid over Q (or over GF(3)), or any rank-22 scheme for 3x3 over any field, would be a major result. Live check 2026-10-08: Lille 4x4x4.html lists <4,4,4>:48 (Dumas-Pernet-Sedoglavic variant of AlphaEvolve, raw scheme uses 1/2, 1/4, 1/8); 3x3x3.html lists <3,3,3>:23 (Laderman 1976); Perminov table 4x4x4: ZT 49 / Z 49 / Q 48 and 3x3x3: 23/23/23; matmulcatalog 4x4x4: F2 47 / R-Q-Z 49 / C 48.

## What counts as a win

Success means an explicit bilinear scheme, exactly verified over the claimed field, with EITHER (a) rank STRICTLY LESS (direction: min) than the rank listed on https://fmm.univ-lille.fr/4x4x4.html for <4,4,4> in a field of characteristic not equal to 2 (i.e. 47 or fewer over Q, Z or GF(p) with p odd; a scheme over Z/Q must be verified with exact integer/fraction arithmetic, a GF(p) scheme mod p), OR (b) rank STRICTLY LESS than the rank listed on https://fmm.univ-lille.fr/3x3x3.html for <3,3,3> over any field (22 or fewer, including GF(2)); with both pages, https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json, https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md and https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md re-fetched live immediately before claiming and none of them already listing an equal or lower rank in the claimed characteristic. A GF(2)-only rank-47 scheme for <4,4,4> does not count (AlphaTensor 2022). These two formats are excluded from fmm-catalogue-small-format-rank so a win is claimed once, here.

## Partial wins

- **p1:** A rank-48 scheme for <4,4,4> with all coefficients in Z (or in {-1,0,1}), exactly verified over Z, strictly below the live 'Z rank' / 'ZT rank' entries for 4x4x4 in https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md and absent from that repository's live schemes/results/Z and /ZT directories and from MerlijnW70's repository (this format is excluded from fmm-ternary-integer-ring-upgrade so it is counted only here).
- **p2:** A lifting milestone for 4x4: a rank-47 scheme for <4,4,4> exactly verified over Z/4Z (all Brent equations hold mod 4) where the live Lille page, Perminov's table and COVERAGE.md list no rank-47 scheme outside GF(2); the certificate is the scheme file plus the mod-4 check.
- **p3:** A machine-checked lower bound: a proof that no rank-22 scheme for <3,3,3> exists over GF(2) (i.e. rank >= 23 over GF(2), improving the published bound of 21 from arXiv:2609.06725 / 2609.18722), delivered as a SAT encoding plus DRAT/LRAT-checked UNSAT certificate or a Lean proof, with the encoding independently re-derived by the skeptic. Recorded as a result; claimed only after the 3-skeptic confirmation.

## How a win is checked

Load U, V, W (or the product list), verify the Brent equations exactly over the claimed field (integer/fraction arithmetic, or mod p), count rank-one terms. For the 4x4 claim, confirm the coefficients are meaningful in the stated characteristic (no 1/2 in an odd-characteristic claim unless reduced mod p; no 1/2 at all for Z). Re-fetch the two Lille pages, fmm_sota.json, Perminov's docs/ranks.md and COVERAGE.md. For p2 verify mod 4; for p3 re-run drat-trim/cake_lpr or lake build on the certificate. Minutes on this Mac (the DRAT check may take longer but must finish within an hour or the certificate is rejected as unverified).

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://fmm.univ-lille.fr/4x4x4.html>

## Sources

- <https://fmm.univ-lille.fr/4x4x4.html>
- <https://fmm.univ-lille.fr/3x3x3.html>
- <https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json>
- <https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md>
- <https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md>
- <https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md>
- <https://arxiv.org/abs/2506.13242>
- <https://arxiv.org/abs/2603.18699>
- <https://arxiv.org/abs/2609.06725>
- <https://arxiv.org/abs/2512.21980>
- <https://arxiv.org/abs/2601.05272>
- <https://epoch.ai/frontiermath/open-problems/matrix-multiplication>
- <https://zenodo.org/records/18514533>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Lift the GF(2) rank-47 AlphaTensor scheme: treat it as a solution mod 2 and attempt Hensel lifting to Z/4, Z/8 ... with the linearised Brent system; an obstruction at the first step is informative, a successful lift to Z/2^k plus rational reconstruction would be the result.
- Flip-graph walks from the rank-48 schemes (Dumas et al. rational variant, AlphaEvolve C variant, and the Z/ZT 49s) over GF(3) and GF(5) looking for a 47 in odd characteristic, then lift.
- Symmetric ansatz: impose the Z3 cyclic symmetry (A->B->C) or the (4x4) isotropy subgroups used in Flip Graphs with Symmetry, reducing 4x4x4 rank-47 to a much smaller polynomial system; try Groebner/SAT on the reduced system over GF(3).
- For 3x3x3 rank 22 over GF(2): a SAT encoding with full symmetry breaking is large but the Sep 2026 lower-bound-21 papers give structure (which orbits are forced); use their invariants to prune and run a bounded search for 22 over GF(2) rather than Q.
- Addition-count side (p3): run Perminov's ternary_addition_reducer and plinopt on the ZT rank-23 scheme with randomized common-subexpression elimination to try to beat the listed count.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Rank 47 over GF(2) is known (AlphaTensor 2022) and rank 48 with 1/2 is known; re-deriving either is not a win. Verify the characteristic claim exactly.
- Border rank 47 or numerically approximate decompositions (residual 1e-6) are not rank; floating-point ALS output needs exact rounding and re-verification.
- Lower bounds: 19 for 3x3 general and 21 over GF(2) (Sep 2026); claims of rank 20 or less over GF(2) contradict proven bounds and indicate a checker bug.
- Addition-count improvements for 3x3x3:23 or 4x4x4:48 are the fmm-additive-complexity-records target, not a partial win here.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/algorithms/fmm-4x4x4-rank47-3x3x3-rank22.md
```

Already set up? Say `run V3R1T4S on fmm-4x4x4-rank47-3x3x3-rank22`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `fmm-4x4x4-rank47-3x3x3-rank22`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
