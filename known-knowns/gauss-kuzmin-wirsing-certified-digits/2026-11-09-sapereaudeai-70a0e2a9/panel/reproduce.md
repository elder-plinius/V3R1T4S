# Panel: REPRODUCE (skeptic)

context: subagent (Claude Code Agent tool)
role: REPRODUCE (fresh context; read only the claim bundle `claim/`)
claim: lambda_2 of the Gauss-Kuzmin-Wirsing operator enclosed with radius < 10^-842 (D = 842), centre `claim/inputs/mu_N2800.txt`, vector `claim/inputs/v_N2800.txt`
injection_suspected: none (no text in the bundle or in program output asked me to do anything)

## Verdict in one paragraph

I wrote my own checker from the definitions in `claim/PROOF.md` before reading `claim/code/gkw_cert.py`, and ran it
at the claim's N = 2800 vector and centre at two parameter sets: my own (4100 bits, J = 11600, Q2 = 80, Qrho = 200)
and the L2 parameters (4300 bits, J = 12320, Q2 = 96, Qrho = 256). It certifies |lambda_2 - mu| <= 4.4767354e-843 and
4.4297905e-843 (each for its own dyadic rounding of the same decimal centre), with exactly one eigenvalue of A_K inside
Gamma_2 and two in |z| > 1/5. I reran the author's certifier at both claimed precisions: the JSON outputs are
identical to `claim/result/cert_L1.json` and `claim/result/cert_L2.json` in every field except `time_s`. Every
REPRODUCE.md command that is said to reproduce a saved file (steps 1-5) does so, up to timings and a resource-usage
line the saved files carry. I re-derived every proof step I could check (below) and found no error.

## Definition my checker was written from (quoted from `claim/PROOF.md`, "Setting")

> c = 3/5, R = 4/5, D = {z : |z - c| < R} ... w = (z - c)/R. H = H^2(D) = {f = sum_{k>=0} a_k w^k holomorphic on D :
> ||f||^2 = sum |a_k|^2 < infinity}. The e_k = w^k form an orthonormal basis. ... h_n(z) = 1/(z+n), n >= 1, and
> (Lf)(z) = sum_{n>=1} h_n(z)^2 f(h_n(z)) ... A_K = (<L e_k, e_j>)_{j,k<K}, L_K = P_K L P_K = A_K (+) 0.

Success criterion used (from `claim/CLAIM.md`, bank text): radius below 10^-D with D > 175, centre agreeing with
Nisoli's 175-digit centre within the two radii, rigorous arithmetic, discretisation error bounded on a stated space,
isolation of lambda_2 certified.

## My independent checker (`panel_work/reproduce/mycheck.py`, `tailcheck.py`)

Implementation choices that differ from the author's code (checked after mine was written):
- v -> monomial coefficients p_m in z: exact rational polynomial composition V((z - 3/5)/(4/5)) with `fmpq_poly`
  (author: synthetic division in balls).
- (Lv)_j for j < J: Hankel sum done as one `arb_poly` convolution (author: chunked `arb_mat` products).
- Hurwitz zeta at PREC + 200 bits; tail bound T_m(J) and kappa written from Lemma 5 as I re-derived it; residual,
  eps_a (Lemma 4 closed form), eps_b (Frobenius rows K <= j < 480 plus l1 tail), Frobenius resolvent bounds at Q points
  with the m_i / (1 - delta m_i) bridge, small gain, Lemma 11 radius, all in Arb balls with upper() at each bound.
- Eigenvalue counting with `acb_mat.eig()` at 1000 bits (author: 2600 / 2866 bits) on my own A_K.

