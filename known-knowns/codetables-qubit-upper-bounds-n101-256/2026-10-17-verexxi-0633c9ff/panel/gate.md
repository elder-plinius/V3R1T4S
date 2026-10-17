# Honesty gate (run's main session), 2026-10-17T00:36:13Z

claim: No qubit stabilizer code [[110,2,37]] exists, so the upper bound on the minimum distance of [[110,2]] qubit codes is at most 36 (the live codetables.de upper bound is 37); proof: the exact Farkas certificate result/cert_110_2_37_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at MISSING (sha256 9366ddf82bcfd8cba8025060d03f553dd6a312f0bd3dd6a767cf6349119c2034) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: 3/3 pass; no downgrade; REPRODUCE/CRITERION had no web access (claim-time page, hash-matched); NOVELTY literature search one arXiv query

status: CONFIRMED_SOLUTION
confirmed_scope: Within the weight-enumerator LP with Rains shadow constraints, the integer Farkas certificate result/cert_110_2_37_sh.json is exactly verified to rule out any [[110,2,d]] qubit stabilizer code with d >= 37, so the codetables.de upper bound 37 (as saved at claim time in data/QECC_q4_n110_k2_claimtime.html) can be lowered to 36, and 36 is not implied by the propagation rules R1-R3 applied to the saved full table.
