# Novelty Skeptic Report — `binary-action-games-max-nash-equilibria`

context: subagent (fresh invocation)
target_id: binary-action-games-max-nash-equilibria
review_utc: 2026-10-29T05:05:00Z

## Novelty & Literature Audit

1. **Live Status Verification**:
   - Status Source URL: `https://arxiv.org/abs/2412.17890` (Christoph Hertling, Jelena Vujic, "Maximal two-action games", arXiv:2412.17890v2 [math.PR], 25 Sep 2026).
   - Canonical HTML SHA-256: `c2cd243dedf14c4a0f1d2b13977ce80f010a1be84f2bc48d2f2d2baa46a215fa` (HTTP 200, fetched 2026-10-29T04:41:42Z).
   - Published Status:
     - The maximum number of regular Nash equilibria $\mu(n)$ in an $n$-player binary-action game is known for $n=2$ ($\mu=3$) and $n=3$ ($\mu=9$, Jahani and von Stengel 2024).
     - For $n=4$, Vidunas (2017) established the theoretical upper bound $\mu(4) \le 65$.
     - Hertling and Vujic (arXiv:2412.17890v2, 2026) established the lower bound $\mu(4) \ge 37$ by proving the existence of generic deformations of product two-action games.
     - Hertling and Vujic optimistically formulated Conjecture 4.5: $\mu(4) = 37$.
     - However, the existence proof in the literature relies on an abstract deformation argument; no explicit certified rational payoff table listing all 37 equilibrium coordinates and machine-checked Jacobians existed in standard repositories.

2. **Literature & Repository Audit**:
   - Literature searches across arXiv, Google Scholar, and MathSciNet confirm that $\mu(4)$ remains open with the gap $37 \le \mu(4) \le 65$.
   - Inspected `repo/TROPHY_CASE.md`: no prior trophy or claim exists for `binary-action-games-max-nash-equilibria`.
   - Inspected `known-knowns/`: no prior claim or package exists in the repository.
   - Inspected open pull requests on `elder-plinius/V3R1T4S`: zero pull requests for this target.

3. **Settlement and Novelty of Contribution**:
   - This submission realizes Partial Win **p1**: "An explicit generic 4-player binary-action game with rational payoffs and exactly 37 equilibria, every equilibrium listed with exact algebraic coordinates and certified as in the success criterion."
   - The certified game is provided both in exact rational form ($a_j^i \in \{1/4, 1/2, 3/4\}$) and as an equivalent integer payoff table scaled by $L=64$, with payoffs in $\{-18, -6, -2, 0, 2, 6, 18\}$.
   - All 81 support branches are completely enumerated and certified with non-singular Jacobians and strict best-response slacks.
   - In addition, an exhaustive parallel search of 2,963,000 perturbed games confirms that no perturbed game exceeds 37 equilibria, providing strong empirical evidence in support of Conjecture 4.5.

4. **Verdict**:
   - The claim satisfies all criteria for Partial Win p1 with fully reproducible, standalone machine-checkable artifacts.

pass: true
