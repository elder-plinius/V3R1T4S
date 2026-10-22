# Run It Yourself (`2026-10-22-mizopl-5ab48b6b`)

## 1. One-Command Exact Integer Verification (~3 seconds)

From the root of this submission directory (`2026-10-22-mizopl-5ab48b6b/`), run:

```sh
sh verify-it-yourself/run_checks.sh
```

(or directly `python3 verify-it-yourself/verify.py`).

### What `verify.py` Checks
1. Runs positive and negative self-tests on Strassen's `(2, 2, 2)` rank-7 ternary scheme (`64/64` exact integer Brent equations pass; corrupted tensor and non-ternary coefficient controls are rejected).
2. Verifies the SHA-256 hash of `object/CERTIFICATE.json` (`4050811589871e8e0b91e766d8587a39fe00649cce86b6e1fb974e755aae0bcf`) and the exact byte count and SHA-256 digest of all 7 JSON scheme files in `object/`.
3. For each of the 7 schemes (`6x12x14_m654_ZT.json`, `9x10x13_m763_ZT.json`, `9x10x16_m920_ZT.json`, `10x15x16_m1484_ZT.json`, `11x15x16_m1629_ZT.json`, `12x13x16_m1546_ZT.json`, `12x13x16_m1541_Z.json`):
   - Reconstructs dense 64-bit integer factor matrices $U \in \mathbb{Z}^{m \times (n_1 n_2)}$, $V \in \mathbb{Z}^{m \times (n_2 n_3)}$, and $W \in \mathbb{Z}^{m \times (n_3 n_1)}$.
   - Verifies that every coefficient is an exact integer, with `max_abs = 1` (all coefficients in $\{-1, 0, 1\}$) for all 6 `ZT` schemes and `max_abs = 2` for `12x13x16_m1541_Z.json`.
   - Verifies `zero_terms = 0`, `distinct_triples = m`, and exact agreement of `nnz_u`, `nnz_v`, `nnz_w`, `total_nnz`, and naive additive `complexity` with `object/CERTIFICATE.json`.
   - Contracts all $(n_1 n_2)(n_2 n_3)(n_3 n_1)$ exact 64-bit integer Brent equations
     $$\sum_{q=0}^{m-1} U[q, i_1 n_2 + i_2] \, V[q, j_2 n_3 + i_3] \, W[q, j_3 n_1 + j_1] = \delta_{i_1, j_1}\,\delta_{i_2, j_2}\,\delta_{i_3, j_3}$$
     across all **29,648,196** equations total (`1,016,064 + 1,368,900 + 2,073,600 + 5,760,000 + 6,969,600 + 6,230,016 + 6,230,016`) and confirms **`0` mismatches**.
   - Verifies Bank Clauses (1) and (2): `rank < previous_zt_rank` (or `rank < previous_z_rank` for `Z`) and `rank >= overall_q_rank`.

### Expected Output

```text
control_positive_strassen_2_2_2: PASS (64/64 equations, mismatches=0)
control_negative_corrupted_brent: PASS (rejected)
control_negative_non_zt_coeff: PASS (rejected)
certificate_sha256=4050811589871e8e0b91e766d8587a39fe00649cce86b6e1fb974e755aae0bcf (PASS)
verified 6x12x14  [ZT] rank= 654 (prev_ZT=666, prev_Z=654, Q=645) max_abs=1 complexity=13241 eqs=1016064 mismatches=0 sha256=5ab48b6b88fd1a7b...
verified 9x10x13  [ZT] rank= 763 (prev_ZT=771, prev_Z=763, Q=758) max_abs=1 complexity=14116 eqs=1368900 mismatches=0 sha256=a351d9eef1a62ff9...
verified 9x10x16  [ZT] rank= 920 (prev_ZT=924, prev_Z=920, Q=916) max_abs=1 complexity=17397 eqs=2073600 mismatches=0 sha256=42ad6efd9f8b6aab...
verified 10x15x16 [ZT] rank=1484 (prev_ZT=1488, prev_Z=1484, Q=1482) max_abs=1 complexity=28160 eqs=5760000 mismatches=0 sha256=02199a88ebd24b14...
verified 11x15x16 [ZT] rank=1629 (prev_ZT=1641, prev_Z=1629, Q=1605) max_abs=1 complexity=39490 eqs=6969600 mismatches=0 sha256=0d2eb6e651f61c7c...
verified 12x13x16 [ZT] rank=1546 (prev_ZT=1548, prev_Z=1544, Q=1509) max_abs=1 complexity=64887 eqs=6230016 mismatches=0 sha256=b639c891628cd5e5...
verified 12x13x16 [Z ] rank=1541 (prev_ZT=1548, prev_Z=1544, Q=1509) max_abs=2 complexity=64983 eqs=6230016 mismatches=0 sha256=911599680fd3bbe0...
VERIFIED: 7/7 schemes (6 ZT + 1 Z), 29648196/29648196 exact integer Brent equations PASS
PASS
```

## 2. Rebuilding All 7 Schemes From Scratch

To inspect or re-run the Higher-Order $S_{b \cdot g}$ Sub-Block Conjugation builder that constructs all 7 schemes from the base decompositions in `dronperminov/FastMatrixMultiplication`:

```sh
python3 how-we-built-it/build_all_7_schemes.py FastMatrixMultiplication rebuilt_schemes
```
