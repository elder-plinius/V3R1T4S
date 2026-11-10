# Baseline Record & Upstream Provenance (`magic-state-distillation-fewest-qubits`)

## 1. Upstream Sources, Fetch Timestamps & SHA-256 Checksums

- **Target Problem Card**: `magic-state-distillation-fewest-qubits` (`★★☆☆☆` Physics)
- **Primary Paper & Official Repository (`arXiv:2606.07734v2`)**:
  - H. R.amedani Jacinto, X. Valcarce, N. Sangouard, *Compact Magic State Distillation*, `https://arxiv.org/abs/2606.07734v2` (`Matrices.tex` sha256: `9f28188732419eb59564e78102dc61a37ee0fc29e378a1474bd36f5df183bb08`, fetched `2026-11-10T09:53:12Z`)
  - `https://github.com/xvalcarce/compact_distillation` (commit `e9e2a9881bf5f4d8627424a6f49e8a2e6416c9f6`, fetched `2026-11-10T09:53:40Z`)
- **Companion Classification Repositories**:
  - A. Wills, M.-H. Hsieh, H. Yamasaki, *Generalised Triorthogonal Codes*, `https://arxiv.org/abs/2609.30860`, `https://github.com/AWillsQuantum/generalised_triorthogonal_classification` (commit `3f70a6bc9910e628b691ab43b11637e7cd00d9be`, `data/protocols/pareto_frontier.json` sha256: `5a54a0b8c52862e391b7c3754a57c6a27ca070cb2cc90b22022923b16eb9268a`, fetched `2026-11-10T09:54:05Z`)
  - S. Jain, *Magic State Factory Catalogue*, `https://arxiv.org/abs/2610.06535v1`, `https://github.com/shubhamj810/magic-state-factory-repo` (commit `612937f92b70ec6f2fb77ec8e71f146a9dc6562e`, `master_catalog/master_catalog.json` sha256: `e38a5e0d4196b45bc0fa577a3ab3bd40b3847f69a2eb0fc2f4868ca0ef43f714`, fetched `2026-11-10T09:54:38Z`)
  - V. Gillot & P. Langevin, *Classification of $\mathrm{RM}(3, 7)$ under $\mathrm{AGL}(7, 2)$*, `http://langevin.univ-tln.fr/project/agl7/data/B-0-3-7.dat` (`sha256: c51042c240417be3915a7bf8ca4fd34d0df5e4309545c3cf6c4c63c9e95f75b7`, fetched `2026-11-10T09:59:10Z`)

## 2. Prior State of the Art vs. Our Certified Results (`p1`, `p2` & Structural Theorems)

| Problem Stratum | Published Status (`arXiv:2606.07734v2`, `2609.30860`, `2610.06535v1`) | Our Certified Contribution |
|---|---|---|
| **Milestone `p1`: $N_{\text{CCZ}}(4)$ ($T$-to-$\text{CCZ}$ at distance $d \ge 4$)** | $9 \le N_{\text{CCZ}}(4) \le 10$; $N=9$ ruled out only up to $n \le 54$ (`2609.30860`), leaving $55 \le n \le 63$ open (`2606.07734v2` Table I) | **Proves $N_{\text{CCZ}}(4) = 10$ across all $1 \le n \le 63$ (`Master Theorem 2`)**: exact $\mathrm{RM}(2, 6)$ weight enumerator has `0` codewords in $[49, 63]$, $n=63$ has collinear rank `57/63` ($\dim(V_4/L_X) = 0 < 3$), and all `912` pointed supports for $m \le 6$ have `0` SAT hits (matched by `W1_48T_to_1CCZ_N10_d4`) |
| **Milestone `p2`: $N_T(4)$ ($T$-to-$T$ at distance $d \ge 4$ on $N = 8$ qubits)** | $8 \le N_T(4) \le 10$; $N = 8, d = 4$ SAT search in `2606.07734v2` timed out after 2 months across $55 \le n \le 127$ | **Proves $N_T(4) \ge 9$ across all $1 \le n \le 127$ (`Master Theorem 1 & 5`)**: self-contained Three-Handle $\mathrm{RM}(3, 7)$ certificate (`3,486` orbits, `6,074,355` disjoint pairs, exact $2^{64}$ orbit mass, and `446,208` shifted supports with `0` SAT hits) verified in `~9s` |
| **Pipeline Control: $N = 7, d \ge 4$ $T$-to-$T$** | Known UNSAT up to $n \le 54$ (`2609.30860`) | **Verified UNSAT across all $1 \le n \le 63$** (`0` SAT hits across all `912` pointed supports of $m \le 6$) |
| **Structural Laws (`Master Theorems 3a, 3b & 4`)** | Empirical observations of $(52, 10, 4) \to (53, 11, 5)$ and $(64, 10, 4) \to (65, 11, 5)$ | **Hyperplane Parity Split Law (`3a`)** ($u_0$ odd, $u_1$ even across all $2^r - 1$ covectors), **98.8% Collinearity Locking (`3b`)** (`3,090 / 3,127` classes of weight $\ge 56$ locked), and **Parity-Extension Lifting Theorem (`4`)** |
