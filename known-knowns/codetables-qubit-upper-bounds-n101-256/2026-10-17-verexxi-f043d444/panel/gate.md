# Honesty gate (run's main session), 2026-10-17T05:56:17Z

claim: No qubit stabilizer code [[125,4,41]] exists, so the upper bound on the minimum distance of [[125,4]] qubit codes is at most 40 (the live codetables.de upper bound is 41); proof: the exact Farkas certificate result/cert_125_4_41_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-17T05:26:18Z (sha256 7907ff3b963f3557d2fa6f91d771451aad2666cbfe77e64b50136c843412b3ea) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: NOVELTY round 2: the first NOVELTY panelist (panel/round1/) wrote pass: false because its pull-request check was inconclusive and its literature search thin; a fresh NOVELTY panelist read the live cell, the qubit-bound pull requests and TROPHY_CASE.md and passed (its arXiv search was partly throttled, as disclosed in novelty.md). REPRODUCE and CRITERION are unchanged. The main session read all three files.

status: CONFIRMED_SOLUTION
confirmed_scope: There is no qubit stabilizer code [[125,4,41]] (certificate: quantum weight-enumerator LP with Rains shadow constraints, verified in exact integer arithmetic), so the [[125,4]] upper bound drops from 41 to at most 40, and 41 is not implied by rules R1, R2, R3 applied to the saved complete table of 2026-10-17.
