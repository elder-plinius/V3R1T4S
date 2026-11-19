# Verification Receipts

Command executed from the package root folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Captured output (`PROVED-HERE`):

```text
[Verifier 1 - C99 Exact i128] Certified lower bound L at least 168131152814625 (168,131,152,814,625)
  max_excluded_lcm                                  = 168131152814624 (168,131,152,814,624)
  band_lower_threshold_floor_B0_div_3               = 56043717604874
  total_initial_prime_abundant_profiles_below_bound = 30147
  band_profiles_checked                             = 7036
  refuted_by_pure_deletion_bff                      = 2519
  max_pure_deletion_bff_measure                     = 124651682101/124657827840
  refuted_by_distortion_certificate                 = 4517
  max_certified_covered_measure                     = 16615714572403899891/16710819340101877760
  min_certified_uncovered_numerator_surplus         = 95104767697977869
VERIFY_C: PASS
[Verifier 2 - Python Exact Fractions] Certified lower bound L at least 168131152814625 (168,131,152,814,625)
  sharp_frontier_factorization                      = 3^4 * 5^3 * 7^2 * 11^2 * 13 * 17 * 19 * 23 * 29
  max_excluded_lcm                                  = 168131152814624 (168,131,152,814,624)
  band_lower_threshold_floor_B0_div_3               = 56043717604874
  total_initial_prime_abundant_profiles_below_bound = 30147
  band_profiles_checked                             = 7036
  refuted_by_pure_deletion_bff                      = 2519
  max_pure_deletion_bff_measure                     = 124651682101/124657827840
  refuted_by_distortion_certificate                 = 4517
  max_certified_covered_measure                     = 16615714572403899891/16710819340101877760
  min_certified_uncovered_numerator_surplus         = 95104767697977869
  ratio_over_egeozturk_11486475                     = 14637315x
  ratio_over_schroeder_9704539845                   = 17325x
VERIFY_PY: PASS
PASS
```
