# How the program was built

Everything here is contributor text and code; the panel did not audit the search, only the object.

## The search

`opt_scheme.py` splits a scheme into its three linear maps (U: the forms over A, V: the forms over B, W: the forms over
the products, stored transposed as in Perminov's layout), writes each as a 0/+1/-1 matrix, and runs a distance-guided
cancellation search on it. The search is the Boyar-Peralta heuristic for linear straight-line programs (pick the pair
of already-computed vectors whose sum or difference most reduces the total Hamming distance from the targets, with
ties broken by a secondary measure and by randomness), extended so that a sum may cancel coordinates, under the rule
that every intermediate must itself be a ternary vector (coefficients in -1, 0, 1), which is what Perminov's reduced
convention requires. `bpopt.c`, `bpopt4.c` and `bpopt5.c` are successive versions of that search (bpopt5 is the one
that produced the U and V programs here); `rectopt.c` and `slpopt.c` are earlier pair-greedy common-subexpression
searches kept for comparison. The W program was found by running the same search on the transpose of W and
transposing the resulting program back (the transposition principle: a straight-line program for a linear map M with
k additions gives one for M^T with k + (columns of M) - (rows of M) additions) using the strict variant bpopt6.
`dense2reduced.py` writes the result in Perminov's reduced-scheme JSON layout; `graphs.py` and `collect.py` are helpers.
The exact commands, seeds and time caps per map are in `COMMANDS.md` when present and otherwise in `SEARCH_REPORT.md`.

## Requirements

A C compiler (`cc -O2 -o bpopt5 bpopt5.c`), python3 3.8 or later; the checkers use only the standard library
(`sym_check.py` needs sympy).

## What is not here

Perminov's scheme files (third-party data): `the-record-we-beat/README.md` names the files and their sha256.
Intermediate search logs are not shipped; the result is reproduced by the checker, not by rerunning the search.
