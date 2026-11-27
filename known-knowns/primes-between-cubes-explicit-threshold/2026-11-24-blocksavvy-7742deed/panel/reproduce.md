role: reproduce
context: fresh subagent (independent REPRODUCE skeptic; saw only kit RULES.md, the PANEL_BRIEFS.md header + REPRODUCE section, and a copy of claim/; did not open attempts/, notes/, scout.md, BRIEF.md or any other panel file)
claim: For every integer n >= exp(exp(29.735)) there is a prime in (n^3 + 1/2, n^3 + 3n^2 + 1/2], hence in (n^3, (n+1)^3), using Yang thesis Thm 1.3 (I3) and Bellotti arXiv:2311.05136v1 Thm 1.1 (I4).
date_utc: 2026-11-24T07:56:41Z

## Package integrity
`sha256sum -c SHA256SUMS` in the copied claim/: all 28 entries OK.

## (1) Inputs checked against data/ (pdftotext of each PDF)
- I1: arxiv_2107.14468.pdf, Theorem 2: "For 50 < T < x and half odd integers x >= x_K we have psi(x) = x - sum_{|gamma|<T} x^rho/rho + O*(K x log x log log x / T)". Table 2: K = 2.4798 for log x_K = 10^6. Matches PROOF.md exactly (strict |gamma| < T, strict 50 < T < x, half-odd x). OK.
- I5 (as given in I1): eq. (4) N(sigma,T) <= C1(sigma)(log kT)^{2 sigma}(log T)^{5-4 sigma} T^{8(1-sigma)/3} + C2(sigma) log^2 T, T >= H0, k in [10^9 H^-1, 1]; N(sigma,T) counts 0 < gamma < T, sigma < beta < 1; section 4: "C1 = C1(1), C2 = C2(sigma1)", "C1(sigma) is increasing and C2(sigma) is decreasing", "we can take C1 = 17.418 ... and C2 = 5.272" (footnote: C2 computed with k = 1). Matches. Note: secondary citation of KLN via Cully-Hugill; harmless, since its term A1 is about 1.1e-1186824 at X0 (PROOF Remark 2 is borne out numerically).
- I2: I1 eq. (3), a1 = 0.1038, a2 = 0.2573, a3 = 9.3675, T >= e. Matches. Consequence N(T) <= T log T for T >= 100 is immediate.
- I3: yang_thesis_2025.pdf, Theorem 1.3: "One has zeta(sigma+it) != 0 if t >= 3 and sigma > 1 - 1/(51.34 (log t)^{2/3} (log log t)^{1/3})". Matches exactly.
- I4: arxiv_2311.05136.pdf (v1, 9 Nov 2023), Theorem 1.1: sigma in [0.98, 1], T >= 3, bound (C1 T^{57.8875(1-sigma)^{3/2}} (log T)^{19703/1800} + C2 T^{33.08(1-sigma)^{3/2}} (log T)^{503/45} + 0.27 (log T)^{14/10}) log log T, C2 = 7.65e10, C1 = 9.77e21 for T > e^{481958}. N(sigma,T) = #{0 < gamma < T, sigma < beta < 1} (Section 1). Matches exactly, including the strict counting.
- I6 (Erdos, theta(t) < t log 4) and I7 (first zero ordinate 14.13..., conjugate symmetry, nu decreasing for t >= 3) are classical/elementary. OK.

## (2) Proof steps re-derived by hand
- Lemma 1: psi - theta = sum_{k>=2} theta(y^{1/k}); at most log y/log 2 nonzero terms with k >= 3, each <= theta(y^{1/3}); I6. Correct.
- Lemma 2: I1 applies at x and y with the same T (50 < T = x^alpha < x < y; both half odd; X >= 10^6). |(y^rho - x^rho)/rho| <= int_x^y u^{beta-1} du <= h x^{beta-1}. Correct.
- Lemma 3: gamma >= 14 > 3 and nu decreasing give beta <= 1 - nu(T). Correct.
- Lemma 4: identity x^{beta-1} = x^{-1} + int_0^beta X x^{sigma-1} d sigma, summed, gives S = 2[N*/x + int_0^1 X x^{sigma-1} M]. (a) N* x^{sigma1-1} <= alpha X x^alpha x^{-2/5} = A0. (b) with k = 1, L^{2 sigma} L^{5-4 sigma} <= L^{3.8} on sigma >= 0.6, x^{-u} T^{8u/3} = e^{-u a8 X} <= e^{-u2 a8 X}, length <= 2/5: A1. Correct. (c) x^{sigma-1} = e^{-uX}, T^{B u^{3/2}} = e^{B alpha u^{3/2} X}; g'(u) = 1 - (3/2) B alpha sqrt(u) >= m_i on [0,u2], so g(u) >= g(nu) + m_i(u - nu) and int_nu^{u2} X e^{-X g(u)} du <= e^{-X g(nu)}/m_i. Correct; 1 - u2 >= 0.98 and L > 481958 place every sigma, T in I4's stated range. (d) M = 0 on [1-nu, 1]. Correct.
- Lemma 5: y <= 2x, log y <= X+1, log log y <= log(X+1) give the 3K x (X+1) log(X+1)/T bound; x^{1/3-alpha} = e^{-delta X}; h = 3(x-1/2)^{2/3} >= 2.99 x^{2/3}. R_E, R_T as stated. Correct.
- Lemma 6: P = X nu with nu = 1/(51.34 L^{2/3} (log L)^{1/3}), L = alpha X: d log P/dX = 1/X - 2/(3X) - 1/(3X log L) = (1 - 1/log L)/(3X), so dP/dX = nu(1 - 1/log L)/3 (confirmed). d(X nu^{3/2}) <= nu^{1/2} dP because d nu < 0, so d(X g_i)/dX >= (1 - B_i alpha sqrt(nu)) dP/dX = Q_i/X. Log-derivative of the A2 term is e_i/X + 1/(X log L) - d(X g_i)/dX <= (e_i + 1/log L - Q_i)/X. Q_i is non-decreasing (every factor is positive and non-decreasing). A0, A1, R_E, R_T log-derivatives as stated. Correct.
- Theorem: X = log(n^3 + 1/2) > 3 log n >= 3 e^Y = X0; y < (n+1)^3. Correct.
No gap found.

