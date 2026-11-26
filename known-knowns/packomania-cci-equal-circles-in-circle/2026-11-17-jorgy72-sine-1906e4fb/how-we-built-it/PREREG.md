# PREREG — 2026-11-17 (frozen BEFORE any attack output is scored)

Target: packomania-cci-equal-circles-in-circle, primary row N=4303 (bank
partial win p2 class: gap value N > 2600 with a lattice-like seed by Eckard
Specht), secondary row N=4315 (first-night fresh-truncation row, same class).
Continuation of the live lead from 2026-11-16 (N=4303 narrow-walk best
-2.788e-06, wide band untested there — the one remaining walk probe).
N=4267 walk bands are BOTH spent (2026-11-15 narrow 0/51, 2026-11-16 wide
0/48) — no walk at 4267 tonight. N=4243 and N=4255 walk bands are BOTH
spent — no walk at either tonight. N=4000 and N=3985 remain queue-blocked
(Karl Desfontaines cci 126–4141 line persists; pending page BYTE-IDENTICAL
to 2026-11-10/11/12/13/14/15/16). N=4153 is claimed and merged (PR #957,
merge commit 5e93e75, 2026-11-06T17:47:49Z — do not re-attack). N=4219/4231/
4195/4189/4177 states are banked from prior runs and are NOT claims tonight.

## Criterion (operative numbers, from the live scout 2026-11-17)
- Table radius r_table(4303) = 0.014342875056562309945593852991
  (row N=4303 of data/radius.txt, sha256
  6c60da0a2feb2ad01f2bed8dd99646021bcfd4cbfecb5ea2a7b332ecfa0beead).
- Table radius r_table(4315) = 0.014323541476018172725671907488
  (row N=4315 of the same live table).
- Scout vs 2026-11-16: table, author, seeds, cci.html, pending page ALL
  byte-identical; cci4315.txt fetched fresh this run (sha256
  9af86ffc1a5fcc6ba0165682e81f4576e39fe21caa31284b973164aa9f3bccc5).
- WIN iff a file of N centers (x_i, y_i), N in {4303, 4315}, satisfies ALL of:
  (a) r* := min(min_{i<j}|c_i - c_j|/2, 1-max_i|c_i|) computed in mpmath at
      50 digits directly from the submitted coordinates, no tolerance,
      satisfies r* - r_table >= 1e-11;
  (b) the configuration is not isometric to the posted data/cci<N>.txt
      (4303: sha256 41642ac69f2fe681b9e210350d697105b6b08adc31691d7f3ae4fcf6cd958351;
       4315: sha256 9af86ffc1a5fcc6ba0165682e81f4576e39fe21caa31284b973164aa9f3bccc5):
      sorted pairwise-distance multisets differ;
  (c) N does not appear in a History-of-updates line on live cci.html
      newer than the scout (newest seen: 11-Oct-2026, Zii Fave N=15 proofs);
  (d) N is outside every cci range on the live pending-requests page at
      verification time — CURRENTLY SATISFIED for both rows: live cci ranges
      are Patankar 652–3943 and Karl 126–4141; 4303 and 4315 are outside both.
- Verdict scale: CONFIRMED_* only via three-skeptic panel + CHECK_RUN: PASS;
  otherwise at most PROMISING (single context). A configuration equal to the
  table within 1e-11 but certified non-isometric = bank partial win p1.
  Clean negatives = NOTHING.

## Statistic / checker that judges it
code/checker.py: `check(path, N)` prints r*, table value, and margin at 50
digits. Non-isometry via `distance_multiset()` differing from the posted
seed's multiset. Validated this run: selftest ALL PASS (posted cci100
reproduces table to ~1e-30; single center perturbed by 1e-6 collapses to
margin ~-4.7e-07) — see data/selftest.log. Posted cci4303.txt and cci4315.txt
reproduce their table rows at 50 digits (checked by the skeptic lens before
attack scoring).

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
loop. deep_polish.py recomputes feasible_r after the ratchet loop (the
2026-10-30 fix, applied 2026-11-06) and now also reverts to the incumbent
on a degrading ratchet (the 2026-11-07 lesson, verified 2026-11-08).
Polish equivalents in tonight's code recompute feasible_r from the returned
configuration before logging, saving, or comparing.

## Lens budgets (this run)
- already-settled: table/queue/history/trophy/seed verification only, no compute.
- wide-walk-4303: greedy walk from the 2026-11-16 narrow-walk best
  (-2.788e-06), sigma UNIFORM 0.065–0.090R, fresh rng seed 20261117 (never
  used), hard cap 1800 s, nice 10. Runs FIRST.
- fresh-trunc-4315: the 96,525-eval hex-truncation recipe, fresh rng seed
  43151711 (never used), nice 10. Runs SECOND.
- deep-polish-4315: 8-ratchet smooth-max polish of the top diverse raw
  candidates from fresh-trunc-4315. Runs THIRD, if time remains.
- narrow-walk-4315 (amendment, noted before it runs): greedy walk from the
  deep-polish best, sigma UNIFORM 0.050–0.065R, fresh rng seed 43151715
  (never used), hard cap 1800 s, nice 10. Runs FOURTH, ONLY if the
  deep-polish best is within 1e-05 of the table (standing rotation-night
  rule). If the polish best is further than 1e-05 below the table, the
  walk does not run and the row is carried as a polish lead.
