# ProteinGym PTEN (Matreyek 2021): zero-shot Spearman 0.5658 vs table best 0.516

## What

On the single ProteinGym assay PTEN_HUMAN_Matreyek_2021, the frozen pre-registered equal-weight z-score ensemble of the 12 model columns that M1 selects using only 187 non-cancer-gene, non-PTEN fitting assays assigns a prediction to all 5,083 reference mutants with no target-assay label entering the method and reaches a skeptic-recomputed Spearman of 0.56576, which exceeds by 0.0498 the 0.516 maximum over all 97 model columns of the independently re-fetched live DMS-level table, satisfying the full success criterion on that one assay alone and implying nothing about the other 12 pre-registered cancer-gene assays or about the method's general performance.

Target: `proteingym-cancer-dms-zero-shot` (V3R1T4S bank, commit 04fdfba). The object is
`object/PTEN_HUMAN_Matreyek_2021.M1.csv`: one prediction per mutant.

Method M1, in one line: rank the 95 published zero-shot columns of ProteinGym v1.3 by protein-balanced mean Spearman over
187 assays of proteins that are neither the 8 bank-named cancer proteins nor 16 further oncology-related proteins. Take the
top 12, z-score each within the target assay (no labels) and average them with equal weights.

## Check it yourself

```
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. It needs Python 3 (standard library) and downloads the official 43 MB ProteinGym reference zip
once (sha256-checked). About a minute on a laptop, plus the download.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| ProteinGym DMS-level Spearman, substitutions | PTEN_HUMAN_Matreyek_2021, max over 97 model columns (VenusREM) | 0.516 | https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv | 2026-10-18T18:46:05Z |

Ours: 0.5658 (margin +0.0498; bar +0.015). Mutant-bootstrap 95% interval of ours minus VenusREM: [+0.039, +0.061].

## Not claimed

- Nothing about the other 12 pre-registered cancer-gene assays. For the record, the same frozen M1 cleared +0.015 on three
  more (P53_HUMAN_Kotler_2018 +0.047, BRCA1_HUMAN_Findlay_2018 +0.033, PTEN_HUMAN_Mighell_2018 +0.017) and fell below the
  table best on six (worst ERBB2_HUMAN_Elazar_2016 -0.155). Those numbers were not panelled. The leave-protein-out base rate
  on the fitting assays was 16%.
- Partial wins p1-p3 are not claimed here.
- No general superiority of the method. The PTEN Matreyek margin leans on the ProSST columns (without them +0.007).
- No clinical meaning: a correlation with a laboratory mutational scan says nothing about any person's variant.
- The 12 published models may themselves have been developed with ProteinGym data; that is outside this result's control.

## Credits

- ProteinGym: Notin, Kollasch, Ritter, van Niekerk, Paul, Spinner, Rollins, Shaw, Orenbuch, Weitzman, Frazer, Dias,
  Franceschi, Gal and Marks, NeurIPS 2023 Datasets and Benchmarks; data and score files from
  https://github.com/OATML-Markslab/ProteinGym and https://marks.hms.harvard.edu/proteingym/.
- The assay: Matreyek, Stephany, Ahler and Fowler, "Integrating thousands of PTEN variant activity and abundance
  measurements reveals variant subgroups and new dominant negatives in cancers", Genome Medicine 13, 165 (2021).
- The 12 combined models, as distributed in ProteinGym (primary references in ProteinGym's README): VenusREM; ProSST
  (K = 128, 512, 1024, 2048, 4096); S3F and S3F-MSA; S2F-MSA; ESCOTT; ESM3 open; RSALOR.
- Target definition: the V3R1T4S bank (github.com/elder-plinius/V3R1T4S).
