# CRITERION skeptic verdict: d=4, N=74

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Files read: CLAIM.md, REPRODUCE.md, hsp4-74-candidate.txt, hsp4-74-posted.txt, hsp4_radius_as_fetched.txt (claim folder only). Nothing else on the machine was read; no network access was used.

Method: my own mpmath script (mp.dps = 50, run with python -I, in a private scratchpad subdirectory holding copies of the three data files). It parses the 74 coordinate lines of hsp4-74-candidate.txt (skipping the single "#" comment line), computes half the minimum pairwise distance and 1 minus the maximum centre norm exactly as the clause states, with no tolerance, and compares against the table row for N = 74 and against the posted configuration.

Command (run inside the scratchpad directory, with the three data files copied there):
    python -I check.py .

Real output:
    rows in table = 299  N range 2 .. 300
    table monotone nonincreasing: True
    table[73] = 0.259369077971  table[74] = 0.258522851648  table[75] = 0.258082894946
    N candidate = 74  N posted = 74  dims all 4: True
    posted first-line radius = 0.258522851648
    candidate: half-min-dist = 0.25852965066045076359  1-maxnorm = 0.25852965066023519309  maxnorm = 0.74147034933976480691
    candidate: all centres within 1 - r*: True
    r* candidate (20 digits) = 0.25852965066023519309
    r* candidate (15 sig)    = 0.258529650660235
    r* posted    (20 digits) = 0.25852285164722350934  |rp - table| = 7.7649e-13
    table (74)   = 0.258522851648
    gain = r*cand - table = 6.79901223519309e-6  strictly greater: True  at least 1e-10: True
    ratio gain/1e-10 = 67990.122
    candidate below table[73] (sanity, not a criterion clause): True
    earlier merged value = 0.258528723899142  candidate strictly exceeds earlier: True  by 9.2676109e-7
    pairs: 2701 2701
    max |sorted distance difference| vs posted = 0.0072840872  count exceeding 1e-8: 2701
    min pair dist candidate = 0.517059301320902  posted = 0.517045703294874
    smallest 3 candidate distances: ['0.517059301321', '0.517059301321', '0.517059301321']
    comment-line r_float 0.25852965066023514 vs mp r* diff = 5.3091e-17

## Clause-by-clause

1. "N centers in R^d (d in {4,5,6}) for one N listed in the live radius.txt" -- VERIFIED from files. hsp4-74-candidate.txt holds exactly 74 lines of 4 coordinates; the snapshot hsp4_radius_as_fetched.txt has 299 rows (N = 2..300) including row "74 0.258522851648". One cell only (d = 4, N = 74); the file name, the comment line, CLAIM.md and the coordinate count all agree on N = 74. Whether the snapshot matches the live file is the NOVELTY skeptic's job (see 7).

2. Container convention and r* definition -- VERIFIED. Unit ball centred at the origin, radius 1: maximum centre norm is 0.74147034933976480691, so every centre lies within 1 - r* (checked explicitly: True). r* = min(half-min-distance, 1 - max norm) = min(0.25852965066045076, 0.25852965066023519) = 0.25852965066023519309; the binding constraint is the container, with the half-min-distance clear of it by 2.2e-13. Computed at mp.dps = 50 with no tolerance from the submitted coordinates. Parser sanity: the same code applied to hsp4-74-posted.txt gives 0.258522851647224, which agrees with the 12-decimal table value to 7.8e-13, so the parsing and formula reproduce Packomania's own number.

3. Strictly greater than the table value by at least 1e-10 -- VERIFIED. gain = r* - 0.258522851648 = 6.79901223519309e-6 (stated to 15 significant digits), i.e. about 68,000 times the 1e-10 margin. Not a rounding artefact: the 12-decimal table rounding is 5e-13, four orders of magnitude below the margin and seven below the gain. The candidate's r* (0.2585297) is also below the table value for N = 73 (0.2593691), so there is no mislabelled-N anomaly.

