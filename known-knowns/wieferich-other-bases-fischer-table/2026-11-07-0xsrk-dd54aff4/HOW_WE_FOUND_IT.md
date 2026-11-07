# How we found it (contributor text, unverified)

**The brief.** The bank's target asks for new Wieferich pairs (b, p), meaning b^(p−1) ≡ 1 (mod p²). Richard Fischer's
tables cover bases up to 10125, searched to 4.8·10^12. A full win needs p beyond that limit. Partial win p1 asks
instead for a pair with a base strictly between 10125 and 65537 and p > 10^12. No public table covers that range of
bases.

**What did not work.** Our first run (one hour, 30 workers) chased the full win. It swept every prime in
[4.8·10^12, 4.8147·10^12) for the 2360 non-perfect-power 70-smooth bases ≤ 10125 and found nothing. The expected
yield was 0.25 pairs. Above the table limit, finds are rare per CPU-hour.

**What worked.** Treating the criterion itself as data. For one prime p, the chance that some base qualifies is
about (number of bases)/p. So the cell with the most finds per CPU-hour is the lowest eligible p, just above 10^12,
taken over the largest eligible base set. Fermat quotients are additive: q_p(ab) ≡ q_p(a) + q_p(b) (mod p). For each
prime the sweep computes the quotients of the 19 primes ≤ 70 once, at a cost of about 19 modular exponentiations. It
then gets every 70-smooth base in 10126..65536 at once (6852 bases, perfect powers removed) as an integer
matrix–vector product in exact floating point. Survivors of that screen are re-checked with an exact pow(b, p−1, p²).

**The find.** The plan was frozen before any compute (how-we-built-it/PREREG.md). Before the attack, the pipeline was
checked against brute force on the same base set in three windows below 10^12 (170, 122 and 30 pairs, identical
sets). The sweep started at exactly 10^12 with 15 workers at idle priority. About eight minutes in, the block
[1000740000000, 1000760000000) returned the screen candidate (24766, 1000747824697), and the exact check confirmed it.
24766 = 2·7·29·61, and none of the four quotients is zero on its own; their sum is exactly p. Three independent
skeptics, each seeing only the claim, then reproduced it, checked novelty and judged the criterion (panel/).
