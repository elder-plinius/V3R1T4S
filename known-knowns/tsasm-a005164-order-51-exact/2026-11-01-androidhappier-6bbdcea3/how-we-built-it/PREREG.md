# PREREG: tsasm-a005164-order-51-exact

frozen_at_utc: 2026-11-01T02:09:55Z

Disclosure note: before freezing, a 30-line Python prototype of the reduction below (in /tmp, not scored) printed
a(0..11) = 1,1,1,2,4,13,46,248,1516,13654,142873,2156888, equal to OEIS. Nothing beyond a(11) was computed before
this file was written.

## Criterion (verbatim, bank)
The exact integer A005164(25) (TSASMs of order 51), obtained by an exact enumeration (a transfer matrix, a DP or an
equivalent count of the matrices themselves), not by evaluating the Hagendorf-Lienardy conjectured formula. The same
program must reproduce a(0)..a(13) exactly. It must also either reproduce a(14)..a(24) or report each disagreement,
and a second independent program must confirm every disagreement. Two independent runs must agree on a(25), using
different prime sets or exact big integers and a different sweep order or state encoding. It counts only if a(25) is
not in the DATA or a b-file of A005164 when re-fetched immediately before claiming.

Partial p1 (verbatim): An exact enumeration (not the conjectured formula) that reproduces every term a(14)..a(24) of
A005164, with code and per-term residues published, so the existing terms no longer depend on a conjecture.

## Exact statistic / checker
- Program A (row-major transfer matrix on the fundamental-domain quadrant, C, counts modulo primes
  P_A = {2305843009213693951 (2^61-1), 4611686018427387847, 4611686018427387817}... final list printed by the program;
  CRT reconstruction to an integer with the symmetric range check below).
- Program B (column-major sweep of the upper triangle, a different state encoding: growing state of finished-row
  prefix bits plus the running column sum; exact integers (unsigned __int128 in C, or Python int for small n) and/or
  a disjoint prime set P_B).
- Program C (brute force from the ASM definition: build full (2n+1)x(2n+1) matrices and test ASM + all 8 symmetries)
  for a(0)..a(7) at least, to validate A and B on small orders.
- A term is "computed" only if A and B give the identical integer. For residue-based results, the CRT modulus must
  exceed 2*10^3 * (a(n-1) * 1000) (i.e. a bound >> any plausible value, ratio of consecutive terms < 1000 at these n),
  and an extra prime not used in the reconstruction must agree (check prime).
- Pass for the full win: A(25) == B(25) exactly; A and B both reproduce a(0)..a(13) exactly; a(14)..a(24) each either
  reproduced or listed as a disagreement confirmed by the other program; a(25) absent from OEIS DATA and b-file in a
  re-fetch immediately before claiming.
- Pass for p1: A and B both reproduce a(14)..a(24) exactly; per-term residues published.
- Correctness tests: checker C must accept a known TSASM (the order-5 TSASM with centre cross) and reject a known
  ASM that is not totally symmetric (identity of order 3) and a non-ASM (all-ones row).

null_test: not needed because the result is an exact integer count produced by two independent deterministic
programs and checked against 25 published terms and a brute-force enumerator; there is no search, score or
"beats chance" statistic.

Baseline (step 3c): not applicable (not an empirical benchmark).
