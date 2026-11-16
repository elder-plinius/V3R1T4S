context: Claude Code subagent, fresh context [Sonnet 5.5]

# REPRODUCE skeptic report

Claim: object/certificate_qrac4.json (sha256 8ca3d435...7788, confirmed by my own hash) plus object/proof_qrac4.md prove p(4) <= 0.741481799559635048 <= 0.741482 for the 4-to-1 single-qubit QRAC with shared randomness.

Definition checked against (criterion, verbatim): "a rigorous, independently re-checkable proof that the optimal n-to-1 QRAC with SR for n = 4 has p <= 0.741481 + 1e-6, i.e. that max over unit vectors v_1..v_4 in R^3 of S/(4*2^5) + 1/2 does not exceed that value", with S = sum over x in {+-1}^4 of ||sum_i x_i v_i||, and the verification method "boxes cover the whole domain (v_1 fixed to (0,0,1) by symmetry, remaining 2(n-1) angles) and each box's rigorous upper bound is below the claimed value".

## 1. Re-derivation of the reduction (my own, then compared with proof_qrac4.md)

1. Shared randomness. A shared-randomness code is a probability mixture of deterministic-seed codes, so its worst-case success is at most the best average over inputs and indices of one seed (the minimax step). It is also at least that value, so the two are equal. The package cites Lemma 2 / Theorem 3 of arXiv:0810.2937 for this. I did not re-prove their lemma. The task statement itself gives the formula p = 1/2 + S/(n 2^(n+1)), so this step is taken from the target, not checked by me. Valid as cited.
2. Bob's measurement. A general two-outcome POVM element is E = ((1+c)/2) I + (v.sigma)/2 with |c|+|v| <= 1. For input bit x_i the success term is (1 + x_i c_i + x_i r.v_i)/2. The c_i terms average to zero over uniform x (they do not depend on the state), so only v_i in the unit ball matters. Helstrom (best state aligned with sum x_i v_i) gives 1/2 + ||sum x_i v_i||/(2n). Averaging over 2^n strings gives the stated formula. Valid. The package's version (mixing with trivial outcomes only shrinks the norm) reaches the same place, a little tersely.
3. Ball to sphere. The norm is convex, so P is convex in each v_i and its maximum over each ball factor sits on the sphere. Valid.
4. Fixing v_1 = (0,0,1) and using the sign symmetry x -> -x: p(v) is invariant under permutations, sign flips u_k -> -u_k (substitute x_k -> -x_k) and O(3) (including reflections). Valid. (The "1/64 over 8 sign tuples" form follows from x -> -x symmetry. Valid.)
5. Canonical form (Theorem 1, steps 2-5). I re-derived each step. The pair with the largest |u_i.u_j| goes to positions (1,2). Flipping signs to make u_1.u_k >= 0 keeps every |u_i.u_j|, so u_1.u_2 is still the largest. Swapping 3 and 4 sorts the z-heights. The frame is f3 = u_1, f1 from u_3 (arbitrary if u_3 = u_1), f2 = ± f3 x f1 with sign chosen so u_4.f2 >= 0 (O(3) allows the reflection). In Weierstrass (stereographic) coordinates r_k^2 = (1-w_z)/(1+w_z) is strictly decreasing in w_z. This gives C4-C6 and the ranges of D = [-1,1]^2 x [0,1] x [-1,1] x [0,1]. C7-C9 are the max-pair property. Every step is valid. Numerical test of the whole canonicalisation: 20000 random 4-tuples, 0 violations of D or C4-C9, max |p(u) - p(representative)| = 2.2e-16 (not shipped in this package).
6. Leaf bounds. Theorem 2 (AM-GM: sqrt(q) <= rho/2 + q/(2 rho), with ||v_i|| = 1 giving q_s = 4 + 2 sum s_i s_j v_i.v_j, so a smooth bound L in the dot products) is valid for any rho > 0. The second-order Taylor bound with the psi function is valid (psi is the exact max of g y + h y^2/2 on [-r,r], monotone in h and |g|). Theorem 3 (concave quadratic tangent bound with u arbitrary, eta = g0 + H_mid u, Hessian radius for the remainder) is valid; I re-derived it. No gap found in any proof step. One cosmetic error: proof_qrac4.md and README state the strategy value as 0.741481456572267067..., while the true value is 0.74148145657226707169 (the last digits are wrong, harmless).

## 2. My own checker (not shipped in this package; written before looking at the author's code)

