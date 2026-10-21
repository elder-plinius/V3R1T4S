# Honesty gate (run's main session), 2026-10-17T00:43:45Z

claim: No qubit stabilizer code [[129,2,43]] exists, so the upper bound on the minimum distance of [[129,2]] qubit codes is at most 42 (the live codetables.de upper bound is 43); proof: the exact Farkas certificate result/cert_129_2_43_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-17T00:42:14Z (sha256 19c28eb589e7dc3562d188b951a584ff23a27b333e04fe8b07ae03a9f901e551) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: 3/3 pass; no downgrade; REPRODUCE/CRITERION had no web access (claim-time page, hash-matched); NOVELTY literature search one query; open PRs read from raw pull-request page (22 PRs, none for this cell)

status: CONFIRMED_SOLUTION
confirmed_scope: The exact integer Farkas certificate result/cert_129_2_43_sh.json (quantum weight-enumerator LP with Rains shadow rows) proves no [[129,2,43]] qubit stabilizer (additive) code exists, which lowers the claim-time codetables.de upper bound for [[129,2]] from 43 to at most 42, and 43 is not implied by the standard propagation rules applied to the other live cells of the saved claim-time table.
