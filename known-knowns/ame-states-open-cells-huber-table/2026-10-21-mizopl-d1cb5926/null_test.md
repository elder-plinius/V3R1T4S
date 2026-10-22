# Null and Perturbation Control Audit (`ame-states-open-cells-huber-table`, Part II: `2026-10-21-mizopl-d1cb5926`)

controls: 400
best_control: 6225/6435 cuts passed (210 failed 7-party cuts; 0/400 random symmetric Z_15 circulants over GF(7) achieve 0 failed cuts)
real: 6435/6435 cuts passed (0 failed 7-party cuts for AME(15,7), 0/48620 failed 9-party cuts for AME(18,16), 0/92378 failed 9-party cuts for AME(19,13), and 0/184755 failed minors for AME(20,13), AME(20,16), AME(20,17), and AME(20,289))
command: python3 verify-it-yourself/verify.py
real_beats_all_controls: yes

## Summary of Null & Perturbation Controls

1. **400 Random Symmetric $\mathbb{Z}_{15}$ Circulants over $\mathbb{F}_7$ (`seed = 42`):** Across `400` uniform random symmetric circulant adjacency matrices $\Gamma(a)$ ($a \in \mathbb{F}_7^7 \setminus \{0\}$) evaluated across all $\binom{15}{7} = 6,435$ seven-party cuts over $\mathbb{F}_7$, `0 / 400` controls achieve `0` singular cuts (best control: `6,225 / 6,435` cuts passed, i.e., `210` failed cuts; mean: `5,342.1 / 6,435` cuts passed), whereas our explicit Paley-perturbed circulant $a = (1, 5, 4, 2, 1, 0, 0) \in \mathbb{F}_7^7$ in `object/ame_15_7_pure_circulant_certificate.json` passes all **`6,435 / 6,435`** cuts (`0` failed cuts).
2. **Impure `codetables.de` Controls (`object/ame_15_5_impurity_and_circulant_nogo_certificate.json`):** Evaluating the existing `codetables.de` $k=0$ stabilizer generators for `[[15, 0, 8]]_7` and `[[15, 0, 8]]_5` catches **`3,003 / 6,435`** failed cuts ($w_{\text{pure}} = 1$ on row 14) and **`190 / 6,435`** failed cuts ($w_{\text{pure}} = 7$ on row 9), respectively.
3. **Exhaustive Below-Threshold Controls (`D31`, `D33`, `D33B`):**
   - Across all $11^9 - 1 = 2,357,947,690$ symmetric $\mathbb{Z}_{19}$ circulants over $\mathbb{F}_{11}$ (`object/ame_19_11_z19_exhaustive_nogo_d31_certificate.json`), `0` achieve `0` bad cuts (best is `209 / 92,378` bad cuts at $a = (1, 0, 7, 1, 3, 2, 4, 3, 7)$), whereas at $q = 13$ (`object/ame_19_13_pure_circulant_certificate.json`), $a = (1, 4, 11, 9, 10, 7, 6, 1, 12) \in \mathbb{F}_{13}^9$ achieves **`0 / 92,378`** bad cuts.
   - Across all $3,544,742,400$ pairs in both `QR` and `QNR` cosets of $G_{40} \subset U(10, \mathbb{F}_{121})$ (`object/ame_20_11_g40_exhaustive_nogo_d33_certificate.json`), `0` achieve `0` bad orbits (best is `12 / 4,970` bad orbits in `QNR`), whereas at $q \in \{13, 16, 17\}$ (`object/ame_20_13_hermitian_mds_d27b_certificate.json`, `object/ame_20_16_hermitian_mds_d29_certificate.json`, `object/ame_20_17_hermitian_mds_d28_certificate.json`), our constructions achieve **`0 / 4,970`** bad orbits (`0 / 184,755` singular minors).
