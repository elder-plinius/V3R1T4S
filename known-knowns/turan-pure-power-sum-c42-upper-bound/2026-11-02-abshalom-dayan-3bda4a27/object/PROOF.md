# Proof that R_n > 501/1000 for every n, hence C_42 >= 501/1000

Label: PROVED-HERE, given the finite hypotheses on the table V, which are checked by the programs in `code/` (see `CERT.md` and `REPRODUCE.md`).

C_42 = limsup R_n, R_n = min max_{1<=k<=n} |z_1^k + ... + z_n^k| over complex z_i with max|z_i| = 1.

Credit: formula (F2) below is formula (14) of G. Biro's 2000 paper (Indag. Math. 11, 343-358). The barrier at rho = 1/sqrt2 that (F1) expresses is the geometry of Biro's argument in that paper. The proof does not use his Lemma 8 or his (38)-(47): it uses one test functional with fixed beta and gamma at each time, and a value function, so it is not an evaluation of his constant.

## 1. Setup

Rotate so that z_1 = 1; the moduli |s_k| do not change. Let s_k = sum z_i^k. Let g(x) = prod_{i>=2}(1 - z_i x) = sum P_m x^m, a polynomial of degree at most n-1, so P_n = 0 and P_0 = 1. Since log g = sum_{k>=1} (1 - s_k) x^k/k, comparing coefficients in x g' = g sum (1 - s_k) x^k gives, for every l >= 1,

    l P_l = M_l - E_l,   M_l := sum_{j<l} P_j,   E_l := sum_{i=1}^l s_i P_{l-i}.     (1.1)

Assume |s_k| <= T for k <= n, where T = 501/1000. The argument below uses only (1.1), P_n = 0 and this bound. Put A_l = sum_{j<l} |P_j| > 0, r_l = M_l/A_l, rho_l = |r_l|, r_l = rho_l e^{i theta_l} when M_l != 0, with theta_{l+1} - theta_l = Arg(r_{l+1}/r_l), h_l = 1/l, w_l = (r_l - E_l/A_l) e^{-i theta_l}, W_l = |w_l|, c_j = M_{j+1}, N_t = sum_{j<t} c_j. Since |E_l| <= T A_l,

    |rho_l - w_l| <= T,  P_l = h_l A_l e^{i theta_l} w_l,  A_{l+1} = A_l (1 + h_l W_l),  c_l = A_l e^{i theta_l} (rho_l + h_l w_l),  rho_1 = 1.

From P_n = 0 and (1.1), M_n = E_n, so rho_n <= T.     (1.2)

Let mu(y) = (T^2 - y^2(1-y^2))/(2y). Since y^2(1-y^2) <= 1/4 < T^2, mu > 0. mu is convex on (0,1], since mu'' = T^2/y^3 + 3y. Let

    e(w,y) = mu(y) + Re w - y|w| = ((|w| - y^2)^2 + T^2 - |y - w|^2)/(2y),

an identity by expanding |y-w|^2. So e >= 0 when |y-w| <= T.

(F1) If r_l != 0: rho_{l+1} - rho_l >= h_l (e_l - mu(rho_l))/(1 + h_l W_l), with e_l = e(w_l, rho_l). Indeed r_{l+1} = (r_l + h_l w_l e^{i theta_l})/(1 + h_l W_l) and |rho + h w| >= rho + h Re w.

(F2) E1_t := sum_{i=1}^t s_i c_{t-i} = 2 N_t - t c_t. Indeed E1_t = sum_{i<=t} E_i (exchange sums), E_i = M_i - i P_i by (1.1), sum_{i<=t} M_i = N_t, and sum_{i<=t} i P_i = t c_t - N_t by Abel summation.

(F3) For complex beta and 1 <= k <= n: E_k + (beta/k) E1_k = sum_{j<k} s_{k-j} (P_j + (beta/k) c_j), so its modulus is at most T sum_{j<k} |P_j + (beta/k) c_j|.

## 2. Constants and hypotheses

T = 501/1000, b = 7/2000, rho_- = 1/sqrt2 - b, rho_+ = 1/sqrt2 + b, beta = -(17/20) i, gamma = 1/2 + (433/500) i (|gamma|^2 = 0.999956 <= 1), L = 8, Lam0 = 5, Lam1 = 10, alpha = 6/5, J0 = 10^6, p(x) = Lam1 x^alpha.

