context: subagent

# Criterion Skeptic Verdict

## Literal Check Against Success Criterion (2) in `CLAIM.md`
- **Target cells (>= 4 required)**: `CLAIM.md` and `table1_cells.json` claim 5 newly resolved cells of Brown et al. (2020) Table 1:
  - Odd-by-even grids from `{L_{5 x 8}, L_{6 x 7}, L_{5 x 10}, L_{6 x 9}, L_{7 x 8}, L_{7 x 10}, L_{8 x 9}, L_{9 x 10}}`: `L_{5x8}` (`G = 0`, 2nd-player win), `L_{6x7}` (`G = 3`, 1st-player win), and `L_{5x10}` (`G = 1`, 1st-player win).
  - Odd-by-odd grids from `{L_{5 x 9}, L_{7 x 7}, L_{7 x 9}, L_{9 x 9}}`: exact nimbers `L_{5x9}` (`G = 4`) and `L_{7x7}` (`G = 1`), satisfying the requirement that outcome-only claims do not count for odd-by-odd grids.
- **Two independent solvers using distinct algorithms**:
  - `nk_solver.cpp`: 128-bit bit-parallel Sprague-Grundy `mex` DP with connected-component XOR splitting, path/cycle octal `.137` folding, true-twin collapse, and 1-WL + individualization-refinement canonical keys.
  - `pn_solver.cpp`: `G + *k` P/N alpha-beta nimber prover with short-circuiting move search, smallest-component-first XORing, no octal `.137` table, and geometric `D_4`/`D_n` canonicalization.
- **Calibration & minor gaps noted**:
  - `A316632` (`n = 1..17`): explicitly covered by both `nk_solver` (`calibrate`) and `pn_solver` (`REPRODUCE.md` loop).
  - `A316533` (`n = 5..26`): `table1_cells.json`, `REPRODUCE.md`, and `nk_solver` `calibrate` only run odd indices `n = 5..25` (even indices `n = 6..26` are 0 by Theorem 12 of Brown et al., and are supported by both solvers' `gp` CLI mode but not explicitly invoked in `REPRODUCE.md`).
  - Table 1 shaded entries: `table1_cells.json` and `REPRODUCE.md` explicitly test `L_{5x5}`, `L_{5x6}`, `L_{5x7}` (plus `L_{3xn}` via `A316632`); other shaded entries (`m <= 4` or even-by-even grids) are not explicitly listed in `REPRODUCE.md` or `table1_cells.json` (though supported by both solvers' `grid` CLI mode).
  - `pn_solver.cpp`'s built-in `calibrate` mode only runs `A316632 (1..12)` and `A316533 odd (5..17)`; full calibration relies on the loops in `REPRODUCE.md`.
- **Novelty / non-subsumption**: `scout_record.md` confirms all 5 claimed Table 1 cells remain open in Brown et al. (2020) and no extensions beyond `A316632` `a(17)` or `A316533` `a(26)` were found.

confirmed_scope: Claimed Criterion (2) scope covers 5 newly resolved open cells of Brown et al. (2020) Table 1 (`L_{5x8}=0`, `L_{6x7}=3`, `L_{5x9}=4`, `L_{7x7}=1`, `L_{5x10}=1`) via two distinct exact solvers (`nk_solver.cpp` and `pn_solver.cpp`), with `REPRODUCE.md` explicitly calibrating `A316632` (`n=1..17`), odd `A316533` (`n=5..25`), and Table 1 shaded entries `L_{5x5}`, `L_{5x6}`, `L_{5x7}`.

pass: true
