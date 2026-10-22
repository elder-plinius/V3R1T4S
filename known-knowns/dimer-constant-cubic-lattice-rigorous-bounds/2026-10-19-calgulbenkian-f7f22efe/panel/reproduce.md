context: Claude Code subagent, fresh context [Claude Sonnet 5.5]

# reproduce: cubic-dimer-z4-ub-332 (p3, l4 <= 0.5840147694)

Scope: does the object give the claimed exact ratio, and is the unpublished Z^4 extension a correct proof. Novelty and criterion belong to the other skeptics. No network.

## 0. Integrity
The contributor's hash list verified from the package folder: all OK. I worked on a private copy of the package; my code is not shipped in this package.

## 1. Definition (quoted from object/DERIVATION.md section 3)
"Layer V = Z/m1 x Z/m2 x Z/m3 ... D = {0, e1, e2, e3} (four forward steps); A[u,v] = 1 iff v - u is in D; T4[U,W] = per A[U, V minus W] if |U|+|W| = N, else 0." Claim: (G0) l4 <= (1/(m1 m2 m3)) log rho(T4), applied at (3,3,2), N = 18, with the p = 4 iterate (XY)^4 1 on 9-subsets and Collatz-Wielandt.

## 2. My own checker (written before opening verify-it-yourself/)
My own C program (not shipped in this package): a dimension-general version of my independent C program (layer = product of cyclic groups; K = all automorphisms from images of the generators with phi(D) a translate of D; orbit representatives of i-subsets; X, Y by depth-first search over injective maps with offsets in D; 256-bit unsigned integers; 12 threads; property C spot test on 300 random orbit members). For (3,3,2): |K| = 2, |G| = 36, 1404 orbits of 9-subsets (as in the object). Runs: my program with arguments 9 4 12 - 3 3 3 2 (p = 4 from the all-ones vector), then a small Python script of mine on its output (neither is shipped):
  orbits mine/cert: 1404 1404
  masks equal & v_p equal & (XYv) equal: True
  max ratio 4527733104115888037323625277988191910329450496 / 3349983888759867418883092542107779072 mask 87381
  equals claimed: True
  bound = 0.584014769338132192  ceil10= 0.5840147694  ceil6= 0.584015
  below ln(8!)/16 = 0.662787681422  by 0.078772912
My own all-ones iterate coincides entry by entry with the shipped vector and its (XYv) column. I also fed the shipped vector (columns id, mask, v only) to my program and recomputed XYv: same maximum ratio and bound. 0.5840147694 is rounded up from the exact 0.58401476933813; the certificate header's 0.5840147693 is rounded down, as the claim's own correction says, and the claim sentence uses the correct 0.5840147694.
Maximum over sectors (all done by me, p = 4 from ones; output not shipped): sector 0: 0.306160326139; 1: 0.381977252268; 2: 0.437313211213; 3: 0.480230784663; 4: 0.513926698608; 5: 0.540074992033; 6: 0.559663479204; 7: 0.573299909536; 8: 0.581351442136; 9: 0.584014769338. Sector 9 is the maximum. N = 18 is even, so sectors 0..9 cover all subset sizes.

## 3. Author's script
sh verify-it-yourself/run_checks.sh (CW_PROCS=12): its output (not shipped separately): trace identity (2,2,2), l = 4: 546803712 = 546803712; property C at (2,2,2) and (3,2,2) HOLDS; "RESULT cert dims=3,3,2 sector=9 orbits=1404 listed_mismatches=0 u=1382 ratio=4527733104115888037323625277988191910329450496/3349983888759867418883092542107779072"; "PASS sector 9 exact ratio equals the shipped one; l4 <= 0.5840147694 (ten places, rounded up)... ALL CHECKS PASS". Agrees with mine (its displayed bound=0.5840147693 is a truncation of the same exact value).

