# PREREG — 2026-11-18 (frozen BEFORE any attack output is scored)

Target: packomania-cci-equal-circles-in-circle, primary row N=4339 (bank
partial win p2 class: gap value N > 2600 with a lattice-like seed by Eckard
Specht). First-night rotation row per the 2026-11-17 report (next rotation
row after 4315). N=4315 is CLAIMED (CONFIRMED_PARTIAL, packaged
outbox/2026-11-17-jorgy72-sine-1906e4fb/) — do not re-attack. N=4153 is
claimed and merged (PR #957, merge commit 5e93e75, 2026-11-06T17:47:49Z —
do not re-attack). N=4303, N=4267, N=4243, N=4255 walk bands are BOTH
spent — no walk at any of them tonight. N=4000 and N=3985 remain
queue-blocked (Karl Desfontaines cci 126–4141 line persists; pending page
moved only on date bumps + a comment marker since 2026-11-17). N=4219/
4231/4195/4189/4177 states are banked from prior runs and are NOT claims
tonight.

## Criterion (operative numbers, from the live scout 2026-11-18)
- Table radius r_table(4339) = 0.014278996448020329132467169733
  (row N=4339 of data/radius.txt, sha256
  6c60da0a2feb2ad01f2bed8dd99646021bcfd4cbfecb5ea2a7b332ecfa0beead).
- Scout vs 2026-11-17: table, author, seeds, cci.html ALL byte-identical;
  cci4339.txt fetched fresh this run (sha256
  baf49c5c256a5afc9794f7e705a24b740a2c1bc3ca62b3c0befbed17d164c3e5, 4339
  rows); pending page moved ONLY on date bumps (09-Nov -> 18-Nov) and a
  comment-marker shift — no new lines.
- WIN iff a file of N centers (x_i, y_i), N = 4339, satisfies ALL of:
  (a) r* := min(min_{i<j}|c_i - c_j|/2, 1-max_i|c_i|) computed in mpmath at
      50 digits directly from the submitted coordinates, no tolerance,
      satisfies r* - r_table >= 1e-11;
  (b) the configuration is not isometric to the posted data/cci4339.txt
      (sha256 baf49c5c256a5afc9794f7e705a24b740a2c1bc3ca62b3c0befbed17d164c3e5):
      sorted pairwise-distance multisets differ;
  (c) N does not appear in a History-of-updates line on live cci.html
      newer than the scout (newest seen: 11-Oct-2026, Zii Fave N=15 proofs);
  (d) N is outside every cci range on the live pending-requests page at
      verification time — CURRENTLY SATISFIED: live cci ranges are
      Patankar 652–3943 and Karl 126–4141; 4339 is outside both.
- Verdict scale: CONFIRMED_* only via three-skeptic panel + CHECK_RUN: PASS;
  otherwise at most PROMISING (single context). A configuration equal to the
  table within 1e-11 but certified non-isometric = bank partial win p1.
  Clean negatives = NOTHING.

## Statistic / checker that judges it
code/checker.py: `check(path, N)` prints r*, table value, and margin at 50
digits. Non-isometry via `distance_multiset()` differing from the posted
seed's multiset. Validated this run: selftest ALL PASS (posted cci100
reproduces table to ~1e-30; single center perturbed by 1e-6 collapses to
margin ~-4.7e-07) — see data/selftest.log. Posted cci4339.txt reproduces its
table row at 50 digits (checked by the skeptic lens before attack scoring).

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

## Narrow-walk condition (standing rotation-night rule)
The narrow-walk-4339 lens runs ONLY if the deep-polish best margin is
within 1e-05 of the table (i.e. best polished margin > -1e-05). If the
condition fails, the walk does NOT run and the lens is recorded as
not-run with the prereg condition cited.

## Margin-reporting rule (applies to every lens this run)
Every margin reported in a lens report is recomputed from the saved file
with the double evaluator, never a tracked value carried through a polish
loop. deep_polish.py recomputes feasible_r after the ratchet loop (the
2026-10-30 fix, applied 2026-11-06) and now also reverts to the incumbent
on a degrading ratchet (the 2026-11-07 lesson, verified 2026-11-08).
Polish equivalents in tonight's code recompute feasible_r from the returned
configuration before logging, saving, or comparing.
