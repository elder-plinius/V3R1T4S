# Honesty gate (run's main session), 2026-10-16T20:00:19Z

claim: No qubit stabilizer code [[152,1,50]] exists, so the upper bound on the minimum distance of [[152,1]] qubit codes is at most 49 (the live codetables.de upper bound is 51); proof: the exact Farkas certificate result/cert_152_1_50_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-16T19:57:55Z (sha256 d03ffa956a2bf8c67ef4d4cd7ff402c86bc7ffff5d0f2189578489dd0167b0d1) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: REPRODUCE first used the opposite orientation for the free-sign equality multipliers, then matched it; no mathematical mismatch.

status: CONFIRMED_SOLUTION
confirmed_scope: For the qubit cell (152,1), the supplied integer Farkas certificates (d=50 and d=51) of the stated weight-enumerator LP with Rains shadow constraints verify in exact integer arithmetic (supplied checker and my own re-implementation), so no [[152,1,50]] (hence no [[152,1,51]]) stabilizer code exists, lowering the recorded live upper bound 51 to at most 49, which the propagation closure of the recorded full-table snapshot (51) does not imply; the live status was taken from the recorded fetch files and not re-fetched by me.
