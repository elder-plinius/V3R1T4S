# Criterion skeptic verdict: claimed partial win p3 (Erdos #699)

context: subagent (fresh context, given only claim/)

## What p3 requires, read literally
1. Exhaustive: every n <= 10^9 and every valid pair 1 <= i < j <= floor(n/2).
2. Goes beyond Cong's n <= 10^7 and the targeted ~1.34e8 checks.
3. Reproduced by an independent implementation, in the bank's own example form: a random sample of n checked by different code, plus a full Kummer scan.

## Findings
- Reduction re-derived. If a prime p lies in [n-i+1, n] with i < j <= floor(n/2), then p >= n-i+1 > n/2 >= j > i. So p is a factor of n(n-1)...(n-j+1) but not of j!, which means it divides C(n,i) and C(n,j), and p >= i. Skipping such (n,i) is valid, and so is the early `break` in code/seg699.c, since the property holds for every larger i too.
- code/seg699.c read line by line:
  - P(n,i) is complete. For p > i, p | C(n,i) exactly when p divides some n-k with k < i. The case p = i is tested with Legendre's formula.
  - The Kummer/Lucas non-divisibility test is correct.
  - The CRT step x' = x + M((r-x)M^{-1} mod p) is correct, with no u64 overflow (M <= n/2 before each multiply).
  - The ranges are right: i in [1, floor(n/2)-1] and j in (i, floor(n/2)].
  - The sieve segment starts at A-1000, which exceeds the largest prime gap below 10^9. Out-of-segment access aborts the run.
  - W=12 distinct prime factors is enough, since numbers <= 10^9 have at most 9.
  - If the cap overflows, it only weakens the filter, so the scan stays sound, and overflow is 0 everywhere.
- Boundaries. n <= 3 has no pairs. The scan starts at n=4. n = 10^9 is a separate chunk (cases=63, 0 candidates). j = floor(n/2) is included.
- Coverage. results/coverage_output.txt shows 1001 contiguous chunks, no gaps, all with candidates=0 and overflow=0. That gives 1.67e10 (n,i) cases, well beyond 10^7 and 1.34e8.
- Independence:
  - code/fast699.c is genuinely different code with a different algorithm: large primes as (n-b)/a, digit seeding, and gap-based case selection.
  - code/third699.py is a separate Python implementation (Miller-Rabin, trial division, Legendre).
  - code/indep699.c uses the same algorithm as seg699, so it is not independent and I give it no weight.
  - Caveat: matching case counts mostly checks prime-gap structure. The substantive agreement is that each program independently reports 0 candidates.
- Sample size. The full scan was done by a single implementation, seg699. Independent reproduction covers:
  - fast699 on every n in [4, 10^5] and [10^7, 7.7e7), about 6.7% of the range;
  - fast699 on 300 random windows of 2,000 n across [10^5, 10^9);
  - third699.py on 200 random n in [10^8, 10^9).

  All of these agree. This matches the bank's example, which is a sample plus a full scan, so I accept it as adequate.
- Null model / sensitivity. Strict mode (p > i only) finds the known exceptions, including (28,5,14), 2048, 2188 and 1594324, so the pipeline can detect positives.

## My own checks
- Compiled the three C programs. Reran seg699 on chunks [617000000, 617999999], [999000000, 999999999] and [10^9, 10^9]. All three match their lines in results/seg699_chunk_summaries.txt exactly.
- Ran fast699 and seg699 on [999997000, 10^9], a boundary window that includes n = 10^9. Both give 55767 cases and 0 candidates.
- Reran seg699 4 3000 0 (cases=13915, 0 candidates) and brute699 3000 0 (fails=0).
- Wrote my own direct-gcd checker using exact binomials, gcd, and stripping primes below i, for all n <= 600. It finds 0 failures. Its strict-variant list is exactly results/calib_compare.txt's list: (10,3,5), (16,2,6), (28,3,14), (28,5,14), (244,3,122), (512,2,147).

## Subsumption
Nothing in the package claims (A) or (B). p3 is not subsumed by any wider claim. It strictly extends the n <= 10^7 computation cited in CLAIM.md.

confirmed_scope: For every n with 4 <= n <= 10^9 and every pair 1 <= i < j <= floor(n/2), the exhaustive Kummer/Lucas scan code/seg699.c (1001 contiguous chunks, 0 candidates, 0 overflow) finds a prime p >= i dividing both C(n,i) and C(n,j), and independently written programs reproduce its zero-candidate result on samples only (code/fast699.c on all n in [4, 10^5] and [10^7, 7.7e7) plus 300 random 2,000-n windows, code/third699.py on 200 random n in [10^8, 10^9)), not by a second full scan.

pass: true
