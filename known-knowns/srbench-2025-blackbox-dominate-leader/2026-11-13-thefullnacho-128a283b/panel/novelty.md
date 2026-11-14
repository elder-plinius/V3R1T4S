context: subagent
# NOVELTY verdict — srbench-2025-blackbox-dominate-leader, dataset 522_pm10

Claimed point: median test R2 0.3313 at median complexity 145.5 (30 GAM shape-compression
expressions, one per split, in expressions.txt).

## Live table fetch (one honest GET, no retries)

- URL: https://media.githubusercontent.com/media/cavalab/srbench/srbench_2025/results/black-box-tuning/results.feather
- Fetched: 2026-11-13 06:21:11–06:21:12 UTC
- Result: HTTP 200, 5,596,634 bytes, sha256 5b428264a346f6bbbeabded219f87454b9206afa70c19c012075c672533f342e
- The sha256 is IDENTICAL to the sha256 recorded in table_record.txt (scout fetch
  2026-11-13 06:02 UTC, "IDENTICAL to the 2026-11-10, 2026-11-11 and 2026-11-12
  fetches; table unchanged"). The table has not changed.
- Medians recomputed by me from my own fresh fetch (839 rows, 30 seeds, 28 algorithms):
  leader PS-Tree 0.300852 / 4996.5; QLattice 0.276510 / 35; TIR 0.250489 / 75;
  Operon 0.236309 / 52; Bingo 0.234161 / 30; GP-GOMEA 0.231105 / 61.
  Confirms the claim's bar: "PS-Tree median R2 0.300852 at median model size 4996.5".
- Pareto front for 522_pm10 recomputed from my fetch: (-0.0040, 1.0, E2E),
  (0.1204, 3.0, PYSR), (0.1758, 9.5, AFP_EHC), (0.1932, 20.5, AFP),
  (0.2342, 30.0, Bingo), (0.2765, 35.0, QLattice), (0.3009, 4996.5, PS-Tree).
  Matches table_record.txt exactly.
- No algorithm in the table has median R2 >= 0.3313 with median size <= 145.5
  (empty query result). The claimed point (0.3313, 145.5) strictly dominates
  PS-Tree (0.3009, 4996.5) and is dominated by no published point.

## Independent check of the claimed numbers

I could not run the packaged checker as-is: code/check_srbench.py imports
data/symbolic_utils.py, whose line 8 does `from read_file import read_file`,
and read_file is absent from claim/data/ and not importable in the run venv.
So instead I re-implemented the scoring independently (same split protocol —
sklearn train_test_split train_size 0.75, random_state = seed; same parse
rules as code/check_srbench.py; complexity = SRBench's own definition in
data/symbolic_utils.py, `complexity()` = preorder_traversal node count).
Result over all 30 expressions in expressions.txt: median R2 0.3312629480085087,
median complexity 145.5, and all 30 per-line R2/cx headers reproduced exactly.
The claimed numbers are genuine as scored, not just asserted in headers.
(Caveat for the reproduction panel: the packaged checker needs read_file
supplied before it runs standalone.)

## Literature / code search (last 24 months)

- Web search "SRBench 2025 black-box benchmark 522_pm10 PS-Tree results": the
  primary source is the SRBench 2025 paper, arXiv 2505.03977 ("Call for Action:
  Towards the Next Generation of Symbolic Regression Benchmark", GECCO '25),
  which lists "522_pm10 500 8 R +" among the 12 black-box datasets and reports
  the same benchmark whose results live in results.feather. No other source
  reports a 522_pm10 result at or above 0.3313. The paper states "Our results
  show that no single algorithm dominates across all datasets."
- Web search "GAM generalized additive model shape compression symbolic
  regression pm10": only generic GAM-on-air-pollution work (AirGAM 2022r1,
  Geosci. Model Dev. 16, 573-595, 2023 — trend estimation on EEA station data,
  not SRBench splits; a 2012 CMU GAM lecture; a 2019 GAM review). No GAM /
  shape-compression symbolic-regression result on the SRBench 522_pm10 splits.
- cavalab/srbench releases (GitHub API): only v1.0 and v2.0, both 2022-01-20,
  no assets — no release asset newer than the srbench_2025 tree. The live
  results.feather is the current table.
- cavalab/srbench pull requests (API, state=all, first 100): method additions
  only (LawSieve, SHR, PIR, Keplearn, GP_ELITE, SMGPRegressor, etc.). None
  reports a 522_pm10 result or a new benchmark table.
- elder-plinius/V3R1T4S pull requests (API, state=all, first 100) and GitHub
  issue search `repo:elder-plinius/V3R1T4S 522_pm10` (total_count 0): no PR
  claims a 522_pm10 result. The two srbench-target PRs found by search
  `repo:elder-plinius/V3R1T4S srbench` are on OTHER datasets: #1044
  ("1028_SWD median test R2 0.3911 beats PS-Tree 0.3800 at size 75.5") and
  #965 ("579_fri_c0_250_5 (R2=0.9...)"). Neither touches 522_pm10.
- Repo TROPHY_CASE.md: grep for `522_pm10|srbench|pm10` returns nothing.
  known-knowns/ and bank/: grep for `srbench|522_pm10` hits only
  bank/targets.json, which contains the target statement itself
  ("srbench-2025-blackbox-dominate-leader"), including the published bar
  quoted there: "522_pm10 PS-Tree 0.301 at size 4996". No prior 522_pm10
  result exists in the repo.

## Trivial-edit comparison (cell and neighbours)

Published points for this cell (median R2, median size): PS-Tree (0.3009, 4996.5),
QLattice (0.2765, 35), TIR (0.2505, 75), Operon (0.2363, 52), Bingo (0.2342, 30),
GP-GOMEA (0.2311, 61), and the rest below 0.23.
- The claimed point (0.3313, 145.5) beats the best published R2 by +0.0304
  (10% relative) while being 34x smaller than the leader. No published point
  is within reach by a trivial edit: deletion/restriction of the 4996-node
  PS-Tree expression cannot produce the claimed additive hinge/log structure,
  and a "local numerical polish" cannot lift QLattice 0.2765 -> 0.3313 (+0.0548)
  or Bingo 0.2342 -> 0.3313 (+0.0971). The claimed expressions are structurally
  different from every published one: purely additive sums over the 7 features
  of <=3-term compressed shapes (hinges at train quartiles, log(1+Abs(.)),
  sqrt(Abs(.)), squares, sin/cos of hour_of_day and day only) — no published
  522_pm10 expression has this form, and none is a seed for them (see below).
- Neighbouring cells: the same target's other datasets (1028_SWD, 579_fri_c0_250_5)
  are different datasets with different expressions; nothing transfers to 522_pm10.

## Procedure not seeded from a published object

Verified from code/gam_sr.py and PREREG.md: the procedure reads only
data/results.feather (for the seed list) and data/522_pm10.tsv.gz. It fits
univariate shapes by backfitting on train only (8 rounds, 20 quantile bins,
3 passes of [1,2,1]/4 smoothing), compresses each shape greedily (<=3 terms)
from a fixed per-feature library on a 60-point quantile grid, and refits all
coefficients jointly by OLS on full train. No published expression, table
entry, or external object is loaded, copied, or used as a seed anywhere in
the code. The expressions in expressions.txt are consistent with that
procedure (per-feature additive terms, hinge knots at train quartiles such as
cars_per_hour 6.2-6.4, wind_speed 1.7/4.3, day ~510-521, sin/cos only for
hour_of_day and day).

## Verdict

The claimed point strictly beats everything known for 522_pm10: it is above
the live leader's median R2 and far below the leader's size, it dominates a
Pareto-front point, no literature, code, release, PR, trophy case, or
known-knowns entry matches or exceeds it, and no trivial edit of any
published expression yields it. The procedure is fixed and unseeded.
pass: true
