# Honesty gate — dreval-ldo-beat-naive-mean-effects (2026-10-24T03:59:35Z)

status: CONFIRMED_SOLUTION
confirmed_scope: On DrEval/drevalpy 1.3.5's own CTRPv2 leave-drug-out pipeline (pinned October-2025 data, `LN_IC50_curvecurator`, 10 CV splits, all 235,974 measured pairs scored with no subsetting, abstention or NaN masking), the drevalpy model class `PotencyTransfer` attains a mean normalized R² of **+0.2249** on the package's own default seed-42 splits (SE 0.0354, 10/10 splits positive) and **+0.2268** on a second split generation verified independent of it (SE 0.0482, 0/10 shared test folds, mean best-match Jaccard 0.088) — both computed by drevalpy's own evaluation code, both exceeding by more than 0.02 absolute and more than 2 SE the live-decoded maximum over all eleven published LDO models (+0.023466, MultiOmicsNeuralNetwork; page re-fetched 2026-10-24T02:41:09Z, sha256 `b7dd9273…4364`), and both beating the author's same-environment same-splits re-runs of NaiveMeanEffectsPredictor (−0.0247, −0.0185) and MultiOmicsNeuralNetwork (−0.0275 and −0.0931, as recomputed here) on 20/20 splits, and on all 20 again when the leader comparison is restricted to the ~54% of pairs drevalpy actually scores that model on — subject to these limits, which are part of the result: it is a benchmark result on a public cell-line screen with no clinical meaning; the model predicts one potency offset per drug and contributes nothing to the ~29% of the scored variance that is drug × cell-line interaction; it adds an external potency prior trained on ~53,500 NCI-60 compounds (every CTRPv2 compound, and everything within Tanimoto 0.60 of one, excluded from that prior's training set), which no leaderboard model uses, so the comparison is not like-for-like on training data, although a τ = 0 ablation of the frozen model — run by this skeptic and independently reproduced in the package on both generations — puts the architecture at +0.1450 and +0.1556 (SE 0.0284, 0.0333) with the prior switched off entirely, still clearing both margin conditions and still beating the leader 10/10 on seed 42, so the prior supplies about 35% of the gain rather than all of it and the record falls under the strict reading of the author's own pre-registration too; the published +0.0235 is in any case a maximum over eleven models the DrEval paper's own Friedman test cannot distinguish (p = 0.742), so ratios against it carry no effect-size meaning; the second generation required patching drevalpy's `GroupKFold` call with `shuffle=True`, because in 1.3.5 the split seed provably does not change LDO test folds, so it is independent but not unmodified-package-generated; the result survives removing the 49 drug-combination "drugs" (+0.2031, +0.2023) but is roughly three times weaker for drugs with no close training analogue (max Tanimoto < 0.30: pooled +0.1615 and +0.1114, per-split mean +0.1174 and +0.0527, 7/10 and 5/10 splits positive), i.e. not separable from the bar on the independent generation's hardest band, and that novel-scaffold band is the part that does depend on the external prior, going negative without it (−0.0186 and −0.0147 per-split); the vault diagnostics on the 82 drugs held out of all development reproduce exactly from the package's now-shipped and provably pre-registered vault list but are too noisy to establish anything (+0.1153 and +0.0868 at standard errors of 0.1404 and 0.1437, t = 0.8 and 0.6), and the package's strictest-exclusion figure (+0.1736 at a Tanimoto-0.50 exclusion) is shipped as a receipt but needs the external prior rebuilt to check and was not verified here; and two of the six artefacts whose sha256 `PREREG.v4.md` freezes no longer match it, because a path sanitisation rewrote their path literals — a disclosed and separately documented change which this skeptic verified, by diffing against the originals with paths masked, to be nothing but those literals plus one `import os` line per file, with every constant, threshold and hyperparameter intact and the other four frozen artefacts, the whole model among them, matching exactly.

## Panel

| seat | file | verdict |
|---|---|---|
| REPRODUCE | `reproduce.md` | pass: true — wrote its own checker first, reproduced every figure to six digits, verified the leave-drug-out property exhaustively in all 20 splits, proved the external prior cannot leak responses |
| NOVELTY | `novelty.md` | pass: true — fetched and decoded the status page itself, enumerated all 306 open pull requests, verified the index works rather than trusting zeros, found no published LDO result above 0.0235 from any group |
| CRITERION | `criterion.md` | pass: true — judged the criterion clause by clause, ran drevalpy's own evaluation code independently, and revised its own verdict twice as defects were repaired |

All three seats ran in fresh contexts, barred from this run's notes outside `claim/`.

## What the panel changed, not just checked

The panel did not merely ratify this claim; it altered it.

- **REPRODUCE built two attacks the verification script accepted** — rescaling the ruler's cell-line
  effects (reported +0.4088 and passed) and silently dropping the five worst test drugs per split (+0.2961).
  Both are now permanent corruption tests and both are rejected. Chasing the first is what uncovered a
  previously unknown defect in drevalpy's experiment loop.
- **NOVELTY's four framing objections were adopted wholesale**: the published Friedman p = 0.742, the
  not-like-for-like training data, the uncontested frontier, and carrying the Lavelle et al. citation and the
  NCI-60 QSAR prior art into the load-bearing documents rather than only the contributor narrative.
- **CRITERION found a contradiction in this run's own pre-registration** that the author had missed:
  `PREREG.md` section 5 forbade "any other external experimental activity data", which is what the NCI-60
  prior is trained on. It also ran the with/without-prior ablation that `H10-PRECOMMIT.md` had
  pre-committed to and the author never ran. `claim/PREREG5-RECONCILIATION.md` answers it by showing the
  claim clears every pre-registered bar under the strict reading too (+0.1450 and +0.1556 against a bar of
  0.0435), rather than by arguing the ambiguity away.
- **Three regressions introduced by the author after the first verdict** — two hash-frozen artefacts edited,
  four scripts left syntactically invalid, and an unsupportable vault claim — were caught by CRITERION on
  re-verification and repaired. The vault retraction is recorded in `claim/DIAGNOSTICS.md`.

## Evidence that the development protocol held

The 82-drug vault, pre-registered in `PREREG.md` section 4 before any response value was read, is shipped as
`claim/how-we-built-it/vault_drugs.txt` and hashes to
`fd91cf6913afe54e641a8a0719e2856adfdf20f6749c9d2258d0cb80b0ef0cb9` — the value frozen in the
pre-registration. It therefore provably is the pre-registered vault and cannot have been chosen after seeing
results. Its figures (+0.1153 and +0.0868) are reported with their standard errors and explicitly described
as not separable from zero.

## Known, disclosed limitations carried in the scope sentence

Two artefacts frozen in `PREREG.v4.md` were path-sanitised to satisfy the no-absolute-paths rule and no
longer match their frozen hashes; the change is one `import os` plus path literals, verified mechanically by
the panel, with old and as-shipped hashes printed in `claim/how-we-built-it/PATH-SUBSTITUTIONS.md`. The four
other frozen artefacts, including the entire model, are shipped unmodified and match exactly. The external
prior's weights are not shipped and its training is not bit-deterministic, so a rebuild reproduces the
method rather than the file. The `teacher050_seed42.txt` receipt needs that rebuild to verify.
