# Preregistration: coin-basket-random-expected-values

Frozen: 2026-10-28T00:32:45Z

## Verbatim Success Criterion
CONFIRMED: the exact integer values of A391791(23), A391791(24), A391791(25) AND A391792(19), A391792(20), A391792(21) (K = 3 new terms of each; direction: new terms), under the entries' own definitions (a(n) = k^(n-1) times the maximum, over all adaptive placement strategies, of the expected largest basket sum; baskets chosen independently and uniformly each turn; coins 1..n each used exactly once), each computed by two independently written exact programs that (i) agree on every new term, (ii) reproduce every published term (A391791 n = 1..22, A391792 n = 1..18), and (iii) use integer or rational arithmetic only (no floating point anywhere in the value recursion). The terms must not already be in the OEIS entries, their b-files or their edit history at verification time. Submitting to the OEIS is an action for the human only.

## Partial Wins
- p1: The three new terms of only one of the two sequences (A391791 n = 23..25, or A391792 n = 19..21), with the same two-program confirmation and calibration.
- p2: A settled status for A391791's stated conjecture over a range: for every n from 10 through the largest n computed, the full set of optimal first moves listed exactly, either confirming that coin floor((n+3)/2) is optimal for each n or giving the first n where it is not (a counterexample to the conjecture as stated in the entry).

## Deterministic Exact Checker
Two independently written compiled solvers (Solver 1 in Rust, Solver 2 in C++) will implement the exact integer recurrence:
W(R, s) = sum_{b=1}^k max_{c in R} W(R \setminus {c}, s + c*e_b)
with base case W(empty, s) = max(s).
Both solvers will evaluate intermediate and final values in 64-bit/128-bit unsigned integers without any floating point approximation.
Agreement must be 100% exact across all terms:
- Calibration: exact match on A391791 for all n in 1..22.
- Calibration: exact match on A391792 for all n in 1..18.
- New terms: exact match on A391791(23..25) and A391792(19..21).
- Conjecture p2: exact match on optimal first move sets for n in 10..25.

null_test: not needed because deterministic exact integer backward induction produces unique mathematical values verified by two independent compiled solvers against OEIS definitions and b-file tables
