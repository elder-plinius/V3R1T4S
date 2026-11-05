# PREREG — 2026-11-05 (frozen BEFORE any attack output is scored)

Target: packomania-cci-equal-circles-in-circle, row N=4153 (bank partial win
p2 class: gap value N > 2600 with a lattice-like seed by Eckard Specht).
Rotation from queue-blocked N=4000 (Karl Desfontaines cci 126–4141 line
persists; pending page byte-identical to 2026-11-04).

## Criterion (operative numbers, from the live scout 2026-11-05)
- Table radius r_table(4153) = 0.014596422226478759387097611060
  (row N=4153 of data/radius.txt, sha256
  6c60da0a2feb2ad01f2bed8dd99646021bcfd4cbfecb5ea2a7b332ecfa0beead).
- Scout vs 2026-11-04: table, author, seeds byte-identical; cci.html
  moved by one cosmetic line only (ref [31] year 2024 -> 2026);
  pending page byte-identical (Karl cci 126–4141 line persists).
- WIN iff a file of 4153 centers (x_i, y_i) satisfies ALL of:
  (a) r* := min(min_{i<j}|c_i - c_j|/2, 1-max_i|c_i|) computed in mpmath at
      50 digits directly from the submitted coordinates, no tolerance,
      satisfies r* - r_table >= 1e-11;
  (b) the configuration is not isometric to the posted data/cci4153.txt
      (sha256 bca1f6739e2a898d6862658e092f0e105667652dac18340da863a8d2eb94ffae):
      sorted pairwise-distance multisets differ;
  (c) N=4153 does not appear in a History-of-updates line on live cci.html
      newer than the scout (newest seen: 11-Oct-2026, Zii Fave N=15 proofs);
  (d) N=4153 is outside every cci range on the live pending-requests page at
      verification time — CURRENTLY SATISFIED: live cci ranges are
      Patankar 652–3943 and Karl 126–4141; 4153 is outside both.
- RESOLVED CAVEAT: the 26-Sep-2026 Moki & Julio "*many*" 4666-candidate
  bundle has been expanded into per-category pending lines, none cci;
  it is no longer an open caveat.
- Verdict scale: CONFIRMED_* only via three-skeptic panel + CHECK_RUN: PASS;
  otherwise at most PROMISING (single context). A configuration equal to the
  table within 1e-11 but certified non-isometric = bank partial win p1.
  Clean negatives = NOTHING. N=4000 states are NOT claims tonight (queue
  condition (d) fails there); the N=4000 walk state is banked only.

## Statistic / checker that judges it
code/checker.py: `check(path, N)` prints r*, table value, and margin at 50
digits. Non-isometry via `distance_multiset()` differing from the posted
seed's multiset. Validated this run: selftest ALL PASS (posted cci100
reproduces table to 8.7e-31; single center perturbed by 1e-6 collapses to
margin -4.659e-07) — see data/selftest.log. Posted cci4153.txt reproduces
its table row (checked by the skeptic lens before attack scoring).

## Thresholds
- margin >= 1e-11 (mpmath 50 digits, no tolerance): required for any win claim.
- margin in (0, 1e-11): documented as negative (feasibility-slack artifact class).
- margin <= 0: negative.

## Null design
null_test: not needed because the claim is an explicit geometric object
checked by a deterministic checker against a published table value — there
is no search statistic, threshold tuned on data, or "beats chance"
component. The checker itself is validated on a known positive and a known
negative before any attack output is scored.

## Scope guard
One object per claim (single N). No bundling across N values. Dedupe: if two
lenses find the same object, panel one carrier and cite the other.

## Margin-reporting rule (applies to every lens this run)
Every margin reported in a lens report is recomputed from the saved file
with the double evaluator, never a tracked value carried through a polish
loop. Polish equivalents in tonight's code recompute feasible_r from the
returned configuration before logging, saving, or comparing.

## Lens budgets (this run)
- already-settled: table/queue/history/trophy/seed verification only, no compute.
  Must explicitly verify N=4153 is outside both live cci queue ranges, the
  Karl line's persistence, the cci.html one-line cosmetic move, and that the
  posted cci4153.txt reproduces the table row.
- fresh-trunc-4153: systematic hex-truncation grid (theta 0-30 deg x 0.25 deg,
  21 spacings around 2*r_table, 5x5 lattice-cell offsets = 63,525 evals),
  then 3,000 random refinements around the grid best (rng seed 20261105),
  then 30,000 full-cell random evals (same rng stream) — the 96,525-eval
  recipe from 2026-10-25/27. Saves the single best truncation.
  Hard cap 1800 s, nice 10.
- deep-polish-4153: 8-ratchet smooth-max polish of the top 4 diverse raw
  candidates from fresh-trunc-4153 (grid best, refine best, random best,
  second distinct basin if present). Saves polished00..03.txt, ranked.
  Hard cap 1800 s, nice 10.
- narrow-walk-4153 (only if deep-polish best lands within 1e-05 of the
  table): small-jitter greedy walk from the polished best, sigma UNIFORM
  0.050-0.065R (the productive narrow band from the N=4000 nights),
  rejam at the incumbent radius then climb, checkpoint on every
  improvement; rng seed 20261105 (fresh; never used before). Hard cap
  1800 s, nice 10.
  Lenses are independent; the better final state is the carried lead,
  deduplicated by recomputed margin.
