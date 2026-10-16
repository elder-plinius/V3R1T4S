# CRITERION skeptic verdict, claim N80 (d=4)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Method: read CLAIM.md, REPRODUCE.md and the three data files in the claim folder; wrote my own checker (not a copy of REPRODUCE.md) and ran it with the project venv python, flag -I, mpmath at 50 digits. The whole output of that single run is reproduced below; every clause verdict cites a line of it. Three comparison symbols in the raw output were spelled out in words so the file carries no angle-bracket characters.

```
candidate: points= 80  comment lines= 1  malformed= []
candidate dims: {4}
candidate half-min-dist = 0.2554696069991235410914895
candidate 1-maxnorm     = 0.2554696069848497611438025
candidate r*            = 0.2554696069848497611438025  binding: wall
candidate r* 15 sig     = 0.25546960698485
all centres inside 1-r*: True
posted: points= 80  indices= 1 .. 80  contiguous: True  header radius= 0.255463163131
posted r* = 0.2554631631305978096867369  half-min= 0.25546316313059780969  wall= 0.25546316313067595178
table rows= 299  min N= 2  max N= 300  row80 raw= '0.255463163131'
|posted r* - table| = 4.0219031e-13    |header - table| = 0.0
gain = r*cand - table = 6.44385384976114e-6   at-least-1e-10: True   strictly greater: True
gain / 1e-10 = 64438.538
pairs= 3160 3160  max sorted-dist diff = 0.012206283  count above 1e-8: 3160
min pair dist candidate = 0.51093921399824708218  (zero would mean a duplicate centre)
float64 r* = 0.2554696069848498   header claims r_float=0.25546960698484977
pairs within 1e-9 of min dist: 229
```

## Clause-by-clause

1. "N centers in R^d (d in {4,5,6}) for one N listed in the live radius.txt"
   VERDICT: met for the file content. hsp4-80-candidate.txt holds exactly 80 rows of 4 numeric coordinates (one comment line, no malformed rows, no duplicate centre: min pair distance 0.5109). d=4, N=80. The snapshot hsp4_radius_as_fetched.txt has 299 rows covering N=2..300 and contains row 80. Whether the LIVE file still lists N=80 with the same value is the novelty skeptic's re-fetch; not counted as failed.

2. "FEASIBLE radius r* := min( min over pairs of |c_i - c_j|/2, 1 - max |c_i| ), unit container ball centred at the origin, mpmath 50 digits, no tolerance"
   VERDICT: met. Computed exactly that way from the candidate coordinates: half-min-distance 0.25546960699912354..., wall term 0.25546960698484976..., so r* = 0.255469606984850 (15 significant digits), bound by the wall term. Container convention checked explicitly: every centre has norm at most 1 - r* (True), consistent with origin-centred radius-1 ball. No tolerance was applied anywhere. The posted packing, parsed with the same code, gives r* = 0.255463163130598, within 4.0e-13 of the 12-decimal table value, which confirms the parser, the container convention and the formula against Packomania's own object.

3. "STRICTLY GREATER than that file's 12-decimal value for N, by at least 1e-10"
   VERDICT: met literally on the snapshot. Table value 0.255463163131 (row "80 0.255463163131"). Gain = r* - table = 6.44385384976114e-6 (15 significant digits), i.e. 64438.5 times the 1e-10 margin; strictly greater: True. Not a rounding artefact: the gain exceeds the table's half-ulp (5e-13) by seven orders of magnitude, and the float64 recomputation (0.2554696069848498) agrees with the 50-digit value, so the claim does not depend on digit tricks. The phrase "re-fetched live immediately before claiming" depends on the novelty skeptic's fetch; CLAIM.md records a 2026-10-16 16:29:32 UTC fetch byte-identical to the 2026-10-14 one.

4. "not isometric to the posted hsp4-80.txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)"
   VERDICT: met. Both multisets have 3160 entries; the maximum sorted-entry difference is 0.0122, and all 3160 entries differ by more than 1e-8. Since the sorted pairwise-distance multiset is invariant under every isometry of R^4 (rotations, reflections, translations), this rules out isometry outright; no almost-isometric relabelling could reconcile a 1.2e-2 gap.

5. "(d, N) does not appear in a History-of-updates entry on the live hsp4.html newer than the one the scout fetched"
   VERDICT: cannot be verified from the claim folder (no copy of hsp4.html is included). CLAIM.md records the expected "Last update: 06-Jul-2025" and REPRODUCE.md gives the one-shot curl. Not counted as failed; the pass below is conditional on the novelty skeptic confirming it.

6. "QUEUE RULE: N must not lie inside any range listed for this category on pending-requests.html re-fetched at verification time"
   VERDICT: cannot be verified from the claim folder. CLAIM.md records no hsp4 entry on 2026-10-16 16:29:32 UTC. Mandatory caveat, stated as the criterion requires: the 26-Sep-2026 "Moki & Julio many 4666 candidates" bundle is category-unspecified and cannot be resolved, so N=80 must be re-checked against the live table once that bundle leaves the pending list. Conditional on the novelty skeptic's re-fetch.

7. "No submission (email) is ever made; the claim is for the verified construction only"
   VERDICT: consistent. CLAIM.md and REPRODUCE.md describe only verification; nothing in the folder indicates a submission.

## Stretch hunt

- Container radius: correct (1, origin); verified both by the inside-check and by reproducing the posted value to 4e-13.
- N mislabel: candidate has 80 points, posted has 80 points with contiguous indices 1..80, table row is 80. Consistent.
- Rounding artefact: no (gain 6.4e-6 versus 12-decimal rounding of 5e-13).
- Multiple cells: this claim concerns a single (d, N) = (4, 80). The CLAIM.md note about N in (68, 69, 74, 75, 76) refers to other cells and does not subsume or get subsumed by N=80.
- Partial wins: the bank entry enumerates no partial win; the only target is the full criterion, and the result is judged against that.
- Null model: not needed and I agree with that. The object is explicit and the checker is deterministic; there is no stochastic claim to compare against chance. The relevant control is the posted packing, which the same code reproduces to 4e-13.
- Hidden quantifiers: "for one N listed" is satisfied by a single N; "re-fetched live" and "at verification time" are the two live dependencies noted in clauses 3, 5 and 6.

confirmed_scope: For d=4, N=80, the 80 centres in hsp4-80-candidate.txt lie in the origin-centred unit 4-ball with feasible radius r* = 0.255469606984850 (mpmath 50 digits, no tolerance, wall-bound), exceeding the snapshot table value 0.255463163131 by 6.44385384976114e-6 (above the 1e-10 margin), and are not isometric to hsp4-80-posted.txt (all 3160 sorted pairwise distances differ, max 1.22e-2); the live-table, history and pending-queue clauses are recorded in CLAIM.md but not re-fetched here, and the Moki and Julio bundle caveat applies.

pass: true
