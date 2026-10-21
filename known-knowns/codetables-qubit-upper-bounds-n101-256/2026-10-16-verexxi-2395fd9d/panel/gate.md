# Honesty gate (run's main session), 2026-10-16T21:09:07Z

claim: No qubit stabilizer code [[133,2,44]] exists, so the upper bound on the minimum distance of [[133,2]] qubit codes is at most 43 (the live codetables.de upper bound is 45); proof: the exact Farkas certificate result/cert_133_2_44_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-16T21:04:04Z (sha256 MISSING) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: NOVELTY panel fetch recorded no body hash (value, time and HTTP status quoted); its literature search was keyword-level

status: CONFIRMED_SOLUTION
confirmed_scope: The two integer Farkas certificates in result/ (shadow-enhanced quaternary-MacWilliams LP, n=133, k=2, d=44 and d=45) are valid, so no [[133,2,d]] qubit stabilizer code exists for d >= 44, which lowers the claim-time snapshot upper bound of 45 (data/QECC_q4_n133_k2_claimtime.html) to at most 43 and is not implied by the R1/R2/R3 propagation closure of the full table snapshot (data/qubit_table_full_n1-256.html).
