# Criterion skeptic: p_c^site(Z^3) <= 4427/10000

context: subagent (fresh, claim/ copy only)

Criterion (verbatim, CLAIM.md): "A rigorous proof that p_c^site(Z^3) <= p* for an explicit rational p* < 1/2, strictly
below every explicit rigorous upper bound published at verification time, whose finite part is an exhaustive
computation in exact rational (or verified interval) arithmetic released with code a stranger can rerun." No partial
wins are enumerated, so the claim has to meet all of it.

I checked the package against MANIFEST.sha256 first: the code files match.

## 1. The argument (PROOF.md), read as a referee

- Growth process (section 1). Each vertex is selected at most once: once a block has been selected, it has no
  unassigned neighbour left. So when block b2 is selected it is a leaf of the exploration tree. The only revealed
  information is eta on tree edges, and each of those is a function of the two endpoint block states. So the history
  is a function of the assigned blocks' states only. The Claim (an xi = 1 block's G lies in the cluster of 0) holds
  by induction on the parent chain. It uses only that G is connected and that B_0 is all open.
- Coupling lemma (section 2). Conditioning on R = {eps(0) all open} is legitimate. P(R) = p^27 > 0, R involves only
  eps(0), and the other blocks stay i.i.d. The last step, P(survival | R) <= theta(p)/p^27, is just division by P(R).
  - The per-step Strassen coupling and the hybrid-field argument do give an i.i.d. Bernoulli(q) field zeta.
  - The die-out/survival split is correct. At die-out, every neighbour of an xi = 1 vertex has received a value with
    zeta <= xi, even when it came through a different parent. So the zeta-cluster of 0 lies inside the finite set
    {xi = 1}.
  - Under survival, infinitely many distinct selected blocks have nonempty G inside C(0).
- Tree-information lemma (section 3). This holds "for every history". Nothing in it uses planarity; it needs only
  three facts:
  1. eta depends on the pair of block states.
  2. The revealed edges form a tree.
  3. Children are fresh blocks.

  Message passing gives w(beta) ∝ pi(beta) sum_gamma 1[eta(gamma, beta) = 1] mu_c(gamma) because b2 is a leaf. Grouping
  by U = mirror of T_F(gamma) writes w as a convex combination of the w_U over nonempty U. For a child of the root,
  mu_c is a point mass and U is the full face, which is one of the 511 U.
- Reduction (section 4). Domination of Bernoulli(q)^k is a family of linear inequalities over up-sets, so it survives
  mixtures. Projecting onto a subset of children maps up-sets to cylinder up-sets and Bernoulli(q)^5 to
  Bernoulli(q)^k. That covers blocks with fewer than 5 children.
  - The root step (6 independent children, r_f(full face) >= q) is checked separately.
  - Every non-root selected block has a parent, so it has at most 5 children.
  - Checks needed: 6 root inequalities, plus 6 entry faces x 511 nonempty U = 3066 laws, each against every nontrivial
    up-set of {0,1}^5. The reduction is complete.
- Strassen (finite poset, up-sets) is used correctly. Child labels do not matter: Q depends only on the number of 1s,
  and every up-set is checked.
- Chain (section 5, result/bound.json, outputs/).
  - Each q_j equals p_{j-1}: 501/1000 -> 2317/5000 -> 9/20 -> 1781/4000 -> 1109/2500 -> 443/1000 -> 1107/2500 ->
    4427/10000.
  - Each link gives theta(p_j) >= p_j^27 theta(q_j) > 0. That is exactly the input the next link needs.
  - Links 4-7 come from a run that started elsewhere (at q = 1/2). A certificate depends only on (p_j, q_j), so it is
    valid to splice them after link 3 of outputs/chainB_*.
  - The base needs theta(501/1000) > 0. That follows from p_c <= 1/2 < 0.501, plus the definition of p_c and the
    monotonicity of theta.
- External inputs: Campanino and Russo 1985 (p_c^site(Z^3) <= 1/2; only the non-strict form is used) and Strassen 1965.
  The van den Berg-Ermakov framework is not used as a black box: both of its lemmas are proved in the text. The
  citations are correctly attributed. The claimants did not open the Campanino-Russo paper itself (they say so in
  table/literature_record.md); its content is attested by Grimmett's survey and by the Gomes-Pereira-Sanchis table.
  It is a well-known theorem.

I found no gap in the argument.

## 2. The finite part (code/)

- Exhaustive. code/cert/main.go loops e = w, w+W, ... < 2^27 over W workers, so every state is visited, in both
  counts mode and laws mode. Nothing is sampled. The face-local site order is the same on opposite faces, so the
  mirror map is the identity on trace bits. OPP in code/cert.py pairs each face with its opposite.
