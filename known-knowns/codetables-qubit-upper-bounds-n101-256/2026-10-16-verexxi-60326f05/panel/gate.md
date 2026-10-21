# Honesty gate (run's main session), 2026-10-16T21:13:49Z

claim: No qubit stabilizer code [[105,4,35]] exists, so the upper bound on the minimum distance of [[105,4]] qubit codes is at most 34 (the live codetables.de upper bound is 35); proof: the exact Farkas certificate result/cert_105_4_35_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-16T21:12:28Z (sha256 93d5fd17b2cb6c3e8fd97bf84154faa5b88c0922c31d7ea4a21ddf75e4e079b0) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: NOVELTY was run twice: the first NOVELTY skeptic wrote pass: false (GitHub API rate limit / incomplete PR and literature checks, no conflicting result found; kept as novelty_attempt1_pass_false.md in the claim folder, not in the package), the retry with a fresh skeptic after the limit reset wrote pass: true; its literature search was abstract-level; propagation taken from the claim's recorded output (re-run by REPRODUCE and CRITERION)

status: CONFIRMED_SOLUTION
confirmed_scope: For the qubit cell (105,4), the saved table record (fetched 2026-10-16T21:02:04Z, upper bound 35) is lowered to 34 by an exact Farkas certificate (result/cert_105_4_35_sh.json; weight-enumerator LP with A_j=B_j for 1<=j<=34, A_j<=B_j for j>=35, and shadow nonnegativity) that check/check_cert.py verifies in integer arithmetic, and the closure of the saved full table under R1, R2, R3 at (105,4) is 35, so the bound is not implied by propagation from other saved cells.
