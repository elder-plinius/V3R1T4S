# REPORT — Stage K (finite seed evaluation), A(25,6,11) plateau walk from the immutable 8,732. Owner: Tess (lead model Opus 5.5)
PREREG sha256 d8e43550150c031b8255cfcc826017dad34cd71d17e60cf6375f5c3210501ed2 (unchanged). T0 09:53:19Z; cut 11:05:19Z; close 11:23:19Z.
Supervisor pte-eval (ef630889...) + winjob (a6291443...): start 09:53:44Z, six jobs one at a time, "all jobs finished" / "supervisor end" 10:44:41Z; every job rc 0; 50 checkpoints, max owned RSS 0.334 GiB, min host available 39.34 GiB; 0 python processes after. Wrapper j7 (0c012a49...): every snapshot checked with the engine suspended (engine CPU delta during pause 0.0 s in every freeze record). Input 8,732 unchanged (TXT e66b06b6...). 0 GET.

## Results (engine time; misses censored at 600 s)
| Run | Seed | First M >= 8,733 | Final best | Snapshots (TXT sha256) |
|---|---|---|---|---|
| R0 control | 105 | t = 15 s (stop-at 8,733 at 16 s) | 8,733 | 8733 4f972f16d5663c66... (= I1 test object; known control) |
| R1 | 201 | t = 192 s | **8,734** (t = 568 s) | 8733 c8f381a3104918b9..., **8734 f9f280613ee2a5c500220a9f022d35d83264a14f96d940c9a517a15cebdf6fde** |
| R2 | 202 | t = 448 s | 8,733 | 8733 5cfe6095364355f8895c2e2934a54b1fe6654560ed4b6eabb3f3e5769225ff8f |
| R3 | 203 | none (censored 600 s) | 8,732 | none |
| R4 | 204 | t = 456 s | 8,733 | 8733 be2e958564af2be2d8cd78281eaceda345d74a437f0fb96d080c49a3ee27a652 |
| R5 | 205 | none (censored 600 s) | 8,732 | none |
Post-checks: all six rc 0, both_valid true. Owner recheck 10:45:22-10:45:32Z (engines dead, single-threaded, attempts/seeds/output/owner_recheck/): all five candidate TXT files valid by cwcheck_int (min_distance 6, pairs_below_d 0) and cwcheck_set (collisions 0).
Overlaps: words kept from the 8,732: 8606 (s105 8733), 8592 (s201 8733), 8577 (s201 8734), 8600 (s202 8733), 8590 (s204 8733). The 8,734 shares 8580 / 8607 / 8594 / 8561 words with the four 8,733 codes: all distinct codes.

## Decision rule (preregistered, Manager 6263866201)
Control recovered (K1). New seeds with M >= 8,733 within 600 s: **3 / 5** (201, 202, 204) -> ">= 2/5: evidence to present for a decision, never an automatic next stage". Exact 95 % Clopper-Pearson interval for 3/5: [0.147, 0.947] — five trials do not give a precise rate; no local-optimum claim either way. Times to first hit among hits: 192, 448, 456 s.
Hypotheses: K1 TRUE; K2 TRUE; K3 TRUE (3/5); K4 (>= 8,735) FALSE (max 8,734).
Reading: from the immutable 8,732 this operator reaches +1 in a majority of 10-min seeds and +2 in one; consistent with J's single flat seed (106, 45 min) being an unlucky draw rather than exhaustion, but J and K are different durations and seeds; no pooled rate is claimed.

## Status and deviations
Best object of the day: A(25,6,11) M = 8,734 (f9f28061...), CANDIDATE PENDING LIVE COMPARISON: not a record, no panel, not published, novelty unknown (live table 8,718 at 2026-10-18T21:39:24Z; open PR 437 claim 8,720; no re-read today, 0 GET). 8,732/8,728/8,721 untouched.
Deviation (declared at 10:10Z in 6264794970): the queue had NO effective barrier conditioning R1-R5 on R0's result; the condition was met in fact (R0 rc 0, M 8,733, both checkers, before R1 started 09:54:08Z) but the design did not guarantee it. Future: control under its own supervisor, queue launched only after reading its receipt.
Run folder name says 0955; T0 is 09:53:19Z.
