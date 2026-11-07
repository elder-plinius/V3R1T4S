# CRITERION verdict: hsp4, N = 111

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Files read: CLAIM.md, REPRODUCE.md, hsp4-111-candidate.txt, hsp4-111-posted.txt, hsp4_radius_as_fetched.txt (nothing else). I did not run the REPRODUCE.md script; I wrote my own checker (mpmath, mp.dps = 50, run with python -I) and ran it against the three data files. The output quoted below is that script's real output.

## Checker output (verbatim)

```
candidate total lines 112 comment lines 1 coordinate rows 111
candidate rows with field count != 4: []
candidate rows: all 4 fields numeric regex: True
posted first line 0.237355353009  posted coordinate rows 111  field counts {5}  indices 1..111: True
dimension check: every candidate row has exactly 4 coords: True
candidate N = 111  pairs = 6105 (expected 6105)
candidate half-min-pair-dist = 0.2373595700277416871
candidate 1 - max norm       = 0.2373595700275016628
candidate r*                 = 0.2373595700275016628  15 sig = 0.237359570027502
candidate max norm = 0.7626404299724983372  all centres within 1 - r*: True  max norm + r* = 1.0
candidate min pair dist = 0.47471914005548337419  at least 2 r*: True
candidate duplicates (pair dist below 1e-6): 0
candidate binding: half-dist - (1-maxnorm) = 2.400242936e-13
posted r* = 0.23735535300820492224  posted half-min = 0.23735535300826185779  posted 1-maxnorm = 0.23735535300820492224
table rows = 299  rows for N=111 = [['111', '0.237355353009']]  first/last N = 2 300  Ns consecutive 2..300: True
table value = 0.237355353009  decimals = 12
|posted r* - table| = 7.9507776e-13  (below 1e-11 parser sanity: True )
gain = r*cand - table = 4.2170185016628e-6  at least 1e-10: True  ratio to 1e-10: 42170.185
strictly greater: True
gain minus 5e-13 (table half-ulp) still at least 1e-10: True
float64 r* = 0.23735957002750163  header r_float = # N=111 r_float=0.23735957002750163 table=0.237355353009 gain=4.217e-06
sorted-dist multiset: max |diff| = 0.0043084619  count above 1e-8: 6105  of 6105
min pair dist cand vs posted: 0.474719140055 0.474710706017  max norm cand vs posted: 0.762640429972 0.762644646992
sorted-norm max |diff| = 0.0021926338
table 110 = 0.237733257728  cand r* - that = -0.0003736877
table 112 = 0.237131194237  cand r* - that = 0.00022837579
r* 25 digits = 0.2373595700275016628022979
gain 20 digits = 4.2170185016628022979e-6
gain 15 sig    = 4.21701850166280e-6
```

## Clause-by-clause

1. "N centers in R^d (d in {4,5,6}) for one N listed in the live radius.txt": hsp4-111-candidate.txt has exactly 1 comment line and 111 coordinate rows, every row exactly 4 numeric fields, no duplicate centres (0 pairs closer than 1e-6), 6105 pairs. d = 4, N = 111. Row "111 0.237355353009" is present in the snapshot hsp4_radius_as_fetched.txt (299 rows, N = 2..300 consecutive). PASS on the files; the "live" part is the NOVELTY skeptic's re-fetch (see section "Not verifiable here").

2. Container convention (unit ball centred at origin, radius 1): max centre norm = 0.76264042997249834, and max norm + r* = 1.0 to 20 digits, i.e. the container constraint is the binding one and every centre lies within 1 - r*. No other container radius would reproduce the claimed r*, so there is no wrong-container stretch. PASS.

3. r* := min( half of the minimum pairwise centre distance, 1 - max_i |c_i| ), mpmath 50 digits, no tolerance: half min pair distance = 0.23735957002774169, 1 - max norm = 0.23735957002750166, so r* = 0.2373595700275016628022979 (15 sig: 0.237359570027502), which matches the value quoted in CLAIM.md and the file's own header (r_float=0.23735957002750163; my float64 recomputation gives the identical double). The two terms differ by only 2.4e-13, so the packing is essentially tight on both constraints, as expected of a polished local optimum. PASS.

