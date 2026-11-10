# Panel: REPRODUCE skeptic

context: subagent (Claude Code Agent tool)
role: REPRODUCE (kit/RUN.md step 6), plus the human's added checks for this panel
claim: `gauss-kuzmin-wirsing-certified-digits`, D = 842 (N = 2800 vector), bundle `claim/`
injection_suspected: none seen (I read CLAIM.md, PROOF.md, PREREG.md, PREREG.v2.md, REPRODUCE.md, the code and parts of data/)

## Verdict in one paragraph

The mathematics reproduces in full. I wrote my own checker from the definitions before reading `claim/code/`. At the
claim's parameters it gives |lambda_2 - s| <= 4.549042402e-843 (D = 842). At my own parameters it gives 4.476735362e-843
(D = 842). Here s is the exact decimal in `claim/inputs/mu_N2800.txt`. All intermediate bounds agree with
`claim/result/cert_L1.json` and `cert_L2.json`. The author's certifier, rerun at 3900 and 4300 bits, writes JSON files that
are identical to the saved ones except for `time_s`. I still fail the bundle on one mismatch, because the kit says "Fail on
any mismatch". `claim/REPRODUCE.md` step 2 (`enclosure.py ... 740 ...`, "Expected: ... the enclosure of
`result/enclosure_C83.txt`") does not regenerate the saved file, and CLAIM.md calls that file "decimal endpoints of C_83 to
740 places". The saved file actually has 860 places and is reproduced byte for byte only with NDEC = 860. With 740, the
endpoints agree on only 739 decimals. No certified number changes. The fix is to change 740 to 860 in CLAIM.md (Object
section) and REPRODUCE.md step 2, or to regenerate the file at 740 and reword. After that fix, every check of this
skeptic passes.

## 1. Independent checker (written before reading the author's code)

Definition used, quoted from PROOF.md "Setting": "c = 3/5, R = 4/5, D = {z : |z - c| < R} ... w = (z - c)/R.
H = H^2(D) ... The e_k = w^k form an orthonormal basis ... h_n(z) = 1/(z+n), n >= 1, and (Lf)(z) = sum_{n>=1} h_n(z)^2
f(h_n(z))".

My own derivation:
- The exact monomial coefficients of v come from integer polynomial composition: F(5z-3) with
  F(y) = sum V_k 4^(N-1-k) y^k, where v_k = V_k 2^E. This is a different route from the author's ball Taylor shift.
- For a polynomial, sum_n (z+n)^(-m-2) = zeta(m+2, z+1). Expanding about z = c gives
  (Lp)_j = (-R)^j/j! sum_m [p_m/(m+1)!] (m+j+1)! zeta(m+j+2, 8/5).
- The correlation over m is computed as one arb_poly product (the author uses Hankel arb_mat blocks).
- The tail beyond J uses my own derivation. zeta(s,a) <= a^-s [1 + (a/(1+a))^s (1 + (1+a)/(s-1))]. The ratio of
  consecutive terms binom(m+1+j,j) 2^-j, which is (m+2+j)/(2(j+1)), decreases in j, which gives a geometric tail. The
  l2 norm of the tail is bounded by its l1 norm.
- The centre is the exact decimal s, taken as an arb ball containing it. So my statement is about s itself and needs no
  rounding step.
- Eigenvalue counting uses Gershgorin discs of X^-1 A_K X. X holds the exact midpoints of approximate eigenvectors, and
  X^-1 is a rigorous ball inverse. Each disc must lie strictly inside or strictly outside each circle. I count with
  `acb_mat.eig` separately as a second check.

Two sanity checks:
- `mine/fixedpoint_test.py` applies the same coefficient formula to g = 1/(1+z), which is (5/8) sum (-1/2)^k w^k. It
  returns max_{j<40} |(L g_N)_j - g_j| <= 3.22e-131 at N = 300, consistent with Lg = g.
- The basis-change check v(w = 1/3) differs between the two bases by less than its ball radius.

