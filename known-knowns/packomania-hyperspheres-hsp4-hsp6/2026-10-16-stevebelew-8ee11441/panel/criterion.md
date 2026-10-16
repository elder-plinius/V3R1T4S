# CRITERION verdict, claim N94 (d=4, N=94)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Read: CLAIM.md, REPRODUCE.md, hsp4-94-candidate.txt, hsp4-94-posted.txt, hsp4_radius_as_fetched.txt (nothing else). All numbers below come from my own script (mpmath, mp.dps = 50, run with python -I in a private scratch directory), not from REPRODUCE.md. The script parses the candidate file as lines of exactly 4 tokens (skipping the one "#" header line), the posted file as lines of exactly 5 tokens (index then 4 coordinates; the radius-only first line is skipped), computes r* = min(min half pairwise distance, 1 - max norm) with no tolerance, and compares sorted pairwise-distance multisets.

Script output (verbatim):

```
candidate: points = 94  non-conforming lines = []
posted: points = 94  non-conforming lines = [(1, '0.245932827006')]
candidate coordinate tokens = 376  sig digits min/max = 15 17
duplicate candidate points: 0
radius.txt rows = 299  N=94 rows = [['94', '0.245932827006']]
table (exact decimal) = 0.245932827006
candidate: half min dist = 0.2459410195369888875859248  1-maxnorm = 0.2459410195368451990247712
candidate r* (50dps) = 0.24594101953684519902477122077410773912161071382492
candidate r* 15 sig  = 0.245941019536845
candidate max norm = 0.75405898046315480098  all inside 1-r*: True
posted: half min dist = 0.2459328270050405833579022  1-maxnorm = 0.2459328270048503541459008
posted r* (25) = 0.2459328270048503541459008  |posted r* - table| = 1.14965e-12
gain = r*cand - table = 8.19253084519902e-6  >= 1e-10: True  strictly > table: True
pair count = 4371 4371  max |sorted dist diff| = 0.009623924484  count > 1e-8 = 4371
first 3 sorted dists cand/posted: ['0.491882039074', '0.491882039074', '0.491882039074'] ['0.49186565401', '0.49186565401', '0.49186565401']
float r* = 0.24594101953684522  header says r_float=0.24594101953684522
contacts near min dist: 279  boundary contacts: 87
```

## Clause-by-clause

1. "N centers in R^d, d in {4,5,6}, for one N listed in the live radius.txt" -- PASS (local part). hsp4-94-candidate.txt holds exactly 94 lines of exactly 4 coordinates, no duplicates, 15-17 significant digits each; the snapshot hsp4_radius_as_fetched.txt has exactly one row for N=94 ("94 0.245932827006"), 299 rows total. d=4, N=94 are labelled consistently in CLAIM.md, the file names, the header line and the data. That the row is in the LIVE file is the live re-fetch (see clause 6).

2. "FEASIBLE radius r* := min(min half pairwise distance, 1 - max norm), unit container ball centred at the origin, mpmath at 50 digits directly from the submitted coordinates with no tolerance" -- PASS. Container convention checked: every candidate centre has norm at most 0.754058980463154801, i.e. all lie within 1 - r* of the origin (the boundary term is the binding one: 1 - maxnorm = 0.24594101953684519902..., half-min-distance = 0.24594101953698888758..., so r* = 0.24594101953684519902477122077410773912161071382492 to 50 digits). No tolerance was applied anywhere. A plain float64 recomputation gives 0.24594101953684522, matching the header's r_float, so the 50-digit value is not a rounding artefact. Parser sanity: the same code on hsp4-94-posted.txt gives r* = 0.24593282700485035, within 1.15e-12 of the 12-decimal table value (consistent with Packomania's coordinates being printed to 12 decimals), so the parser and the formula agree with Packomania's own convention.

3. "STRICTLY GREATER than the file's 12-decimal value for N, by at least 1e-10" -- PASS (against the snapshot). gain = r*cand - 0.245932827006 = 8.19253084519902e-06 (15 significant digits), which is strictly positive and about 81,900 times the 1e-10 margin. The claim's "about 8.19e-06" and the header's "gain=8.193e-06" are consistent with this. Literal comparison is against the live re-fetched value, which I cannot do from the files (clause 6).

