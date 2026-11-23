# Run It Yourself (`RUN_IT_YOURSELF.md`)

All commands below run from the root of this package folder in a fresh shell.

## 1. Run the Standalone First-Principles Checker (~13 seconds, Python 3.10+ and the standard library)

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
[1/4] Checked toroidal table for n=1..16 (direct game-tree solve for n=1..12) in 0.52s
[2/4] Verified 21-orbit ply-3 strategy certificate for G(TQ_14) = 1 (all 144 replies in H_14 refuted) in 3.65s
[3/4] Checked planar margin tables (direct R_8, R_10, R_12 solves and the R_14 mutual-reply certificate) in 9.08s
[4/4] Checked planar A344227 table for n=0..16 (exact mex solve for n=0..8) in 0.35s
All checks passed in 13.61s.
PASS
```

The quick check directly solves the toroidal game trees for sizes 1–12 and
checks the independent size-14 certificate against every legal reply. It
directly solves the planar margins at sizes 8, 10 and 12, verifies the
size-14 planar mutual-reply certificate, and directly solves the planar
nimbers at sizes 0–8. For the remaining values it checks the board geometry
and recorded results for consistency. Use the C++ commands below to
recompute those outcomes and margins in full.

## 2. Recompute the Claimed Values with the Two C++ Solvers

### 2.1 Pure-Python Unhinted Full-Tree Verification of $G(TQ_4 \dots TQ_{14})$ (~8–23 seconds)

```sh
python3 how-we-built-it/verify_tq14_python.py
```

### 2.2 Solver A (`evaluator-first`: $D_4$-Zobrist alpha-beta + BMI2 `_pext_u64` local leaf masks)

Requires `g++` with C++20, OpenMP (`-fopenmp`), and x86_64 BMI2 (`-march=native`):

```sh
g++ -O3 -march=native -fopenmp -std=c++20 how-we-built-it/solver_a_full.cpp -o solver_a_full
./solver_a_full 1   # Part 1: Toroidal G(TQ_1..16) and H_n winning-reply counts (~2-4 seconds)
./solver_a_full 2   # Part 2: Central-strike refutation margins R_8..16 (~6 minutes; R_8..14 takes ~2 seconds)
./solver_a_full 3   # Part 3: Planar OEIS A344227(0..16) calibration (~10 minutes)
rm -f solver_a_full
```

### 2.3 Solver B (`retrograde-dag`: bottom-up complete Node-Kayles tables $W_0 \dots W_8$ + collision-free 256/384-bit canonical keys + $\tau$-reflection leaf detection)

```sh
g++ -O3 -march=native -fopenmp -std=c++20 how-we-built-it/solver_b_tq.cpp -o solver_b_tq
./solver_b_tq       # Toroidal G(TQ_1..16) and H_n winning-reply counts (~25-60 seconds)
rm -f solver_b_tq

g++ -O3 -march=native -fopenmp -std=c++20 how-we-built-it/solver_b_margins.cpp -o solver_b_margins
./solver_b_margins 1  # Central-strike refutation margins R_8..16 (~6 minutes; R_8..14 takes ~4 seconds)
./solver_b_margins 2  # Planar OEIS A344227(0..16) calibration (~10.5 minutes)
rm -f solver_b_margins
```
