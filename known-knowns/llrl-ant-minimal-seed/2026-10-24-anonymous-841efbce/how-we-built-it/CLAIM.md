# CLAIM (partial win p1 of local target llrl-ant-minimal-seed)

Rule LLRL (generalised Langton ant, Gajardo-Lutfalla-Rao arXiv 2409.10124): colours 0..3; on colour c the ant turns
LEFT for c in {0,1,3} and RIGHT for c = 2, writes c+1 mod 4, then steps one cell. The ant starts at (0,0) facing north;
y grows downward (north = (0,-1)). From the blank grid the read-colour sequence becomes periodic with period 384 and drift
(4,-4) per period (highway H384) after exactly 256241 updates (GLR's "after 256100 steps" is a rounded figure).
onset(C) = least t such that the read colours from update t on equal H384 (some phase) forever.
g(k) = least onset over finite starting configurations with at most k non-zero cells (any non-zero colour costs 1).

| k | g(k) | minimisers (x,y,colour), fixed frame, modulo never-read cells | count |
|---|---|---|---|
| 0 | 256241 | blank | 1 |
| 1 | 555 | (1,0,1) | 1 |
| 2 | 318 | (1,0,2) (1,-1,1) | 1 |
| 3 | 245 | (1,0,2) (1,-1,1) (0,2,3) | 1 |
| 4 | 195 | (-1,0,2) (0,-1,2) (0,2,1) (1,-2,1) | 1 |
| 5 | 174 | (0,1,3) (2,1,3) (0,2,2) (1,2,3) (3,0,1) | 1 |
K0 = 12: twelve non-zero cells are the fewest that put the ant on H384 at update 0; there are exactly 10 such 12-cell
seeds (data/minimisers.txt); 11 cells give none.

Evidence (details in METHOD.md, commands in REPRODUCE.md, logs in data/):
- k=1..4: exhaustive by checker A (run 1428 hsearch, re-validated in this run with the split build for k=1..3; k=4 split re-run: data/this-run/A/val_k4*)
  and by checker B (run 1428 lcb.c; re-run in this run with lcb_fast.c: identical MIN/VIOLATION lines and leaf counts).
- k=5: checker A, 4-way disjoint split, TMAX=175 inclusive, all 4 workers finished (data/this-run/A/k5_T175_w*.txt):
  min best_onset 174, one minimiser. Checker B (lcb_fast, 40 pieces, T=174): 542,179,718 leaves, 0 seeds with onset <= 173,
  exactly one MIN at 174, the same cell set (data/this-run/B/k5_T174/, compare_k5.txt).
- K0: A and B at T=0 for K=11 give none and for K=12 give the same 10 seeds (compare_k12_T0.txt).
- Checker C (independent Python simulator + translate certificate) re-checks every minimiser: certificate true at onset,
  false at onset-1 (data/this-run/C/ccheck_minimisers.txt); blank 256241 in data/prior-run-1428/C/.
- Highway persistence is proved by the translate certificate (code/sim/CERT.md), not assumed.
Not claimed: g(k) for 6 <= k <= 11 (open; see the run report), any other highway than H384.
