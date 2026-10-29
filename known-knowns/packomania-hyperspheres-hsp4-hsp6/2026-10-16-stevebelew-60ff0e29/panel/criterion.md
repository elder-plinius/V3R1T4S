# CRITERION verdict — hsp4, N = 91

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Files read: CLAIM.md, REPRODUCE.md, hsp4-91-candidate.txt, hsp4-91-posted.txt, hsp4_radius_as_fetched.txt (all in the claim folder; nothing else).

Method: my own script (check_n91.py, written from scratch, not REPRODUCE.md's script) run with the project venv Python under -I, mpmath mp.dps = 50. It parses the three data files, recomputes r* exactly as the clause defines it (minimum over all pairs of half the Euclidean distance, and 1 minus the maximum norm; the smaller of the two; no tolerance anywhere), checks the container convention, the margin, the isometry test, and several stretch/rounding traps. Full output is reproduced below; every verdict cites a line of it.

## Command output (verbatim except that comparison symbols are spelled ge, gt, lt and arrows as colons, to keep this file free of angle brackets)

```
candidate file lines: 92  comment lines: 1
candidate header: # N=91 r_float=0.24699818287380881 table=0.246960900415 gain=3.728e-05
candidate fields-per-line histogram: {4: 91}
candidate malformed lines: []
posted file lines: 92  first line: 0.246960900415
posted fields-per-line histogram: {5: 91}
posted indices == 1..91: True
N candidate = 91  N posted = 91  dim = {4}
distinct candidate rows: 91

--- candidate ---
min half-distance    = 0.24699818287386051216622127656  pair (7, 37)
1 - max norm         = 0.24699818287380882063495515293
r* candidate (50dps) = 0.24699818287380882063495515293
r* candidate 15 sig  = 0.246998182873809
binding constraint   = boundary
all centres within 1-r*: True  max norm = 0.75300181712619117937
all pair dists ge 2r*  : True
--- posted ---
min half-distance    = 0.2469609004145086223244688775
1 - max norm         = 0.246960900414188106200391710947
r* posted (50dps)    = 0.246960900414188106200391710947

table rows: 299  first N: 2  last N: 300
table Ns strictly increasing: True  N range 2 .. 300
rows with N=91: [['91', '0.246960900415']]
table value for 91 = 0.246960900415  decimals in table string: 12
posted header radius = 0.246960900415  equals table string: True
|r* posted - table| = 8.118938e-13  (lt 1e-11: True )
neighbours: 90 : ['0.247386955229']  92 : ['0.246689832003']
table monotone decreasing around 91: True
candidate r* vs row 90 value: below

gain = r*cand - table = 3.72824588088206e-5
gain ge 1e-10 : True   gain gt 0: True
gain / 1e-10  = 372824.59
gain - 5e-13 ge 1e-10 : True
header r_float matches r* to 15 sig: True

pair count: 4095 4095
max |sorted dist diff| = 0.008581477   count gt 1e-8: 4095
min dist cand / posted: 0.493996365747721 0.493921800829017
max |sorted norm diff| = 0.0051618868
candidate contacts (dist within 1e-9 of 2r*): 274  boundary contacts: 85
posted contacts    (dist within 1e-9 of 2r*): 271  boundary contacts: 84

sha256[:16] candidate: 60ff0e29ee286c3b  posted: de33341e2fac7aec  table: f3ddaa944aac0147
```

## Clause-by-clause

1. "N centers in R^d (d in {4,5,6})" — PASS. hsp4-91-candidate.txt has exactly one comment line and 91 data lines, each with exactly 4 numeric fields (histogram {4: 91}, no malformed lines, 91 distinct rows). d = 4, N = 91, one object, one cell. The header's N=91 label matches the row count; the posted file also has 91 indexed rows 1..91.

2. "for one N listed in the live radius.txt" — PASS on the snapshot. hsp4_radius_as_fetched.txt has 299 rows, N = 2..300 strictly increasing, exactly one row "91 0.246960900415" with 12 decimals. That this snapshot equals the LIVE file re-fetched immediately before claiming is the NOVELTY skeptic's re-fetch; I cannot verify it from the folder (not counted as failed; the margin verdict in clause 4 is conditional on the live row still reading 0.246960900415).

3. "FEASIBLE radius r* := min( min over pairs i,j |c_i - c_j| / 2, 1 - max_i |c_i| ), unit container ball centred at the origin, mpmath 50 digits, no tolerance" — PASS. Recomputed from the raw coordinate strings: min half-distance = 0.24699818287386051... (pair 7,37), 1 - max norm = 0.24699818287380882..., so r* = 0.24699818287380882063495515293 (boundary-bound; the pair term is 5.2e-14 larger, and r* is the minimum of the two, so this changes nothing). Container convention confirmed: max centre norm 0.7530018171261912 = 1 - r* exactly, every centre within 1 - r*, every pair distance ge 2 r* (both booleans True). The file is explicitly in container-radius-1 coordinates; no rescaling or alternative container radius is involved. Parser sanity: the same code on hsp4-91-posted.txt gives r* = 0.246960900414188..., within 8.1e-13 of the table string, so the convention and the parser match Packomania's.

4. "STRICTLY GREATER than that file's 12-decimal value for N by at least 1e-10" — PASS (literal). Gain = r*(candidate) - 0.246960900415 = 3.72824588088206e-05 (15 significant digits), i.e. 372,824.59 times the 1e-10 margin. Rounding-artefact check: even subtracting the table's full half-ulp (5e-13) the margin holds. The gain is also well below the N = 90 table value (0.247386955229), so this is not a mislabelled-N or off-by-one-row artefact. The header's r_float agrees with the 50-digit r* to 15 significant digits. (CLAIM.md writes "0.246998182873809..." which is the 15-significant-digit rounding of 0.24699818287380882; harmless.)

5. "not isometric to the posted hsp4-91.txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)" — PASS. Both multisets have C(91,2) = 4095 entries; the max elementwise difference of the sorted lists is 8.58e-03 and ALL 4095 entries differ by more than 1e-8. The sorted multiset is invariant under every isometry of R^4 (and under relabelling), so this is a valid certificate of non-isometry. Corroborating: sorted centre-norm multisets differ by up to 5.2e-03, contact counts differ (274 vs 271 sphere contacts, 85 vs 84 boundary contacts), and the minimum pair distances differ (0.4939963657 vs 0.4939218008). The two packings are nearby in the same basin (max distance difference under 1e-2), which is permitted by the clause as written; the clause asks only for non-isometry, which is met by a factor of about 1e6.

6. "(d, N) does not appear in a History-of-updates entry on the live hsp4.html newer than the one the scout fetched" — NOT VERIFIABLE from the folder. CLAIM.md records the expected "Last update: 06-Jul-2025" and REPRODUCE.md gives the one-shot curl; the live check is the NOVELTY skeptic's job. Not counted as failed; the pass below depends on it.

7. QUEUE RULE — NOT VERIFIABLE from the folder. CLAIM.md records "no hsp4 entry on 2026-10-16 16:29:32 UTC" and the mandatory caveat that the 26-Sep-2026 "Moki & Julio *many* 4666 candidates" bundle is category-unspecified and cannot be resolved; per the criterion the verdict must carry this caveat and N = 91 must be re-checked against the live table once that bundle leaves the pending list. I carry the caveat here. The live check is the NOVELTY skeptic's job; not counted as failed.

8. "No submission (email) is ever made" — consistent: CLAIM.md claims only the verified construction; nothing in the folder indicates a submission.

## Stretch / hidden-quantifier hunt

- Container radius: unit ball, origin-centred, confirmed numerically (max norm = 1 - r*). Not stretched.
- Tolerance: none used; comparisons are exact mpf at 50 digits on the raw 17-significant-digit strings. The result is far from any tolerance edge (gain 3.7e-05 vs 1e-10 margin).
- N label: 91 data rows, 91 posted rows, table row 91. Not mislabelled; candidate r* sits strictly between the N = 90 and N = 92 table values as a new N = 91 record should.
- Cells: exactly one (d = 4, N = 91). The CLAIM.md note about N in (68, 69, 74, 75, 76) concerns other cells; N = 91 is not among them, so the "better packing for the same cell" sentence does not subsume this claim from the evidence in the folder. Whether an earlier N = 91 improvement exists in the run history is outside this folder and does not affect the criterion's literal clauses.
- Dimension: every row has 4 coordinates; no padding or dropped coordinate.
- Null model: not needed. The criterion is a deterministic predicate on an explicit object (compute r* from the coordinates, compare to a fixed number, compare a sorted multiset); there is no sampling, no estimate, and no chance mechanism for a null model to calibrate. I agree with the instruction's position and do not object.

## Scope

confirmed_scope: The 91 centres in hsp4-91-candidate.txt lie in the unit 4-ball centred at the origin and, computed at 50 digits with no tolerance exactly as the criterion defines, have feasible radius r* = 0.246998182873809 (binding constraint: boundary), exceeding Packomania's snapshotted 12-decimal hsp4 table value for N = 91, 0.246960900415, by 3.72824588088206e-05 (above the 1e-10 margin), and their sorted pairwise-distance multiset differs from that of the posted N = 91 packing (hsp4-91-posted.txt) by up to 8.58e-03, so the two are not isometric; the live-table, history-of-updates and pending-queue clauses are not verifiable from this folder and are left to the NOVELTY skeptic, with the mandatory caveat that the category-unspecified 26-Sep-2026 bundle cannot be resolved.

Verdict: every clause that can be decided from the submitted files is met literally and by a wide margin; nothing is stretched. Pass is conditional only on the three live-site clauses (2, 6, 7) that this skeptic cannot check and that are assigned to the NOVELTY skeptic.

pass: true
