# REPRODUCE skeptic — V3R1T4S run 2026-10-14-0717, claims D_534 E_548 F_777 G_542 H_743 I_745
context: subagent (executor), fresh
role: REPRODUCE (independent checker written from criterion.txt first; author verify/hp.py used only afterwards as a secondary cross-check)

## Criterion used (quoted from claim/*/criterion.txt, identical across all six folders)
> "E* computed in mpmath at 30 digits from the normalized coordinates is STRICTLY LOWER ... than the minimum energy for that N over ALL of: Deeter's table ..., CCD Thomson/table.html, CCD Thomson2/table.html, the CCD Riesz s=1 table ..., the Wikipedia table ... by at least 1e-6 in absolute energy, AND the configuration is a certified strict local minimum (mpmath tangent-space Newton to gradient norm < 1e-20, all 2N-3 non-rotational tangent Hessian eigenvalues > 0), AND it is a different basin from every posted table configuration for that N: polishing each table's own point file ... with the same routine must give an energy higher than E* by >= 1e-6."

## Independent checker (../panel/reproduce_work_DI/ relative to claim/: mycheck.py, tables.py; no import of claim code)
- Energy: Coulomb sum 1/|x_i - x_j| over all pairs, each point normalized in mpmath at dps 30, mp.fsum at dps 30. Also recomputed with normalization at dps 50 and summed at dps 40 (same digits).
- Tangent gradient: g_i = -sum_j (x_i - x_j)/r^3 at dps 50, projected to g_i - (g_i.x_i)x_i, 2-norm over all points.
- Hessian: float64 Euclidean Coulomb Hessian -> Riemannian tangent Hessian B^T H B - diag(x_i.g_i), 3 rotation generators projected out by QR, eigvalsh on the 2N-3 block; crude error bound 10*n*eps*||H||.
- Distinct basin: my own polish of each posted Riesz file (scipy L-BFGS float64 gtol 1e-12, then tangent Newton steps with dps-50 gradient and float64 Hessian until grad < 1e-24), then mpmath dps-30 energy.
- Tables: regex parse of the saved claim/<X>/data/*.html (Riesz s=1, CCD Thomson, CCD Thomson2, Deeter, Wikipedia); sha256 of each saved page and points file checked against scout_table.md and data/fetch_log.txt.
- Every cand file: N rows, every coordinate has 40 decimals (>= 20 needed); sha256 matches claim.md for all six.

## Per-claim results (my measurements)

### D_534 — PASS
1) E* (dps30) = 135762.8145401324761574878 = claim.md = expected/cand_534_cert.json. (dps40: 135762.81454013247615748782930847589)
2) tangent grad2 = 6.11671e-31 (dps50-normalized; 1.16e-27 if normalized at dps30) — both < 1e-20; matches claimed 6.117e-31.
3) Hessian: dim_nonrot 1065, smallest 3.5543315923375 (cert 3.5543315923359, diff 1.5e-12), nneg 0, my crude certified_min 3.55433159 (cert 3.554331588471217); 3 rotational modes ~1e-12.
4) Posted Riesz data/points_534_1.dat: raw 135762.9050570236177650059 -> my polish 135762.9050570236176987786 (grad 3.6e-37, min eig 2.27191, nneg 0) = expected/riesz_534_polished.json exactly. Polished − E* = 9.0516891e-02 >= 1e-6.
5) Riesz s=1 cell 534 = 135762.9050570 (= scout_table.md); table − E* = 9.0516868e-02. No N=534 row in Deeter (max 524), CCD Thomson, CCD Thomson2, Wikipedia (max 470).

### E_548 — PASS
1) E* = 143066.8793744849140468194 = claim = cert.
2) grad2 = 6.44478e-23 (< 1e-20; matches 6.445e-23).
3) dim_nonrot 1093, smallest 0.4227914964758 (cert 0.4227914964748, diff 1.0e-12), nneg 0, crude certified_min 0.42279149 (cert 0.4227914923447352).
4) Posted points_548_1.dat polished: 143067.0064628337757525183 (grad 6.4e-28, min eig 2.30445) = expected exactly. Polished − E* = 1.2708835e-01.
5) Riesz cell 548 = 143067.0064628 (= scout); table − E* = 1.2708832e-01. No row in other tables.

### F_777 — PASS
1) E* = 289900.778533909713618485 = claim = cert.
2) grad2 = 1.93249e-27 (3.06e-27 at dps30 normalization); matches 1.932e-27.
3) dim_nonrot 1551, smallest 3.3212561121624 (cert 3.3212561121675, diff 5.1e-12), nneg 0, crude certified_min 3.32125610 (cert 3.3212561022742695).
4) Posted points_777_1.dat polished: 289900.8082429848528735925 (grad 6.3e-28, min eig 3.03246) = expected exactly. Polished − E* = 2.9709075e-02.
5) Riesz cell 777 = 289900.8082430 (= scout); table − E* = 2.970909e-02. No row in other tables.

### G_542 — PASS
1) E* = 139913.0793830909490116457 = claim = cert.
2) grad2 = 1.86714e-25; matches 1.867e-25.
3) dim_nonrot 1081, smallest 2.1797592000990 (cert 2.1797592001006, diff 1.6e-12), nneg 0, crude certified_min 2.17975919 (cert 2.1797591960811413).
4) Posted points_542_1.dat polished: 139913.1454539417389736485 (grad 4.3e-27, min eig 3.72465) = expected exactly. Polished − E* = 6.6070851e-02.
5) Riesz cell 542 = 139913.1454539 (= scout); table − E* = 6.6070809e-02. No row in other tables.

### H_743 — PASS
1) E* = 264837.5287041150044362828 = claim = cert.
2) grad2 = 1.57057e-24; matches 1.571e-24.
3) dim_nonrot 1483, smallest 3.6335971242983 (cert 3.6335971242933, diff 5.0e-12), nneg 0, crude certified_min 3.63359711 (cert 3.633597115460639).
4) Posted points_743_1.dat polished: 264837.5858503620609677129 (grad 2.0e-26, min eig 2.23476) = expected exactly. Polished − E* = 5.7146247e-02.
5) Riesz cell 743 = 264837.5858504 (= scout); table − E* = 5.7146285e-02. No row in other tables.

### I_745 — PASS
1) E* = 266280.2015165256924341327 = claim = cert.
2) grad2 = 1.52921e-22; matches 1.529e-22.
3) dim_nonrot 1487, smallest 3.2790932218445 (cert 3.2790932218489, diff 4.4e-12), nneg 0, crude certified_min 3.27909321 (cert 3.27909321294825).
4) Posted points_745_1.dat polished: 266280.2589229108841027487 (grad 9.9e-28, min eig 1.31188) = expected exactly. Polished − E* = 5.7406385e-02.
5) Riesz cell 745 = 266280.2589229 (= scout); table − E* = 5.7406374e-02. No row in other tables.

## Proof-step re-derivation
- Newton step count 0 is justified: every candidate already has tangent grad2 < 1e-20; with smallest non-rotational eigenvalue >= 0.42, the quadratic-model energy change ||g||^2/(2*lambda_min) <= 3e-44, far below the 1e-12 requirement.
- Distinct basin: each posted file polishes into its own certified minimum 0.0297–0.127 above E*; posted polished energies reproduce the live table cells to all 7 printed decimals, so the table cell is that basin.
- Table minimum over all listed sources: for all six N, only the CCD Riesz s=1 table has a row (Deeter 4..524, CCD Thomson max 972 without these N, CCD Thomson2 sparse, Wikipedia max 470), so the minimum is the Riesz cell; all margins >= 2.97e-02 >> 1e-6.
- Determinism: dps30 vs dps50 normalization give identical 25-digit E*; secondary cross-check run of the author's verify/hp.py (`--newton 0 --hessian`) AFTER my own checker reproduced expected/cand_*_cert.json E_final_mpmath30, grad2 and certified_min bit-for-bit for all six.
- Not exhaustive-search claims (single-object improvements), so the sampling rule does not apply.

## Caveats (not failures)
- Hessian certificate is numerical (float64 eigvalsh plus a rounding/Weyl bound), not interval-rigorous; that is what the criterion's verification_method asks for ("build the 3N x 3N Hessian in double"). Margins of the smallest eigenvalue over the bound are about 8 orders of magnitude.
- I did not re-fetch live tables (role limited to saved files); freshness of "re-fetched live immediately before claiming" rests on data/fetch_log.txt (2026-10-14T14:23:27Z–14:23:39Z UTC), whose sha256s match the saved pages and points files.
- The criterion text says Deeter covers N = 4..523; the saved page goes to 524. Irrelevant here because every claimed N is >= 534.

Scratch outputs (relative to claim/): ../panel/reproduce_work_DI/{D_534,E_548,F_777,G_542,H_743,I_745}.json, hp_*.json.
pass: true
