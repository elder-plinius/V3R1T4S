# REPRODUCE skeptic: p_c^site(Z^3) <= 4427/10000

context: subagent (fresh, claim/ copy only)

Order of work: read claim/PROOF.md and claim/CLAIM.md, re-derived the argument, wrote and ran my own exhaustive
checker (skeptic code, kept under the reproduce work folder: skeptic/enum/main.go, skeptic/exact.py,
skeptic/gtest.py) before opening claim/code, claim/REPRODUCE.md or claim/outputs; then read the author's code,
built it from source in a fresh copy of claim/, ran the claim/REPRODUCE.md commands and compared with claim/outputs/.
Nothing outside the claim/ copy was read.

## 1. Proof re-derivation (claim/PROOF.md sections 0-5)

- Setting. In global coordinates the site (2,y,z)+3v is adjacent to (3,y,z)+3v = (0,y,z)+3w for w = v+e_1, so the
  "mirror" is the identity on the two transverse coordinates, and eta(v,w) = 1 iff the two facing traces of G
  meet. eta is a function of (eps(v), eps(w)). OK.
- Growth process and Claim. xi(u) = 1 (u != 0) means eta(parent,u) = 1, so G(eps(u)) is nonempty, connected and has
  a site adjacent to a site of G(eps(parent)); induction along the parent chain from the all-open B_0 containing 0.
  A selected vertex has no unassigned neighbour after its step, so each step selects a new block. OK.
- Lemma 1 (coupling). zeta(0) <= xi(0) = 1. At each step the Strassen coupling uses fresh uniforms; earlier zeta are
  functions of earlier xi and of auxiliaries independent of the block states, so the new xi given (history, earlier
  zeta) has the law given the history, and each zeta batch is Bernoulli(q)^children independent of the past; the
  hybrid-field argument gives the product law. Die-out: every neighbour of a xi = 1 vertex was assigned with
  zeta <= xi, so the zeta-cluster of 0 is inside the finite set {xi = 1}. Survival: infinitely many disjoint
  nonempty sets G(eps(v)) + 3v lie in C(0). Hence theta(q) <= P_p(survival | R) <= theta(p)/p^27. OK.
- Lemma 2 (tree information). The history event is R together with {eta(e) = x_e on the exploration-tree edges}
  (the selection rule is a deterministic function of the revealed values). The constraint graph is a tree. The
  selected block b2 is a leaf (a vertex receives children only when it is selected, and it is selected once), so
  its only constrained edge is to its parent c. The children are unassigned, so under the posterior their eps are
  i.i.d. pi and independent of the tree blocks; given eps(b2) = beta the children's xi are independent
  Bernoulli(r_i(T_i(beta))). Cutting the tree at (c, b2) gives w(beta) proportional to
  pi(beta) sum_gamma 1[eta(gamma,beta) = 1] mu_c(gamma); eta depends on gamma only through U = mirror of T_F(gamma),
  so w = sum_U lambda_U w_U over nonempty U (empty U contributes 0), and Z_U > 0 (all-open state). For c = 0,
  mu_c is the point mass at the all-open state, so U = full face, which (ii) covers. OK.
- Reduction. {P : P(A) >= Q(A) for all up-sets A} is convex (linear inequalities); projection to a subset of the
  children preserves domination (an up-set in fewer coordinates lifts to an up-set). A non-root b2 has at most 5
  children, all among the 5 non-entry faces. Root: 6 independent Bernoulli(r_f(full face)) dominate
  Bernoulli(q)^6 iff every r_f(full face) >= q. Strassen on the finite poset {0,1}^5 (7581 up-sets including the
  empty and full sets, which hold trivially). OK.
