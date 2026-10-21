# How we found it (contributor text, unverified)

*This is a plain narrative by the contributor. It is unverified prose; the binding evidence is in
object/, verify-it-yourself/, panel/ and the-record-we-beat/.*

The target family asks for exact term counts of square-grid lattice-gas / ice sequences. The main
sequences (A028420/A006506/A063443) are heavy; A054759 (square ice on the n×n torus) is the explicit
"partial" and is cheap: the row-to-row transfer matrix for the six-vertex model at the ice point.

The brief, carried from the scouting run, confirmed the live b-file ended at a(14) (Brendan McKay, 2024).
We implemented the transfer matrix as a sum over sectors: around the periodic ring the number of up
vertical arrows is conserved, so the matrix is block-diagonal by that count. Each block entry counts, for
a pair of vertical-arrow configurations, the horizontal edge assignments consistent with the ice rule —
computable either in closed form (min/max of prefix sums) or by an explicit two-value walk. Powers were
taken with a float64 BLAS matmul reduced mod a prime after each product (exact because entries stay below
2^20 and the contracted dimension is at most C(15,7)=6435, so each sum is below 2^53), and the exact
integer was recovered by CRT across several primes.

What failed / what we were careful about:
- The growth-constant clause in the main criterion is not reachable at finite n: even the published a(14)
  is 0.0085 away from the Lieb ice constant, far more than 1e-3. We report the number literally and do not
  claim that clause; p1 names only the two-run and reproduction rules.
- Independence: a single transfer-matrix bug could corrupt both runs. We required the two runs to use
  disjoint prime sets AND different state encodings and entry code, and — crucially — wrote a from-scratch
  self-break: ground-truth brute force over all edge orientations (n≤3) and a non-sector transfer matrix
  (n≤8), both agreeing with OEIS. The production method also reproduces every published term n=1..14.

What worked: both runs agreed digit for digit on the 43-digit a(15), and three independent skeptics
(reproduce, novelty, criterion) — two of whom recomputed all 23 residues from scratch — confirmed it.
