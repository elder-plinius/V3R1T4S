# How the objects were built (exact commands; Python 3.9+, standard library only, single thread)

All code here is the run's own code, copied as it ran.

1. Exact solver (extender lens), points-needed coordinates, component-wise exact policy iteration (safeguarded Newton on the 2x2 cycle of each component, exact 2x2 rational solves). One run computes every n <= 45 and writes one certificate per n:

       python3 -I code/solver_extender.py 45 certs 1 45 values.txt --b-dir ../data

   (12.64 s for the exact solve at N = 45; generates n = 1..45 certificates and values table).

2. Independent solver (contrarian lens), a completely different algorithm: pure-turn-plan exact minimax, closed-form fixed point per component, no policy iteration:

       python3 -I code/solver_contrarian.py 45 values_contrarian.txt

   (62.96 s for the exact solve at N = 45).

3. Cross-comparison of both independent solvers:

       python3 -I code/cross_compare.py

   (Zero mismatches across all 45 terms; exact match with OEIS n = 1..15 and repository n = 16..30).
