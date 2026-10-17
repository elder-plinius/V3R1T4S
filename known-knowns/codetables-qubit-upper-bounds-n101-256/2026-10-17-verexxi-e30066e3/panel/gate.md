# Honesty gate (run's main session), 2026-10-17T05:56:16Z

claim: No qubit stabilizer code [[115,2,39]] exists, so the upper bound on the minimum distance of [[115,2]] qubit codes is at most 38 (the live codetables.de upper bound is 39); proof: the exact Farkas certificate result/cert_115_2_39_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-17T00:34:27Z (sha256 29968216baaba12c154cba958db46710334c45fb045b682c07f8705575a9f5c3) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: REPRODUCE round 2: the first REPRODUCE file (panel/round1/) passed but contains an absolute scratch path, so it cannot be published unedited; a fresh REPRODUCE panelist on the owner's PC re-ran the checks and passed. NOVELTY and CRITERION are unchanged. The main session read all three files.

status: CONFIRMED_SOLUTION
confirmed_scope: The exact integer Farkas certificate result/cert_115_2_39_sh.json (Rains-shadow quantum weight-enumerator LP, A_i<=B_i, A_i=B_i for 0<i<39) is accepted by check/check_cert.py, proving no [[115,2,39]] qubit stabilizer code exists and so lowering the codetables.de upper bound for [[115,2]] from 39 to at most 38, a value not implied by the R1/R2/R3 propagation closure of the saved complete table.
