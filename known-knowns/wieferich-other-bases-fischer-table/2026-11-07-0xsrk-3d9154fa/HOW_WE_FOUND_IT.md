# How we found it (contributor text, unverified)

**The brief.** The bank's target asks for new Wieferich pairs (b, p), meaning b^(p−1) ≡ 1 (mod p²). Richard Fischer's
tables cover bases up to 10125, searched to 4.8·10^12. Partial win p1 asks instead for a pair with a base strictly
between 10125 and 65537 and p > 10^12. No public table covers that range of bases.

**The campaign.** Several runs of the same campaign swept every prime in [10^12, 1.03474·10^12) for the 6852
non-perfect-power 70-smooth bases in 10126..65536. They found seven pairs, against about 8.5 expected. Four are
submitted separately. This package holds the fifth.

**Method.** Fermat quotients are additive: q_p(ab) ≡ q_p(a) + q_p(b) (mod p).
- For each prime p, the sweep computes the quotients of the 19 primes ≤ 70 once, which costs about 19 modular
  exponentiations.
- It then screens every 70-smooth base in 10126..65536 at once. This pair's sweep used the exact meet-in-the-middle
  screen:
  - each base is split as b = a·c, with a built from {2, 3, 5, 7} and c from the primes 11..67;
  - b is a candidate exactly when q_p(a) ≡ −q_p(c) (mod p), which one sort of exact integer residues per prime finds.
- Every candidate is re-checked with an exact pow(b, p−1, p²).

**The find.**
- The block [1024040000000, 1024060000000) returned the single candidate (56350, 1024048960667), and the exact check
  confirmed it. It was one of three exact pairs of that sweep. The run's frozen plan (how-we-built-it/PREREG.md)
  allows one claim per run, so each pair waits for its own review.
- This package's run carried it over:
  - the plan was frozen before the claim folder was built;
  - a new break attempt was made;
  - three isolated skeptics saw only the claim (panel/).
- 56350 = 2·5²·7²·23. None of the four prime quotients is zero on its own, but
  q(2) + 2·q(5) + 2·q(7) + q(23) = 1024048960667 = p exactly (values in panel/novelty.md, section 4).
- 56350 is the only base in 2..70000 for which this p is a Wieferich prime.
