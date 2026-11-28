# CLAIM (partial win p2 of bank target llrl-ant-minimal-seed)

Rule LLRL (generalised Langton ant, Gajardo-Lutfalla-Rao arXiv 2409.10124): colours 0..3; on colour c the ant turns
LEFT for c in {0,1,3} and RIGHT for c = 2, writes c+1 mod 4, then steps one cell. The ant starts at (0,0) facing north;
y grows downward (north = (0,-1)). From the blank grid the read-colour sequence becomes periodic with period 384
(highway H384) after exactly 256241 updates. onset(C) = least t such that the read colours from update t on equal H384
(some phase) forever (exact translate certificate). g(k) = least onset over finite starts with at most k non-zero cells
(any non-zero colour costs 1). Fixed frame; minimisers modulo never-read cells.

| k | g(k) | unique minimiser (x,y,colour) |
|---|---|---|
| 0 | 256241 | blank |
| 1 | 555 | (1,0,1) |
| 2 | 318 | (1,0,2) (1,-1,1) |
| 3 | 245 | (1,0,2) (1,-1,1) (0,2,3) |
| 4 | 195 | (-1,0,2) (0,-1,2) (0,2,1) (1,-2,1) |
| 5 | 174 | (0,1,3) (2,1,3) (0,2,2) (1,2,3) (3,0,1) |
| **6** | **139** | **(0,1,3) (0,2,2) (1,2,3) (1,4,3) (2,1,3) (3,0,1)** |

g(0..5) and K0=12 were CONFIRMED_PARTIAL as p1 (run 2026-10-24-1605). **This claim adds g(6)=139 with a unique minimiser**, which is the k=5 minimiser plus the cell (1,4,3).

## Evidence for k=6
- **Checker A (hsearch.c):** first-read DFS, 40 pieces at SPLITD=8. Pieces 0-5,7-13,15-21,28 finished on the box at TMAX=174 (data/this-run/box_done_A/: NONE onset<=174 except p16 best=173 and p21 best=174). Remaining 19 pieces finished on a home PC at TMAX=140 as 84 sub-pieces (data/this-run/A/done/). Combined coverage 40/40; min_onset=139; one minimiser (merge: `sh code/hsearch/run_merge_A.sh`). TMAX=174 on a finished piece excludes every onset <=174 in that piece, so those pieces cannot hide an onset-139 seed.
- **Checker B (lcb_fast.c):** independent fixed-depth light-cone DFS at T=139, 400 pieces at LCB_SPLITD=60 (data/this-run/B/done/). 5,011,329,083 leaves; 0 VIOLATION (onset <=138); 1 MIN = A's minimiser; flags=0. B's partition is independent of A's; B alone covers the full space. Merge: `sh code/lcone4/run_merge_B.sh`.
- **Checker C / independent sim:** package ccheck.py and ant.c, plus code/indep/sim_llrl.py (written from scratch, no shared code with ant.c/ccheck.py), all report onset=139 P=384 D=(-4,-4) cert true at 139 and false at 138 (data/this-run/C/).
- Digests: A-results-digest bc8fc1f6719817ee; B-results-digest cbd7913df3b309c1 (match send_back; recomputed in data/this-run/audit/).
- Home send_back: data/this-run/send_back.txt. Coverage audit: data/this-run/audit/COVERAGE_AUDIT.md.

## Seed definition match
Exactly 6 non-zero cells; colours in {1,2,3}; ant at (0,0) facing north; y down; LLRL turns; onset = updates already done; no symmetry reduction beyond "modulo never-read cells" (both checkers enumerate in the fixed frame with cost = number of non-zero first-read colours, budget K=6).

## Not claimed
- Full success criterion (g(k) for all k up to K0-1=11).
- Re-opening p1 / K0.
- Any highway other than H384.
- That the plane-filling or persistence question is settled beyond the translate certificate.
