# REPRODUCE skeptic report — proteingym-cancer-dms-zero-shot, partial win p1

context: subagent (Claude Code Agent, fresh context)

## Definition under test (verbatim, from CLAIM.md "Partial wins")

> p1: Beat the live per-assay best by >= 0.015 Spearman on at least three cancer-gene assays simultaneously with ONE method and ONE frozen configuration (pre-registered, fitted only on non-cancer assays). Multi-assay consistency with a single configuration is far stronger evidence than a single-assay win.

Success criterion (verbatim, CLAIM.md): "Success means a saved score file assigning one real-valued fitness prediction to every mutant in the ProteinGym reference CSV for a chosen cancer-gene DMS assay (the assay's own reference file as distributed by ProteinGym, sha256 logged), produced by a method that is ZERO-SHOT with respect to that assay - it may use sequence, structure, MSAs, and other models' published score files, but no measurement from ANY ProteinGym DMS assay of the same UniProt protein may enter the method, and no hyperparameter, weight, threshold, model-selection decision or combination weight may be chosen using the target assay's labels - such that the Spearman correlation, recomputed by the skeptic with the official ProteinGym scoring convention (same mutant set, same direction convention, same NaN handling), is STRICTLY HIGHER (direction: max) than the maximum over all model columns for that assay in the live DMS-level Spearman CSV (re-fetched immediately before claiming) by at least 0.015 absolute. ..."

Method M1 (PREREG.md, quoted in substance): protein-balanced mean Spearman of each of the 95 model columns over the fitting
assays; select the 12 highest; on the target assay, z-score each selected model's raw scores over that assay's mutants
(mean 0, sd 1; no labels) and take the unweighted mean of the 12 z-scores.

I wrote my own checker from these texts before reading the author's code (panel_work/reproduce/check.py), then compared.

## 1. Objects, mutant sets, finiteness

All 13 result files are present, one per assay named in split.json target_assays. For every one: the result mutant set
equals the matching inputs/reference/ mutant set, with the same row count, unique mutants, and every prediction finite
(no NaN, no inf). The 13 inputs/scores/ target files carry the same mutant set as their reference file, and their
DMS_score column agrees with the reference's to 1e-8. Row counts: BRCA1 1837, BRCA2 265, ERBB2 326, MSH2 16749, the three
P53_Giacomelli 7467 each, P53_Kotler 1048, PTEN_Matreyek 5083, PTEN_Mighell 7260, RASH 3134, RASK_abundance 26012,
RASK_binding 24873. No model-column NaN appears in any fitting or target score file, so NaN handling is moot.

## 2. Recomputed Spearman and margins (my checker, scipy spearmanr, joined on mutant)

| assay | rho (result file) | live table max | margin | >= 0.015 |
|---|---|---|---|---|
| BRCA1_HUMAN_Findlay_2018 | 0.593036 | 0.560 | +0.0330 | yes |
| BRCA2_HUMAN_Erwood_2022_HEK293T | 0.433512 | 0.534 | -0.1005 | no |
| ERBB2_HUMAN_Elazar_2016 | 0.540154 | 0.695 | -0.1548 | no |
| MSH2_HUMAN_Jia_2020 | 0.420702 | 0.409 | +0.0117 | no |
| P53_HUMAN_Giacomelli_2018_Null_Etoposide | 0.523377 | 0.509 | +0.0144 | no |
| P53_HUMAN_Giacomelli_2018_Null_Nutlin | 0.501448 | 0.523 | -0.0216 | no |
| P53_HUMAN_Giacomelli_2018_WT_Nutlin | 0.553182 | 0.616 | -0.0628 | no |
| P53_HUMAN_Kotler_2018 | 0.768585 | 0.722 | +0.0466 | yes |
| PTEN_HUMAN_Matreyek_2021 | 0.565763 | 0.516 | +0.0498 | yes |
| PTEN_HUMAN_Mighell_2018 | 0.578414 | 0.561 | +0.0174 | yes |
| RASH_HUMAN_Bandaru_2017 | 0.585065 | 0.619 | -0.0339 | no |
| RASK_HUMAN_Weng_2022_abundance | 0.382280 | 0.470 | -0.0877 | no |
| RASK_HUMAN_Weng_2022_binding-DARPin_K55 | 0.717125 | 0.710 | +0.0071 | no |