Method: pure Python standard library, outward-rounded fixed-point integer intervals (200 bits, floor/ceil rounding, integer sqrt rounded outward) plus exact Fractions for all rational constants. No floats enter any bound. I wrote it from the definition above plus the preorder-string layout in the JSON (digit 0-4 = split that coordinate at its exact midpoint; S<code>, A, Q = leaves). Three leaf methods, tried in order: (A) AM-GM bound with my own rational rho taken from the box midpoint, evaluated by interval arithmetic; (B) Taylor-2 bound on the AM-GM function; (Q) interval Hessian of p by forward second-order jets, exact rational LDL^T positivity test for -H_mid, tangent bound. A leaf that none of these closes is bisected further by me (widest coordinate, up to 14 levels). S leaves: strict closed-box exclusion S4..S9 re-evaluated in interval arithmetic.

Exact output (python3 -I a working file (not shipped) object/certificate_qrac4.json, 8 processes, nice 19, 48 s wall):
```
sha256 8ca3d435fdd22f906e7113aadfa38c09762836b6077d27a8b301a77e91847788
leaves 43476 internal 43475 splits [11797, 8524, 9164, 7671, 6319]
sum of leaf volumes 8 root volume 8
results {('S', True): 10914, ('B', True): 24750, ('R', True): 7432, ('A', True): 317, ('Q', True): 63}
refined leaves 7432 extra subboxes 15108 max refined bound 0.7414819877720719
max leaf upper bound (non-S, passed) 0.7414819969152845
failures 0
```
Reading: the tree string decodes with no characters left over and no missing children. Leaf count, per-coordinate split counts and the S count (10914) match the package. Leaf volumes sum exactly to 8, the volume of the root box D, with dyadic bisection, so the leaves tile D with no gaps and no overlaps; closed boxes share boundaries and the exclusions are strict, so boundaries are handled. All 43476 leaves checked, none sampled; 0 failures. Every non-excluded leaf has a rigorous upper bound <= 0.741482, with a maximum of 0.74148199692 (my looser method). Limit: my simpler bounds closed only 25130 of the 32562 non-S leaves directly; 7432 of the author's A leaves needed my own extra bisection (15108 sub-boxes in total) to pass at the 0.741482 threshold. That means I verified the bound over the author's cover with my own refinement, not that each author leaf passes under a bound as simple as mine; the author's tighter per-leaf bound is not what I re-implemented. The union is still the author's cover of D, refined, and the bound holds on all of it. My checker's maximum (0.7414819969) is a looser number than the author's 0.741481799559635048; I did not reproduce that exact 18-digit figure from my own checker, only the weaker statement <= 0.741482.

Negative controls (not shipped in this package): (i) with threshold 0.74148 (below the true max) the leaves containing the optimum corner z = (0,0,1,0,1) all fail, as they must; (ii) changing S codes on 400 sampled S leaves, 0 of 400 still count as excluded; (iii) S4..S9 on a box around the optimum all return False; (iv) a truncated tree and a tree with an extra leaf are both rejected on decode.

## 3. Attainment and gap

Strategy v = (e3, e3, e1, e2), which is z = (0,0,1,0,1) in D (a corner of the domain; it satisfies C4-C9). Computed from the definition, all 16 sign terms, with exact integer sqrt to 50 digits: p = 0.7414814565722670716874..., equal to 1/2 + (sqrt2 + sqrt6)/16 = 1/2 + (1+sqrt3)/(8 sqrt2). The n = 2 calibration gives 0.85355339059327376. Gap from the strategy to my checker's certified maximum: 5.40e-7. Gap from the strategy to the claimed 0.741482: 5.43e-7. The package's own 3.43e-7 figure refers to its tighter 0.7414818 bound. So the bound is nearly attained, within about 5.4e-7 by my own checker (3.4e-7 by the author's).

## 4. Cross-check with the author's script (run only after my verdict above)

mpmath is not installed for the system Python, and no network is allowed, so I copied an mpmath already on this machine to the scratch folder and ran verify_qrac4.py with it via python3 -I. It printed: 43476 leaves, A 32152, Q 410, S 10914, split counts [11797, 8524, 9164, 7671, 6319], Max certified UB 0.741481799559635048, final line PASS (59 s). This agrees with my result and with the package's numbers.

## 5. Remaining caveats

- The shared-randomness equivalence and the formula for p are taken from arXiv:0810.2937 and the task statement, not re-proved here.
- The certificate stores only leaf codes, not per-leaf numbers, so each A/Q leaf bound must be recomputed (the author's script does, so do I); my method is weaker on 7432 leaves and needed extra bisection.
- Whether a later upstream result ties or beats this (repository review rule) was not part of this role.

## Verdict

The reduction is valid at every step; the cover is exact and gap-free; all 43476 leaves hold under independent outward-rounded arithmetic (with my own extra refinement on 7432); the bound is within about 5.4e-7 of an explicit strategy; the author's script cross-checks.

pass: true
