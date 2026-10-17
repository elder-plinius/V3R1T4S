# Honesty gate (run's main session), 2026-10-17T05:56:38Z

claim: No qubit stabilizer code [[135,8,43]] exists, so the upper bound on the minimum distance of [[135,8]] qubit codes is at most 42 (the live codetables.de upper bound is 43); proof: the exact Farkas certificate result/cert_135_8_43_sh.json of the quantum weight-enumerator linear program with Rains shadow constraints, verified by check/check_cert.py in integer arithmetic.
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7), from reading the three files:
- hedging panelist: none on the verdict; the limits they list (no web for REPRODUCE/CRITERION; reliance on the
  published MacWilliams and Rains shadow theorems; web-search-only PR check) are disclosures, covered by NOVELTY's
  live fetch and by the contrarian lens's brute-force checks of the LP formulas on real codes.
- reproduction mismatch: none.
- value strictly better than the live table: yes; NOVELTY's live fetch at 2026-10-17T05:26:53Z (sha256 98f7ab4b286f9e163f24a0a4518963451cedc989b13ed0f3d52ad4556ef51f91) shows the upper bound the claim lowers; panel fetch < 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; certificate at d = live upper bound included where it differs from the best one.
- scope wider than reproduced: no (CRITERION sentence used verbatim).
- sample / capped search / probable prime: not applicable (deterministic exact certificate).
- table value by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell.
- note: Fresh three-panelist review on the owner's PC. Step 5 found the certificate is also accepted with k+1 and larger k and rejected with k-1, as expected from d(n,k+1) <= d(n,k). NOVELTY's arXiv requests were refused (429/503) and it searched OpenAlex and the web instead, as disclosed. The main session read all three files.

status: CONFIRMED_SOLUTION
confirmed_scope: Both the shipped check/check_cert.py and my own independent re-implementation accept result/cert_135_8_43_sh.json in exact integer arithmetic, which proves that the qubit stabilizer weight-enumerator LP (quaternary MacWilliams link, A_i = B_i for i from 1 to 42, A_i at most B_i, nonnegativity, Rains shadow nonnegativity) is infeasible for n = 135, k = 8, so no [[135,8,d]] qubit stabilizer code with d at least 43 exists, which lowers the upper bound recorded for cell (135,8) in the claimant's saved codetables.de snapshots (hash-matched to CLAIM.md, fetches recorded there as 2026-10-17T00:27:18Z and 2026-10-17T00:29:55Z) from 43 to 42, and that 42 is not implied by the propagation rules R1, R2, R3 (nor by puncturing or the quantum Singleton bound) applied to any other cell of the saved complete table, whose closure at (135,8) is 43; I did not re-fetch the live table or search the literature.
