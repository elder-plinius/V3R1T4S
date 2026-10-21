# Honesty gate (run's main session), 2026-10-17T00:43:46Z

claim: No qubit stabilizer code [[135,1,45]] exists, so the upper bound on the minimum distance of [[135,1]] qubit codes is at most 44 (the live codetables.de upper bound is 45); proof: the exact Farkas certificate result/cert_135_1_45_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-17T00:42:40Z (sha256 2a04a91c8a2b060c19f079102e24e85b231f1a8587404c1248cb81a3dff26d77) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: 3/3 pass; no downgrade; REPRODUCE/CRITERION had no web access (claim-time page, hash-matched); NOVELTY literature search one query; open PRs read from raw pull-request page (22 PRs, none for this cell)

status: CONFIRMED_SOLUTION
confirmed_scope: Within the weight-enumerator LP with Rains shadow constraints (A_0=1, sum A_i=2^(n-k), A_j=B_j for 1<=j<=44, A_j<=B_j for j>=45, shadow>=0, A>=0), the exact integer Farkas certificate result/cert_135_1_45_sh.json passes check/check_cert.py, so no [[135,1,45]] qubit stabilizer code exists and the upper bound for the [[135,1]] cell (45 in the claim-time page data/QECC_q4_n135_k1_claimtime.html) drops to at most 44, not implied by propagation from the other live cells in the saved table.
