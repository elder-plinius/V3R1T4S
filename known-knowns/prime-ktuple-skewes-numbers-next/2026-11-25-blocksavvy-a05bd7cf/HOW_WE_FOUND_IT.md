# How we found it (contributor text, unverified)

The bank entry suggested a partial win: show no sexy-prime crossing below 10^14, because a check to 10^10 had found a growing deficit.
Before running the big sieve we compared the public OEIS A080841 counts with 4*C2*Li2(10^n): the deficit was +12726 at 10^11 but
-97764 at 10^12, so a crossing had to lie between them and the 10^14 partial win could not be true. A fast 6k+-1 bitset sieve
(2.5 minutes to 10^12 on 6 threads) with an Arb chord bound per block located the first block with a negative margin; an exact
per-pair Arb check inside that block gave p = 349018493647. A second, separately written sieve with an mpmath monotone bound found
the same p, and both agree block by block to 10^12. Calibration on twins and cousins fixed the counting convention (inclusive).
What failed: nothing dramatic; the first tries of the constant via a plain Euler product gave only 7 digits, so we used the
accelerated zeta-product identity with an explicit tail.
