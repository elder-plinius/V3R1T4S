# METHOD (k=6)

## Checkers (no shared code between A and B)
- **A, hsearch.c:** DFS over first-read cell colours (non-zero costs 1, budget K). Phase-completion test against the 384 highway phases. Cutoff TMAX: prints SOL for local best onset <= TMAX, then RESULT. Split: subtrees at first-read depth SPLITD numbered in DFS order; job wid of W keeps sc ≡ wid (mod W). Above SPLITD the best-cut is off so numbering is identical across jobs. Optional SUBM/SUBJ further partitions a piece; without it, output is byte-identical to the unsplit binary (package selftest).
- **B, lcb_fast.c:** fixed-depth light-cone DFS to depth T over colours of cells the ant can read within T steps, budget K. VIOLATION = already on highway at step T-1 (onset <= T-1). MIN = onset exactly T. Split at step depth LCB_SPLITD into W jobs. Trie prefilter is a necessary condition only.
- **C:** ccheck.py (dict grid) and ant.c (array grid); indep/sim_llrl.py (this run, from scratch). Translate certificate: after one period from time t, same heading, nonzero drift D, and colours along the period path match under shift by D for all cells with projection <= max support projection.

## Why box TMAX=174 pieces count for a TMAX=140 claim
hsearch starts with best = TMAX+1. A RESULT of NONE onset<=174 means best never fell to <=174, so no seed with onset <=174 exists in that piece — a fortiori none with onset 139. A RESULT with best_onset=173 (p16) means nothing better than 173 in that piece. Best-cut only prunes branches that cannot beat the current best; it cannot hide a better seed.

## Controls (package selftest + this run)
- Blank onset 256241 (indep sim and prior p1).
- Planted positives: known k=5 and onset-140 seeds certify.
- B at T=139 with viol=0 is the no-smaller-onset control for k=6.
- A/B agreement on the unique minimiser.
- Digests of all A and B result files match the home send_back.
