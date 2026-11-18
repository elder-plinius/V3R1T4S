# Skeptic 3 — Target Criterion, Bit-Order Convention & Scope Honesty Audit (`criterion.md`)

- `context`: `fresh independent skeptic verification of bank/targets.json criteria and scope limits`
- `target_id`: `nist-aes-circuit-records`
- `milestones_checked`: `p3 (InvMixColumns 92@10) and p4 Route 1 (InvS-box GD=10) + 8 zero-NOT [Inv]S-box 4D Pareto cells (9 witnesses)`

## Audit Findings

1. **Gate Model & Bit Convention Compliance:** `InvMixColumns` circuits use strictly 2-input `{XOR}` on `x0:x31 -> y0:y31` (`x_{8b+r}` = bit `r` of byte `b`), forward `S-box` uses strictly 2-input `{AND, XOR, XNOR}` on `U0:U7 -> S0:S7` (`U0/S0` MSB), and `InvS-box` uses strictly 2-input `{AND, XOR, XNOR}` on `x0:x7 -> y0:y7` (`x0/y0` MSB), matching `usnistgov/Circuits` `%NCFF-0.1-2026` conventions.
2. **Scope Honesty:** `README.md` (`## Not claimed`) states upfront that `0 / 6` CSRC wish-list items are solved (`111@14` is `+1` gate above `(c)` `<= 110@14`), `p1`, `p2`, and `p4` Route 2 remain open, documents NIST's `2`-`NOT` `148@10` file, and distinguishes `TIMEOUT_UNKNOWN` / `ITERATION_LIMIT` from `UNSAT`.

pass: true
