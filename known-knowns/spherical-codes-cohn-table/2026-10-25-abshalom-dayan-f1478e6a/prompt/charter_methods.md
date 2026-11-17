## Quarries

1. **id:** spherical-codes-cohn-table
   **question:** For some (d, N) row in the live table at spherical-codes.org that has no proven-optimal star and is not labelled "needs more optimization", are there N vectors in R^d whose maximum pairwise inner product (the cosine of the minimal angle), computed in mpmath at 50 digits after normalising each vector, is lower than the table's 12-decimal cosine by at least 1e-10?
   **shape:** record (table cell); beating a "needs more optimization" row is the partial win only, and a kissing-number configuration (9 <= d <= 23 with cosine <= 0.5) belongs to quarry 2.
   **where defined:** bank entry `spherical-codes-cohn-table`; spherical-codes.org (HTML index, /plain CSV, /data/<d>/<N> coordinate files).
   **status to confirm first:** the HTML index row (the star exists only there, and so does the "needs more optimization" label; /plain carries neither), the /plain value, and that the posted /data file reproduces the table to 1e-11; arXiv for the chosen (d, N). Last bank check 2026-10-20: the table was being re-optimised quickly (about 4,900 rows still labelled).
   **why us:** orbit unions under finite reflection groups (W(F4), W(E6), W(E7), W(E8) and subgroups) chosen by reasoning, then smooth-max descent, active-set SLSQP on the true minimal-angle objective, and an mpmath polish; the Tammes problem in dimension 3 is the hardest sub-case.
   **weight:** 5 · **wild:** no

2. **id:** kissing-number-low-dim
   **question:** In some dimension d from 9 to 23, is there a set of vectors with identical squared norm, given exactly, with every pairwise inner product at most half the squared norm, that is larger than the entry for d in Cohn's kissing-number table (and any newer arXiv claim)?
   **shape:** record (table cell); exact integer or rational coordinates only, floating-point configurations with tiny overlap never count. Partial wins: a larger exact configuration in a dimension d >= 24 listed in Cohn's table, or a rigorous exact-arithmetic upper-bound improvement.
   **where defined:** bank entry `kissing-number-low-dim`; Cohn's kissing-number table (cohn.mit.edu/kissing-numbers); AlphaEvolve's d11 result and its successors; arXiv:2606.10402, arXiv:2606.18984, arXiv:2603.10425.
   **status to confirm first:** Cohn's table and arXiv for the last 6 months: d11, d12, d14, d18, d19 and d21 all moved in 2026, and the d18, d19 and d21 gains reached the table only after 2026-10-03 (Cohn 2026-10-20 orientation values: d9 306, d10 510, d11 604, d12 841, d13 1154, d14 1932, d18 8358, d19 12460, d21 31560; re-read, never use as the bar).
   **why us:** lattice orbit plus deep-hole insertion (laminated lattices Lambda_13 and K_13 for d13 and d14), prescribed large groups with an exact maximum clique of compatible orbits, then rational snapping of continuous optima and a Gram-matrix check in exact integers.
   **weight:** 4 · **wild:** no

3. **id:** heilbronn-records
   **question:** For some n from 3 to 36 and some container (unit square, unit-area triangle, or the convex-region category) on the live leaderboard, is there a placement of n points whose minimum triangle area, computed in exact rational arithmetic under the leaderboard's published normalisation, strictly beats the posted record?
   **shape:** record (table cell).
   **where defined:** bank entry `heilbronn-records`; Tej Stead's leaderboard (math.tejstead.com/heilbronn); Rob Gardiner's heilbronn-solutions and Lackovic's heilbronn-search repositories; optimality proofs arXiv:2607.15021 (triangle, n <= 8) and arXiv:2603.11107 (square, n <= 9).
   **status to confirm first:** the live leaderboard cell right before claiming (records moved daily; ten new ones on 18-19 Oct 2026), and any newer arXiv. Per-category normalisation (unit square, unit-area triangle, convex hull) must be read from the leaderboard, not assumed. EinsteinArena's Heilbronn n=11 problem has its own scoring and is a different thing.
   **why us:** active-set NLP (maximise t subject to the smallest triangle areas) re-identifying the active set, symmetry-constrained searches (C2, C3, D2, mirror) for the less-attacked n from 26 to 36, cross-container transfer, and a Newton or KKT equalisation in mpmath before exact Fraction verification of every triangle.
   **weight:** 3 · **wild:** no