4. Strictly greater than the 12-decimal table value by at least 1e-10: table = 0.237355353009 (12 decimals confirmed). gain = r* - table = 4.21701850166280e-6 (15 sig), i.e. 42170 times the 1e-10 floor; strict inequality holds; subtracting the table's half-ulp (5e-13) does not change the verdict, so this is not a rounding artefact. Parser sanity: r* of hsp4-111-posted.txt recomputed by the same rule = 0.237355353008205, within 7.95e-13 of the table row, so the table row really is the feasible radius of the posted file under exactly this definition. PASS.

5. Not isometric to the posted configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere): the sorted multisets differ in all 6105 positions, max |diff| = 4.31e-3; independently the sorted norm multisets differ by up to 2.19e-3 and the minimum pair distance differs (0.474719140 vs 0.474710706). Far above 1e-8. PASS.

6. History-of-updates clause ((d, N) not in an entry on the live hsp4.html newer than the one the scout fetched): CLAIM.md records "Last update: 06-Jul-2025" as the expected string and states the 2026-10-16 radius.txt fetch is byte-identical to the 2026-10-14 fetch. The claim folder contains no snapshot of hsp4.html, so I cannot verify this from files; not counted as failed. Depends on the NOVELTY skeptic's live fetch.

7. Queue rule (N = 111 not inside any hsp4 range on pending-requests.html re-fetched at verification time): CLAIM.md records "no hsp4 entry on 2026-10-16 16:29:32 UTC". Not verifiable from the files; not counted as failed; depends on the NOVELTY skeptic's live fetch. Mandatory caveat, stated as the criterion requires: the 26-Sep-2026 "Moki & Julio *many* 4666 candidates" bundle on the pending list is category-unspecified and cannot be resolved, so N = 111 must be re-checked against the live hsp4 table once that bundle disappears from the pending list.

8. No submission is made: nothing in the claim folder is or describes an email or submission. PASS.

## Stretch hunt

- Mislabelled N: 111 rows counted directly; r* = 0.23735957 sits strictly between the table's N = 110 (0.23773326) and N = 112 (0.23713119) values, consistent with N = 111 and not with a neighbouring cell.
- More than one cell: the claim is for the single cell (d = 4, N = 111). The note about N in (68, 69, 74, 75, 76) concerns other cells and is not part of this claim; it does not subsume or widen this one.
- Rounding artefact: excluded (gain 4.2e-6 against a 1e-12 table resolution).
- Wrong container radius: excluded (max norm + r* = 1 exactly).
- Tolerance smuggled into the checker: none; r* is the raw minimum of the two exact terms.
- The claim says "by about 4.22e-06": the exact gain is 4.21701850166280e-6, which rounds to 4.22e-06. Consistent.

## Null model

Not needed and I agree with the brief: the object is an explicit set of 111 coordinates judged by a deterministic, tolerance-free computation against a fixed published number; there is no sampling, no statistic and no chance baseline for the feasible radius of a given point set.

## Not verifiable here

Clauses 1 ("live"), 6 and 7 rest on live fetches of radius.txt, hsp4.html and pending-requests.html, which are the NOVELTY skeptic's job. My pass below is conditional on those fetches matching what CLAIM.md records (row "111 0.237355353009", no newer History-of-updates entry for hsp4 N = 111, no hsp4 range covering 111 on the pending list), and carries the Moki & Julio caveat above.

confirmed_scope: From the files alone, hsp4-111-candidate.txt gives 111 centres in the unit 4-ball (d=4, N=111) with feasible radius r* = 0.237359570027502 computed tolerance-free in mpmath at 50 digits, exceeding the snapshot table value 0.237355353009 by 4.21701850166280e-6 (at least 1e-10), and non-isometric to hsp4-111-posted.txt (sorted distance multisets differ by up to 4.3e-3), with the live-table, history and queue clauses left to the NOVELTY skeptic and the Moki & Julio bundle caveat outstanding.

pass: true
