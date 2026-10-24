# REPRODUCE skeptic verdict: Langton's ant g(k) table, target langton-ant-fT-minimal-seed
context: fresh headless Grok Build CLI session (grok -p), started with no prior conversation in a copy of claim/

## What I read
- claim/CLAIM.md (rule, onset, g(k) table, stated highway assumption), claim/REPRODUCE.md, claim/TARGET_CRITERION.md, claim/data/TABLE.txt, claim/data/minimisers.txt.
- claim/data/this-run/fsearch RESULT and `t=` lines, claim/data/this-run/lcone DONE/MIN/VIOLATION lines, and claim/data/this-run/lcone/minimiser_compare.txt.
- After the independent simulator and the k=1..3 search were already written and run: claim/code/fsearch/fsearch.c, claim/code/lcone/lcone.c, claim/code/fsearch/drive.sh.
- Public OEIS A126978 (highway start 9977, period 104) and the A255938 blank-grid black-cell prefix.

## What I ran
Independent simulator `mysim.py`, written from the CLAIM.md rule only (white turns right, black turns left, flip, step; start (0,0) facing north; y positive downward), before opening claim/code:

`nice -n 19 timeout 400 python3 mysim.py`

- Blank grid, 40081 steps: `blank onset t=9977 drift=(-2, 2) dir=3`. Black-count prefix `[0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 6, 7, 8, 9, 10, 9, 8, 7, 6, 7]` matches A255938. `a(9977+104)-a(9977) = 12` and `a(9976+104)-a(9976) = 10`. Spatial closure held for 288 periods (through step 9977+30056), black-cell change +12 each period, `bad=0`.
- All 13 lines of minimisers.txt: computed onset equals listed `t`, cell count equals `k`, cells distinct, and `*` marks first read at or after onset. `FAILS 0`.

Independent exhaustive search `mysearch.c` (`gcc -O2`), reachable-read DFS: the first black cell lies on the blank path and each later black cell lies on the path determined by the earlier ones, so every set of at most k blacks that can affect turns in the first `g(k)+3*104` steps is generated once. A real onset at t prints three periods of the blank highway turn word in that window, so zero such prints with t < g(k) rules out an earlier onset.

`nice -n 19 timeout 400 gcc -O2 -o mysearch mysearch.c && nice -n 19 timeout 400 ./mysearch`

```
blank onset 9977 drift (-2,2) dir 3 phases 104
blank closure bad=0
k=1 Tgoal=310 leaves=150 min_onset=310 n_at_min=1 n_below=0
  BEST t=310 cells: (0,-2)
k=2 Tgoal=162 leaves=7940 min_onset=162 n_at_min=1 n_below=0
  BEST t=162 cells: (-1,3) (1,3)
k=3 Tgoal=126 leaves=331958 min_onset=126 n_at_min=1 n_below=0
  BEST t=126 cells: (0,-2) (1,-3) (3,-5)
```

Rebuilt checkers and reran every REPRODUCE.md invocation (1 worker):

`nice -n 19 timeout 400 gcc -O2 -o fsearch claim/code/fsearch/fsearch.c`
`nice -n 19 timeout 400 gcc -O2 -o lcone claim/code/lcone/lcone.c`

fsearch K T and fsearch K (T-1) for k=1..11 at the table values, plus `fsearch 10 0` (about 63s total). lcone K T 1 0 for k=1..10 at the table T, plus `lcone 11 0`, `lcone 10 0`, `lcone 0 9977`, `lcone 3 127`, `lcone 7 46`. Key lines:

