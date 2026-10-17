# Honesty gate (run's main session), 2026-10-17T05:56:18Z

claim: No qubit stabilizer code [[195,2,65]] exists, so the upper bound on the minimum distance of [[195,2]] qubit codes is at most 64 (the live codetables.de upper bound is 65); proof: the exact Farkas certificate result/cert_195_2_65_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-17T00:44:22Z (sha256 db84e866276bb307905e0c3a6637edeaa1c3c9e50ed10d0c87721a5a46ac1030) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: CRITERION round 2: the first CRITERION panelist (panel/round1/) could not run code (its shell was denied) and wrote pass: false; a fresh CRITERION panelist re-ran the shipped and its own checker and passed. REPRODUCE and NOVELTY are unchanged. The main session read all three files.

status: CONFIRMED_SOLUTION
confirmed_scope: Relative to the saved claim-time codetables.de snapshot (upper bound 65 for [[195,2]]), the integer Farkas certificate claim/result/cert_195_2_65_sh.json (quantum weight-enumerator LP with the MacWilliams link, A_j = B_j for j from 1 to 64, A_j at most B_j, A at least 0, and Rains shadow nonnegativity) is valid under two independent exact-integer checks, so no qubit stabilizer code [[195,2,d]] with d at least 65 exists and the upper bound for this single cell is at most 64, a value that the R1-R3 closure of the saved complete table (also with the extra rule d(n,k) at most d(n-1,k)+1) does not imply (the closure stays 65); I did not re-fetch the live table and did not search the literature outside the table.
