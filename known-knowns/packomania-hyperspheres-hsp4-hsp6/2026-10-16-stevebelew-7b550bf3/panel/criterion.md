# CRITERION verdict, claim N104 (hsp4, d=4, N=104)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Method: read CLAIM.md (criterion quoted verbatim), REPRODUCE.md, and the three data files; wrote my own independent mpmath checker (not a copy of the REPRODUCE.md snippet), run with the panel venv python with -I, mp.dps = 50, no tolerance anywhere. Full command output is reproduced under each clause; every number below is from that run.

## Clause 1: "N centers in R^d (d in {4,5,6}) for one N listed in the live radius.txt"
Verdict: PASS (locally; liveness of the table is the NOVELTY skeptic's job).
Output:
    candidate: comment lines = 1  points = 104  dims per point = {4}
    distinct candidate points = 104
    table rows total = 299  rows for N=104 = 1 [['104', '0.240535464233']]
    table N range 2 300 all distinct True
hsp4-104-candidate.txt has exactly one "#" comment line and 104 coordinate lines of 4 numbers each, all distinct; d=4, N=104, one cell only. The snapshot hsp4_radius_as_fetched.txt has exactly one row for N=104, carrying 12 decimals.

## Clause 2: container convention (unit ball centred at origin, radius 1) and the r* formula
Verdict: PASS.
Output:
    cand dmin/2 = 0.24053869780501100244
    cand 1-maxnorm = 0.24053869762389658209
    cand r* (50 dps) = 0.240538697623896582089346515939
    cand r* 15 sig = 0.240538697623897
    binding constraint = norm
    centres with norm exceeding 1-r*: []   (printed as 'norm gt 1-r*' in the raw run)
r* was computed exactly as the clause says: min over the 5356 pairs of half the distance, and 1 minus the maximum centre norm, with mpmath at 50 digits straight from the file text. The binding term is the container (1 - max norm); the pairwise term is 1.8e-10 above it, so both constraints are active to within the polish tolerance and the min is taken correctly. Every centre satisfies norm at most 1 - r* (empty violation list). The container convention is confirmed by the posted-packing sanity check in clause 5: Packomania's own posted coordinates, run through the same formula with centre at the origin and radius 1, reproduce the table value to 6.5e-13, so the convention and the parser are right.

## Clause 3: "STRICTLY GREATER than that file's 12-decimal value for N ... by at least 1e-10"
Verdict: PASS (against the snapshot; the "re-fetched live immediately before claiming" part depends on the NOVELTY skeptic's re-fetch).
Output:
    table decimals = 12
    gain = r*cand - table = 3.23339089658209e-6  at least 1e-10: True  strictly greater: True   (raw run printed the comparison operators as symbols)
    claimed gain ~3.23e-06; actual / 1e-10 = 32333.9
Candidate r* to 15 significant digits: 0.240538697623897. Table value: 0.240535464233. Gain = 3.23339089658209e-6, which is about 32,000 times the required 1e-10 margin and about 3.2 million times the table's 5e-13 rounding half-width. No rounding artefact can account for this; the candidate file carries 15 to 17 significant digits per coordinate (output: sig digit counts in candidate file = [15, 16, 17]), far beyond what is needed. The header comment's r_float=0.24053869762389657 is the double-precision rendering of the 50-digit value 0.2405386976238965820...; the 2e-18 discrepancy is immaterial and the criterion is judged on the mpmath value.

## Clause 4: "not isometric to the posted hsp4-104.txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)"
Verdict: PASS.
Output:
    pair count = 5356 5356
    max |sorted-dist diff| = 0.0052927923  count exceeding 1e-8 = 5356   (raw run printed the comparison operator as a symbol)
    min |sorted-dist diff| = 2.1248402e-7
    cand dmin = 0.48107739561002200488  posted dmin = 0.48107092846469269893
The sorted multiset of the 5356 pairwise distances is invariant under every isometry of R^4, so this is a sufficient test. Every one of the 5356 sorted entries differs by more than 1e-8 (the smallest difference is 2.1e-7, the largest 5.3e-3); the minimum pair distances alone differ by 6.5e-6. The two packings are not isometric.

## Clause 5: parser and posted-file sanity (supports clauses 2 and 3)
Verdict: PASS.
Output:
    posted: header radius = 0.240535464233  points = 104  indices 1..104 = True
    posted r* recomputed = 0.24053546423234634947  |diff vs table| = 6.53651e-13  |diff vs header| = 6.53651e-13
    posted dmin/2 = 0.24053546423234634947  1-maxnorm = 0.24053546423238794468
hsp4-104-posted.txt has the radius on line 1 and 104 lines "index x1 x2 x3 x4" with indices 1..104. Its recomputed r* matches the table row to 6.5e-13, inside the 12-decimal rounding, so the file is the N=104 posted packing (no mislabelled N) and the table row, the posted file and the container convention are mutually consistent.

## Clause 6: "(d, N) does not appear in a History-of-updates entry on the live hsp4.html newer than the one the scout fetched"
Verdict: NOT VERIFIABLE FROM THE CLAIM FOLDER; not counted as failed. CLAIM.md records that the table was re-fetched 2026-10-16 16:29:32 UTC, HTTP 200, byte-identical to the 2026-10-14 fetch, and REPRODUCE.md expects "Last update: 06-Jul-2025". If the NOVELTY skeptic's live fetch shows a newer history entry naming hsp4 N=104, or a changed row for 104, this verdict must be withdrawn.

## Clause 7: QUEUE RULE (pending-requests.html, re-fetched at verification time)
Verdict: NOT VERIFIABLE FROM THE CLAIM FOLDER; not counted as failed. CLAIM.md records no hsp4 entry on the pending page at 2026-10-16 16:29:32 UTC. Mandatory caveat per the criterion: the 26-Sep-2026 "Moki & Julio *many* 4666 candidates" bundle is category-unspecified and cannot be resolved, so N=104 must be re-checked against the live hsp4 table once that bundle disappears from the pending list. This verdict is conditional on the NOVELTY skeptic's live re-fetch confirming no hsp4 range covering 104.

## Clause 8: "No submission (email) is ever made"
Verdict: PASS as recorded; nothing in the folder indicates a submission, and the claim is for the verified construction only.

## Stretch hunt
- Hidden quantifiers: none found; the criterion is for one (d, N) and the claim names exactly one, d=4, N=104.
- Wrong container radius or centre: ruled out by clause 5 (posted coordinates reproduce the table value under the stated convention).
- Mislabelled N: ruled out (104 points in both files, table row unique, posted indices 1..104).
- Rounding artefact: ruled out (gain is 3.2e-6, four orders above the 1e-10 margin).
- More than one cell: no; the note about N in (68, 69, 74, 75, 76) concerns other cells and is not part of this claim.
- Partial win: none claimed; this is judged as a full win on the single cell.
- Null model: not needed and I agree with that explicitly. The object is explicit, the checker is deterministic, and r* is a direct function of the submitted coordinates; there is no stochastic baseline against which a "chance" improvement could be measured, and the margin is not near the rounding floor.

confirmed_scope: For d=4, N=104, the 104 centres in hsp4-104-candidate.txt lie in the unit ball centred at the origin and have feasible radius r* = 0.240538697623897 (mpmath, 50 digits, no tolerance), exceeding the Packomania hsp4 radius.txt snapshot value 0.240535464233 by 3.23339089658209e-6 (above the 1e-10 margin) and not isometric to the posted hsp4-104 packing (all 5356 sorted pairwise distances differ by more than 1e-8), with the history and queue clauses recorded in CLAIM.md but dependent on the NOVELTY skeptic's live re-fetch and on the unresolved 26-Sep-2026 category-unspecified bundle caveat.

pass: true
