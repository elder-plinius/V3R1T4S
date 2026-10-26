# Diagnostics — where the result holds and where it is weakest

Every number here is from the shipped `object/` files, reproducible with
`attempts/confirmation/code/similarity_bands.py` and `diagnostics.py`. None of it is the claim; all of it was
pre-declared in `how-we-built-it/PREREG.v4.md` section 5 and is reported whichever way it fell.

## By similarity to the training drugs — the band that matters

Single agents only, so the known combination leak cannot carry a band. "max Tanimoto" is each held-out
drug's maximum Morgan similarity to any drug in that split's train+validation set.

| max Tanimoto to training | drugs | pairs | pooled normalized R² | mean of per-split | splits > 0 |
|---|---:|---:|---:|---:|---:|
| **seed 42** | | | | | |
| [0.00, 0.30) — novel scaffolds | 207 | 85,262 | **+0.1615** | +0.1174 | 7/10 |
| [0.30, 0.45) | 118 | 52,387 | +0.0900 | +0.0074 | 7/10 |
| [0.45, 0.60) | 80 | 33,918 | +0.4485 | +0.3826 | 10/10 |
| [0.60, 1.01) — close analogues | 91 | 34,216 | +0.3438 | +0.2644 | 7/10 |
| all single agents | | 205,783 | +0.2354 | | |
| **independent generation** | | | | | |
| [0.00, 0.30) — novel scaffolds | 214 | 90,342 | **+0.1114** | +0.0527 | 5/10 |
| [0.30, 0.45) | 109 | 45,761 | +0.1989 | +0.1324 | 8/10 |
| [0.45, 0.60) | 80 | 33,755 | +0.4028 | +0.1465 | 6/10 |
| [0.60, 1.01) | 93 | 35,925 | +0.3881 | +0.1980 | 7/10 |
| all single agents | | 205,783 | +0.2293 | | |

**Read this honestly.** The result does extend to drugs with no close analogue in training — 207 and 214
such drugs, pooled +0.1615 and +0.1114, both above the 0.0435 bar. But that band is the **weakest and the
least stable**: its per-split mean is far below its pooled value (+0.117 and +0.053), and only 7/10 and
5/10 splits are positive. Performance is best in the middle-to-high similarity bands. Anyone reading this
as "solved for novel chemistry" is reading it wrong.

**And it depends on how much chemistry is in training.** In the development setting, where 82 vault drugs
were withheld from training as well as testing (417 training drugs instead of ~490), the novel-scaffold band
was **not positive at all** (mean per-split −0.046, `../attempts/interaction-transfer/output/h6_widegrid.log`).
The novel-scaffold gain is therefore sensitive to training-set size, which is exactly what one expects if the
mechanism is interpolation between known chemistry rather than genuine extrapolation.

## By drug type

| subset | PotencyTransfer | baseline | note |
|---|---:|---:|---|
| all drugs (seed 42) | +0.2249 | −0.0247 | the claim |
| single agents only | +0.2038 | −0.0297 | the gain is **not** the combination leak |
| combinations only | +0.2031 | −0.1953 | drevalpy issue #300 lists these as an open LDO leak |
| the 82 vault drugs | +0.1153 (SE **0.1404**) | −0.1345 (SE 0.0533) | never examined during development |
| the 74 never-exposed vault drugs | +0.0868 (SE **0.1437**) | −0.1493 (SE 0.0559) | see the vault note below |

**The vault numbers do not support a claim, and an earlier version of this file wrongly said they were
"still above the bar".** With standard errors of 0.14 on 10 splits, t is about 0.6 to 0.8: these estimates
are not separable from zero, let alone from the 0.0435 bar. The vault is 82 of 545 drugs, so a per-split
vault subset is small and the spread is correspondingly large. What they *do* show is a direction — the
point estimates are positive for this model and clearly negative for the baseline (−0.1345, SE 0.0533,
which *is* separable) — and nothing stronger should be read into them. The correction was prompted by the
verification panel after this run shipped the standard errors for the first time.

The vault was drawn from a fixed seed before any response value was read, and 8 of its 82 identifiers were
briefly exposed in one descriptive computation through a whitespace-splitting bug; that is why both the
82-drug and the 74-drug figures are reported. The vault was deliberately **not** redrawn, because redrawing
after exposure would be a choice made with knowledge of the data.

