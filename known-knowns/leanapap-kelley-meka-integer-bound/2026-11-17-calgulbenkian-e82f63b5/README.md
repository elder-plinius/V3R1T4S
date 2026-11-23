# Lean 4 Formal Proof of the Kelley-Meka Integer 3AP-Free Bound (`leanapap-kelley-meka-integer-bound`)

## What

Against LeanAPAP master fb5cb9c (re-fetched, still live) at Lean v4.36.0-rc2, the six staged files compile in a full lake build and prove, under open Finset Real, exactly the criterion's corrected theorem int with axioms only propext, Classical.choice and Quot.sound, and BohrSet.regularity (p1) is also proved sorry-free with its statement unchanged.

## Check it yourself

From this package folder (with a clean `YaelDillies/LeanAPAP` checkout at commit `fb5cb9c4f594cbeeb160c715618d13640984c521` and Mathlib cache):

```sh
LEANAPAP_ROOT=./LeanAPAP sh verify-it-yourself/run_checks.sh
```

Expected last output line: `PASS` (cold-compiles all 6 proof modules from source, runs full `lake build`, verifies `#check @int` and `#print axioms int`, and restores `LeanAPAP` git-clean in ~90 seconds).

## Compared to

- **Repository**: https://github.com/YaelDillies/LeanAPAP (`master` commit `fb5cb9c4f594cbeeb160c715618d13640984c521`)
- **Target files**: `APAP/Integer.lean` (`theorem int`, `347` B, `:= sorry`) and `APAP/Prereqs/Bohr/Regular.lean` (`BohrSet.regularity`, `924` B, `:= sorry`)
- **Prior formalization status**: `LeanAPAP` formalized only the finite-field model `theorem ff` (`APAP/FiniteField.lean`); no Lean proof of the integer Kelley-Meka `1/12` bound existed in `LeanAPAP`, `mean-fourier`, `add-combi`, or `mathlib4`
- **Fetched**: `2026-11-16T21:40:44Z` (`HTTP 200`, SHA-256 `79d85781dde7385ab3f6a4f35fe41eac43a2f27c8d0c72aa23b7d652e95ea7d4`)

## Not claimed

- The mathematical theorem is due to Zander Kelley and Raghu Meka (2023), following the Bohr-set exposition of Thomas F. Bloom and Olof Sisask (2023) and regular Bohr-set machinery of Jean Bourgain (1999); only the machine-checked Lean 4 formalization is new here.
- Sub-`1/12` exponent improvements (such as Bloom-Sisask `1/9`) and numerical optimization of `(c, C)` are not claimed.

## Credits

- **Zander Kelley and Raghu Meka**, *Strong Bounds for 3-Progressions*, FOCS 2023 / *Annals of Mathematics* (https://arxiv.org/abs/2302.05537).
- **Thomas F. Bloom and Olof Sisask**, *The Kelley-Meka bounds for sets free of three-term arithmetic progressions*, 2023 (https://arxiv.org/abs/2302.07211).
- **Jean Bourgain**, *On triples in arithmetic progression*, *Geom. Funct. Anal.* 9(5), 968-984 (1999).
- **Yael Dillies and Bhavik Mehta**, *LeanAPAP* repository, blueprint, and physical almost-periodicity / unbalancing infrastructure (https://github.com/YaelDillies/LeanAPAP).
- **Mathlib and AddCombi Communities** (https://github.com/leanprover-community/mathlib4, https://github.com/leanprover-community/add-combi).
