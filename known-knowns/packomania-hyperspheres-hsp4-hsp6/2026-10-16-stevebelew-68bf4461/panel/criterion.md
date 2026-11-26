# CRITERION verdict for claim N81 (d=4, N=81)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Files read: CLAIM.md, REPRODUCE.md, hsp4-81-candidate.txt, hsp4-81-posted.txt, hsp4_radius_as_fetched.txt (all relative to the claim folder). Nothing else was read.

Method: I wrote my own checker (not the REPRODUCE.md script), run as `python -I check81.py claim/` with the venv interpreter, mpmath at mp.dps = 50, no tolerance anywhere. Parsing: candidate file = skip the one "#" line, then every line must have exactly 4 tokens; posted file = first line is the radius, each later line must have exactly 5 tokens "index x1 x2 x3 x4". Pairwise distances are computed with mpmath sqrt from the parsed mpf coordinates; r* = min(dmin/2, 1 - max norm).

Full output of that run (verbatim):

```
dimension of every candidate point = 4: True
N candidate = 81 | N posted = 81
candidate sig digits per coordinate (min,max): 15 17
duplicate candidate points: False
cand: dmin/2 = 0.25408038179202321225 | 1-maxnorm = 0.25408038179177490302 | r* = 0.25408038179177490302
cand r* 15 sig = 0.254080381791775
cand binding constraint: container
all cand centres within 1-r*: True | max norm = 0.74591961820822509698 | 1-r* = 0.74591961820822509698
posted: dmin/2 = 0.25405866935070047925 | 1-maxnorm = 0.25405866935045098641 | r* = 0.25405866935045098641
posted header radius = 0.254058669351 | |r*posted - header| = 5.4901e-13
table rows for N=81: [['81', '0.254058669351']] | total rows = 299 | Ns unique: True
table decimals: 12
gain = r*cand - table = 2.1712440774903e-5
gain >= 1e-10 (strict mpf compare): True | rc > table: True
claimed gain ~2.17e-05: 2.17e-5
posted r* at most table (table not understated): True -5.4901e-13
len multisets 3240 3240
max |sorted dist diff| = 0.06457333035 | count > 1e-8 = 3240
max |sorted norm diff| = 0.3338790579
header: # N=81 r_float=0.25408038179177495 table=0.254058669351 gain=2.171e-05
|r_float header - r*| = 4.6975e-17
```

## Clause-by-clause

1. "N centers in R^d (d in {4,5,6}) for one N listed in the live radius.txt"
   - Verdict: PASS (from files). 81 lines of exactly 4 coordinates, no duplicates, so d=4, N=81. Row "81 0.254058669351" is present in hsp4_radius_as_fetched.txt (299 rows, N unique). The word "live" depends on the NOVELTY skeptic's re-fetch; from the snapshot the row exists.

2. "FEASIBLE radius r* := min( min over pairs i,j of |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance"
   - Verdict: PASS. Computed exactly as stated: dmin/2 = 0.254080381792023..., 1 - max norm = 0.254080381791774903..., so r* = 0.25408038179177490302 (the container is the binding constraint, by about 2.5e-13). Container convention checked: every centre has norm at most 1 - r* (max norm + r* = 1 to 50 digits, i.e. the outermost ball is exactly tangent to the unit sphere, as a min() definition forces). The r* is the min of the two terms, not the pair term alone, so no stretched definition. r* to 15 significant digits: 0.254080381791775. The candidate header's r_float agrees with the 50-digit r* to 4.7e-17 (a float64 rendering of the same number, not a different claim).

3. "STRICTLY GREATER (direction: max) than that file's 12-decimal value for N ... by at least 1e-10"
   - Verdict: PASS (against the snapshot). Table value 0.254058669351 (12 decimals confirmed). gain = r*cand - table = 2.1712440774903e-05 (15 significant digits), compared as mpf with no tolerance: gain >= 1e-10 is True and r* > table is True. The gain is about 2.2e5 times the 1e-10 margin, so no rounding artefact can flip it. Parser sanity: r* of the posted packing computed the same way is 0.25405866935045... which rounds to the table's 0.254058669351 (difference 5.5e-13, below the 12-decimal rounding), so the posted file, the table row, and my parser are mutually consistent. Note also r* for N=81 (0.254080) stays below the table's N=80 value (0.255463163131), so the result does not contradict monotonicity in N, which would have signalled a mislabelled N.

