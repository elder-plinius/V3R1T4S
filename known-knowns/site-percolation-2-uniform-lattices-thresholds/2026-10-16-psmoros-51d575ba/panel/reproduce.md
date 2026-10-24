Saved by the main session of run 2026-10-16-0731 from the REPRODUCE subagent's returned text (fresh Agent-tool context, model fable, finished 08:48Z), text below as returned between its BEGIN and END markers.

# REPRODUCE skeptic: p2 claim, row #22 bond threshold (2-uniform (2/3)(3^3,4^2)+(1/3)(4^4), word TSS)

context: fresh subagent (Agent tool), model fable, given only a copy of claim/

Session: started 07:51:29Z, all checks finished 08:48:41Z (times from `date -u`). Work folder: work/ (own code, a venv
with numpy 2.5.4 / scipy 1.18.1 / pypdf, build of the authors' binaries, outputs). Every number, hash, time and HTTP
status below is copied from command output.

## 0. Package integrity (PROVED-HERE)
- `shasum -a 256 result/p2_value.json` = 51d575bafaa6558f1f65bd6cd46f1fd2bc113e4717d93994d9bbbdeccec68c23 (= CLAIM.md).
- `shasum -a 256 status_source/wikipedia_percolation_threshold.html` =
  2f44ce4065839fa2baf1c1655cdcf5aa40e21fcdb7cdabf69287093e0fd27e95 (= CLAIM.md); `wc -c` = 2514902 (= "2,514,902").
- My own tag-stripping grep of that HTML at the row reads: "22 (2/3)(3^3,4^2) + (1/3)(4^4) 5,4 4 2/3 0.5648(2) [74]
  0.44528611(40) [citation needed]"; the authors' parsed row (status_source/table_2uniform_parsed.json, num 22: bond
  value 0.44528611, sigma 4e-07, citation_needed true, config {3^3.4^2: 2/3, 4^4: 1/3}, zbar "4 2/3") says the same.
- result/p2_value.json: value 0.445287065459697, sigma 2.093e-08, sigma_rule4 7.293e-09, sigma_v2 2.093e-08; its
  sequence_tm (W=2..10) is string-identical to data/tm/TSS_bond.tsv (checked programmatically).
- Code hashes: code/tm/tm.cpp 13aa395550db03374911940eddc4c5b54f6f3777c64828200354cc28b6a6bf5a,
  code/eig/eig.c 1f4f515c1b5a16ac23a0647d63d748c1bbab4cd85cd29dd11f07604117dd253f,
  code/eig/mkgraph.py 5f1bc2322b032ad3e2880ec6541bc653b707d2cfe101b1a613831139851c694f.

## 1. Lattice identity, own builder (PROVED-HERE)
Definition quoted from CLAIM.md: "vertices on rows y = 0..R-1, x = 0..W-1; every row has edges (x,y)-(x+1,y); a gap of
type S between rows y and y+1 adds (x,y)-(x,y+1) (a strip of squares); a gap of type T adds (x,y)-(x,y+1) and
(x+1,y)-(x,y+1) (a strip of triangles). Word TSS".
work/lattice_check.py (sha256 c4b4a64cbbc3ec0850b38e16663279d078745665e024510e910563bf7a43c8ca) builds the torus graph
from this text, classifies each vertex by the cyclic sequence of face sizes around it (3 if two consecutive neighbours
are adjacent, else 4) and counts:
  word TSS W 7 periods 2: vertices 42 edges 98; configs {'3^3.4^2': '2/3', '4^4': '1/3'} zbar 14/3
  controls: TS -> {'3^3.4^2': '1'} zbar 5; S -> {'4^4': '1'} zbar 4; T -> {'3^6': '1'} zbar 6; TSSS -> {1/2, 1/2} zbar 9/2
This equals row #22 ("(2/3)(3^3,4^2) + (1/3)(4^4)", z 5,4, z-bar 4 2/3). SKETCH (not needed for the verdict): an
edge-to-edge tiling by regular triangles and squares whose vertices are all 3^3.4^2 or 4^4 is a strip tiling (the two
squares at a 3^3.4^2 vertex span a straight line, so the three triangles lie in a strip, and this propagates along the
line); T strips must be isolated (adjacent T strips give 3^6); fraction 2/3 forces T-density 1/3; the only 2-uniform
sequence with that density is TSS (e.g. TSSSTS splits the 3^3.4^2 vertices into two orbits); the two mirror choices of
the half-shift across a T strip are the same tiling and give isomorphic graphs. The authors' `q9_check.py lattice TSS`
prints n 144, degrees {4: 48, 5: 96}, the same fractions, zbar 14/3.

