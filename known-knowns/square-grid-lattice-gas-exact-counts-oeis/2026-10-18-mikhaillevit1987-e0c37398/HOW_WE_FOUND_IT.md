# How we found it (contributor text, unverified)

The bank target square-grid-lattice-gas-exact-counts-oeis lists exact OEIS terms as partial win p1. A054759 (square
ice on the n x n torus) ended at a(14). We wrote a cell-by-cell transfer-matrix sweep in Rust that counts
trace(T^n) modulo several 62-bit primes, using orbit representatives of the starting row, and ran it twice with
different sweeps, symmetry groups and disjoint prime sets. Both runs reproduce a(1..14) and agree on n = 15, 16, 17.
A second, independent method (flux-sector matrices in numpy) reproduced a(1..13) and a(15). The panel's REPRODUCE
skeptic then wrote its own code and recomputed a(15) and a(16).

What did not work: the claim failed CRITERION because p1 asks for the next unknown term, which is a(15), already
claimed in an open pull request. The OEIS extension a(15..17) is being proposed to OEIS separately by the contributor.