- Chain. Each passing link gives theta(p_j) >= p_j^27 theta(q_j). Base: q_1 = 501/1000 > 1/2 >= p_c^site(Z^3)
  (Campanino-Russo 1985, cited; only the non-strict p_c <= 1/2 is used), so theta(q_1) > 0. q_j = p_{j-1} for
  j = 2..7: 501/1000 -> 2317/5000 -> 9/20 -> 1781/4000 -> 1109/2500 -> 443/1000 -> 1107/2500 -> 4427/10000 (same
  list in claim/PROOF.md, claim/result/bound.json, and enforced by claim/code/chain.py, which sets q = p after
  each link). Hence theta(4427/10000) > 0 and p_c <= 4427/10000. OK.

No logical gap found. One under-specification: claim/PROOF.md does not define "site order" for the last tie-break
(the code uses site id 9x+3y+z). This is harmless: the proof holds for any deterministic connected-or-empty rule,
and my checker used its own order (bit index x+3y+9z); on the same integer states that is the author's rule in
x<->z reflected coordinates, and the counts coincide exactly after relabelling faces (section 4).

## 2. Definition implemented (quoted from claim/PROOF.md)

> Block B = {0,1,2}^3 (27 sites); B_v = B + 3v for v in Z^3. [...] x in B_v and y in B_w are Z^3-adjacent iff x lies
> on that face of B_v and y = x + (w - v) (each face site has exactly one partner, its mirror image across the face).

> eps(v) in {0,1}^B is the configuration of B_v translated to B. G(eps) is the largest open component of eps
> (connectivity inside B); ties are broken by the larger sum over the six faces of the number of the component's
> sites on that face, then by the first component found in site order; and G = empty set if that component has
> fewer than s = 6 sites (or eps has no open site).