4. "not isometric to the posted hsp4-94.txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)" -- PASS. Both multisets have 4371 = 94*93/2 entries; the maximum absolute difference between sorted entries is 0.00962392, and ALL 4371 sorted entries differ by more than 1e-8 (already the smallest distance differs: 0.491882039074 vs 0.491865654010). The sorted multiset is isometry-invariant, so this is a sufficient test for non-isometry. The two packings are different objects, not a re-labelling or re-rotation of the posted one.

5. "(d, N) does not appear in a History-of-updates entry on the live hsp4.html newer than the one the scout fetched" -- NOT VERIFIABLE FROM THE FILES; not counted as failed. CLAIM.md records "Last update: 06-Jul-2025" as the expected value and status_source as the hsp4.html page; nothing in the claim folder is a copy of that page. This depends on the NOVELTY skeptic's live re-fetch.

6. "re-fetched live immediately before claiming" (radius.txt) -- NOT VERIFIABLE FROM THE FILES; not counted as failed. CLAIM.md records a fetch at 2026-10-16 16:29:32 UTC, HTTP 200, byte-identical to the 2026-10-14 fetches; the snapshot hsp4_radius_as_fetched.txt is the only evidence in the folder and I cannot confirm its provenance or that the live row is still "94 0.245932827006". The margin verdict in clause 3 depends on this.

7. QUEUE RULE: "N must not lie inside any range listed for this category on pending-requests.html re-fetched at verification time" -- NOT VERIFIABLE FROM THE FILES; not counted as failed. CLAIM.md records no hsp4 entry on 2026-10-16 16:29:32 UTC. Caveat required by the criterion, stated here explicitly: the 26-Sep-2026 "Moki & Julio *many* 4666 candidates" bundle on the pending list is category-unspecified and cannot be resolved; N=94 (hsp4) must be re-checked against the live table once that bundle disappears from the pending list. This clause depends on the NOVELTY skeptic's live re-fetch of the pending-requests page.

8. "No submission (email) is ever made; the claim is for the verified construction only" -- PASS as recorded. CLAIM.md claims only the verified construction and records no submission; nothing in the folder suggests otherwise.

## Stretch hunt

- Rounding artefact: no. The 50-digit r* and the float64 r* agree to 16 digits, and the gain (8.19e-06) is 6 orders of magnitude above the table's 12-decimal rounding and 5 orders above the 1e-10 margin.
- Wrong container radius: no. The claim uses the unit ball (radius 1) centred at the origin; the boundary term 1 - max norm is the binding constraint and all 94 centres are inside the ball of radius 1 - r*. The parser-sanity check on the posted packing reproduces Packomania's table value to 1.15e-12, so the convention matches theirs.
- Mislabelled N or d: no. 94 points, 4 coordinates each, in both files; the table row read is N=94.
- More than one cell: no. The claim is for the single cell (d=4, N=94). The note in CLAIM.md about N in (68, 69, 74, 75, 76) concerns other cells and is not part of this claim; it does not subsume N=94.
- Hidden quantifiers: the criterion says "for one N" -- satisfied by N=94 alone. "Enumerated partial win": the bank entry enumerates none, so only the full criterion applies; this is judged as a full win, not a partial.
- Null model: not needed and I agree with that explicitly. The object is explicit, the checker is deterministic and tolerance-free, and the comparison is to a fixed published number; there is no statistical claim to test against chance.

## Dependencies

My pass is conditional on the three live clauses (5, 6, 7) holding as CLAIM.md records them; that re-fetch is the NOVELTY skeptic's job. Every clause I could check from the files holds literally, with wide margin.

confirmed_scope: In d=4 with N=94, the 94 centres in hsp4-94-candidate.txt lie in the unit ball centred at the origin and have tolerance-free 50-digit feasible radius r* = 0.245941019536845 (to 15 significant digits), exceeding the snapshot radius.txt table value 0.245932827006 by 8.19253084519902e-06 (at least 1e-10), and their sorted pairwise-distance multiset differs from that of hsp4-94-posted.txt by up to 0.0096 (more than 1e-8), so the configuration is not isometric to the posted one; the live-table, history-of-updates and pending-queue clauses are recorded in CLAIM.md but were not re-fetched here.

pass: true