## 2. Own transfer-matrix computation of the cylinder roots (PROVED-HERE for the exact cases; NUMERICAL agreement)
Definition quoted from Jacobsen 2015 (arXiv 1507.03027, fetched PDF, eqs. 11-13): "Z2D ~ (Lambda_open)^m, Z0D ~
(Lambda_closed)^m", Z2D "corresponds to an FK cluster spanning the length of the cylinder", Z0D to "a dual FK cluster",
"PB(q,v) = 0 <=> Lambda_open = Lambda_closed, valid for a basis B of size n x m, with n finite and m -> infinity".
Before reading the authors' code I wrote work/tm_mine.py (sha256
f2125ec4d5c5a5468a8ca6cb4cb433c4678d4ca839d9ea0c87158c8fd80a75c4): states are set partitions of the W row sites;
sector "through" keeps a marked block connected to the far past and kills a history when it dies (Lambda_open); sector
"nowrap" tracks an integer lift of every site on the universal cover of the annulus and kills a history when an edge
closes a non-contractible cycle (Lambda_closed). Edges are applied site by site per row (horizontal displacement +1
including the seam edge, vertical 0, T diagonal -1), rotation symmetry reduces the full-row states, the full matrix of
each sector is built numerically at each p, the Perron root comes from numpy.linalg.eigvals, and the root of
Lambda_through - Lambda_nowrap from scipy brentq (xtol 1e-16). Exact tests, run before any TSS root:
  square bond p=1/2:  f = 0.0 (W=2), 5.6e-16 (3), 2.2e-16 (4), 1.3e-15 (5), 1.1e-15 (6); control f(p=0.45, W=3) = -1.28e-01
  triangular bond p=2 sin(pi/18)=0.34729635533386066: f = -1.1e-16 (2), -2.2e-16 (3), 4.4e-16 (4), 3.3e-16 (5), -7.8e-16 (6);
  control f(p=0.40, W=3) = +1.55e-01
Roots from my code versus the saved data/tm/TSS_bond.tsv and TS_bond.tsv (data/eig/bond.tsv agrees with tm to
<= 1.6e-15 at every W, measured):
  TSS W=2 0.4452882619112611   diff +0.0e+00
  TSS W=3 0.44529702219858164  diff -5.0e-16
  TSS W=4 0.4452910533179715   diff -5.6e-17
  TSS W=5 0.44528839219117405  diff +0.0e+00
  TSS W=6 0.44528752047593884  diff +3.3e-16
  TSS W=7 0.44528724327564667  diff -2.2e-16   (246 rotation classes per sector, 351 s)
  TSS W=8 0.44528714744907394  diff +1.1e-16   (810 classes per sector, 1869 s)
  TS  W=2 0.41961541967036314  diff +0.0e+00
  TS  W=3 0.4196455337197532   diff -2.1e-15
  TS  W=4 0.41964456822376606  diff -5.6e-16
  TS  W=5 0.4196424984071258   diff +0.0e+00
  TS  W=6 0.4196414112920269   diff +2.2e-16
  12 roots, worst |diff| 2.1e-15. W = 9, 10 were not attempted with my (pure Python) code; for those the rerun of the
  authors' two programs (section 3) is the check.
Only after this did I read tm.cpp and eig.c: tm.cpp uses the same two sectors (universal-cover lifts for no-wrap,
persistence of label 1 for the through cluster), the same row-word edge rules, power iteration and Brent on
log Lambda_open - log Lambda_closed; eig.c is a structurally different program (generic torus graph from mkgraph.py,
truncated Taylor-series weights in p - P0, Newton on Lambda_open - Lambda_closed) with the same sectors.

