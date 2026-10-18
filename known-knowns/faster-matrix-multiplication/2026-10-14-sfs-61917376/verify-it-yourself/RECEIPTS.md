Actual local command: sh verify-it-yourself/run_checks.sh
Elapsed seconds: 0.612

```text
{"valid": true, "format": [4, 5, 8], "rank": 118, "addition_counts": {"u": 101, "v": 159, "w": 226}, "additions": 486, "identities_verified": 25600}
{
  "pass": true,
  "sha256": "61917376617f1db0a75f5e9f5efd8bbd748713896418760b469126ea042ae5ee",
  "format": [
    4,
    5,
    8
  ],
  "rank": 118,
  "integer_exact": true,
  "expanded_factors_ternary": true,
  "complexity": {
    "naive": 1521,
    "reduced": 486
  },
  "cost_detail": {
    "u": {
      "fresh_binary_gates": 101,
      "terminal_binary_gates": 0,
      "live_fresh_gates": 101,
      "max_abs_intermediate_coefficient": 1
    },
    "v": {
      "fresh_binary_gates": 159,
      "terminal_binary_gates": 0,
      "live_fresh_gates": 159,
      "max_abs_intermediate_coefficient": 1
    },
    "w": {
      "fresh_binary_gates": 226,
      "terminal_binary_gates": 0,
      "live_fresh_gates": 226,
      "max_abs_intermediate_coefficient": 2
    }
  },
  "tensor": {
    "coefficients_checked": 25600,
    "nonzero_tensor_coefficients": 160,
    "active_distinct_products": 118
  },
  "execution": {
    "basis_pairs_executed": 800,
    "output_comparisons": 25600
  },
  "expanded_support": {
    "u": 526,
    "v": 662,
    "w": 601
  }
}
PASS
```
