# PREREG.v4: ED target, DESCRIPTIVE ONLY (written 2026-11-13T02:58:48Z by date -u)

Written after the decisive hosp scoring (MAIN and p1 not met) and before any forecast of ours exists for the ED target
(wk inc rsv prop ed visits). PREREG.md R1 chose hosp as the primary target and said the ED target is "descriptive only,
never a claim"; this stays so. Purpose: show whether route (a)'s method family does better where the vintages carry a
longer history (NSSP data from 2022-10-01 in every vintage), to inform the human's decision on route (a).
Method: the frozen route (b) pipeline (FROZEN_PARAMS.json, unchanged code) applied mechanically to the ED series:
proportion treated as a rate with population 1 (z = log(1e5 * proportion + c)); vintage rule R5 unchanged (same
as_of dates); min_hist = 2022-10-01 (the NSSP series start; the 2024-11-09 value of PREREG.v2 is an NHSN reporting
rule that does not apply to NSSP); everything else unchanged. Fallback R8 unchanged.
Scoring: R6's statistic vs RSVHub-ensemble on its ED tasks (oracle truth), plus US/states and per-model comparisons,
all descriptive. Scored once.
