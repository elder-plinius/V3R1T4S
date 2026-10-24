# METHOD — minimal highway seeds g(k) and f(T) for Langton's ant (run 2026-10-23-1306)
Definitions in ../../target.md. Rule: white->turn right, black->turn left, flip, step. Ant at origin heading N
(wlog by rotation/translation; seeds listed in that frame, y down). Onset counted in updates as in OEIS A126978
(blank grid 9977). g(k) = least onset over configurations with at most k black cells; f(T) = least k with g(k) <= T.

## 1. Search (code/fsearch.c, driven by code/drive.sh)
Forward DFS over the ant's first reads: each time the ant first reads a cell, branch white or black (black costs 1).
At every time t the completion test checks, for each of the 104 phases p of the blank-grid highway (rotated to the
current heading), the phase's first-read list for 80 periods: read cells must have the phase's colour, unread cells the
phase needs black cost 1 each. Feasible iff placed + cost <= k; then the configuration is on the highway at t by the
exact criterion (Jillhewar 2026, Thm 3.1; also an earlier private Lean lemma, not needed here). Beyond 80 periods the highway reads
only cells at Chebyshev distance >= Dmin=159 from the start of the window, which are white because every placed cell
is within radius 13 (flagged=0 in every run). Iterative deepening on T gives the least t and all minimisers at it.
Complete for onset <= TMAX given correct code.

Added 2026-10-23 (documentation fixes requested in panel/criterion.md; no change to code or results):
- **Reliance on the blank highway.** fsearch, like every check in this run, relies on the standard fact that the
  blank-grid ant is on the period-104 highway forever from update 9977 (drift (-2,2) per period in our frame). We checked
  it by simulation to update 9977+30104 (complete2/lcone.c, calib.py), 9977+11440 (docfix/dmin_radius.py) and
  200,000 steps (code/check_onset.py); beyond that it is the standard (provable) fact, not something this run proves.
- **Dmin=159 for every period, not just 80-85.** fsearch measures Dmin on periods 80-85. For all later periods:
  docfix/dmin_radius.py checks that each first read in highway period j+1 is the first read of period j translated by
  the drift (-2,2) (true for all periods to 9977+11440, and for all periods by the blank-highway fact above). Let
  pi(v) = ((v-a).(-1,1))/2 for the ant position a at the window start; |v-a|_Chebyshev >= pi(v), and pi rises by exactly 2
  per period under the translation. Over all 104 phases, min pi over period-80 first reads is 158.5, so every cell first
  read in any period j >= 80 has Chebyshev distance >= 158.5 + 2(j-80), i.e. >= 159 (output docfix/dmin_radius.out;
  per-period minima 159, 161, 163, ... as measured). This is the same projection argument lcone uses for c_back.
- **Those far cells are white in the phase state too.** At every one of the 104 phases the blank-grid black debris lies
  within Chebyshev radius 48 of the ant (docfix/dmin_radius.out; the criterion reviewer found the same independently),
  and 48 < 159, so cells first read after 80 periods are white in both the configuration and the phase state.
- **Minimiser counts ignore never-read black cells.** g(k) is over configurations with at most k black cells; black
  cells the ant never reads could pad a smaller configuration without changing its onset. Minimisers are counted modulo
  such cells (two configurations that differ only on never-read cells are one minimiser). Every listed minimiser uses
  exactly k black cells, so the table is unaffected.

## 2. Independent checks
- code/check_onset.py: separate dict-based simulator, 200,000 steps, heading 104-periodicity plus a sweep check.
  Every minimiser reproduces (output/crosscheck.txt). It reports onset-1 throughout, including the blank grid
  (9976 vs 9977): an indexing convention, not a disagreement.
- ../brute/: separate C brute force over every placement in a box, proving g(1)=310 and g(2)=162 (unique) over all
  placements by a box argument, and reproducing g(3)=126 (unique) in a radius-14 box (not complete). See ../brute/SUMMARY.md.

## 3. Limits
k = 3..10: originally fsearch alone for completeness; now independently confirmed by complete2/lcone.c (section 4) (minimisers checked by both simulators). Minimiser counts are
"up to the fixed start frame" (ant N at origin). Literature/OEIS checks are search-limited (lit.md, oeis.md).

## 4. Second independent completeness check (complete2/, added 2026-10-23 ~12:05 ET)
complete2/lcone.c, written from scratch (no shared code with fsearch.c or brute): forward light-cone DFS over the colours
of newly read cells (budget K, no bounding box), with a different exact highway test: force the future turns to the
blank highway's 104-periodic turn word at each phase, checking known cells and assigning never-visited ones, and stop
via an exact back-reach bound (c_back=18) once the ant can reach neither cells visited before T nor the blank highway's
pre-history. Same onset convention as the table (blank 9977). For every K=1..10: no onset at V-1, and the minimisers at
V are exactly fsearch's (1 each, 2 at K=7); K=11 at T=0 gives the 2 seeds (phases 4, 37); K=10 at T=0 gives none.
Controls: blank onset 9977; K=3,T=127 flags the 126 seed. Details complete2/RESULTS.md. So k=3..10 no longer rest on
fsearch alone.
This check too rests on the standard fact that the blank-grid highway continues forever from update 9977 (lcone's own
blank simulation checks the 104-periodic turn word to update 9977+30104; beyond that it is the standard fact). Its stop
rule uses the exact back-reach bound c_back=18 of the periodic path, which holds for every later period by translation.

## 5. The table and its onset convention (keep these together)
| k (black cells) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| g(k) (least onset, updates) | 9977 | 310 | 162 | 126 | 67 | 62 | 49 | 45 | 40 | 24 | 17 | 0 |
| minimisers (fixed frame, modulo never-read cells) | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 2 |

Onset convention: t = number of updates done, onset = least t at which the state is on the highway (blank grid 9977,
as in OEIS A126978). code/check_onset.py and ../brute/ report one less throughout (blank grid 9976): an indexing
convention, not a disagreement. fsearch and complete2/lcone use the table's convention.
