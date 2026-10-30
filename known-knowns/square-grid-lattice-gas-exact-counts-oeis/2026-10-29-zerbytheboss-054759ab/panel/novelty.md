# Novelty Skeptic Report — `square-grid-lattice-gas-exact-counts-oeis`

context: subagent (fresh invocation)
target_id: square-grid-lattice-gas-exact-counts-oeis
review_utc: 2026-10-29T16:15:00Z

## Novelty Audit
1. **Square Ice on Torus ($A054759$)**:
   - Prior best published in OEIS $b054759.txt$ is $n = 14$ by Brendan McKay (April 18, 2024).
   - Terms $a(15)$ and $a(16)$ extend the known sequence by two terms.
   - Live OEIS sequence page confirmed no competing updates or extensions.
2. **Rectangular Tables ($A089980$ & $A210662$)**:
   - $A210662$ published up to $m \le 27$. Row $m = 28$ extends the table to a new row.
3. **Monomer-Dimer $N = 28$ Status**:
   - $A028420(28)$ is uncomputed in the literature (Liang Kai reached $n=27$ in 2020).
   - The milestone honestly notes $N = 28$ is in progress and restricts claimed wins strictly to Partial Wins `p1` and `p2`.
4. **Prior PR & Claim Audit**:
   - Zero competing claims or PRs exist on `elder-plinius/V3R1T4S`.

pass: true