4. **id:** packomania-csqv-sum-of-radii
   **question:** For some N <= 62, is there a packing of N circles of variable radii in the unit square, certified feasible in exact rational arithmetic (touching allowed), whose sum of radii exceeds both the live Packomania csqv value and the best value in every public repository the bank names by at least 1e-11?
   **shape:** record (table cell); for N = 26 the live EinsteinArena leaderboard must be beaten too.
   **where defined:** bank entry `packomania-csqv-sum-of-radii`; packomania.com csqv table (csqv<N>.txt, sumradii.txt, pending-requests.html); AlphaEvolve's sum-of-radii problem (N = 26, 32); jasonzliang/circle-packing-sota and RasimAbiyev/circle-packing-explorations; arXiv:2609.05093.
   **status to confirm first:** the csqv table, its pending-requests page (all October 2026 csqv submissions are saved but unprocessed until November, so for N > 62 the live table is not the frontier; this is why the quarry stops at 62), and every sota/* directory of the public repositories for the chosen N, which are updated daily. Bank values on 2026-10-08: N=26 2.635983084919, N=32 2.939572771205.
   **why us:** perturbation of the published csqv<N>.txt configuration and re-solving the active constraint system on (x, y, r), alternative contact graphs solved exactly, transfer between N, and symmetry classes; float slack never counts, only exact-rational feasibility of the saved coordinates.
   **weight:** 2 · **wild:** no

5. **id:** packomania-cci-equal-circles-in-circle
   **question:** For some N listed in the live Packomania cci radius table, is there a set of N centres whose feasible radius, min(half the smallest pairwise distance, 1 minus the largest centre norm), computed in mpmath at 50 digits straight from the coordinates, exceeds the table radius by at least 1e-11 and is not isometric to the posted configuration?
   **shape:** record (table cell); a second optimum equal to the table radius is a partial win only, not a record.
   **where defined:** bank entry `packomania-cci-equal-circles-in-circle`; packomania.com/cci (cci.html, txt/radius.txt, cci<N>.txt, author.txt, pending-requests.html).
   **status to confirm first:** the live radius.txt row, the cci.html history of updates (last table update 25-Dec-2024; N = 15 proofs announced 11-Oct-2026) and pending-requests.html: N from 652 to 3943 is excluded because a cci submission is queued there, and the category-unspecified 26-Sep-2026 bundle is an open caveat that the verdict must state.
   **why us:** large N from 1000 to 2600, where most rows are one author's own and the 2023-2024 waves stopped near 1000: perturb-and-repack from the posted coordinates, hexagonal-core templates, rattler exploitation, and an exact KKT jam in mpmath.
   **weight:** 1 · **wild:** yes

## Lenses

1. **key:** constructor · **title:** Build from structure · **skeptic:** no
   Choose a structured family (restrictions of larger schemes, group orbits, lattices from codes, symmetric seeds) where the objective has a fast exact evaluator, reason about which parameters could beat the record, then search only that family. Dead when the family's best provably cannot reach the record.

2. **key:** optimizer · **title:** Warm-start from the record · **skeptic:** no
   Start from the current record object, perturb and polish with an exact objective (flip-graph walks, active-set or SLSQP polishing followed by exact certification). Dead when long runs plateau at the record across three seeds.

3. **key:** solver · **title:** Let a solver argue · **skeptic:** no
   Encode the cell as SAT, ILP or a polynomial system with symmetry breaking you can justify, and keep every certificate. Dead when encodings time out at sizes below what a record needs.

4. **key:** object-as-data · **title:** Read the record holder · **skeptic:** no
   Treat the current best object as data: invariants, symmetries, near-misses and slack; find regularities its authors did not use. Dead when local moves around the record all lose.

5. **key:** evaluator-first · **title:** Exact, fast, twice · **skeptic:** no
   Spend the first hour on a fast exact evaluator and a second independent one; test both on the record holder and on seeded flawed objects. Floats only for search.

6. **key:** already-settled · **title:** Prove it is not new · **skeptic:** yes
   Assume the cell is already beaten: read the live table, its pending submissions, the public repositories the bank names, arXiv for the last 6 months, this repo's TROPHY_CASE.md, known-knowns and open pull requests. Dead (for the cell) when it is listed or claimed.

## Heuristics

1. Exact arithmetic or an interval certificate decides; floats only search.
2. Two independent exact checkers before believing any object.
3. Seed from the record holder.
4. Prefer cells where the checker runs in seconds.
5. A tie is not a record; one cell per claim.
6. Re-read the live cell right before claiming.
7. Compare against the sorted or canonical form of the cell (permutations, rotations, reflections, isomorphism).
8. Pick cells the active record-chasers are not working this week.

## Kill criteria

1. The two exact checkers disagree and it cannot be resolved.
2. The live cell, or a public repository the bank names, already equals or beats the object.
3. The cell is improved in this repo, an open pull request, a sibling workspace or the literature.
4. Search plateaus at the record across three distinct seeds.
5. The only margin is float tolerance: the exact or interval certificate shows no gain of at least the criterion's margin.
6. The exact check cannot run at the cell's size on one laptop.

