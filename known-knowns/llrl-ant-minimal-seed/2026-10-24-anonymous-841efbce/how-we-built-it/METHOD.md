# METHOD — how each value is established (run 2026-10-24-1605, builds on run 2026-10-24-1428)

Conventions (PREREG): y grows downward; headings 0:N(0,-1) 1:E 2:S 3:W; R = clockwise. LLRL: on colour c the ant turns
L for c in {0,1,3}, R for c = 2, writes c+1 mod 4, steps. Ant at (0,0) facing N. onset = number of updates done when the
read-colour sequence becomes the blank-grid period-384 highway word H384 (some phase) forever. Any non-zero colour costs 1.
Minimisers are reported in this fixed frame, modulo cells that are never read.

## Highway persistence (no assumption needed)
code/sim/CERT.md: exact translate certificate. If, at time t with period P, drift D != 0 and pose(t+P) = pose(t)+D, the state
s_{t+P}(c+D) = s_t(c) on the forward tube U of the period's read cells, then reads are P-periodic forever from t.
Every claimed onset is certified at onset and fails at onset-1 (checked by C, and by B's own certificate code).

## Checker A — code/hsearch/hsearch.c (first-read DFS + phase completion test)
DFS over the colour of each cell at its FIRST read (that is the only free choice; later reads are determined). Budget K
non-zero cells. Every STRIDE steps a completion test asks: is there a phase p of H384 whose future first-read list
(precomputed from the blank run for NPER periods, relative to the ant pose) agrees with all decided cells, with the
undecided cells that need a non-zero colour costing <= K - used? Cells first-read later than NPER periods lie at
Chebyshev distance >= Dmin = 238 from the ant and must read 0 there (zreq); since the seed lies within radius maxR
(<= 85 observed, 2*maxR+8 < Dmin), a seed cannot influence them. On success, every feasible completion is re-simulated
from scratch and its exact onset found by backward extension; best = min. A branch is cut once a failed test time >= best
(it cannot give an onset below best). TMAX = the bound being proved (inclusive), not a cap on the search.
Run 1605 change: a disjoint split (args W wid SPLITD): the SCTR-th node at first-read depth SPLITD goes to worker SCTR%W;
above SPLITD the best-cut is disabled so all workers enumerate identically (equal `subtrees=` counts in every RESULT line).
Merge: g = min best_onset over workers; minimisers = union of SOL lines at that onset (SOL lines also print intermediate
bests, so filter by the final minimum). Validated: k=1..4 values and minimisers identical to run 1428 (see data).

## Checker B — code/lcone4/lcb.c and lcb_fast.c (independent code: sparse hash grid, own blank word, own certificate)
Fixed-depth DFS over first-read colours to depth T (budget K). At depth T-1 (VIOLATION) and T (MIN) each leaf is
tested against every phase p of H384: the ant's reads are forced to follow H384 from phase p (known cell must match;
unknown cell gets the required colour, non-zero costs 1, budget K); after J forced periods (J=1,2,4..64) the fully
specified state is tested with the translate certificate. No certificate by J=64 => FLAG (none occurred).
One run at T proves both: no seed with onset <= T-1 (viol=0) and the full minimiser list at T.
lcb_fast.c (run 1605) = lcb.c + a necessary-condition prefilter: a trie of all 384 rotations of H384 to depth 48 is walked
once per leaf with exactly the forced-read rules; only phases surviving 48 forced steps get the unchanged full test.
Exact (filter only removes phases whose full test must fail); about 8x faster. Pieces: LCB_SPLITD=25, 40 pieces.
Validated: k=1..4 MIN/VIOLATION lines and leaf counts identical to lcb.c (run 1428), planted positive k=2 T=319 flagged.

## Checker C — code/sim/ccheck.py (pure Python dict-grid simulator + certificate, no shared code)
Re-simulates each minimiser, finds least period, backward-extends the onset, certifies at onset, fails at onset-1.
(C checks period 384 and drift 4; equality to the H384 word itself is checked by A and B.)

## Controls
Blank-grid onset 256241 (A phase build, B blankword, C, ant.c). A: Langton RL K=1..3 give 310,162,126 (known values).
B: planted positive (k=2 at T=319 reports the 318 seed as VIOLATION). Known negatives: K=11 at T=0 gives none (A and B);
B at T=g-1 gives 0 seeds for every k.
