# CRITERION skeptic verdict: iea37-cs1-circular-wind-farm-layout, 64 turbines, full success criterion

context: subagent (Claude Code Agent tool, fresh context, saw only claim/)

Files read: CLAIM.md, criterion.txt, REPRODUCE.md, object/layout.json, references/iea37-aepcalc.py,
references/iea37-windrose.yaml, references/iea37-335mw.yaml, references/iea37-par*-opt64.yaml,
references/pr938-layout.yaml, status/pr938-live.json, status/pr-search.json, status/status-page.html (title/file list only).
I did not open provenance/ (it does not bear on the criterion). Work: panel/work-criterion/check.py,
check-output.txt, match.py, match-output.txt. claim/ was not modified (PYTHONDONTWRITEBYTECODE=1).

## Evaluators
- Official: references/iea37-aepcalc.py (sha256 ec2d16f2...6b535) imported unmodified; its calcAEP called with its
  own getWindRoseYAML / getTurbAtrbtYAML readers (16 bins, ws 9.8, D 130.0, rated power 3350000.0 W).
- Independent: my own scalar re-implementation from the criterion's equations. My first version had the wrong
  rotation sign and disagreed; after the fix it agrees to within 1e-9 MWh everywhere.
- Validation: par12-opt64 official 1526474.8024800713, mine 1526474.8024800716 (REPRODUCE: 1526474.8024800716);
  par4-opt64 official 1513311.1936146398, mine 1513311.1936146400 (REPRODUCE: 1513311.19361464).
- I cannot compare the script with upstream from inside claim/. My equation-level evaluator matches it, and it
  reproduces the posted values, so any change to it would have to leave the AEP unchanged.

## Word-by-word check
| Criterion clause | Result |
|---|---|
| layout for the 64-turbine scenario | object/layout.json: coordinates_m only, shape (64, 2), all finite, 64 distinct hubs. Exactly one object. |
| every hub at distance at most R = 3000, no tolerance, double | max sqrt(x^2+y^2) = 2999.999900000135 (excess -9.999986514230841e-05). An exact rational check (Fraction x^2+y^2 <= 9e6) also passes for all 64. 15 hubs lie within 1e-3 m of R, and the smallest slack is 1.000e-04 m. Rounding to 3 dp would push hubs outside (+3.939e-04), so copies must keep full precision; the claim warns about this. |
| every pair at least 260 m | 2016 pairs; min distance 307.51364081707464 m; the exact rational check passes. Not marginal. |
| AEP from official model | 1543800.4664981714 MWh (official), 1543800.4664981714 (mine). The claim's 1543800.4665 matches. |
| STRICTLY GREATER by at least 0.01 than posted record 1526474.8025, used as posted | margin 17325.6640 MWh, so it passes. The claim uses the posted value (not the projected 1526474.68), which is the stricter reading and correct. The highest of all 12 posted opt64 files, recomputed, is iea37-par12-opt64.yaml, so the record is correctly identified. |
| strictly greater than every CONFIRMED V3R1T4S known-known (64) | status/pr-search.json (6 items, all open, none merged/labelled) shows no confirmed 64-turbine known-known. Items #578/#900 cover 16 turbines and #913 covers 36. #948 is a bank proposal for a different (robust) target. #866 is a data audit. The only 64-turbine item is PR #938, an open draft. The quantifier is vacuous or satisfied. Even if #938 counted as confirmed, the object beats it (next row). |
| re-check known-knowns and open claims; state which it beats | CLAIM.md names both: the posted record (participant 12) and open PR #938. Beating #938 is required by the novelty/claim-time rule, not by the criterion's CONFIRMED clause, because #938 is open and unreviewed (its body's "CONFIRMED_SOLUTION" is its own panel's label). The object beats it anyway. |
| PR #938 comparison | Recomputed from references/pr938-layout.yaml (sha256 d63ed6df...dd93c851, matching the PR body): official 1539447.1173686478, mine 1539447.1173686476. It is feasible (max r 2999.999999000001, min spacing 567.69 m). Object margin 4353.3491 MWh, matching the claimed 4353.35. status/pr938-live.json head 9f1145de... matches the head named in CLAIM.md. |

## Hidden quantifiers, stretched definitions, subsumption
- "every hub ... no tolerance": checked in both float and exact rational arithmetic. No tolerance is used.
- "posted record, used as posted": applied literally against 1526474.8025 + 0.01.
- "every CONFIRMED known-known at claim time": the evidence is the status snapshot in claim/status/. The search query
  string is not recorded, so I can only confirm what that snapshot contains. This limitation does not change the
  verdict, since the object also beats the strongest open 64-turbine claim.
- Not subsumed: the object exceeds PR #938, the only competing 64-turbine claim, by 4353 MWh. Under min-total-distance
  matching, 63/64 hubs are more than 50 m from their partner in participant 12 (median 323.5 m) and in PR #938
  (median 334.9 m). It is not a re-labelled copy of either.
- Full criterion, not a partial win. No physical or site-realism claim is made (consistent with the pitfalls).
- Null model: I agree that none is needed. The claim is one explicit deterministic object with a deterministic
  evaluation, and the margin is far beyond any floating-point effect (official vs independent difference < 1e-9 MWh).
- Wording note: CLAIM.md calls PR #938 "the strongest known open V3R1T4S claim". That is accurate for 64 turbines.
  #578 at 16 turbines is a different scenario.

confirmed_scope: The single 64-turbine layout in object/layout.json is strictly feasible for IEA37 case study 1 (all 64 hubs within 3000 m, maximum radius 2999.999900000135 m; all 2016 pairs at least 260 m apart, minimum 307.514 m; checked in double precision and exact rational arithmetic with no tolerance) and has AEP 1543800.4665 MWh under the official iea37-aepcalc.py model, which exceeds the posted participant-12 record 1526474.8025 MWh by 17325.66 MWh and the open, unconfirmed PR #938 layout (1539447.1174 MWh, recomputed) by 4353.35 MWh, with no confirmed V3R1T4S 64-turbine known-known in the claim's status snapshot, so it meets the full success criterion for the 64-turbine cell.

pass: true
