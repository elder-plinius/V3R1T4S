# Preregistered Evaluation Bar (`kings-hard-core-entropy-a247413-digits`)

frozen_utc: 2026-10-28T22:26:00Z
target_id: kings-hard-core-entropy-a247413-digits
category: physics
null_test: not needed because deterministic arbitrary-precision transfer-matrix and CTM algorithms compute exact mathematical constants verified by Collatz-Wielandt bounds

## 1. Verbatim Target Bank Criteria
> Success means a decimal value of the A247413 constant with D decimals, D >= (number of terms in A247413 DATA, re-fetched live immediately before claiming) + 4, such that (a) two independent methods (for example CTM adapted to next-nearest-neighbour exclusion via 2x2 block spins, and exact strip transfer matrices with sequence extrapolation) agree on all D decimals, (b) both reproduce the 18 published digits, (c) the digits are stable over at least three increases of the truncation parameter, and (d) a literature/OEIS search finds no published value with D or more decimals. Direction: more digits.

## 2. Partial Wins (Verbatim)
- **p1:** Rigorous two-sided bounds on the A247413 constant certifying at least 12 correct decimals, from Calkin-Wilf-type inequalities on cylinder and torus transfer matrices evaluated in exact arithmetic, with the Collatz-Wielandt certificate vectors published.
- **p2:** The boundary (surface) free-energy coefficient of the king-graph model with free boundaries, which Kai Liang estimates in arXiv 2505.12776, to at least 4 more decimals than his published estimate, by two independent methods (note: the hard-core gas on the triangular lattice is the exactly solved hard-hexagon model and is not a target).

## 3. Preregistered Thresholds and Checkers
1. **Target Decimals ($D$):**
   - Live OEIS A247413 DATA has 26 terms (`1,3,4,2,6,4,3,9,5,1,1,2,4,6,0,1,2,9,7,8,5,1,7,3,0,1`).
   - We target $D \ge 26 + 4 = 30$ decimal digits (specifically targeting $D = 32$ to $36$ stable decimal digits).
2. **Two Independent Lenses:**
   - **Lens 1 (Baxter's $2 \times 2$ block-spin CTMRG):** Evaluated in 80-digit precision arithmetic (`mpmath`). Truncation parameter: bond dimension $\chi \in \{16, 24, 32, 40, 48\}$.
   - **Lens 2 (Boundary-MPS / strip transfer matrix Prony sequence extrapolation):** Evaluated in 80-digit precision arithmetic (`mpmath`). Truncation parameter: cylinder circumference $W \in \{16, 18, 20, 22, 24\}$.
3. **Reproducibility Checks:**
   - Both methods must reproduce OEIS A063443 for $n \le 12$:
     $a(1)=1, a(2)=2, a(3)=5, a(4)=35, a(5)=314, a(6)=6427, a(7)=202841, a(8)=12727570, a(9)=1355115601, a(10)=269718819131, a(11)=94707789944544, a(12)=60711713670028729$.
   - Both methods must reproduce all 18 published digits: $1.34264395112460129\dots$
   - Both methods must agree on all $D \ge 30$ digits.
   - Digits must be stable across $\ge 3$ truncation parameter increases.
4. **Rigorous Two-Sided Collatz-Wielandt Bounds (`p1`):**
   - For strip/cylinder transfer matrices $M$, export strictly positive certificate vectors $v > 0$.
   - Certify two-sided bounds $\min_i \frac{(Mv)_i}{v_i} \le \lambda \le \max_i \frac{(Mv)_i}{v_i}$.
   - Two-sided bounds on $\kappa$ certifying $\ge 12$ correct decimal digits.
