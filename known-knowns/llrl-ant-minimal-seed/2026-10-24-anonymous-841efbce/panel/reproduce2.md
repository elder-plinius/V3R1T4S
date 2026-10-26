# REPRODUCE-EXHAUSTIVE skeptic verdict: LLRL ant g(k) table k=0..5 and K0=12, target llrl-ant-minimal-seed (partial win p1)
context: fresh headless Grok Build CLI session (grok --prompt-file), started with no prior conversation in a copy of claim/

## What I read
- claim/CLAIM.md, claim/REPRODUCE.md, claim/TARGET_CRITERION.md, claim/METHOD.md, claim/data/minimisers.txt
- claim/code/lcone4/lcb_fast.c (full) and runner.sh. One run of `lcb_fast RULE K T NPIECES piece` is a first-read light-cone DFS with budget K. Worker `piece` keeps the nodes at depth `LCB_SPLITD` whose visit index is congruent to `piece` modulo `NPIECES` (with NPIECES=1 the modulus test keeps every node). At depth T-1 a translate-certified highway hit is a VIOLATION (some seed with at most K non-zero cells has onset at most T-1). At depth T the same hit is a MIN. viol=0 and a single MIN is the claim that g(K)=T with that unique minimiser. The depth-48 phase trie drops only prefixes that fail the same forced-read rules used by the full test.
- claim/code/sim/CERT.md and the `certify` implementation in lcb_fast.c (sufficient translate check: heading returns, drift nonzero, reads match the blank word, and s_{t+P}(c+D)=s_t(c) out to the support projection).
- claim/code/hsearch/hsearch.c (checker A: first-read DFS, stride-8 completion test, exact onset by backward extension, split at SPLITD).
- Stored logs: claim/data/this-run/B/val_k4_T195.txt; claim/data/this-run/B/k5_T174/p0.txt through p39.txt and the matching .err files; claim/data/this-run/B/compare_k5.txt; claim/data/prior-run-1428/B/k4_T195.txt; claim/data/this-run/A/q_k5_T174/NOTE.txt, p3.txt, p7.txt, p10.txt, p35.txt.

## What I ran
Rebuild, gcc (Debian 14.2.0-19) 14.2.0:
`gcc -O2 -o scratch/lcb_fast scratch/lcb_fast.c`
(source copied from claim/code/lcone4/lcb_fast.c).

A pool of 4 processes, every invocation under `timeout 400 nice -n 19`, RSS about 68 MB each:
- `./lcb_fast LLRL 4 195 1 0`
- `env LCB_SPLITD=25 ./lcb_fast LLRL 5 174 40 i` for every i from 0 through 39

Wall clock 63 s (epoch 1792863238 to 1792863301). All 41 jobs exited 0. None hit the 400 s timeout. Longest k=5 piece was p0 at 62 s. k=4 took 14 s.

k=4 stdout:
```
MIN t=195 p=261 k=4 cells: (-1,0,2) (0,-1,2) (0,2,1) (1,-2,1)
DONE rule=LLRL K=4 T=195 wid=0/1 leaves=27257864 viol=0 mins=1 flags=0
```
stderr: `blank: onset 256241 period 384`
stderr followed by stdout is byte-identical to claim/data/this-run/B/val_k4_T195.txt. The four DONE lines in claim/data/prior-run-1428/B/k4_T195.txt sum to the same leaf count 27257864.

k=5: all 40 stdout files and all 40 stderr files are byte-identical to claim/data/this-run/B/k5_T174/. Sum of `leaves=` is 542179718. VIOLATION lines: 0. MIN lines: 1, on piece 12 only:
```
MIN t=174 p=228 k=5 cells: (0,1,3) (2,1,3) (0,2,2) (1,2,3) (3,0,1)
DONE rule=LLRL K=5 T=174 wid=12/40 leaves=11730989 viol=0 mins=1 flags=0
```
Every other piece has mins=0, viol=0, flags=0. Sum of the DONE viol and mins fields is 0 and 1.

Extra checker A, same compiler flags: `gcc -O2 -o scratch/hsearch claim/code/hsearch/hsearch.c`, then
`./hsearch LLRL 5 174 256241 384 - 40 i 8` for i in {3, 7, 10, 35}, again `timeout 400 nice -n 19`, four at once, RSS about 8 MB each during the run.
All four exited 0. Stdout is byte-identical to the stored A-queue files.
- p10 in 215 s: `# new best 174` / `SOL onset=174 k=5 found_t=176 phase=230 cells: (0,1,3) (2,1,3) (0,2,2) (1,2,3) (3,0,1)` / `RESULT split=10/40@8 subtrees=21067 rule=LLRL K=5 best_onset=174 minimisers=1 nodes=11838685 tests=67399822 maxR=13 Dmin=238 flagged=0`
- p3 in 11 s, p35 in 12 s, p7 in 15 s: `NONE onset<=174` with nodes 610813, 703036, 796957 and the stored test counts; each has subtrees=21067.
stderr on each: `phases built P=384: forced non-zero first reads min 12 (phase 65) max 27; Dmin(after 60 periods)=238; late non-zero first reads=0`

## Findings
The full checker-B enumeration reproduces g(4)=195 with one minimiser, cells (-1,0,2) (0,-1,2) (0,2,1) (1,-2,1), viol=0, flags=0, leaves=27257864.
The full 40-piece checker-B enumeration reproduces g(5)=174 with one minimiser, cells (0,1,3) (2,1,3) (0,2,2) (1,2,3) (3,0,1), 542179718 leaves, 0 violations, 0 flags. The B minimiser is on piece 12. The A-queue minimiser is on piece 10; that piece, rebuilt and re-run here, returns the same five cells at onset 174, and pieces 3, 7, and 35 return no onset at or below 174.
No output line disagreed with the stored logs.

## Caveats
This session's pass is the exhaustive B recomputation of k=4 and k=5, plus four A pieces. Checker C, the k=1..3 table, the planted k=2 control, K=11, and K=12 were not re-executed. The other 36 A-queue pieces were not re-executed. The translate certificate was read against CERT.md and was not re-derived, and `LCB_NOTRIE` was not compared to lcb.c on these instances. Blank onset 256241 and period 384 were taken from the line B and the A phase builder printed, not from a separate ant.c run.

scope: I re-executed checker B for k=4 unsplit and for all 40 k=5 pieces and they match the stored logs with g(4)=195 and g(5)=174 each having one minimiser, and I matched checker A pieces 3, 7, 10, and 35; I did not re-run checker C, k other than 4 and 5, or the K0=12 search.
pass: true
