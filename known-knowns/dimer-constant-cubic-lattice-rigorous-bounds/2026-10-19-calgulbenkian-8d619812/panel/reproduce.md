context: Claude Code subagent, fresh context [Claude Sonnet 5.5]

# reproduce: cubic-dimer-l3-ub-55 (main win, l3 <= 0.4520095976)

Scope: I judged only whether the saved object reproduces the claimed number and whether the written derivation is a correct proof. Novelty and the criterion text are for the other skeptics. Network was not used.

## 0. Integrity
The contributor's hash list verified from the package folder: every file OK (no failures printed). The three certificate parts concatenate to a file with sha256 8d6198121bb490e8f44f352114144556fd75cc33aa98b4f698335ca274342661, equal to the whole-file hash in object/PARTS.sha256. Work was done in a private copy; my code is not shipped in this package.

## 1. Definition (quoted from object/DERIVATION.md, He's Section 2)
"A[u,v] = 1 iff v - u in {(0,0),(1,0),(0,1)}" on V = Z/m x Z/n; "T[U,V] := per A[U, V \ V'] if |U|+|V'| = mn, else 0". Collatz-Wielandt: for nonnegative A and positive x, rho(A) <= max_u (Ax)_u / x_u. Claimed chain: l3 <= (1/25) log rho(T_{5,5}) = (1/50) max_i log rho(X_i Y_i) <= (1/50) log (max ratio), maximised over sectors i = 0..12.

## 2. My own checker (written before opening verify-it-yourself/)
My own program (not shipped in this package; C, pthreads, 12 threads, 256-bit unsigned integers). It builds from the definition: the layer Z/5 x Z/5 (vertex = 5*x+y, bit v of the mask); the group K of automorphisms phi of Z/5 x Z/5 (images of the two generators, bijective, phi(D) a translate of D) giving |K| = 6 and |G| = 150 with action v -> u + phi(v); orbit representatives (minimum mask) of i-subsets and (25-i)-subsets; and X, Y as sums over all injective forward maps found by depth-first search (no use of any symmetry in the count itself). (XYx)(U) = sum over injections f: U -> V, f(u)-u in D, of (Yx)(orbit of V minus f(U)), and Y the same with sizes swapped. Orbit sums are taken from the representative (property C); I spot-tested property C on 300 random orbit members per run (0 failures in every run). All ratio comparisons and the maximum are done by Python integer cross-multiplication (two small Python scripts of mine, not shipped); log and rounding with mpmath at 60 digits.

