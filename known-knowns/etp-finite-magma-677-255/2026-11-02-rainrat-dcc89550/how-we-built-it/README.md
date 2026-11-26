# How We Built It (`2026-11-02-rainrat-dcc89550`)

## 1. Files in `how-we-built-it/`

- `PREREG.md`: Pre-registered target criteria, null-test declaration, and lens plan frozen before experimentation (`2026-11-01T16:44:38Z`).
- `build_separation_models.py`: Standalone Python 3 script (standard library only) that generates `object/separation_models.json` (`Fin7`, `Fin25`, `Fin55`).
- `orbit_solver.cpp`: Exact C++17 constraint-propagation and backtracking solver used to verify the `Equation677` spectrum for `n = 1..8` and exclude counterexamples to `Equation677 => Equation255` for `n = 2..9`.

## 2. Exact Commands

Rebuild `object/separation_models.json`:
```sh
python3 how-we-built-it/build_separation_models.py object/separation_models.json
```

Verify both `object/separation_models.json` and `object/Equation677.lean`:
```sh
sh verify-it-yourself/run_checks.sh
```

Compile the C++ orbit-case solver (optional):
```sh
g++ -O3 -std=c++17 -fopenmp how-we-built-it/orbit_solver.cpp -o orbit_solver
./orbit_solver 8
```
