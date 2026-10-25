# Verification Receipts (`2026-10-19-mizopl-b40b1ef7`)

Command run from the package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Exact output:

```text
[1/5] Object SHA-256 digests and byte sizes verified (3/3 files).
[2/5] Chronological disjointness (2,165 M77 vs 999 post-1977 inscriptions, 3,731 tokens) and W740 reading direction (223/231 = 96.54%) verified.
[3/5] Masked-sign top-1 restoration accuracies and 10,000-resample paired bootstraps (vs KN3-Left & SIGIL p = 0.0001 across all strata; vs KN3-Bidir p = 0.0001 pooled, 0.0019 Mohenjo-daro, 0.0147 Harappa; vs KN3-BlanketF p = 0.0048 pooled, 0.2988 Mohenjo-daro, 0.0188 Harappa) verified.
[4/5] Partial Win p3 verified (30 shared parallel frames vs 10,000-permutation null mean 7.6427, max 23, p = 0.0001 < 0.001).
[5/5] 400 SIGIL matched-null controls verified (best_control = 0.096221 < real = 0.200482).
PASS
```