Band: Bd = {(y,w): y in [rho_-, rho_+], |y-w| <= T}. On Bd: |w| <= Wb := rho_+ + T, |w|/y <= Zb := Wb/rho_-, e <= eb := mu_max + Wb(1 + rho_+), where mu_max = max_{[rho_-,rho_+]} mu = mu(rho_-).

V: the function on [-8,0] x R/2 pi Z that is bilinear in (tau,phi) on each cell of the grid tau_i = -8 + i/200 (i = 0..1600), phi_j = 2 pi j/2514, with node values the binary64 numbers in `V_b.npy`. Cells C; V_C is the bilinear function on C. |d_tau V_C| <= L_tau, |d_phi V_C| <= L_phi.

(HJB) For every cell C, (tau,phi) in C, y in [rho_-, rho_+], and w on the circle |y-w| = T, with x = e^tau:

    d_tau V_C + (Im w/y) d_phi V_C + |w| V >= T |w + beta x y| - 2 y x Re(gamma beta e^{i phi}) - p(x) e(w,y).

(INIT) V(-8,phi) >= T + (T+2)|beta| e^{-8} for all phi.

(TERM) For y in [rho_-, rho_+] and w = y - T e^{i psi}, psi in [pi, 2 pi]: Re(gamma(y - w - beta y)) + Lam0 e(w,y) >= V(0,0) + m.

(LATE) Let y_1 = 1, y_{l+1} = y_l - mu(y_l)/l. Then y_l > 0 for all l <= J0, y_{J0} > rho_+, and J0 >= 2 Zb + 2.

Derived constants: C0 := L_tau/2 + L_phi Zb^2 + Wb(L_tau + L_phi Zb) + T|beta|rho_+ + 2|beta|rho_+(1+Zb) + (T+2)|beta|Wb + 2 alpha Lam1 eb; eps1 := (2 C0 + 2 L_tau + (T+2)|beta| + |beta|Wb)/J0; C' := Lam0 + Lam1/alpha = 40/3; eta' := (m - eps1)/C'; 2b' := 2b - mu(rho_+)/J0; varpi := Wb/J0.

(GAP) eta' > (1 + varpi) mu_max, and 2b' > mu_max (L + 1/J0).

**Theorem.** Under these hypotheses, every tuple has max_{k<=n}|s_k| > 501/1000. So R_n > 501/1000 for every n, and C_42 >= 501/1000.

## 3. Lemma R (ray lemma)

Fix y > T, reals a0, a1, a2, a3 and complex c. Let G(w) = a0 + a1 Im w + a2 |w| + a3 Re w - T|w + c|. The minimum of G on the disc |y-w| <= T is attained on the circle. If the last term is absent, the minimum on the upper half disc {|y-w| <= T, Im w >= 0} is attained on the upper arc.

Proof. Since y > T, w = 0 is outside the closed disc. Take w in the disc, omega = w/|w|. On the ray s -> s omega, s > 0, the first four terms are affine in s and -T|s omega + c| is concave. The ray meets the disc in a closed segment with both ends on the circle, and a concave function on a segment is at least the smaller of its end values. Upper half disc: if Im w > 0 the whole segment has Im > 0, so both ends lie on the upper arc. If Im w = 0 then omega = 1 and the ends are y - T and y + T, which are psi = 2 pi and psi = pi. QED.

Use: at fixed (tau,phi,y) the (HJB) difference has this form with a2 = V - p y, a3 = p, because e = mu + Re w - y|w|. So (HJB) holds on the whole disc, for any sign of a2. The (TERM) expression has the affine form, so (TERM) holds on the upper half disc.

## 4. Lemma A (path lemma)

Let g: [0,1] -> [-8,0] x R/2 pi Z be Lipschitz. For almost every s there is a cell C with g(s) in C and (V o g)'(s) = grad V_C(g(s)) . g'(s).

Proof. V o g is Lipschitz, so differentiable almost everywhere. For each C, T_C = g^{-1}(C) is closed, and almost every point of T_C is an accumulation point of T_C at which V o g and g are differentiable. Along T_C, V = V_C, so the limit of difference quotients is grad V_C . g'. Finitely many T_C cover [0,1]; when several cells qualify, take the one of lowest index, so the choice is measurable. QED.

