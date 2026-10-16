# Honesty gate (run's main session), 2026-10-16T21:09:10Z

claim: No qubit stabilizer code [[140,2,46]] exists, so the upper bound on the minimum distance of [[140,2]] qubit codes is at most 45 (the live codetables.de upper bound is 47); proof: the exact Farkas certificate result/cert_140_2_46_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-16T21:04:31Z (sha256 MISSING) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: NOVELTY panel fetch recorded no body hash (value, time and HTTP status quoted); its literature search was keyword-level

status: CONFIRMED_SOLUTION
confirmed_scope: The supplied certificates (result/cert_140_2_46_sh.json and result/cert_140_2_47_sh.json) are exact integer Farkas certificates, passing check/check_cert.py, that the quantum weight-enumerator LP with Rains shadow constraints is infeasible for [[140,2,46]] and [[140,2,47]], so no qubit stabilizer code [[140,2,46]] exists, lowering the upper bound recorded in the claim-time table (47) to at most 45, and 45 is not implied by the propagation rules applied to the saved complete table.
