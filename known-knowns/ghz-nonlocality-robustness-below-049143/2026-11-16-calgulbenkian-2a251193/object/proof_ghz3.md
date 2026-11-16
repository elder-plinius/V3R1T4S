# Rigorous Proof of $v^* \le 0.49139712 < 0.49142$ for Three-Qubit GHZ White-Noise Nonlocality

## Theorem

Let $|\mathrm{GHZ}_3\rangle = \frac{1}{\sqrt{2}}(|000\rangle + |111\rangle) \in (\mathbb{C}^2)^{\otimes 3}$ and let

$$\rho(v) = v |\mathrm{GHZ}_3\rangle\langle\mathrm{GHZ}_3| + (1 - v) \frac{I_8}{8}, \qquad v \in [0, 1].$$

There exists an explicit tripartite binary-outcome Bell functional $\mathcal{B} = \sum_{i=0}^{17} \sum_{j=0}^{23} \sum_{k=0}^{71} M_{ijk} A_i \otimes B_j \otimes C_k$ with exact integer coefficients $M_{ijk} \in \mathbb{Z}$ (`object/bell_ghz3_18x24x72.json`) and $(m_A, m_B, m_C) = (18, 24, 72)$ projective qubit observables on $(\mathbb{C}^2)^{\otimes 3}$ such that:

1. **Exact deterministic local bound**: Over all deterministic local hidden-variable strategies $(a, b, c) \in \{\pm 1\}^{18} \times \{\pm 1\}^{24} \times \{\pm 1\}^{72}$,
   $$L = \max_{a, b, c} \sum_{i=0}^{17} \sum_{j=0}^{23} \sum_{k=0}^{71} M_{ijk} a_i b_j c_k = 130\,692\,616.$$
2. **Exact white-noise expectation**: $Q_{\text{noise}} = \mathrm{Tr}((I_8 / 8) \mathcal{B}) = 0$.
3. **55-digit certified GHZ expectation**:
   $$Q_{\text{GHZ}} = \langle \mathrm{GHZ}_3 | \mathcal{B} | \mathrm{GHZ}_3 \rangle \in [265\,961\,302.907030467068957871517, \; 265\,961\,302.907030467068957871518].$$
4. **Critical visibility upper bound**:
   $$v^* = \frac{L - Q_{\text{noise}}}{Q_{\text{GHZ}} - Q_{\text{noise}}} \in [0.4913971114274656713239021, \; 0.4913971114274656713239022] < 0.49142 = 0.49143 - 10^{-5}.$$

Hence $\rho(v)$ violates a Bell inequality with finitely many projective measurements for every $v > 0.4913971114274656713239022$.

---

## Step 1: Projective Measurements and Quantum Expectations

Define the single-qubit observables for Parties A, B, and C by

$$A_i = \cos\alpha_i \, \sigma_x + \sin\alpha_i \, \sigma_y \quad \left(\alpha_i = \frac{i\pi}{18},\; 0 \le i \le 17\right),$$

$$B_j = \cos\beta_j \, \sigma_x + \sin\beta_j \, \sigma_y \quad \left(\beta_j = \frac{j\pi}{24},\; 0 \le j \le 23\right),$$

$$C_k = \cos\gamma_k \, \sigma_x + \sin\gamma_k \, \sigma_y \quad \left(\gamma_k = \frac{k\pi}{72},\; 0 \le k \le 71\right).$$

Each operator is Hermitian, traceless ($\mathrm{Tr}(A_i) = \mathrm{Tr}(B_j) = \mathrm{Tr}(C_k) = 0$), and satisfies $O^2 = (\cos^2\phi + \sin^2\phi) I_2 = I_2$ identically, so its eigenvalues are $\pm 1$ (valid binary projective qubit observables). Because $\mathrm{Tr}(A_i \otimes B_j \otimes C_k) = \mathrm{Tr}(A_i)\mathrm{Tr}(B_j)\mathrm{Tr}(C_k) = 0$, the white-noise value is $Q_{\text{noise}} = \frac{1}{8} \mathrm{Tr}(\mathcal{B}) = 0$.

For any planar observable $\sigma_\phi = \cos\phi\,\sigma_x + \sin\phi\,\sigma_y$, we have $\sigma_\phi |0\rangle = e^{i\phi}|1\rangle$ and $\sigma_\phi |1\rangle = e^{-i\phi}|0\rangle$. Therefore

