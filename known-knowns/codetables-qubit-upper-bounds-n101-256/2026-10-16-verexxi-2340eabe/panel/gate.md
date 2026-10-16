# Honesty gate (run's main session), 2026-10-16T21:09:18Z

claim: No qubit stabilizer code [[146,2,48]] exists, so the upper bound on the minimum distance of [[146,2]] qubit codes is at most 47 (the live codetables.de upper bound is 49); proof: the exact Farkas certificate result/cert_146_2_48_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-16T21:05:00Z (sha256 e767c28e676aecd16c0ce703b8a38796dd935f742602a9912db4846cad96e627) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: NOVELTY literature search was keyword-level (titles/abstracts); propagation check in NOVELTY taken from the claim's recorded output, re-run by CRITERION and REPRODUCE

status: CONFIRMED_SOLUTION
confirmed_scope: Two independently re-run exact-integer Farkas certificates (result/cert_146_2_49_sh.json and result/cert_146_2_48_sh.json) show that the quantum weight-enumerator LP with Rains shadow constraints is infeasible for [[146,2,49]] and for [[146,2,48]], so no qubit stabilizer code [[146,2,d]] with d >= 48 exists, which lowers the table upper bound for cell (146,2) from 49 to at most 47 and is not implied by the propagation closure of the saved live table (49).
