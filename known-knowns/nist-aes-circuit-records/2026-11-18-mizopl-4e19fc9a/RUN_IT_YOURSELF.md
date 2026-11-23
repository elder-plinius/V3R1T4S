# Run It Yourself

## 1. Zero-Dependency Offline Verification of All `13` Circuits (`< 0.3s`)

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final line (`exit 0`):

```text
PASS
```

## 2. Adversarial Negative Control (`--corrupt`, `exit 1`)

```sh
sh verify-it-yourself/run_checks.sh --corrupt
```

## 3. Re-Compiling the C++17 Search Engines & Running Python Exact Audits

```sh
clang++ -O3 -std=c++17 -pthread how-we-built-it/xorflux_cpp.cpp -o xorflux_cpp
./xorflux_cpp --targets how-we-built-it/invmixcols_targets.txt --seeds how-we-built-it/seed_92_10.txt --self-test
clang++ -O3 -std=c++17 how-we-built-it/synthesize_invsbox_gd10.cpp -o synthesize_invsbox_gd10
clang++ -O3 -std=c++17 -pthread how-we-built-it/gd10_super_synth.cpp -o gd10_super_synth
python3 -B how-we-built-it/tier1_exact_solver.py
python3 -m pip install -r how-we-built-it/requirements.txt
python3 -B how-we-built-it/exact_toplayer_milp.py --circuit object/aes-invmixcols-xor92-depth10.circ.txt --func invmixcols --depth 10
```
