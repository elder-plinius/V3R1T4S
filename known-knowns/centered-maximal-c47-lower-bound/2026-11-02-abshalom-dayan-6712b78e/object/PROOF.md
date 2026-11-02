# Reduction from a periodic measure to c_2

Definition used (page 47a). For f in L^1(R^2) put M f(z) = sup_{r>0} (1/|Q(z,r)|) int_{Q(z,r)} |f|, with Q(z,r) the closed square with centre z and side 2r. The constant c_2 is the least C with alpha |{M f >= alpha}| <= C ||f||_1 for all f in L^1 and alpha > 0.

Setting. P is a finite set of points in the cell C = [0,Lx) x [0,Ly) with masses m_p > 0, M = sum m_p, extended periodically; mu is the resulting measure. A certificate is a finite list of rectangles R_j, each with a finite set S_j of points of the periodic extension and a rational rho_j > 0, such that for every z in R_j and every p in S_j, |z-p|_inf <= rho_j, and 4 rho_j^2 <= mu(S_j). Let V be the union of all period translates of the R_j.

Claim. c_2 >= |V intersect C| / M.

Proof.
1. Fix an integer K and eta > 0. Let P_K be the atoms in a block of (2K)^2 cells. Put f = sum_{p in P_K} m_p (2 eta)^(-2) 1_{Q(p,eta)}. Then f is in L^1 and ||f||_1 = (2K)^2 M.
2. Let D bound |z-p|_inf over all rectangles, z in R_j, p in S_j, and let c = ceil(D/min(Lx,Ly)) + 1. Let z be in the inner block, the block with c cells removed on each side, and z in a translate of R_j, with translated set S. Every p in S has |z-p|_inf <= D, so p lies in the block, because c min(Lx,Ly) >= D + min(Lx,Ly). So S is inside P_K.
3. For such z, the closed square Q(z, rho_j + eta) contains Q(p, eta) for each p in S, so the average of f over it is at least mu(S) / (4 (rho_j+eta)^2) >= rho_j^2 / (rho_j+eta)^2 >= alpha := (rho_min/(rho_min+eta))^2, with rho_min = min_j rho_j > 0. Here t -> (t/(t+eta))^2 is increasing, and overlapping smoothed atoms are no problem because f is a sum.
4. So {M f >= alpha} contains the part of V in the inner block. By periodicity that part has area (2K-2c)^2 |V intersect C|.
5. The definition of c_2 gives c_2 (2K)^2 M >= alpha (2K-2c)^2 |V intersect C|. Let K -> infinity and eta -> 0. QED.

Strict level sets and open squares. For alpha' < alpha, {M f > alpha'} contains {M f >= alpha}, so letting alpha' rise to alpha gives the same bound for the strict form. Open squares follow by enlarging the radius by an arbitrarily small factor.

Normalisation. The value is taken at alpha = 1 for mu, against mass M per cell; scaling positions by t and masses by t^2 leaves it unchanged. Level alpha for mu is level 1 for mu/alpha, a different measure with a different value; other levels are not claimed and the proof needs only alpha = 1. Lin's and Tomar's values are the same ratio: tests/ runs these programs on their measures.

What the checkers do. check_a.py and check_b.c enumerate boxes [x1,x2] x [y1,y2] with corners on atom coordinates of the periodic extension, x1 and y1 in the cell, sides at most the reach. S is the set of atoms in the closed box; mu(S) its exact mass. Let rho be the largest multiple of 2^-40 with 4 rho^2 <= mu(S), in exact integers. Every z in [x2-rho, x1+rho] x [y2-rho, y1+rho] has all of S within rho, so this rectangle is valid for the certificate when nonempty. The reach only removes rectangles, so it can only lower the value. Pieces are clipped to the cell and the area of their union is computed exactly. Because rho is rounded down, the printed value is a lower bound on the true ratio; the inequality needs only that.

Why reach is not a loss here. No witness square can have side above S* where f(S) = M (1/Lx + 1/S)(1/Ly + 1/S) < 1: a closed interval of length S holds at most S/L + 1 images of an atom of period L, so mu(Q) <= M (S/Lx+1)(S/Ly+1) < S^2. For this object f(10) = 0.98715 < 1. check_a at reach 4, 5, 6, 8 gives 1.710996424554, 1.710996424554, 1.711011823672, 1.711011823672. checkers/third/vsweep.c, which enumerates all tight boxes below S*, gives both a lower and an upper enclosure of the true ratio: [1.71101182367469, 1.71101182367477]. The claim needs only the lower bound.

Exact statement. For the measure in object/measure.json the checkers' value is the rational number in CLAIM.md, a lower bound on the level-set ratio, so c_2 is at least that number.

Sources for the route: Tomar's paper states this reduction as a lemma on periodic measures; Lin's formalization uses the same route. Neither is relied on: the proof above is complete as written.
