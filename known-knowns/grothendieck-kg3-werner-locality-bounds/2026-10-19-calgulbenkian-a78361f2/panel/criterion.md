# criterion, kg8-e8 partial win p2
context: Claude Code subagent, fresh context [Sonnet 5.5]

Literal p2: 'A certified local bound for one of the 2409.03739 heuristic symmetric instances (d in {4,7,8}) that turns their heuristic value into a proven bound, re-checkable in under an hour by an independent exact method.' Only p2 is claimed here; the main criterion (K_G(3) above 1.43670) is not claimed.

What I re-derived myself (own scripts, not the author's):
1. The matrix. I located the 120 x 120 integer block in the MATLAB file (stored as 64-bit integers), confirmed symmetry, diagonal -7, off-diagonals in {-3,0,3}, and that (A+13I)/3 is PSD of rank 8 with diagonal 2 and entries in {0,+-1}: a Gram matrix of 120 norm-2 vectors in R^8 with 56 neighbours per row, i.e. (up to signs and order) the 120 positive roots of E8. So A = D(3G-13I)D.
2. Q. With G the Gram of the roots, sum of r r^T over positive roots is 30 I, so ||G||_F^2 = 7200, tr G = 240 and Q = (3*7200 - 13*240)/2 = 9240. Exact.
3. Upper bound L <= 6104. I re-derived the reduction: L = max_b ||A b||_1 with (Ab)_i = 3ip(r_i,w) - 13 b_i, w = sum b_j r_j; Weyl invariance of ||Ab||_1 under w -> g w (with the induced signed permutation of b); w = 2v with v in the root lattice (parity, E8 unimodular); w lies in the root zonotope whose vertices all have |w|^2 = |2 rho|^2 = 2480, so by convexity |v|^2 <= 620; dominant v = sum c_k omega_k, c_k >= 0 integers. I enumerated these myself from the Cartan matrix: exactly 18454, the same set as the certificate file. For each, I checked in exact integer arithmetic the weak-duality bound D_w(mu) = -ip(w,mu) + sum_i max_s(|3x_i - 13 s| + sip(r_i,mu)) <= 6104 with the supplied mu (the Cartan matrix was rebuilt from the witness file's root set: an E8 diagram, determinant 1, the 120 vectors closed under simple reflections). All 18454 bounds are <= 6104; exactly 2 equal 6104.
4. Lower bound: the supplied sign vector b gives ||A b||_1 = 6104 on the (3G-13I) built from that root set. So L = 6104 exactly and K_G(8) >= 9240/6104 = 165/109.

Clauses:
- A certified local bound for a 2409.03739 heuristic symmetric instance (d=8, m=120, E8): MET. The paper marks 165/109 with an asterisk (heuristic solution of SDP_1); L = 6104 is now proved (the weak-duality certificates are verified exactly; the symmetry steps are standard and I re-derived them).
- Turns the heuristic value into a proven bound: MET. What p2 credits is the proof of L, not the number 165/109, which the paper already prints as heuristic; this is NOT a table improvement and the contributor's 0.0204 gain over 1.49339 is not what is credited.
- Re-checkable in under an hour by an independent exact method: MET (my check runs in seconds; the method is one symmetry-reduction plus dual certificates, not a second algorithm; the bank's example of 'a custom bound with symmetry' covers it). The matrix is the paper authors' own supplementary file; p2 does not require a new instance.
- Open question on rigour: floating-point LPs produced the dual vectors but each is verified exactly, so acceptable; steps on the zonotope and Weyl action are standard.
This does not meet the main criterion and moves no published K_G(3) bound. Whether a newer paper already proves L for this instance (arXiv search) is the novelty skeptic's question; not decidable from the folder.

confirmed_scope: For the paper's d=8 E8 instance (120 x 120 matrix 3G-13I, signs and order arbitrary), the local bound max a^T A b is exactly 6104, so Q/L = 9240/6104 = 165/109 is a proven lower bound for K_G(8); this converts the heuristic value to a proven one (partial win p2) and says nothing about K_G(3).
pass: true
