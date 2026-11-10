# How we found it (contributor text, unverified)

**The brief.** The bank's target asks for new Wieferich pairs (b, p), meaning b^(p−1) ≡ 1 (mod p²), for bases
3..10125, with p above the searched limit that Richard Fischer's tables state. For bases 1053..10125 that limit is
4.8·10^12.

**The campaign.** Several runs of the same campaign swept every prime in [4.8·10^12, 4.8494·10^12) for the 2360
non-perfect-power 70-smooth bases in 1053..10125. Together they found one pair, this one, against about 0.83
expected.

**Method.** Fermat quotients are additive: q_p(ab) ≡ q_p(a) + q_p(b) (mod p).
- For each prime p, the sweep computes the quotients of the 19 primes ≤ 70 once, which costs about 19 modular
  exponentiations.
- It then screens every 70-smooth base in 1053..10125 at once with an exact meet-in-the-middle screen:
  - each base is split as b = a·c, with a built from {2, 3, 5, 7} and c from the primes 11..67;
  - b is a candidate exactly when q_p(a) ≡ −q_p(c) (mod p), which one sort of exact integer residues per prime finds.
- Every candidate is re-checked with an exact pow(b, p−1, p²).
- Before this base set was swept with the new screen, the screen was checked against the older float screen. It
  matched on 40 of Fischer's own table pairs and on one full block. A random block of that sweep was later recomputed
  by an independent path, and the record matched.

**The find.**
- The block [4848800000000, 4848820000000) returned the single candidate (5481, 4848813530161), and the exact check
  confirmed it.
- The run's frozen plan (how-we-built-it/PREREG.md) allows one claim per run and already had one, so the pair waited
  for its own review.
- This package's run:
  - re-fetched every table immediately before the claim;
  - froze its plan before building the claim folder;
  - repeated the break attempt;
  - had three isolated skeptics, who saw only the claim (panel/).
- 5481 = 3³·7·29. None of the three prime quotients is zero on its own, but
  3·q(3) + q(7) + q(29) = 9697627060322 = 2p exactly (values in panel/novelty.md, section 6).
- 5481 is the only base in 2..10125 for which this p is a Wieferich prime.
