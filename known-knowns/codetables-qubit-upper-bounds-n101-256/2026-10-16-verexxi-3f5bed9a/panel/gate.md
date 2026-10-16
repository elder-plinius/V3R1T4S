# Honesty gate (run's main session), 2026-10-16T19:54:01Z

claim: No qubit stabilizer code [[139,1,46]] exists, so the upper bound on the minimum distance of [[139,1]] qubit codes is at most 45 (the live codetables.de upper bound is 47); proof: the exact Farkas certificate result/cert_139_1_46_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-16T19:49:03Z (sha256 22fe191aa3c3310d48d62cbf7e88640b2110cce4e0842998fb73e796bf75ba2e) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: NOVELTY saw an unopened search hit brandonlign/quantum-code-bounds; the main session identified it by web search (no repository read) as a package about [[14,3]] only (n = 14), so it cannot cover this cell (scout.md addendum). REPRODUCE read the checker's docstring (not its code) for the stored row-sign convention after its own draft failed on that convention; equality multipliers are sign-free, so soundness is unaffected.

status: CONFIRMED_SOLUTION
confirmed_scope: The exact-integer Farkas certificates for the quantum weight-enumerator LP (with Rains shadow nonnegativity, and with only the criterion's listed constraints) verify for [[139,1,46]] and for [[139,1,47]], so there is no additive qubit [[139,1,d]] code for d >= 46 and the codetables.de upper bound for [[139,1]], which was 47 at the recorded fetch of 2026-10-16T19:43Z, can be lowered to at most 45, and the closure of the other live cells under the stated propagation rules at (139,1) is 47, so this is not implied by them.
