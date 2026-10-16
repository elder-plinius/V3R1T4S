# CRITERION skeptic verdict: N67 (d=4)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Files read: CLAIM.md, REPRODUCE.md, hsp4-67-candidate.txt, hsp4-67-posted.txt, hsp4_radius_as_fetched.txt. Nothing else.
Method: my own checker (crit67.py, written in a scratch directory, NOT the script in REPRODUCE.md), mpmath at mp.dps = 50, run with the project venv python and -I. Strict parser: candidate must be exactly one "#" line then lines of exactly 4 numeric tokens; posted file must be one radius line then "index x1 x2 x3 x4" with indices 1..67 contiguous; table row selected by exact token match "67".

Command: python -I crit67.py (argument: the claim folder)
Real output:

    candidate: comment lines = 1  data lines = 67  N = 67
    posted: header radius = 0.264026543809  N = 67  indices 1..67 contiguous = True
    table row for N=67: "67 0.264026543809"  (decimals = 12, rows in file = 299, N range 2..300)
    dim check: all candidate rows have 4 coords: True
    candidate: min pair half-dist = 0.26407220586965137158  1-maxnorm = 0.26407220586962721961
    candidate r* (50 dps)         = 0.264072205869627219605564806722
    candidate r* (15 sig)         = 0.264072205869627
    container: max |c_i| = 0.73592779413037278039  all |c_i| at most 1 - r*: True  binding side: boundary
    posted: r* = 0.2640265438085066801  |r*posted - table| = 4.9332e-13
    gain = r*cand - table = 4.56620606272196e-5   strictly above table: True   gain at least 1e-10: True
    gain / 1e-10 = 456620.61
    rounding check: table +/- 5e-13 band: r*cand - (table+5e-13) = 4.566206e-5
    pairs = 2211  max |sorted dist diff| = 0.015099516  count above 1e-8 = 2211
    candidate min pair dist positive: True  duplicate points: 0
    header line: # N=67 r_float=0.26407220586962721 table=0.264026543809 gain=4.566e-05 moves=10

## Clause-by-clause

1. "N centers in R^d (d in {4,5,6}) for one N listed in the live radius.txt"
   VERDICT: met on the files. d = 4 (every candidate row has exactly 4 coordinates), N = 67 (exactly 67 data lines, no duplicates, no mislabelling: header says N=67, posted file has 67 indexed points, table row is "67"). One N, one cell. The note about N in (68, 69, 74, 75, 76) is a separate earlier matter and does not widen this claim. "Listed in the LIVE file" depends on the NOVELTY skeptic's re-fetch; the snapshot hsp4_radius_as_fetched.txt lists 67 (299 rows, N = 2..300).

2. "FEASIBLE radius r* := min( min over pairs i,j of |c_i - c_j| / 2, 1 - max_i |c_i| ) (unit container ball centred at the origin), computed in mpmath at 50 digits directly from the submitted coordinates with no tolerance"
   VERDICT: met. Computed exactly as stated, no tolerance, mp.dps = 50, straight from hsp4-67-candidate.txt. r* = 0.264072205869627 (15 sig; 50-digit value 0.264072205869627219605564806722...). The binding term is the boundary term 1 - max|c_i| = 0.26407220586962721961 (max norm 0.73592779413037278039); the pair term is 0.26407220586965137158, larger by 2.4e-14, so both terms are essentially tight, which is what an optimised packing looks like. Container convention confirmed independently: applying the same formula to Packomania's posted coordinates reproduces the table value to 4.9e-13 (within 12-decimal rounding), so the posted packing and the candidate are judged in the same container (unit ball, origin, radius 1); no wrong-container-radius stretch.

