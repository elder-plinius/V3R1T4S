# Panelist Report: REPRODUCE (`ame-states-open-cells-huber-table`, Part II: `2026-10-21-mizopl-d1cb5926`)

context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
target_id: ame-states-open-cells-huber-table

## 1. Quoted Mathematical Definitions and Mandate

Per the V3R1T4S `REPRODUCE` panelist mandate, all 28 certificates in `object/` were independently verified from first-principles mathematical definitions of Absolutely Maximally Entangled states $\operatorname{AME}(n, D)$, pure graph states $\lvert G\rangle$ over $\mathbb{F}_q$ and $\mathbb{Z}_D$, Hermitian/Euclidean self-dual $[2k, k, k+1]_{q^2}$ MDS codes, and Stabilizer-MDS entangled couplings over $\mathbb{Q}(\zeta_5)$:

1. **Graph-State Cut-Rank Criterion (Schlingemann 2002; Helwig et al. 2012):** A symmetric hollow adjacency matrix $\Gamma \in R^{n \times n}$ over a commutative ring $R$ ($\mathbb{F}_q$ or $\mathbb{Z}_D$) defines an $\operatorname{AME}(n, D)$ graph state (`[[n, 0, k+1]]_D` where $k = \lfloor n/2 \rfloor$) if and only if for every $k$-party subset $S \subset \{0, \dots, n-1\}$ ($\lvert S\rvert = k$), the $(n-k) \times k$ off-diagonal submatrix $\Gamma_{S^c, S}$ has full column rank $k$ over every residue field $\mathbb{F}_p$ ($p \mid D$).
2. **Hermitian / Euclidean Self-Dual MDS Code Criterion (Rains 1999; Ketkar et al. 2006):** For $n = 2k$, a systematic generator matrix $G = [I_k \mid U]$ over $\mathbb{F}_{q^2}$ defines an $\operatorname{AME}(2k, q)$ (`[[2k, 0, k+1]]_q`) stabilizer state if $U U^\dagger = -I_k$ (Hermitian self-dual, or $U U^\dagger = I_k$ in characteristic $2$, or $U U^T = \pm I_k$ over $\mathbb{F}_{q^2}$ yielding $\operatorname{AME}(2k, q^2)$) and every $r \times r$ square submatrix of $U$ ($1 \le r \le k$, total $\sum_{r=1}^k \binom{k}{r}^2 = \binom{2k}{k} - 1$ minors) has non-zero determinant in $\mathbb{F}_{q^2}^\times$.

---

## 2. File Integrity & Checksum Verification of All 28 `object/` Certificates

All 28 JSON certificates in `object/` were hashed and verified before executing any verification routine:

