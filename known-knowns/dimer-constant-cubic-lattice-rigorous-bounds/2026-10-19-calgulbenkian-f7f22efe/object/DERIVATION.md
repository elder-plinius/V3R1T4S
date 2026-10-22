# Derivation: an upper bound on the dimer constant l4 of Z^4 from 4D diagonal layers

STATUS: THE EXTENSION OF HE'S ARGUMENT FROM Z^3 TO Z^4 USED HERE IS THE AUTHOR'S OWN AND IS NOT PUBLISHED.
He (arXiv 2607.28810, Section 4, quoted) says only: "the method described in this paper can be generalized without
modification to hypercubic lattices in higher dimensions, though we did not pursue this direction". Nothing in the
fetched sources states or proves the 4D lemmas. They are written out below from the triage agent's re-derivation
and the author's notes.

OPEN QUESTION 1 for the panel: is this extension proved? The steps to scrutinise are (F1)-(F6) in section 3.

## 1. The quantity and the comparator (from the fetched sources)

l4 is the dimer constant of Z^4: l4 = lim (1/vol) log (number of perfect matchings of a box of volume vol in Z^4), the
limit existing as all sides tend to infinity (Hammersley 1966 for Z^d; He states it for Z^3; Butera, Federbush and
Pernici write it lambda_d(1)).

Butera, Federbush, Pernici (arXiv 1305.7028, Phys. Rev. E 88, 032113 (2013)), LaTeX source fetched 2026-10-19. The
caption of their table says the rigorous bounds are "(1/2) ln(2d) - 1/2 <= lambda_d(1) <= ln((2d)!)/4d" with
citation [13] = P. Federbush and S. Friedland, J. Stat. Phys. 143, 306 (2011) (for d = 3 they use other references).
The row for d = 4 reads, quoted:

    lambda_4(1) & 0.53972077 & 0.576517 & 0.57666(3) & 0.66278769

with columns Lower Bound, Non-rig. L.B., Our Estimate, Upper Bound. So the Z^4 upper bound in that table is
ln(8!)/16 = 0.66278769 and the rigorous Z^4 lower bound it shows is 0.53972077 = (1/2) ln 8 - 1/2. (Argon's PREREG
gave a "published lower bound 0.55808612 (Schrijver 1998, BFP Table III)"; BFP's table does not show that number.
The lower bound is not used by this claim.) Whether a better Z^4 upper bound exists elsewhere in the literature was
not searched beyond three arXiv API queries (table-record/); one hit, arXiv 1502.06734 (positivity of virial
coefficients in lattice dimer models and upper bounds on the number of matchings on graphs), was not read.

## 2. The inequality to be proved

(G0) For integers m1,m2,m3 >= 2:  l4 <= (1/(m1 m2 m3)) log rho(T4_{m1,m2,m3}), with T4 defined next. The claim takes
(m1,m2,m3) = (3,3,2).

## 3. Definitions and proof

