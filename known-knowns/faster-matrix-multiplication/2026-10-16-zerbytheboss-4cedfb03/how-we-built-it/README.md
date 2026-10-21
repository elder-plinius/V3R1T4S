# How the scheme was built

Contributor text and code; no panel audits the search, only the object.

`flip4.py` runs the randomized walk (flip and isotopy moves on rank-38 schemes, ternary-preserving), calling Perminov's ternary_addition_reducer (https://github.com/dronperminov/ternary_addition_reducer, third-party, not shipped) to obtain a reduced SLP for each candidate; `lib.py` is the exact Brent and reduced-count checker used in the loop; `mk.py` is a helper that writes Perminov-layout JSON. Starting schemes are Perminov's 3x4x4_m38 files (third-party, not shipped). Requirements: python3, numpy, a C++ compiler for the reducer. Exact commands and seeds were not archived beyond the argument list of flip4.py (seed, duration, input file, tag, pplus, gp, piso); a rerun gives a scheme of similar cost, not this exact file.
