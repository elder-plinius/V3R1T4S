# Skeptic 3 — Problem Card Criterion & Scope Honesty Audit (`criterion.md`)

- `context`: `fresh independent skeptic review auditing problem card criteria and scope honesty`
- `target_id`: `magic-state-stabilizer-rank-exponents`

## Audit Findings

1. **Alignment with Problem Card Partial-Win Tiers (`p2`, `p3`)**:
   - The problem card defines `p2` as certified finite-$m$ lower-bound and structural progress on qubit magic states (`qubit_H`, `qubit_T`, `CS`) and `p3` as finite-$m$ rank bounds, structural obstructions, and exact MILP closures on qutrit ($d=3$) magic states (`Norrell`, `H_3`, `Strange`).
   - The package accurately claims `CONFIRMED_PARTIAL` (`partial_win: p2, p3`), explicitly states under `## Not Claimed` and `## What We Did Not Touch, Open Frontier & Invitation to Reuse / Cite` that it does not claim strict upper-bound improvements $\alpha_T < 0.3952$ or $\alpha_F < 0.374$ (`p1`), and quotes `confirmed_scope` word-for-word under `## What` in `README.md`.
2. **Exact Arithmetic & Self-Containment**:
   - Every witness in `object/constructive_witnesses.json` and every certificate in `object/p2_p3_lower_bound_certificates.json` is verified from first principles without external data files, network calls, or floating-point solver tolerances.

pass: true