$$\langle \mathrm{GHZ}_3 | A_i \otimes B_j \otimes C_k | \mathrm{GHZ}_3 \rangle = \frac{1}{2}\left(e^{i(\alpha_i + \beta_j + \gamma_k)} + e^{-i(\alpha_i + \beta_j + \gamma_k)}\right) = \cos\!\left(\frac{(4i + 3j + k)\pi}{72}\right).$$

---

## Step 2: Explicit Integer Bell Tensor $M_{ijk}$

Let $w = (w_0, \dots, w_{35}) \in \mathbb{Z}^{36}$ be the exact integer vector stored in `object/bell_ghz3_18x24x72.json` (`w_int`). Define $F : \mathbb{Z}_{144} \to \mathbb{Z}$ by

- $F(s) = w_s$ for $0 \le s \le 35$,
- $F(36) = 0$,
- $F(s) = -w_{72 - s}$ for $37 \le s \le 72$,
- $F(s) = F(144 - s)$ for $73 \le s \le 143$.

By construction, $F$ satisfies antiperiodicity $F(s + 72) = -F(s)$ and evenness $F(-s \bmod 144) = F(s)$ for all $s \in \mathbb{Z}_{144}$. Set

$$M_{ijk} = F((4i + 3j + k) \bmod 144) \in \mathbb{Z} \qquad (0 \le i < 18,\; 0 \le j < 24,\; 0 \le k < 72).$$

Evaluating $Q_{\text{GHZ}} = \sum_{i,j,k} M_{ijk} \cos\!\left(\frac{(4i + 3j + k)\pi}{72}\right)$ in 55-digit outward-rounded interval arithmetic (`mpmath.iv`, cross-checked against explicit Pauli-matrix contractions in `verify-it-yourself/verify_ghz3.py`) gives the claimed enclosure for $Q_{\text{GHZ}}$.

---

## Step 3: Exact Symmetry Reduction to $D_{36} \times C_{48}$ Orbit Pairs

