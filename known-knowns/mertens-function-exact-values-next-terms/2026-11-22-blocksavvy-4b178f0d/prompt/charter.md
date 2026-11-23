# Research charter v2 (published part: methods only)

Published under the human's setup answer "methods only": quarries, lenses, heuristics and kill criteria.

## Quarries
1. **id:** `percolation-3d-higher-d-low-precision-rows`
   - **question:** For one cell of the 3D / higher-d percolation-threshold tables still listed to 3-4 digits (first choice: the honeycomb stack, z = 5, site 0.3701(2) and bond 0.3093(2), one cell per claim), can the threshold be measured to one-sigma 1e-5 (partial p2) or 1e-6 (full)?
   - **shape:** record (smaller uncertainty)
   - **where defined:** Wikipedia "Percolation threshold" 3D and higher-dimensional tables; S. C. van der Marck, Phys. Rev. E 55 (1997) 1514 and 6593; K. Malarz, Phys. Rev. E 91 (2015) 043301; simple-cubic reference values of Xu et al. (2014) as cited in the bank entry; bank entry `percolation-3d-higher-d-low-precision-rows`
   - **status to confirm first:** the chosen cell's listed value and uncertainty in the live table; any newer paper below 1e-5 for that lattice or an equivalent one; open pull requests here for the same cell.
   - **why us:** Newman-Ziff union-find in C needs tens of MB, parallelises across 8 cores, and the required simple-cubic reproduction doubles as the pipeline's calibration; precision is bought with patience, night after night.
   - **weight:** 5
   - **wild:** no
2. **id:** `smallest-mnist-99-percent-network`
   - **question:** Does a network with at most 696 conservatively counted parameters reach 99.00% on the MNIST test set, or (partial p1) one with at most 697 reach 99.10%, or (partial p2) one with at most 500 reach 98.80%?
   - **shape:** record (fewest parameters at a fixed accuracy)
   - **where defined:** J. Warn, Parameter-Efficient-MNIST README (697 parameters, 99.03%); R. Grimov, mnist-minimal-model; bank entry `smallest-mnist-99-percent-network`
   - **status to confirm first:** the README's current record and any smaller verified claim in its issues, forks or elsewhere.
   - **why us:** restricting to a structured family of separable and grouped convolutions makes architecture search cheap and complete, and the conservative count rule is read like an audit; throughput of training runs is the bottleneck.
   - **weight:** 4
   - **wild:** no
3. **id:** `tser-beat-reference-30-resample-best-rmse`
   - **question:** On one named small TSER dataset, does a regressor beat the best reference and published 30-resample mean test RMSE?
   - **shape:** record (lower mean RMSE)
   - **where defined:** C. W. Tan, C. Bergmeir, F. Petitjean, G. Webb, "Time series extrinsic regression" (2021); timeseriesclassification.com regression reference results; tsml-eval publications/y2023/tser_archive_expansion; bank entry `tser-beat-reference-30-resample-best-rmse`
   - **status to confirm first:** the reference rmse files and the archive-expansion results for the chosen dataset.
   - **why us:** most of the work is a leakage-free resampling pipeline and an exact reproduction of a published baseline before any new model is scored; small datasets fit this box.
   - **weight:** 3
   - **wild:** no
4. **id:** `apn-new-ccz-class-dim9-10`
   - **question:** Is there an APN function in dimension 9 or 10 (or an APN permutation in dimension 9, partial p1) whose exactly computed CCZ invariant differs from every known instance?
   - **shape:** existence
   - **where defined:** UiB Boolean Functions wiki tables; C. Beierle and G. Leander, IEEE TIT (2022), arXiv:2009.07204; Yu, Li, Ichanska, Kaleyski, IACR ePrint 2024/1778; bank entry `apn-new-ccz-class-dim9-10`
   - **status to confirm first:** the wiki tables and arXiv/ePrint for new dimension-9 and dimension-10 datasets.
   - **why us:** restricted structured families (quadratic, coefficients in a subfield, symmetric under a cyclotomic action) give exhaustive searches with exact invariants as fingerprints.
   - **weight:** 2
   - **wild:** yes
