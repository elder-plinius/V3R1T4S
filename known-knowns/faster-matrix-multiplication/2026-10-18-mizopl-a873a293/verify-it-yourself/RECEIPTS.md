# Verification Receipts (`2026-10-18-mizopl-a873a293`)

## 1. Object Integrity

- **File:** `object/9x12x14_m954_ZT.json`
- **Size:** `915,296` bytes (`894 KB`, `< 1 MB`)
- **Format & Rank:** `9x12x14`, rank `954`, ring `ZT = {-1, 0, 1}` (`max_abs = 1`, `zero_terms = 0`)
- **SHA-256:** `a873a293abc4e1b7c659250591e544062ad26ca556af28f29b25e63998355b02`

## 2. Output of `sh verify-it-yourself/run_checks.sh`

```text
control_positive_strassen_2_2_2: PASS (64/64 equations, mismatches=0)
control_negative_corrupted_brent: PASS (rejected)
control_negative_non_zt_coeff: PASS (rejected)
sha256=a873a293abc4e1b7c659250591e544062ad26ca556af28f29b25e63998355b02
format=9x12x14 rank=954 ring=ZT max_abs=1 zero_terms=0
previous_zt_record=960 previous_z_record=960 overall_q_record=940 delta_zt=-6
total_brent_equations=2286144 mismatches=0
PASS
```

## 3. 1-Minimality & Non-Degeneracy Receipt

- **Zero rank-1 terms (`all-zero u_q, v_q, or w_q`):** `0`
- **Distinct rank-1 triples `(u_q, v_q, w_q)`:** `954`
- **Redundant rank-1 terms (`deleting q in 0..953 leaves 0 mismatches`):** `0` (deleting any single rank-1 term breaks between `9` and `1,512` Brent equations over `Z`).
