context: Claude Code subagent, fresh context [claude-sonnet-5-5]

role: criterion. Cell: cubic-dimer-h3-ub-54. Win: p2 of dimer-constant-cubic-lattice-rigorous-bounds. I made no network fetch. The record files (the-record-we-beat/) were used for the comparator text only. Whether a newer h3 bound exists is the novelty skeptic's question.

Hash check: all files match the contributor's hash list (run from inside the package folder). The two certificate parts, concatenated, hash to 4db684405f60...0f74c0c, as README.md states. The parts split a line mid-way, so concatenate them before parsing.

Criterion as I read it (the target's success criterion, also compared with the target list in the repository):
- The bound is strictly better than the best published bound by at least 1e-6.
- (i) There is an explicit nonnegative integer or rational test vector.
- (ii) The transfer-layer definition is given.
- (iii) An exact integer cross-multiplied Collatz-Wielandt ratio gives the claimed bound rounded outward.
- (iv) A written derivation, or exact citation, shows why the ratio bounds the constant.

p2, verbatim: "A certified improvement of either published bound on the 3D monomer-dimer entropy h3 at unit activity: 0.7849602275 <= h3 <= 0.7862023450 (FKLM, arXiv math/0603001 and refs), same certificate rules."

Own mechanical checks (a dynamic-program applier, an orbit preparer, a ratio finder, a naive enumerator and a graph-fact checker, all written from scratch and not shipped in this package). I wrote them from the definition T[U,W] = sum over S inside V minus U of per A[S,W], with D = {(0,0),(1,0),(0,1)}. I did not read the author's mdlayer.c or check_h3.py.
1. The dynamic-program applier applies the whole 2^20 x 2^20 matrix by a vertex-by-vertex dynamic program in exact 128-bit integers. I validated it against a naive enumeration of the definition on random vectors at (2,2), (2,3), (3,2) and (3,3). Every row matched exactly.
2. The orbit preparer computes the translation orbits of Z/5 x Z/4 on all 2^20 subsets itself. It confirmed that the file lists exactly 52488 orbits, in order, with canonical mask equal to the minimum image, and that all values are positive integers (min 41938010, max 281474976710656). It expanded the vector to all 1048576 states. It uses the 20 translations only and no coordinate swap, because 5 differs from 4.
3. The ratio finder takes the maximum of (Tx)_U / x_U over all 1048576 states by integer cross-multiplication. The result is 1891821269973664/281869529, attained at U = 524031, equal to the claimed ratio. The ratio is 6711691.3157848431357..., and log(ratio)/20 = 0.785968076808533207421... This rounds up to 0.7859681 at 7 places and to 0.785968076809 at 12 places. The margin below 0.7862023450 is 2.3427e-4.
4. The graph-fact checker checked the graph facts. For (m,n,l) in (5,4,4), (5,4,8), (10,8,4), (10,8,8), (20,16,16), the graph with edges from (a,b,k) to (a+d1,b+d2,k+1) has mnl vertices, is simple and 6-regular, and is bipartite by height parity. The maps T(2m,n,l), T(m,2n,l) and T(m,n,2l) to T(m,n,l) (reduce mod the smaller modulus) are 2-to-1 neighbourhood-preserving coverings, checked at (5,4,4).

Clauses.
1. Improvement over the published upper bound by at least 1e-6: met. The claim is 0.7859681 against 0.7862023450, a margin of 2.34e-4. The comparator is quoted from FKLM's introduction (credited there to Friedland-Peled). I did not re-fetch it.
2. Same quantity: met. FKLM define h3 as the sup over p of h3(p). The claim bounds the growth of the total number of matchings at unit activity. By E4, the liminf of that growth is at least every h3(p0), hence at least the sup. That is the direction an upper bound needs. The converse is not needed.
3. (i) Explicit vector: met. It is 52488 positive integers, one per translation orbit, covering every state.
4. (ii) Transfer-layer definition: met. DERIVATION.md section 3 gives it. I rebuilt it independently and got the author's ratio exactly.
5. (iii) Exact cross-multiplication and outward rounding: met. I reproduced the ratio and the roundings with Python integers and 40-digit mpmath. The claimed figure is rounded up.
6. (iv) Written derivation: met, with the caveat that it is the author's own and unpublished. See the re-derivation below.

Re-derivation of the steps that depend on (m,n), at (5,4).
- E1, the quotient. The map [x] to ((x1 mod m, x2 mod n), x1+x2+x3 mod l) is well defined, because every generator of span(m(e1-e3), n(e2-e3), l e3) has coordinate sum 0 or l. Its kernel is exactly that lattice (checked by hand), so it is a bijection onto Z/m x Z/n x Z/l with mnl vertices. The edges x to x+e1, x+e2, x+e3 go from height k to k+1 with layer shifts (1,0), (0,1), (0,0), which is D. Nothing uses the parity of m or n. Simplicity needs only m,n >= 2 (the three shifts are distinct mod (m,n)) and l >= 3. Bipartiteness comes from height parity with l even, so m = 5 odd is irrelevant. 6-regularity holds (graph-fact checker). A matching is a cyclic sequence of sets U_k, so the matching count equals tr(T^l). Unit weight on monomers is the only change from He's perfect-matching identity. The folder reports brute-force agreement of the trace identity at small sizes. My own matrix check covers the matrix side (the dynamic program against naive enumeration), and my graph check covers the graph side.
- E2, the 2-lift. The torus is bipartite (height parity, l = 2^p even). T(2m,n,l), T(m,2n,l) and T(m,n,2l) are degree-2 covers of T(m,n,l) (checked above). Csikvari's inequality M(H,t) <= M(G,t)^2 holds for all t >= 0, and t = 1 is inside its hypotheses. The statement is quoted in the folder; I did not fetch Csikvari's paper.
- E3, box in torus. The box (M,N,L) = (2^p m, 2^p n, 2^p) is a spanning subgraph of Z^3/span(M e1, N e2, L e3). L divides M and N, so M e3 and N e3 lie in He's lattice. Then M e1 = M(e1-e3) + M e3 is in it, and likewise N e2. So the rectangular lattice equals span(M(e1-e3), N(e2-e3), L e3), and the torus is T(M,N,L). Its sides are all at least 3, so it is simple. Going from T(M,N,L) down to T(m,n,L) takes p lifts in each of two directions, 2p in all, so the exponent is 2^(2p), the product of the degrees.
- E3, spectral bound. tr(T^l) <= 2^(mn) rho^l holds for any nonnegative matrix with 2^(mn) eigenvalues, each of modulus at most rho.
- E4 and E5, normalisation. vol = 2^(3p) m n. Then (2^(2p) / (2^(3p) m n)) * log(2^(mn) rho^(2^p)) = log(rho)/(mn) + log(2)/2^p. The factor is 1/(mn) = 1/20 at (5,4), which is what the claim and my computation use. The limit p to infinity leaves (1/20) log rho.
- Collatz-Wielandt. T is nonnegative and x is strictly positive (checked), so rho <= max_U (Tx)_U / x_U, which is the exact ratio computed above.
I find nothing at (m,n) = (5,4) that needs more than the (3,3) derivation did. The sibling (3,3) cell is the same theorem at a smaller size and is subsumed by this one. As the claim says, only the (5,4) bound is the improvement to record.

Answers to the open questions in the claim record (not shipped) that concern the criterion.
1. Is the extension proved? Yes. I re-derived E1 to E5 above, and the (5,4) case needs no step beyond (3,3). The derivation is unpublished but complete, and the criterion accepts a written derivation. The label "He's Theorem 2.4" was a mis-citation of Csikvari's inequality. The folder says so, and it affects no step.
2. Does FKLM's h3 (sup over densities) match the growth of the total count? Only the inequality liminf (1/vol) log Phi >= h3 is needed, and E4 derives it correctly from FKLM's box limit (sides 2^p m, 2^p n, 2^p all tend to infinity). Equality is not needed.
3. Newer rigorous h3 bound: not decided here. This is for the novelty skeptic. The folder's arXiv API queries and its FKLM excerpt show none. I did not read Friedland-Peled.
4. Orbit vector from the 20 translations only: acceptable. The check applies the whole matrix and takes the maximum over every state, so validity does not depend on any symmetry. I verified the orbit structure myself.
5. Matrix applied by a dynamic program rather than stored: acceptable. The criterion asks for an independent program that recomputes the ratio from the definition. My own dynamic program, validated against naive enumeration at four small sizes, gives the identical exact ratio.

Doubts and limits: the comparator 0.7862023450 and its currency come from the folder's FKLM excerpt and were not re-fetched. I did not re-run the trace identity at (5,4); the folder reports brute-force agreement at small sizes, and my checks of the graph structure plus the argument above cover (5,4).

confirmed_scope: The 3D monomer-dimer entropy h3 of Z^3 (growth of the total number of matchings at unit activity, FKLM's sup over density) satisfies h3 <= 0.7859681, by exact integer Collatz-Wielandt on the full 1048576-state monomer-dimer diagonal-layer matrix at (m,n) = (5,4) (ratio 1891821269973664/281869529, log/20 = 0.7859680768...), below FKLM's 0.7862023450 by 2.34e-4, resting on a written but unpublished extension of He's argument that I re-derived with no gap; the currency of the comparator is left to the novelty skeptic.

pass: true
