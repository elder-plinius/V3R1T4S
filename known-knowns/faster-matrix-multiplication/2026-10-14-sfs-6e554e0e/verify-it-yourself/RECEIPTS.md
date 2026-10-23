Actual local command: sh verify-it-yourself/run_checks.sh
Elapsed seconds: 0.352

```text
{"valid": true, "format": [2, 5, 6], "rank": 47, "addition_counts": {"u": 38, "v": 65, "w": 76}, "additions": 179, "identities_verified": 3600}
{
  "format": [
    2,
    5,
    6
  ],
  "ring": "Z",
  "active_products": 47,
  "rank_one_terms_distinct": 47,
  "coefficient_count": 3600,
  "expected_one_coefficients": 60,
  "expected_zero_coefficients": 3540,
  "mismatches": 0,
  "additions": 179,
  "naive_additions": 332,
  "binary_gates": 179,
  "basis_pairs": 300,
  "basis_binary_gate_checks": 53700,
  "basis_product_checks": 14100,
  "basis_output_checks": 3600,
  "phases": {
    "u": {
      "base_inputs": 10,
      "fresh_count": 38,
      "final_count": 47,
      "fresh_additions": 38,
      "final_additions": 0,
      "additions": 38,
      "dead_fresh": [],
      "live_base_count": 10,
      "free_singleton_positive": 47,
      "free_singleton_negative": 0,
      "fresh_expanded_values": [
        -1,
        0,
        1
      ],
      "final_expanded_values": [
        -1,
        0,
        1
      ]
    },
    "v": {
      "base_inputs": 30,
      "fresh_count": 28,
      "final_count": 47,
      "fresh_additions": 28,
      "final_additions": 37,
      "additions": 65,
      "dead_fresh": [],
      "live_base_count": 30,
      "free_singleton_positive": 16,
      "free_singleton_negative": 5,
      "fresh_expanded_values": [
        -1,
        0,
        1
      ],
      "final_expanded_values": [
        -1,
        0,
        1
      ]
    },
    "w": {
      "base_inputs": 47,
      "fresh_count": 20,
      "final_count": 12,
      "fresh_additions": 20,
      "final_additions": 56,
      "additions": 76,
      "dead_fresh": [],
      "live_base_count": 47,
      "free_singleton_positive": 0,
      "free_singleton_negative": 0,
      "fresh_expanded_values": [
        -1,
        0,
        1
      ],
      "final_expanded_values": [
        -1,
        0,
        1
      ]
    }
  },
  "expanded_tensor_value_histogram": {
    "1": 60,
    "0": 3540
  },
  "ordering": "A[i,k]=i*5+k; B[k,j]=k*6+j; output C[i,j]=j*2+i",
  "pass": true,
  "scheme_sha256": "6e554e0ee89a3fda23f7c59d261ca1f27bcb089e141db911246437ca50e931e9"
}
PASS
```