| quantity | mine, run A (4100 b, J 11600, Q2 80, Qrho 200) | mine, run B (4300 b, J 12320, Q2 96, Qrho 256) | claim (L1 / L2 JSON) |
|---|---|---|---|
| r_head | 1.40407e-842 | 1.40407e-842 | 1.4041e-842 / 1.4041e-842 |
| r_tail | 1.37627e-1358 (J 11600) | 6.74816e-1518 | 2.3711e-1271 (J 11200) / 6.7482e-1518 |
| r_tail at J = 11200 (tailcheck.py) | 2.37113e-1271 | | 2.3711e-1271 |
| ||v|| lower | 5.07917627074 | 5.07917627074 | 5.079176271 |
| eta | <= 2.76436e-843 | <= 2.76436e-843 | 2.7644e-843 (+/- 4.18e-848) |
| eps_a / eps_b rows / eps_b tail | 1.63818e-7 / 0.000147291 / 4.33764e-51 | same | 1.6382e-7 / 0.00014729 / 4.3376e-51 |
| eps | <= 0.000147455 | <= 0.000147455 | 0.00014746 (+/- 4.86e-9) |
| ||A_K||_F | 1.347995273 | 1.347995273 | 1.3479953 |
| M_K on Gamma_2 (|z - mu| = 1/100) | 158.16785 (Q 80) | 156.54752 (Q 96) | 160.662 (Q 64) / 156.548 (Q 96) |
| eps M_K on Gamma_2 | 0.0233227 | 0.0230837 | 0.02369 / 0.02308 |
| M_K on |z| = 1/5 | 57.914151 (Q 200) | 55.697450 (Q 256) | 55.6974 / 55.6974 |
| eps M_K on |z| = 1/5 | 0.00853974 | 0.00821288 | 0.008213 / 0.008213 |
| M = M_K/(1 - eps M_K), Gamma_2 / rho | 161.94483 / 58.412983 | 160.24661 / 56.158674 | 164.561 / 56.1587 (L1); 160.247 (L2) |
| eig count: inside Gamma_2 / in |z| > 1/5 / meeting a circle | 1 / 2 / 0 (of 80) | 1 / 2 / 0 (of 80) | 1 / 2 (of 80) |
| s eta (Lemma 11) | 1.173e-840 | 1.153e-840 | (< 1) |
| radius |lambda_2 - mu| | <= 4.4767354e-843 | <= 4.4297905e-843 | 4.54904e-843 / 4.42979e-843 |

Run B uses exactly the L2 parameters and the same dyadic mu as L2; its radius 4.4297905e-843 matches L2's
4.42979e-843, and M_K values match to the printed digits. Run A uses parameters of my own choosing and lands between
L1 and L2 as expected from Q2 = 80 lying between 64 and 96. Both runs: |mu_mine - s| <= 8.27e-1236 (A) and
9.22e-1296 (B), so the decimal centre s is within radius + 1e-1235 of lambda_2.

The two big eigenvalue balls in both runs: [1.0000000000000000000 +/- 3e-25] and [-0.30366300289873265860 +/- 2.56e-21]
(the eigenvalue 1 of Lemma 2 reappearing is a sanity check that my A_K is the right matrix).

Centre checks, my own parsing of `claim/data/83a.md` (175 digits) and `claim/data/b038517.txt` (382 digits) in exact
rationals with C = -s: |C - Nisoli| = 4.095e-176 <= radius + 10^-175: True; OEIS b-file within radius + 10^-382: True
(|diff| = 6.16e-383); 649-decimal file within radius + 10^-649: True.

## Author's commands rerun (REPRODUCE.md), compared with the saved files

| step | command (from claim/) | result | saved file comparison |
|---|---|---|---|
| 1 L1 | `certify ... 80 3900 11200 0.01 0.2 64 256` | RESULT radius [4.5490e-843 +/- 4.25e-848], D = 842, isolation/counting ok = True, exit 0, 211.1 s | JSON identical to `claim/result/cert_L1.json` except time_s (211.1 vs 156.7); log identical modulo timings and the saved PEAK_RSS line |
| 1 L2 | `certify ... 80 4300 12320 0.01 0.2 96 256` | RESULT radius [4.4298e-843 +/- 9.54e-849], D = 842, ok = True, exit 0, 241.0 s | JSON identical to `claim/result/cert_L2.json` except time_s (241.0 vs 178.6); log identical modulo timings |
| 2 | `refs.py data` | exit 0 | byte-identical to `claim/data/refs.json` |
| 2 | `compare.py` L1 / L2 | ALL_CHECKS PASS twice | byte-identical to `claim/result/compare_L1.txt` / `compare_L2.txt` |
| 2 | `enclosure.py ... 860 my_L1 my_L2` | half-width <= [4.5535915e-843 +/- 4.76e-851] < 10^-842, D = 842 | byte-identical to `claim/result/enclosure_C83.txt` |
| 3 | `gershgorin_count.py 80 3900 ...` | GERSHGORIN_COUNT PASS, 1 disc inside Gamma_2, 2 in |z| > rho, max disc radius [9.42e-1003 +/- 2.02e-1006] | identical to `claim/result/gershgorin_K80_p3900.txt` except its trailing PEAK_RSS/ELAPSED line |
| 4 | `certify` with `mu_N2800_shift800.txt` | radius [1.6456e-800 +/- 5.25e-806], D = 799 (shift not certified away) | JSON identical to `claim/result/cert_NEG_L.json` except time_s |
| 5 | `crosscheck.py v_N2800 3900` | CROSSCHECK_PLACEHOLDER | |
| 6 | eigvec (optional) | not run (over my memory budget, proves nothing) | |