3. "STRICTLY GREATER (direction: max) than that file's 12-decimal value for N ... by at least 1e-10"
   VERDICT: met literally on the snapshot. Table value 0.264026543809 (12 decimals). gain = 4.56620606272196e-5, at least 1e-10 (about 456,621 times the margin). Not a rounding artefact: even against the top of the table's rounding band (table + 5e-13) the gain is still 4.566e-5. "Re-fetched live immediately before claiming": CLAIM.md records a fetch at 2026-10-16 16:29:32 UTC, HTTP 200, byte-identical to the 2026-10-14 fetches; I cannot verify liveness from the files, that is the NOVELTY skeptic's job. If the live row for 67 is unchanged at 0.264026543809, this clause holds.

4. "not isometric to the posted hsp4-67.txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)"
   VERDICT: met. 2211 = C(67,2) sorted distances compared position-wise; max difference 0.0151, and all 2211 positions differ by more than 1e-8. The sorted multiset is invariant under every isometry (rotation, reflection, translation), so this is a sound test; the two configurations are not isometric. It is also implied by clause 3 (different min distance / different r*), but checked directly anyway.

5. "(d, N) does not appear in a History-of-updates entry on the live hsp4.html newer than the one the scout fetched"
   VERDICT: not verifiable from the files; not counted as failed. CLAIM.md names hsp4.html as status_source and REPRODUCE.md expects "Last update: 06-Jul-2025". Depends on the NOVELTY skeptic's live fetch of hsp4.html.

6. QUEUE RULE: "N must NOT lie inside any range listed for this category on pending-requests.html re-fetched at verification time" plus the mandatory caveat
   VERDICT: as recorded, met; not verifiable from the files. CLAIM.md records no hsp4 entry on pending-requests.html at 2026-10-16 16:29:32 UTC. Mandatory caveat, stated here as the criterion requires: the 26-Sep-2026 "Moki & Julio *many* 4666 candidates" bundle is category-unspecified and cannot be resolved; N = 67 must be re-checked against the live table once that bundle disappears from the pending list. Depends on the NOVELTY skeptic's live re-fetch.

7. "No submission (email) is ever made; the claim is for the verified construction only"
   VERDICT: consistent; CLAIM.md claims only the construction.

## Stretch hunt

- Rounding artefact: no (gain is 4.6e-5, five orders of magnitude above the 1e-10 margin and the 5e-13 table rounding).
- Wrong container radius / centre: no (posted packing reproduces its table value under the identical formula; candidate's max norm is 1 - r* exactly, so it is tight against the unit sphere, not a smaller or larger ball).
- Mislabelled N: no (67 everywhere).
- More than one cell: no (single N = 67; the 68/69/74/75/76 note is explicitly separate).
- Tolerance smuggled into r*: no (my checker uses none; REPRODUCE.md's checker uses none either).
- Precision: coordinates carry 17 significant digits; r* computed at 50 digits; the 15-digit figure 0.264072205869627 is stable.
- Partial wins: none claimed and none needed; this is judged against the full criterion.

## Null model

Not needed, and I agree with the brief: the object is explicit and the criterion is a deterministic computation on it (min over pairs, max over norms, compare to a fixed number). There is no statistical hypothesis to test against chance; a null model would add nothing.

## What this verdict depends on

Clauses 1 (live listing), 3 (live table row), 5 (history) and 6 (queue) rest on live re-fetches that I did not perform; CLAIM.md's recorded fetches are consistent with them holding. Everything computable from the submitted files is confirmed by my own 50-digit check.

confirmed_scope: From hsp4-67-candidate.txt alone, in d=4 with N=67, the feasible radius computed at 50 digits with no tolerance in the unit ball centred at the origin is r* = 0.264072205869627, which exceeds the snapshot table value 0.264026543809 by 4.56620606272196e-5 (at least the required 1e-10) and is not isometric to the posted hsp4-67 configuration (all 2211 sorted pairwise distances differ by more than 1e-8); the live table, history-of-updates and queue clauses are consistent with CLAIM.md's recorded fetches but were not re-fetched by me.

pass: true