- `RESULT K=1 best_t=310 minimisers=1 nodes=95 maxR=9 Dmin=159 flagged=0` and cell `(0,-2)`; `RESULT K=1 NONE t<=309 nodes=95 maxR=9 Dmin=159`
- `RESULT K=2 best_t=162 minimisers=1 nodes=1716 ... flagged=0`; `NONE t<=161 nodes=1709`
- `RESULT K=3 best_t=126 minimisers=1 nodes=20708 ... flagged=0`; `NONE t<=125 nodes=20429`
- `RESULT K=4 best_t=67 minimisers=1 nodes=41582 ... flagged=0`; `NONE t<=66 nodes=40579`
- `RESULT K=5 best_t=62 minimisers=1 nodes=217274 ... flagged=0`; `NONE t<=61 nodes=211183`
- `RESULT K=6 best_t=49 minimisers=1 nodes=434648 ... flagged=0`; `NONE t<=48 nodes=405063`
- `RESULT K=7 best_t=45 minimisers=2 nodes=1150524 ... flagged=0`; `NONE t<=44 nodes=1041910`
- `RESULT K=8 best_t=40 minimisers=1 nodes=1971129 ... flagged=0`; `NONE t<=39 nodes=1719958`
- `RESULT K=9 best_t=24 minimisers=1 nodes=205483 ... flagged=0`; `NONE t<=23 nodes=156951`
- `RESULT K=10 best_t=17 minimisers=1 nodes=26544 ... flagged=0`; `NONE t<=16 nodes=16719`; `RESULT K=10 NONE t<=0 nodes=2 maxR=0 Dmin=159`
- `RESULT K=11 best_t=0 minimisers=2 nodes=1 maxR=0 Dmin=159 flagged=0` with both 11-cell seeds
- lcone: `S0=9977 D=(-2,2) cback=18` on every run. `DONE K=1 T=310 ... leaves=190 viol=0 mins=1`; k=2 leaves=3404 mins=1; k=3 leaves=40515 mins=1; k=4 leaves=79503 mins=1; k=5 leaves=410495 mins=1; k=6 leaves=774440 mins=1; k=7 leaves=1966057 viol=0 mins=2; k=8 leaves=3197376 viol=0 mins=1; k=9 leaves=274330 mins=1; k=10 leaves=26988 mins=1. Those leaf counts are the sums of the five `this-run` worker files.
- Controls: `DONE K=0 T=9977 ... leaves=2 viol=0 mins=1`; `DONE K=10 T=0 ... leaves=1 viol=0 mins=0`; `DONE K=11 T=0 ... leaves=1 viol=0 mins=2`; `DONE K=3 T=127 ... leaves=41186 viol=1 mins=1`; `DONE K=7 T=46 ... leaves=2212874 viol=2 mins=2`.

A line-by-line compare of fsearch `RESULT` / `t=` / `#` lines against `claim/data/this-run/fsearch` gave `fsearch mismatches 0`. Normalised `(k, t, cell set)` lists: `fsearch==ref True`, `lcone==ref True` (13 configurations, equal to minimisers.txt).

## Findings
Blank onset is 9977 in this frame, with drift (-2, 2) per 104 steps. Every minimiser in minimisers.txt has the listed onset and the listed number of black cells, and direct simulation keeps the highway period after that time. For k=1, 2, and 3 the exhaustive search finds no configuration of at most k black cells whose turn sequence enters the period-104 highway before the table value, and it finds exactly one minimiser at that value, the listed cells. Rebuilt fsearch and lcone reproduce the table and the stored this-run transcripts for every REPRODUCE.md command, including both planted-positive controls and the K=10 at T=0 empty result. No mismatch.

## Caveats
Minimality for k=4..11 is the rerun of their two checkers, not a third enumeration of my own. CLAIM.md states the assumption that the blank highway, once started at update 9977, repeats forever; I checked that numerically (closure and +12 black cells per period past onset+30000) and did not prove it. `claim/data/this-run/lcone/minimiser_compare.txt` contains the line `ref 13 fsearch 0 lcone 13` and `fsearch==ref (k>=1): False`, which disagrees with the fsearch `k*.txt` transcripts in the same tree and with this rerun (both match minimisers.txt, 13 configurations). The following line of that file says the fsearch rerun matches. The transcripts themselves match.

scope: I verified blank onset 9977, every listed minimiser's onset and cell count, exhaustive minimality for k=1, 2, and 3, and a full gcc -O2 rerun of fsearch and lcone for the REPRODUCE.md commands against TABLE.txt and data/this-run; I did not enumerate k>=4 myself and did not audit novelty or the literature.
pass: true
