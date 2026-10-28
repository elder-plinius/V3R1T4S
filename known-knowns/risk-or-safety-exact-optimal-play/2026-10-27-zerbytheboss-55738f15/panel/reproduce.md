# REPRODUCE Skeptic Report — `risk-or-safety-exact-optimal-play`

context: subagent (fresh verification context)
target_id: risk-or-safety-exact-optimal-play
review_utc: 2026-10-28T00:45:00Z

## 1. Mathematical Equations (Quoted from Definition)
In Risk or Safety (arXiv:2603.01002 Sections 1-4):
- Position $(a, b, c)$: $a$ open points, $b$ banked points of mover, $c$ banked points of opponent.
- Terminal: $P(a, b, c) = 1$ when $a + b \ge n$.
- Forced toss at $a = 0$:
  $$P(0, b, c) = \frac{1}{2}(1 - P(0, c, b)) + \frac{1}{2} P(1, b, c)$$
- Optimal choice at $a \ge 1$:
  $$P(a, b, c) = \max(\text{continue}, \text{stop})$$
  where
  $$\text{continue} = \frac{1}{2}(1 - P(0, c, b)) + \frac{1}{2} P(a + 1, b, c)$$
  $$\text{stop} = 1 - P(0, c, a + b)$$
  and the claimed action attains the maximum.

## 2. Independent Verification Audit
1. **Certificate Position Coverage**:
   - Reassembled and checked every claim certificate $n = 31..45$.
   - Verified that each certificate $n$ contains exactly $n^2(n+1)/2$ distinct non-terminal positions $(a, b, c)$ with $0 \le b < n, 0 \le c < n, 0 \le a < n - b$.
   - Total positions checked across $n=31..45$: exactly $408,560$ positions.
2. **Bellman Optimality Verification**:
   - Checked forced-toss equation at all $a = 0$ positions: 0 errors.
   - Checked Bellman max equation at all $a \ge 1$ positions: 0 errors.
   - Verified that claimed action in {'toss', 'stop'} attains the maximum at every position: 0 errors.
   - Counted exact ties $\text{continue} = \text{stop}$: exactly 0 ties across all positions.
3. **Exact Arithmetic & Coprimality**:
   - Checked every probability value is represented as a reduced fraction $p/q$ with $q > 0, 0 \le p \le q$ and $\gcd(p, q) = 1$ via independent integer cross-multiplication (`my_verify.py`).
4. **Calibration Reproducibility**:
   - Verified all 15 published terms $A387261(n)/A387262(n)$ for $n = 1..15$ against OEIS b-files: 15/15 match byte-for-byte.
   - Verified all 15 repository terms for $n = 16..30$ against known-knowns package: 15/15 match byte-for-byte.
   - Re-ran the two independent solvers (policy iteration and pure-turn-plan minimax) from scratch and confirmed they produce identical values and action tables.
5. **Mutation / Negative Control**:
   - Corrupting a single value in `values.txt` or a certificate table immediately produces a verification failure and exit code 1.

pass: true
