# Honesty gate (run's main session), 2026-10-17T00:47:13Z

claim: No qubit stabilizer code [[219,2,73]] exists, so the upper bound on the minimum distance of [[219,2]] qubit codes is at most 72 (the live codetables.de upper bound is 73); proof: the exact Farkas certificate result/cert_219_2_73_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at MISSING (sha256 6af37db32446cc5a70ab0ca1d21d9bc154d598ba1e6af22b4e3cf828b22857b3) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: 3/3 pass; no downgrade; REPRODUCE/CRITERION had no web access (claim-time page, hash-matched); NOVELTY literature search one query; open PRs read from raw pull-request page (22 PRs, none for this cell; main session read at 00:40:57Z)

status: CONFIRMED_SOLUTION
confirmed_scope: For the single qubit cell [[219,2]], the saved claim-time codetables.de record (upper bound 73) is lowered to 72 because result/cert_219_2_73_sh.json is an exact integer Farkas certificate, checked by check/check_cert.py, that no [[219,2,d]] stabilizer code with d >= 73 satisfies the quantum weight-enumerator LP with Rains shadow constraints, and the propagation closure of the saved complete table at (219,2) is 73, so 72 is not implied by other cells.
