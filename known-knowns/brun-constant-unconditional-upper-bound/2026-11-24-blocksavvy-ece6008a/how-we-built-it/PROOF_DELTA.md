# Proof delta against submission 2026-11-24-blocksavvy-e6b84d42 (B < 2.126988 under GRH)

Base: the e6b84d42 proof (reproduced verbatim below section R in PROOF.md, sections A, B, S, C, D, E, F; its post-panel errata included).
This claim changes exactly ONE step, the bound for the Selberg remainder in the intervals whose sieve level z_i is at most 20000 (22 of
the 9906 intervals, the first 22). Every other interval term's FORMULA, the head, the tail, the GRH constant, c1, V(z), W(z) and the pi_2(z)
correction are unchanged; but the z_i of all intervals were re-chosen by the optimiser, so the other 9884 terms differ numerically
(+7.6e-9 in total, see R4) [post-panel erratum (b)].

## R. Change (R): per-modulus combination of the Selberg remainder (NEW)

### R1. Signed remainder (KNOWN; Klyve thesis 2007, Theorem 5.4 proof, the display before (5.16) and (5.13), p.117)
For real lambda_d with lambda_1 = 1, lambda_d = 0 for d > z (d | P_z), Klyve's proof gives the chain
  S(A,P,z) <= sum_{a in A} ( sum_{d | (a, P_z)} lambda_d )^2 = sum_{d1,d2 <= z, d_i | P_z} lambda_d1 lambda_d2 #A_[d1,d2],
and (5.13) defines R_d by #A_d = X/f(d) + R_d for every d | P_z. Substituting (an equality, no absolute values yet):
  S(A,P,z) <= X sum lambda_d1 lambda_d2 / f([d1,d2]) + sum_{d1,d2} lambda_d1 lambda_d2 R_[d1,d2].
Klyve's printed (5.16) then puts absolute values on the second sum (its "=" is a slip for "<="); Dunn's Theorem 2.2 and claim S
bound it by (sum |lambda_d|)^2 max_q |R_q| = Lambda(z)^2 max_q |R_q|.

### R2. Grouping by modulus (KNOWN, standard rearrangement; applied numerically to Brun's constant here for the first time as far as the
panel's search found) [post-panel erratum (a)]
Credit: this is the standard upper-bound-sieve form of Selberg's sieve, e.g. Tao, 254A Notes 4 "Some sieve theory" (2015), eq. (28):
lambda+_d := sum_{[d1,d2]=d} rho_d1 rho_d2 are upper-bound sieve coefficients, with remainder sum_d |lambda+_d| |r_d|; Vaughan's notes on
Selberg's sieve (https://personal.science.psu.edu/rcv4/Selberg.pdf) keep the signed remainder sum lambda_d lambda_e R_[d,e]. Neither Klyve
(5.16) nor Dunn (Theorem 2.1, code r = M(z)) uses it; both bound each pair separately.
Each pair (d1, d2) has q = [d1, d2] odd squarefree with q | P_z and q <= z^2. Grouping the second sum by q:
  sum_{d1,d2} lambda_d1 lambda_d2 R_[d1,d2] = sum_q rho_q R_q,   rho_q := sum_{[d1,d2] = q} lambda_d1 lambda_d2,
so |.| <= Sigma(z) max_{q <= z^2, q | P_z} |R_q| with Sigma(z) := sum_q |rho_q| <= sum_q sum_{[d1,d2]=q} |lambda_d1 lambda_d2| = Lambda(z)^2.
In Dunn's setting R_q = E(x; q, -2) = pi(x; q, -2) - li(x)/phi(q) (claim S1, A) for q > 1; for q = 1 the set A excludes p = 2, so
R_1 = E(x; 1) - 1 [post-panel erratum (c): inherited from Dunn; |R_1| <= |E(x;1)| + 1 and the extra 1 is far inside the
slack of the GRH bound sqrt(x) log x K(x) at x >= 4e18, as in the base claim], and the GRH bound for max_q |E(x;q)| used in the
e6b84d42 proof (Grenie-Molteni, section B, uniform over q <= z_i^2 through lambda_i = min(1/2, 2 log z_i / log m_i)) applies
unchanged. Hence, in section A's interval term, r(z_i)^2 may be replaced by any certified upper bound for Sigma(z_i) instead of
Lambda(z_i)^2. The main term X/V(z) is untouched (same weights). The pi_2(z) correction and the partial summation of Dunn's Lemma
3.1 are linear in the per-x sieve bound and do not see the change.
Since lambda_d depends on z only through n = floor(z) (all sums run over integers <= z), Sigma(z) = Sigma(floor z).

