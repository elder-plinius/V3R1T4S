# How We Built It — `coin-basket-random-expected-values`

## Exact Integer Solvers
This directory contains the independent compiled backward-induction solvers that computed the new terms:

1. `solver1_rust.rs`: Multi-threaded Rust solver using colexicographical combinatorial ranking and parity difference profile indexing for k=2, and sorted-partition indexing for k=3.
   - Compilation: `rustc -O -C target-cpu=native solver1_rust.rs -o solver1_rust`
   - Execution: `./solver1_rust 2 25` (for k=2, n=1..25) and `./solver1_rust 3 21` (for k=3, n=1..21)

2. `solver2_cpp.cpp`: Independent multi-threaded C++20 solver using layer-by-layer dynamic programming with OpenMP/std::thread parallelization over subset layers.
   - Compilation: `clang++ -O3 -std=c++20 -pthread solver2_cpp.cpp -o solver2_cpp`
   - Execution: `./solver2_cpp 2 25` and `./solver2_cpp 3 21`

3. `PREREG.md`: The pre-registration protocol defining the search, verification invariants, and success criteria.