> Writing T_F(eps) for the trace of G(eps) on face F, eta(v, w) = 1 iff T_F(eps(v)) and the mirror of
> T_{F'}(eps(w)) meet, where F, F' are the faces of B_v, B_w on their common boundary.

> nu_beta = prod over children i of Bernoulli(r_i(T_i(beta))), with r_i(T) = P_p(T meets the mirror of the trace
> of G(eps') on the facing face) for independent eps'. [...] w = sum_U lambda_U w_U, with
> w_U(beta) ∝ pi(beta) 1[T_in(beta) meets U], over nonempty U in the entry face.

> (i) at the root step (eps(0) all open, U = the full face for each child): r_f(full face) >= q for each face f;
> (ii) for each entry face F_in and each nonempty U contained in F_in, the law of the 5 children's eta under w_U
> dominates Bernoulli(q)^5. By Strassen's theorem this is: for every up-set A of {0,1}^5, law_U(A) >= q-measure of A.

## 3. Skeptic checker (independent, written before reading claim/code)

- skeptic/enum/main.go, mode counts: all 2^27 states; components by bit-parallel flood fill (6-neighbour
  adjacency inside B); G = max by (size, face-sum), exact ties keep the component with the smallest minimum bit
  index; G = empty if |G| < 6; exact integer counts c[d][T][k] = #{states : k open sites, trace of G on face d = T}.
- skeptic/exact.py: exact rationals (Python Fraction / big integers) for P(trace_d = T), r_d(T),
  1 - r_d(T), pi_k = p^k (1-p)^(27-k); root condition (i) checked exactly; every table value rounded outward
  to float64, each enclosure confirmed by exact comparison.
- skeptic/enum/main.go, mode accum: for every state, every entry face din and every child pattern x in {0,1}^5,
  pi_k * prod_children (x_i ? r_i : 1 - r_i), accumulated into lo/hi sums keyed by (din, trace_din(G), x).
  Rigour: all quantities are nonnegative, each term has 5 roundings and then at most 2^27 + 6 additions (M < 2^28
  roundings, u = 2^-53, no underflow: every nonzero input >= 1e-30, asserted), so the exact sums lie in
  [lo * (1 - 2^-24), hi * (1 + 2^-23)] (a priori bound, stricter than needed).
- Consistency check: for every (din, T), the sum over x of the bounds must bracket the exact P(trace_din = T),
  since r + (1 - r) = 1.
- Per (din, U): exact big-integer subset-sum (zeta) transform gives the numerators summed over T meeting U, and
  the exact normaliser Z_U = P(T_in meets U); the law bounds are rounded down/up to float64 (verified exactly).
- Up-sets of {0,1}^5 generated recursively (A = A0 + shifted A1 with A0 subset of A1); the count of 7581 and the
  upward closure of each set are asserted; the 7579 nontrivial ones are used. Check: lower-bound sum >= Q(A)
  rounded up + 1e-12, where 1e-12 is far above the float error of a 32-term nonnegative sum (<= 32u).
- Unit test of my G/trace code against a plain BFS written separately from the same definition (random states
  plus constructed tie cases):
```
tested 160204 states, mismatches 0
```

## 4. Skeptic results

Exhaustive counts pass (4 s on 6 cores), and the sha256 of my counts rewritten in the author's file format
(skeptic face d -> author face [4,5,2,3,0,1][d], same bit patterns, same face-local indices), next to
claim/outputs/counts_b333_s6.sha256:
```
$ enum counts out/counts.txt  (first 3 lines of the output file)
# skeptic counts: d T k count (nonzero only)
# states=134217728 emptyG=14352467 tie_by_facesum=470056 tie_by_siteorder=151299
# |G| histogram: 14352467 0 0 0 0 0 7364204 8132062 8536300 8918178 9510878 10274701 11055452 11616701 11628067 10743701 8848781 6306036 3809083 1928841 812005 280993 78620 17362 2917 351 27 1
$ sha256sum (skeptic counts rewritten in author format) ; cat claim/outputs/counts_b333_s6.sha256
be9baff2b77732cb3d3abae91c8b07fb2cc128102b4f2f63ac643b2d097ec2ff *out/counts_in_author_format.txt
be9baff2b77732cb3d3abae91c8b07fb2cc128102b4f2f63ac643b2d097ec2ff  out/counts_b333_s6.txt (cert.exe 3 3 3 6 6 counts, sorted output)
```

My independent counts reproduce the author's recorded counts file bit for bit.

Skeptic check output for each link (accumulation pass about 41 s per link; the check prints the root
margins r_d(full face) - q, the consistency check, the worst up-set margin as a rigorous bracket [lower, upper]
with its location in my face/child labelling, and the verdict):
Link p = 2317/5000, q = 501/1000:
```
root: r_d(full face) - q = ['2.600951e-01', '2.601849e-01', '2.600029e-01', '2.602951e-01', '2.599481e-01', '2.604062e-01'] ok
consistency of accumulators with exact trace laws: ok; worst relative bracket width 1.788e-07
up-sets checked: 3066 laws x 7579 nontrivial up-sets = 23237214 comparisons
worst margin P_U(A) - Q(A) in [1.938744e-04, 1.940311e-04] at entry face 4, U=000000001 (|U|=1), A=0xffffffcc (|A|=28)
  face 0 worst lower margin 1.938744e-04
  face 1 worst lower margin 2.289047e-04
  face 2 worst lower margin 1.938744e-04
  face 3 worst lower margin 3.126304e-04
  face 4 worst lower margin 1.938744e-04
  face 5 worst lower margin 3.787144e-04
negative lower margins: 0
RESULT link p=2317/5000 q=501/1000: root ok, up-sets ok  (5.5s)
```
Link p = 9/20, q = 2317/5000:
```
root: r_d(full face) - q = ['2.641850e-01', '2.642691e-01', '2.640976e-01', '2.643733e-01', '2.640451e-01', '2.644795e-01'] ok
consistency of accumulators with exact trace laws: ok; worst relative bracket width 1.788e-07
up-sets checked: 3066 laws x 7579 nontrivial up-sets = 23237214 comparisons
worst margin P_U(A) - Q(A) in [1.115867e-04, 1.117379e-04] at entry face 2, U=000000001 (|U|=1), A=0xfffffcfc (|A|=28)
  face 0 worst lower margin 1.115867e-04
  face 1 worst lower margin 1.461283e-04
  face 2 worst lower margin 1.115867e-04
  face 3 worst lower margin 2.286276e-04
  face 4 worst lower margin 1.115867e-04
  face 5 worst lower margin 2.935277e-04
negative lower margins: 0
RESULT link p=9/20 q=2317/5000: root ok, up-sets ok  (4.1s)
```
Link p = 1781/4000, q = 9/20:
```
root: r_d(full face) - q = ['2.651396e-01', '2.652214e-01', '2.650542e-01', '2.653231e-01', '2.650027e-01', '2.654273e-01'] ok
consistency of accumulators with exact trace laws: ok; worst relative bracket width 1.788e-07
up-sets checked: 3066 laws x 7579 nontrivial up-sets = 23237214 comparisons
worst margin P_U(A) - Q(A) in [1.136203e-04, 1.137694e-04] at entry face 2, U=000000001 (|U|=1), A=0xfffffcfc (|A|=28)
  face 0 worst lower margin 1.136203e-04
  face 1 worst lower margin 1.477743e-04
  face 2 worst lower margin 1.136203e-04
  face 3 worst lower margin 2.293814e-04
  face 4 worst lower margin 1.136203e-04
  face 5 worst lower margin 2.935158e-04
negative lower margins: 0
RESULT link p=1781/4000 q=9/20: root ok, up-sets ok  (5.9s)
```
Link p = 1109/2500, q = 1781/4000:
```
root: r_d(full face) - q = ['2.654996e-01', '2.655806e-01', '2.654149e-01', '2.656815e-01', '2.653638e-01', '2.657848e-01'] ok
consistency of accumulators with exact trace laws: ok; worst relative bracket width 1.788e-07
up-sets checked: 3066 laws x 7579 nontrivial up-sets = 23237214 comparisons
worst margin P_U(A) - Q(A) in [2.034570e-04, 2.036054e-04] at entry face 4, U=000000001 (|U|=1), A=0xffffffcc (|A|=28)
  face 0 worst lower margin 2.034570e-04
  face 1 worst lower margin 2.374507e-04
  face 2 worst lower margin 2.034570e-04
  face 3 worst lower margin 3.186931e-04
  face 4 worst lower margin 2.034570e-04
  face 5 worst lower margin 3.825205e-04
negative lower margins: 0
RESULT link p=1109/2500 q=1781/4000: root ok, up-sets ok  (4.4s)
```
Link p = 443/1000, q = 1109/2500:
```
root: r_d(full face) - q = ['2.655448e-01', '2.656255e-01', '2.654604e-01', '2.657261e-01', '2.654094e-01', '2.658292e-01'] ok
consistency of accumulators with exact trace laws: ok; worst relative bracket width 1.788e-07
up-sets checked: 3066 laws x 7579 nontrivial up-sets = 23237214 comparisons
worst margin P_U(A) - Q(A) in [1.654623e-04, 1.656104e-04] at entry face 0, U=000000001 (|U|=1), A=0xfffffafa (|A|=28)
  face 0 worst lower margin 1.654623e-04
  face 1 worst lower margin 1.993944e-04
  face 2 worst lower margin 1.654623e-04
  face 3 worst lower margin 2.804973e-04
  face 4 worst lower margin 1.654623e-04
  face 5 worst lower margin 3.442079e-04
negative lower margins: 0
RESULT link p=443/1000 q=1109/2500: root ok, up-sets ok  (7.5s)
```
Link p = 1107/2500, q = 443/1000:
```
root: r_d(full face) - q = ['2.656089e-01', '2.656895e-01', '2.655246e-01', '2.657899e-01', '2.654737e-01', '2.658929e-01'] ok
consistency of accumulators with exact trace laws: ok; worst relative bracket width 1.788e-07
up-sets checked: 3066 laws x 7579 nontrivial up-sets = 23237214 comparisons
worst margin P_U(A) - Q(A) in [1.992792e-04, 1.994272e-04] at entry face 0, U=000000001 (|U|=1), A=0xfffffafa (|A|=28)
  face 0 worst lower margin 1.992792e-04
  face 1 worst lower margin 2.331904e-04
  face 2 worst lower margin 1.992792e-04
  face 3 worst lower margin 3.142460e-04
  face 4 worst lower margin 1.992792e-04
  face 5 worst lower margin 3.779171e-04
negative lower margins: 0
RESULT link p=1107/2500 q=443/1000: root ok, up-sets ok  (7.7s)
```
Link p = 4427/10000, q = 1107/2500:
```
root: r_d(full face) - q = ['2.655408e-01', '2.656213e-01', '2.654565e-01', '2.657217e-01', '2.654056e-01', '2.658246e-01'] ok
consistency of accumulators with exact trace laws: ok; worst relative bracket width 1.788e-07
up-sets checked: 3066 laws x 7579 nontrivial up-sets = 23237214 comparisons
worst margin P_U(A) - Q(A) in [1.230925e-04, 1.232404e-04] at entry face 4, U=000000001 (|U|=1), A=0xffffffcc (|A|=28)
  face 0 worst lower margin 1.230925e-04
  face 1 worst lower margin 1.569932e-04
  face 2 worst lower margin 1.230925e-04
  face 3 worst lower margin 2.380250e-04
  face 4 worst lower margin 1.230925e-04
  face 5 worst lower margin 3.016762e-04
negative lower margins: 0
RESULT link p=4427/10000 q=1107/2500: root ok, up-sets ok  (4.7s)
```

Comparison of worst margins (my rigorous bracket, from the outputs above, against the author's value in
claim/result/bound.json and claim/outputs/*_summary.txt):

| link | p | q | skeptic worst-margin bracket | author worst margin | inside |
|---|---|---|---|---|---|
| 1 | 2317/5000 | 501/1000 | [1.938744e-04, 1.940311e-04] | 1.939266e-04 | yes |
| 2 | 9/20 | 2317/5000 | [1.115867e-04, 1.117379e-04] | 1.116371e-04 | yes |
| 3 | 1781/4000 | 9/20 | [1.136203e-04, 1.137694e-04] | 1.136700e-04 | yes |
| 4 | 1109/2500 | 1781/4000 | [2.034570e-04, 2.036054e-04] | 2.035065e-04 | yes |
| 5 | 443/1000 | 1109/2500 | [1.654623e-04, 1.656104e-04] | 1.655116e-04 | yes |
| 6 | 1107/2500 | 443/1000 | [1.992792e-04, 1.994272e-04] | 1.993285e-04 | yes |
| 7 | 4427/10000 | 1107/2500 | [1.230925e-04, 1.232404e-04] | 1.231418e-04 | yes |

All seven links pass the root condition (smallest r_f(full face) - q over all links and faces is 2.599e-01) and all
3066 x 7579 up-set inequalities per link, under my own exhaustive, rigorous checker.

## 5. Author's commands (fresh copy of claim/, built from source)

Manifest check of the fresh copy, and the tail bytes of claim/outputs/chainA_summary.txt:
```
$ sha256sum -c MANIFEST.sha256  (in the fresh copy)
./CLAIM.md: OK
./PROOF.md: OK
./REPRODUCE.md: OK
./code/cert.py: OK
./code/cert/go.mod: OK
./code/cert/main.go: OK
./code/chain.py: OK
./code/upsets.py: OK
./outputs/chainA_log.txt: OK
./outputs/chainA_summary.txt: OK
./outputs/chainB_log.txt: OK
./outputs/chainB_summary.txt: OK
./outputs/counts_b333_s6.sha256: OK
./result/bound.json: OK
./table/literature_record.md: OK
$ tail -c 40 outputs/chainA_summary.txt | od -c
0000000   <       1   /   2       f   o   r       l   i   n   k       1
0000020   )  \n  \n   [   e   x   i   t   e   d       w   i   t   h    
0000040   c   o   d   e       1   ]  \n
0000050
```

claim/REPRODUCE.md commands run verbatim, except `python` -> the venv interpreter (plain `python` is a broken alias
on this machine), plus a second counts run for determinism (full log, interpreter path shown as `python`):
```
+ cd code/cert
+ go build -o cert.exe .
+ echo 'build exit=0'
build exit=0
+ mkdir -p out
++ date +%s
+ start=1792369603
+ ./code/cert/cert.exe 3 3 3 6 6 counts out/counts_b333_s6.txt
++ date +%s
+ echo 'counts exit=0 (43 s)'
counts exit=0 (43 s)
+ sha256sum out/counts_b333_s6.txt
be9baff2b77732cb3d3abae91c8b07fb2cc128102b4f2f63ac643b2d097ec2ff *out/counts_b333_s6.txt
++ date +%s
+ start=1792369646
+ ./code/cert/cert.exe 3 3 3 6 6 counts out/counts_b333_s6_rerun.txt
++ date +%s
+ echo 'counts rerun exit=0 (43 s)'
counts rerun exit=0 (43 s)
+ sha256sum out/counts_b333_s6_rerun.txt
be9baff2b77732cb3d3abae91c8b07fb2cc128102b4f2f63ac643b2d097ec2ff *out/counts_b333_s6_rerun.txt
+ python code/chain.py out/counts_b333_s6.txt out/chainB q1=501/1000 2317/5000 9/20 1781/4000
link 1: p = 2317/5000, q = 501/1000: CERTIFICATE: PASS (p = 2317/5000, q = 501/1000)
checked 3066 entry laws x 7579 up-sets; worst margin 1.939266e-04 at entry face 0 U=0b1 up-set (1, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
link 2: p = 9/20, q = 2317/5000: CERTIFICATE: PASS (p = 9/20, q = 2317/5000)
checked 3066 entry laws x 7579 up-sets; worst margin 1.116371e-04 at entry face 4 U=0b1 up-set (2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
link 3: p = 1781/4000, q = 9/20: CERTIFICATE: PASS (p = 1781/4000, q = 9/20)
checked 3066 entry laws x 7579 up-sets; worst margin 1.136700e-04 at entry face 0 U=0b1 up-set (1, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
chain complete: p_c^site(Z^3) <= 1781/4000 (given Campanino-Russo's p_c < 1/2 for link 1)
+ echo 'chainB exit=0'
chainB exit=0
+ python code/chain.py out/counts_b333_s6.txt out/chainA q1=1781/4000 1109/2500 443/1000 1107/2500 4427/10000
link 1: p = 1109/2500, q = 1781/4000: CERTIFICATE: PASS (p = 1109/2500, q = 1781/4000)
checked 3066 entry laws x 7579 up-sets; worst margin 2.035065e-04 at entry face 0 U=0b1 up-set (1, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
link 2: p = 443/1000, q = 1109/2500: CERTIFICATE: PASS (p = 443/1000, q = 1109/2500)
checked 3066 entry laws x 7579 up-sets; worst margin 1.655116e-04 at entry face 0 U=0b1 up-set (1, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
link 3: p = 1107/2500, q = 443/1000: CERTIFICATE: PASS (p = 1107/2500, q = 443/1000)
checked 3066 entry laws x 7579 up-sets; worst margin 1.993285e-04 at entry face 0 U=0b1 up-set (1, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
link 4: p = 4427/10000, q = 1107/2500: CERTIFICATE: PASS (p = 4427/10000, q = 1107/2500)
checked 3066 entry laws x 7579 up-sets; worst margin 1.231418e-04 at entry face 0 U=0b1 up-set (1, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
chain complete: p_c^site(Z^3) <= 4427/10000 (given Campanino-Russo's p_c < 1/2 for link 1)
+ echo 'chainA exit=0'
chainA exit=0
+ echo ALLDONE
ALLDONE
```

Reproduced logs against claim/outputs/:
```
$ diff claim/outputs/chainB_log.txt vs reproduced out/chainB/chain_log.txt (timings, folder prefix and command lines normalized)
IDENTICAL
$ diff root/checked/CERTIFICATE lines: claim/outputs/chainA_log.txt links 4-7 vs reproduced out/chainA links 1-4
IDENTICAL
```

Cross-check of the author's reproduced laws files against my accumulators (faces relabelled, child bits permuted;
both are enclosures of the same numbers, so every pair must overlap; T = 0 excluded because the author skips
G-empty states, which only feed T = 0, never a nonempty U):
```
$ cross_laws.py skeptic acc (link 7) vs reproduced out/chainA/link4_p4427_10000_laws.txt
compared 98112 intervals (T != 0): non-overlapping 0; max relative lo difference 4.636e-11
$ cross_laws.py skeptic acc (link 1) vs reproduced out/chainB/link1_p2317_5000_laws.txt
compared 98112 intervals (T != 0): non-overlapping 0; max relative lo difference 4.626e-11
```

## 6. Determinism

The author's counts step was run twice: both sha256 equal be9baff2...c2ff = claim/outputs/counts_b333_s6.sha256
(log above). My own passes, run twice:
```
$ sha256sum (skeptic first run vs rerun)
2b6b409b04bc35cb0efd3e2bedaf2f2f4da70912656226e1fe3845ed5da88ea4 *out/counts.txt
2b6b409b04bc35cb0efd3e2bedaf2f2f4da70912656226e1fe3845ed5da88ea4 *out/rerun/counts.txt
69ffea169f19b7c80368ad739f23f5a1ecc1f3263f345f9539ad935ce144a826 *out/acc_4427_10000.txt
69ffea169f19b7c80368ad739f23f5a1ecc1f3263f345f9539ad935ce144a826 *out/rerun/acc_4427_10000.txt
36bf26ec359e1935f69558009c67f397ad7cf17c69a432db4f66fa3fb77a830f *out/table_4427_10000.txt
36bf26ec359e1935f69558009c67f397ad7cf17c69a432db4f66fa3fb77a830f *out/rerun/table_4427_10000.txt
```

## 7. Mismatches, gaps and remarks (none affects the result)

1. claim/outputs/chainA_summary.txt ends with a tool-harness line "[exited with code 1]" (bytes shown in section 5).
   In my reproduction claim/code/chain.py exits 0 for both commands, and the saved logs show exit 0 for every step.
   This is a provenance blemish in a saved output file. The certified content is reproduced exactly.
2. claim/outputs/chainA_* come from a seven-link run starting at q = 1/2 (log folder out/chain), not from
   claim/REPRODUCE.md's second command. claim/REPRODUCE.md says so, and the reproduced links match line for line.
3. chain.py's closing line always says "(given Campanino-Russo's p_c < 1/2 for link 1)", also with q1 = 501/1000,
   where only p_c <= 1/2 is used. This is only the printed wording.
4. claim/PROOF.md section 4 says "interval arithmetic with outward rounding" while section 5 says "all checks passed in
   exact arithmetic". The code does outward-rounded float intervals followed by an exact integer final comparison, as
   claim/result/bound.json states. Again, wording only.
5. "Site order" for the last tie-break is not defined in claim/PROOF.md (see section 1). This is harmless.
6. claim/REPRODUCE.md says the worker count "changes only speed". From reading main.go, the float bits of the laws
   file depend on the worker count through the summation order. The bounds stay valid and the integer counts do not
   depend on it. Not tested.
7. Timing: the counts took 43 s here, against "about 2 minutes" in claim/REPRODUCE.md.

Outside this skeptic's remit: whether 0.4427 is below every published rigorous bound (the claim package cites
Campanino-Russo's 1/2 as the record) was not assessed.

## Verdict

The argument re-derives with no gap. My independent exhaustive checker, written from the definitions, confirms every
link of the chain in rigorous arithmetic: root condition, consistency with exact trace laws, and all 3066 x 7579
up-set inequalities per link. My counts reproduce the author's recorded counts sha256. The author's build reproduces
claim/outputs exactly and deterministically. Every claimed worst margin lies inside my rigorous bracket. The chain is
logically valid from theta(501/1000) > 0.

pass: true
