# How We Built It — Technical Artifact (`magic-state-stabilizer-rank-exponents`)

## 1. Overview of the Four Mathematical Engines

1. **Master Theorem 55 (The 135-Tableau Pauli-Fiber & Bitwise-XOR Slice Homomorphism on $D_3$):**
   - Every 3-qubit stabilizer state in $D_3$ (`1,080` states across `51` affine flats of $\mathbb{F}_2^3$: `8` of dim 0, `28` of dim 1, `14` of dim 2, `1` of dim 3) has quadratic form $Q$, linear phase $l \in \{0,1,2,3\}^3$, and affine shift $c \in \mathbb{F}_2^3$.
   - Grouping by $(W, Q, l \bmod 2)$ partitions $D_3$ into **135 Pauli-Tableau Fibers of 8 states each** ($135 \times 8 = 1,080$), indexed within each fiber by $k \in \mathbb{F}_2^3$.
   - When any 5-qubit stabilizer state $|\phi\rangle \in D_5$ is sliced across the first two qubits $u \in \{00, 01, 10, 11\}$, all active 3-qubit slices lie inside the **same** 8-state Pauli-Tableau Fiber and satisfy the exact bitwise-XOR relation $k(11) = k(00) \oplus k(01) \oplus k(10)$.
   - Coupled with the $G_3 = S_3 \ltimes \text{Stab}_{\mathcal{C}_1}^3$ unitary symmetry group (`|G_3| = 162` for $|F\rangle$, `|G_3| = 48` for $|T\rangle$), this reduces the rank-4 slice cover test at $m=5,6$ to `2,372` (`qubit_T`) and `2,406` (`qubit_H`) orbit representatives of 4-covers on $u=00$, all of which leave `0` surviving 5-qubit stabilizer completions (`Certs #1 & #2`, proving $\chi(|F\rangle^{\otimes 5,6}) \ge 5$ and $\chi(|T\rangle^{\otimes 5,6}) \ge 5$).

2. **Master Theorem 52 (Even-Qubit Slice Theorem for $|CS\rangle^{\otimes 3}$):**
   - Applying $P_{000} = (\langle 0|_{A_1}\langle 0|_{A_2}\langle 0|_{A_3}) \otimes I_{B_1 B_2 B_3}$ to $|CS\rangle^{\otimes 3}$ projects onto the unentangled single-qubit magic product state $|\psi_0\rangle^{\otimes 3} = (2|0\rangle + (1+i)|1\rangle)^{\otimes 3} \in \mathbb{Z}[i]^8$.
   - Exhaustive 2-tuple and $S_3$-reduced 3-tuple checks over $D_3$ (`1,080` states) prove `rank2_hits = 0` and `rank3_hits = 0`, while the explicit 4-state decomposition `idx = [0, 7, 568, 624]` with weights `[4, -2+2i, 2+2i, 2-2i]` matches $|\psi_0\rangle^{\otimes 3}$ with `0` integer residual (`Cert #3`, proving $\chi(|\psi_0\rangle^{\otimes 3}) = 4$).

3. **Master Theorem 42B (Complete Untwisted $\mathbb{Z}_4$-Cycle Rank-6 Obstruction for Qutrit $|H_3\rangle^{\otimes 4}$):**
   - Under the 4-qubit cyclic shift $g(x_0, x_1, x_2, x_3) = (x_1, x_2, x_3, x_0)$ on $\mathbb{F}_3^4$, there are exactly `[9, 48, 58, 16, 1]` ($132$ total) $g^2$-invariant affine flats supporting `192` $g$-fixed qutrit stabilizer states and `6,960` untwisted 2-state pair orbits $|\phi\rangle + g|\phi\rangle$.
   - Projecting modulo the 2D Galois target plane $\text{span}(|H_3^+\rangle^{\otimes 4}, |H_3^-\rangle^{\otimes 4})$ proves `max_k3_run = 2 < 3`, `k4_hits = 0`, and `hits_1p4f = 0` across all `144` Off-Fixed pair orbits (`Cert #4`).

4. **Master Theorem 54 (Gaussian-Rational Contraction of Face-Cat States $|\text{cat}_{2k}(F)\rangle$ & 2D $\mathbb{Z}[i, \sqrt{3}]$ Galois LNS):**
   - For $|F\rangle \propto 2|0\rangle + (\sqrt{3}-1)(1+i)|1\rangle$, the Galois conjugate is $|\bar{F}\rangle = Z|F\rangle$. Therefore $|\text{cat}_{2k}(F)\rangle = \frac{1}{2}(|F\rangle^{\otimes 2k} + (Z|F\rangle)^{\otimes 2k})$ supported on even Hamming weights contracts the $\sqrt{3}$ radical completely (`(-1 + i)^w` for even $w$), lying strictly inside $\mathbb{Q}(i)^{2^{2k}}$!
   - Consequently, $\chi(|\text{cat}_6(F)\rangle) = 3 < 6 = \chi(|F\rangle^{\otimes 6})$ (`W03..W04`) and $\chi(|\text{cat}_{10}(F)\rangle) \le 9 < 15$ (`W06..W07`), and our 2D $\mathbb{Z}[i, \sqrt{3}]$ Galois-split LNS discovers new non-product rank-6 decompositions of $|F\rangle^{\otimes 6}$ (`W08..W09`) and 2-block rank-9 decompositions of $|F\rangle^{\otimes 7}$ (`W10`).
