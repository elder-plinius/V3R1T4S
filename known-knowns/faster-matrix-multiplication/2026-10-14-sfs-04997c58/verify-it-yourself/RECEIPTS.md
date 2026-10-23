Actual local command: sh verify-it-yourself/run_checks.sh
Elapsed seconds: 0.229

```text
{"valid": true, "format": [3, 5, 5], "rank": 58, "addition_counts": {"u": 50, "v": 70, "w": 94}, "additions": 214, "identities_verified": 5625}
{
  "active_distinct_products": 58,
  "basis_failures": 0,
  "basis_pairs_checked": 375,
  "basis_witness": null,
  "dimensions": [
    3,
    5,
    5
  ],
  "exact_integer_identity": true,
  "expanded_factor_scalars": [
    -1,
    0,
    1
  ],
  "integer_tensor_witness": null,
  "literal_scalars": [
    -1,
    1
  ],
  "mod2_tensor_failures": 0,
  "naive_cost": 357,
  "rank": 58,
  "reduced_cost": 214,
  "sha256": "04997c5844e0968c43b347b7e911059ac1464c5da653b29bd3838a489723df7c",
  "side_audit": {
    "U": {
      "binary_cost": 50,
      "dead_gates": 0,
      "fresh_aliases": 0,
      "fresh_binary_gates": 50,
      "fresh_count": 50,
      "max_abs_intermediate": 1,
      "output_aliases": 58
    },
    "V": {
      "binary_cost": 70,
      "dead_gates": 0,
      "fresh_aliases": 0,
      "fresh_binary_gates": 70,
      "fresh_count": 70,
      "max_abs_intermediate": 1,
      "output_aliases": 58
    },
    "W": {
      "binary_cost": 94,
      "dead_gates": 0,
      "fresh_aliases": 0,
      "fresh_binary_gates": 94,
      "fresh_count": 94,
      "max_abs_intermediate": 2,
      "output_aliases": 15
    }
  },
  "tensor_coefficients_checked": 5625,
  "tensor_failures": 0
}
PASS
```
