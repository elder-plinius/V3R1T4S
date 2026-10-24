# complete2: second, independent completeness check of g(k), k=1..11 (2026-10-23, ~11:50-12:05 ET)

Code: lcone.c (written from scratch, no code shared with code/fsearch.c or ../../brute/), driver drive2.sh, calib.py.
Logs: logs/ (per-worker outputs k{K}_w{0..4}.out/.err, single-worker k1/k2/k3.out, controls ctrl_*.out, k11_T0.out,
all_minimisers.txt, drive2.log).

## Method (different highway test from fsearch)
- Forward light-cone DFS: the ant starts at the origin heading N (y down) on a grid whose colours are unknown; each time it
  reads a never-visited cell, branch white (free) / black (cost 1), budget K. No bounding box: only cells the ant actually
  reads are ever assigned. Depth T.
- Highway test at depth T-1 and T, by the turn word rather than grid-phase lists: the blank-grid turn sequence is periodic
  with period 104 from update 9977 (calib.py and lcone's own blank simulation; checked to 9977+30104 updates).
  For each of the 104 phases p, force the ant's future turns to be w[p], w[p+1], ... (rotation-free, since turns are
  relative). Each read of a known cell must have the required colour; each read of a never-visited cell assigns the
  required colour (black costs 1, fail if over K). Stop with success once (a) the blank highway from phase p can no longer
  read any cell of its pre-phase history and (b) the ant can no longer reach any cell visited in [0,T). Both use the exact
  back-reach bound c_back = 18 of the periodic path (pi(v) = v.D, D = per-period drift; pi rises by |D|^2 per period,
  so the minimum over the future equals the minimum over one period). After the stop, every future read is either a cell
  visited during the forced window (identical state to the blank highway's) or a fresh cell (white in both).
  This is the exact criterion of METHOD.md stated through turns: future turns = highway word <=> state agrees with a
  highway phase on all future first-read cells. Rests on the standard fact that the blank highway is periodic forever
  from 9977 (as do all our checks).
- Completeness: any configuration with <= K blacks and onset <= T is reached by the DFS path that follows its own colours,
  and its leaf passes the test at the right phase. Persistence means onset < V iff on the highway at time V-1.
- Convention: time t = number of updates done; onset = least t such that the turn sequence from update t on is the
  highway word. Blank grid gives 9977 (same as the table / fsearch t; check_onset.py and brute use t-1).

## Results (no run flagged; all workers exit 0; no grid-edge or unresolved forced runs)
| K | V (table) | violations at V-1 | minimisers at V | leaves | matches fsearch |
|---|---|---|---|---|---|
| 1 | 310 | 0 | 1: (0,-2) | 190 | yes |
| 2 | 162 | 0 | 1 | 3,404 | yes |
| 3 | 126 | 0 | 1 | 40,515 | yes |
| 4 | 67 | 0 | 1 | 79,503 | yes |
| 5 | 62 | 0 | 1 | 410,495 | yes |
| 6 | 49 | 0 | 1 | 774,440 | yes |
| 7 | 45 | 0 | 2 | 1,966,057 | yes (both) |
| 8 | 40 | 0 | 1 (phase 103) | 3,197,376 | yes |
| 9 | 24 | 0 | 1 | 274,330 | yes |
| 10 | 17 | 0 | 1 | 26,988 | yes |
| 11 | 0 | n/a | 2 (phases 4, 37) | 1 | yes |
Minimiser cells (fixed frame, * = black but first read after onset) are identical to output/crosscheck.txt for every K
(logs/all_minimisers.txt). Counts are in the fixed start frame (ant at origin facing N).
K=10 at T=0: 0 seeds (so f(0)=11 needs 11 cells).

## Controls
- Blank grid (K=0, T=9977): no violation at 9976, onset 9977. Matches A126978 convention.
- K=3, T=127: the 126 seed is reported as a VIOLATION at 126 (planted-positive control for the V-1 test).
Run time: all K together < 1 min wall (5 workers, nice 19, CPU limit 450 s/worker). Peak memory ~12 MB/worker.

Verdict: g(1..11) independently confirmed by a second method (k=1,2 now by three). Caveat: single author/context;
correctness of lcone.c is not separately reviewed.
