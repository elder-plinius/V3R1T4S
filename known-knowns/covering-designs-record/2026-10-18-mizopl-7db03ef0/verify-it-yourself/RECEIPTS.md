# Verification Receipts (`2026-10-18-mizopl-7db03ef0`)

## 1. Object Integrity

- **File:** `object/design_40_16_7.txt`
- **Size:** `319,951` bytes (`7,251` lines)
- **Parameters:** $(v, k, t) = (40, 16, 7)$, $b = 7,251$ distinct blocks (`1`-minimal, `0` redundant blocks)
- **SHA-256:** `7db03ef01cd698f6764f590955f51732a64cd8a41dbe97efce69a6738d479985`

## 2. Output of `sh verify-it-yourself/run_checks.sh`

```text
control_positive_fano_7_3_2: PASS (21/21 covered, uncovered=0)
control_negative_fano_minus_1: PASS (rejected with uncovered=3)
sha256=7db03ef01cd698f6764f590955f51732a64cd8a41dbe97efce69a6738d479985
v=40 k=16 t=7 blocks=7251 distinct=7251
schonheim_lower_bound=1965
previous_cr_record=7470 previous_ljcr_record=7470 delta=-219
total_7_subsets=18643560 uncovered=0
PASS
```