| File | Verified Bytes | Verified SHA-256 |
|---|---:|---|
| `object/ame_10_10_shortened_binary_stabilizer_certificate.json` | `3,499` | `b720ce506d1839bfbdfc3ad55141c04fdcb6d211f17c746551484fe45c5fd5ab` |
| `object/ame_13_5_quantum_mds_13_1_7_certificate.json` | `6,437` | `87f2c3d21cf8eb399cd86e24ea59f7e474ec3f5b2bf6cc38786bd7f75a7a40fd` |
| `object/ame_15_5_impurity_and_circulant_nogo_certificate.json` | `2,620` | `cbba73c92693572b709824ec50ff920b51ee8fc44bcfadee81e672067a9f60e6` |
| `object/ame_15_7_pure_circulant_certificate.json` | `1,459` | `0f52a39f008990cc838d37ccea061405387f7c0be5b641bc12f709e735e07575` |
| `object/ame_15_8_pure_circulant_certificate.json` | `3,293` | `5748900e8ca81df578ab6d502db90c9ca3e8853f9a7d0f290d066d0d56985ecd` |
| `object/ame_15_9_pure_circulant_certificate.json` | `551` | `86551558a3a4077551d953f71638a319497b427f61681b4c2cc7403ff024c266` |
| `object/ame_16_11_pure_hermitian_constacyclic_graph_certificate.json` | `3,554` | `0ea466b6539da517aae44d2551799fd70af0571e62e84b831b7001572fb3aa4f` |
| `object/ame_16_13_pure_hermitian_constacyclic_graph_certificate.json` | `3,474` | `c344aec0c2f38aeed16e18ac3ed69dbb4d124b91b81f74e1979c3a82ef81d23b` |
| `object/ame_16_16_pure_d8_double_circulant_certificate.json` | `3,655` | `4a23dd161482a2457337811515591b51a0d8f03516169bb5c2e4a956ba776f74` |
| `object/ame_16_17_pure_d8_double_circulant_certificate.json` | `3,776` | `24d0e8d97217f3201275b4333d2352dac3b4b52fab88745b5e80374242271a81` |
| `object/ame_16_19_pure_d8_double_circulant_certificate.json` | `3,727` | `c868b813122ccb1efc78d7cd19e7a9ebee0a82c4c6c9be33643318958df617d4` |
| `object/ame_17_7_pure_circulant_certificate.json` | `1,030` | `b68f2aac4f1d72977309f0eb08c761e1f122e6b8f395e8e0a4484647ac2232f4` |
| `object/ame_17_8_pure_circulant_certificate.json` | `4,176` | `0bc632480b2bfb3a90117f0676e8894dc5972ea32cb315cd47e1d04077f20a28` |
| `object/ame_18_16_pure_circulant_certificate.json` | `4,033` | `ff4ecacde996416017fb46a4cdcbd71461823766631321f7b0975c2d76d44025` |
| `object/ame_18_7_pure_circulant_certificate.json` | `557` | `59b3292f2583484c47300497e74dd5f50d682377a75349de1646ec3c4d660081` |
| `object/ame_19_11_z19_exhaustive_nogo_d31_certificate.json` | `1,669` | `24d52c747ca3ce7a5ef63bac3f13a36590406dca9f135f1b804067a9a0577b8a` |
| `object/ame_19_13_pure_circulant_certificate.json` | `4,263` | `274159da339c820b8b15ca26cd2665c1ee5a46d89ecdec6a40d380502b9ebf71` |
| `object/ame_19_16_pure_circulant_certificate.json` | `4,517` | `5dac5fa4efd3dc93d077fe1e81e8b8edef3af5a3e97c487719ba72887fa3e369` |
| `object/ame_19_17_pure_circulant_certificate.json` | `4,458` | `496c619a046592cddf0a8ab925825885c08ac7e534822d1ddadd39004439800c` |
| `object/ame_19_19_pure_circulant_certificate.json` | `4,462` | `afa20e21fc44d632dbe6cb3206a8aab3f5b5dbb488e67170848c84e1bb74227b` |
| `object/ame_20_11_g40_exhaustive_nogo_d33_certificate.json` | `5,252` | `c607322a60f05c4364befc884970dc150e7d5ddd68a4d9c4d7ae1713479247ab` |
| `object/ame_20_13_hermitian_mds_d27b_certificate.json` | `4,307` | `ba711a679e88004b8ed4ec8ba4df74c39d6aae8b7ff32ef3f54110d956735e68` |
| `object/ame_20_16_hermitian_mds_d29_certificate.json` | `4,613` | `b344b023b0d5c7783e07d9723e0aa166b1a668be5dbcdb5ca717ab5c0c826465` |
| `object/ame_20_17_hermitian_mds_d28_certificate.json` | `7,557` | `d1cb59262b7cf1832669061429b3bbfb6fb2f562f52feed2fc4eb82d56b3245e` |
| `object/ame_20_gf289_so10_d25_d26_certificate.json` | `4,859` | `81c81257fcb23097c26876eb38a83a29b7aed5d1ba94eddecf87ad1aa23ab09d` |
| `object/ame_table_n2_to_20_status_and_estimates.json` | `57,888` | `95e817c436014f28c17e6f25070c66ef35b194f082e2190796da1a70ab347d51` |
| `object/universal_paley_jacobsthal_ame_13_14_17_18_certificate.json` | `2,234` | `a442249dde030b73dc17e87675962b2dc1600fd558d46289c89a40fc8ade8615` |
| `object/universal_paley_jacobsthal_ame_19_20_certificate.json` | `8,803` | `0fc32a1ed4d418da7bb324e845549e1f74c51b58b17e5da0004a4f4b7077905d` |

---

## 3. Independent Verification Results (`0.28s` End-to-End)

1. **`AME(20, 17)`, `AME(20, 16)`, `AME(20, 13)`, and `AME(20, 289)` (`n = 20` Quantum MDS & Pure Graph States):**
   - `object/ame_20_17_hermitian_mds_d28_certificate.json`: Verified $U U^\dagger = -I_{10}$ over $\mathbb{F}_{289} = \mathbb{F}_{17}[\alpha]/(\alpha^2 - 3)$, non-singularity of all `4,970` $G_{40}$-orbit representatives (covering all `184,755` square minors of $U$), and full rank `10` over $\mathbb{F}_{17}$ of the explicit $20 \times 20$ symmetric graph adjacency matrix $\Gamma_{20,17}$ across all `184,756 / 184,756` 10-party cuts (`0` singular cuts via the compiled native C bit-sliced sweep).
   - `object/ame_20_16_hermitian_mds_d29_certificate.json`: Verified $U U^\dagger = I_{10}$ over $\mathbb{F}_{256} = \mathbb{F}_2[x]/(x^8 + x^4 + x^3 + x^2 + 1)$, non-singularity of all `4,970` $G_{40}$-orbits (`184,755 / 184,755` minors), and full rank `10` over $\mathbb{F}_{16}$ (and full rank `40` over $\mathbb{F}_2$ of the $80 \times 80$ binary graph matrix) across all `184,756 / 184,756` 10-party cuts.
   - `object/ame_20_13_hermitian_mds_d27b_certificate.json`: Verified $U U^\dagger = -I_{10}$ over $\mathbb{F}_{169} = \mathbb{F}_{13}[\alpha]/(\alpha^2 - 2)$, non-singularity of all `4,970` $G_{40}$-orbits (`184,755 / 184,755` minors), and full rank `10` over $\mathbb{F}_{13}$ of the explicit $20 \times 20$ symmetric graph adjacency matrix $\Gamma_{20,13}$ across all `184,756 / 184,756` 10-party cuts.
   - `object/ame_20_gf289_so10_d25_d26_certificate.json`: Verified $U U^T = -I_{10}$ over $\mathbb{F}_{289}$, non-singularity of all `4,970` $G_{40}$-orbits (`184,755 / 184,755` minors), and Theorem D26 single-column puncturing to `AME(19, 289)`.
