# Preregistered Evaluation Bar (`monomer-dimer-square-lattice-constant-digits`)

frozen_utc: 2026-10-28T22:30:00Z
target_id: monomer-dimer-square-lattice-constant-digits
category: physics
null_test: not needed because deterministic arbitrary-precision transfer-matrix and CTMRG algorithms compute exact mathematical constants verified by Collatz-Wielandt bounds and exact OEIS A028420 counts

## 1. Verbatim Target Bank Criteria
> Success means a decimal value of h2 (natural log, per site) with at least 20 decimals such that (a) two independent methods agree on all claimed decimals (for example CTM or VUMPS on the monomer-dimer transfer operator, and exact strip transfer matrices of width up to about 24 with extrapolation), (b) the value lies inside Kong's bracket [0.662798972831, 0.662798972845] and agrees with 0.662798972834 to its 12 decimals up to final-digit rounding, (c) the digits are stable over at least three truncation increases, and (d) an arXiv/Google Scholar/OEIS search, re-run immediately before claiming, finds no published value with as many decimals. Direction: more digits.

## 2. Partial Wins (Verbatim)
- **p1:** A rigorous enclosure of h2 certifying at least 12 decimals (improving Friedland-Peled's 8 certified decimals and making Kong's bracket rigorous or not), via Friedland-Peled transfer-matrix inequalities evaluated in exact or interval arithmetic with published certificate vectors.
- **p2:** At least 15 decimals, by two independent methods, of the square-lattice monomer-dimer free energy at another standard monomer activity reported in the literature with fewer digits (for example Kong's fixed-density values f2(1/2) = 0.633195588930), stating the published comparator with its source.

## 3. Preregistered Thresholds and Checkers
1. **Target Decimals ($D$):**
   - We target $D \ge 24$ matching decimal digits (exceeding the required $\ge 20$ decimals).
2. **Two Independent Lenses:**
   - **Lens 1 (Symmetric CTMRG on the Vertex Tensor):** Evaluated in 80-digit precision arithmetic (`mpmath`). Truncation parameter: bond dimension $\chi \in \{8, 12, 16, 20, 24, 28, 32\}$.
   - **Lens 2 (Cylinder Transfer Matrix in Cyclic Orbit Basis with Sequence Extrapolation):** Evaluated in 80-digit precision arithmetic (`mpmath`). Truncation parameter: cylinder circumference $W \in \{8, 10, 12, 14, 16\}$.
3. **Reproducibility Checks:**
   - Both methods must reproduce OEIS A028420 for $n \le 14$:
     $a(1)=1, a(2)=7, a(3)=131, a(4)=10012, a(5)=2810694, a(6)=2989126727, a(7)=11945257052321, a(8)=179788343101980135, a(9)=10185111919160666118608, a(10)=2172138783673094193937750015, a(11)=1743829823240164494694386437970640, a(12)=5270137993816086266962874395450234534887, a(13)=59956919824257750508655631107474672284499736089, a(14)=2567773069787030667011494675812637832667677810219203068$.
   - Both methods must produce values falling strictly inside Kong's bracket $[0.662798972831, 0.662798972845]$ and agreeing with $0.662798972834$ to 12 decimals.
   - Both methods must agree on all $D \ge 24$ decimal places.
   - Digits must be stable across $\ge 3$ consecutive truncation parameter increases.
4. **Rigorous Two-Sided Collatz-Wielandt Bounds (`p1`):**
   - For transfer matrices $M$, export strictly positive certificate vectors $v > 0$.
   - Certify two-sided bounds $\min_i \frac{(Mv)_i}{v_i} \le \lambda \le \max_i \frac{(Mv)_i}{v_i}$.
   - Rigorous enclosure on $h_2$ certifying $\ge 12$ correct decimal digits.
