# Skeptic Review: Novelty (`bitcoin-selfish-mining-revenue-bounds`)

context: subagent

## 1. Prior Literature Baseline
In the foundational work on optimal Bitcoin selfish mining (Sapirshtein, Sompolinsky, Zohar, 'Optimal Selfish Mining Strategies in Bitcoin', Financial Cryptography 2016, arXiv:1507.06183), Table 2 reports upper bounds on the attacker's relative revenue (REV) under $\gamma = 0$ at truncation $T = 95$:
- $\alpha = 0.40$: Upper bound $0.48904$
- $\alpha = 0.425$: Upper bound $0.57226$
- $\alpha = 0.45$: Upper bound $0.70109$
- $\alpha = 0.475$: Upper bound $0.90476$ (trivial bound $\alpha / (1-\alpha)$)

Subsequent work by Bar-Zur, Eyal, and Tamar (PTO, AFT 2020, arXiv:2007.05614, Table 1, forks capped at 95) reported heuristic lower bounds:
- $\alpha = 0.425$: $0.56809$
- $\alpha = 0.45$: $0.66894$
- $\alpha = 0.475$: $0.80184$

All prior literature values were floating-point approximations obtained from numerical solvers without exact machine-checkable dual certificates.

## 2. Certified Improvements
This claim establishes the first mathematically certified upper bounds that strictly improve upon SSZ Table 2:
1. **$\alpha = 0.45$ Solution Claim**:
   - Published SSZ upper bound: $0.70109$.
   - Certified upper bound: $U = 70099/100000 = 0.70099$.
   - Improvement: $1.0 \times 10^{-4}$ strictly lower than published literature.
   - Dual certificates provided for both compensation formula variants ($T = 95$ under Variant 2 and $T = 180$ under Variant 1).
2. **$\alpha = 0.475$ Solution Claim**:
   - Published SSZ upper bound: $0.90476$.
   - Certified upper bound: $U = 45233/50000 = 0.90466$.
   - Improvement: $1.0 \times 10^{-4}$ strictly lower than published literature.
3. **$\alpha = 0.425$ Partial Win (p2)**:
   - Certified upper bound $U = 1788/3125 = 0.57216$ ($1.0 \times 10^{-4}$ below SSZ $0.57226$).
4. **$\alpha = 0.40$ Partial Win (p2)**:
   - Certified upper bound $U = 24447/50000 = 0.48894$ ($1.0 \times 10^{-4}$ below SSZ $0.48904$).
5. **Stationary Policy Evaluation (p1)**:
   - At $\alpha = 0.45$: $\text{REV} = 0.66941800 > 0.66894 + 10^{-6} = 0.66894100$.
   - At $\alpha = 0.475$: $\text{REV} = 0.80381566 > 0.80184 + 10^{-6} = 0.80184100$.

## 3. Absence of Competing Claims
Inspection of `TROPHY_CASE.md` and repository open PRs confirms that no prior claim exists certifying upper bounds below SSZ Table 2 or providing exact rational dual certificates for `bitcoin-selfish-mining-revenue-bounds`.

pass: true
