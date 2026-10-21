# Honesty gate (run's main session), 2026-10-16T21:10:01Z

claim: No qubit stabilizer code [[148,2,49]] exists, so the upper bound on the minimum distance of [[148,2]] qubit codes is at most 48 (the live codetables.de upper bound is 50); proof: the exact Farkas certificate result/cert_148_2_49_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-16T21:05:21Z (sha256 d59b202d91deade3d265d1144a3eda548db859b69f7d8ea0dc7a98136aeb98c0) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: NOVELTY literature/PR search was keyword-level; the main session's own single read of the open-PR list (78 open, HTTP 200, 2026-10-16T21:08Z) shows no PR for this cell

status: CONFIRMED_SOLUTION
confirmed_scope: For the qubit cell (148,2), the exact integer Farkas certificates result/cert_148_2_50_sh.json (d = 50, the live upper bound recorded 2026-10-16) and result/cert_148_2_49_sh.json (d = 49) both verify under check/check_cert.py for the shadow-augmented quantum weight-enumerator LP (stabilizer codes only), so no [[148,2,50]] (hence, by the d = 49 certificate, no [[148,2,49]]) stabilizer code exists, and the propagation closure of the saved complete table at (148,2) is 50, so the new bound of 48 is not implied by other saved cells.
