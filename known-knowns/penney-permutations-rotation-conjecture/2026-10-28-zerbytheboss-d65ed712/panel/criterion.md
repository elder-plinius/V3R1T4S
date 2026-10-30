# Criterion Skeptic Report — `penney-permutations-rotation-conjecture`

context: subagent (fresh invocation)
target_id: penney-permutations-rotation-conjecture
review_utc: 2026-10-28T18:50:00Z

## Criterion Compliance Audit

1. **Target Specification & Win Criterion**:
   - Criterion (from `repo/bank/targets.json` and `repo/known-unknowns/graphs-games-automata/penney-permutations-rotation-conjecture.md`):
     - Partial win `p1`: "Pr(sigma precedes tau) < 1/2 for all sigma in S_4"
     - Partial win `p2`: "Pr(sigma precedes tau) < 1/2 for all sigma in S_5"
     - Full win: "A specific k >= 4 and sigma in S_k whose right rotation tau satisfies Pr(sigma precedes tau) >= 1/2"

2. **Evaluation of Submitted Results for Claim `p1` and Exploration of `p2`**:
   - For all 24 permutations $\sigma \in S_4$, taking $\tau = (\sigma_2, \sigma_3, \sigma_4, \sigma_1)$:
     - An exact finite horizon $H \le 36$ is exhibited.
     - Exact non-negative integer counts $A(H), B(H), R(H)$ are computed where $A(H) + B(H) + R(H) = H!$.
     - In every case, $2 \cdot (A(H) + R(H)) < H!$, which implies $(A(H) + R(H))/H! < 1/2$ and $B(H)/H! > 1/2$.
     - Because $\Pr(\sigma \prec \tau) \le (A(H) + R(H))/H!$, this rigorously proves $\Pr(\sigma \prec \tau) < 1/2$.
   - For $S_5$:
     - Exact integer DP counts $A(16), B(16), R(16)$ are computed for all 120 permutations, strictly satisfying $A + B + R = 16! = 20,922,789,888,000$.
     - Bob's rotation wins with conditional probability $B / (A + B) > 54.78\%$ across all 120 permutations, confirming zero counterexamples.
     - True probabilities are bounded within explicit two-sided rational intervals $[A/16!, (A+R)/16!]$.
   - Independent verification scripts recompute and verify all counts, bounds, and symmetries in pure Python in seconds.
   - All conditions for Partial Win `p1` are completely satisfied.

3. **Status Declaration**:
   - Because $S_5$ crossing to $(A+R)/H! < 1/2$ and the full conjecture for general $k$ remain open, this claim is properly and strictly classified as `CONFIRMED_PARTIAL` (`p1`).

pass: true
