# Honesty gate (run's main session), 2026-10-17T00:43:44Z

claim: No qubit stabilizer code [[127,2,42]] exists, so the upper bound on the minimum distance of [[127,2]] qubit codes is at most 41 (the live codetables.de upper bound is 42); proof: the exact Farkas certificate result/cert_127_2_42_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-17T00:41:49Z (sha256 cae0ee29dc7683f64c5a3c79c55a0bca14dac338465c9840b4105c053ca2b3b1) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: 3/3 pass; no downgrade; REPRODUCE/CRITERION had no web access (claim-time page, hash-matched); NOVELTY literature search one query; open PRs read from raw pull-request page (22 PRs, none for this cell)

status: CONFIRMED_SOLUTION
confirmed_scope: The exact integer Farkas certificate result/cert_127_2_42_sh.json (quantum weight-enumerator LP with A_i<=B_i, A_i=B_i for 0<i<42, and Rains shadow nonnegativity) proves no [[127,2,42]] qubit stabilizer code exists, which lowers the claim-time table upper bound for cell (127,2) from 42 to at most 41, and that bound is not implied by the propagation rules applied to the saved claim-time table.
