# Honesty gate — runs/2026-11-02-0316

Read: panel/reproduce.md (pass: true), panel/novelty.md (pass: true), panel/criterion.md (pass: true).
No hedging panelist. Reproduce: independent B20 rerun matched 225354012176304818; A_final/B_final agree; repro_matrix PASS.
Novelty: OEIS A364417 still ends a(19); value absent from DATA/b-file/draft and searched literature.
Criterion: full bank success for A364417(20), not a partial win; confirmed_scope no wider than evidence.
Gate re-fetch (one GET each, User-Agent V3R1T4S-research-agent, 2026-11-02T07:41:24Z, HTTP 200):
  A364417 text sha256 8b0c55d787cc7a9d9f25ee5f1d615cd753597d1430ab09a8a86f6db07c5537f7 (unchanged);
  b364417 ends n=19; draft "No pending changes"; claimed value absent.
No downgrade triggers from kit/RUN.md step 7.

status: CONFIRMED_SOLUTION
confirmed_scope: Two independently written exact frontier-DP programs (benzZQ.c and benzB64.c) each give A364417(20) = 225354012176304818, a value absent from the OEIS A364417/A364416 DATA, b-file and draft as re-fetched 2026-11-02 01:40 ET, and benzZQ.c (but not benzB64.c) reproduces every published term A364416(3..20) and A364417(3..19).
