# Preregistration: FMM Ternary/Integer Ring Upgrades & Additive Complexity Records

## 1. Scope & Strict Constraints
- **Working Directory**: `{WORKDIR}/attacks/fmm`
- **No External Submissions**: Strictly local computation and verification only. No git pushes, PRs, or network submissions.
- **Target 1 (`fmm-ternary-integer-ring-upgrade`)**:
  1. Audit and verify `calgulbenkian`'s 7 Oct-14 ring upgrades (`4x13x15` Z 533, `4x13x15` ZT 535, `4x14x15` Z 569, `7x8x15` Z 570, `9x10x14` ZT 816, `9x11x14` Z 889, `9x13x14` Z 1039) against the live `FastMatrixMultiplication/README.md` (`data/perminov_README.md`), `FastMatrixMultiplication/schemes/results/{ZT,Z}` (`data/perminov_tree.txt`), `fmm-schemes` (`data/merlijn_tree.txt`), and `data/fmm_sota.json`.
  2. Construct and verify **at least 2 brand-new `ZT` or `Z` schemes** (not among those 7 and not `6x12x14` ZT 524) that strictly improve the live `perminov_README.md` `ZT` or `Z` upper bound while remaining $\ge$ the global SOTA rank over $\mathbb{Q}$.
  3. Verify all schemes exactly over $\mathbb{Z}$ via `tools/verify_z_brent.py` (exact integer Brent equations $\sum_{q=1}^r U_{q,a} V_{q,b} W_{c,q} = \delta_{a_2,b_1}\delta_{a_1,c_1}\delta_{b_2,c_2}$ or transposed).
- **Target 2 (`fmm-additive-complexity-records`, $\max(n,m,p) \le 8$)**:
  1. Audit all 84 formats with $\max(n,m,p) \le 8$ across `FastMatrixMultiplication/schemes/results/addition_reduced_ZT`, `schemes/reduced_known.json`, `data/fmm_sota.json`, `data/matmulcatalog_COVERAGE.md`, and V3R1T4S PRs (`pr_report.txt` and `open_prs_all.txt`).
  2. Test the 19 unclaimed SOTA-rank formats in `addition_reduced_ZT` (`2x2x2` through `2x3x8`, `2x4x6`, `3x3x5`, `3x4x4`) and test the 3 open-PR formats (`<2,4,7>` rank 45, `<2,5,6>` rank 47, `<4,5,5>` rank 76) using Boyar–Peralta cancellation search (`bpopt6`, `bpopt6_128`, `bpopt5`) and pair-CSE (`slpopt`) across primal and transposed maps.
  3. Verify all SLPs symbolically over $\mathbb{Z}$ using both `tools/check_slp.py` and `tools/sym_check.py`.

## 2. Methodology
1. **5-to-6 Inverse-Distributivity Unfolding (`Z -> ZT`)**:
   Identify 5-term clusters $(r_1, r_2, r_3, u_1, u_2)$ inside `<3,3,4>` rank-29 blocks embedded in Perminov's `Z` schemes (`14x15x15_m1895_Z.json`, `10x15x15_m1389_Z.json`) where $U[r_1] = U[r_2] + U[r_3]$, $V[r_2] - V[r_1] = V[u_2]$, $V[r_1] - V[r_3] = V[u_1]$, unfold each 5-term cluster with $\pm 2$ coefficients into 6 ternary terms (+1 rank per cluster), and apply ternary flip-graph reduction (`bin/zt_flip_reduce` with the `av > 1` merge guard fix).
2. **Subspace Homomorphism Base Substitution (`Q -> Z / ZT`)**:
   Detect rational base tensor blocks `<2,4,5>` ($32 \to 33$ `ZT`), `<3,3,6>` ($40 \to 42$ `ZT`), `<4,4,4>` ($48 \to 49$ `ZT`), and `<3,4,7>` ($63 \to 64$ `ZT`, accounting for 1 leading integer triad) inside Perminov's `_Q.json` schemes, solve the exact $\mathbb{Q}$-linear transition maps $(P_U, P_V, P_W)$ via Gaussian elimination over `fractions.Fraction`, optimize over the signed permutation symmetry group of each base `ZT` scheme, and reduce via `bin/zt_flip_reduce`.
3. **Primal/Transpose Boyar–Peralta SLP Search (`fmm-additive-complexity-records`)**:
   Optimize $U, V, W$ and $U^T, V^T, W^T$ (with `strict=1` transposed-program ternarity enforcement for transposed maps and 128-bit bitmask support in `bin/bpopt6_128` for $64 < N \le 128$), convert DAGs via `G.transpose` and `G.to_perminov`, and verify with `tools/check_slp.py` and `tools/sym_check.py`.
