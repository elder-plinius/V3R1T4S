# AlphaEvolve-family analytic constants: autocorrelation inequalities and Erdos minimum overlap

📊 **Record tables** · standard · tractability ★☆☆☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

Improve any of these constants with an explicit step function. (i) C_1a, the Sidon (first) autocorrelation constant (upper bound via a nonnegative f minimizing max(f*f)/(∫f)^2 with the repo normalization; Tao's constants/1a.md). (ii) The Erdos minimum overlap constant C_1b, which is equivalent to Erdos problem #36 (Haugland 2016, arXiv:1609.08000; Tao's constants/1b.md); upper bound via a step function f with f+g=1. (iii) The second autocorrelation constant C_2 (lower bound via ||f*f||_2^2 / (||f*f||_1 ||f*f||_inf)). (iv) The third autocorrelation constant C_3 (upper bound; EinsteinArena 'third autocorrelation inequality'; not the GHR sum-difference constant C_3a). As of 2026-10-20: MILO (arXiv:2609.38349, 29 Sep 2026) claims Erdos overlap 0.3808586 -> 0.3808568, C_1a 1.50274365 -> 1.50274360 and C_3 1.45081 -> 1.44889; the live arena Erdos overlap leader is NIGHTFALL-DevinWright 0.3808564 (then CristianBudala 0.3808566), below MILO's claim; the live arena first-autocorrelation leader is Atris 1.50274349 (then AgentDiscover 1.50274353), with exact value 1.50274348670958... on Tao's 1a page; C_2 >= 0.963588 (arena, ClaudeExplorer). Lower-bound side: Erdos >= 0.379005 (White 2022) is the established bound on Tao's 1b page; for C_1a, 1.2802 (Ivanisvili-Xie 2026) is the verified entry on Tao's 1a page and 1.292 (Piterbarg-Bajaj-Vincent 2026) is listed there as unverified. arXiv:2606.31182 (Kim-Pilanci, Jun 2026) claims C_1a >= 1.2937 and Erdos >= 0.37912 with interval-arithmetic dual certificates; these are claims, not yet listed on Tao's pages or checked here. Improvements now land at the 1e-7 to 1e-8 level among many competing agents.

## What counts as a win

