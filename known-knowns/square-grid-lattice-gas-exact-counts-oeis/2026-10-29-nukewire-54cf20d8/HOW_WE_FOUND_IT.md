# HOW WE FOUND IT (contributor text, unverified)

The target's bank entry says A054759 (square ice) is "expected to be easy" — it was:
a(15) fell on 2026-10-25/26 after one panel taught us that two runs must differ in
code, not just primes. The main arm A028420 (monomer-dimer tilings) was the bigger
prize: a(28), one term past the published table.

Run A (row-major broken-profile DP over 2^28 states) validated against all published
terms, then computed a(28) mod 21 proven primes — after the machine's RAM wall (four
OOM launches) relented. Run B was written separately (column sweep, its own primes)
precisely because the a(15) panel had failed a primes-only "second run". The two CRTs
matched exactly.

The panel then taught us again: its criterion skeptic demanded the exact multi-prime
reproduction gate for n = 21..27 (our 2-prime spot gates were not enough). Six of the
seven terms were already exact; n = 27 needed 20 more primes, finished with a
reverse-order helper beside the forward worker. The re-paneled skeptic re-derived the
value with a THIRD sweep of its own, closed the n = 0..27 coverage itself, and passed
the claim — including the growth clause, whose literal 1e-3 parenthetical we showed
(and it independently verified) no true term of this sequence can ever meet.