5. **id:** `kings-hard-core-entropy-a247413-digits`
   - **question:** Can the unit-activity non-attacking-kings entropy constant (OEIS A247413) be given to at least (live DATA length + 4) decimals by two independent methods, or rigorously bracketed to 12 decimals (partial p1)?
   - **shape:** record (more digits) / bound (certified two-sided bracket)
   - **where defined:** OEIS A247413 and A063443; K. Liang, arXiv:2505.12776 (2025); N. Calkin and H. Wilf, arXiv:math/9810155 (1998); bank entry `kings-hard-core-entropy-a247413-digits`
   - **status to confirm first:** the live DATA length (26 terms when last read) and the open pull requests here that already claim 33 and 36 digits with Collatz-Wielandt bounds; attack only if both are resolved and something is left.
   - **why us:** row-by-row strip transfer matrices are a staged sweep; exact big-rational arithmetic gives digit stability and certificates on modest memory.
   - **weight:** 1
   - **wild:** no

## Lenses
1. **key:** `forming-line` - **title:** The roll-forming line - **skeptic:** no
   You build the object one station at a time: a strip of fixed width passes through, and each pass adds one row or
   cell, with the boundary profile as the only state. First moves: write the exact one-row step, check it on widths
   1-6 against known counts, then grow the width. Dead sign: state count outgrows half the free memory before the
   digits stabilise.
2. **key:** `small-data` - **title:** Many small cases, then the pattern (method card) - **skeptic:** no
   You do not trust one big run. You compute the quantity exactly for many small sizes (widths, lattice sizes,
   parameter budgets), tabulate, and let the table show its convergence or fitted law before you scale. First moves:
   a table of at least 8 sizes with exact or high-precision values and a fit. Dead sign: successive estimates stop
   converging or the fit's residuals show structure.
3. **key:** `obstruction` - **title:** Find what forbids it (method card) - **skeptic:** no
   You look for the invariant that would rule the target out (a parameter lower bound, an exact identity mapping a
   cell to a solved lattice, a CCZ invariant already taken) and search only where it is silent. First moves: list
   the invariants and compute them for the known objects. Dead sign: the invariant is satisfied everywhere and
   prunes nothing.
4. **key:** `structured-family` - **title:** Shrink to a family you can finish (method card) - **skeptic:** no
   You restrict to a family where search is cheap and complete (block-symmetric states, separable convolutions,
   subfield-coefficient polynomials) and finish it exhaustively, then break the symmetry on purpose. First moves:
   enumerate the family's size and cost per member. Dead sign: the family is already exhausted in the literature.
5. **key:** `spectral` - **title:** Linear algebra over exact fields - **skeptic:** no
   You treat the problem as a large structured matrix or a Boolean function's spectrum: power iteration with exact
   rationals and certified bounds, Walsh transforms, ranks over GF(2). First moves: a fast exact evaluator and its
   timing. Dead sign: certificates widen instead of tightening as size grows.
6. **key:** `auditor` - **title:** The auditor - **skeptic:** yes
   You assume the quarry is already settled, trivial or ill-posed, and you hunt the exploit: a newer paper, an
   equivalent lattice already known, a counting loophole, a leaked test split, a criterion that a constant
   predictor nearly meets. First moves: read the criterion as an adversarial spec and list every way a result could
   pass it dishonestly. Dead sign: none; this lens ends with a written verdict either way.

## Heuristics
1. Reproduce a published value before computing a new one.
2. Five truncations or sizes, or no claim of stability.
3. Count parameters and digits conservatively; when in doubt, count it.
4. A cheap exact evaluator beats a clever slow one.
5. Prefer the structured family you can finish over the open space you cannot.
6. Every digit claimed needs two methods that share no code.
7. Memory first: size the largest state before starting the sweep.
8. Read the criterion twice as an attacker would.

## Kill criteria
1. The record moved past what this box can reach in a week of nights.
2. Two methods disagree and the disagreement cannot be located in one run.
3. The published baseline cannot be reproduced within its tolerance.
4. State or memory grows faster than the digits gained per size step.
5. The result is a tie or follows from a published object by a trivial edit.
6. An equivalent problem is already solved under another name.