## 5. Lemma B (one discrete step)

Fix k, j with J0 <= j < k and (rho_j, w_j) in Bd. Put x_j = j/k, tau_j = log x_j, phi_j = theta_j - theta_k, V_j = V(tau_j, phi_j), R_j = T|w_j + beta x_j rho_j| - 2 rho_j x_j Re(gamma beta e^{i phi_j}), assuming tau_j >= -8. Then

    A_{j+1} V_{j+1} - A_j V_j >= h_j A_j (R_j - p(x_j) e_j) - h_j^2 A_j (C0 - (T+2)|beta|Wb).     (B)

Proof. Let h = h_j, z = h w_j/rho_j; |z| <= h Zb <= 1/2. Delta tau = log(1+h), |Delta tau - h| <= h^2/2. Delta phi = Arg(1+z), |Delta phi| <= h Zb (since Arg(1+z) is at most |z| in modulus for Re z >= 0, and Re w_j >= rho_j - T > 0), |Delta phi - Im z| <= |log(1+z) - z| <= |z|^2. Let g(s) = (tau_j + s Delta tau, phi_j + s Delta phi), a = Im w_j/rho_j. By Lemma A,

    V_{j+1} - V_j = int_0^1 (Delta tau d_tau V_C + Delta phi d_phi V_C)(g(s)) ds >= h int_0^1 (d_tau V_C + a d_phi V_C)(g(s)) ds - h^2 (L_tau/2 + L_phi Zb^2).

Apply (HJB) on the disc at g(s) with (y,w) = (rho_j, w_j). With x_s = e^{tau(s)}: |x_s - x_j| <= 1/k <= h, |phi_s - phi_j| <= h Zb, p(x_s) <= p(x_j) + 2 alpha h Lam1 (since x_{j+1} <= 1 and alpha h <= 1). So

    T|w + beta x_s y| >= T|w + beta x_j y| - T|beta| y h,
    2 y x_s Re(gamma beta e^{i phi_s}) <= 2 y x_j Re(gamma beta e^{i phi_j}) + 2 y |beta| h (1 + Zb),
    p(x_s) e <= p(x_j) e + 2 alpha h Lam1 eb.

Finally A_{j+1}V_{j+1} - A_j V_j = A_j [V_{j+1} - V_j + h W_j V_{j+1}] and |V_{j+1} - V(g(s))| <= h(L_tau + L_phi Zb). Collecting the terms gives (B). QED.

## 6. Proof of the Theorem

Suppose |s_k| <= T for all k <= n.

**Step 1: late entry.** Note rho_l <= 1 because |M_l| <= A_l. The map y -> y - h mu(y) is nondecreasing on (0,1] for h <= 1, since mu'(y) = 2y^2 - 1 - mu/y <= 1. Since mu > 0, y_l is decreasing while positive, so by (LATE) y_l is in (rho_+, 1] for l <= J0. We show rho_l >= y_l for l <= min(n, J0), by induction, starting from rho_1 = y_1 = 1. If l < min(n, J0) and rho_l >= y_l > rho_+, then r_l != 0, so (F1) and e >= 0 give rho_{l+1} >= rho_l - h_l mu(rho_l) >= y_l - h_l mu(y_l) = y_{l+1}. So rho_l > rho_+ for l <= min(n, J0). By (1.2), rho_n <= T < rho_-, so n > J0. Let B be the first index with rho_B < rho_-, A the last index below B with rho_A > rho_+. Then B > A >= J0. Let l0 = A + 1. Monotonicity gives rho_{l0} >= rho_+ - mu(rho_+)/A > rho_-. For l0 <= l < B, rho_l is in [rho_-, rho_+].

**Step 2: one time k.** Take k with l0 e^8 <= k <= B - 1, j0 = ceil(k e^{-8}), so j0 >= l0 > J0. If Im w_k < 0, replace every s_i by its conjugate: (1.1) conjugates, and rho, W, A, e are unchanged, so the inequality (D) below is unaffected. So assume Im w_k >= 0.

Multiply (F3) by gamma e^{-i theta_k}, take real parts, and use |gamma| <= 1 and (F2):

    Re(gamma e^{-i theta_k}(E_k - beta c_k)) <= sum_{j<k} R*_j,   R*_j := T|P_j + (beta/k) c_j| - (2/k) Re(gamma e^{-i theta_k} beta c_j).