By convexity (Bauer's maximum principle), the classical local maximum over shared-randomness strategies equals the maximum over deterministic strategies $(a, b, c) \in \{\pm 1\}^{18} \times \{\pm 1\}^{24} \times \{\pm 1\}^{72}$. Optimizing analytically over $c_k \in \{\pm 1\}$ for each $k$ gives

$$L = \max_{a \in \{\pm 1\}^{18},\, b \in \{\pm 1\}^{24}} L(a, b), \qquad L(a, b) := \sum_{k=0}^{71} \left| \sum_{i=0}^{17} \sum_{j=0}^{23} M_{ijk} a_i b_j \right|.$$

For any $m \ge 2$ and $x \in \{\pm 1\}^m$, define its antiperiodic extension $\tilde{x} : \mathbb{Z}_{2m} \to \{\pm 1\}$ by $\tilde{x}_r = x_r$ ($0 \le r < m$) and $\tilde{x}_{r+m} = -x_r$. Define the antiperiodic shift $T_m : \{\pm 1\}^m \to \{\pm 1\}^m$ and antiperiodic reflection $R_m : \{\pm 1\}^m \to \{\pm 1\}^m$ via

$$(\widetilde{T_m x})_r = \tilde{x}_{r+1}, \qquad (\widetilde{R_m x})_r = \tilde{x}_{-r} \qquad (r \in \mathbb{Z}_{2m}).$$

Clearly $T_m^{2m} = \mathrm{id}$, $R_m^2 = \mathrm{id}$, and $R_m T_m R_m = T_m^{-1}$, so $\langle T_m \rangle \cong C_{2m}$ and $\langle T_m, R_m \rangle \cong D_{4m}$.

**Lemma (Exact Invariance of $L(a, b)$).** For all $a \in \{\pm 1\}^{18}$ and $b \in \{\pm 1\}^{24}$:
1. $L(T_{18} a, b) = L(a, b)$ and $L(a, T_{24} b) = L(a, b)$.
2. $L(R_{18} a, R_{24} b) = L(a, b)$.

*Proof.* Using $F(s + 72) = -F(s)$, extend $S_k(a, b) := \sum_{i=0}^{17} \sum_{j=0}^{23} F(4i + 3j + k) a_i b_j$ to $k \in \mathbb{Z}_{144}$ via

$$S_k(a, b) = \frac{1}{4} \sum_{i \in \mathbb{Z}_{36}} \sum_{j \in \mathbb{Z}_{48}} F(4i + 3j + k) \tilde{a}_i \tilde{b}_j, \qquad L(a, b) = \frac{1}{2} \sum_{k \in \mathbb{Z}_{144}} |S_k(a, b)|.$$

- Replacing $a$ by $T_{18} a$ substitutes $\tilde{a}_{i+1}$ for $\tilde{a}_i$. Setting $i' = i + 1 \in \mathbb{Z}_{36}$ shifts $4i + 3j + k = 4i' + 3j + (k - 4)$, so $S_k(T_{18} a, b) = S_{k - 4}(a, b)$, leaving $\sum_{k \in \mathbb{Z}_{144}} |S_k|$ unchanged. Similarly, $S_k(a, T_{24} b) = S_{k - 3}(a, b)$, proving (1).
- Replacing $(a, b)$ by $(R_{18} a, R_{24} b)$ substitutes $i' = -i \in \mathbb{Z}_{36}$ and $j' = -j \in \mathbb{Z}_{48}$. Since $F(-s) = F(s)$, $F(-4i' - 3j' + k) = F(4i' + 3j' - k)$, giving $S_k(R_{18} a, R_{24} b) = S_{-k}(a, b)$ and leaving $\sum_{k \in \mathbb{Z}_{144}} |S_k|$ unchanged, proving (2). $\blacksquare$

**Corollary (Reduction to $\mathcal{C}_A^{\text{red}} \times \mathcal{C}_B$).** Let $\mathcal{C}_A^{\text{red}} \subset \{\pm 1\}^{18}$ contain one representative from each $D_{36}$-orbit under $\langle T_{18}, R_{18} \rangle$, and let $\mathcal{C}_B \subset \{\pm 1\}^{24}$ contain one representative from each $C_{48}$-orbit under $\langle T_{24} \rangle$. Then

$$\max_{a \in \{\pm 1\}^{18},\, b \in \{\pm 1\}^{24}} L(a, b) = \max_{a^* \in \mathcal{C}_A^{\text{red}},\, b^* \in \mathcal{C}_B} L(a^*, b^*).$$

*Proof.* Given any $(a, b)$, pick $a^* \in \mathcal{C}_A^{\text{red}}$ in the $D_{36}$-orbit of $a$. Either $a^* = T_{18}^\alpha a$ (set $b' = b$) or $a^* = T_{18}^\alpha R_{18} a$ (set $b' = R_{24} b$); by the Lemma, $L(a, b) = L(a^*, b')$. Letting $b^* = T_{24}^\beta b' \in \mathcal{C}_B$ represent the $C_{48}$-orbit of $b'$, the Lemma gives $L(a^*, b') = L(a^*, b^*)$. $\blacksquare$

By Burnside's Lemma (verified both analytically and by full domain partition in `certify_orbits_b.cpp`):

- $|\{\pm 1\}^{18} / C_{36}| = \frac{1}{36}(2^{18} + 6 \cdot 2^2 + 2 \cdot 2^6) = \frac{262\,296}{36} = 7\,286$,
- $|\{\pm 1\}^{18} / D_{36}| = \frac{1}{72}(262\,296 + 18 \cdot 2^9) = \frac{271\,512}{72} = 3\,771 = |\mathcal{C}_A^{\text{red}}|$,
- $|\{\pm 1\}^{24} / C_{48}| = \frac{1}{48}(2^{24} + 2 \cdot 2^8) = \frac{16\,777\,728}{48} = 349\,536 = |\mathcal{C}_B|$,
- $|\mathcal{C}_A^{\text{red}}| \times |\mathcal{C}_B| = 3\,771 \times 349\,536 = 1\,318\,100\,256$.

Exhaustively evaluating $L(a^*, b^*)$ across all $1\,318\,100\,256$ orbit pairs using two completely independent C++17 implementations (`certify_orbits_a.cpp` on minimum-bitmask representatives via Four-Russians byte tables, and `certify_orbits_b.cpp` on disjoint maximum-bitmask representatives via 64-bit incremental Hamming-diff updates) yields the identical exact integer maximum $L = 130\,692\,616$, completing the proof. $\blacksquare$
