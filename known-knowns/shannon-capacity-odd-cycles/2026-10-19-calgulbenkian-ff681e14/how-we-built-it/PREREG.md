# Preregistration: `shannon-capacity-odd-cycles` (Wave 6)

## 1. Problem Statement & Win Conditions

For an odd cycle $C_m$ ($m \ge 7$ odd) with vertex set $\mathbb{Z}_m = \{0, 1, \dots, m-1\}$, the $d$-th strong power $C_m^{\boxtimes d}$ has vertex set $\mathbb{Z}_m^d$, where two distinct vertices $u, v \in \mathbb{Z}_m^d$ are adjacent (confusable) if and only if
$$\min\bigl((u_i - v_i) \bmod m,\; (v_i - u_i) \bmod m\bigr) \le 1 \quad \forall i \in \{1, \dots, d\}.$$
The Shannon capacity is
$$\Theta(C_m) = \sup_{d \ge 1} \alpha(C_m^{\boxtimes d})^{1/d} = \lim_{d \to \infty} \alpha(C_m^{\boxtimes d})^{1/d}.$$

### Live 2026 Records to Beat
Across all 2026 sources (`constants/9a.md`, Tandon `arXiv:2608.30273` [30 Aug 2026], Buys–Polak–Zuiddam `arXiv:2607.29681` & `spectra-research/shannon-capacity-lean` commit `aa21eeb12b75` [10 Aug 2026], Gao `arXiv:2607.27869`, and Itty–Rosin–Carstensen–Reichman `arXiv:2607.21517`), the maximum published lower bounds are:

- **$\Theta(C_7)$**: `3.25883262035326630912153905181047543760538759432195...` (Tandon `arXiv:2608.30273`, Theorem 2, $d = 500$; exceeds BPZ Lean v2 `3.25882798592000703452...`).
- **$\Theta(C_9)$**: `4.3267487109222245...` ($81^{1/3}$ from Baumert et al. 1971).
- **$\Theta(C_{11})$**: `5.295492315784620...` (BPZ Lean v2 `CertC11.lean`, $d = 207$; exceeds BPZ v1 `5.294502522149` and Itty et al. $21909^{1/6} \approx 5.289773$).
- **$\Theta(C_{13})$**: `6.302926729310108...` (BPZ Lean v2 `CertC13.lean`, $d = 522$; exceeds BPZ v1 `6.302455083464` and Itty et al. $62530^{1/6} \approx 6.300109$).
- **$\Theta(C_{15})$**: `7.301628695930103...` (BPZ Lean v2 `CertC15.lean`, $d = 3664$; exceeds BPZ v1 `7.301600534487` and Itty et al. $8076974^{1/8} \approx 7.301399$).
- **$\Theta(C_{19})$**: `9.357200030000796...` (BPZ Lean v2 `CertC19.lean`, $d = 11856$; exceeds BPZ v1 `9.357192705918`).
- **$\Theta(C_{21})$**: `10.347918137743866753257838343154...` ($11466^{1/4}$ from BPZ Lean v2 `CosetC21.lean`, $d = 4$; exceeds BPZ v1 `10.342455853338`).
- **$\Theta(C_{23})$**: `11.334557922754518...` (BPZ Lean v2 `CertC23.lean`, $d = 3040$; exceeds BPZ v1 `11.328224257774`).

### Win Tiers
1. **Full Win**: An explicit independent set $S \subset C_m^{\boxtimes d}$ ($m \ge 7$ odd) or a fully specified, finite-certificate-verified recursive construction giving $\Theta(C_m) \ge |S|^{1/d}$ (computed with exact integer bisection / `mpmath` to $\ge 50$ digits) **strictly greater** than the maximum 2026 lower bound for that $m$ across all sources above.
2. **Partial Win `p1`**: An explicit independent set in $C_7^{\boxtimes 10}$ of size $> 134,753$ (`Itty et al. 2026`), verified by exhaustive check.
3. **Partial Win `p2`**: An explicit independent set in $C_{15}^{\boxtimes 5}$ of size $> 19,946$ (`X-evolve`), verified by exhaustive check.
4. **Partial Win `p3`**: A fixed-dimension independence record $\alpha(C_m^{\boxtimes d})$ for odd $m \ge 9$ exceeding all published values (e.g., $\alpha(C_{11}^{\boxtimes 4}) > 766$, $\alpha(C_{13}^{\boxtimes 4}) > 1,535$, $\alpha(C_{15}^{\boxtimes 3}) > 383$, $\alpha(C_{21}^{\boxtimes 4}) > 11,466$, $\alpha(C_{23}^{\boxtimes 4}) > 16,501$), verified by exhaustive check.

## 2. Attack Strategy & Verification Protocol

1. **Attack 1 ($\Theta(C_7)$ World Record via Improved Heterogeneous Certificates & BPZ DAG Optimization)**:
   - Optimize 1-for-1 and multi-vertex exchanges on $J^+ \subset C_7^{\boxtimes 10}$ and automorphisms on $J^+$, $J_{15}$, and $J_{30}^{++}$ to strictly increase $(C_1, C_2, C_4)$, and optimize the heterogeneous + BPZ substitution DAG to strictly beat Tandon's 500-dimensional bound `3.25883262035326630912153905181047543760538759432195`.
   - Every finite certificate is derived from scratch from explicit codebooks and checked by exact integer arithmetic and bitset neighborhood verification.
2. **Attack 2 ($\Theta(C_{11}), \Theta(C_{13}), \Theta(C_{15}), \Theta(C_{19}), \Theta(C_{21}), \Theta(C_{23})$ World Records)**:
   - Apply Tandon's heterogeneous recursion (`hetgao`) and deeper/weighted BPZ substitution schedules (`S2a, S2b, S3a..S3h`, `K3a, K4a, K4b`) to the certified base port systems of $C_{11}, C_{13}, C_{15}, C_{19}, C_{23}$, and construct a port system or larger fixed-dimension code on $C_{21}^{\boxtimes 4}$.
3. **Attack 3 (Fixed-Dimension Explicit Independent Sets for `p1`, `p2`, `p3`)**:
   - Fast C bitset conflict-guided Large Neighborhood Search (`delete-k / add-(k+1)` and tabu plateau search) on $C_7^{\boxtimes 10}$ (`> 134,753`), $C_{15}^{\boxtimes 5}$ (`> 19,946`), and $C_{11}^{\boxtimes 4}, C_{13}^{\boxtimes 4}, C_{15}^{\boxtimes 3}, C_{21}^{\boxtimes 4}, C_{23}^{\boxtimes 4}$.
   - Every finite independent set is saved as a plain-text list of integer $d$-tuples and verified by a standalone script `results/verify_shannon.py`.
