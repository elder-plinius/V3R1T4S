null_test: required
frozen_utc: Wed Nov 25 00:46:15 UTC 2026 (date -u, written before any zero computation, K2 evaluation or lattice run of this run)

# PREREG: Mertens first-counterexample bound, follow-up run (bank id mertens-smallest-counterexample-upper-bound)

Prior run runs/2026-11-24-0728 (PR #1234) claimed only p1 (Kim-Nguyen table re-evaluation). This run does NOT
re-claim p1 and makes no statement about Kim-Nguyen's tables. Its objects are p4 (bzyzz certificate check) and p3
(a new y below y_KN). Reused from 0728, by reference and sha256: certified zeros n <= 98,625 (256 bits), the
certified h_StR pipeline (lib/), the bzyzz K2 chunk files for n = 98,626..600,000 (128 bits).

## Definitions (frozen)
rho = 1/2 + i*gamma, zeros indexed by FLINT acb.zeta_zeros (rigorous isolation by index, python-flint 0.9.0).
bzyzz point: v = 3484971332733132396.5383341489440461, k = 1.5e-10, T0 = 1.3e6 (github.com/bzyzz/mertens_bound).
K2(v) = 2 * sum_{0 < gamma < T0} exp(-k gamma^2) * Re( exp(i gamma v) / (rho zeta'(rho)) ).
(Same formula as 0728's code, which matched bzyzz's 'K2_main_(n<=600000)' to 7.8e-15.)
h_StR(y) = 2 * sum_{0 < gamma < 74000} exp(-3e-9 gamma^2) * Re( exp(i gamma y) / (rho zeta'(rho)) ).

## Lens k2tail (p4)
Compute: zeros n = 600,001..2,325,573 with zeta'(rho) in arb at 96 bits (balls; precision loss only widens balls),
chunked, resumable, by index; completeness: gamma_{2,325,572} < 1.3e6 < gamma_{2,325,573} from certified balls.
Statistic: K2_full = (0728 certified K2 over n <= 600,000) + 2 * sum over n = 600,001..2,325,572, as an arb ball.
If time allows, a second, independent recomputation of n = 1..600,000 at 96 bits in this run's code, which must
overlap 0728's ball.
Outcomes (frozen):
- CONFIRMS-NUMERICS: K2_full ball overlaps bzyzz's stated full K2 (1.0003052504 +- 2.3e-11, read from their repo
  certificate) AND lower(K2_full) - E > 1 with E = 2.391e-11 (their error bound, reproduced in 0728 as 2.3907931e-11).
  This meets p4's literal option "the ball-arithmetic K_2 sum at its point over all zeros below 1.3e6".
- DOCUMENTED ERROR: K2_full ball disjoint from bzyzz's stated value, or the zero count/boundary differs.
- NOT COMPLETED: any index gap.
Scope ceiling: the p4 check covers the K2 numerics only; Pintz Theorem A reading, Pintz Lemma 4-5 constants and
the 1/zeta constant M are NOT re-derived here and stay "unchecked". A p4 claim must say so, and that the bzyzz
bound remains unreviewed.

## Lens lattice2 (p3)
Hit (frozen, same as 0728): exact decimal y < 19571878850562201959.215107 (strict), certified
lower(|h_StR(y)|) > 1 + 6e-8 over the complete zero list gamma < 74000 (98,625 zeros), at prec 256 and 320, both
must agree. Bound comparison: exp(y + sqrt(y)) vs exp(y_KN + sqrt(y_KN)), same formula both sides, no Lemma E.
Method: lattice settings NOT covered in 0728 (larger N, e.g. 160; new random targets / sign mixing; radius 1.25+),
fpylll BKZ + the 0728 C pruned enumerator, float screen, then the frozen 0728 pipeline (polish +-1e-3, round to 12
decimals, certified sum).
Null test (frozen design): 400 controls, y uniform from [1e18, 1.957e19] with NEW seed 20261125, same pipeline.
Real hit must beat every control. Checker positive control y_KN (must certify), negative control y_KN + 0.5.

## Status ceiling
Single context: at most PROMISING. No gate.md in this run session; claim/ is built for a fresh-context panel.

## Budget
Box CPU only, $0, nice 10, <= 7 worker processes total (8 cores; measured peak RSS per zero worker 26 MB),
hard cap ~5 h wall for k2tail, ~4 h for lattice2. Checkpoint per chunk.
