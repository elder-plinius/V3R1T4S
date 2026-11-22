# PROOF: rigorous bounds for the monomer-dimer entropy h2 of the square lattice

Z(a,b) = number of matchings (all subsets of pairwise disjoint edges, the empty set included) of the a x b grid graph (free boundary).
h := sup_{a,b} ln Z(a,b)/(ab).  We show h = lim ln Z(a,b)/(ab) (so h = h2) and prove

  (U)  h <= (ln beta(M))/M                          for every even M >= 4,
  (L)  p h >= ln beta(p+2q) - ln beta(2q)           for all integers q >= 2, p >= 1,

where beta(m) is the spectral radius of the matrix P_m defined below.  The checker applies (U) with M = 22 and (L) with q = 11, p = 2.

## 0. Definitions
For m >= 3 let P_m be the 2^m x 2^m matrix indexed by subsets s,t of Z_m (cyclic row of m sites):
P_m[s,t] = 0 if s and t intersect, otherwise the number of matchings of the subgraph of the m-cycle induced on the sites outside s u t.
P_m is symmetric with nonnegative integer entries. beta(m) := rho(P_m).

## 1. Facts
(F1) A subgraph has at most as many matchings as the graph.  (F2) Matchings of a disjoint union multiply.
(F3) Z(a1+a2,b) >= Z(a1,b) Z(a2,b) (delete the edges between rows a1 and a1+1; apply F1, F2); same in the other index. Hence ln Z is superadditive in each index.
(F4) Z(a,b) <= 5^(ab), so h < infinity.
Claim 1. For fixed b, g_b := lim_a ln Z(a,b)/a exists and equals sup_a (Fekete); g_{b1+b2} >= g_{b1}+g_{b2} (F3); g_b <= hb; and
g_b/b -> h. Proof: for fixed (a0,b0), tiling gives ln Z(a,b) >= floor(a/a0)floor(b/b0) ln Z(a0,b0) (leftover vertices unmatched), so
liminf ln Z(a,b)/(ab) >= ln Z(a0,b0)/(a0 b0); take sup. Likewise g_b >= floor(b/b0) g_{b0} gives liminf g_b/b >= g_{b0}/b0 >= ln Z(a0,b0)/(a0b0). QED.

## 2. Transfer matrix identity
For m,L >= 3: Tr P_m^L = number of matchings of the torus C_m x C_L (a simple graph), and (P_m^L)[{}, {}] = matchings of the cylinder C_m x P_L.
Proof: for a matching, let s_r be the set of columns whose vertical edge between row r and r+1 is used. The horizontal edges used in row r form a
matching of the induced subgraph of the cycle on the columns not in s_{r-1} u s_r, and s_{r-1}, s_r are disjoint; conversely every such choice is a matching.
So the count is the sum over (s_r) of prod_r P_m[s_{r-1}, s_r]. Consequently Tr P_m^L = Tr P_L^m (same torus).

## 3. Spectral facts (B real symmetric, nonnegative, 2^m x 2^m, rho = spectral radius = largest eigenvalue, |lambda_i| <= rho)
(S1) Tr B^L >= rho^L for L even.  (S2) Tr B^L <= 2^m rho^L.  (S3) Tr B^{p+2q} <= rho^p Tr B^{2q} (p >= 0, q >= 1): sum lambda^{p+2q} <= sum |lambda|^p lambda^{2q}.
(S4) Collatz-Wielandt: for B >= 0 and a vector x with all entries > 0, min_i (Bx)_i/x_i <= rho(B) <= max_i (Bx)_i/x_i.
 Upper: rho(B) = rho(D^-1 B D), D = diag(x); this matrix has row sums (Bx)_i/x_i and rho <= max row sum.
 Lower (B symmetric): take v >= 0, v != 0, Bv = rho v; then rho v.x = v.Bx >= (min ratio) v.x and v.x > 0.
(S5) 0 <= A <= B entrywise implies rho(A) <= rho(B).

## 4. beta(m)^(1/m) -> e^h
Let A_m be the analogue of P_m for the open row (path). Z(L,m) = (A_m^L)[{},{}] <= alpha^L, alpha = rho(A_m). Conversely a Perron vector v >= 0 has v_{} > 0
(alpha v_{} = sum_t A[{},t] v_t > 0 as A[{},t] >= 1), and for even L (A^L)[{},{}] = sum lambda_k^L u_k[{}]^2 >= alpha^L v_{}^2, where u_k is an orthonormal eigenbasis with u_1 = v, so v is the Perron vector normalised to unit Euclidean length (otherwise read v_{}^2 / |v|^2). Hence alpha = lim Z(L,m)^(1/L) = e^{g_m}
and (ln alpha(m))/m -> h (Claim 1). Also A_m <= P_m so alpha <= beta (S5).
Upper: for even L >= 4, beta(m)^L <= Tr P_m^L (S1) = #matchings of torus <= 2^(m+L) Z(m,L) (a torus matching is a grid matching plus a subset of the m+L wrap edges) <= 2^(m+L) e^{hmL}.
Letting L -> infinity (even): ln beta(m)/m <= h + ln2/m. Together: lim_m ln beta(m)/m = h.

## 5. Proof of (U)
Let M >= 4 be even and m >= 3 arbitrary. By section 2, Tr P_m^M = Tr P_M^m. By (S1) (M even) the left side is >= beta(m)^M; by (S2) the right side is <= 2^M beta(M)^m.
So ln beta(m)/m <= ln 2/m + ln beta(M)/M. Let m -> infinity (section 4). QED.

## 6. Proof of (L)
Let q >= 2, p >= 1, m >= 3. By (S3), beta(m)^p >= Tr P_m^{p+2q} / Tr P_m^{2q}. Both exponents are >= 3, so section 2 gives Tr P_m^n = Tr P_n^m for n = p+2q and n = 2q.
Take m even: (S1) gives Tr P_{p+2q}^m >= beta(p+2q)^m and (S2) gives Tr P_{2q}^m <= 2^{2q} beta(2q)^m. Hence beta(m)^p >= 2^{-2q} (beta(p+2q)/beta(2q))^m.
Apply (1/m) ln and let m -> infinity along even m: p h >= ln beta(p+2q) - ln beta(2q). QED.

## 7. Hypotheses, summarized
P_n is real symmetric and nonnegative (S1-S5 apply). Torus identity needs all cycle lengths >= 3 (here 2q >= 4, p+2q >= 5). U needs M even. L needs m even in the limit only; p and p+2q may have any parity.
Bounds on beta: with an integer vector x > 0, (S4) gives lo = min y_i/x_i <= beta <= max y_i/x_i = up, y = P x computed exactly. Then
h <= ln(up_M)/M and h >= (ln(lo_{p+2q}) - ln(up_{2q}))/p. The checker does exactly this with M = 22, 2q = 22, p = 2 (vectors at widths 22 and 24).
Symmetry shortcut: P_m commutes with the dihedral group of the m-cycle (rotations and the reflection act on subsets s, and P_m[s,t] depends only on s u t and s n t = {}),
so if x is invariant then so is y = Px, and the extremal ratios may be taken over one representative per orbit; the checker stores x only on orbit representatives and expands it.