## Analogue-exclusion sensitivity of the external prior

| external compounds excluded within Tanimoto | development | confirmatory (seed 42) |
|---|---:|---:|
| 0.85 (the original, leaky rule) | +0.227 | — |
| 0.70 | +0.172 | — |
| **0.60 (frozen)** | **+0.163** | **+0.2243** |
| 0.50 (strictest) | +0.123 | **+0.1736** |

Monotone. Part of the prior's power is analogue knowledge; a substantial part survives at the strictest
setting, where no external training compound is within Tanimoto 0.50 of any benchmark drug.

## What remains unsolved

The model predicts **one scalar per drug**, so the drug × cell-line interaction — about **31%** of what this
metric scores — is untouched by the claim. A development-only exploration of transferring interaction
profiles from similar training drugs (`../attempts/interaction-transfer/`) raised development performance
from +0.163 to +0.192, improving in 10/10 splits — **but gave nothing on novel scaffolds** (−0.001, 5/10
splits). It is recorded as a live lead, not part of this claim, and it was not run on any confirmatory split.

---

## A third defect in the benchmark's tooling, found while verifying the ruler

**In drevalpy 1.3.5, every model after the first in a single run is trained on the validation rows added
once more per preceding model.**

`experiment.py` binds `train_dataset = split["train"]` **without copying**, then calls
`train_dataset.add_rows(validation_dataset)` before the final fit. `add_rows` mutates in place, so the
stored split permanently gains the validation rows. The next model in the same run takes the same object and
adds validation again.

**Evidence, from this claim's own object.** The shipped `NaiveMeanEffectsPredictor` ran second in its run
(after `PotencyTransfer`). Replaying its cell-line means over candidate training sets:

| training rows used for the replay | max abs difference from the shipped ruler |
|---|---:|
| train + validation (what the code intends) | 2.14e-01 |
| **train + validation + validation** | **6.25e-07** |
| train + 3 x validation | 1.80e-01 |

Confirmed independently three ways: a hand replay from the object, a direct `model.train()` call, and a full
`train_and_predict` call all reproduce the *intended* fit (2.14e-01 away), while only the double-counted
validation set matches the shipped ruler. The verification panel's reproduce seat found the same 6.25e-07.

### Does it affect this claim? No, to four decimal places.

`attempts/confirmation/code/clean_ruler_robustness.py` re-scores the claim against a **clean** ruler
reconstructed from the object (validation counted once):

| ruler used | seed 42 | independent |
|---|---:|---:|
| shipped (as drevalpy emitted it) | +0.2244 | +0.2263 |
| replayed buggy ruler | +0.2244 | +0.2263 |
| **clean ruler (validation once)** | **+0.2243** | **+0.2261** |

All three agree to 0.0002, all 10/10 splits positive in every case. The claim does not depend on the defect.

### But it has a consequence for the published leaderboard, which this run cannot resolve

The published report evaluates **11 models in one pipeline**. If they ran in a single invocation, then under
this defect the k-th model is fitted on train + k copies of validation — the last model on train plus
**eleven** copies. The ruler that defines every published normalized metric would then itself depend on
where `NaiveMeanEffectsPredictor` sat in that list.

This run **cannot** establish that the published numbers are affected: the published run's model order and
whether it used one invocation or several are not visible from the artefacts fetched here. It is recorded as
a question the maintainers can answer and this run cannot, and it is reported as a duty rather than used to
argue anything about this claim. Reporting it upstream is an outward action and was not taken.

### What it changed in the verification script

A naive ruler-authenticity check — "the shipped ruler must equal the train+validation cell-line mean" —
**fails on a genuine object** because of this defect. `check_claim.py` therefore regresses the shipped ruler
on the replay for each k from 1 to 12 and requires slope 1 and intercept 0 for the best-matching k
(observed: both exactly 0.00000). That tolerates the defect while still rejecting any **rescaling** of the
ruler, which changes the slope for every k. Both attacks the panel built — rescaling the ruler's cell-line
effects by 3x, and silently dropping the five worst test drugs per split — are now permanent corruption
tests in `run_checks.sh` and both are rejected.
