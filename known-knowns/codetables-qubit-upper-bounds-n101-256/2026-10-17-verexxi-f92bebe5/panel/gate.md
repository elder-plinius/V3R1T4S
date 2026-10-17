# Honesty gate (run's main session), 2026-10-17T11:43:26Z

claim: No qubit stabilizer code [[128,5,42]] exists, so the upper bound on the minimum distance of [[128,5]] qubit codes is at most 41 (the live codetables.de upper bound is 43); proof: the exact Farkas certificate result/cert_128_5_42_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-17T05:59:24Z (sha256 8c721d4d79ff6172421d20ce629c1eee19f20b1f4093e65bd21d06c4d0ad24e7) shows the upper bound the claim lowers; that fetch was more than 6 h old at the gate, so the main session fetched the cell once more (one request, same User-Agent, sha256 8c721d4d79ff6172421d20ce629c1eee19f20b1f4093e65bd21d06c4d0ad24e7) and the upper bound is unchanged; no new qubit-bound pull request since the panel's check.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: NOVELTY round 2: the first NOVELTY panelist (panel/round1/) wrote pass: false because it could not read the full open pull-request list; a fresh NOVELTY panelist read the live cell, the qubit-bound pull requests and TROPHY_CASE.md and passed (its arXiv search was partly throttled, as disclosed in novelty.md). REPRODUCE and CRITERION are unchanged. The main session read all three files.

status: CONFIRMED_SOLUTION
confirmed_scope: The exact Farkas certificate in result/cert_128_5_42_sh.json, verified in integer arithmetic by check/check_cert.py, proves that no [[128,5,42]] qubit stabilizer code (hence no [[128,5,43]]) exists, so the upper bound for [[128,5]] drops from the claim-time table value 43 to at most 41, below the propagation closure value of 42 from other claim-time cells.
