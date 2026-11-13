# How We Found It (contributor text, unverified)

1. The reference Python scripts linked from OEIS A316632/A316533 used NetworkX `is_isomorphic` in a linear scan over all seen graphs.
2. We built two independent C++20 128-bit bit-parallel solvers:
   - `nk_solver.cpp` (`evaluator-first`): connected-component XOR splitting, $O(1)$ path/cycle octal `.137` folding, true-twin collapse, and 1-WL + individualization-refinement exact canonical keys.
   - `pn_solver.cpp` (`search-engineer`): `G + *k` P/N alpha-beta short-circuiting prover with smallest-component-first XORing and geometric $D_4$/$D_n$ symmetry normalization.
3. Both solvers reproduced all calibration terms (`A316632` `n=1..17`, odd `A316533` `n=5..25`, shaded Table 1 `L_{5x5}=3, L_{5x6}=3, L_{5x7}=2`) and agreed on 5 newly resolved Table 1 cells: `L_{5x8}=0`, `L_{6x7}=3`, `L_{5x9}=4`, `L_{7x7}=1`, `L_{5x10}=1`.
