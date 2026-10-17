# Honesty gate (run's main session), 2026-10-17T00:41:06Z

claim: No qubit stabilizer code [[123,2,41]] exists, so the upper bound on the minimum distance of [[123,2]] qubit codes is at most 40 (the live codetables.de upper bound is 41); proof: the exact Farkas certificate result/cert_123_2_41_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at MISSING (sha256 e9456087a9727b8bab30fb2a7349a1e6ff783a93202a8e43134974101282116b) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: 3/3 pass; no downgrade; REPRODUCE/CRITERION had no web access (claim-time page, hash-matched); NOVELTY PR check was a summarised page, confirmed by main session with one direct read of the PR list at 00:40:57Z (22 PRs, none for this cell); literature search one query

status: CONFIRMED_SOLUTION
confirmed_scope: The exact integer Farkas certificate result/cert_123_2_41_sh.json (weight-enumerator LP with MacWilliams linking, A_i<=B_i, A_i=B_i for 0<i<41, nonnegativity and shadow nonnegativity) proves that no [[123,2,41]] qubit stabilizer code exists, so the [[123,2]] distance upper bound is at most 40 versus the claim-time table value 41, and this value is not implied by propagation from other cells of the saved claim-time table.