## 4. Proof of the extension re-derived (F1 to F6)
(F1) Q = Z^4/<m1(e1-e4), m2(e2-e4), m3(e3-e4), l e4>, l even >= 4, all m_j >= 2. Neighbours are x +- e_i; two coincide, or one equals x, iff a nonzero difference among +-e_i, +-e_i +- e_j, +-2e_i lies in the lattice. Lattice vectors have first three coordinates a_j m_j. A difference with a coordinate +-1 among the first three would need m_j | 1: impossible. +-2e_i with i <= 3 needs m_i = 2, a_i = +-1 and then the fourth coordinate b l -+ 2 must vanish: b l = +-2, impossible for l >= 4. Differences supported on e4 alone need a = 0 and b l = +-1 or +-2: impossible. So Q is simple and 8-regular; every lattice vector has even coordinate sum, so coordinate-sum parity is a proper 2-colouring. my trace script also asserts simple, 8-regular and bipartite for (2,2,2), l = 4.
(F2) The map x -> ((x1 mod m1, x2 mod m2, x3 mod m3), x1+x2+x3+x4 mod l) is onto with kernel exactly the lattice (solve x_j = a_j m_j, x4 = l c - sum a_j m_j), hence an isomorphism; edges x -> x+e_i raise the height by 1 and shift the layer by e1, e2, e3, 0 for i = 1..4, which is D. The transfer argument gives pm(Q) = tr(T4^l). Independent computational check (my own script, not shipped: Q built by triangular reduction, perfect matchings by the Ryser permanent over the bipartition, T4 built from the definition): (2,2,2), l = 4: 546803712 = 546803712 (its output is not shipped).
(F3) Doubling an m_j or l gives an index-2 sublattice, so the identity on Z^4 induces a 2-to-1 covering that is bijective on neighbourhoods: a 2-lift with bipartite base. Csikvari's pm(H) <= pm(G)^2 for a 2-lift H of a bipartite G (J. Eur. Math. Soc. 2017, via He's Theorem 2.4) is cited, not re-derived (no network); it is stated for arbitrary bipartite graphs, with no dimension restriction.
(F4) The lattice for (2^p m; 2^p) contains 2^p m_j e_j (since 2^p m_j e4 is a multiple of 2^p e4), so it is the rectangular lattice <2^p m_j e_j, 2^p e4>; the box is a spanning subgraph of that torus; 3p lifts (l = 2^p fixed, all graphs simple and bipartite) give pm(box) <= pm(Q_{m,2^p})^{2^{3p}}; and pm(Q_{m,2^p}) = tr(T4^{2^p}) <= 2^N rho^{2^p}.
(F5) The volume is 2^{4p} N, so (1/vol) log f(box) <= (1/N) log rho + (log 2)/2^p, and p -> infinity gives l4 <= (1/N) log rho(T4). This is the per-site normalisation of Butera-Federbush-Pernici's lambda_4(1).
(F6) Compression: for g = (u, phi) with phi(D) = s + D, the map v -> u + phi(v) sends an edge with difference in D to an edge with difference in s + D, so with g_*(w) = g(w) - s (again in G, a bijection) T[gU, g_*W] = T[U,W]; summing over an orbit shows the column-orbit sums do not depend on the representative row (property C), so T P = P T-hat and, with ||T^k||_inf <= ||T-hat^k||_inf, rho(T) <= rho(T-hat). Nothing uses |D| = 3. My program tests property C on 300 random members at (3,3,2) with 0 failures; the author's check does the full matrices at (2,2,2) and (3,2,2). T-hat^2 is block diagonal over sector pairs, so rho(T-hat)^2 = max_i rho(X_i Y_i), and Collatz-Wielandt for the positive integer vector completes the bound: l4 <= (1/36) log(ratio) = 0.584014769338132.
I find the extension proved, modulo Csikvari's lemma as cited and the existence of the limit defining l4 (Hammersley). Every place where dimension 3 could enter (F1 differences, the lifts, the rectangular torus, the group action) was re-derived above for d = 4.

## 5. Open questions touching reproduction
Q1: proved as above, up to the cited lemma. Q4: |G| = 36 = 18 translations x |K| = 2 confirmed by my rebuild. Q5: only (3,3,2) is claimed; I checked only it. Q2 and Q3 (comparator, lower-bound sourcing) are not reproduction questions; the saved BFP row shows lower bound 0.53972077 and estimate 0.57666, both below 0.5840147694, consistent with a true upper bound.

Mismatch count: 0. Non-determinism: none.
pass: true
