# Honesty gate (run's main session), 2026-10-17T11:43:28Z

claim: No qubit stabilizer code [[175,3,57]] exists, so the upper bound on the minimum distance of [[175,3]] qubit codes is at most 56 (the live codetables.de upper bound is 59); proof: the exact Farkas certificate result/cert_175_3_57_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-17T05:59:01Z (sha256 100faa6c5f8e72cfbb25bd0c033727fbd08ed9af57991177286c3106a26ef37e) shows the upper bound the claim lowers; that fetch was more than 6 h old at the gate, so the main session fetched the cell once more (one request, same User-Agent, sha256 100faa6c5f8e72cfbb25bd0c033727fbd08ed9af57991177286c3106a26ef37e) and the upper bound is unchanged; no new qubit-bound pull request since the panel's check.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: NOVELTY round 2: the first NOVELTY panelist (panel/round1/) wrote pass: false because it could not read the full open pull-request list; a fresh NOVELTY panelist read the live cell, the qubit-bound pull requests and TROPHY_CASE.md and passed (its arXiv search was partly throttled, as disclosed in novelty.md). REPRODUCE and CRITERION are unchanged. The main session read all three files.

status: CONFIRMED_SOLUTION
confirmed_scope: Within the saved claim-time codetables.de snapshot (upper bound 59 for qubit [[175,3]]), the integer-checked Farkas certificates with shadow constraints prove that no [[175,3,d]] stabilizer code exists for d = 57 through 59, so the upper bound is at most 56, and propagation from the other live cells gives only 58.
