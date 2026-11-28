# How We Found It

*contributor text, unverified*

Following Cremer (arXiv:2610.18740v1) and Gasarch-Kelly-Pugh (1996), finding the $i$-th element of $n$ elements with minimum comparisons can be framed as acyclic poset decision graph synthesis.

We compiled Cremer's `core32` proof-number search engine with 192-bit canonical state keys, LTO thin, and the 1.66M-state precomputed $n \le 12$ groundtruth oracle table. For $n=18$, proof-number search with transposition table size $B=23$ successfully proved decision graphs strictly beating both Gasarch-Kelly-Pugh 1996 Table 3 and Hadian-Sobel bounds at $(18, 9) \le 34$, $(18, 8) \le 35$, $(18, 7) \le 34$, and $(18, 6) \le 31$.
