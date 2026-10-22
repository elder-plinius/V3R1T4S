# PREREG — ghr-sum-difference-c3a (partial win p1)

## Frozen Acceptance Rule
A finite-depth masked-digit construction $(B, q, N, x_f)$ over $G = \{1518, 1524, 1587, 2024, 2032, 2116\}$ is accepted as a confirmed partial win (`p1`) if and only if:
1. The exact same verifier first reproduces Kleinwaks's published finite-depth certificate `1.19102809` on $(B = 17032, Q = 34065, N = 10^{13})$.
2. Every positive difference $d \in \widetilde{D}_+$ has an explicit witness $(\alpha_d, \beta_d) \in M^2$ with $\alpha_d - \beta_d = d$ and $\alpha_d + \beta_d = \kappa(d)$, and all $1 + 2|\widetilde{D}_+|$ elements of $\widetilde{D} = \{0\} \cup \{\pm d : d \in \widetilde{D}_+\}$ have pairwise distinct residues modulo $q$.
3. Every type count $n_d = \lfloor N x_f^{\kappa(d)} / W \rfloor$ is uniquely determined (`cnt_lo == cnt_hi`) in $2^{-128}$ integer fixed-point interval arithmetic (`cfFloorOK == True`), with $n_0 = N - 2\sum_{d \in \widetilde{D}_+} n_d > 0$ and $L = \sum_{d \in \widetilde{D}_+} n_d \kappa(d) \ge B$.
4. All hypotheses of the GHR Lemma hold on $V = 2U$: $0 \in V$, $V \subset \mathbb{Z}_{\ge 0}$, $\max V > 0$, and $|V - V| < 2\max V + 1 < 5 q^N$.
5. Both 60-digit `mpmath.iv` interval/directed-rounding arithmetic and 100% pure integer-interval (`atanh` + Lean `StirlingBounds.lean`) arithmetic certify $C_{3a}(V) \ge 1.19102809 + 10^{-7}$.

null_test: not needed because the claim is an explicit deterministic finite-depth mathematical construction verified by exact integer and interval arithmetic against a published table bound; 400 random mask controls and full-interval controls are additionally checked in the criterion audit.

ratchet_budget: n/a (deterministic exact counting certificate)