Left side: E_k = A_k e^{i theta_k}(rho_k - w_k) and c_k = A_k e^{i theta_k}(rho_k + h_k w_k), so it is at least A_k Re(gamma(rho_k - w_k - beta rho_k)) - A_k |beta| Wb/k.

Early terms, j < j0: |c_j| <= A_{j+1} <= A_{j0} and sum_{j<j0}|P_j| = A_{j0}, so sum_{j<j0} R*_j <= A_{j0}(T + (T+2)|beta| j0/k), with j0/k <= e^{-8} + 1/k. By (INIT) and tau_{j0} + 8 <= e^8/k <= 1/(j0 - 1) <= 2/j0, this is at most A_{j0}[V_{j0} + (2 L_tau + (T+2)|beta|)/j0].

Late terms, j0 <= j < k: P_j + (beta/k) c_j = h_j A_j e^{i theta_j}(w_j + beta x_j(rho_j + h_j w_j)), so R*_j <= h_j A_j R_j + h_j^2 A_j (T+2)|beta| Wb. By (B), R*_j <= A_{j+1}V_{j+1} - A_j V_j + h_j A_j p(x_j) e_j + h_j^2 A_j C0.

Add and telescope. A_{j0}V_{j0} cancels, so the sign of V is not used; tau_k = 0 and phi_k = 0. Divide by A_k, use A_j <= A_k on the nonnegative terms and sum_{j>=j0} h_j^2 <= 2/j0:

    Re(gamma(rho_k - w_k - beta rho_k)) <= V(0,0) + sum_{j0<=j<k} h_j p(j/k) e_j + eps1.

With (TERM) on the upper half disc:

    m - eps1 <= Lam0 e_k + sum_{j0<=j<k} h_j p(j/k) e_j.     (D)

**Step 3: sum over k.** Let S = sum_{l0<=l<B} h_l and K = {k: l0 e^8 <= k <= B-1}. Then S_K := sum_K h_k >= S - 8 - 1/l0. Multiply (D) by h_k and sum over K (if K is empty, S_K = 0 and the next inequality is trivial). Since e_j >= 0, the sums exchange, and sum_{k>j} (1/k)(j/k)^alpha <= int_j^infty j^alpha t^{-1-alpha} dt = 1/alpha, so

    (m - eps1) S_K <= C' sum_{l0<=j<B} h_j e_j.

**Step 4: crossing.** Sum (F1) on l0 <= l < B: sum h_l e_l/(1 + h_l W_l) <= rho_B - rho_{l0} + mu_max S <= -2b' + mu_max S, and 1 + h_l W_l <= 1 + varpi. Therefore

    eta'(S - 8 - 1/J0) <= (1 + varpi)(mu_max S - 2b').     (X)

Since e >= 0, also mu_max S >= 2b'. Define f(S) = eta'(S - 8 - 1/J0) - (1 + varpi)(mu_max S - 2b'). By (GAP) f has positive slope, and f(2b'/mu_max) = eta'(2b'/mu_max - 8 - 1/J0) > 0. So f(S) > 0 for every S >= 2b'/mu_max, which contradicts (X). QED.

## 7. Where the hypotheses are checked

| Hypothesis | Program | Method |
|---|---|---|
| (HJB) | `code/check_hjb.py`, `code/check2.c` | see `CERT.md` |
| (INIT), (TERM), Lipschitz bounds | `code/check_hjb.py`, `code/check2.c`, `code/late_gap.py` | |
| (LATE), (GAP), J0 >= 2 Zb + 2 | `code/late_gap.py` | Arb, and exact integers for (LATE) |

Values from `logs/late_gap.txt` and `logs/check2_full.out`: L_tau <= 0.97226858, L_phi <= 0.75338514, C0 <= 61.3960103, eps1 <= 0.00012790, m >= 0.0146231. Then eta' >= 0.00108714, mu_max <= 0.00072866, eta' - (1+varpi) mu_max >= 0.00035848, 2b' - mu_max(L + 1/J0) >= 0.00117072. (GAP) needs m >= 0.00984336 with these constants. Since eta' > 0, the case distinctions in Steps 3 and 4 are as written.
