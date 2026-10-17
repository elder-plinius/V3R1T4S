# Honesty gate (run's main session), 2026-10-17T05:50:25Z

claim: No qubit stabilizer code [[110,5,36]] exists, so the upper bound on the minimum distance of [[110,5]] qubit codes is at most 35 (the live codetables.de upper bound is 37); proof: the exact Farkas certificate result/cert_110_5_36_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-17T05:45:50Z (sha256 22454f4e6b49c2cdb38e5734342607b33a49b92c6c638dd802e6b45fc071767c) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: 3/3 pass, main session read all three panel files; NOVELTY checked PR pages 1-3 (none for this cell)

status: CONFIRMED_SOLUTION
confirmed_scope: Both certificates verify in exact integer arithmetic, so no [[110,5,36]] (and no [[110,5,37]]) qubit stabilizer code exists, giving upper bound d(110,5) <= 35 versus the claim-time live table value of 37 and the live-table propagation closure of 36.
