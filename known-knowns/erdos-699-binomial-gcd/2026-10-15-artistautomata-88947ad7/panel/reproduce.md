# REPRODUCE skeptic verdict: erdos-699-binomial-gcd, partial win p3 (exhaustive n <= 10^9)

context: subagent (fresh context, given only claim/)

## Definition checked (quoted from claim/CLAIM.md)
"for every n with 4 <= n <= 10^9 and every pair of integers 1 <= i < j <= floor(n/2), some prime p >= i
divides both C(n,i) and C(n,j)"

## Own checker, written from the definition before opening the author's code
Before opening any file under claim/code/ I wrote `mine/my699.c` (md5 1fe0c4b7790df0440c3cf6cdda870d2b). It has its own
segmented factor sieve, its own CRT generator and a different search: survivor sets are filtered incrementally over i,
which the author's code does not do. The steps, each derived again here:
1. G = n - (largest prime <= n). If i > G, the prime q = n - G lies in (n-i, n]. Then q > n-i >= n/2 >= j > i, so q
   divides the numerator of C(n,i) and of C(n,j) and divides neither i! nor j!. Also q >= i. So these i are settled.
2. i = 1: j*C(n,j) = n*C(n-1,j-1). If gcd(n, C(n,j)) = 1, then n | j, which is impossible for 0 < j < n. Any prime
   divisor of the gcd is >= 1 = i.
3. For 2 <= i <= min(G, floor(n/2)-1) the program builds S_i, the exact set of primes p >= i that divide C(n,i):
   - primes p > G: since p > i, p | C(n,i) exactly when p divides some n-k with k < i. These come from factoring the
     window. A prime p > G can divide at most one number in a window of length G.
   - primes p in [i, G]: Lucas digit test on (n, i).
   A counterexample j is a j in (i, floor(n/2)] that is base-p digit-dominated by n for every p in S_i (Lucas).
   Candidates come from CRT on the necessary condition j mod p <= n mod p. Every candidate then gets the full Lucas
   test against all of S_i. The survivor set built from the primes > G is kept across i; this is sound because that
   set only grows as i grows and the j-range only shrinks. The small primes are applied freshly for each i.
   Counterexamples are printed, never discarded.

## Validation of my checker
- Brute force taken directly from the definition (`mine/brute.py`): exact gcd of the exact binomials, with prime
  factors < i (or <= i for the strict variant) removed. For n <= 400: 0 counterexamples (non-strict). In the strict
  variant (p > i) it finds 5 exceptions, identical to my699's (diff: `SAME`).
- `mine/naive.c` (Legendre valuation for every prime, every j, no reductions). `./naive 4 600 1` checks all i, not
  only the cases: `NAIVE A=4 B=600 cases=1939 pairs=8955050 fails=0`. `./naive 1000000 1000100`:
  `cases=1511 pairs=755522230 fails=0`, and my699 gives the same `cases=1511`.
- Positive controls (strict variant), my699:
  `./my699 4 100000 1` -> (10,3,5) (16,2,6) (28,3,14) (28,5,14) (244,3,122) (512,2,147) (2048,2,713) (2188,3,1094),
  `counterexamples=8`. The first six match results/calib_compare.txt. `./my699 1594324 1594324 1` ->
  `COUNTEREX n=1594324 i=3 j=797162`, matching results/positive_controls.txt. The checker does detect failures.
- Calibration counts match the author's: `./my699 4 3000` -> cases=13915 (results/seg_3000.txt);
  `./my699 4 100000 1` -> cases=779987 (results/seg_4_100000.txt).

## Full range, own program (exhaustive, not a sample)
I ran 1001 chunks of 10^6 matching the author's boundaries, plus [10^9, 10^9], with 3 workers at nice 10. Wall time
was about 40 minutes, with another job using CPU at the same time. `mine/cmp.py` checks each chunk: the range,
nchecked = B-max(A,4)+1, counterexamples=0, and my cases equal to the author's cases in
results/seg699_chunk_summaries.txt.
```
{'chunks': 1001, 'n': 999999997, 'cases': 16738476359, 'cex': 0, 'fallback': 139} maxG 281
missing 0 []
bad []
ALL_CHUNKS_MATCH_AND_ZERO_COUNTEREXAMPLES n=4..1e9
```
The total cases, 16738476359, equals the author's results/coverage_output.txt. maxG = 281 is right for the known
largest prime gap below 10^9 (282, after 436273009). Every n in [4, 10^9] was checked: 999,999,997 values, 0
counterexamples.

## Re-running the author's program, and determinism
I compiled code/seg699.c myself (`gcc -O2`) and re-ran it on chunks A = 0, 123e6, 436e6 (the maximal-gap chunk),
777e6, 999e6 and [1e9, 1e9]. Each DONE line is byte-identical to its line in results/seg699_chunk_summaries.txt. My
own re-runs of the same 6 chunks are byte-identical to my first run (deterministic). Example:
```
MYDONE A=436000000 B=436999999 nchecked=1000000 cases=16797204 enumerated=1370132 counterexamples=0 fallback=0 maxG=281 maxest=834902
DONE A=436000000 B=436999999 strict=0 cases=16797204 enumerated=56081268 overflow=0 candidates=0
```
The "enumerated" counts differ, as they should for two different algorithms. The cases and the zero-counterexample
results agree.

## Author's code (read after my checker)
code/seg699.c uses the same reduction (primes > i from the factored window, plus p = i by Legendre) and a CRT plus
full-Lucas filter. Its overflow branch drops constraints only (the candidate set becomes a superset), so it stays
sound, and every chunk reports overflow=0 and candidates=0. I did not re-run fast699, third699 or sample_windows. My
independent full-range run supersedes them for the exhaustive claim.

## Verdict
Confirmed. For all 4 <= n <= 10^9 and all 1 <= i < j <= floor(n/2), my independently written exhaustive checker finds
a prime p >= i dividing both C(n,i) and C(n,j). It agrees chunk by chunk with the author's case counts, and the
author's sampled chunks reproduce byte for byte. No mismatch, no missing chunk, no non-determinism.

pass: true
