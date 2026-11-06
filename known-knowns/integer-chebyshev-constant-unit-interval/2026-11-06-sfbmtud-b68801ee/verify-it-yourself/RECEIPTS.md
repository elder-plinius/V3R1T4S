# Runner validation receipts

These are scaffold-validation receipts for the provisional v6 object. They are not a receipt for a later final object and are not an independent mathematical verification. The runner reuses the included portable Bernstein checker.

## Full clean-copy v6 execution

Object SHA256: `e42c4bc09a857ca80dbbd8fe90171d6b26a3a6afc0a0a334f643f3296b29c99c`.
Exact configured threshold: `0.422643878`.
Portable checker SHA256: `6720628d0e51eb6c20852c5dbbc6b4627b5eace0105b363f3e6d20adbc3527ea`.
Runner SHA256 during this full trial: `cf3e4a2ce233243dd6734557d9efc54d1725d471027a7c0fdd28eaa19cdbeb97`.
Shell launcher SHA256: `fe316b1f7857dbf220a874eeeb609e0bf5fd006c8e479da0751dfc234bbcaf0f`.
Configuration SHA256: `dfe28f78b51c1faf8a480829d988fab93bc9ad4949f9ae61e440260f5e93e9e8`.

Executed once from a relocated clean package copy with inherited `PYTHONOPTIMIZE=2`; the shell launcher reset it to zero. Actual output:

```text
Object SHA256: e42c4bc09a857ca80dbbd8fe90171d6b26a3a6afc0a0a334f643f3296b29c99c
Checker SHA256: 6720628d0e51eb6c20852c5dbbc6b4627b5eace0105b363f3e6d20adbc3527ea
Computing the full rigorous continuum certificate.
Exact threshold: 0.422643878
Integer factors: 181
Exact x-degree: 2000000000000288
Certified dyadic intervals: 7981
Maximum subdivision depth: 24
Finite cover: complete
Strict integer acceptance margin: 10005729341065038150517747111659880056335250
Verification seconds: 143.949577
Peak RSS (KiB on Linux): 24884
PASS
```

Exit code: 0. End-to-end seconds: 144.03581708800266. Package files unchanged: true. Temporary proof outputs removed: true.

## Corrupted object

One numeric digit of the object bytes was changed without changing the configured SHA256. No continuum computation was started. Actual output:

```text
Object SHA256 mismatch.
FAIL
```

Exit code: 1. Rejection seconds: 0.038769023998611374.

## Final wrapper controls

An engineering audit identified two invalid-path failure-output gaps after the full v6 trial: dot paths and symlink loops could produce a traceback. The wrapper now rejects both cleanly. These changes do not modify the frozen mathematical checker or the normal success path.

Current runner SHA256: `fca52d77cf8a0fdd4663a1c92ee00c8c0b8b319adb7a22f5c06d6d7d1a2162bb`.
Current METHOD.md SHA256: `6a25705b80592a23c903b03178b89d093ba53269d62d6181f39ddb5d7f9cf80b`.

All 14 targeted controls passed on the final wrapper. Each left package files unchanged and removed temporary outputs:

| Case | Exit code | Last line | Seconds |
|---|---:|---|---:|
| valid_elementary | 0 | PASS | 0.161464 |
| semantic_false_bound | 1 | FAIL | 0.154426 |
| semantic_bad_degree | 1 | FAIL | 0.156926 |
| corrupt_object | 1 | FAIL | 0.037650 |
| corrupt_checker | 1 | FAIL | 0.043343 |
| invalid_config | 1 | FAIL | 0.036089 |
| missing_object | 1 | FAIL | 0.032779 |
| traversal_path | 1 | FAIL | 0.041472 |
| inherited_optimization | 0 | PASS | 0.106878 |
| space_in_package_name | 0 | PASS | 0.104458 |
| dot_path | 1 | FAIL | 0.050999 |
| dot_slash_path | 1 | FAIL | 0.047134 |
| dot_repeat_path | 1 | FAIL | 0.048926 |
| symlink_loop | 1 | FAIL | 0.045879 |

The final package must be run again after its object bytes, exact threshold and configuration are frozen. That final execution and package-level mechanical check are separate from these scaffold receipts.

## Final-object direct mathematical verification

The following actual receipt comes from the same frozen portable_v2 mathematical checker, invoked directly with Python3 -S before the final panel. It is not a fabricated wrapper transcript. The package checker separately reruns the final wrapper from a clean copy.

```json
{
  "core_controls": "PASS",
  "log_precision_bits": 128,
  "log_series_terms": 48,
  "claim_level": "PROVED-HERE",
  "certificate_sha256": "b68801eed7ca3043a7b817aa6567d92b6d73519c3be888936589519de71055ce",
  "threshold_exact": "422640947/1000000000",
  "threshold_decimal_input": "0.422640947",
  "factor_count": 213,
  "w_degree": 1000000000026,
  "x_degree": 2000000000052,
  "unweighted_degree_sum": 4293,
  "real_rootedness": "not assumed or tested",
  "checker_variant": "portable_v1",
  "site_packages_disabled": true,
  "visited": 19217,
  "accepted_leaves": 9609,
  "pending_cells": 0,
  "maximum_depth": 22,
  "accepted_methods": {
    "hull": 2658,
    "taylor2": 6951
  },
  "finite_cover_complete": true,
  "max_accepted_upper_scaled": "-586124321139279012674695748190385178949983936335288",
  "comparison_target_scaled": "-586124321139190743389294925489611514861266810588520",
  "minimum_acceptance_margin_scaled": "88269285400822700773664088717125746768",
  "worst_accepted_cell": [
    19,
    239550
  ],
  "common_scale_denominator": "340282366920938463463374607431768211456",
  "normalization": 2000000000052,
  "elapsed_seconds": 222.18361902499964,
  "peak_rss_kib": 26720,
  "python_version": "3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]",
  "mode": "taylor2"
}
```
