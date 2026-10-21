# Honesty gate (run's main session), 2026-10-16T19:48:29Z

claim: No qubit stabilizer code [[132,1,44]] exists, so the upper bound on the minimum distance of [[132,1]] qubit codes is at most 43 (the live codetables.de upper bound is 45); proof: the exact Farkas certificate result/cert_132_1_44_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-16T19:46:15Z (sha256 61399b24e3e415e90dd5ea5a3eeb0897c628605dbaef73de052b897140b2bd11) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: NOVELTY used web search only (no GitHub tool).

status: CONFIRMED_SOLUTION
confirmed_scope: For qubit stabilizer codes, the exact integer Farkas certificates result/cert_132_1_44_sh.json and result/cert_132_1_45_sh.json (quantum weight-enumerator LP with Rains shadow constraints, verified by check/check_cert.py and by my independent re-implementation) show that no [[132,1,d]] code exists for any d >= 44, lowering the recorded table upper bound of 45 (from the saved fetches, not re-fetched by me) to at most 43, and that value is not implied by R1/R2/R3 propagation from the other cells of the saved table (closure at (132,1) = 45).
