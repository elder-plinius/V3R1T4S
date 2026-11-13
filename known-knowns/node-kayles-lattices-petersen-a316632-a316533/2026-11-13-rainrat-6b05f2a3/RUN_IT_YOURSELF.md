# Run It Yourself

From this package root:
```sh
sh verify-it-yourself/run_checks.sh
```
This compiles both independent C++20 solvers (`how-we-built-it/nk_solver.cpp` and `how-we-built-it/pn_solver.cpp`), verifies all calibration values (`A316632` `n=1..17`, odd `A316533` `n=5..25`, shaded Table 1 `L_{5x5}=3, L_{5x6}=3, L_{5x7}=2`) and all 5 claimed Table 1 cells (`L_{5x8}=0, L_{6x7}=3, L_{5x9}=4, L_{7x7}=1, L_{5x10}=1`) against `object/table1_cells.json`, and prints `PASS`.
