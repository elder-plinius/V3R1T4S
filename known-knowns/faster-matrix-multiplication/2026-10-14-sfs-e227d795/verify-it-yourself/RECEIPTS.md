Actual local command: sh verify-it-yourself/run_checks.sh
Elapsed seconds: 0.15

```text
{"valid": true, "format": [3, 4, 5], "rank": 47, "addition_counts": {"u": 38, "v": 44, "w": 74}, "additions": 156, "identities_verified": 3600}
{
  "pass": true,
  "format": [
    3,
    4,
    5
  ],
  "rank": 47,
  "literal_additions": 156,
  "stage_additions": {
    "U": 38,
    "V": 44,
    "W": 74
  },
  "stage_cost_parts": {
    "U": {
      "fresh": 38,
      "terminal": 0
    },
    "V": {
      "fresh": 44,
      "terminal": 0
    },
    "W": {
      "fresh": 23,
      "terminal": 51
    }
  },
  "expanded_naive_additions": 277,
  "coefficient_count": 3600,
  "coefficient_mismatch_count": 0,
  "coefficient_mismatch_first": [],
  "tensor_nonzero_count": 60,
  "tensor_matches_mod_2": true,
  "basis_pair_count": 240,
  "basis_mismatch_count": 0,
  "basis_mismatch_first": [],
  "terminal_ternary": true,
  "terminal_ternary_violations_first": [],
  "active_products": 47,
  "distinct_products_up_to_sign": 47,
  "reached_variable_counts": {
    "W": 70,
    "U": 50,
    "V": 64
  },
  "declared_variable_counts": {
    "U": 50,
    "V": 64,
    "W": 70
  },
  "unreached_variable_indices": {
    "U": [],
    "V": [],
    "W": []
  },
  "declared_binary_gate_counts": {
    "U": 38,
    "V": 44,
    "W": 74
  },
  "reachable_binary_gate_counts": {
    "U": 38,
    "V": 44,
    "W": 74
  },
  "intermediate_max_absolute_coefficients": {
    "U": 1,
    "V": 1,
    "W": 1
  },
  "binary_partial_max_absolute_coefficients": {
    "U": 1,
    "V": 1,
    "W": 1
  },
  "aliases_by_stage": {
    "U": 0,
    "V": 0,
    "W": 0
  },
  "terminal_shapes": {
    "U": [
      47,
      12
    ],
    "V": [
      47,
      20
    ],
    "W": [
      15,
      47
    ]
  },
  "input_sha256": "e227d795fa1418070e30f21b18eac6a55d7426e51cfc8f8ef99c57b831d021f2"
}
PASS
```