Scripts: `mine/mycheck.py` (sha256 ec520a55...1a5914), `mine/mycompare.py` (6cf0c69f...758546), `mine/fixedpoint_test.py`
(535e698d...f8f56f).

| quantity | mine, 4100 bits, J 11800, J0 560, Q2 80, Qrho 256 | mine, claim L1 params (3900, J 11200, J0 480, Q2 64) | saved cert_L1.json | saved cert_L2.json (4300, J 12320, Q2 96) |
|---|---|---|---|---|
| r_head | 1.4040663e-842 | 1.4040663e-842 | 1.4041e-842 | 1.4041e-842 |
| r_tail (beyond J) | 1.4865746e-1402 | 2.3711340e-1271 | 2.3711e-1271 | 6.7482e-1518 |
| \|\|v\|\| lower | 5.07917627074 | 5.07917627074 | 5.079176271 | (same) |
| eta | 2.7643582e-843 | 2.7643582e-843 | 2.7644e-843 | 2.7644e-843 |
| eps_a (K = 80) | 1.6381810e-7 | 1.63818e-7 | 1.6382e-7 | same |
| eps_b rows | 0.00014729133 | 0.00014729133 | 0.00014729 | same |
| eps_b tail | 1.0900826e-70 (J0 560) | 4.33764e-51 | 4.3376e-51 | same |
| eps | 0.00014745515 | 0.00014745515 | 0.00014746 | 0.00014746 |
| \|\|A_K\|\|_F | 1.347995273 | 1.347995273 | 1.3479953 | same |
| M_K on Gamma_2 | 158.16785 | 160.66201 | 160.662 | 156.548 |
| M_K on \|z\| = 1/5 | 55.697450 | (same) | 55.6974 | 55.6974 |
| eps M_K (Gamma_2 / rho) | 0.0233227 / 0.00821288 | 0.0236904 / (same) | 0.02369 / 0.008213 | 0.02308 / 0.008213 |
| M (Gamma_2 / rho) | 161.94483 / 56.158674 | 164.56052 / (same) | 164.561 / 56.1587 | 160.247 / 56.1587 |
| eigenvalue counts | Gershgorin 1 in Gamma_2, 2 in \|z\| > 1/5, 0 straddling; eig: 80 balls, 1 / 2, 0 ambiguous | same | 80; 1 / 2 | 80; 1 / 2 |
| radius | 4.476735362e-843 | 4.549042402e-843 | 4.54904e-843 | 4.42979e-843 |
| D | 842 | 842 | 842 | 842 |

- The eigenvalue ball of A_K inside Gamma_2 is [-0.3036630028987326585974481219015562291726 +/- 1.51e-41]. It is the same
  in my runs and in the saved JSON.
- Geometry checks hold: |s| - 1/100 > 1/5 and s + 1/100 < 0.
- My run times were 147.6 s (4100 bits) and 142.5 s (3900 bits). I did not measure peak memory: the in-script counter
  returned 0.

Negative control with my checker: same v, centre `claim/inputs/mu_N2800_shift800.txt`. It gives eta 1.0000000e-800 and
radius 1.645605246e-800 (D = 799). The saved `cert_NEG_L.json` has 1.64561e-800. The radius is >= 1e-800, so the shifted
centre is not certified away.

## 2. Author's certifier rerun (REPRODUCE.md step 1), run one after the other

- L1 (3900 bits, J 11200, Q2 64): exit 0, 175 s. RESULT radius 4.5490e-843, D = 842, isolation ok = True.
- L2 (4300 bits, J 12320, Q2 96): exit 0, 214 s. RESULT radius 4.4298e-843, D = 842, isolation ok = True.
- Both rerun JSONs differ from `claim/result/cert_L1.json` / `cert_L2.json` only in the line `time_s` (156.7 vs 175.3,
  178.6 vs 213.5). The computation is deterministic.