sha256 of all five inputs match the values listed in REPRODUCE.md. The negative-control centre is exactly
s + 10^-800 (checked in exact rationals). Determinism: two independent executions (the author's saved run and mine)
give identical JSON values; my checker gives the same r_head, eta and eps in both of its runs.

## Proof steps re-derived

- Lemma 1: m_1 = 5/6, r_1 = 5/12, rho_1 = 13/16; for n >= 2 rho_n = (c - 1/(n+c+R))/R < 3/4 (n = 2 gives 13/34). Checked.
- Lemma 2 / 4: Cauchy-Schwarz point bound rho^K (1 - rho^2)^(-1/2); |z+1| >= 4/5 gives 25/16; convexity gives
  sum_{n>=2} (n - 1/5)^(-2) <= 1/(3/2 - 1/5) = 10/13; ||g||_H2 <= sup|g|. eps_a recomputed: 1.63818e-7. Checked.
- Lemma 3: Taylor coefficients of zeta(m+2, z+1) about c give (-1)^j binom(m+1+j, j) R^j zeta(m+2+j, 8/5); radius 8/5 > R. Checked (and A_K reproduces the eigenvalue 1).
- Lemma 5: kappa(sigma) from the integral comparison, R/a = 1/2, ratio (m+2+j)/(2(j+1)) decreasing, q < 1 iff m < J. Checked; my tail values equal the claim's.
- Lemma 6: L - P_K L P_K = L(I - P_K) + (I - P_K) L P_K; operator norm <= Frobenius; tail columns l2 <= l1. Checked.
- Lemma 7: tail j >= J of Lv bounded by sum |p_m| T_m(J) (v_j = 0 for j >= N, N < J). Checked.
- Lemma 8: L_K = A_K (+) 0 gives max(||(A_K - z)^-1||, 1/|z|); nearest-sample distance 2 r sin(pi/(2Q)); Neumann bridge m_i/(1 - delta m_i). Checked.
- Lemma 9: small gain eps M_K < 1 on both circles (mine 0.0233 / 0.0085 and 0.0231 / 0.0082); homotopy L_t keeps
  the Riesz projector rank constant; exterior count via the annulus up to R_big > ||A_K||_F + eps. Checked.
- Lemma 11: ||Pi|| <= r0 M, ||S|| <= M(1 + r0 M) on Gamma and inside by the maximum principle; gives
  (1 - s eta)|lambda - mu| <= r0 M eta. Checked; mu is the centre of Gamma_2 and 0 is outside its disc.
- Lemma 12: |mu| - r0 > 1/5, the other eigenvalue in |z| > 1/5 is 1, conjugation symmetry gives lambda real, mu + r0 < 0 gives lambda < 0. Checked.
- Lemma 13: h_n(cl D) compact in D' and h_m h_n(cl D') inside |z - 1/2| <= 1/2, compact in D (max |z - 3/5| there is 3/5 < 4/5). Checked.
- Lemma 10: the eigenvalue count rests on Arb's certified `acb_mat.eig` (python-flint 0.9.0 docstring: default
  "vdhoeven_mourrain", raises if it cannot isolate) in both the author's code and mine, plus the author's Gershgorin
  check after a similarity, which I reran and which agrees.

## What worried me (none is a failure)

- My eigenvalue count uses the same Arb `acb_mat.eig` routine as the author's (on an independently built A_K), so the
  count is not independent of that library routine; the Gershgorin script (rerun, PASS) is the routine-independent check.
- The status page table (`claim/data/83a.md` line 29) prints Nisoli's centre ending "...6424297" while the full centre
  in the same file ends "...64764297"; the comparison uses the full 175-digit centre and passes. Cosmetic, upstream.
- The status page and open-PR state were fetched by the author; I did not re-fetch (no network in my role), so
  "175 is still the record" rests on `claim/data/preclaim/` as saved.
- Timings on this machine were 1.3-1.4x the REPRODUCE.md figures (other jobs were running); not a correctness issue.

pass: true