## 3. Rebuild and rerun of both authors' programs (PROVED-HERE for the rerun)
`clang++ -O3 -std=c++17` and `clang -O2 ... -lm` as in REPRODUCE.md: both compile clean (Apple clang 17.0.0). Reruns
(nice -n 10, time-capped, at most three at a time, PIDs recorded in work/pids.txt): tm TSS bond W=2..10 (W=9 107.6 s,
W=10 376.4 s), tm TS bond W=2..10 (W=10 406.4 s), tm kagome bond W=2,4,6,8,10, the 11 exact-test evals, eig TSS W=2..9
(W=9 root 0.44528710866737464, 325 s class), eig TS W=2..8. work/compare.py against the saved tables:
  compared 38 values; worst |diff| = 2.72e-15
  (TSS tm W=2..10 diffs: 0, -1.1e-15, -1.7e-15, -2.2e-15, -2.2e-15, -2.7e-15, +2.6e-15, -2.2e-16, -1.3e-15;
   kagome tm <= 2.6e-15; TS tm <= 2.2e-15; eig TSS/TS <= 2.6e-15)
Rerun TSS tm sequence: 2 0.44528826191126109, 3 0.44529702219858108, 4 0.44529105331796981, 5 0.44528839219117189,
6 0.44528752047593628, 7 0.44528724327564417, 8 0.44528714744907644, 9 0.44528710866737586, 10 0.44528708982128162.
The 11 EVAL lines of the rerun are character-identical to data/tm/exact_tests.txt (S bond W=3..6 at 1/2, T site W=3..6
at 1/2, T bond W=3..5 at 2 sin(pi/18); |f| <= 6.4e-16). Peak RSS seen: tm TS W=10 285 MB. data/tm/STS_bond.tsv (cyclic
shift of the word) equals TSS to <= 1.5e-15 at W=5..8.

## 4. Extrapolation rules, own implementation (PROVED-HERE)
work/extrap_mine.py (sha256 099ec9fa7d06ae09afdd57c73f626ec9327262af0a6e4ffe435be37323299d5e) implements rule 4, rule 9
and PREREG.v2 from their quoted text (three-point power-law fit solved for D by brentq; E3 = exact solve of
pc + A W^-4 + B W^-6 + C W^-8 on the last four, as CLAIM.md states; monotone/shrinking test on the last 4; drift_3 over
the trailing three-size windows). On the REPRODUCED tm sequence:
  last-4 differences -9.58e-08, -3.88e-08, -1.88e-08 (monotone, shrinking: rule-4 main branch, no fallback)
  E1 = 0.4452870654596949 (D 5.4386)   E2 = 0.44528707220717384 (D 6.1510)   E3 = 0.4452870581667734
  sigma_B = max(|E1-E2| 6.7475e-09, |E1-E3| 7.2929e-09) = 7.2929e-09
  E1 windows W_max=7,8,9,10: 0.44528704823534776, 0.4452870751284107, 0.4452870722071851, 0.4452870654596969
  drift_3 = max(6.7475e-09, 9.6687e-09, 1.7224e-08) = 1.7224e-08; 2.87 sigma_B = 2.0931e-08; sigma_v2 = 2.0931e-08
  rule 9: delta = +9.5546e-07 vs 0.44528611; combined sqrt(2.0931e-8^2 + 4e-7^2) = 4.0055e-07; |delta|/combined = 2.385
  -> "confirms" (<= 3); also |delta| > table sigma 4.0e-07; stated sigma 2.09e-08 <= 5e-08.
On the saved table the same code gives E1 = 0.4452870654596969, E2 = 0.4452870722071851, E3 = 0.4452870581667649, i.e.
CLAIM.md's 0.445287065459697 / 0.445287072207185 / 0.445287058166765, sigma_B 7.293e-09, sigma_v2 2.093e-08, ratio
2.39; on the saved eig table E1 = 0.44528706545969654, same sigmas. The authors' own scripts (extrap.py, sigma_v2.py,
extrap_eig.py, q9_check.py claim) print the same numbers and "VERDICT: MEETS NUMERIC RULES".
Transposed-orientation diagnostic: the roots in data/eigT/TSS_T_bond_m{1,2,3}.out are 0.44529061706892398,
0.44528728349077684, 0.44528709822247819 as quoted; my three-point fit on n = 3, 6, 9 gives 0.4452870512184558 (claim
0.445287051218456), 1.4e-08 below E1.
HEURISTIC robustness (not a rule): fixed-exponent fits on the saved sequence, two-point (9,10) with D = 4, 5, 6, 7, move
pc by -1.16e-08, -2.8e-09, +3.0e-09, +7.1e-09 from E1; three-point (8,9,10) with exponent pairs (4,6), (5,7), (6,8) by
-1.5e-09, -8e-10, +1.3e-09: all inside sigma_v2 = 2.09e-08. The table difference (9.6e-07) is 50x the largest of these;
p(10) alone is already 9.8e-07 above the table value with the sequence decreasing by 1.9e-08 per step and shrinking.

