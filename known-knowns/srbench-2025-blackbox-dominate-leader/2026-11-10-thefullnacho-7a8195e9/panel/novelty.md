# NOVELTY verdict — SRBench 2025 black-box, 1028_SWD

context: subagent

## Claim under review
30 closed-form expressions for PMLB dataset 1028_SWD, one per listed seed,
median test R² 0.3910 (saved values; REPRODUCE.md notes re-scoring the
4-decimal-rounded strings gives 0.3911) and median complexity 75.5, against the
bar median R² > 0.3800 and median complexity ≤ 3270 (PS-Tree).
Sources read: claim.md, expressions.json, REPRODUCE.md, table_record.txt,
data/results.feather (local copy), plus TROPHY_CASE.md in the repo copy.

## (1) Live status-source check — DONE, table unchanged
- Single honest GET, 2026-11-10 06:20:59 UTC:
  URL: https://raw.githubusercontent.com/cavalab/srbench/srbench_2025/results/black-box-tuning/results.feather
  Result: HTTP 200, 132 bytes — the Git LFS pointer, not the data file:
  `oid sha256:5b428264a346f6bbbeabded219f87454b9206afa70c19c012075c672533f342e`,
  size 5596634.
- That oid and size match table_record.txt exactly, and the local copy
  data/results.feather hashes to the same sha256
  (5b428264a346f6bbbeabded219f87454b9206afa70c19c012075c672533f342e).
  The live table is therefore byte-identical to the scout's fetch; no retry
  was made (the pointer match is the verification, per the no-retry rule).
- Leader recomputed from that byte-identical table (30 splits, model_size
  medians excluding -1): PS-Tree median r2_test 0.3800, median model_size
  3270 (n=30). Runner-up EQL 0.3736 / 59. Full top of table: GP-GOMEA
  0.3715 / 84.5, Brush 0.3672 / 46.5, GPZGD 0.3655 / 43.5, TIR 0.3628 / 67.5.
- Claimed median 0.3910 strictly beats the leader by 0.0110, at median
  complexity 75.5 ≤ 3270. It also beats the nearest-complexity neighbour
  EQL (0.3736 at size 59) on R². Not a tie.

## (2) Literature / code search, last 24 months — no better published result
- The SRBench 2025 paper itself (arXiv:2505.03977, GECCO '25) is the source
  of this table; its black-box track lists 1028_SWD (1000 rows, 10 features)
  among the 12 datasets, and its results are the table re-fetched above.
- Web searches for "SRBench 2025 1028_SWD", "1028_SWD symbolic regression",
  "cavalab srbench 2025 black-box PS-Tree", and srbench pull-request /
  results updates surfaced no result beating median R² 0.3800 on 1028_SWD
  under the SRBench 2025 protocol, and no srbench PR updating the 2025
  black-box results. (GitHub API was not attempted: rate-limited earlier
  today per the task brief; web search used instead.)
- Considered and excluded: Bemporad's PARC piecewise-affine paper reports
  R² up to ~0.997 on 1028 SWD, but it is ~2021 (outside the 24-month
  window), is not symbolic regression, returns a piecewise model with up to
  30 partitions rather than a single closed-form expression, and was not run
  under the SRBench 2025 30-seed protocol — it is not a result in this cell.
  The Soltani et al. SCML 2026 learning-to-rank deck uses 1028_SWD only as
  a model-selection dataset, with no new beating result.

## (3) Repo TROPHY_CASE.md and known-knowns/ — clean
- TROPHY_CASE.md contains zero mentions of "srbench" or "1028" (grep: 0 hits).
- known-knowns/ contains no srbench or symbolic-regression entry.

## (4) Trivial-edit test vs the published objects
The published objects for this cell are the `symbolic_model` strings in
data/results.feather. I compared the claimed expressions against the
published models for 1028_SWD (all algorithms; inspected best models for
PS-Tree, EQL, GP-GOMEA, Brush in full):
- Claimed form (all 30 splits, uniform): a 12-term dictionary sum —
  pairwise products x_i*x_j, squared deviations (x_i − 2)², hinges
  Max(0, 2 − x_i) / Max(0, x_i − 2), occasional log(x_i) or 1/x_i, plus a
  constant. Zero trig terms in any of the 30 expressions.
- EQL (runner-up): linear terms plus a single product of two affine forms —
  a different functional family; deleting/restricting it yields a linear
  model or a bilinear product, never a 12-term hinge dictionary sum.
- PS-Tree (leader): Piecewise sin-based expressions, median size 3270 —
  wholly different structure and ~43× the complexity.
- GP-GOMEA / Brush: trig-heavy (sin/cos) and Tanh/If/Cos forms respectively.
- No published model in the table contains a Max(0, 2 − x) hinge or an
  (x − 2)² term at all, so no deletion, restriction, propagation rule,
  relabelling, symmetry, or local numerical polish of any published object
  produces the claimed family. The procedure (RBF kernel-ridge teacher,
  dictionary student) is not seeded from a published object and names none.
- The claimed expressions are therefore genuinely new objects for this cell,
  not trivial edits of published ones, and they strictly beat every known
  median in the cell.

## Caveats
- Novelty only: correctness of the R²/complexity scoring is for the
  reproduction skeptic, not this panel. I verified the saved per-split
  values in expressions.json have median R² 0.3910 and median complexity
  75.5 as stated, but did not independently re-score the expressions.
- The live fetch returned the LFS pointer rather than the feather bytes;
  the leader recomputation rests on the pointer oid matching the local
  copy's sha256 exactly, which proves the live table content is unchanged.

## Verdict
The result strictly beats everything known for SRBench 2025 black-box
1028_SWD (leader PS-Tree 0.3800 → claimed 0.3910, complexity 75.5 ≤ 3270),
no better published result exists in the last 24 months, nothing in
TROPHY_CASE.md or known-knowns/ covers it, and the expressions are not
trivial edits of any published model in the table.

pass: true