Count with margin >= 0.015: 4 (p1 needs >= 3). The four rho values and margins match CLAIM.md's table to the digits it
prints, and the nine non-wins match the claim that nine do not clear the bar. Each bar is the maximum over all 97 model
columns of that row, excluding Number of Mutants, Selection Type, UniProt ID, MSA_Neff_L_category and Taxon (all five are
present in the packaged CSV). I re-fetched the live CSV from the status source URL during this review (141,235 bytes): as a
dataframe it is equal to the packaged inputs/DMS_substitutions_Spearman_DMS_level.csv (217 x 102, .equals() True), and the
margins computed against the freshly fetched table are identical to the table above.

## 3. Independent re-implementation of M1

From the PREREG.md text alone, using inputs/scores/ and inputs/split.json: 95 model columns per score file (one fitting
file, ANCSZ_Hobbs_2022, carries an extra DMS_bin_score column, which I excluded as a label-derived column rather than a
model); Spearman of each column against DMS_score on each of the 187 fitting assays (0 NaN rhos); protein-balanced mean
with weight 1/(number of fitting assays sharing that UniProt ID), taken from inputs/DMS_substitutions.csv. My top 12 with
their protein-balanced means: VenusREM 0.54197, ProSST-2048 0.53046, ProSST-4096 0.52445, S3F_MSA 0.51723,
ProSST-1024 0.51300, S2F_MSA 0.50814, ESCOTT 0.50258, ESM3 0.49936, ProSST-512 0.49900, ProSST-128 0.49637,
RSALOR 0.49134, S3F 0.48957 — identical, and in the same order, to the 12 listed in EXTERNAL_SCORES.md. The 13th is
PoET 0.48930, so the 12/13 gap is only 0.00026; the cut is thin, but both K=12 and the ranking rule are pre-registered and
computed on fitting assays only.

One configuration (population z-score, ddof=0, equal weights) reproduced all 13 result files, with maximum absolute
deviation per file between 2.9e-10 and 5.2e-10, i.e. the 10-significant-digit rounding of the packaged score inputs; the
Spearman recomputed from my own predictions equals the Spearman from the result files to 0.0e+00 on all 13. The sample-sd
variant (ddof=1) deviates by up to 5.1e-3 and is not the configuration used. Only after this did I read code/m1.py: it
implements the same steps. Its protein weights are read from the live CSV's UniProt ID column instead of
DMS_substitutions.csv, but the resulting selection is the same — its printed selection is exactly my 12 — and, run from a
copy of claim/, it reproduced result/ with the same ~4e-10 agreement.

## 4. Label independence and leakage

- Randomising the targets' DMS_score (in copies of both inputs/scores/ and inputs/reference/) and re-running code/m1.py
  changed no prediction at all: max |diff| = 0.0 on all 13 files, and the selected 12 models were unchanged. My own
  re-implementation is likewise invariant under permuted target labels (exact array equality).
- UniProt IDs: the 187 fitting assays' UniProt set is disjoint from the 13 targets' set (BRCA1, BRCA2, ERBB2, MSH2, P53,
  PTEN, RASH, RASK _HUMAN), and also from the 17 extra-excluded oncology assays' set. fitting_assays equals all 217 assays
  in DMS_substitutions.csv minus the 13 targets minus the 17 extra exclusions.
- sha256 of PREREG.md = 365981fd71fee2d6d4e236fbdfaa476f05b76d8129de5f0e0722581a061420ad and of inputs/split.json =
  bf163ae630a11ccf759b27ee72cce9f617c8b48c262c891d5298541a9a5a3163, both as stated in CLAIM.md / PREREG.md.

## 5. Determinism

Two consecutive runs of code/m1.py on an untouched copy produced byte-identical outputs for all 13 assays, and the same
selection both times. My own checker gave bit-exact equal prediction arrays on repeated reads of the same inputs. No RNG
and no order- or thread-dependent result was observed. The result/ files are not byte-identical to a fresh run only in
their float text formatting; values agree to ~4e-10, the rounding level of the distributed inputs.

## Caveats (none of them failures)

- The bar is read from the published table at three decimals; the four winning margins (0.0330, 0.0466, 0.0498, 0.0174)
  all exceed 0.015 by more than any 0.0005 rounding of the published value.
- PTEN_HUMAN_Mighell_2018 at +0.0174 is the narrowest of the four; since p1 needs three, it is not load-bearing.
- Everything above is exhaustive over the 13 claimed objects, the 187 fitting assays and the 95 model columns; nothing was
  sampled or spot-checked.

pass: true
