# Claim (partial win p4 of bank target mertens-smallest-counterexample-upper-bound)

**One sentence.** With separately written python-flint/Arb ball-arithmetic code, the K_2 sum of the bzyzz/mertens_bound
certificate at v = 3484971332733132396.5383341489440461, k = 1.5e-10, over all 2,325,572 zeta zeros with
0 < gamma < T0 = 1.3e6 (zeros and their indexing from Arb's acb_dirichlet_zeta_zeros, the same routine the certificate
uses) is enclosed in K2 = [1.00030525038651 +- 5.07e-15] (result/aggregate_claim.json; 128-bit balls for n <= 600,000,
96-bit for n > 600,000). This ball lies inside the certificate's stated K2 = [1.0003052504 +- 2.30e-11], and its lower
end exceeds 1 + E by 3.0525e-4, where E = 2.391e-11 is the certificate's own error bound (bzyzz THEOREM.md, taken from
the certificate and NOT checked here). The part over 600,000 < n <= 2,325,572, which the certificate only bounds by
[+- 9.43e-12], evaluates to [1.3e-14 +- 9.56e-16]; our n <= 600,000 part [1.00030525038650 +- 4.03e-15] overlaps the
certificate's K2_main [1.000305250386499012059 +- 3.21e-22]. This confirms the certificate's K_2 inequality K2 > 1 + E
at its stated E, and finds no error in the K_2 sum.

status label: NUMERICAL (rigorous ball-arithmetic computation, assuming FLINT/Arb is correct; the bzyzz criterion and
its error bound E remain unreviewed).

## Independence caveat
The code (code/k2_chunks.py, code/aggregate_claim.py) is written separately from the certificate's certify_K2.py and
certio.py. The zeros are not from an independent source: both use FLINT/Arb's acb_dirichlet_zeta_zeros
(python-flint acb.zeta_zeros), and N(T0) = 2,325,572 rests on that routine's rigorous indexing. Panel evidence
(panel/reproduce.md): the REPRODUCE skeptic's own code (exact rational k and v, 160/128/96 bits) counted
arb(1300000).zeta_nzeros() = 2325572 independently of the index enumeration and obtained
K2 = [1.00030525038651186516826 +- 3.73e-24], inside the ball above.

target id: mertens-smallest-counterexample-upper-bound
partial win claimed: p4, first option only ("the ball-arithmetic K_2 sum at its point over all zeros below 1.3e6").

## p4 (verbatim from bank/targets.json)
An independent check of the bzyzz/mertens_bound certificate, done with separately written code: either the ball-arithmetic K_2 sum at its point over all zeros below 1.3e6, or a numerical re-derivation of its error terms J1..J6 and the 1/zeta bound. The result either confirms it or documents a concrete error.

## Success criterion of the target (verbatim, for context; NOT claimed)
Success means a real y (or v), given exactly, evaluated in rigorous ball arithmetic over the complete zero list below the stated cutoff, that meets one of three criteria. The first is |h_StR(y)| > 1 + 6e-8 (Saouter-te Riele's published parameters). The second is |h_P(y)| > 1 + e^-40 with y in [e^7, e^50000] (Pintz). The third is the bzyzz/mertens_bound criterion at its stated (k, T0, T1) with its error bound E. The claim also gives the resulting bound B on the smallest counterexample, computed by the formula that goes with the criterion used. B must be STRICTLY SMALLER (direction: min) than exp(3484971332733178124), the smallest public claim on 2026-10-30. A claim that uses the bzyzz criterion inherits its unreviewed status and must say so. A claim that uses a new kernel or new error terms gives the full derivation, and the skeptic checks every inequality numerically. A refinement (Saouter-te Riele Lemma E, the |M(x +- n)| argument) counts only when compared with the same refinement applied to the record point. The skeptic re-evaluates h at y with independently computed zeros and re-checks the theorem's hypotheses (range of y, error margin). Before claiming, re-check arXiv, the Wikipedia page and the bzyzz/mertens_bound README for a newer record, and beat it.

## Definitions used
rho = 1/2 + i gamma (gamma > 0), K2(v) = 2 * sum_{0<gamma<T0} exp(-k gamma^2) * Re( exp(i gamma v) / (rho zeta'(rho)) ),
k = 1.5e-10, T0 = 1.3e6, v as above (inputs/bzyzz_k2_certificate.json: params k, v, T0; inputs/bzyzz_README.md).

## Precision note
chunks_head128/ (128 bits, used by default) gives the tight ball above. chunks_head/ is a 96-bit run of the same range;
its ball [1.0003 +- 1.68e-5] (result/aggregate_claim_head96.json, from `python code/aggregate_claim.py chunks_head`) is
wide because the 96-bit zero error times v ~ 3.5e18 enters the phase, but it also contains the certificate's value.
All chunk sums in this package were computed by this run's code (code/k2_chunks.py).

## Not claimed
- No new bound on the first Mertens counterexample. No p1, p2 or p3 (run's lattice search found no y below Kim-Nguyen's y).
- This does not make the bzyzz / Bi-Hou bound reviewed: Pintz Theorem A / Corollary A as used (Y = e^u), Pintz
  Lemmas 4-5 constants, the re-derived error terms J1..J6 (hence E) and the 1/zeta constant M = 22.767 (needs ~6.2M
  zeros on [1.3e6, 4.3e6]) are not checked here.
- Nothing about Kim-Nguyen's tables (that is a separate, earlier submission).

## Files
- code/k2_chunks.py: per-chunk sums by zero index, at the precision given by its PREC argument (128 for chunks_head128,
  96 for chunks_head and chunks_tail); code/aggregate_claim.py: the checker (overlap and containment tests).
- chunks_head128/ (n = 1..600,000, 128 bits; 1,500 files), chunks_head/ (same range, 96 bits) and chunks_tail/ (n = 600,001..2,325,573; 4,314 files): saved chunk sums.
- result/aggregate_claim.json (default, head128) and result/aggregate_claim_head96.json: checker outputs. inputs/: the bzyzz certificate files as fetched (status in status_source.md).

## Credits
- Zhenyu Bi and Enze Hou: the certificate checked here, https://github.com/bzyzz/mertens_bound (commit a0b267c2) and
  HAL hal-05838582, https://hal.science/hal-05838582 . E = 2.391e-11 is from their THEOREM.md
  (https://github.com/bzyzz/mertens_bound/blob/a0b267c2c7ff32a917732cf16ee860d705ca4a08/THEOREM.md).
- Leandro Hector Gallego, https://doi.org/10.5281/zenodo.23700211 : an independent claim, also about exp(3.485e18), at a
  different (k, y, T0) (k = 5.7e-12, T0 = 7,999,035.172); his exponent is 36,813.58 lower than bzyzz's. Not assessed.
- Seungki Kim and Phong Q. Nguyen, https://arxiv.org/abs/2502.21021 : peer-reviewed record exp(1.96e19).
- J. Pintz, "An effective disproof of the Mertens conjecture", Asterisque 147-148 (1987) 325-333,
  https://www.numdam.org/item/AST_1987__147-148__325_0/ : the criterion.
- Y. Saouter and H. te Riele, "Improved results on the Mertens conjecture", Math. Comp. 83 (2014) 421-433,
  https://doi.org/10.1090/S0025-5718-2013-02716-0 : the K_2 framework and error terms.
- FLINT/Arb (Fredrik Johansson and the FLINT team), https://flintlib.org , and python-flint,
  https://github.com/flintlib/python-flint : zeros and ball arithmetic.
