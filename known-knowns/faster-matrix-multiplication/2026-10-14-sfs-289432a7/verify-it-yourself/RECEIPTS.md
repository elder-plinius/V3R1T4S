Actual local command: sh verify-it-yourself/run_checks.sh
Elapsed seconds: 0.229

```text
{"valid": true, "format": [2, 4, 8], "rank": 51, "addition_counts": {"u": 37, "v": 68, "w": 77}, "additions": 182, "identities_verified": 4096}
{
  "format": [
    2,
    4,
    8
  ],
  "products": 51,
  "active_distinct_products": 51,
  "output_order": "j*n+i",
  "input_order": "A i*m+h; B h*p+j",
  "binary_additions": {
    "u": 37,
    "v": 68,
    "w": 77
  },
  "total_additions": 182,
  "naive_additions": 354,
  "tensor_coefficients_checked": 4096,
  "tensor_mismatches": 0,
  "first_tensor_mismatches": [],
  "basis_pairs_checked": 256,
  "direct_output_values_checked": 4096,
  "direct_mismatches": 0,
  "first_direct_mismatches": [],
  "mod2_tensor_mismatches": 0,
  "audit": {
    "u": {
      "counts": {
        "fresh": 37,
        "terminal": 0,
        "aliases": 51,
        "free_negative_aliases": 0
      },
      "fresh_gates": 37,
      "dead_fresh_indices": [],
      "expanded_coefficient_domain": [
        -1,
        0,
        1
      ],
      "intermediate_coefficient_domain": [
        -1,
        0,
        1
      ],
      "max_intermediate_absolute_coefficient": 1
    },
    "v": {
      "counts": {
        "fresh": 68,
        "terminal": 0,
        "aliases": 51,
        "free_negative_aliases": 0
      },
      "fresh_gates": 68,
      "dead_fresh_indices": [],
      "expanded_coefficient_domain": [
        -1,
        0,
        1
      ],
      "intermediate_coefficient_domain": [
        -1,
        0,
        1
      ],
      "max_intermediate_absolute_coefficient": 1
    },
    "w": {
      "counts": {
        "fresh": 77,
        "terminal": 0,
        "aliases": 16,
        "free_negative_aliases": 0
      },
      "fresh_gates": 77,
      "dead_fresh_indices": [],
      "expanded_coefficient_domain": [
        -1,
        0,
        1
      ],
      "intermediate_coefficient_domain": [
        -2,
        -1,
        0,
        1,
        2
      ],
      "max_intermediate_absolute_coefficient": 2
    }
  },
  "zero_hidden_scalar_operations": true,
  "extra_metadata_keys": [
    "research_method"
  ],
  "exact_Z_product": true,
  "scheme_sha256": "289432a72c0f86a04925e6475d31d4ff86d92a65fb8d57f4b57f918c3866d654"
}
PASS
```
