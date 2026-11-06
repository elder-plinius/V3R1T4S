# CLAIM: least highway onset of Langton's ant with at most k black cells, k = 0..11

Target: langton-ant-fT-minimal-seed (local user-added target; criterion in TARGET_CRITERION.md, copied verbatim).

## Statement
Langton's ant (white: turn right, black: turn left, flip the cell, step forward), starting at (0,0) facing north
(y grows downward), on a grid with finitely many black cells. onset(C) = the number of updates done when the ant's
turn sequence becomes, from then on, the period-104 highway word (equivalently: the grid+ant state agrees, on every
cell the ant will first-read in the future, with one of the 104 phases of the blank-grid highway, up to rotation and
translation). Blank grid: onset 9977 (OEIS A126978 convention). g(k) = min onset over all finite configurations with
at most k black cells.

| k | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| g(k) | 9977 | 310 | 162 | 126 | 67 | 62 | 49 | 45 | 40 | 24 | 17 | 0 |
| minimisers | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 2 |

Minimisers (fixed start frame, modulo black cells the ant never reads): data/minimisers.txt (* = black cell whose
first read happens after the onset). f(T) = least k with g(k) <= T follows from the table.

## Evidence
1. Completeness, checker A: code/fsearch/fsearch.c (forward DFS over first reads, completion test against the 104 grid
   phases; METHOD.md section 1 and the 2026-10-23 additions). Run uncapped for every k = 1..11 up to the table value.
2. Completeness, checker B: code/lcone/lcone.c (written separately, no shared code; forward light-cone DFS with the
   forced highway TURN WORD and an exact back-reach bound; code/lcone/RESULTS.md). For each k = 1..10 it reports 0
   configurations on the highway at time V-1 and lists the minimisers at V (V = table value).
3. Third check for k = 1, 2: code/brute/brute.c (plain box brute force with a box-escape argument, exhaustive; k = 3 by
   brute3.c is supporting evidence only, NOT exhaustive: 5,780 triples escape the box).
4. Independent re-simulation of every minimiser and the blank grid: code/verify/verify.py (Python stdlib, 200,000 steps).
5. Outputs: data/this-run/ (both checkers re-run on 2026-10-24 UTC in this run), data/prior-run-* (original run).
6. Controls: blank grid onset 9977 (no highway at 9976); planted positives K=3,T=127 and K=7,T=46 are reported as
   violations; K=10 at T=0 gives no seed (so f(0) = 11).

## k = 0 and k = 11
- k = 0 is the classical blank-grid value (single configuration; re-simulated by verify.py and lcone's control).
- k = 11: g(11) = 0 is the least possible onset, so minimality is trivial once the two 11-cell seeds are verified on the
  highway at time 0 (verify.py; both checkers). The statement "exactly 2 minimisers" at k = 11 comes from an exhaustive
  T = 0 search by BOTH checkers (fsearch 11 0 and lcone 11 0). g(10) > 0 is shown by both checkers (K=10, T=0: none).

## Assumption (stated explicitly)
Every part of this claim assumes the standard fact that the blank-grid ant, once on the highway at update 9977, repeats
the 104-update period forever (drift (-2,2) per period in this frame). We checked it numerically to update 9977+30104 (lcone/calib) and
200,000 updates (verify.py); we do not prove it here. (It follows from the period-104 pattern being self-reproducing on
a blank half-plane, which is the standard argument, but no formal proof is part of this claim.)
The Lean lemma mentioned in METHOD.md (from an earlier private run) is not needed: the completion test is justified
directly in METHOD.md (future trajectory is determined by colours at future first reads).

## Not claimed
Anything about the highway conjecture; other ant poses (any pose reduces to this one by rotation/translation, but the
minimiser COUNTS are frame-specific); k >= 12 (moot since g(11) = 0); a formal proof of the blank-highway fact.
Onset convention: check_onset.py and brute report one less (blank 9976); the table uses 9977.
