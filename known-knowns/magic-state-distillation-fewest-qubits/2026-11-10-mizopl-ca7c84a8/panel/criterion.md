# Skeptic 3 — Problem Card Criterion & Scope Honesty Audit (`criterion.md`)

- `context`: `fresh independent skeptic review auditing problem card criteria and scope honesty`
- `target_id`: `magic-state-distillation-fewest-qubits`

## Audit Findings

1. **Alignment with Problem Card Partial-Win Tiers (`p1`, `p2`)**:
   - The problem card (`magic-state-distillation-fewest-qubits.md`) defines `p1` as a $T$-to-$\text{CCZ}$ protocol with $d \ge 4$ on $N = 9$ qubits or a machine-checked certificate that none exists on $N = 9$ (establishing $N_{\text{CCZ}}(4) = 10$), and `p2` as a machine-checked certificate for $N = 8$ alone at distance $d = 4$ (establishing $N_T(4) \ge 9$), together with the pipeline control confirming no $d = 4$ protocol exists at $N = 7$.
   - Our package certifies both `p1` ($N_{\text{CCZ}}(4) = 10$) and `p2` ($N_T(4) \ge 9$), includes the $N = 7, d = 4$ pipeline control (`0` SAT hits), and provides explicit upper-bound tightness matrices in `object/constructive_tightness_witnesses.json`.
2. **Scope Honesty**:
   - The package accurately claims `CONFIRMED_PARTIAL` (`partial_win: p1, p2`, as verified by our local 3-skeptic review panel), quotes `confirmed_scope` verbatim under `## What` in `README.md`, and explicitly documents under `## Not Claimed` and `## What We Did Not Touch, Open Frontier & Invitation to Reuse / Cite` that $N_T(4) \in \{9, 10\}$ ($r = 8$, $\mathrm{RM}(4, 8)$) and $N_T(5) \in \{10, 11\}$ remain open.

pass: true
