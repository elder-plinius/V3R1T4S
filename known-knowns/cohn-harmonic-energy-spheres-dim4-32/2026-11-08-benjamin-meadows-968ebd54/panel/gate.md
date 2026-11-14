# Honesty gate: cohn-harmonic-energy-spheres-dim4-32 64-20

gate_by: packaging run, after reading reproduce.md, novelty.md and criterion.md for this claim
gate_time_utc: 2026-11-08T03:05Z

status: CONFIRMED_SOLUTION
panel: reproduce pass: true; novelty pass: true; criterion pass: true
confirmed_scope: 64 unit vectors in R^20 (object/64-20.txt) with harmonic energy E* = sum_{i<j} |x_i - x_j|^-18 = 6.68546368135722749098 (mpmath at 40 digits and Decimal at 60), lower than the only table energy 6.7232495038 for (N, n) = (64, 20) at https://cohn.mit.edu/harmonic-energy/ by 0.0378; a nondegenerate local minimum; not a simplex or cross polytope; and in a different basin from the 2021 data set's configuration, which polishes to 6.7232495037738.
conditions: the universal-optima page https://cohn.mit.edu/harmonic-optima now returns 404; that clause was settled from its 2024-06-04 Wayback copy (no universal optimum in R^20; its conjectured optima there are N = 56 and 120), the table's own optimality marks and Cohn-Kumar Table 1; arXiv's API rate-limited part of the search, which used the arxiv.org search pages instead; the same configuration is in packing-records v1.3; the table keeper was emailed 2026-11-08.
