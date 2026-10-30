# Skeptic Review: Target Criterion (`bitcoin-selfish-mining-revenue-bounds`)

context: subagent

## 1. Criterion Verification Checklist
The success criterion in `target.md` specifies:
> "A machine-checkable certificate that max over all policies of REV in the untruncated SSZ model (definitions as in arXiv 1507.06183, Sections 2-4, with gamma = 0) is at most U, where U <= 0.70099 at alpha = 0.45 or U <= 0.90466 at alpha = 0.475. Each bar is 1e-4 below the published SSZ Table 2 upper bound (0.70109, 0.90476); lower is better."

### Checklist Evaluation:
1. **Machine-Checkable Format**:
   - Certificates are serialized in standard JSON format containing rational $\rho = U$, gain $g < 0$, truncation $T$, and bias vector $h(s)$ for all states.
   - Verified via independent checker `runs/2026-10-28-1530/claim/verify_certificate.py` in exact rational arithmetic. PASS.
2. **Bounds Satisfaction**:
   - $\alpha = 0.45$: Certified $U = 70099/100000 = 0.70099 \le 0.70099$. PASS.
   - $\alpha = 0.475$: Certified $U = 45233/50000 = 0.90466 \le 0.90466$. PASS.
   - Both certified bounds are $\ge 10^{-4}$ below the published SSZ Table 2 upper bounds ($0.70109$ and $0.90476$). PASS.
3. **Finite Over-Paying MDP ($N_\rho^T$) Construction**:
   - Model built with identical states, actions, transition probabilities, and compensation rewards as defined in SSZ Section 4.2.
   - Evaluated under both formula interpretations (Variant 1: unbracketed LaTeX; Variant 2: factored $(1-\rho)$). Both pass with zero violations. PASS.
4. **Dual Certificate Inequalities**:
   - Checked that for every state $s$ and every legal action $a$, $R(s, a) + \sum_{s'} P(s' \mid s, a) h(s') - h(s) \le g$ holds with $g < 0$.
   - Verified in exact arithmetic: 27,648 states verified for each certificate with 0 violations. PASS.
5. **SSZ Table 2 Calibration & Sanity Requirement**:
   - Rebuilt independent model solver and reproduced published $\epsilon$-OPT values:
     - $\alpha = 0.425$: gain is within $10^{-5}$ of 0 at $\rho = 0.56808$. PASS.
     - $\alpha = 0.45$: gain is within $10^{-5}$ of 0 at $\rho = 0.66891$. PASS.
   - Policy iteration / value iteration of $N_\rho^T$ at $\alpha = 0.45, \rho = 0.66$ returns strictly positive gain ($g = +0.01114721 > 0$ in Rust, $+0.013792 > 0$ in Python). PASS.
6. **Partial Wins**:
   - Partial win p1: Stationary policies evaluated in exact arithmetic yield $\text{REV} = 0.66941800 > 0.66894 + 10^{-6}$ at $\alpha = 0.45$ and $\text{REV} = 0.80381566 > 0.80184 + 10^{-6}$ at $\alpha = 0.475$. PASS.
   - Partial win p2: Certified upper bounds $U = 0.57216 \le 0.57226 - 10^{-4}$ at $\alpha = 0.425$ and $U = 0.48894 \le 0.48904 - 10^{-4}$ at $\alpha = 0.40$. PASS.

All criteria are fully satisfied without exception.

pass: true
