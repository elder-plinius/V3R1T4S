# How we found it (contributor text, unverified)

**The brief.** The bank's target asks for new Wieferich pairs (b, p), meaning b^(p−1) ≡ 1 (mod p²). Richard Fischer's
tables cover bases up to 10125, searched to 4.8·10^12. Partial win p1 asks instead for a pair with a base strictly
between 10125 and 65537 and p > 10^12. No public table covers that range of bases.

**The campaign.** Several runs of the same campaign swept every prime in [10^12, 1.01894·10^12) for the 6852
non-perfect-power 70-smooth bases in 10126..65536. They found four pairs, against about 4.7 expected. Three are
submitted separately. This package holds the fourth.

**Method.** Fermat quotients are additive: q_p(ab) ≡ q_p(a) + q_p(b) (mod p). For each prime p the sweep computes the
quotients of the 19 primes ≤ 70 once, about 19 modular exponentiations. It then gets every 70-smooth base in
10126..65536 at once, as an integer matrix–vector product in exact floating point, and the screen's tolerance is
proven larger than its rounding error for p < 2^43. Every survivor is re-checked with an exact pow(b, p−1, p²).

**The find.**
- The block [1017260000000, 1017280000000) returned the single screen candidate (28860, 1017279755641), and the exact
  check confirmed it. It was the second exact pair of that run. The run's frozen plan (how-we-built-it/PREREG.md)
  allows one claim per run, so the pair waited for its own review.
- The next run carried it over:
  - an independent break attempt by a second agent;
  - a real-size control in which a newer exact screen recovered the same pair and the same q-matrix hash from the
    same block;
  - three independent skeptics who saw only the claim (panel/).
- 28860 = 2²·3·5·13·37. None of the five prime quotients is zero on its own, but
  2·q(2) + q(3) + q(5) + q(13) + q(37) = 3051839266923 = 3p exactly.
- 28860 is the only base in 2..65536 for which this p is a Wieferich prime.