4. Not isometric to the posted hsp4-74.txt configuration -- VERIFIED. Both configurations have 2701 pairwise distances; the sorted multisets (an isometry invariant) differ by up to 0.0072840872, and all 2701 sorted entries differ by more than 1e-8. The minimum pair distances alone differ by 1.36e-5. Clearly a different packing.

5. History-of-updates clause ("(d, N) does not appear in a History-of-updates entry on the live hsp4.html newer than the one the scout fetched") -- NOT VERIFIABLE FROM FILES. CLAIM.md records "Last update: 06-Jul-2025" as the expected value and that the 2026-10-16 16:29:32 UTC fetch was byte-identical to the 2026-10-14 fetches. I did not re-fetch; this depends on the NOVELTY skeptic's live re-fetch. Not counted as failed.

6. Queue rule (N = 74 not inside any hsp4 range on pending-requests.html at verification time) -- NOT VERIFIABLE FROM FILES. CLAIM.md records no hsp4 entry on 2026-10-16 16:29:32 UTC. Mandatory caveat, as the criterion itself requires: the 26-Sep-2026 "Moki & Julio *many* 4666 candidates" bundle is category-unspecified and cannot be resolved, so N = 74 must be re-checked against the live table once that bundle disappears from the pending list. Depends on the NOVELTY skeptic's live re-fetch. Not counted as failed.

7. "re-fetched live immediately before claiming" (table value) -- NOT VERIFIABLE FROM FILES. The snapshot hsp4_radius_as_fetched.txt is what I checked against; CLAIM.md records it as fetched 2026-10-16 16:29:32 UTC, HTTP 200. The pass below is conditional on the live row for N = 74 still reading 0.258522851648.

8. No submission -- consistent with CLAIM.md ("No submission (email) is ever made"); nothing in the folder suggests otherwise.

## Stretch checks

- Rounding artefact: no (gain is 6.8e-6 against a 5e-13 table rounding).
- Wrong container radius: no (unit ball, max norm 0.7415, container constraint is the active one and is computed as 1 - max norm).
- Mislabelled N: no (74 points in the file, 74 in CLAIM.md, 74 in the comment line, r* lies between the table rows for 73 and 75).
- More than one cell: no (single cell d = 4, N = 74; the note in CLAIM.md about N in (68, 69, 75, 76) describes other cells' history, not this claim).
- Comment-line r_float agrees with the mpmath value to 5.3e-17; it is informational only and not what I relied on.
- Degenerate contacts: the three smallest candidate distances coincide to 12 digits (a normal rigid-packing contact structure), nothing anomalous.

## Null model

Not needed, and I agree with the brief: this is an explicit, finite object (74 points) judged by a deterministic checker against a fixed numeric threshold; there is no statistical hypothesis to compare against chance, and the clause outcomes are reproducible exactly.

## Subsumption judgement (earlier improvement of the same cell)

An earlier improvement of cell (4, 74) with r* = 0.258528723899142 was confirmed on 2026-10-14 and merged upstream. This candidate's r* = 0.258529650660235 strictly exceeds that earlier value by 9.2676109e-7, which is about 9,300 times the 1e-10 margin, far above any rounding effect. The cell-level fact "a packing beating Packomania's N = 74 row exists" was already established on 2026-10-14; what this claim adds is a strictly better packing of the same cell. Judged on its own against the criterion (as CLAIM.md's note states), it meets every file-checkable clause, and because it strictly improves the merged value by a margin that is itself non-trivial, I treat it as a genuine, non-subsumed win: it is a different object with a better feasible radius, not a re-presentation of the earlier result.

confirmed_scope: For d=4, N=74 the 74 centres in hsp4-74-candidate.txt lie in the unit ball centred at the origin and have feasible radius r* = 0.258529650660235 (mpmath, 50 digits, no tolerance), which exceeds the snapshot table value 0.258522851648 by 6.79901223519309e-6 and the earlier merged value 0.258528723899142 by 9.2676109e-7, and the packing is not isometric to the posted hsp4-74 configuration; the live-table, history and queue clauses rest on the recorded 2026-10-16 16:29:32 UTC fetches and on the standing Moki & Julio bundle caveat.

pass: true
