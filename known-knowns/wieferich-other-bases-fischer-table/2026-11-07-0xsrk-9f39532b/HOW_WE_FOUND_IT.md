# How we found it (contributor text, unverified)

**The brief.** The bank's target asks for new Wieferich pairs (b, p), meaning b^(p−1) ≡ 1 (mod p²). Richard Fischer's
tables cover bases up to 10125, searched to 4.8·10^12. Partial win p1 asks instead for a pair with a base strictly
between 10125 and 65537 and p > 10^12. No public table covers that range of bases.

**What came before.** Earlier runs of the same campaign swept every prime in [10^12, 1.0063·10^12) for the 6852
non-perfect-power 70-smooth bases in 10126..65536. They found one pair, (24766, 1000747824697), submitted separately,
and then nothing in the next 2.1·10^9 (0.52 pairs expected). The full-win cell above 4.8·10^12 yields about eight
times fewer pairs per CPU-hour, so this run put every worker on the p1 cell, starting at its frontier.

**Method.** Fermat quotients are additive: q_p(ab) ≡ q_p(a) + q_p(b) (mod p). For each prime p the sweep computes
the quotients of the 19 primes ≤ 70 once, about 19 modular exponentiations. It then gets every 70-smooth base in
10126..65536 at once, as an integer matrix–vector product in exact floating point; the screen's tolerance is proven
larger than its rounding error for p < 2^43. Every survivor is re-checked with an exact pow(b, p−1, p²).

**The find.** The plan was frozen before any compute (how-we-built-it/PREREG.md). The pipeline was first re-checked
against brute force on the same base set (p1_known_positives_output.txt). The sweep resumed at 1006300000000 with
30 workers at idle priority. The block [1011540000000, 1011560000000) returned the single screen candidate
(28910, 1011548897263), and the exact check confirmed it.
- 28910 = 2·5·7²·59. None of the four prime quotients is zero on its own, but
  q(2) + q(5) + 2·q(7) + q(59) = 2023097794526 = 2p exactly.
- Over the 195371719 primes swept in this run, 1.33 pairs were expected and one was found.
- Three independent skeptics, each seeing only the claim, then reproduced it, checked novelty and judged the
  criterion (panel/).