- Exact and verified arithmetic.
  - r_f and pw[k] are exact Fractions built from the integer counts.
  - code/cert.py encloses each one by floats lo <= x <= hi, using an exact Fraction comparison plus nextafter.
  - The Go engine widens every product and every sum by one ulp, outward (down/up). All quantities are nonnegative, no
    a*b+c pattern exists that could be fused, and nothing comes near underflow. So [lo, hi] encloses the true sums.
  - code/cert.py turns every float into an exact integer (scale 2^1100). It bounds P_U(A) from below by
    floor(num_lo 2^56 / Z_hi) and compares the result with ceil(Q(A) 2^56) in exact int64. No overflow is possible:
    each term is <= 2^56 and there are at most 31 terms.
  - The root check r_f(full) >= q is an exact Fraction comparison.
- Up-sets: code/upsets.py gives 7581 distinct up-sets of {0,1}^5, the Dedekind number M(5). I checked that each one
  is closed upward, and that the recursion gives 168 for m = 4, matching a brute-force count. 7581 - 2 = 7579.
- Code tests I ran (small blocks only; I did not run 3x3x3). I wrote my own exact checker from PROOF.md alone: its
  own BFS, coordinate faces and mirror, up-sets enumerated through antichains, all in Fractions. I compared it with the
  claim's Go engine plus code/cert.py:
  - 2x2x2 block, minSize 2, at (p, q) = (3/5, 11/20), (11/20, 3/5) and (7/10, 7/10).
  - 2x2x3 and 3x2x2 blocks, minSize 3, at (31/50, 63/100).

  In every case PASS/FAIL agreed and the worst margins agreed to 7 significant figures. All 3072 (2x2x2) and 9216
  (2x2x3, 3x2x2) Go intervals enclosed my exact values.
- A Monte Carlo estimate (2e5 samples) of P(G touches a given face) for the 3x3x3 block at p = 0.4427 gave 0.707-0.709
  across the six faces. The logged root minimum is 0.708206, so the two agree.
- Rerunnable: REPRODUCE.md gives the build and chain commands. The runtime is modest (minutes, about 2 GB). Non-blocking
  issues:
  1. REPRODUCE.md says "Go >= 1.21" but code/cert/go.mod declares `go 1.26.4`. An older toolchain will download
     1.26.4, or refuse to build if GOTOOLCHAIN=local. The source itself needs nothing newer than 1.21.
  2. code/chain.py hardcodes the `.exe` path and the `3 3 3 6 6` arguments (documented).
  3. code/chain.py always prints "given Campanino-Russo's p_c < 1/2 for link 1", even when the run starts at
     q1 = 501/1000. This is cosmetic; PROOF.md states the base correctly.
  4. The counts file ships only as a sha256 (outputs/counts_b333_s6.sha256); a rerun regenerates it.

## 3. "Explicit rational p* < 1/2, strictly below every explicit published bound"

- p* = 4427/10000 is an explicit rational, and it is below 1/2.
- The claim's record (table/literature_record.md, CLAIM.md) names the best published bound as Campanino-Russo's
  p_c < 1/2, tabulated as 0.5000 by Gomes-Pereira-Sanchis. It is backed by Grimmett's 2016 remark. The record says
  plainly what is not a bound: a Monte Carlo confidence interval, and the bond-percolation bound, which is a different
  model.
- The comparison is stated honestly, but the record rests on two secondary sources, not a systematic search. The
  hidden quantifier "every ... published" therefore rests on the novelty skeptic's literature check, which is outside
  this role.

## 4. Null models

This is a deterministic certificate, so no statistical null applies. The relevant sanity null: a sound method can
never certify a value below the true p_c (about 0.3116 by Monte Carlo). 0.4427 is above it. On small blocks the method
fails at p = 11/20 < q = 3/5 and passes only around p >= 0.6-0.7, which fits the expectation that smaller blocks give
weaker bounds.

## 5. Not checked here

- The full 3x3x3 runs. I relied on the logged outputs; another skeptic reruns them.
- The completeness of the literature.

confirmed_scope: Conditional on the released code reproducing the logged 3x3x3 certificates (outputs/chainB_log.txt links 1-3 and outputs/chainA_log.txt links 4-7), PROOF.md together with those exhaustive outward-rounded and exact-integer checks rigorously proves p_c^site(Z^3) <= 4427/10000 from Campanino-Russo's p_c^site(Z^3) <= 1/2, a bound strictly below the best published bound named in the claim's record (Campanino-Russo's non-explicit p_c < 1/2, tabulated as 0.5000).
pass: true
