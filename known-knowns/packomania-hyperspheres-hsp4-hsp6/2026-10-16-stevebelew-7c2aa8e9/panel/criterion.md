# CRITERION verdict for claim N83 (d=4)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Files read: CLAIM.md, REPRODUCE.md, hsp4-83-candidate.txt, hsp4-83-posted.txt, hsp4_radius_as_fetched.txt (claim folder only). I did not run REPRODUCE.md's script; I wrote my own mpmath script (mp.dps = 50, run with python -I in a separate scratch directory, data passed by path) and reproduced every clause I could from the files. Output below is pasted verbatim from that run.

## My script output (single run)

```
candidate: total lines 84  comment lines 1  coord rows 83  all rows have exactly 4 fields: True
posted: total lines 84  first line ['0.252008330509']  coord rows 83  all rows have 5 fields: True  indices 1..83 in order: True
candidate significant digits per coordinate: min 14 max 17
table rows 299  N range 2 .. 300  all 12-decimal: True
table row 83: [['83', '0.252008330509']]
candidate: min half-distance = 0.25201068494714287585  1-maxnorm = 0.25201068494708888664  maxnorm = 0.74798931505291111336
candidate r* (50 dps) = 0.25201068494708888664310142074008333009469420727062
candidate r* 15 sig  = 0.252010684947089
binding constraint: boundary
all centres within 1 - r*: True
posted r* (20) = 0.2520083305081919912  |posted r* - table| = 8.08009e-13
table = 0.252008330509
gain = r*cand - table = 2.35443808888664e-6  >= 1e-10: True  strictly > table: True
gain vs posted r* exact = 2.35443889689544e-6
gain / 1e-10 = 23544.38089
pair count 3403 3403  = C(83,2)= 3403
max |sorted-distance diff| = 0.01185410297  count > 1e-8: 3403  > 1e-8 somewhere: True
max |sorted-norm diff| = 0.01739869052
min pair distance candidate = 0.5040213698942857517  posted = 0.50401666101680438377
table 82 = 0.252894034506  84 = 0.251296923021  candidate r* < table(82): True
header: # N=83 r_float=0.25201068494708889 table=0.252008330509 gain=2.354e-06
```

## Clause-by-clause

1. "N centers in R^d (d in {4,5,6}) for one N listed in the live radius.txt" -- PASS (from files). hsp4-83-candidate.txt has exactly one comment line and 83 rows of exactly 4 coordinates (14-17 significant digits each); d=4, N=83. hsp4_radius_as_fetched.txt has 299 rows (N=2..300, all 12-decimal) and contains the row "83 0.252008330509". Whether that row is still live is the NOVELTY skeptic's re-fetch; CLAIM.md records a 2026-10-16 16:29:32 UTC fetch byte-identical to the 2026-10-14 snapshot.

2. "FEASIBLE radius r* := min( min_{i<j} |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance" -- PASS. My own computation at mp.dps=50, no tolerance, no rescaling, no recentering: min half-distance 0.25201068494714287585, 1 - max norm 0.25201068494708888664, so r* = 0.25201068494708888664310142074008333... (boundary constraint is the binding one, by about 5.4e-14). Container convention confirmed: max centre norm is 0.74798931505291 and every centre satisfies |c_i| <= 1 - r* (printed True). The header's r_float 0.25201068494708889 agrees with my value to double precision.

