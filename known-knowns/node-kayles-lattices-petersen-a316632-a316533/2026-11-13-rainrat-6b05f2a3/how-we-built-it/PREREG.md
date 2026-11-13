# Pre-registration (`PREREG.md`)

- **Frozen at (UTC)**: `2026-11-13T00:53:30Z`
- **Target**: `node-kayles-lattices-petersen-a316632-a316533`

## Success Criterion (verbatim)
CONFIRMED: (1) the next 5 contiguous exact terms of OEIS A316632 (G(L_{3 x n}) for n = 18..22) AND the next 12 contiguous indexed terms of OEIS A316533 (G(GP(n,2)) for n = 27..38, comprising the 6 unknown odd indices n = 27, 29, 31, 33, 35, 37 and the 6 even indices which equal 0 by Theorem 12), OR (2) at least 4 newly resolved cells of Brown et al.'s Table 1, consisting of exact Sprague-Grundy nimbers (or certified 1st/2nd-player outcomes) for unknown-outcome odd-by-even grids in {L_{5 x 8}, L_{6 x 7}, L_{5 x 10}, L_{6 x 9}, L_{7 x 8}, L_{7 x 10}, L_{8 x 9}, L_{9 x 10}} and/or exact Sprague-Grundy nimbers for odd-by-odd grids in {L_{5 x 9}, L_{7 x 7}, L_{7 x 9}, L_{9 x 9}} (outcome-only claims do not count for odd-by-odd grids since Theorem 5 already proves G > 0). All claimed values must be computed by two independently written solvers using distinct algorithms that both reproduce every shaded (published) entry in Table 1 of Brown et al. (2020) (including G(L_{5 x 7}) = 2) and all published terms of A316632 (n = 1..17) and A316533 (n = 5..26).

## Partial Wins (verbatim)
- `p1`: Extend OEIS A316632 (Node-Kayles on the 3 x n lattice) contiguously through n = 20 (n = 18, 19, 20) and OEIS A316533 (Node-Kayles on GP(n,2)) contiguously through n = 32 (including odd n = 27, 29, 31), verified by two independent Sprague-Grundy solvers that reproduce all published terms.
- `p2`: Settle the 1st/2nd-player outcome (or exact nimber) of the two smallest open odd-by-even outcome cells in Brown et al. Table 1 (the 40-vertex lattice L_{5 x 8} and the 42-vertex lattice L_{6 x 7}) OR determine the exact Sprague-Grundy nimbers of the two smallest open odd-by-odd cells (L_{5 x 9} and L_{7 x 7}), verified by two independent solvers that reproduce all published cells of Table 1 (including G(L_{5 x 7}) = 2).

## Verification Protocol & Thresholds
- Every claimed term or cell must be computed by two independently written solvers using distinct algorithms (e.g., Solver A: connected-component Sprague-Grundy DP with canonical graph isomorphism / exact bitmask hashing; Solver B: independent Sprague-Grundy / heap-sum `G + *g` alpha-beta or distinct-algorithm solver).
- Both solvers must reproduce 100% of:
  - A316632 (`n = 1..17`): `[2, 1, 1, 0, 3, 3, 2, 2, 2, 3, 3, 5, 2, 4, 1, 3, 2]`
  - A316533 (`n = 5..26`): `[1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]`
  - Shaded Table 1 entries of Brown et al. (2020), including `G(L_{5 x 5}) = 3`, `G(L_{5 x 6}) = 3`, `G(L_{5 x 7}) = 2`.
- Zero discrepancies allowed between Solver A and Solver B on any claimed value.

## Null Test
null_test: not needed because this target computes exact deterministic Sprague-Grundy nimbers and game outcomes checked by two independent exact solvers against published OEIS sequences and Table 1 of Brown et al. (2020).
