# CRITERION skeptic verdict: LLRL ant g(k) table k=0..5 and K0=12, target llrl-ant-minimal-seed (partial win p1)
context: fresh headless Grok Build CLI session (grok --prompt-file), started with no prior conversation in a copy of claim/

## What I read
TARGET_CRITERION.md (partial win p1 only), CLAIM.md, METHOD.md, REPRODUCE.md, code/sim/CERT.md, code/sim/ant.c, code/sim/ccheck.py, code/hsearch/hsearch.c (and merge.sh, par.sh), code/lcone4/lcb.c, code/lcone4/lcb_fast.c, code/lcone4/compare.py, data/minimisers.txt, and the this-run and prior-run-1428 logs for checkers A, B, and C (RESULT/DONE/SOL/MIN/VIOLATION lines, k=5 piece files, controls).

## What I ran
All heavy commands were `timeout 400 nice -n 19` and single-process. Compiled with `gcc -O2` into a scratch directory: `hsearch`, `lcb`, `lcb_fast`.

Independent simulator (own dict grid and own translate certificate, not the claim's C code), blank N=270000 and each claimed seed:
- blank: `onset=256241 P=384 D=(4, -4) cert=True cert_m1=False checked=4678` (same checked count as prior `ant.c` log). Two periods equal. Least period 384.
- k=1..5 and all 10 K0 seeds: certificate true at the claimed onset, false at onset−1 (no predecessor when onset is 0), H384 word identity true (a rotation of the blank word), no proper divisor of 384 fits the word. The extra A seed at onset 175 also certifies and matches H384.
- RL blank: `onset=9977 P=104` cert true, cert at 9976 false (standard Langton highway).

Rebuilt checker A (`./hsearch RULE K TMAX 256241 384 - 1 0 6`, RL with `9977 104`):
- LLRL K=1 TMAX=600: `best_onset=555 minimisers=1` cells `(1,0,1)` `nodes=268 tests=11342 maxR=11 Dmin=238 flagged=0` (matches `data/this-run/A/val_k1.txt`).
- LLRL K=1 TMAX=554: `NONE onset<=554` (a SOL at 555 is TMAX+1, which the RESULT line correctly excludes).
- LLRL K=2 TMAX=320: `best_onset=318` cells `(1,0,2) (1,-1,1)` `flagged=0 Dmin=238`.
- LLRL K=3 TMAX=250: `best_onset=245` cells `(1,0,2) (1,-1,1) (0,2,3)` `flagged=0`.
- LLRL K=11 TMAX=0: `NONE onset<=0 nodes=19642` and stderr `forced non-zero first reads min 12 ... late non-zero first reads=0`.
- LLRL K=12 TMAX=0: `best_onset=0 minimisers=10 flagged=0`. Cell sets equal the 10 lines in `data/minimisers.txt`.
- RL K=1 TMAX=320: `best_onset=310` seed `(0,-2,1)` `nodes=95 tests=2152 Dmin=119 flagged=0`.

Rebuilt checker B (`lcb_fast` and `lcb`, unsplit `1 0`):
- LLRL K=1 T=555: `MIN (1,0,1) leaves=536 viol=0 mins=1 flags=0`, stderr `blank: onset 256241 period 384`. `LCB_NOTRIE=1` produced the same line. T=554: `viol=0 mins=0 leaves=536`.
- LLRL K=2 T=318: `MIN (1,0,2) (1,-1,1) leaves=32780 viol=0 mins=1`. Original `lcb` matched that leaf count and MIN line. T=317: `viol=0 mins=0 leaves=32636`. T=319 planted: `VIOLATION t=318` of that same seed, `leaves=32936 viol=1 mins=1`.
- LLRL K=11 T=0: `viol=0 mins=0`. K=12 T=0: `mins=10 flags=0`, same 10 cell sets as A and `minimisers.txt`.
- RL K=1 T=310: `MIN (0,-2,1) leaves=190 viol=0 mins=1`, stderr `blank: onset 9977 period 104`. My certificate on that seed: onset 310, P=104, cert true, cert at 309 false.

Log audit (not a re-execution): B k=5 has all 40 pieces, wids 0..39, `leaves=542179718 viol=0 mins=1 flags=0`, the single MIN is the k=5 cell set. Every piece stderr is `blank: onset 256241 period 384`. A k=5 4-way all have `subtrees=3367`; minimum `best_onset=174` with one SOL, the same cells. A k=4 4-way all have `subtrees=1909` and the minimum is 195 with the claimed cells. Prior B k=4 split leaf counts sum to `27257864`, equal to this-run unsplit `val_k4_T195.txt`. `compare_k5.txt` and `compare_k12_T0.txt` say IDENTICAL; I recomputed the sets from the raw SOL/MIN lines.

## Findings
Partial win p1 holds, clause by clause.

(i) Every claimed value and minimiser for g(0) and g(1)..g(5), and every K0 seed, was re-confirmed here by an independent simulator. The translate certificate is a correct sufficient condition (CERT.md): if the pose advances by a nonzero drift D and the forward tube agrees, the reads stay P-periodic. It holds at each claimed onset and fails at onset−1, so that onset is exactly the first time the tail is periodic. The periodic word is the blank-grid word H384, not merely some period-384 sequence. Drifts are sign variants of (4,−4), which is the same word read at a different heading.

(ii) Completeness for k=1..5 is exhaustive and uncapped in the required sense. Checker A enumerates every first-read colouring with at most k non-zero cells. A successful completion test returns the minimum onset of the feasible phase completions; any other continuation of the same prefix shares the reads already made, so it cannot start H384 earlier. A failed test at time t means the branch is not on H384 yet, so its onset is at least t, and the best-cut (and the TMAX cut) only drops branches that cannot beat the best onset already proved. TMAX is an inclusive bound on the onset being proved. The far-cell gap holds on the logged successes: late first reads after 60 periods are all 0, Dmin=238, and 2·maxR+8 < 238 (largest success maxR in the logs is 85). The W-way split disables the best-cut above SPLITD and partitions first-read nodes at SPLITD by SCTR mod W; equal `subtrees=` counts are what that lockstep predicts, and the k=4 and k=5 logs have them. Checker B is a different program (open-addressed hash grid, its own blank-word scan, its own certificate). One run at depth T tests T−1 and T, so viol=0 and a MIN at T is exactly "no seed of size ≤ K has onset ≤ T−1, and these seeds have onset ≤ T". The depth-48 trie is a necessary filter: a phase is dropped only when the same forced-read rules (known colour must match, non-zero costs 1, budget K) already fail, and every survivor is passed to the unchanged certificate test. `LCB_NOTRIE` and `lcb.c` matched `lcb_fast` on the cases I ran, and the stored k=3 orig-vs-fast logs match each other (leaves 1283843, same MIN). A and B share no source. Controls are present for both: blank onset 256241, a planted positive (B at k=2, T=319 returns the onset-318 seed as a VIOLATION; A and B both return Langton RL K=1 onset 310 on seed (0,−2,1)), and known negatives (B viol=0 at T=g(k)−1, A NONE for K=1 at TMAX=554, both NONE for K=11 at T=0). I re-ran the k=1..3 searches and those controls; the leaf/node counts match the stored logs. For k=4 and k=5 I audited the finished logs rather than re-running them: both checkers report one minimiser, B has viol=0 and flags=0, and the cell sets agree.

(iii) K0=12. Both checkers' T=0 searches, re-run here, find no 11-cell seed and exactly the same 10 twelve-cell seeds as `data/minimisers.txt`. My certificate puts each of those ten on H384 at update 0. The phase build's minimum number of forced non-zero first reads is 12, which is why 11 is impossible for this word.

Hidden quantifiers. The frame is fixed: ant at (0,0) facing north, y downward, L on colours {0,1,3}, R on colour 2, write c+1 mod 4. g(k) is an at-most-k minimum; the searches charge one per non-zero read cell and also allow fewer than k. Unread cells cannot change the trajectory, which is the stated "modulo never-read cells" quotient. Onset is the number of updates already done when the reads become H384, and the certificate failure at onset−1 rules out an off-by-one. The highway is the blank-grid H384 word, not another period-384 highway.

## Caveats
I did not re-execute the k=4 or k=5 searches (the stored A k=5 worker 2 log is the long one). Those two values rest on reading the checkers and on the finished logs, which agree with each other and with the binary I rebuilt (k=1..3 and the T=0 runs match the logs digit for digit). The secondary A 40-way pass at TMAX=174 is incomplete (pieces 26 and 34 were still running); the complete A proof for k=5 is the 4-way TMAX=175 run. I did not re-run A's K=0 walk out to step 256241; g(0) is from my simulator, which agrees with the prior ant.c certificate including the tube-cell count 4678. Publication status was not part of p1 and was not decided. g(k) for 6 ≤ k ≤ 11 was not claimed and was not checked.

confirmed_scope: For LLRL in the fixed frame (origin, facing north, y down), g(0)=256241 on the blank grid; g(1)=555, g(2)=318, g(3)=245, g(4)=195, g(5)=174, each with exactly one minimiser modulo never-read cells, namely (1,0,1), (1,0,2)+(1,-1,1), that pair plus (0,2,3), (-1,0,2)+(0,-1,2)+(0,2,1)+(1,-2,1), and (0,1,3)+(2,1,3)+(0,2,2)+(1,2,3)+(3,0,1); K0=12 with exactly the 10 onset-0 seeds in data/minimisers.txt, and no 11-cell seed has onset 0 on H384.
scope: I verified p1's clauses (i), (ii) for k=1..5, and (iii) for K0=12, by reading both checkers and the certificate, re-simulating every listed minimiser against H384, and re-running A and B on k=1..3, the RL control, and the T=0 searches; I did not re-run the k=4 or k=5 enumerations and I did not judge novelty or g(k) for k=6..11.
pass: true
