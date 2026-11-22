# How we found it (contributor text, unverified)

- Brief: the V3R1T4S bank target mertens-function-exact-values-next-terms has a partial win p1, "new terms of
  A084235 beyond a(17)". OEIS stopped at a(17) = 108500046711 (2014); published extrema (Hurst; A304241/A304242)
  put a(18) between 2.97e11 and 3.31e11, which a segmented Mobius sieve reaches on one 8-core machine.
- Run 1 (extender lens): a product-check segmented Mobius sieve in C with OpenMP, blocks of 1e8 from k = 1 to
  3.4e11, recording per block the sum and the max/min prefix, so the first block that can reach 2^n is known
  without storing M(k). Validation gates frozen in PREREG.md before measuring: M(10^8..10^11) from A084237 and
  a(14..17) from A084235 all reproduced. An exact scan of block 3300 gave k = 330055906058, M = -262144.
- Run 2 (contrarian lens): a different mu test (log-sum threshold instead of a product check), different segment
  and block sizes, its own combiner, run fresh from k = 1 to 3.30125e11. It agrees with run 1 at all 660 common
  grid points and gives the same first hit. A sympy trial-factorisation spot checker agreed on 9 random windows.
- What failed or was limited: the first nightly session ran out of time before run 2 finished; it was rerun in
  full from k = 1 in a follow-up session rather than resumed. 2^19 is not reached by 3.4e11 (not claimed).
- Panel: three fresh subagent contexts saw only the claim folder. REPRODUCE wrote its own sieve and ran it in full
  from k = 1; NOVELTY found no publication of the value; CRITERION judged p1 met for a(18) only.
