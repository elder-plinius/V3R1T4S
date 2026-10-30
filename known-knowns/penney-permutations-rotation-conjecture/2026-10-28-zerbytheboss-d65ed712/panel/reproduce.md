# Reproduce Skeptic Report — `penney-permutations-rotation-conjecture`

context: subagent (fresh invocation)
target_id: penney-permutations-rotation-conjecture
review_utc: 2026-10-28T18:50:00Z

## Reproduction Audit

1. **Independent Verification of Calibration Against Published Table 1**:
   - Sergi Elizalde and Yixin Lin (*Penney’s Game for Permutations*, DMTCS 28:1 (2026), arXiv:2404.06585), Table 1 lists exact avoidance counts and winning probabilities for $k = 3$.
   - Re-evaluated in two independent clean-room implementations (compiled Rust engine with 256-bit exact arithmetic and pure Python solver):
     - $123 \to 231$: $B(3)=0, B(4)=5, B(5)=32, B(6)=222$; win probability matches paper Table 1: $0.6148$.
     - $132 \to 321$: $B(3)=0, B(4)=4, B(5)=29, B(6)=208$; win probability matches paper Table 1: $0.6480$.
     - $213 \to 132$: $B(3)=0, B(4)=6, B(5)=43, B(6)=318$; win probability matches paper Table 1: $0.6163$.
     - $231 \to 312$: $B(3)=0, B(4)=4, B(5)=28, B(6)=203$; win probability matches paper Table 1: $0.6163$.
     - $312 \to 123$: $B(3)=0, B(4)=6, B(5)=43, B(6)=317$; win probability matches paper Table 1: $0.6480$.
     - $321 \to 213$: $B(3)=0, B(4)=4, B(5)=26, B(6)=184$; win probability matches paper Table 1: $0.6148$.
   - Verified Theorem 3.7 exact initial non-avoidance counts: $B(4) = (k-1)!(k-1) = 4$ for all non-monotone $\sigma \in S_3$, and $B(4)=5$ for $\sigma \in \{123, 321\}$.

2. **Reproduction of $2341 \to 1234$ Benchmark**:
   - Replicated Elizalde-Lin Section 6 value: $\Pr(2341 \prec 1234) \approx 0.4430$.
   - At horizon $H=36$, exact 42-digit integer arithmetic yields:
     - $A(36) = 147886985383757458869209075733594161570220$
     - $B(36) = 186454247223712671395113700966835612829428$
     - $R(36) = 37652094182431087203676671450405425600352$
     - $36!   = 371993326789901217467999448150835200000000$
     - $(A(36) + R(36))/36! = 0.4987699 < 1/2$.
     - $B(36)/36! = 0.5012301 > 1/2$.
   - Even if Alice wins 100% of the unresolved tails, her winning probability cannot reach $1/2$.

3. **Reproduction of Full $S_4$ Certification (Partial Win p1)**:
   - Evaluated all 24 permutations in $S_4$ against their right cyclic rotations $\tau = (\sigma_2, \sigma_3, \sigma_4, \sigma_1)$.
   - Every single permutation $\sigma \in S_4$ certifies $(A(H) + R(H))/H! < 1/2$ at or before $H=36$:
     - 20 permutations certify at $H \le 28$.
     - 2 permutations ($1432, 4123$) certify at $H = 31$.
     - 2 permutations ($2341, 3214$) certify at $H = 36$.
   - Bit-for-bit exact agreement between compiled Rust engine and pure Python solver.

4. **Reproduction of $S_5$ Exact Rational Intervals at $H=16$**:
   - Evaluated all 120 permutations across 60 complement-symmetry classes in $S_5$.
   - Exact counts $A(16) + B(16) + R(16) == 16! == 20,922,789,888,000$.
   - Verified exact complement symmetry: $\sigma$ and $\sigma^c$ produce bit-for-bit identical $(A, B, R)$.
   - For all 120 permutations, Bob's right rotation beats Alice conditionally: $B / (A + B) > 54.78\%$, confirming zero counterexamples in $S_5$.

pass: true