### R3. Certified upper bound for Sigma(n), n <= 20000 (PROVED-HERE + exact computation)
lambda_d = mu(d) prod_{p|d}(p-1)/(p-2) G_d(n/d)/V(n), G_d(y) = sum_{t <= y, t odd squarefree, (t,d) = 1} prod_{p|t} 1/(p-2) (claim S1,
Klyve (5.24)-(5.26)). Author's program (code/lamfx.py): every lambda_d as an EXACT rational (python-flint fmpq), then
L_d = round(2^40 lambda_d) exactly, so |2^40 lambda_d - L_d| <= 1/2. code/rhofx.c computes P_q = sum_{[a,b]=q} L_a L_b over ordered
pairs EXACTLY in 128-bit integers and S = sum_q |P_q| (and checks sum_q P_q = (sum_d L_d)^2 exactly). Since
|2^80 lambda_a lambda_b - L_a L_b| <= |L_a| e_b + e_a |L_b| + e_a e_b <= |L_a| + |L_b| + 1 (e = rounding errors, |e| <= 1),
  2^80 Sigma(n) <= S + sum_{(a,b)} (|L_a| + |L_b| + 1) = S + 2 N sum_d |L_d| + N^2   (N = number of odd squarefree d <= n).
The right side is an exact rational. No floating point enters it. Sigma(n)/Lambda(n)^2 is about 0.645 for n between 3000 and 20000.
Checks: Lambda(n) = W(n)/V(n) holds EXACTLY in rationals and lambda_1 = 1 exactly at every level used (out/control_K5.txt);
the bound exceeds the exact-rational Sigma(n) by < 1e-11 relative for ten n <= 300 (Python Fractions, out/controls_K3_K4.txt);
it agrees with the lead's long-double value to ~1.3e-11 at every level used (same file).
The standalone checker (verify/check_rho.py) recomputes the weights in arb balls at 128 or 256 bits (not rationals), certifies its own
rounding |2^40 lambda_d - L_d| <= 1 from the ball, sums with its own sort-based exact accumulator (verify/rhocount.c), and checks
lambda_1 = 1, sum |lambda_d| <= W_up(n)/V_low(n) and the identity sum_q P_q = (sum L)^2.

### R4. Result (NUMERICAL, arb, outward rounding)
Interval terms for z_i <= 20000 use Sigma; the z_i are re-chosen by the float optimiser with a Sigma/Lambda^2 model (any admissible
z_i gives a valid bound; 22 intervals end up with z_i <= 20000, five of them pinned at the cap, n in {19993, 19997, 19999}).
Author's program: B <= 2.1257394310040893870 at 128 and 256 bits (out/rho_exact_p128.json, out/rho_exact_p256.json).
Standalone checker: B <= 2.1257393973040676877 at 128 and 256 bits. Claimed: B < 2.1257395.
Margin note (post-panel): the certified value sits about 1.0e-7 below the claimed 2.1257395 (author program 6.9e-8 below); the
margin is thin but rigorous (every term outward-rounded or exact).
Control K1: the same program with the change switched off gives 2.1269872000642055706 = the e6b84d42 program value (out/K1_rho_off_p128.json).
Gain over e6b84d42: 0.0012478, all from the first 22 intervals (largest single gain 1.57e-4 in interval 0; the other 9884
terms are 7.6e-9 larger in total because the optimiser's bracket follows the previous z).
