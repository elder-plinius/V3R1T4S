# Honesty gate (run's main session), 2026-10-16T21:10:05Z

claim: No qubit stabilizer code [[159,2,52]] exists, so the upper bound on the minimum distance of [[159,2]] qubit codes is at most 51 (the live codetables.de upper bound is 53); proof: the exact Farkas certificate result/cert_159_2_52_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-16T21:05:39Z (sha256 bf8570d740bdf2ba0d51826bb553e6604fc381be9067b1b7032690bd16267652) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: NOVELTY literature/PR search was keyword-level; the main session's own single read of the open-PR list (78 open, HTTP 200, 2026-10-16T21:08Z) shows no PR for this cell

status: CONFIRMED_SOLUTION
confirmed_scope: Within the standard stabilizer-code LP with Rains shadow constraints, result/cert_159_2_53_sh.json and result/cert_159_2_52_sh.json are exact integer Farkas certificates (verified by check/check_cert.py) that no qubit stabilizer code [[159,2,53]] or [[159,2,52]] exists, lowering the saved-record codetables.de upper bound for cell (159,2) from 53 to at most 51, and that value is not implied by the propagation rules R1-R3 applied to the saved full table (closure at (159,2) is 53).
