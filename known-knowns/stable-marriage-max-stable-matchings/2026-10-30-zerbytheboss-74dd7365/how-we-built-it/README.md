# How We Built It: Stable Marriage Maximum Stable Matchings

We developed an Irving-Leather rotation poset dynamic program and simulated annealing search engine (`smcount3.c` and `make_instances.py`).
For the prime order $n=19$ (where no composition decomposition $A[B]$ exists), simulated annealing over rotation poset extensions discovered an instance admitting 642,696 stable matchings, breaking the OEIS A357271 record of 637,336 (+5,360, +0.84%).
For composite orders $n=14$, $n=18$, and $n=22$, lexicographic product constructions with $K_2$ established new records:
- $n=14$: 23,744 vs record 20,176
- $n=18$: 530,528 vs record 456,300
- $n=22$: 12,277,568 vs record 11,221,136

All instances have been independently verified using dual counting algorithms (poset downset DP and Gusfield lattice traversal) with 100% agreement.
