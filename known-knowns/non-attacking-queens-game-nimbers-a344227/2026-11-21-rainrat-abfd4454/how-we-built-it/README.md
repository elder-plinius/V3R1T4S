# How We Built It (`how-we-built-it/README.md`)

## Contents

- `PREREG.md`: Pre-registration frozen at `2026-11-21T16:57:58+00:00` prior to the solver runs.
- `solver_a_full.cpp`: Solver A (`evaluator-first` lens) — C++20 bitboard solver using 8-way $D_4$ board-symmetry Zobrist hashing, a lockless 64-bit fingerprint transposition table, and hardware BMI2 `_pext_u64` local leaf evaluation (`k <= 14`).
- `test_tq_fast.cpp`: Fast toroidal probe for $TQ_1 \dots TQ_{18}$.
- `verify_tq14_python.py`: Pure-Python standard-library game-tree solver verifying $G(TQ_4 \dots TQ_{14})$ without ply-3 hints.
- `solver_b_tq.cpp`: Solver B toroidal solver (`retrograde-dag` lens) — C++20 bitboard solver using bottom-up precomputed complete Node-Kayles tables $W_0 \dots W_7$, collision-free 384-bit lexicographical $D_4((0,0))$ canonical keys (zero Zobrist hashing), and Theorem S1 $\tau$-reflection leaf detection.
- `solver_b_margins.cpp`: Solver B planar central-strike refutation margin and OEIS A344227 solver (`retrograde-dag` lens) — C++20 bitboard solver using a bottom-up precomputed 32 MiB complete Node-Kayles table $W_0 \dots W_8$ ($2^{28}$ graphs), collision-free 256-bit canonical keys, and embedded odd-subboard $\tau$-reflection leaf detection.

## Solver B implementation note (2026-11-23 UTC)

The frozen preregistration described induced-graph degree sequences and 1-WL
signatures for Solver B canonicalization. The shipped toroidal solver instead
chooses the lexicographically smallest full 384-bit board under the eight
symmetries fixing the origin, and stores that exact board as its transposition
key. The planar solver uses its own exact 256-bit board keys. Solver A uses
Zobrist fingerprints. The acceptance criteria and recorded results are as
stated in the frozen preregistration and panel.

## Exact Build and Run Commands

- **Toolchain**: `g++` (C++20, `-O3 -march=native -fopenmp`) and `python3` (3.10+, standard library only).
- See `../RUN_IT_YOURSELF.md` for the exact commands to compile and run each program.
