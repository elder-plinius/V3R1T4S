# Erdős #699: no counterexample for any n <= 10^9 (partial win p3)

## What
For every n with 4 <= n <= 10^9 and every pair 1 <= i < j <= floor(n/2), the exhaustive Kummer/Lucas scan code/seg699.c (1001 contiguous chunks, 0 candidates, 0 overflow) finds a prime p >= i dividing both C(n,i) and C(n,j), and independently written programs reproduce its zero-candidate result on samples only (code/fast699.c on all n in [4, 10^5] and [10^7, 7.7e7) plus 300 random 2,000-n windows, code/third699.py on 200 random n in [10^8, 10^9)), not by a second full scan.

The panel's REPRODUCE skeptic also ran a second full exhaustive scan of every n in [4, 10^9] with its own
independently written program; case counts matched on all 1001 chunks (panel/reproduce.md). The confirmed scope above
is the CRITERION skeptic's sentence, kept word for word.

## Check it yourself
`sh verify-it-yourself/run_checks.sh`: expected last line `PASS`; about 1 minute on a laptop (Python 3 only). The
full rebuild is in RUN_IT_YOURSELF.md (about 4.5 h on 4 cores).

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| erdosproblems.com forum thread #699 | largest exhaustive check | all n <= 10^7 (Cong, 06 Jan 2026); targeted 2^k, k <= 27 and 3^m + 1, m <= 17 | https://www.erdosproblems.com/forum/thread/699 | 2026-10-15T00:13:42Z |
Status page https://www.erdosproblems.com/699 (fetched 2026-10-15T00:13:42Z, HTTP 200): open. Details in the-record-we-beat/.

## Not claimed
- Not a proof of the conjecture, and nothing about n > 10^9.
- Not the stronger p > i variant (which has known exceptions such as (28,5,14)).
- No claim about Cong's repository, which the panel could not reach (HTTP 403 from its network); a larger unposted run
  there would affect novelty, not correctness.

## Credits
- P. Erdős and G. Szekeres, who posed the problem [ErSz78]; Guy's Unsolved Problems in Number Theory, B31.
- T. F. Bloom, Erdős Problem #699, https://www.erdosproblems.com/699, and the forum thread.
- Cong (https://github.com/conglu1997/erdos_699_rust), whose exhaustive n <= 10^7 check and strict-variant exception
  list we compared against and used as positive controls.
- Liam Price (proof claim for j <= 3i/2 and n = 2j), Marco Del Pin, and the forum contributors cited on the thread.
- Kummer's and Lucas's theorems; Legendre's formula; Sylvester and Schur.
- The V3R1T4S kit, https://github.com/elder-plinius/V3R1T4S, which ran the work and the panel.
