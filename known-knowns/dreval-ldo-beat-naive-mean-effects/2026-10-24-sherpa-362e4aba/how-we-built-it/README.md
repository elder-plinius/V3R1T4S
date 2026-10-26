# How it was built

Every file here is either the frozen model, a script that was actually run, or a pre-registration.

## The model

| file | role |
|---|---|
| `potency_core.py` | the reference implementation, frozen in `PREREG.v4.md` |
| `potency_transfer_model.py` | the drevalpy 1.3.5 model class wrapping it, so the confirmatory runs go through the package's own pipeline, splits, tuning loop and evaluation |
| `potency_core_fast.py` | an exact-equivalent faster core, used only for the 400 null-test controls. Equivalence receipts: identical hyperparameter choices, predictions within 2.1e-7 |
| `devharness.py` | the development harness: removes the 82 vault drugs and uses development split seed 7 |

### What it computes

For an unseen drug *d* and cell line *c*:

    prediction(c, d) = cell_line_mean(c) + b + kappa * (delta_hat(d) - mean training delta)

`cell_line_mean(c)` is exactly what the NaiveMeanEffectsPredictor predicts when a drug is unseen, so the
model's entire contribution is the second term: an estimate of that drug's own average potency.

`delta_hat` is kernel ridge regression of each **training** drug's mean residual on

    K = Tanimoto(Morgan 2048) + beta * Jaccard(target pathways) + tau * z z^T

`alpha, beta, tau, b, kappa` are chosen by 5-fold **drug-grouped** cross-validation inside the training
drugs only (inner seed 12345). `kappa` is clipped to [0, 1.5]. Views are identifiers only, so drevalpy keeps
every drug and cell line in the evaluation — 235,974 pairs, the full measured set, with no
feature-availability subsetting.

**No per-drug statistic is ever computed over data that contains held-out drugs.** Everything is learned
inside `train()` from the training rows the pipeline hands it.

## The external potency prior (the decisive component)

**Credit first.** The idea of improving unseen-drug prediction by training on the public NCI-60 screen is
from **Lavelle et al., arXiv:2608.11444** (2026), whose Table 3 reports drug-blind R² rising from 0.03 to
0.22 on an expansion dominated by NCI-60. Predicting NCI-60 panel potency from structure is itself an
established QSAR problem (Cortés-Ciriano et al., `10.1093/bioinformatics/btv529`; Martorana et al.,
`10.3390/ijms232214374`). This work's only addition is the exclusion rule below and the sensitivity curve
over its threshold.

| file | role |
|---|---|
| `h10_build_teacher.py` | builds the NCI-60 training set and applies the exclusions |
| `h10_leak_audit.py` | the audit that caught 3 CTRPv2 compounds hidden under other identifiers |
| `h10_teacher_threshold.py` | retrains the prior at each exclusion threshold |
| `H10-PRECOMMIT.md` | the rules, fixed before any NCI-60-derived feature was scored, with both amendments dated |

`z` is a structure-only potency prior: an MLP (2048-1024-256-1, dropout 0.3, AdamW, 25 epochs) trained on
**53,486 NCI-60 compounds** to predict panel-mean log10 GI50 at the single standard 1e-4 M top dose, from
Morgan-2048 fingerprints alone. Inside NCI-60 its random 5-fold CV Pearson r is 0.80.

**Exclusions, the part that matters.** Removed from the prior's training data: every compound sharing a
PubChem CID with a CTRPv2 drug; every compound whose **salt-stripped** parent shares an InChIKey
connectivity block with a CTRPv2 drug; and every compound within **Tanimoto 0.60** of any CTRPv2 compound
(474 removed). So no CTRPv2 drug — vault drugs included — and no close analogue of one, is in the prior's
training data.

The audit is why the rule is this strict: the original rule (CID match plus raw-SMILES Tanimoto 0.85) let
**3 CTRPv2 compounds through as salt forms**, because counter-ions add fingerprint bits and push a salt
below the cutoff. Found before claiming; recorded with the affected identifiers.

## Confirmation and verification

| file | role |
|---|---|
| `repro_seed42.sh` | re-runs the published models in this environment on the official splits |
| `make_splits_independent.py` | builds the genuinely independent second split generation and enforces the pre-committed independence check |
| `run_confirmatory.py` | runs the frozen model through drevalpy's own CLI entry point |
| `evaluate_with_drevalpy.py` | scores it with the package's own `parse_results` + `prep_results` |
| `diagnostics.py` | the pre-declared subset diagnostics (single agents, combinations, vault, similarity bands) |
| `null_test.py` | the 400-control permutation test |

## Pre-registrations, in order, each superseding only what it names

| file | what it fixed |
|---|---|
| `PREREG.md` | the criterion, the statistic, the thresholds, the vault, the forbidden inputs, `null_test: required` |
| `PREREG.v2.md` | pinned drevalpy 1.3.5, because 1.6.0 lacks the published leader |
| `PREREG.v3.md` | pinned the October-2025 data record, because the current one breaks that leader |
| `PREREG.v4.md` | froze the model and the confirmatory protocol, with hashes |
| `PREREG.v5.md` | recorded that the seed repeat was not independent, and defined the corrected generation |

`PREREG.v4.md` section 2 states plainly how many configurations were tried in development (about 15, all
logged) and that the development numbers are not the claim.

## No hyperparameter file

`get_hyperparameter_set()` returns `[{}]`: there is nothing for drevalpy's outer tuning loop to choose,
because every hyperparameter is selected by drug-grouped CV inside the training drugs. The
`best_hpams_split_*.json` files in the result directory are therefore `{}` by design.