Layer V = Z/m1 x Z/m2 x Z/m3, N = m1 m2 m3 (18 for (3,3,2)); D = {0, e1, e2, e3} (four forward steps); A[u,v] = 1 iff
v - u is in D; T4[U,W] = per A[U, V minus W] if |U|+|W| = N, else 0 (He's definition with one more step).
Quotient graphs: for even l >= 4,  Q_{m,l} = Z^4 / Lambda, Lambda = <m1(e1-e4), m2(e2-e4), m3(e3-e4), l e4>.

(F1) Simple, 8-regular, bipartite. An element of Lambda is a1 m1(e1-e4) + a2 m2(e2-e4) + a3 m3(e3-e4) + b l e4, with
first three coordinates a_j m_j and fourth coordinate b l - sum a_j m_j. The differences to exclude are +-e_i,
+-e_i +- e_j and +-2 e_i (i,j in 1..4). A difference with a coordinate +-1 among the first three needs m_j | 1, impossible for
m_j >= 2; a difference +-2 e_i with i <= 3 needs m_i = 2, a_i = +-1 and then b l = +-2 in the fourth coordinate, impossible
for l >= 4; differences supported on e4 alone (+-e4, +-2e4) need a = 0 and b l = +-1 or +-2, impossible for l >= 4.
So the eight neighbours of each vertex are distinct and different from it. Every element of Lambda has even coordinate sum
(m_j(e_j - e4) has sum 0; l is even), so the parity of the coordinate sum is a bipartition. (The checker's brute-force
quotient builder asserts that no edge is a loop.)

(F2) Trace identity. The map [x] -> ((x1 mod m1, x2 mod m2, x3 mod m3), x1+x2+x3+x4 mod l) is a group isomorphism
Z^4/Lambda -> V x Z/l. The edges x -> x+e_i go from height k to k+1 and the offsets in the layer are (1,0,0), (0,1,0),
(0,0,1), (0,0,0) for e1,e2,e3,e4, i.e. D. By the same transfer-matrix argument as He's Lemma 2.2,
pm(Q_{m,l}) = tr(T4^l). Checked by brute force for (2,2,2), l = 4: 546803712 perfect matchings equal the trace
(cwcheck.py trace 2,2,2 4).

(F3) 2-lifts. Lambda for (2 m1, m2, m3; l) is an index-2 subgroup of Lambda for (m1, m2, m3; l), and likewise for doubling
m2, m3 or l, so the identity on Z^4 induces a 2-to-1 map that is a bijection on neighbourhoods: the doubled graph is a
2-lift (He's argument). Csikvari's inequality as quoted by He (label thm: 2-lift, Theorem 2.4 by order; Csikvari,
J. Eur. Math. Soc. 2017, Lemma 4.2; we did not fetch it): "If G is a bipartite graph and H is a 2-lift of G, then, for all
t >= 0, M(H,t) <= M(G,t)^2", with corollary "pm(H) <= pm(G)^2". The graphs are bipartite by (F1).

(F4) Box in torus, then lifts. For p >= 2 the lattice <2^p m1 e1, 2^p m2 e2, 2^p m3 e3, 2^p e4> is rectangular and equals
Lambda for (2^p m; 2^p) (because m_j times 2^p e4 lies in <2^p e4>). The box with those sides is a spanning subgraph, so
f(box) <= pm(Q_{2^p m, 2^p}). Doubling m1, m2, m3 p times each (3p lifts, l = 2^p >= 4 throughout) gives
pm(Q_{2^p m,2^p}) <= pm(Q_{m,2^p})^{2^{3p}}, and pm(Q_{m,2^p}) = tr(T4^{2^p}) <= 2^N rho(T4)^{2^p} (at most 2^N eigenvalues,
each of modulus at most rho).

(F5) Limit. vol = 2^{4p} N, so (1/vol) log f(box) <= (1/N) log rho + (log 2)/2^p; letting p tend to infinity gives (G0).

(F6) Compression and sectors. G = V x| K, K = the automorphisms phi of the group V with phi(D) = s + D for some s;
|G| = 36 for (3,3,2) (18 translations times |K| = 2; the checker rebuilds G by brute force from this definition; Argon's
table describes the point group incorrectly, see CLAIM.md). He's proofs of property C and of the compression
(Props. 3.1-3.2) use only that phi is a bijection of V and phi(D) = s + D, not |D| = 3; with g_* = (u - s_phi, phi) the
identity T[U,W] = T[gU, g_*W] and the intertwining T P = P \hat T hold verbatim, giving rho(T4) = rho(\hat T4). The
checker verifies property C by brute force on the full matrices for (2,2,2) and (3,2,2) (RECEIPTS.md); this is a check
of the lemma on small cases, not a proof. The sector decomposition rho(\hat T)^2 = max_i rho(X^(i) Y^(i)) is He's (T only
links |U| = i to |W| = N - i). Here N = 18 is even and sector 9 has X = Y.

## 4. The exact inequality checked

For sector i, X = Phi_i and Y = Phi_{N-i}, where (Phi_k y)(U) = sum over injections f: U -> V with f(u) - u in D of
y(orbit of V minus f(U)). Collatz-Wielandt (Horn and Johnson, Matrix Analysis, Thm 8.1.26): for a nonnegative matrix A and
a positive vector v, rho(A) <= max_u (Av)_u / v_u. The shipped file lists, for sector 9, v = (XY)^4 1 and (XY)^5 1 on
1404 orbits. The maximum ratio is 4527733104115888037323625277988191910329450496 / 3349983888759867418883092542107779072
at orbit 1382, whose logarithm divided by 36 is 0.5840147694 (rounded outward to six places: 0.584015). The same p = 4
iterates from the all-ones vector are computed for every sector 0..9 by cwcheck.py iter; sector 9 is the largest. Then
l4 <= (1/N) log rho(T4) = (1/(2N)) max_i log rho(X Y) <= 0.5840147694. The hypotheses hold: XY is nonnegative, and the
vectors are positive (all-ones iterates; XY has positive diagonal because the identity injection u -> u is allowed).

## 5. What is and is not from the source

From He: the method, Lemma 2.2, the 2-lift lemma, Csikvari's inequality, Props. 3.1-3.2 and Cor. 3.4 in 3D. The author's
own and unpublished: every 4D statement in section 3, and the choice of (3,3,2).
