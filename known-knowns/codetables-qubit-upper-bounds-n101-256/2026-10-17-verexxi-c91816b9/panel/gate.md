# Honesty gate (run's main session), 2026-10-17T00:36:13Z

claim: No qubit stabilizer code [[120,2,40]] exists, so the upper bound on the minimum distance of [[120,2]] qubit codes is at most 39 (the live codetables.de upper bound is 40); proof: the exact Farkas certificate result/cert_120_2_40_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at MISSING (sha256 992696ad605b36e1e26626457066c36aa9661a55be10541d8001ad85bd5c04a9) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: 3/3 pass; no downgrade; REPRODUCE/CRITERION had no web access (claim-time page, hash-matched); NOVELTY literature search one query

status: CONFIRMED_SOLUTION
confirmed_scope: The exact Farkas certificate result/cert_120_2_40_sh.json passes the integer checker check/check_cert.py (quantum weight-enumerator LP with A_j=B_j for 1<=j<=39, A_j<=B_j for j>=40 and Rains shadow nonnegativity), proving no [[120,2,40]] qubit stabilizer code exists, which lowers the upper bound of the saved claim-time codetables.de cell (120,2) from 40 to at most 39 without that value being implied by the propagation rules applied to the saved full qubit table.
