# Finite hypotheses to check on the table V (stand-alone statement)

Files: `V_b.npy` (float64 little-endian, C order, shape (nt+1, nth)), `V_b.json` (parameters). Read both with your own code.

Exact parameters: T = 501/1000, b = 35/10000, rho_- = 1/sqrt2 - b, rho_+ = 1/sqrt2 + b, beta = -(85/100) i, gamma = 1/2 + (866/1000) i,
L = 8, Lam0 = 5, Lam1 = 10, alpha = 6/5, nt = 1600, nth = 2514, d = L/nt = 1/200, dphi = 2 pi/nth, tau_i = -8 + i d, phi_j = j dphi (periodic in j).

V(tau, phi) is the function that on each cell [tau_i, tau_{i+1}] x [phi_j, phi_{j+1}] is the bilinear interpolant in (tau, phi) of the four table values.
The table entries are exact binary64 numbers. x = e^tau, p(x) = Lam1 x^alpha.

Inside a cell, write V_tau, V_phi for the partial derivatives of that cell's bilinear function.

For rho in [rho_-, rho_+], psi in [0, 2 pi], put w = rho - T e^{i psi}, W = |w|, e = (W - rho^2)^2/(2 rho).

(HJB) For every cell, every (tau, phi) in the closed cell, every rho in [rho_-, rho_+], every psi:

    G := V_tau + (Im w/rho) V_phi + W V - T |w + beta x rho| + 2 rho x Re(gamma beta e^{i phi}) + p(x) e  >= 1e-6.

(INIT) V(tau_0, phi_j) >= T + (T + 2)|beta| e^{-L} for all j.

(TERM) Let m_cert := min over rho in [rho_-, rho_+], psi in [pi, 2 pi] of Re(gamma(T e^{i psi} - beta rho)) + Lam0 e, minus V(0, 0) (table entry V[nt][0]).
Report a certified lower bound for m_cert. It should be above 0.0098.

Also report certified upper bounds for max |V_tau| and max |V_phi| over all cells.

Output: smallest certified lower bound of G found over all cells, the cell attaining it, and pass or fail.
