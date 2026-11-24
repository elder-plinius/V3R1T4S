# How we found it (contributor text, unverified)

- Brief: the V3R1T4S bank target brun-constant-unconditional-upper-bound has a partial win p1: a GRH bound strictly
  below Dunn's 2.1594, at the same standard. The frozen PREREG asked for a rigorous replay of Dunn first, and then an
  improvement lens only if it beats the replay R by at least 1e-4 through a genuine change of method (PREREG.v2).
- Replay (L1): exact fixed-point V(z) tables to 1e10, Dunn's inputs, and arb balls gave R = 2.1593210324,
  reproducing 2.1594. Polishing (re-optimising z_i, a free z bracket) gained only about 1.5e-5. That is polish, and it
  was not counted.
- What worked (L3b): Dunn applies the Johnston–Starichkova GRH constant, which is valid for every modulus up to
  sqrt(x), to moduli that are at most z_i^2, far smaller. Grenié–Molteni's explicit Chebotarev bound, applied to
  Q(zeta_q), gives a constant that depends on log q / log x. Using it per interval gives U' = 2.1569563.
- Hardening: replacing the Dusart li bounds with direct li costs nothing. Klyve's c3 lemma was replaced by our own
  proved V(z) lemma, because dropping the V(z) growth entirely gives 2.459, so some lemma is load-bearing. The
  result, U'' = 2.1569669, is slightly weaker than U' but rests on fewer cited inputs, and it is the headline.
- What failed or was limited: Klyve's thesis and Oliveira e Silva's twin-prime page could not be fetched (one try
  each) during the run. The thesis PDF was found later through the repository's item JSON, and Theorem 5.7 was
  checked against it before submission (README, Not claimed). An early CLAIM.md carried a wrong re-fetch time, which was corrected at the gate. The panel noted the
  inherited pi_2(z) omission, now added.
- Panel: three fresh subagent contexts saw only the claim folder. REPRODUCE rebuilt everything bit for bit; a fresh
  REPRODUCE rerun also evaluated the bound with its own sieve and code (total 2.156966935529958839) and mutation-tested the
  checker. NOVELTY found no prior use. CRITERION judged p1 met, conditional only.