4. "re-fetched live immediately before claiming"
   - Verdict: NOT VERIFIABLE BY ME. CLAIM.md records a fetch of radius.txt at 2026-10-16 16:29:32 UTC, HTTP 200, byte-identical to the 2026-10-14 fetch. I cannot confirm the live value from the files; this depends on the NOVELTY skeptic. Not counted as failed.

5. "not isometric to the posted hsp4-81.txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)"
   - Verdict: PASS. Both multisets have C(81,2) = 3240 entries. Maximum entrywise difference of the sorted multisets is 0.0646, and all 3240 positions differ by more than 1e-8. The sorted pairwise-distance multiset is invariant under every isometry of R^4 (including reflections and relabelling), so a difference anywhere rules out isometry. Independently, the sorted centre-norm multisets differ by up to 0.334, so the two packings also differ as configurations relative to the container centre. The configurations are clearly different objects, not a re-polish of the posted one.

6. "(d, N) does not appear in a History-of-updates entry on the live hsp4.html newer than the one the scout fetched"
   - Verdict: NOT VERIFIABLE BY ME. CLAIM.md gives the expected "Last update: 06-Jul-2025" via REPRODUCE.md; no history page snapshot is in the claim folder. Depends on the NOVELTY skeptic's live fetch.

7. QUEUE RULE: "the N must NOT lie inside any range listed for this category on pending-requests.html re-fetched at verification time"
   - Verdict: NOT VERIFIABLE BY ME. CLAIM.md records no hsp4 entry on 2026-10-16 16:29:32 UTC. Depends on the NOVELTY skeptic's live fetch.

8. Mandatory caveat: "The 26-Sep-2026 'Moki & Julio *many* 4666 candidates' bundle is category-unspecified and cannot be resolved; the verdict must state this caveat"
   - Caveat stated here as required: the 26-Sep-2026 "Moki & Julio *many* 4666 candidates" bundle on Packomania's pending-requests page is category-unspecified and cannot be resolved; N=81 in hsp4 must be re-checked against the live table once that bundle disappears from the pending list. CLAIM.md records this caveat itself.

9. "No submission (email) is ever made; the claim is for the verified construction only."
   - Verdict: PASS as recorded. CLAIM.md claims only the verified construction; nothing in the folder indicates a submission.

## Stretch / subsumption hunt

- Container radius: unit ball, origin-centred, confirmed by the max-norm check (not a radius-of-enclosing-ball or a 1+r container).
- Rounding artefact: gain is 2.2e-05, five orders above the margin; the posted packing's own r* reproduces the table row to 5.5e-13, so the comparison is apples to apples.
- Mislabelled N: 81 points counted directly; consistent with the N=80/82 table neighbours.
- One cell only: the claim names a single (d, N) = (4, 81). CLAIM.md's note about earlier confirmed cells (68, 69, 74, 75, 76) concerns different N and does not subsume this one; N=81 is not among them.
- Definition of r*: the min() over both terms was applied; the pair term is larger than the container term here, so quoting dmin/2 alone would have overstated r* by 2.5e-13, but the claimed 0.254080381791775 is the correct min.
- Null model: not needed. The object is an explicit, deterministic point set judged by a deterministic 50-digit checker against a published table value; there is no stochastic selection step to control for. I agree with the instruction on this.

## Scope

confirmed_scope: From the files alone, the 81 four-dimensional centres in hsp4-81-candidate.txt have feasible radius r* = 0.254080381791775 (mpmath, 50 digits, no tolerance, every centre within 1 - r* of the origin) in the unit 4-ball, exceeding the snapshot Packomania hsp4 table value 0.254058669351 for d=4, N=81 by 2.1712440774903e-05 (above the 1e-10 margin), and are not isometric to the posted hsp4-81 packing (all 3240 sorted pairwise distances differ by more than 1e-8); the live-table, history-page and queue-page clauses depend on the NOVELTY skeptic's re-fetch and carry the unresolved Moki & Julio bundle caveat.

pass: true