2. **`AME(19, 13)`, `AME(19, 16)`, `AME(19, 17)`, `AME(19, 19)`, `AME(18, 16)`, `AME(18, 7)`, `AME(17, 7)`, `AME(17, 8)`, `AME(16, 11)`, `AME(16, 13)`, `AME(16, 16/17/19)`, `AME(15, 7)`, `AME(15, 8)`, `AME(15, 9)`, `AME(13, 5)`, and `AME(10, 10)`:**
   - Every circulant, double-circulant, and bordered-circulant graph state was reconstructed from its generator vector and verified in exact finite-field / ring arithmetic to have `0` singular $k$-party cuts across all $\binom{n}{\lfloor n/2 \rfloor}$ subsets (`1,716 / 1,716` for $n=13$, `6,435 / 6,435` for $n=15$, `12,870 / 12,870` for $n=16$, `24,310 / 24,310` for $n=17$, `48,620 / 48,620` for $n=18$, `92,378 / 92,378` for $n=19$).
   - For `object/ame_10_10_shortened_binary_stabilizer_certificate.json`, verified that the $8 \times 20$ binary stabilizer generator matrix of the shortened `[[10, 2, 4]]_2` code has rank `8`, pairwise commutes, and enumerates $2^8 = 256$ stabilizer elements with minimum non-identity weight $d^\perp = 6 > 5$, and verified the Delsarte LP bounds $r_{\min}(n, d^\perp)$.
3. **Impurity & Exhaustive No-Go Certificates (`ame_15_5`, `D31`, `D33/D33B/D34`):**
   - `object/ame_15_5_impurity_and_circulant_nogo_certificate.json`: Verified `[[15, 0, 8]]_5` impurity ($w_{\text{pure}} = 7$ on row 9, `190 / 6,435` bad cuts), `[[15, 0, 8]]_7` impurity ($w_{\text{pure}} = 1$ on row 14, `3,003 / 6,435` bad cuts), and the $\mathbb{Z}_{15}$ circulant near-miss witness $a = (0, 3, 1, 2, 1, 0, 0) \in \mathbb{F}_5^7$ (`105 / 6,435` bad cuts).
   - `object/ame_19_11_z19_exhaustive_nogo_d31_certificate.json`: Verified that the global near-miss witness $a = (1, 0, 7, 1, 3, 2, 4, 3, 7) \in \mathbb{F}_{11}^9$ across all $11^9 - 1 = 2,357,947,690$ symmetric 19-circulants has `1 / 126` bad self-conjugate orbits (`19` cuts) and `6 / 2,494` bad dihedral orbits (`209 / 92,378` bad 9-party cuts = `99.7738%`).
   - `object/ame_20_11_g40_exhaustive_nogo_d33_certificate.json`: Reconstructed the exact $10 \times 10$ block-circulant matrices over $\mathbb{F}_{121}$ for the `QR` coset near-miss (`31 / 4,970` bad orbits), the `QNR` coset `sub = 0 / 177` witness (`0 / 177` sub-orbits, `34 / 4,970` total), the `QNR` coset global minimum witness (`u11 = [109, 59, 31, 90, 110], u12 = [74, 39, 50, 66, 109]`, `2 / 177` sub-orbits + `10 / 4,793` ext-orbits = **`12 / 4,970` bad orbits = `99.7586%`**), and the $G_{20}^{\text{unit}}$ bi-unitary witness (`0 / 125` sub-orbits).

---

## 4. Determinism & Corrupted-Copy Check

Running `sh verify-it-yourself/run_checks.sh` twice from a clean copy completed in `0.28s` and printed `VERIFIED: All 28 Part II AME & Quantum MDS Certificates PASS in 0.28s` followed by `PASS`. Mutating a single digit of `object/ame_10_10_shortened_binary_stabilizer_certificate.json` deterministically exited with code `1` and printed `FAIL`.

pass: true
