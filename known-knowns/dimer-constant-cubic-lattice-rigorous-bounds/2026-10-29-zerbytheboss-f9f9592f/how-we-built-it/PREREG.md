# PREREG: dimer-constant-cubic-lattice-rigorous-bounds

Date: 2026-10-29T21:10:00Z

## Frozen Success Criterion
Success means a rigorous bound on $\lambda_3$ that is strictly smaller than the best published bound $\lambda_3 \le 0.452130$ (Qidong He, arXiv:2607.28810v2, 2026-08-11), by at least $10^{-6}$ (i.e. $\lambda_3 \le 0.452129$), together with a machine-checkable certificate: the explicit strictly positive integer test vector $v \in \mathbb{N}_{>0}^{N}$, the exact rational/integer Collatz-Wielandt constant $C$, verified by exact integer cross-multiplication:
$$(X_{m,n}^{(i)} Y_{m,n}^{(i)} v)_k \le C \cdot v_k \quad \forall k \in \{0, \dots, N-1\}$$
yielding $\lambda_3 \le \frac{1}{2mn}\log C \le 0.452129$ rounded outward.

## Partial Win Criteria
- **p1:** Independent reproduction of He (2026) Table 2 bounds up to $(5,5)$ to six decimals (rounded upward).
- **p2:** Certified improvement of 3D monomer-dimer entropy $h_3$ bracket $[0.7849602275, 0.7862023450]$.
- **p3:** Certified upper bound on the dimer constant of $\mathbb{Z}^4$ improving $[0.5338, 0.6238]$ (yielding $\lambda_4 \le 0.596949$).

## Methodology & Preregistered Estimators
1. **Lattice & Diagonal Transfer Formulation**:
   - Graph $\mathbb{T}_{m,n,l} = \mathbb{Z}^3 / \Lambda_{m,n,l}$ with diagonal layers $L_k$ of height $k$.
   - Forward displacement set $D = \{(0,0), (1,0), (0,1)\} \subset V_{m,n}$.
   - Transfer matrix entry $\bra{U} T_{m,n} \ket{V} = \operatorname{per} A_{m,n}[U, V_{m,n} \setminus V]$ if $|U| + |V| = mn$, else 0.
2. **Symmetry Quotient**:
   - $G_{m,n} = V_{m,n} \rtimes K_{m,n}$ with linear automorphisms $K_{m,n}$ from He Table 1.
   - Orbits of subsets under $G_{m,n}$ decompose into sectors $i = 0, \ldots, \lfloor mn/2 \rfloor$.
3. **Collatz-Wielandt Iterations & Lanczos Polish**:
   - Compute matrix-free block products $Y_{m,n}^{(i)} v$ and $X_{m,n}^{(i)} w$ via bitmask injective matching enumeration.
   - For $(5,5)$, compute $p=3, 4$ iterates or Lanczos Perron eigenvector, scale to positive integers $v \in \mathbb{N}_{>0}^{35070}$.
   - Evaluate exact integer bounds $(X Y v)_k \le C v_k$.
4. **Independent Skeptic Verification**:
   - Independent verification binary recomputing transitions directly from $D$ and checking $(X Y v)_k \le C v_k$ with exact integer cross-multiplication.
   - Zero floating-point rounding errors permitted.

null_test: not needed because all transfer matrices, symmetry orbits, and Collatz-Wielandt ratio checks are deterministic mathematical operations verified against published values in He (2026) Table 2 and exact algebraic theorems.
