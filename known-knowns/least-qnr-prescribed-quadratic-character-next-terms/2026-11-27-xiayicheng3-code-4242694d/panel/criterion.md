# CRITERION skeptic: A002224(42) = 6072205049848081

context: subagent (Claude Code Agent tool, fresh context, saw only claim/)

Inputs read: claim/CLAIM.md, claim/REPRODUCE.md, claim/result/*, claim/code/*, claim/data/*. Nothing else under runs/.
My own scripts and outputs are in panel_work/criterion/ (mycheck.py, calib.py, competitors.py, small/myenum.py,
small/wheel_rescheck.c, small/*.txt). I made no network calls.

## Verdict in brief

The claim is for the full success criterion, for exactly one named cell (A002224, n = 42). It is not a partial win.
Clause (1), the property check, is met with margin by my own independent script, and primality is proven without conditions.
Clause (2), minimality, is met as far as a claim package can meet it: a complete search from 1 (not a window) that
reproduces the known terms, and I found no gap in it on review. Clause (2) also requires a skeptic re-run with a separately
written enumerator. The package cannot supply that; the REPRODUCE skeptic must. My pass depends on that re-run
(condition C1 below).

## 1. Is n = 42 the named next unknown index?

- The criterion names "A002224 (n = 42)" explicitly as one of the six admissible cells.
- claim/data/b002224.txt has 41 lines, n = 1..41, contiguous, with no comment lines. The last line is `41 178936222537081`.
  Its sha256 (70fa340e...) and the sha256 of A002224.html (e8763c3a...) match the fetch table in CLAIM.md.
- The saved OEIS page shows data to n = 35 and links "Table of n, a(n) for n = 1..41" (M. Hortmann). It has no comment,
  extension or bound for a(42). So n = 42 is the next unknown index and is absent. Direction: 42 is strictly beyond the b-file.
- Hidden quantifier: the criterion says "re-fetched ... immediately before claiming and must still be absent". The fetch
  is dated 2026-11-27T16:27:36Z, at the start of this run. That satisfies the clause if the claim is recorded in this run.
  If it is recorded materially later, the b-file must be fetched again (condition C2). The page carries the keyword
  "changed", meaning a recent edit, so this check is not a formality.

## 2. Property, clause (1)

My script panel_work/criterion/mycheck.py is written from the OEIS definition only and shares no code with the author.
It uses its own sieve, its own Jacobi symbol, Euler's criterion, Miller-Rabin and a Lucas certificate. For
q = 6072205049848081 it gives:
- q mod 8 = 1.
- First n primes with p_1 = 2: p_42 = 181, so there is no off-by-one. All 42 of 2..181 are QRs by Euler's criterion
  (pow(p,(q-1)/2,q) = 1), and independently by the Jacobi symbol.
- The least QNR is 197 = p_45, so q has the first 44 primes as QRs. A002224 prescribes only that the first n primes
  are QRs and puts no condition on p_{n+1}. "Exactly the prescribed character" is therefore met without stretching the
  definition. This differs from A000229, which prescribes the exact least QNR.
- Primality: q < 3.317e24, so the criterion asks for no Pocklington/ECPP certificate. Deterministic Miller-Rabin with
  the first 13 prime bases (Sorenson-Webster bound 3.317e24) is a deterministic proof at this size, and q < 2^64 lies in
  the range where BPSW is verified to have no counterexample. My answer to the question is yes: deterministic MR or BPSW
  is acceptable here. The question is moot anyway, because I also gave two unconditional proofs:
  - A Lucas (n-1) certificate. q-1 = 2^4 * 3^2 * 5 * 11 * 13 * 58976350523, with every factor proven prime by
    trial division. Witness a = 223 gives a^(q-1) = 1 and a^((q-1)/r) != 1 for each prime factor r.
  - Trial division by all 4,555,398 primes up to isqrt(q)+1 = 77924355 found no divisor.
- Control: 178936222537081 = A002224(41) is prime and 1 mod 8, and its least QNR is 181. It has the first 41 primes
  as QRs but not the first 42. This agrees with the b-file and with a(42) > a(41).
- The author's checker (claim/code/check_a002224.py) prints the same results. It is not independent, so I do not count it.

Clause (1) is met.

## 3. Minimality, clause (2)

What the criterion requires: "a complete search shows that no smaller integer has the property", starting from 1
(the bracket shortcut applies only to A000229(39)), plus a skeptic re-run with a separately written enumerator that finds
nothing below q.

What the package provides, from my review of claim/code/wheel.c and claim/code/analyze.py:
- Reduction. For a prime q = 1 mod 8: (2/q) = 1, and quadratic reciprocity gives (p/q) = (q/p) for odd p. Every prime
  with the A002224(42) property is therefore a nonzero QR mod every odd prime up to 181. The wheel keeps every q = 1 mod 8
  that is a nonzero QR mod all odd primes up to 113 (p_30 = 113). That is a necessary condition for n >= 30, so no
  qualifying prime is dropped. The base-2 Fermat filter never drops a prime.
- The final property is not taken from the sieve. analyze.py recomputes it with Euler's criterion from the definition,
  including p = 2, and requires deterministic MR primality, so the reciprocity step can only cost completeness, never
  admit false positives.
- Completeness of the wheel. M = 8*3*5*...*31 = 802241960520. I compiled a copy of wheel.c whose sampled sanity check
  (every 9973rd residue) is replaced by a check of all residues plus a sort. All 29,937,600 residues are distinct, lie
  below M, are 1 mod 8 and are QRs mod 3..31. The count equals prod (p-1)/2, so the residue set is exactly complete.
  The periods k = 0..K-1 with K = X/M + 1 cover [0, K*M), which contains [1, X]. The search is from 1, not a window.
- I found no defect in the table bounds (index < 2p <= 94 < 96), the 128-bit arithmetic in the Fermat test, the q > X
  skip, the uint64 range, or the q <= X filter in analyze.py.
- Search range: the JSON records [1, 10^16] and REPRODUCE.md uses X = q. Both cover [1, q].
- Calibration from 1: the author's output reports A002224(30..41) all MATCH, including A002224(38) = 112434732901969.
  I did not rerun the 10^16 search. I ran the author's code at X = 3e13, 3e14 and 1e15. Each run printed CALIBRATION PASS:
  n = 30..35 matched at 3e13, and a(40) = a(41) = 178936222537081 were found at 3e14 and 1e15.
- Separately written sub-range cross-check. panel_work/criterion/small/myenum.py uses numpy with a different CRT split
  (M = 8*3*...*29), no byte tables and no Fermat filter. It finds exactly the same 142 primes in [1, 3e13] as the
  author's wheel (identical sets) and reproduces a(30..35). The wheel's three non-prime survivors are 1 and
  1093^2 = 1194649 and 3511^2 = 12327121. The last two are base-2 Fermat pseudoprimes (Wieferich squares), which is
  expected behaviour.
- Consistency of the author's untrusted count (95181 prime survivors up to 1e16). Prime survivors divided by the naive
  li(x)/4 * 2^-29 gives 0.30 at 3e13, 0.49 at 3e14 and 0.58 at 1e15 (all measured by me), and 0.73 at 1e16 (author).
  The trend is smooth, so I see no sign of a truncated or padded run.

What is missing from the package: the skeptic re-run. My sub-range check covers 0.5% of [1, q) with my own code and
about 16% with the author's code, so it does not substitute for the re-run. The criterion's parenthetical reads
"a different modulus split, or a plain sieve on a sub-range". I read it as follows. A plain sieve on a sub-range can serve
only as an extra spot check. Clause (2) requires the skeptic to "re-run that search", and the verification method says
"from scratch", so the minimality claim is confirmed only when the separately written enumerator covers all of [1, q).

Cross-check list in the verification method: A000229 a(30..38) and A002223(38) are terms of other cells, in other residue
classes; A002223 is the 7 mod 8 analogue implied by the A000229(39) bracket. A 1 mod 8 enumerator cannot produce them.
The success criterion ties the A002223(38)/A002224(38) reproduction to the A000229 bracket shortcut only. For this cell,
the relevant check is the reproduction of A002224 terms from 1, which is present, and I do not treat the other items as
blockers.

Null model: I agree that no statistical null test is needed. A deterministic exhaustive search with a complete residue
set either covers the range or it does not. As a plausibility null I compared the naive Chebotarev count expected below
a(n), li(a(n))/4 * 2^-(n-1), across the b-file. Verified terms range from 1.3 to 22.2 (n = 23: 22.2; n = 36: 20.9).
The claimed a(42) gives 19.6, inside the empirical spread, so it is not an outlier. I also tried to falsify the claim
with pseudosquare values I recall from memory, outside the package and unverified, and used only as candidate
counterexamples. 696161110209049 (QRs through 191) and 2854909648103881 (QRs through 193) are both below q, nonsquare
and 1 mod 8, but composite, so neither refutes the claim. The fact that q has QRs through 193 and lies above the
second value fits pseudosquare monotonicity.

## 4. One cell, no stretched definitions, no subsumption

- One cell: the claim is A002224(42) only. The same evidence also implies a(43) = a(44) = q, because q has the first 44
  primes as QRs and a(n) is nondecreasing. The author's analysis prints those lines, but they are not the named
  "next unknown index", the claim does not claim them, and they must not be booked as extra cells.
- Definition: prime (proven), 1 mod 8, the first 42 primes counted from p_1 = 2 (2..181), nonzero QRs. Composite
  numbers with the same character, such as the two pseudosquares above, are excluded by the definition and do not
  count against minimality. That reading belongs to A002224, not to the nonsquare sequences A001992 or A002189.
- Subsumption: nothing in the package already gives a(42) or a bound that settles it. Partial win p1's A002224 branch
  ("exceeds 10^16") is contradicted by the claim, not met, and p2 is not claimed. This is a full-success claim and
  would subsume p2-type evidence, not the reverse.

## Conditions on which this pass depends

- C1 (required by clause (2)): the REPRODUCE skeptic re-runs the search from 1 with a separately written enumerator
  (a different CRT split or a different method) covering all of [1, 6072205049848081]. It must reproduce the A002224
  b-file terms from 1, at least A002224(38) = 112434732901969 and preferably n = 30..41. It must find
  6072205049848081, and it must find no prime q' = 1 mod 8 with q' < 6072205049848081 having the first 42 primes as QRs.
  If that re-run is missing, partial (sub-range only), or finds anything below q, the result does not meet the
  criterion and the panel verdict must be false regardless of this file.
- C2 (procedural): A002224 n = 42 must still be absent from the live b-file at the time the claim is recorded. The
  recorded fetch time is 2026-11-27T16:27:36Z.

confirmed_scope: 6072205049848081 is a prime congruent to 1 mod 8 for which each of the first 42 primes (2 through 181) is a quadratic residue, and no smaller prime congruent to 1 mod 8 has that property, so A002224(42) = 6072205049848081, an index absent from the OEIS b-file fetched on 2026-11-27 (which ends at n = 41).

pass: true
