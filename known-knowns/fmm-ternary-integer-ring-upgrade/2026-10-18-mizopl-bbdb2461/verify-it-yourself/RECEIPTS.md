# Verification Receipts (`2026-10-18-mizopl-bbdb2461`)

## 1. Object Integrity

- **File:** `object/14x15x15_m1894_ZT.json`
- **Size:** `944,884` bytes (`922.7 KB`, `< 1 MB`)
- **Format & Rank:** `14x15x15`, rank `1,894`, ring `ZT = {-1, 0, 1}` (`max_abs = 1`, `zero_terms = 0`)
- **SHA-256:** `bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb`

## 2. Output of `sh verify-it-yourself/run_checks.sh`

```text
control_positive_strassen_2_2_2: PASS (64/64 equations, mismatches=0)
control_negative_corrupted_brent: PASS (rejected)
control_negative_non_zt_coeff: PASS (rejected)
sha256=bbdb24611006dbe7d8c3549701f177f8cf1b56090e6a928dd7ca961cd62979bb
format=14x15x15 rank=1894 ring=ZT max_abs=1 zero_terms=0
previous_zt_record=1905 previous_z_record=1895 overall_q_record=1848 delta_zt=-11 delta_z=-1
total_brent_equations=9922500 mismatches=0
PASS
```

## 3. 1-Minimality & Non-Degeneracy Receipt

- **Zero rank-1 terms (`all-zero u_q, v_q, or w_q`):** `0`
- **Distinct rank-1 triples `(u_q, v_q, w_q)`:** `1,894`
- **Redundant rank-1 terms (`deleting q in 0..1893 leaves 0 mismatches`):** `0` (deleting any single rank-1 term causes exact integer Brent equation mismatches over `Z`).
