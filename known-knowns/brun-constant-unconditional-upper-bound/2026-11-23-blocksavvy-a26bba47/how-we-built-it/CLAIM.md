# Claim
One sentence: Assuming GRH for Dirichlet L-functions (and RH), Brun's constant satisfies B < 2.156967.
target_id: brun-constant-unconditional-upper-bound (partial win p1)
Criterion p1 (verbatim from the bank): "Under GRH, a bound B < U' with U' strictly below Dunn's 2.1594, at the same proof and
certification standard."
Status source: https://teorth.github.io/optimizationproblems/constants/81a.html, fetched 2026-11-23T16:18:57Z and re-fetched
2026-11-23T16:57:58Z (HTTP 200, both sha256 f8344f6ab5e7162878949de7b362dcbe4e5a54a48df35185e564e1901d4e0cc9), and fetched
independently by the novelty skeptic at 2026-11-23T17:11:43Z (HTTP 200, same sha256): best conditional upper bound 2.1594 [D2025]
(L. Dunn, "Improved upper bound on Brun's constant under GRH", Bull. Aust. Math. Soc. 113(2) (2026) 293-303, doi:10.1017/s0004972725100233,
first published online 2025-07-04, which is why the status page writes 2025; arXiv:2504.15658v2); no open pull request touches constants/81a.
Values (python-flint arb, sup of the final ball; 128 and 256 bits give identical sups):
- U'' = 2.1569669355 (headline, rounded up to 2.156967): Dunn's framework (arXiv:2504.15658v2 Theorem 3.1) with three input changes: (B) the
  GRH error constant c_pi depends on the modulus via Grenie-Molteni Cor. 1.2 with log q <= 2 log z; (L) li(x) computed
  directly instead of Dusart/Schoenfeld bounds; (V) our own lower bound for V(z), z > 1e10, instead of Klyve's c3 lemma.
- U' = 2.1569562895 (rounded up to 2.156957): change (B) alone, every other input exactly Dunn's.
- R = 2.1593210324: Dunn's own method and inputs replayed rigorously (calibration; reproduces his 2.1594).
Hypothesis: GRH for the Dedekind zeta functions of Q(zeta_q), which factor into Dirichlet L-functions, so GRH for
Dirichlet L-functions suffices. No Hecke or Artin L-functions beyond these.
Margins: U'' + pi_2(z) correction (<= 1.03e-15) is 2.15696693552995885 (sup), so the margin below 2.156967 is 6.4e-8 at the
chosen z_i. The z_i come from a float optimiser, so U'' at the chosen z_i moves by ~1e-8 with the optimiser's precision (53-bit: 2.1569669653,
64-bit: 2.1569669272; both still < 2.156967, panel/reproduce.md); the reproduce skeptic's own free optimisation gives 2.1569642936 (margin 2.7e-6).
Any admissible z_i give a valid bound, so this is optimisation noise, not a rigour issue. The headline stays the conservative 2.156967;
change (B) alone gives U' = 2.1569562895 (< 2.156957), which additionally relies on Klyve's c3 lemma and Dusart's Theorem 5.1.
Certificate: out/a_bound_certificate.json (every z_i and term) with a standalone checker verify/ (vcount.c + check.py, arb).
Files: PROOF.md, REPRODUCE.md, CHANGES.md, code/, out/, verify/.
