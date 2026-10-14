# Preregistration: Constant-Weight Code A(27, 6, 10)

- **Target ID**: `constant-weight-codes`
- **Hypothesis**: Unpolished group codes (`g`) in Andries E. Brouwer's table of constant-weight binary codes discard candidate group orbits that have internal pairwise distance conflicts (`< d`), even when such an orbit has zero cross-conflicts with a maximum-weight clique of internally valid orbits. Breaking group symmetry on these discarded zero-conflict orbits yields an immediate strict improvement over the published lower bound.
- **Success Criterion**: Explicit binary code of length $n=27$, constant weight $w=10$, and minimum pairwise Hamming distance $d \ge 6$ with size $M > 12,987$.
- **Verification**: Exhaustive pairwise Hamming distance check and 8-subset collision check confirming zero violations.
