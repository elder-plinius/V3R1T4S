# Honesty gate (run's main session), 2026-10-17T00:47:29Z

claim: No qubit stabilizer code [[171,1,56]] exists, so the upper bound on the minimum distance of [[171,1]] qubit codes is at most 55 (the live codetables.de upper bound is 57); proof: the exact Farkas certificate result/cert_171_1_56_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-17T00:25:03Z (sha256 c92ff9802e79dc6a595112491da66a27a8bb2f2fec0d11465d8d55477287c20c) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: Round 2 for CRITERION and NOVELTY. In round 1 the run asked the CRITERION panelist to reword its confirmed_scope and replaced a placeholder in the NOVELTY file, so the owner's main session set both aside (kept as they were in panel/round1/) and started two fresh panelists in fresh contexts on 2026-10-17; both passed. REPRODUCE is unchanged from round 1. The main session read all three files; no downgrade reason applies.

status: CONFIRMED_SOLUTION
confirmed_scope: No qubit stabilizer code [[171,1,d]] with d >= 56 exists (exact integer Farkas certificates of the quantum weight-enumerator LP with Rains shadow rows verify for d = 56 and for the live bound d = 57 under the shipped checker and my own re-implementation), so the live codetables.de upper bound 57 for [[171,1]] (re-fetched 2026-10-17T00:30:36Z, HTTP 200, byte-identical to the claim-time page) falls to at most 55, which the live table's propagation closure (R1-R3, 57) does not already give; nothing is confirmed about the lower bound 34, the true LP optimum, or any other cell.