## (3) Own interval evaluation (written before opening code/)
Reviewer scratch (sandbox, not in package): my_check.py (python-flint arb, prec 128/256/512) and my_iv.py (mpmath.iv, 300 bits), written from the PROOF.md definitions, with Y entered as the exact decimal "29.735".
- X0 = 3e^{29.735} in [24596180649633.9 +/- 0.03]; nu0 = 1.54628855315321e-11; X0 nu0 = 380.327925898173.
- A0 = 6.2e-712132358108, A1 = 1.1e-1186824, A2 = 0.467126672244 (terms 0.4671266687, 3.5e-9, 6.4e-147), R_E = 2.0e-10667, R_T = 3.6e-1780330922006.
- Phi(X0) = [0.934253344488 +/- 1.15e-13] (arb, same at 128/256/512); mpmath.iv: [0.93425334448811436994..., 0.93425334448811436994...]. Phi(X0) < 1: certified.
- (M1), (M2a/b), (M4), (M3) for i = 1,2,3 (B_i alpha sqrt(nu0) < 1, m_i > 0, Q_i >= e_i + 1/log L0), (V) (X0 >= 1e6, L0 > 481958, log L0 > 1, nu0 < u2), a8 > 0, T >= 3e12, 1 - u2 >= 0.98: all True.
- Y = 29.734: Phi = [1.04446600951 +/- 4.4e-12] > 1.04 (certified), so it fails. Remark 1 is confirmed.
- Spot check (not used for the proof): Phi decreases along Y = 29.735, 29.7351, 29.736, 29.74, 29.8, 30, 31, 35, 50, 100, with all conditions holding. This agrees with Lemma 6.

## (4) Author code vs. out/
Ran code/run_all.sh (PY = workspace venv; python-flint 0.9.0, mpmath 1.3.0). It printed FAIL/PASS/PASS/MUTATIONS_AS_EXPECTED/ALL_CONTROLS_BEHAVE/FAIL/PASS/RUN_ALL_DONE. The regenerated out/ is byte-identical to the shipped out/ (diff -r empty). A second run is byte-identical to the first, so the code is deterministic. out/main_prec256.txt gives Phi = [0.934253344488 +/- 1.15e-13], X0 nu0 = 380.327925898, which agrees with my checker to every printed digit. The 29.734 run gives Phi = 1.04446600951 (FAIL), which also matches. cert_arb.py implements the same A0, A1, A2, R_E, R_T and Q_i formulas as PROOF.md.

## Notes (not reasons to fail under REPRODUCE)
- CLAIM.md cites PREREG.md for the frozen thresholds, but PREREG.md is not in the claim package. CRITERION should check this.
- I4 is an unrefereed v1 preprint and I3 is a thesis. I reproduced the claim conditional on their exact statements, and nothing more. Bellotti's proof itself uses the c = 53.989 region; combining her stated theorem with Yang's region is logically fine.
- I5 and I2 are cited secondhand, through Cully-Hugill and Bellotti. They are numerically irrelevant: they contribute below e^{-10^4}.

Verdict: every input statement matches its source text, every lemma re-derives, an independent arb + mpmath.iv evaluation certifies Phi(3e^{29.735}) = 0.9342533... < 1 with all of (M1)-(M4), (V), and Y = 29.734 certifiably fails. The author's pipeline reproduces out/ byte-for-byte and deterministically. Labels: PROVED-HERE conditional on I1-I7 as stated (I3 thesis, I4 preprint).
pass: true
