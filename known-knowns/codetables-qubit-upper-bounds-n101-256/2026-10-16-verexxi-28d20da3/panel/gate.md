# Honesty gate (run's main session), 2026-10-16T18:31:42Z

claim: no [[150,1,50]] qubit stabilizer code exists (certificates claim/result/cert_150_1_50_sh.json and cert_150_1_51_sh.json).
panel: reproduce.md pass: true; novelty.md pass: true; criterion.md pass: true (three Sonnet subagents, same VM, each given only its own copy of claim/).

Downgrade checks (kit/RUN.md step 7):
- hedging panelist: no. REPRODUCE lists two limits (no live re-fetch of its own; the MacWilliams and Rains shadow
  theorems used, not re-proved from scratch). These are disclosed reliance on published theorems (KNOWN:
  Calderbank-Rains-Shor-Sloane quant-ph/9608006; Rains quant-ph/9611001), which the contrarian lens also checked
  against brute-force enumeration of 126 random codes and three d = 3 codes (attempts/contrarian/random_codes_output.txt),
  and which CRITERION checked on [[5,1,3]], Steane, Shor and [[4,2,2]]. Its verdict on the certificates is unhedged.
- reproduction mismatch: none (a row-scaling convention was resolved by REPRODUCE; both certificates verify under
  three independent checkers: check_cert.py, attempts/contrarian/code/check2.py, the REPRODUCE skeptic's own).
- value strictly better than the live table: yes; live upper bound 51, fetched by NOVELTY at 2026-10-16T18:28:09Z
  (HTTP 200, sha256 47511f9f95f6a377da769c0fb1bd811497a555cbc1b10b11c76385bb3c9dfa6c, identical to the claim-time
  fetch at 18:15:30Z). Panel fetch is less than 6 h old at the gate.
- stretched criterion / hidden quantifier: none found; the literal clause "d equal to the live table upper bound" is met by
  cert_150_1_51_sh.json, and d = 50 gives the stronger bound 49. Not implied by propagation (closure of live cells = 51).
- scope wider than reproduced: no; the CRITERION sentence is used verbatim.
- sample as complete / capped search as exclusion / probable prime: not applicable (deterministic exact certificate).
- table value obtained by evasion: no (one plain request per page, User-Agent naming V3R1T4S, no retries).
- bundling: one cell, (150,1).
- Process note: the NOVELTY skeptic attempted one GitHub tool read of the repository elder-plinius/V3R1T4S; the tool
  refused it (outside this session's scope); nothing was attached, written or posted. Its verdict rests on the live
  table fetch, web literature searches and the pinned TROPHY_CASE.md. Reported to the human under "Needs you".

status: CONFIRMED_SOLUTION
confirmed_scope: For the qubit cell (n,k)=(150,1) with 101<=n<=256, the exact integer Farkas certificates result/cert_150_1_50_sh.json and result/cert_150_1_51_sh.json of the stated weight-enumerator LP (A_0=1, sum A=2^149, A_j=B_j for j<d, A_j<=B_j for j>=d, A>=0, shadow Sh_j>=0) verify under check/check_cert.py and an independent re-implementation, proving no [[150,1,d]] stabilizer code exists for d=50 or d=51 (so the upper bound is at most 49, lowering the recorded live bound of 51 by at least 2), and this is not implied by R1-R3 propagation of other cells of the recorded table snapshot (closure at (150,1) is 51); the live-fetch timing itself was not independently verifiable.
