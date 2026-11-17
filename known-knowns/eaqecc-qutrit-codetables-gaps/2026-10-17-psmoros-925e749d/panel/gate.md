# Honesty gate (kit RUN.md step 7), run 2026-10-17-1119

gate written by the main session (model claude-opus-5-5) at 2026-10-17T19:11:33Z, after it read all three panel files.

status: CONFIRMED_SOLUTION
confirmed_scope: The 56-row, 66-column GF(3) symplectic generator matrix object/S_33_1_31_24.txt (sha256 925e749d…629edc) defines a degenerate entanglement-assisted qutrit code with n = 33, s = 56 independent generators, c = 24, k = 1 and exact minimum distance d = 31 under the criterion's definition (exhaustive over all 3^10 vectors of span(S)^perp, excluding span(S) ∩ span(S)^perp), which is strictly greater than d_lower = 25 and at most d_upper = 32 of the cell [[33,1,25-32;24]]_3 of the live table eaqecc.codetables.de/qutrit.php (page "Last change: 10.07.2025", sha256 37bbf731…c936c, re-fetched 2026-10-17T18:55:50Z), and no table entry with c <= 25 has d_lower >= 30.

## Reading of the panel

- panel/reproduce.md (fable, fresh subagent): pass: true. It used its own checker plus a second numpy-free route: n 33, s 56, c 24, k 1, d 31. The logical-vector digests are identical across routes and runs. The author's checker agrees. Its own parse of the table cell gives 25-32.
- panel/novelty.md (opus, fresh subagent): pass: true. Its live fetch at 2026-10-17T18:49:50Z gave HTTP 200 and sha256 37bbf731..., with the cell [[33,1,25-32;24]]_3. It found no PR, no TROPHY_CASE entry and no paper (2007.01249, 2010.07902, 2207.05647, 2206.09782, 2607.02170, and others) that has this code or implies it.
  - Caveat recorded, not a hedge on the verdict: an elementary k = 1 extension rule applied to the table's own teleportation codes gives [[33,1,30;24]]_3. So the margin over what is easily derived from known codes is +1 (31 vs 30), not the +6 over the listed d_lower. The new ingredient is the [[12,1,10;3]]_3 core inside the object.
- panel/criterion.md (opus, fresh subagent): pass: true. Every clause is met literally.
  - (33,1,24) is a listed entry of the table, not a value between rows.
  - d is computed by the criterion's definition and matches an operational Alice-only error analysis.
  - d = 31 <= d_upper = 32; c = 24 >= 1; non-catalytic.
  - The claim is not subsumed: no entry has d_lower >= 30 with c <= 25.

## Gate checks

- No panelist hedged its verdict, and reproduction showed no mismatch.
- The value is strictly better than the live table, 31 > 25. It is also better than the 30 obtainable from known codes by the extension rule.
- No stretched criterion: the cell is an exact row and k = 1 >= 1.
- Scope: the CRITERION sentence covers exactly what was reproduced. It is one object and one cell, not a bundle.
- No sample presented as complete: the enumeration is exhaustive over 3^10 vectors.
- No table value obtained by evasion: every fetch was one plain GET through the run's helper, and the stop list is empty (0 lines at the gate).
- The panel's table fetches (18:49:50Z, 18:55:50Z) are under 6 h old, so no re-fetch was needed.
- Crowd re-checked at the gate (2026-10-17T19:11Z, gh pr list "eaqecc" and "qutrit"): only PR #331, for cell (14,3,5).

## Not claimed here (ledgered in the dossier)

The run found many more qualifying cells. Under PREREG rule 5 they are not claimed in this run:
- small-cases: 112 k = 1 cells;
- additive: 137 cells;
- hull-qc: (16,3,3) and (16,4,4);
- hull-algebraic: 17 GF(9)-linear and 7 lengthened cells, one of them KNOWN in print;
- archaeologist: (27,7,6) and (27,6,7).
Each needs its own claim and panel.
