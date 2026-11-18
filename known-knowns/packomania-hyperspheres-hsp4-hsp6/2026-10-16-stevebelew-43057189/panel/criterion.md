# CRITERION verdict: hsp4 N=89

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Method: read CLAIM.md, REPRODUCE.md and the three data files in the claim folder only. Wrote my own checker (mpmath, mp.dps = 50, no tolerance, Python run with -I) in a private scratchpad subdirectory and ran it against the claim folder. Full output is reproduced at the end; the labels "at-least", "strictly-greater" and "exceeding" are my own output labels for the comparisons they name.

## Clause-by-clause

1. "N centers in R^d (d in {4,5,6}) for one N listed in the live radius.txt"
   - hsp4-89-candidate.txt: 90 lines = 1 comment line + 89 coordinate rows, every row 4 numbers, 89 distinct rows. d=4, N=89.
   - hsp4_radius_as_fetched.txt: 299 two-column rows, N = 2..300, row "89 0.247998099891" present.
   - Verdict: PASS (the "live" part of this clause depends on the NOVELTY skeptic's re-fetch; the snapshot in the folder is what I checked).

2. "FEASIBLE radius r* := min( min over pairs i less than j of |c_i - c_j| / 2, 1 - max_i |c_i| ), unit container ball centred at the origin, mpmath 50 digits, directly from the submitted coordinates, no tolerance"
   - Candidate: dmin/2 = 0.24800542008473357698, 1 - maxnorm = 0.24800542008440667899; the container term is binding, so r* = 1 - max|c_i|.
   - r* (50 digits) = 0.24800542008440667899066559596859197503166605598113; to 15 significant digits 0.248005420084407, which matches the value quoted in CLAIM.md. The float64 reproduction 0.24800542008440662 matches the file's comment line. No tolerance was applied; every centre satisfies |c_i| at most 1 - r* and every pair distance is at least 2 r* (both checked at 50 digits and printed True).
   - Container convention confirmed: radius 1, origin-centred; the candidate's largest norm is 0.751994579915593..., i.e. exactly 1 - r*.
   - Verdict: PASS.

3. "STRICTLY GREATER than that file's 12-decimal value for N, by at least 1e-10"
   - table = 0.247998099891; gain = r*cand - table = 7.32019340667899e-06 (15 significant digits). strictly-greater: True; at-least 1e-10: True. The margin is about 73,000 times the required 1e-10, so this is not a rounding artefact.
   - Parser sanity: r* recomputed from hsp4-89-posted.txt is 0.24799809989033811122, which differs from the table value by 6.6e-13, within the table's 12-decimal rounding; so the posted file, the table row and my loader are mutually consistent.
   - Verdict: PASS (against the snapshot; the live re-fetch is the NOVELTY skeptic's clause).

4. "not isometric to the posted hsp4-89.txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)"
   - Both multisets have 3916 entries. Max |sorted distance difference| = 0.011206352; all 3916 positions differ by more than 1e-8. The minimum pair distances also differ (0.496010840169467 vs 0.49599619978092). The sorted multiset is isometry-invariant, so this is a valid non-isometry certificate.
   - Verdict: PASS.

5. "(d, N) does not appear in a History-of-updates entry on the live hsp4.html newer than the one the scout fetched"
   - Not verifiable from the claim folder. CLAIM.md records the expected "Last update: 06-Jul-2025" and REPRODUCE.md gives the curl command. Depends on the NOVELTY skeptic's live fetch. Not counted as failed.

6. QUEUE RULE: "N must NOT lie inside any range listed for this category on pending-requests.html re-fetched at verification time"
   - Not verifiable from the claim folder. CLAIM.md records no hsp4 entry on 2026-10-16 16:29:32 UTC. Depends on the NOVELTY skeptic's live fetch. Not counted as failed.
   - Mandatory caveat (stated here as the criterion requires): the 26-Sep-2026 "Moki & Julio *many* 4666 candidates" bundle on the pending list is category-unspecified and cannot be resolved; N=89 must be re-checked against the live hsp4 table once that bundle disappears from the pending list.

7. "No submission (email) is ever made; the claim is for the verified construction only"
   - CLAIM.md makes no submission claim and claims only the construction. Consistent.

## Stretch hunt

- Mislabelled N: no; 89 rows in the candidate, 89 rows in the posted file, table row 89 used.
- Wrong container radius: no; r* is bound by 1 - max|c_i| with radius 1, exactly the clause's definition. Any larger container assumption would have been visible as a slack container term, and it is not.
- Rounding artefact: no; gain is 7.32e-06, five orders of magnitude above the 1e-10 floor and the 5e-13 table rounding.
- More than one cell: no; the claim names a single cell d=4, N=89. The note in CLAIM.md about N in (68, 69, 74, 75, 76) concerns other N values and does not list 89; nothing in the folder records an earlier confirmed N=89 improvement, so I see no subsumption from within the folder (anything outside the folder is not mine to read).
- Trivial transform of the posted packing: no; every sorted pair distance differs, and a rescaling would not be an isometry anyway.
- Enumerated partial wins: none are needed; the full criterion is met on every clause I can check.

## Null model

Not needed and not applicable: the object is explicit and the criterion is a deterministic computation on it (minimum pair distance, maximum norm, exact comparison to a published constant). There is no statistical question for a null model to answer. I agree with the instruction on this point.

## Checker output (verbatim)

```
hsp4-89-candidate.txt: 90 lines; first line repr: '# N=89 r_float=0.24800542008440662 table=0.247998099891 gain=7.320e-06'
hsp4-89-posted.txt: 90 lines; first line repr: '0.247998099891'
N cand 89 N posted 89 dims {4}
distinct cand rows 89
table rows 299 N range 2 300 all 2-col: True
row 89: [['89', '0.247998099891']]
cand: dmin/2 = 0.24800542008473357698  1-maxnorm = 0.24800542008440667899  binding: container
cand r* (50dps) = 0.24800542008440667899066559596859197503166605598113
cand r* 15 sig  = 0.248005420084407
posted: dmin/2 = 0.24799809989045992188  1-maxnorm = 0.24799809989033811122
posted r*       = 0.24799809989033811122  |posted r* - table| = 6.6189e-13
table           = 0.247998099891
gain = r*cand - table = 7.32019340667899e-6  at-least 1e-10: True  strictly-greater: True
all cand centres within 1 - r*: True
all cand pair dists at-least 2 r*: True
pair count 3916 3916
max |sorted dist diff| = 0.011206352  count exceeding 1e-8: 3916
cand dmin = 0.496010840169467  posted dmin = 0.49599619978092
float64 r* = 0.24800542008440662
```

confirmed_scope: For d=4, N=89, the 89 centres in hsp4-89-candidate.txt lie in the origin-centred unit ball with feasible radius r* = 0.248005420084407 (mpmath 50 digits, no tolerance), exceeding the snapshot table value 0.247998099891 by 7.32019340667899e-06 and not isometric to hsp4-89-posted.txt; the live-table, history and queue clauses are deferred to the NOVELTY skeptic and the Moki and Julio bundle caveat stands.

pass: true