## 5. Calibration statements (PROVED-HERE)
- TS bond, rule 4 on data/tm/TS_bond.tsv: E1 = 0.4196403627452036 (rerun sequence 0.4196403627452118), D 4.53, sigma_B
  5.659e-09; reference 0.41964035886369(2) read from Scullard-Jacobsen 2020 Table I of the fetched PDF ("Frieze (f)
  0.419 640 358 863 69(2)"); delta = +3.88e-09 <= 5e-08 as rule 9 requires. Note: PREREG.v2 applied to TS would give
  sigma_v2 = 1.77e-07 (drift_3 dominated); rule 9 asks only for |delta| <= 5e-08, which holds.
- Kagome bond vs SJ2020 Table II (digits read from the fetched PDF, n = 1..6): tm diffs -3.4e-17, -3.1e-16, -5.1e-17,
  +5.9e-17, +2.5e-15, +8.8e-18; eig diffs -3.4e-17, -9.4e-17, -6.1e-16, -6.1e-16, +4.3e-15 (n = 1..5). CLAIM.md's
  "<= 2.5e-15" holds for the tm table; the eig n = 5 value is 4.3e-15 off (minor wording overstatement, immaterial).
- Exact cases: sections 2 (my code) and 3 (rerun of theirs).
- Minor: code/eig/extrap_eig.py uses a BST E3 and prints sigma_B 6.747e-09 for TSS; the claim uses the larger extrap.py
  value 7.293e-09; with the smaller one sigma_v2 would be 1.94e-08, same verdict. Whether the E3 choice was "stated
  before use in the lens notes" (rule 4) cannot be checked from claim/ alone.

## 6. Web access and process hygiene
Two GETs through the shared helper, both HTTP 200: https://arxiv.org/pdf/1507.03027 (sha256
48004dc4bd22ae9d2f4cd3dfdb3685c5a6c25d1a4c707083a103f4044e0375d6, 574584 bytes, 2026-10-16T08:00:29Z) and
https://arxiv.org/pdf/1910.12376 (sha256 32c67e04472de0789db28366c231b2f6a1211911ca9fdb20ceced4e7279423d0, 347481
bytes, 2026-10-16T08:00:30Z). Stop lists were checked before fetching (export.arxiv.org is stopped host-wide; arxiv.org
was not listed); no stop was triggered by me. At most three compute processes at a time, all niced and time-capped,
PIDs in work/pids.txt; at 08:48:40Z none of them was alive (checked by recorded PID; nothing killed). No
instruction-like text was found in the claim package or the fetched pages (no injection_suspected).

## Verdict
PROVED-HERE: the lattice built from the claim's own definition is row #22; the condition used is Jacobsen 2015 eq. (13)
as printed in the fetched paper; my independent solver reproduces the saved cylinder roots for W = 2..8 (TSS) and
W = 2..6 (TS) to <= 2.1e-15 after passing the square and triangular exact cases; both authors' programs rebuild and
rerun to the saved tables to <= 2.7e-15 over 38 values including the full TSS W = 2..10 sequence; my own
implementation of rules 4 and 9 and of PREREG.v2 on the reproduced sequence gives E1 = 0.445287065459695,
sigma_B = 7.293e-09, sigma_v2 = 2.093e-08, rule-9 verdict "confirms" at 2.39 combined sigma with |delta| = 9.55e-07,
larger than the table's 4.0e-07 bar; the TS and kagome calibrations hold against the fetched Scullard-Jacobsen 2020
tables; result/p2_value.json and its hash match CLAIM.md. The claimed value 0.445287065(21) and its stated sigma follow
from the saved and independently reproduced data by the frozen rules, with no mismatch, no missing object and no
non-determinism observed (reruns agree to the last few bits). Whether the frozen reading of "7 digits" (stated sigma
<= 5e-08, PREREG rule 9) and the row's status are acceptable is for the CRITERION and NOVELTY skeptics; nothing I
found contradicts them.

pass: true
