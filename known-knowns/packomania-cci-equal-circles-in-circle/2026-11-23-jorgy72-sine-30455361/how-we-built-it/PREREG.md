# PREREG — 2026-11-23 (frozen BEFORE any attack output is scored)

Target: packomania-cci-equal-circles-in-circle, primary row N=4405 (bank
partial win p2 class: gap value N > 2600 with a lattice-like seed by Eckard
Specht). First-night rotation row: the 2026-11-22 report names N=4405 as the
next rotation row. N=4381's walk bands are BOTH spent — no walk at 4381
tonight (a different attack family only, per the 2026-11-22 lead). N=4357 is
CLAIMED (confirmed-partial, packaged outbox/2026-11-20-jorgy72-sine-
d82bab79/) — do not re-attack. N=4345 is CLAIMED (packaged
outbox/2026-11-19-jorgy72-sine-e8859dd3/) — do not re-attack. N=4339 is
CLAIMED (packaged outbox/2026-11-18-jorgy72-sine-ea04e0b5/) — do not
re-attack. N=4315 is CLAIMED (packaged outbox/2026-11-17-jorgy72-sine-
1906e4fb/) — do not re-attack. N=4153 is claimed and merged (PR #957,
merge commit 5e93e75, 2026-11-06T17:47:49Z — do not re-attack). N=4303,
N=4267, N=4243, N=4255 walk bands are BOTH spent — no walk at any of them
tonight. N=4000 and N=3985 remain queue-blocked (Karl Desfontaines cci
126–4141 line persists; pending page BYTE-IDENTICAL to the 2026-11-22
verification fetch). N=4219/4231/4195/4189/4177 states are banked from prior
runs and are NOT claims tonight.

## Criterion (operative numbers, from the live scout 2026-11-23)
- Table radius r_table(4405) = 0.014190212053 (live radius.txt, 12-decimal,
  re-fetched tonight; sha256
  bbbf290022342473e79e5e465f939f020f6fe97d0c69ea904599e2463293d4a7).
  The live HTML table ends at N=3877 and carries no row for 4405. The
  archived 30-decimal value (2026-11-22 HTML) is
  0.014190212052536014904153227050 — 4.64e-13 LOWER, so the 12-decimal live
  value is the stricter bar and is the operative one.
- Scout vs 2026-11-22: site rebuilt again (22 Nov 20:32 GMT; HTML full page
  again, 12-decimal, 2691 rows ending at N=3877; txt 430 rows changed, 429
  larger + 1 smaller by -6e-12 at N=760 — the 22-Nov-2026 Specht wave);
  pending page BYTE-IDENTICAL — no movement at all.
- WIN iff a file of N centers (x_i, y_i), N = 4405, satisfies ALL of:
  (a) r* := min(min_{i<j}|c_i - c_j|/2, 1-max_i|c_i|) computed in mpmath at
      50 digits directly from the submitted coordinates, no tolerance,
      satisfies r* - r_table >= 1e-11, where r_table is the live
      12-decimal value above;
  (b) the configuration is not isometric to the posted data/cci4405.txt
      (sha256 98f2b10dfc1f0dda4e4bdf4ff9f892de95d5e95d3bd13ea6b8af62f5739df1a1,
      12-decimal format, 4405 data rows):
      sorted pairwise-distance multisets differ;
  (c) N does not appear in a History-of-updates line on live cci.html
      newer than the scout (newest entries: 22-Nov-2026 Specht wave
      N=259..998, and the 21-Nov-2026 Patankar/Desfontaines bundles —
      none lists N=4405);
  (d) N is outside every cci range on the live pending-requests page at
      verification time — CURRENTLY SATISFIED: live cci ranges are
      Patankar 652–3943 and Karl 126–4141; 4405 is outside both.
- Verdict scale: CONFIRMED_* only via three-skeptic panel + CHECK_RUN: PASS;
  otherwise at most PROMISING (single context). A configuration equal to the
  table within 1e-11 but certified non-isometric = bank partial win p1.
  Clean negatives = NOTHING.

## Statistic / checker that judges it
code/checker.py (adapted this run for the site's new state — see "Checker
adaptation" below): `check(path, N)` prints r*, table value, and margin at
50 digits. Non-isometry via `distance_multiset()` differing from the posted
seed's multiset. Validated this run: selftest ALL PASS — the strict positive
on the archived 30-decimal cci100 against the archived 30-decimal table
(reproduces to 8.7e-31), the new-format positive on the live 12-decimal
cci100 against the live radius.txt (reproduces to 7.4e-15), and the
perturbed-center negative — see data/selftest.log. Posted cci4405.txt
checked at 50 digits — see data/seed4405_check50.log (margin at rounding
level, as expected for 12-decimal coordinates; the seed is isometric to
itself, so no claim question arises).

## Checker adaptation (site state change, 2026-11-23)
- The live HTML table is now 12-decimal AND ends at N=3877: N=4405 has no
  live HTML row. table_radius() now reads the live radius.txt (12-decimal,
  re-fetched tonight) as the operative table source; that value is 4.64e-13
  higher than the archived 30-decimal value, so the bar is stricter.
- The strict selftest positive now uses archived30_radius() (the 2026-11-22
  30-decimal table) against the archived 30-decimal cci100; the live-format
  positive uses the live radius.txt.
- load_centers() is unchanged: it already skips '#' header lines and reads
  parts[1], parts[2], so the 12-decimal seed format parses.

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
The narrow-walk-4405 lens runs ONLY if the deep-polish best margin is
within 1e-05 of the table (i.e. best polished margin > -1e-05). If the
condition fails, the walk does NOT run and the lens is recorded as
not-run with the prereg condition cited. If a verified above-bar claim
is found, the walk does NOT run — the claim supersedes it (same as
2026-11-17, 2026-11-18, 2026-11-19 and 2026-11-20).

## Margin-reporting rule (applies to every lens this run)
Every margin reported in a lens report is recomputed from the saved file
with the double evaluator, never a tracked value carried through a polish
loop. deep_polish.py recomputes feasible_r after the ratchet loop (the
2026-10-30 fix, applied 2026-11-06) and now also reverts to the incumbent
on a degrading ratchet (the 2026-11-07 lesson, verified 2026-11-08).
Polish equivalents in tonight's code recompute feasible_r from the returned
configuration before logging, saving, or comparing. Print mpmath values
with mp.nstr, never via float() (the 2026-11-18 lesson: float-rounded
%.30f prints are off by ~7e-19 from true 50-digit values).
