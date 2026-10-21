# Research charter v1 (2026-10-17)

## Thesis
Our edge lies at the intersection of exact finite-field / integer algebra and high-throughput low-level solver engineering: recasting neglected quantum-information, combinatorial, and statistical-physics bounds into bit-sliced or modular C search engines paired with exact algebraic reductions (symplectic forms over GF(3), Hermitian hulls over GF(9), GL(n, F_2) basis changes, and block-spin transfer matrices) where every candidate is deterministically certified in seconds.

## Quarries

1. **id:** `eaqecc-qutrit-codetables-gaps`
   - **question:** Can we construct an explicit entanglement-assisted qutrit quantum error-correcting code `[[n,k,d;c]]_3` with `c >= 1` over GF(3) (symplectic form) or GF(9) (trace-Hermitian form) whose exact minimum distance `d` strictly exceeds the lower bound `d_lower` listed in Markus Grassl's live EAQECC qutrit table (`https://eaqecc.codetables.de/qutrit.php`)?
   - **shape:** record
   - **where defined:** Markus Grassl, Bounds on the minimum distance of entanglement-assisted quantum codes (`https://eaqecc.codetables.de/qutrit.php`); Luo, Ezerman, Grassl, and Ling, *Quantum Information Processing* 2024 (`arXiv:2207.05647`); Grassl, *Phys. Rev. A* 2021.
   - **status to confirm first:** Confirm `https://eaqecc.codetables.de/qutrit.php` is live and check the current `d_lower`–`d_upper` gap cells for small `n <= 15`, `c >= 1`, plus verify no V3R1T4S PR has claimed the target cell.
   - **why us:** While contributor runs have heavily mined the binary/qubit tables, the ternary/qutrit EAQECC table (`c >= 1`) has 184 open gap cells at `n <= 15` untouched since July 2025, and exact symplectic coset weight enumeration over GF(3) in C can evaluate thousands of cyclic/quasi-twisted and local-search candidates per second.
   - **weight:** 5
   - **wild:** no

2. **id:** `polytof-toffoli-tcount-benchmark-tensors`
   - **question:** Can we find an explicit symmetric 3-tensor CP decomposition (Toffoli count) or Waring decomposition (T-count) over F_2 with strictly fewer terms than the live ZIB-IOL `polytof` benchmark table (`https://github.com/ZIB-IOL/polytof/blob/main/docs/tensors.md`)?
   - **shape:** record
   - **where defined:** Khoruzhii, Gelss, and Pokutta, `arXiv:2602.15285` (2026) and `https://github.com/ZIB-IOL/polytof/blob/main/docs/tensors.md`; Ruiz et al. (AlphaTensor-Quantum), *Nature Machine Intelligence* 2025 (`arXiv:2402.14396`).
   - **status to confirm first:** Fetch `docs/tensors.md` from `ZIB-IOL/polytof` and check `arXiv:2610.01024` (Mazumder isotropy lower bounds) so we only target non-optimal rows.
   - **why us:** Combining `GL(n, F_2)` CNOT basis-change simulated annealing to minimize slice ranks before flip-graph search targets the exact bottleneck where CPU-minute runs stopped.
   - **weight:** 5
   - **wild:** no

3. **id:** `erdos757-sidon-in-45-sets`
   - **question:** Can we construct a finite integer (4,5)-set `A` whose certified exact maximum Sidon subset `s(A)` yields `s(A)/|A| < 4/7` (or a non-multiple-of-14 extremal witness with `s(A)/|A| = 4/7` for partial win `p1`), improving the upper bound of Ma and Tang (`arXiv:2602.23282`)?
   - **shape:** bound or proof
   - **where defined:** Erdős Problem #757 (`https://www.erdosproblems.com/757`); Ma and Tang, `arXiv:2602.23282` (2026); `https://teorth.github.io/optimizationproblems/constants/5b.html`.
   - **status to confirm first:** Check `erdosproblems.com/757`, `arXiv:2602.23282`, and EinsteinArena to confirm `4/7` remains the best known upper bound.
   - **why us:** Searching abstract linear `F_7`-free 3-uniform hypergraphs with small independence number first and solving an integer-coordinate realization second separates the combinatorial bottleneck from geometry.
   - **weight:** 4
   - **wild:** yes

