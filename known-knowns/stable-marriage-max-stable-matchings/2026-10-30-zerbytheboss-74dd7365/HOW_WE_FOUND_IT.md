# How We Found It

contributor text, unverified

We investigated the structure of the Irving-Leather rotation poset and its downsets for stable marriage instances of size $n \ge 14$.
For prime orders like $n=19$, where no non-trivial lexicographic product $A[B]$ exists, records depend on the existence of dense rotation posets with wide antichains.
We designed a parallel simulated annealing search engine operating over preference matrix permutations guided by rotation poset downset evaluation.
The search discovered an order $n=19$ instance with 128 rotations and 95,449 memoized subproblems, yielding exactly 642,696 stable matchings.
We independently verified this count using a complete Gusfield breakmarriage lattice walk from the man-optimal to the woman-optimal matching, confirming zero blocking pairs on every visited matching.
