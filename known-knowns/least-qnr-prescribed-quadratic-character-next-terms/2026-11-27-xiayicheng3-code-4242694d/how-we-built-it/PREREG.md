# PREREG (frozen 2026-11-27T16:30:48Z, before any attack output)

Criterion (verbatim, bank): see target.md. Cell: A002224(42) (n = 42), "the next unknown index" of A002224 per the live
b-file fetched 2026-11-27T16:27:36Z.

Statistic / checker:
1. Property: checker/check_a002224.py q 42 prints property=True (deterministic MR, q = 1 mod 8, Euler's criterion
   p^((q-1)/2) = 1 mod q for all 42 primes 2..181).
2. Minimality: an exhaustive enumeration of all q = 1 mod 8 in [1, X] with q mod p a nonzero QR for every odd prime
   p <= 113 (the first 30 primes), followed by primality and Euler-criterion checks of every survivor. X = 1e16.
   The enumeration must first reproduce every term A002224(30..41) of the live b-file exactly (calibration). Any
   mismatch voids the run.
3. Independence: lens 2 repeats the enumeration with a different CRT modulus and a different loop structure; the two
   survivor lists for the first 41 primes (2..179) QR must be identical.

Thresholds:
- Full win: the least prime q <= 1e16 with property(q, 42) = True, both lenses agreeing, calibration passing.
- Partial win p1 ("A002224(42) exceeds 10^16"): no such q <= 1e16, both lenses agreeing, calibration passing.
- Anything else: nothing.

null_test: not needed because the claim is an explicit object (or an exhaustive empty search) judged by a
deterministic checker and a complete enumeration, not a statistical or "beats chance" search.
