# Verification Receipts (`2026-10-18-mizopl-2b72790b`)

## 1. Object Integrity

- **File:** `object/design_68_14_5.txt`
- **Size:** `632,681` bytes (`618 KB`, `< 1 MB`)
- **Lines (blocks):** `15,675`
- **SHA-256:** `2b72790b8149daebd293b91cddae0105bc2a19b798b414d405e66f81828bcf07`

## 2. Output of `sh verify-it-yourself/run_checks.sh`

```
control_positive_fano_7_3_2: PASS (35/35 covered, uncovered=0)
control_negative_fano_minus_1: PASS (rejected with uncovered=3)
sha256=2b72790b8149daebd293b91cddae0105bc2a19b798b414d405e66f81828bcf07
v=68 k=14 t=5 blocks=15675 distinct=15675
schonheim_lower_bound=5785
previous_cr_record=16004 previous_ljcr_record=16004 delta=-329
total_5_subsets=10424128 uncovered=0
PASS
```

## 3. 1-Minimality Receipt

- **Redundant blocks (`all 2,002 5-subsets covered >= 2 times`):** `0`
- **Minimum uniquely covered 5-subsets per block across all 15,675 blocks:** `6`