3. "STRICTLY GREATER than that file's 12-decimal value for N ... by at least 1e-10" -- PASS literally. table = 0.252008330509 (12 decimals, as in the file). gain = r* - table = 2.35443808888664e-06, which is 23544x the 1e-10 margin. Rounding artefact ruled out: the table value can be at most 5e-13 from the true posted radius, and my recomputation of the posted packing gives r* = 0.25200833050819199, within 8.1e-13 of the table (parser sanity passes; the posted file's first line 0.252008330509 also matches). The gain against the exact posted r* is 2.354438897e-06, same to 7 digits. The candidate r* is also below the table value for N=82 (0.252894034506), so this is not a mislabelled-N packing of fewer balls.

4. "not isometric to the posted hsp4-83.txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)" -- PASS. Both multisets have C(83,2)=3403 entries; the maximum entry-wise difference of the sorted multisets is 0.01185 and all 3403 entries differ by more than 1e-8. (The sorted pairwise-distance multiset is invariant under every Euclidean isometry, so this is a valid certificate of non-isometry. Sorted centre norms also differ by up to 0.0174, consistent with the two being genuinely different packings rather than a rigid motion.) The posted file was checked to have indices 1..83 in order and 5 fields per row; I parsed the last 4 fields as in the criterion's convention.

5. "(d, N) does not appear in a History-of-updates entry on the live hsp4.html newer than the one the scout fetched" -- NOT VERIFIABLE FROM THE FILES; not counted as failed. CLAIM.md records the hsp4.html last update as 06-Jul-2025 (REPRODUCE.md expected line) and the table row unchanged on 2026-10-16 16:29:32 UTC. The pass below depends on the NOVELTY skeptic's live re-fetch confirming no newer history entry for (4, 83).

6. QUEUE RULE: "the N must NOT lie inside any range listed for this category on pending-requests.html re-fetched at verification time" -- NOT VERIFIABLE FROM THE FILES; not counted as failed. CLAIM.md records no hsp4 entry on the pending page on 2026-10-16 16:29:32 UTC. Mandatory caveat carried forward: the 26-Sep-2026 "Moki & Julio *many* 4666 candidates" bundle is category-unspecified and cannot be resolved, so N=83 must be re-checked against the live table once that bundle disappears from the pending list. The pass below depends on the NOVELTY skeptic's live re-fetch of the pending page.

7. "No submission (email) is ever made; the claim is for the verified construction only" -- CONSISTENT. CLAIM.md claims only the construction; nothing in the folder indicates a submission.

## Stretch / hidden-quantifier hunt

- Container radius: unit ball at origin is used as-is; the candidate is not rescaled, and the boundary term 1 - max|c_i| is the binding term, so a wrong container radius would have changed r* directly. None found.
- N: exactly 83 coordinate rows in both files; r* sits strictly between the table values for N=82 and N=84, as expected for a genuine N=83 cell.
- One cell only: the claim is for (d=4, N=83) alone; the note about earlier confirmed improvements for N in (68, 69, 74, 75, 76) concerns other cells and does not subsume this one. Not a partial win; it is the full criterion for this one cell.
- Rounding: the 1e-10 margin is exceeded by four orders of magnitude; no digit-boundary games possible.
- Precision of the submitted coordinates: 14-17 significant digits; my 50-digit r* is computed from those literal strings, so the stated r* is a property of the submitted object, not of a higher-precision private copy.
- Null model: not needed. The object is explicit, the checker is deterministic, and the criterion is a strict inequality on a quantity computed exactly from the submitted coordinates; there is no statistical selection to correct for. I agree with the panel instruction on this point.

## Dependencies

The pass is conditional on the NOVELTY skeptic's live checks of clauses 5 and 6 (radius.txt row 83 still 0.252008330509, no newer History-of-updates entry for N=83, no hsp4 range on pending-requests.html covering 83). Every clause decidable from the submitted files passes on my independent recomputation.

confirmed_scope: For d=4, N=83, the 83 centres in hsp4-83-candidate.txt lie in the unit ball centred at the origin with feasible radius r* = 0.252010684947089 (mpmath, 50 digits, no tolerance), exceeding the snapshot Packomania table value 0.252008330509 by 2.354438e-06 (margin clause met by 23544x), and are not isometric to hsp4-83-posted.txt (sorted pairwise-distance multisets differ by up to 0.01185), with the history and queue clauses recorded in CLAIM.md as of 2026-10-16 16:29:32 UTC but left to the live re-fetch.

pass: true