- `code/refs.py` reproduces `data/refs.json`. `code/compare.py` on the reruns gives output identical to
  `result/compare_L1.txt` and `compare_L2.txt` (ALL_CHECKS PASS).
- `code/gershgorin_count.py 80 3900 ...` reproduces `result/gershgorin_K80_p3900.txt`: GERSHGORIN_COUNT PASS, max disc
  radius [9.42e-1003 +/- 2.02e-1006].
- `code/enclosure.py inputs/mu_N2800.txt 740 ...`, as written in REPRODUCE.md, does NOT reproduce
  `result/enclosure_C83.txt`. Its endpoints are given to 740 places and "agree on the first 739 decimals". The half-width
  and D lines are unchanged: <= 4.5535915e-843 < 10^-842, D = 842. With NDEC = 860 the output is byte-identical to the
  saved file. This is the mismatch that fails the bundle.
- Input sha256 values match REPRODUCE.md for all five input files.

## 3. Proof steps re-derived

- Lemma 1: m_1 = 5/6, r_1 = 5/12, rho_1 = 13/16. For n >= 2, rho_n = (c - 1/(n+c+R))/R rises to 3/4. |z+1| >= 4/5.
- Lemma 4: sum_{n>=2} (n-1/5)^-2 <= 10/13 by midpoint convexity. Also ||g||_{H^2} <= sup_D |g| and |f(zeta)| <= rho^K (1-rho^2)^-1/2
  on range(I - P_K).
- Lemma 6: L - P L P = L(I-P) + (I-P)LP.
- Lemma 8: the resolvent of L_K = A_K (+) 0 is max(||(A_K - z)^-1||, 1/|z|). The chord bound is
  delta = 2 r sin(pi/(2Q)), and the Neumann-series step is correct.
- Lemma 9: the small-gain homotopy keeps the Riesz projector ranks constant. The exterior count uses
  R_big > ||A_K|| + eps.
- Lemma 11: ||Pi|| <= r0 M, ||S|| <= M(1 + r0 M) on Gamma by the maximum principle, which gives (1 - s eta)|lambda - mu| <= r0 M eta.
- Lemma 12: the two eigenvalues outside |z| = 1/5 are 1 (Lg = g, checked numerically above) and lambda. lambda is real
  by conjugation symmetry and negative.
- Lemma 13: h_m(h_n(cl D')) lies in |z - 1/2| <= 1/2, which is inside D.
- The author's code does what PROOF.md states:
  - mu = arb(s).mid();
  - the residual uses the exact v and |p_m| upper bounds;
  - certify stops on any eigenvalue ball that straddles a circle, on sampling that is too coarse, or on failed small gain;
  - D is checked with rad < 10^-D in arb.

Centre checks, by my own exact-rational comparison with radius 4.54905e-843:
- |(-s) - Nisoli's 175-digit centre| = 4.095e-176 <= r + 1e-175.
- The 382 OEIS b-file decimals agree within r + 1e-382.
- The 649 non-certified decimals agree within r + 1e-649.
- The saved enclosure endpoints contain [-s - r, -s + r], have half-width 4.55359e-843 < 1e-842, and agree on 842
  decimals.

## 4. Not done / limits

- I did not run step 5 (crosscheck.py; numerical, not part of the proof) or step 6 (eigvec; excluded, over the memory budget).
- I did not rerun the author's NEG run. My own checker reproduced its radius instead.
- I did not re-fetch the status page (no network for this role). The bundle's snapshot gives 175.
- Arb/python-flint ball arithmetic and the cited KNOWN theorems (Kato; Gershgorin) are trusted, not re-proved.

## 5. Required fix

Make CLAIM.md ("to 740 places") and REPRODUCE.md step 2 (`enclosure.py inputs/mu_N2800.txt 740 ...`) agree with the saved
`result/enclosure_C83.txt` (860 places), or regenerate that file at 740 places and reword. The 740 looks carried over
from the N = 2400 object. A re-check is one command and takes about a second.

pass: false
