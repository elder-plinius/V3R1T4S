# NOTES: DRAT route for "no 5 x 8 Life orphan" (segment 2, 14:00 ET 2026-10-26). Scoping, not a claim.
## Key observation
"Exists a 5x8 target with no predecessor" looks like 2-QBF, but it is PLAIN SAT once the column-transfer reachable set
is encoded with forward implications only (code/tcnf.c):
  vars T (target bits), E[j][v] (forced true when target column j == v), R[j][s] (s = pair of predecessor columns);
  clauses  E[j][v] v (col j != v);  -R[j-1][a,b] v -E[j][col(a,b,d)] v R[j][b,d];  R[0] = all true;  final -R[w][s] all s.
Soundness: any model has R >= true reachable set, so all-final-false forces a target with NO predecessor (an orphan).
Completeness: an orphan T with R = exact reachable set satisfies every clause. So UNSAT <=> no h x w orphan, and a
DRAT proof of UNSAT checked by drat-trim is a certificate. Size: w*2^(3(h+2)) ternary clauses (h=5,w=8: ~16.8M).
## Validation done this segment
- 9 rule masks x h=1,2, widths 1..8: first SAT width matches the earlier mitm.c on all 18 cases (output/control_rules.txt);
  every smaller width UNSAT with DRAT VERIFIED. SAT models brute-force checked (python, independent) on B/S h1w1 and
  mask B64/S1 h2w2: NO_PREDECESSOR confirmed.
- Life h=1..4 small widths UNSAT, DRAT verified (output/life_*.txt).
## Growth (Life, 1 kissat thread, nice 19) -- see output/life_h*_w*.txt
| h | w | clauses | kissat solve | DRAT size | drat-trim |
|---|---|---|---|---|---|
| 4 | 5 | 1.31M | 7.1 s | 21 MB | VERIFIED 34 s |
| 4 | 6 | 1.58M | 12.5 s | 23 MB | VERIFIED 62 s |
| 4 | 7 | 1.84M | 27.1 s | 33 MB | VERIFIED 84 s |
| 4 | 8 | 2.10M | 74.0 s | 63 MB | VERIFIED 167 s  (=> DRAT-certified "no 4 x w orphan, w <= 8"; reproduces part of Wade, not new) |
| 5 | 2 | 4.21M | 1.9 s | 130 MB | VERIFIED 315 s |
| 5 | 3 | 6.31M | 10.1 s | 131 MB | VERIFIED 337 s |
| 5 | 4 | 8.41M | 32.0 s | 149 MB | drat-trim TIMEOUT at 600 s (not verified) |
| 5 | 5 | 10.5M | 121.5 s | 178 MB | VERIFIED 446 s |
(h=5 w=6 with DRAT and w=7 solve-only were started at 14:19 ET; results appended below if they finished in the segment.)
## Estimate (GUESSES, labelled)
- kissat solve time at h=5 grows ~3-4x per width (1.9 -> 10 -> 32 -> 121 s). GUESS: w=6 ~6-8 min, w=7 ~25-30 min,
  w=8 ~1.5-2 h single-threaded, memory ~1-2 GB. That is box-feasible over two or three afternoon segments only if the
  solve can be split (cube on the first target column(s): 32 cubes per column, each independent with its own DRAT),
  or as a home package on the 9900X (likely hours, not days -- GUESS).
- The bottleneck is DRAT checking: drat-trim already takes 5-10 min at w=2..5 (it is dominated by the 4-10M input
  clauses, not by proof length) and timed out once at 600 s. Better route: CaDiCaL with LRAT output + the bundled
  lrat-check (third_party/drat-trim/lrat-check.c), or drat-trim with a much longer cap at home. GUESS: w=8 checking
  is hours on one core per cube; cubing makes it parallel and resumable.
- Cubing soundness: cubes on T-bits of column 1 (32 cubes, each adds units) cover all targets; each cube UNSAT with
  its own verified proof, plus a trivial tautology check that the cubes cover all 32 values, gives the full UNSAT.
- p1 wants two CNF encodings. Second encoding candidates (needs a design call): (a) the mirrored right-to-left
  transfer (shares the idea, weakly independent), (b) the direct 2-layer Tseitin encoding of the predecessor grid made
  plain-SAT by the same forward-reachability trick over rows instead of columns (states = pairs of 10-cell rows,
  2^20 per step, ~2^30 clauses per step: too big, GUESS), (c) the meet-in-the-middle split (left reachable set and
  mirrored right set must be disjoint for an orphan): two half-width transfers + a disjointness clause; different
  shape, ~same size. (c) looks best.
- Status implication: a DRAT-verified UNSAT of this encoding at h=5 w=8, plus a second encoding, plus the two existing
  numerical programs, would meet the "two independent checks" bar; whether "no 5 x 8 orphan" is new still needs the
  human literature check (Beer 2022 / Hartman et al. 2013 cover boxes with both sides <= 7).
| 5 | 6 | 12.6M | 579 s | 256 MB | VERIFIED 453 s  (=> DRAT-certified "no 5 x w orphan, w <= 6"; already known in literature) |
| 5 | 7 | 14.7M | not solved: killed at the 1000 s CPU cap (no result) | - | - |
Revised GUESS after w=6: growth 3.8x-4.8x per width, so w=7 ~40-50 min and w=8 ~3-4 h single-threaded kissat, ~1-2 GB,
DRAT ~0.4-0.6 GB per run. Uncubed w=8 does not fit a 35-min segment; cubed on target column 1 (32 cubes, GUESS a few
minutes each plus 5-10 min drat-trim each) it fits about 2-3 box afternoons with 5 workers, or one evening at home.
Recommendation: next segment(s) build the cube driver + second encoding (c) and validate both on h=4 w=8 and h=5 w<=6
(must match: UNSAT with DRAT verified, and the control rules must give the same first-SAT widths as mitm.c); then
decide box (multi-day) vs home package for 5x8.
All jobs ended by 14:38 ET; /tmp proof files deleted (sizes recorded above).
