# Lean 4 Kernel Proof of `Group.subsingleton_of_pow_prime_eq_one` in Imperial FLT

## What

On FLT main a321020 (re-checked today, no open PR or issue touching it), replacing the single sorry in Group.subsingleton_of_pow_prime_eq_one (and thus its @[to_additive] twin) in FLT/Patching/Utils/CompactHausdorffRings.lean with the claimed 803-line proof leaves the statement unchanged, builds that module and its importer AdicTopology under lean v4.35.0, and shows only propext, Classical.choice and Quot.sound, without a whole-repo build run by this skeptic.

## Check it yourself

From this package folder (with a clean `ImperialCollegeLondon/FLT` checkout at commit `a3210204ad8876e851e32f73dd97d882bf1ccd0a` and Mathlib cache):

```sh
FLT_ROOT=./FLT sh verify-it-yourself/run_checks.sh
```

Expected last output line: `PASS` (runs in about 90 seconds on a laptop once the `FLT` Mathlib cache is downloaded).

## Compared to

- **Repository**: https://github.com/ImperialCollegeLondon/FLT (`main` commit `a3210204ad8876e851e32f73dd97d882bf1ccd0a`)
- **Declaration**: `Group.subsingleton_of_pow_prime_eq_one` (and `@[to_additive]` `AddGroup.subsingleton_of_nsmul_prime_eq_zero`) in `FLT/Patching/Utils/CompactHausdorffRings.lean`
- **Upstream status**: `:= by sorry` (`0` open PRs touching `CompactHausdorffRings.lean`, `0` assigned/claimed issues)
- **Fetched**: `2026-11-16T16:55:45Z` (`HTTP 200`, SHA-256 `72b11ca144f518793a167af9109a5b31fa4e3b03377ef4ecd3e99bcf9c002eda`)

## Not claimed

- Triviality of connected compact Hausdorff abelian groups of prime exponent is a classical consequence of the Gelfand-Raikov / Peter-Weyl / Pontryagin theorem; only the sorry-free Lean 4 formalization in `ImperialCollegeLondon/FLT` is claimed.
- General Pontryagin duality for arbitrary locally compact abelian groups is not claimed.

## Credits

- **Kevin Buzzard**, **Richard Taylor**, **Thomas Browning** (author of `FLT/Patching/Utils/CompactHausdorffRings.lean`), and contributors to `ImperialCollegeLondon/FLT` (https://github.com/ImperialCollegeLondon/FLT, https://imperialcollegelondon.github.io/FLT/blueprint/).
- **Mathlib Community** (https://github.com/leanprover-community/mathlib4): Haar measure, Urysohn separation, `BoundedContinuousFunction.arzela_ascoli`, and Riesz compactness foundations.
- Related harmonic-analysis repositories inspected for novelty verification: `YaelDillies/mean-fourier` (https://github.com/YaelDillies/mean-fourier), `shosonoda/pontryagin` (https://github.com/shosonoda/pontryagin, vendored in unsubmitted fork `futarchy-fi/FLT`), and `anthropics/fermats-last-theorem` (https://github.com/anthropics/fermats-last-theorem).
