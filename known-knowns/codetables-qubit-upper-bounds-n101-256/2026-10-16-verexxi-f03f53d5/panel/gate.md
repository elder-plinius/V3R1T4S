# Honesty gate (run's main session), 2026-10-16T20:07:06Z

claim: No qubit stabilizer code [[158,1,52]] exists, so the upper bound on the minimum distance of [[158,1]] qubit codes is at most 51 (the live codetables.de upper bound is 53); proof: the exact Farkas certificate result/cert_158_1_52_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-16T20:01:22Z (sha256 d31b4dac0672c8edbfbd0ad60974cf6129f0b89a016a234ed4e0fc1fe4db9540) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: Batched panel (three cells, nine separate fresh skeptics, each seeing only its own folder). REPRODUCE sign/orientation slips on free-sign equality rows or inequality direction were self-corrected and disclosed; no mathematical mismatch.

status: CONFIRMED_SOLUTION
confirmed_scope: For the single qubit cell (n,k)=(158,1), the exact integer Farkas certificates in result/cert_158_1_53_sh.json (the table's listed upper bound 53) and result/cert_158_1_52_sh.json both pass the standalone integer checker and my own re-derived checker, so no [[158,1,52]] or [[158,1,53]] stabilizer code exists (upper bound 51, versus 53 in the saved codetables.de snapshot), and the propagation closure over all other cells of that snapshot still gives 53; the snapshot's liveness at claim time (2026-10-16T19:44Z) was taken from recorded timestamps and hashes, not re-fetched by me.
