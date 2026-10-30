# Preregistered Evaluation Bar (`hard-core-entropy-square-honeycomb-digits`)

frozen_utc: 2026-10-29T02:40:00Z
target_id: hard-core-entropy-square-honeycomb-digits
category: physics
null_test: not needed because deterministic arbitrary-precision transfer-matrix and CTM algorithms compute exact mathematical constants verified by Collatz-Wielandt bounds

## 1. Verbatim Target Bank Criteria
> Success means a decimal value of the square-lattice constant kappa (or the honeycomb constant) with D correct-looking decimals where D >= (longest published digit string for that constant, re-fetched live immediately before claiming: OEIS A085850 DATA plus any b-file for kappa; Baxter's 38 decimals for honeycomb) + 5, AND (a) two computations by independent methods (for example CTM at two different truncation sizes run to a fixed point, and a separate transfer-matrix or VUMPS/boundary-MPS calculation with Richardson-type extrapolation) agree on all D decimals, (b) both agree with the first 40 published decimals of kappa (36 for honeycomb), (c) the run logs show the claimed digits stable over at least the last three increases of truncation, and (d) an arXiv/Google Scholar/OEIS search finds no published value with D or more decimals. Direction: more digits. Disagreement with Baxter's flagged last two or three digits is allowed but must be stated explicitly.

## 2. Partial Wins (Verbatim)
- **p1:** A rigorous enclosure of kappa certifying at least 20 correct decimals (beyond the 15 certified by Friedland, Lundow and Markström), from Calkin-Wilf / Friedland-Peled transfer-matrix inequalities evaluated with exact rational or interval arithmetic, shipped with the eigenvalue certificates (Collatz-Wielandt vectors) so a skeptic can recheck the inequalities exactly.
- **p2:** At least 20 decimals, by two independent methods, of the hard-core (z = 1) entropy constant of the 4-8-8 lattice (Steven Finch, Errata and Addenda to Mathematical Constants, arXiv 2001.00578, Section 5.12, quotes only 1.54956010...) or of the 'triangular Kagome' lattice that Finch reports as still open; the lattice definition must match Finch's cited source.
- **p3:** Independent reproduction of Baxter's 43 decimals of kappa to at least 48 decimals that settles whether his last two or three digits are correct, reported either as confirmation or as a documented correction.

## 3. Preregistered Thresholds and Checkers
1. **Target Decimals ($D$):**
   - Live OEIS A085850 DATA has 43 decimal places:
     `1.5030480824753322643220663294755536893857810`.
   - We target $D \ge 43 + 5 = 48$ decimal digits (specifically certifying $D = 50$ to $65$ stable matching decimal digits).
2. **Two Independent Lenses:**
   - **Lens 1 (Baxter's Symmetric Corner Transfer Matrix Variational Equations / CTMRG):** Evaluated in 80-to-100-digit precision arithmetic (`mpmath`). Truncation parameter: bond dimension $\chi \in \{16, 20, 24, 28, 32, 36, 40\}$.
   - **Lens 2 (Boundary-MPS / Cylinder Strip Transfer Matrix Extrapolation):** Evaluated in 80-to-100-digit precision arithmetic (`mpmath`). Circumference $W \in \{6, 8, 10, 12, 14, 16, 18, 20, 24\}$ in cyclic translation and reflection orbit basis with Collatz-Wielandt bounding gap $< 10^{-50}$ and Richardson / Wynn-epsilon sequence extrapolation.
3. **Reproducibility Checks:**
   - Both methods must reproduce OEIS A006506 for $n \le 12$:
     $a(0)=1, a(1)=2, a(2)=7, a(3)=63, a(4)=1234, a(5)=55447, a(6)=5598861, a(7)=1280128950, a(8)=660647962955, a(9)=770548397261707, a(10)=2030049051145980050, a(11)=12083401651433651945979, a(12)=162481813349792588536582997$.
   - Both methods must reproduce all first 40 published digits of OEIS A085850:
     `1.5030480824753322643220663294755536893857`.
   - Settle Baxter's flagged last three digits (`810`).
   - Digits must be stable across $\ge 3$ truncation parameter increases.
4. **Rigorous Two-Sided Collatz-Wielandt Bounds (`p1`):**
   - For strip/cylinder transfer matrices $M$, export strictly positive certificate vectors $v > 0$ for $W \in \{16, 20, 24\}$.
   - Certify two-sided bounds $\min_i \frac{(Mv)_i}{v_i} \le \lambda \le \max_i \frac{(Mv)_i}{v_i}$.
   - Rigorous bounds certifying $\ge 20$ correct decimal digits of $\kappa$.