Success means an exact rational step function (data file) whose exactly computed functional (no FFT floating-point scores) is STRICTLY BETTER in that constant's direction (min for Erdos overlap, C_1a and C_3; max for C_2) than the BEST value at verification time over: the live EinsteinArena leaderboard for that problem (https://einsteinarena.com/problems/first-autocorrelation-inequality, https://einsteinarena.com/problems/erdos-min-overlap, https://einsteinarena.com/problems/second-autocorrelation-inequality, https://einsteinarena.com/problems/third-autocorrelation-inequality), Tao's live pages (https://github.com/teorth/optimizationproblems/blob/main/constants/1a.md and 1b.md), arXiv:2609.38349 (MILO) and any newer arXiv claim, by at least 1e-6 absolute in the correct normalization (arena display may be halved; calibrate on published data first). Wherever a record holder's function is published (arena submissions, the Together AI repo, AlphaEvolve problem pages, links on Tao's pages), the verifier recomputes its UNROUNDED value with the same exact evaluator and compares against that, never against a rounded display; a record whose function is not published (e.g. MILO's) is used at its printed value. Context on 2026-10-20: C_3 bar 1.44889, Erdos 0.3808564, C_1a 1.50274349, C_2 0.963588 (C_3 and C_2 not re-read). Dual-side lower-bound improvements count only with a rigorous interval-arithmetic or exact certificate.

## Partial wins

- **p1:** A rigorous dual-side record: a lower bound C_1a > 1.2937 or Erdos minimum overlap > 0.37912, strictly above the best lower bound found at verification time, counting the verified entries on Tao's 1a/1b pages (1.2802 IX2026; 0.379005 White 2022), the unverified 1.292 (PBV2026) and the claimed bounds of arXiv:2606.31182, with an interval-arithmetic or exact certificate the skeptic re-runs.
- **p2:** A sub-threshold exact record: an exact rational step function that beats the best live value for one constant by less than 1e-6, with the improvement certified in exact rational arithmetic in the arena's normalization (strict, not a floating-point tie).
- **p3:** An exactly certified improvement (direction: min) of a discrete minimum-overlap value M(n) on the live page https://www.neutreeko.net/mop/index.htm for some n where that page lists only a bound (not a proven optimum), with the partition of {1..2n} given explicitly and the overlap recomputed exactly over all shifts.

## How a win is checked

First recompute the current record holders' UNROUNDED values from their published functions (arena submissions, Together AI repo, AlphaEvolve problem pages, TTT data) with the same exact evaluator used for the candidate, to fix the normalisation and the true record digits. Use exact arithmetic with fractions or integers after scaling. The autoconvolution of a step function on a uniform grid is piecewise linear with knots at grid points, so its max is attained at a knot: compute the discrete convolution of the integer heights exactly. For C_2, integrate the piecewise-linear f*f squared exactly per interval (quadratic, so closed form). For the Erdos overlap, the correlation of step functions is piecewise linear, so check all breakpoints exactly and verify f+g=1, 0<=f<=1, and ∫f=1. Calibrate by re-deriving a published value (e.g. AlphaEvolve's 1.5053 or TTT's 1.50287 data) in the same normalization. EinsteinArena's display uses a halved scale (e.g. 0.75143 vs 1.50287). For a discrete M(n) claim, recompute max over shifts k of |A ∩ (B+k)| exactly and compare with the live neutreeko page.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://einsteinarena.com/>

## Sources

- <https://einsteinarena.com/>
- <https://github.com/jmsung/einstein>
- <https://teorth.github.io/optimizationproblems/>
- <https://google-deepmind.github.io/alphaevolve_repository_of_problems/>
- <https://github.com/vinid/einstein-arena>
- <https://arxiv.org/abs/2609.38349>
- <https://arxiv.org/abs/2606.31182>
- <https://github.com/teorth/optimizationproblems/blob/main/constants/1b.md>
- <https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/5.html>
- <https://github.com/togethercomputer/EinsteinArena-new-SOTA>
- <https://www.neutreeko.net/mop/index.htm>
- <https://arxiv.org/abs/1609.08000>
- <https://arxiv.org/abs/2201.05704>
- <https://github.com/teorth/optimizationproblems/blob/main/constants/1a.md>
- <https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/2.html>
- <https://www.erdosproblems.com/36>
- <https://einsteinarena.com/problems/erdos-min-overlap>
- <https://einsteinarena.com/problems/first-autocorrelation-inequality>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Do LP/QP alternation. For a fixed active set of near-maximal autoconvolution knots, the problem in f is an LP after normalizing ∫f=1. Iterate active-set LP (scipy HiGHS) at grid sizes 10^4-10^5, which is more principled than gradient methods.
- Use multiscale upsampling with Nesterov or Adam on a log-sum-exp smoothed max, annealing the temperature, then an exact LP polish.
- Exploit the 'block-oscillation' and asymmetry structure noted by arena agents. Parametrize f as a smooth envelope times a high-frequency comb and optimize envelope parameters.
- Pursue the dual side for a partial win: improved lower bounds for C_1a (verified 1.2802, Ivanisvili-Xie 2026; unverified 1.292, PBV2026; claimed 1.2937, arXiv:2606.31182) via Fourier/SDP certificates. These are verifiable as rigorous inequalities with interval arithmetic.
- Warm-start from the published SimpleTES/TogetherAI/AlphaEvolve step functions (EinsteinArena repo, AlphaEvolve problem page). Refine by sequential linear programming: linearise the bilinear term around the current f, minimise the max over the active breakpoints with a trust region, and repeat.
- Progressive upsampling (N = 1k to 50k steps) with FFT-based subgradients on the max (bundle or prox-linear methods), then rationalise and re-certify exactly.
- Structural priors from Haugland: near-optimal f is mostly 0/1 with thin transition zones. Parametrise the transition profiles with few parameters and optimise globally (CMA-ES), then polish with LP.
- For the lower bound: White's Fourier/SDP approach. Raise the truncation order or add new valid inequalities and solve the SDP with a certificate (rational rounding).
- Warm-start from the published Together AI / TTT-Discover / AlphaEvolve step functions and refine with sequential LP, minimising the max over active breakpoints under a trust region.
- Upsample (N = 600 to 50k steps) with FFT subgradients and a prox-linear or bundle method, then rationalise and re-certify exactly.
- Equalisation heuristic: optimal f should make f*f nearly flat on a large plateau. Solve for f that makes f*f equal a target plateau via Newton on the step heights.
- Try structured families (sums of power-law spikes near ±1/4 plus smooth bulk) and polish them with the LP.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Normalization mismatches between AlphaEvolve, Tao's repo and EinsteinArena (factor 2, support [-1/4,1/4] vs [0,1]).
- FFT round-off makes scores look better by around 1e-9. Use exact certification only.
- There are dozens of agents on these leaderboards and improvements are in the 6th decimal. Re-fetch the leaderboard right before claiming.
- The direction of the bound (upper vs lower) differs per problem.
- Paper claims (MILO) may use different normalizations from the arena. Calibrate on its published data before comparing.
- The third autocorrelation bar jumped from 1.4508 to 1.4489 in Sep 2026. Old baselines will cause false claims.
- Normalisation mismatch between the discrete M(n)/n and continuous scalings ([-1,1] versus [0,2]).
- Evaluating the sup only on a grid rather than at all breakpoints.
- Claiming improvements at the 1e-7 level from float arithmetic.
- Forgetting that g = 1 - f >= 0 requires f <= 1.
- Records move monthly, so re-check the repo on the day.
- Comparing against the rounded 0.380868 rather than the record's exact value.
- Records changed four times in about a year; re-fetch 1b.md on the day.
- Support/normalisation mismatch ([-1/4,1/4] versus [0,1] or [-1/2,1/2] conventions).
- Evaluating the max on a grid instead of at all breakpoints.
- Float-level 'improvements' below 1e-7.
- Comparing against the rounded 1.502862.
- The third autocorrelation constant C_3 here is NOT the GHR sum-difference constant C_3a (Tao's constants/3a.md, bank entry ghr-sum-difference-c3a). Never compare values across them.
- Tao's 1a/1b pages lagged the arena and MILO on 2026-10-03 (1.502862 and 0.380868). On 2026-10-18 they list the arena leaders and Atris's refinements (1.5027434868, 0.3808585504) but not MILO's claimed 0.3808568, so take the best over all the criterion's sources, never one page.
- Lower-bound provenance: White 2022 (0.379005) and IX2026 (1.2802) are verified; PBV2026 (1.292) is asterisked as unverified on Tao's page; arXiv:2606.31182's 1.2937 and 0.37912 are claims.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/record-tables/alphaevolve-analytic-constants.md
```

Already set up? Say `run V3R1T4S on alphaevolve-analytic-constants`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `alphaevolve-analytic-constants`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
