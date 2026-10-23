# Actual checker output

```text
{"valid": true, "format": [2, 5, 5], "rank": 40, "addition_counts": {"u": 31, "v": 55, "w": 62}, "additions": 148, "identities_verified": 2500}
{
  "pass": true,
  "format": [
    2,
    5,
    5
  ],
  "multiplications": 40,
  "active_products": 40,
  "duplicate_rank_one_terms": [],
  "opposite_rank_one_terms": [],
  "additions": 148,
  "naive_expanded_additions": 283,
  "cost_by_stage": {
    "u": {
      "cost": 31,
      "fresh_cost": 31,
      "final_cost": 0,
      "fresh_count": 31,
      "alias_count": 40
    },
    "v": {
      "cost": 55,
      "fresh_cost": 11,
      "final_cost": 44,
      "fresh_count": 11,
      "alias_count": 17
    },
    "w": {
      "cost": 62,
      "fresh_cost": 62,
      "final_cost": 0,
      "fresh_count": 62,
      "alias_count": 10
    }
  },
  "checked_tensor_coefficients": 2500,
  "checked_basis_pairs": 250,
  "checked_scalar_output_values": 2500,
  "expected_nonzero_coefficients": 50,
  "actual_nonzero_coefficients": 50,
  "input_order": {
    "a": "A[i,t] -> i*5+t",
    "b": "B[t,j] -> t*5+j"
  },
  "output_order": "C[i,j] -> j*2+i",
  "expanded_final_coefficients_ternary": true,
  "tensor_digest": "0b46b3e202602c62a9b4202c0724d6abb467cbca10e8e7b21572a0d7854f466d",
  "expanded_scheme_digest": "65a453e1db66f57aee3c7d9a2c2de6e62cc3b7b6601d92067e79215675314adb",
  "sequential_references_and_liveness_checked": true,
  "file_sha256": "fb2744d037444d6e5f84f56628cf97a01ad2650e374421fbe4961bfafefd7ca2"
}
PASS
```

Observed elapsed seconds: 0.165173
