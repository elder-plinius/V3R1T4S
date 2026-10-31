# Criterion skeptic report (CriterionA) — claim/ (bound 1 - 1.0215562e-15)

context: subagent

confirmed_scope: Conditional on GEK's published Lemma 3.3 (the wedge-area minimiser W*), Lemma 3.5 and the Lemma 4.2 nested-ball construction, and on Arb (python-flint 0.9.0) being correct, every packing of congruent regular tetrahedra has limsup density at most 1 - 1.0215562e-15, with the argument re-executed and reconciled with the written reduction but not machine-checked in a proof assistant.

## What I did
- Fetched the GEK paper once (https://arxiv.org/pdf/1008.2830) and compared its statements with REDUCTION.md K1-K5.
- Re-ran from a fresh copy: `rig_dp.py 150`, `scheme.py 40`, `verify_final.py` (python-flint 0.9.0 / Arb, 160 bit). Output reproduced exactly: 155 states directly verified, 0 closure-justified; rho(0,5) >= 8.619948e-12; rho(0,40) >= 3.636896e-12; scheme Q=40, k=38, u=0.0084, q=5, q_v=9, m=2, m_v=3, 120 good centres per tetrahedron, Delta=8; b >= 1.021556e-15; deficit >= 1.0215562e-15.
- Wrote my own float re-implementation of the recursion from the text of REDUCTION.md (R1 root solve, R2 ordering/infeasibility, monotone closure) using scipy quadrature. It gives rho(1,2)=2.984e-3, rho(1,4)=1.2105e-7, rho(0,5)=8.654e-12, rho(0,6..40)=3.651e-12. These agree with the certified values (the certified ones are a few 1e-3 relative lower), so the code matches the written reduction.
- Hand-checked the arithmetic of b: (120/9)(4pi/3)/v_t · u³ · rho = 1.0217e-15.

## Checks of the new lemmas
- Lemma V (wedge volume <= alpha + E(e)): I re-derived the slab argument. For c not interior, one half-space has offset s1<=0, the wedge sits in W' with s1=0, the slab thickness is |s2|<=e, and the slice is a disc minus a segment of area R²(pi - arccos y + y sqrt(1-y²)), y = x cot(theta)/R. The argument is correct, and E_up is a ball-enclosure Riemann upper sum, which is sound. MC test on 2735 random wedges (c not interior): no violation beyond noise (max excess -8e-4).
- Lemma A (several caps, F = 1 - alpha - sqrt2/(3 pi)): slice argument and convexity-vertex argument re-derived. Correct.
- Lemma R (R1/R2/R3): I re-derived the logic, including edge cases (absent objects, u_k>1, ties, e>=1 giving the cap value, wedge->cap monotonicity under the partial order). It is sound. The Arb code only ever subtracts upper bounds or adds lower bounds, and `arb(mid, rad)` rounds the radius up, which I tested.
- K1 exact area a(r): I checked numerically (3e6-point sphere lattice, all bisector angles) that the minimum wedge area at edge distance r is attained at the flush wedge and equals the closed form (r=.1,.3,.6,.85 agree to 3e-6 relative) and that random non-flush wedges never undercut a(dist). GEK's appendix proves "minimum = W*" with the Gauss-Bonnet area, so the exact a(r) is GEK's own quantity; the Taylor polynomial in Lemma 3.3 is only a weakening.
- K4 (GEK Lemma 3.5): 2e5 random placements, no case of a ball with radius sqrt2/3 * (min vertex distance) meeting 3 faces.
- Counting scheme (Claims 1-3, independent set, boundary): re-derived. Key points checked: K5 distance t*sqrt(2/3); ball inclusion B(c,R1) in B(c'',sqrt(2/3)d); only wedge-type objects enter the K2 count (the tetrahedron holding a vertex near c is not counted and need not be); 2 centres per edge in an open interval of length 2*sigma; same-tetrahedron centres never conflict; m_v = floor(2 r_v/sigma)+1 = 3; cube-boundary argument is uniform in the packing (O(L²) layer), so the limsup density is bounded for any packing, not only periodic.

## Proved vs imported vs numeric
- Proved in the reduction (and checked by me): Lemma V, Lemma A, Lemma R, Claims 1-3, boundary argument, base values.
- Imported from GEK (published, proof by GEK in text or appendix, not re-proved): K1 (planar minimisation), K2 (Cor 3.4 mechanism, now with q up to 40 and the exact a), K3 (the Lemma 4.2 construction; the profile recursion uses its defining properties — wedges with edge in the open ball stay wedges, other objects become caps, contained objects deleted — which are in GEK's construction text, though GEK only display the weaker K(c-1,w) ∪ K(c+1,w-1) conclusion), K4 (Lemma 3.5, constant 3/sqrt2).
- Numeric only (not in the proof): MC checks, differential evolution, float prototypes.

## Residual weaknesses (not fatal under the criterion as worded)
- Not machine-checked; Arb trusted. Two comparisons use `float(x.lower())` (nearest-double rounding), which could move a bound by ~1e-16 relative; the certified margins are ~1e-6 relative, so this is cosmetic.
- K1, K3 and K4 rest on GEK's sketch-level proofs ("an exercise in planar geometry", the cap-enlargement non-overlap step). The result is exactly as rigorous as GEK's own 2.6e-25 bound on these points and no more.
- The gain over GEK (about 4e9) comes from (i) exact area/volume functions (GEK say in their conclusion that such improvements are straightforward), (ii) the profile recursion, (iii) a counting scheme with larger deficit balls (Q=40). I found no flaw in any of these.
- I did not search the literature for a published result that subsumes this; the Wikipedia status in CLAIM.md still lists GEK as the record.

pass: true
