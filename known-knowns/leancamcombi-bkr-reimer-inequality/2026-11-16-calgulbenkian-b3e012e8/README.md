# Lean 4 Kernel Proof of the van den Berg–Kesten–Reimer Inequality (`Finset.card_certificator_le`)

## What

On a clean LeanCamCombi checkout at master 0a42535 (toolchain v4.36.0-rc2, dependency revisions equal to the manifest pins), replacing only the `:= sorry` of Finset.card_certificator_le with the proof in object/VanDenBergKesten.lean (plus extra private helpers and non-public imports) yields a file that elaborates with no errors, leaves the lemma statement and certificator definition verbatim, depends only on propext, Classical.choice and Quot.sound, while issue #34 is still open with no PR proving it.

## Check it yourself

From this package folder (with a clean `YaelDillies/LeanCamCombi` checkout at commit `0a42535119073f677dd60a28acbbdcda11b87f60` and Mathlib cache):

```sh
LEANCAMCOMBI_ROOT=/path/to/LeanCamCombi sh verify-it-yourself/run_checks.sh
```

Expected final output line: `PASS` (runs in about 12 seconds on a laptop once the `LeanCamCombi` cache is downloaded).

## Compared to

- **Repository & Issue**: https://github.com/YaelDillies/LeanCamCombi/issues/34 (`master` commit `0a42535119073f677dd60a28acbbdcda11b87f60`)
- **File & lemma**: `CamCombi/PlainCombi/VanDenBergKesten.lean`, `Finset.card_certificator_le`
- **Upstream status**: `:= sorry` (`Issue #34` open since 2025-01-22, unassigned, `0` open or closed PRs proving the lemma; general Reimer inequality also listed as an open `theorem_wanted` in `facebookresearch/atlas-lean`)
- **Source URL**: https://raw.githubusercontent.com/YaelDillies/LeanCamCombi/master/CamCombi/PlainCombi/VanDenBergKesten.lean (fetched `2026-11-15T15:47:21Z`, SHA-256 `9c109ea9c6cb4cf479a6b3d07a5a581e28b41106cb82c54c7ca92c8da91421d2`)

## Not claimed

- The van den Berg–Kesten–Reimer theorem and Butterfly Lemma are classic mathematical results (van den Berg–Kesten 1985; Reimer 2000; Borgs–Chayes–Randall 1999); only the sorry-free Lean 4 formalization is claimed.
- `Finset.card_certificator_le` in `LeanCamCombi` establishes the uniform counting-measure inequality on `Finset (Finset α)`; general non-uniform weighted product measures are not part of the target lemma.

## Credits

- **J. van den Berg and H. Kesten** (*J. Appl. Probab.* 22, 1985, 556-569): original conjecture and monotone BK inequality.
- **D. Reimer** (*Combin. Probab. Comput.* 9, 2000, 27-32): general proof of the BKR inequality and the Butterfly Lemma.
- **C. Borgs, J. T. Chayes, and D. Randall** (*Perplexing Problems in Probability*, Birkhäuser, 1999, 159-173): orthogonality exposition of Reimer's Butterfly Lemma.
- **Yaël Dillies** (<https://github.com/YaelDillies/LeanCamCombi>): Lean 4 definition of `Finset.certificator` (`𝒜 □ ℬ`), companion lemmas, and Issue #34 specification.
- **Mathlib Community** (<https://github.com/leanprover-community/mathlib4>): Lean 4 `Finset` and `BooleanAlgebra` foundations.