Run on the shipped sector-12 vector (parts concatenated, columns id/mask/x only, so Argon's listed (Tx) column was not an input):
  (own program, run on the shipped sector-12 vector with arguments 5 5 12 0 12; 11 s wall)
  (own Python script on that output; its output follows):
  order/mask/x mismatches vs file: 0
  author's listed (T x)_u equals my recomputed (XYx)_u for rows: 35070 of 35070
  all x positive: True
  max ratio (mine): 68004910275217693829986 / 10405826313374  at mask 32739 orbit 53
  claimed 68004910275217693829986/10405826313374 equal: True
  bound sector12 = 0.452009597554481  ceil10= 0.4520095976  ceil6= 0.45201
My orbit set equals the file's: 35070 orbits, identical canonical masks in identical order.

Sectors 0..11 (builder vectors; output of my own script, not shipped), all 12 checked by me, not a sample:
  sector 11: 282404744906972997897/49494065286 -> 0.449295087507 (30064 orbits)
  sector 10: 301133314805378772813/69324082204 -> 0.443840531152 (22108)
  sector 9: 363203564097052574687/126318622370 -> 0.435588436653 (13868)
  sectors 8..0: 0.424439601996, 0.410240592489, 0.392766187734, 0.37169121726, 0.346540901492, 0.316594829546, 0.28067583544, 0.236587252374, 0.17877850544 (sector 0)
  max over sectors 0..11 = 0.449295087507 < sector 12.
So the maximum over the 13 sectors is sector 12: 0.452009597554. Every vector entry is a positive integer. As an extra, from the all-ones vector my code gives sector 12 at p=2: 0.452129162602 (He's own figure), so the converged vector is a genuine improvement on his iterate, not an artefact.

Rounding: exact value 0.452009597554481; rounded up to ten places 0.4520095976, to six places 0.452010. Both claimed figures are rounded outward (up). Margin to He's 0.452130: 1.204e-4 (> 1e-6).

## 3. Author's script
sh verify-it-yourself/run_checks.sh (CW_PROCS=12; the C stage used the script's default of all cores, 28 threads, for about a minute, over my 12-thread allowance; noted). Its output (not shipped separately) ends "ALL CHECKS PASS", sector-12 ratio identical to mine, "PASS C implementation, all 13 sectors: maximum 0.4520095976 in sector 12". No disagreement with my checker.

## 4. Proof steps re-derived (the bound is valid)
(a) Quotient graph. Lambda = <m(e1-e3), n(e2-e3), l e3>. The map x -> (x1 mod m, x2 mod n, x1+x2+x3 mod l) is a surjective homomorphism onto Z/m x Z/n x Z/l whose kernel is exactly Lambda (solve x1 = ma, x2 = nb, x3 = lc - ma - nb), so it is an isomorphism, and the up-edges from (a,b,s) go to (a,b,s+1), (a+1,b,s+1), (a,b+1,s+1), i.e. the offsets D. For m,n >= 2 and even l >= 4 the six neighbours are distinct (up and down neighbours differ in height; the three up ones differ in the layer), so the graph is simple, 6-regular; heights alternate in parity (l even) so it is bipartite.
(b) Trace identity: a perfect matching is a cyclic sequence of "matched-upward" sets with |U|+|W| = mn and T[U,W] ways between layers, so pm = tr(T^l). I did not rely on the author's code: my own script (not shipped) builds the quotient by triangular reduction of Z^d modulo the lattice, counts perfect matchings of the bipartite quotient by the Ryser permanent formula, and compares with tr(T^l) from a matrix I built from the definition: (2,2,4): 4752 = 4752; (3,2,4): 194244 = 194244; (2,2,6): 190992 = 190992 (its output is not shipped).
(c) 2-lifts: Lambda for (2m, n, l), (m, 2n, l), (m, n, 2l) has index 2 in Lambda for (m,n,l), so the identity on Z^3 gives a 2-to-1 covering that is bijective on neighbourhoods. The inequality pm(H) <= pm(G)^2 for a 2-lift H of a bipartite G is Csikvari's (J. Eur. Math. Soc. 2017), cited by He as his Theorem 2.4; I could not fetch it (no network) so I take it as a citation, not a re-derivation. Numeric sanity on actual graphs (same script): total-matching counts Phi satisfy Phi(T_{4,2,4}) = 87631492737 <= Phi(T_{2,2,4})^2 = 93822753025, and likewise for l = 8.
(d) Box in torus: with L = 2^p, M = 2^p m dividing, M e3 lies in <L e3>, so M(e1-e3) gives M e1 in Lambda and Lambda(2^p m, 2^p n, 2^p) = <2^p m e1, 2^p n e2, 2^p e3> is rectangular; the box is a spanning subgraph of the torus (sides >= 8), so f(box) <= pm(torus) <= pm(T_{m,n,2^p})^{4^p} = tr(T^{2^p})^{4^p} <= (2^{mn} rho^{2^p})^{4^p}. Dividing log by volume 2^{3p} mn and letting p -> infinity gives l3 <= (1/mn) log rho(T). No inequality is reversed.
(e) Compression: with property C (verified numerically here and provable from phi(D) = s + D: g(v)=u+phi(v) maps edges with difference in D to edges with difference in s+D, and g_*(w) = g(w) - s is in G), T P = P T-hat for the orbit indicator matrix P. Then T^k 1 = P T-hat^k 1 gives ||T^k||_inf <= ||T-hat^k||_inf, so rho(T) <= rho(T-hat) (the converse inequality is not needed). T-hat sends size-k orbits to size-(25-k) orbits, so T-hat^2 is block diagonal with blocks X_i Y_i and Y_i X_i (i = 0..12 covers all sizes 0..25), and rho(T-hat)^2 = max_i rho(X_i Y_i). Collatz-Wielandt for the nonnegative X_i Y_i and the positive integer vector gives the stated bound. The factor: l3 <= (1/25) log rho(T-hat) = (1/50) log rho(T-hat^2) <= (1/50) log(max ratio). My code uses exactly this.
Remaining reliance: (i) Csikvari's lemma as cited; (ii) Hammersley's existence of the limit defining l3; both are published and standard. I find no gap.

## 5. Open questions of the claim record (not shipped) that concern reproduction
Q3 (13 sectors on builder vectors): I checked all 12 builder vectors exactly myself; each ratio gives a bound at most 0.449295088, so the maximum is sector 12. Accepted. Orbit counts: my rebuilt counts are 35070 (sector 12) and 30064 (sector 11), agreeing with the folder's rebuilt figures; Argon's RESULTS.md sector-11 count 29,828 and its p=2 value 0.4491342670 are wrong, as the folder says (exact p=2 value from my run: 0.449397508943). This does not touch the claim, which uses the exact recomputation. Q4: hypotheses met (nonnegative matrix, positive vector, plain Collatz-Wielandt, no positive-diagonal needed). Q5: |G| = 150 confirmed (|K| = 6). Q1 and Q2 (novelty) are not my role.

Mismatch count: 0. Non-determinism: none seen (repeated runs identical).
pass: true
