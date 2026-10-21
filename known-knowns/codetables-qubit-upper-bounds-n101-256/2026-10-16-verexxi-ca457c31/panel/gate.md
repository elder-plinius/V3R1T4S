# Honesty gate (run's main session), 2026-10-16T19:57:23Z

claim: No qubit stabilizer code [[145,1,48]] exists, so the upper bound on the minimum distance of [[145,1]] qubit codes is at most 47 (the live codetables.de upper bound is 49); proof: the exact Farkas certificate result/cert_145_1_48_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-16T19:54:33Z (sha256 50d08374d09ec79d0a120e630b25db0ffb33ea0151e4594074ba26392a64bf77) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: REPRODUCE's first draft used the opposite orientation for the equality rows (a free-sign multiplier convention) and then matched the docstring's stated orientation; no mathematical mismatch.

status: CONFIRMED_SOLUTION
confirmed_scope: For qubit stabilizer codes of length 145 and dimension 1, exact integer Farkas certificates of the quantum weight-enumerator LP with MacWilliams link, A_j = B_j below d, A_j <= B_j from d, and shadow nonnegativity, which I re-verified with the claimant's checker and my own re-implementation, show that no [[145,1,d]] code exists for any d >= 48, so the upper bound of the table cell (145,1) (recorded as 49) lowers to at most 47, and the propagation closure of the recorded live table at that cell is 49, so this is not implied by other recorded cells.
