# How the scheme was built

Contributor text and code; no panel audits the search, only the object.

`flip4.py` runs the randomized walk (flip and isotopy moves on rank-45 schemes, ternary-preserving), calling Perminov's ternary_addition_reducer (https://github.com/dronperminov/ternary_addition_reducer, third-party, not shipped) to obtain a reduced SLP for each candidate; `lib.py` is the exact Brent and reduced-count checker used in the loop; `mk.py` is a helper that writes Perminov-layout JSON; `dag_cone_collapse.py` converts each factor's SLP into a canonical binary DAG and applies an exact exclusive-cone 2-sum rewrite followed by single-use output folding (lowering the 167-addition walk candidate to 161 by reducing `V` from 61 to 60 additions). Starting scheme is Perminov's `2x4x7_m45_cr174_cn308_ZT_reduced.json` (third-party, not shipped). Requirements: python3, numpy, a C++ compiler for the reducer.
