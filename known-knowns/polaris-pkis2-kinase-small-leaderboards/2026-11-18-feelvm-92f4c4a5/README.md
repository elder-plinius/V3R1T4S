# polaris/pkis2-lok-slk-c-1: CLASS_LOK PR-AUC 0.6343 vs the live board's best 0.2553

## What

On the official 132-row test split of the named benchmark polaris/pkis2-lok-slk-c-1, the saved prediction file (probabilities for CLASS_LOK/CLASS_SLK in official split order, manifest with slug, pinned parquet sha256 and exact test index array) achieves skeptic-recomputed CLASS_LOK pr_auc 0.634333770922 — strictly above all six listed leaderboard values (best 0.2553191489361702; margin +0.379014621986; ahead in 1.000000 of 10,000 bootstrap resamples) — fitted per the in-folder pipeline only on the 508 official train rows with the declared continuous LOK/SLK train-row auxiliary (recomputed InChIKey audit: 640 unique keys, 0 train/test overlap), with the harness calibration reproducing the listed null-model values bit-exactly and, per the recorded 400-control null test, the real value above every control (best 0.607118) — a genuine, non-subsumed win for this one cell only.

(Quoted word for word from `panel/gate.md`. Concretely: the benchmark
https://polarishub.io/benchmarks/polaris/pkis2-lok-slk-c-1 asks for a multi-task kinase-inhibition
classifier over the PKIS2 LOK/SLK panel - 640 compounds, official scaffold split 508 train /
132 test, targets `CLASS_LOK` and `CLASS_SLK` (the benchmark README says "threshold: > 80";
the official CLASS columns are exactly (percent inhibition >= 80) - three edge rows sit at
exactly 80.0, all of them train rows; the scoring uses the official CLASS columns directly),
main metric `pr_auc`.
The live leaderboard lists the first target's metric: its six entries are all Polaris "baseline
null model" submissions, four of them constant all-positive predictors, best listed `pr_auc`
0.2553191489361702. The claimed object is `object/preds.csv`: probabilities for both targets on
the official 132 test rows, produced by a two-component rank-blend fitted only on the 508 official
train rows - an ExtraTrees regressor on the continuous percent-inhibition label plus a LightGBM
classifier on the class label, rank-averaged, with a monotone Platt map fitted out-of-fold. No
external PKIS or ChEMBL record and no test-row label was used; an InChIKey audit of the fold is
recorded in the producing run.)

## Check it yourself

From this folder, in any POSIX shell (Git-bash, WSL, Linux/macOS), with any Python 3.8+
(standard library only - no third-party packages needed):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Rough time: ~30 seconds. The check verifies the 132 prediction rows
against the official split, recomputes PR-AUC/ROC from the definition (pure Python, validated
against scikit-learn to 12 decimals in the producing run), checks the +0.020 margin and the
10,000-resample bootstrap rule, reproduces the listed null-model values exactly, rejects a
corrupted copy of the object, and cross-checks the official input pins online when a connection
is available. Full output: `verify-it-yourself/RECEIPTS.md`.

## Compared to

| field | value |
|---|---|
| table | Polaris leaderboard, https://polarishub.io/benchmarks/polaris/pkis2-lok-slk-c-1 |
| cell | CLASS_LOK pr_auc (the metric every listed entry reports; evidence in the-record-we-beat/snapshot.md) |
| value before | 0.2553191489361702 (pkis2-lok-slk-c-1_DGLGraphTransformer_PNAModel, Polaris baseline null model, 2023-12-08) |
| value now | **0.634333770922** (ROC 0.880208333333; CLASS_SLK pr_auc 0.377856659137; two-target mean 0.506095215029) |
| fetched (UTC) | 2026-11-18T13:5xZ (scout) and 2026-11-18T16:04:25Z (immediately before the claim), HTTP 200, page sha256 5671da872b25a3afad11552ace4f0301c3f5afa3db0ac23f45868c9cddb58fbc |
| margin | +0.3790215 absolute (rule: >= +0.020) |
| bootstrap | 10,000 resamples of the 132 test rows, seed 20261118: fraction above the best listed value 1.000000 (rule: >= 0.95); the two-target mean-interpretation: 0.999600 |
| null test | 400 label-permutation controls through the same pipeline; the real value beats all 400 (best control 0.607118) |

## Not claimed

- Any other cell of the bank target. The sibling cells attacked earlier in the same run are
  documented negatives: `pkis2-kit-wt-reg-v2` (test MSE 760.78 vs live 849.61, but the bootstrap
  rule gave 0.807 < 0.95) and `pkis2-kit-wt-cls-v2` (PR-AUC 0.6602, short of the +0.020 margin);
  neither is claimed. The EGFR/RET v2 cells and the v1 single-task boards were measured or scouted
  and not beaten.
- The CLASS_SLK target alone: it is reported (0.3779) but not claimed as a record; its own
  400-control null margin is thin (+0.00021 over the best control, disclosed in
  how-we-built-it/null_test.md). The claimed metric is the one the live leaderboard lists.
- Any statement about the listed entries' models beyond their published values, or about Polaris
  leaderboards not named here.
- No submission was made to Polaris; this package is an offline claim with a checkable object.

## Credits

- Polaris (polarishub.io) and the benchmark's creators (`lu-valencelabs` / the Polaris team): the
  benchmark, the dataset `polaris/kinase-pkis2-1` (CC-BY-4.0), the public API and split, and the six
  listed baseline entries whose published values calibrate the check.
- Drewry et al., PKIS2 (PMID 28767711): the underlying chemogenomic set (GSK, Takeda, Pfizer).
- The V3R1T4S bank entry `polaris-pkis2-kinase-small-leaderboards`, which defined the win rule and
  the traps (empty-board, v1-vs-v2, InChIKey provenance) this claim follows.
- The CheMeleon repository (Burns et al., MIT): its published RF baseline was reproduced on the
  sibling KIT cell in the same run, calibrating the harness before this cell was attacked.
- Produced and verified by the feelvm agent workspace, 2026-11-18; three-skeptic panel
  (reproduce / novelty / criterion) in `panel/`.
