# Honesty gate (run's main session), 2026-10-17T05:50:25Z

claim: No qubit stabilizer code [[173,2,57]] exists, so the upper bound on the minimum distance of [[173,2]] qubit codes is at most 56 (the live codetables.de upper bound is 59); proof: the exact Farkas certificate result/cert_173_2_57_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-17T05:43:02Z (sha256 19e8a7b675dd86211a013ee68b646d28f4710b3c694d39490baa9bc02069a02f) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: 3/3 pass, main session read all three panel files; NOVELTY checked PR pages 1 and 2 and git ls-remote

status: CONFIRMED_SOLUTION
confirmed_scope: For the qubit cell [[173,2]], the saved claim-time codetables.de upper bound 59 is lowered to at most 56, because the exact integer Farkas certificates result/cert_173_2_57_sh.json (and result/cert_173_2_59_sh.json for the literal d=59) of the quantum weight-enumerator LP with Rains shadow constraints verify under check/check_cert.py, and the propagation closure of the saved full table at (173,2) is 58, so the bound is not implied by other cells.