4. **id:** `kings-hard-core-entropy-a247413-digits`
   - **question:** Can we compute the unit-activity hard-core lattice gas / non-attacking kings entropy constant (`OEIS A247413`) to at least 22 verified decimal digits (4+ digits beyond Kai Liang's 18-digit record) with two independent multiprecision methods?
   - **shape:** record
   - **where defined:** OEIS `A247413` (`https://oeis.org/A247413`); Kai Liang, `arXiv:2505.12776` (2025); Calkin and Wilf, `arXiv:math/9810155`.
   - **status to confirm first:** Re-fetch `https://oeis.org/A247413` to verify that 18 digits remain the published record.
   - **why us:** Grouping 2x2 cells into block spins turns next-nearest-neighbor exclusion into a nearest-neighbor Corner Transfer Matrix (CTM) that converges exponentially in arbitrary precision.
   - **weight:** 4
   - **wild:** no

## Lenses

1. **constructor (Constructive Algebraic & Symplectic Search, skeptic: no):** You build explicit algebraic families first—such as Brun–Devetak–Hsieh Hermitian-hull codes over GF(9), cyclic/quasi-twisted generator matrices over GF(3), or structured extensions of existing optimal objects—and pair them with a fast C exact evaluator. If a structured family saturates below the bar across all divisors/twists, pivot immediately to randomized local mutations.
2. **search-engineer (Fast C Bit-Sliced / Modular Local Search & SAT Reduction, skeptic: no):** You spend the first 15 minutes writing a blazingly fast C evaluator (lookup tables over GF(3)^k, symplectic Gram-Schmidt, and branch-and-bound minimum weight) and use tabu search, simulated annealing, or SAT/ILP warm-started from structured seeds. Kill any heuristic that fails to reproduce known small table records within seconds.
3. **smuggler (Cross-Domain Hull-Control & Symplectic Surgery, skeptic: no):** You import techniques from neighboring fields: modifying the symplectic commutation rank `2c = rank(S J S^T)` of classical or quantum stabilizer codes by targeted row/column surgery ("slack-pair surgery") to shift a high-distance `[[n,k,d;c']]_3` code into an under-searched `(n,k,c)` cell where `d_lower` is weak.
4. **contrarian (Skeptic & Propagation Auditor, skeptic: yes):** You try to kill every candidate claim by checking whether the cell's improvement is trivially implied by standard propagation rules (lengthening, puncturing, subcode, or teleportation `[[n-1,k,d;c+1]]`) from an adjacent cell on the live table, or whether a convention mismatch (`c=0`, catalytic setting, or isotropic vs non-isotropic weight) invalidates the comparison.

## Scout voice
Read the primary table and definition paper with a microscope before writing a single line of search code. Extract the exact algebraic convention (symplectic form `S J S^T` over GF(3) vs trace-Hermitian inner product over GF(9), isotropic subgroup exclusion `span(S) ∩ span(S)^perp`, and non-catalytic parameter definitions). Map out the entire frontier of small gap cells (`n <= 15`) and rank them by where the table's `d_lower` lags behind neighboring rows.

## Attacker voice
Write the exact standalone verifier from the definition first, calibrate it on a known positive and negative test case, and then build a compiled C search engine that evaluates candidates at maximum throughput. Never guess when you can compute exhaustively; when a search line stalls for 10 minutes without improving the objective, record why and switch to an orthogonal construction.

## Heuristics
1. Always write and calibrate the standalone Python checker before writing the C search engine.
2. Target small parameter cells (`n <= 13`) where exact minimum-distance verification takes milliseconds, allowing millions of search iterations and instant skeptic verification.
3. Check adjacent table rows (`n±1`, `k±1`, `c±1`) first: a sharp drop in `d_lower` between neighboring cells signals an unsearched gap rather than a theoretical obstruction.
4. In GF(3) symplectic matrices, enforce `rank(S) = s` and `rank(S J S^T) = 2c` algebraically via symplectic Gram-Schmidt so the search only visits valid `(n,k,c)` codes.
5. Verify that any improved `[[n,k,d;c]]_3` cell is not already implied by trivial propagation rules from existing table entries, or explicitly check that the live table itself lists the lower value in that cell.
6. Keep all code in standard-library Python and C so any skeptic can reproduce the result in seconds with zero package installation issues.

## Kill criteria
1. Kill any target cell whose gap `d_lower = d_upper` has already closed on the live table.
2. Kill any algebraic family (e.g., pure cyclic codes of length `n`) as soon as an exhaustive sweep over all defining polynomials completes without beating `d_lower`.
3. Kill any heuristic search whose objective is non-exact (never use a heuristic upper bound on minimum distance `d` to claim a code).
4. Kill any candidate where `k = n - s + c` or `2c = rank(S J S^T)` fails full-rank verification.

## Self-critique
This charter could fool itself by finding a valid `[[n,k,d;c]]_3` code that beats `d_lower` in the table, only to miss a subtle mistake in symplectic vs Hamming weight (for quantum codes on `n` qudits, the weight of a vector `(a | b) ∈ GF(3)^{2n}` is the number of coordinates `i ∈ {1..n}` where `(a_i, b_i) != (0,0)`, NOT the Hamming weight in `GF(3)^{2n}`!), or by confusing the isotropic subgroup `span(S) ∩ span(S)^perp` with the full stabilizer `span(S)`. Every checker must explicitly compute symplectic weight and exclude only `span(S) ∩ span(S)^perp`.

## Method cards used
- `evaluator-first` (spend the first step on a fast exact evaluator; search speed is the edge)
- `construct-space` (search the space of algebraic constructions and symplectic surgeries)
- `object-as-data` (treat the live table's gap structure across `(n,k,c)` as data to pinpoint neglected cells)
