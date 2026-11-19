# Run It Yourself — `coin-basket-random-expected-values`

## Quick Verification
To run the bundled quick check from within this package directory:

```bash
sh verify-it-yourself/run_checks.sh
```

Note that `verify-it-yourself/check_coin_basket.py` compares the `object/` files with values stored in the script and recomputes from the game definition only `n = 1..6` (`k = 2`) and `n = 1..4` (`k = 3`), so it does not validate the new terms (`A391791(23..25)` and `A391792(19..21)`). Recomputing all terms through `n = 25` (`k = 2`) and `n = 21` (`k = 3`) from the definition requires compiling the solvers in the next section.

Expected terminal output:
```text
=== Verification of Jehn's Random-Basket Coin Game ===
[1] Verifying format and integrity of object files...
[2] Verifying OEIS A391791 (k=2) published terms (n=1..22)... PASS
[3] Verifying OEIS A391791 (k=2) new terms (n=23..25)... PASS
[4] Verifying OEIS A391792 (k=3) published terms (n=1..18)... PASS
[5] Verifying OEIS A391792 (k=3) new terms (n=19..21)... PASS
[6] Verifying Jehn's conjecture audit for n=10..25... PASS
[7] Re-evaluating exact Bellman backward induction from scratch for small instances... PASS
All verifications succeeded with 100% exact integer arithmetic.
PASS
```

## How to Rebuild the Object Files from Scratch
To rebuild the exact integer solutions using the two independent compiled solvers:

### Solver 1 (Rust):
```bash
rustc -O -C target-cpu=native how-we-built-it/solver1_rust.rs -o solver1_rust
./solver1_rust 2 25 > A391791_rust.txt
./solver1_rust 3 21 > A391792_rust.txt
```

### Solver 2 (C++):
```bash
clang++ -O3 -std=c++20 -pthread how-we-built-it/solver2_cpp.cpp -o solver2_cpp
./solver2_cpp 2 25 > A391791_cpp.txt
./solver2_cpp 3 21 > A391792_cpp.txt
```

### Full Verification:
Compare the outputs with `diff A391791_rust.txt A391791_cpp.txt` to confirm bit-identical exact agreement.
