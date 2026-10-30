# ProteinGym cancer-gene assays, partial win p1: one frozen zero-shot ensemble beats the table on 4 of 13

## What

With one pre-registered, frozen, zero-shot configuration (equal-weight mean of the z-scored top-12 of 95 published ProteinGym v1.3 model columns, selected only on 187 non-cancer assays sharing no UniProt id with any target), M1 exceeds the maximum over all 97 model columns of the 2026-10-18 live ProteinGym DMS-level Spearman table by at least 0.015 on four of the 13 pre-registered cancer-gene assays — PTEN_HUMAN_Matreyek_2021 (+0.0498), P53_HUMAN_Kotler_2018 (+0.0466), BRCA1_HUMAN_Findlay_2018 (+0.0330) and PTEN_HUMAN_Mighell_2018 (+0.0174), three distinct cancer genes — while losing on the other nine, a 4/13 rate consistent with the pre-registered 16% per-assay base rate and therefore no evidence of general superiority on cancer-gene assays.

Target: `proteingym-cancer-dms-zero-shot`, partial win p1 (V3R1T4S bank, commit 04fdfba). The objects are the 13 prediction
files in `object/`, one per pre-registered cancer-gene assay, all made by the same frozen method M1.

## Check it yourself

```
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS`. It needs Python 3 (standard library) and downloads ProteinGym's 43 MB reference zip once. A few
minutes on a laptop.

## Compared to

Live ProteinGym DMS-level Spearman table,
https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv,
fetched 2026-10-18T20:50:39Z. Maximum over all 97 model columns:

| assay | table max (column) | M1 | margin |
|---|---|---|---|
| PTEN_HUMAN_Matreyek_2021 | 0.516 (VenusREM) | 0.5658 | +0.0498 |
| P53_HUMAN_Kotler_2018 | 0.722 (ProSST K=1024) | 0.7686 | +0.0466 |
| BRCA1_HUMAN_Findlay_2018 | 0.560 (S3F-MSA) | 0.5930 | +0.0330 |
| PTEN_HUMAN_Mighell_2018 | 0.561 (S3F-MSA) | 0.5784 | +0.0174 |

## Not claimed

- General superiority. M1 loses on the other nine assays, worst ERBB2_HUMAN_Elazar_2016 (-0.155), and 4/13 matches the
  pre-registered 16% per-assay rate (P(>= 4 of 13) = 0.14).
- The full criterion on PTEN_HUMAN_Matreyek_2021 is a separate claim, draft PR #463. The two overlap on that assay.
- Partial win p2 (MSH2 +0.02): not met (+0.0117).
- No clinical meaning: a laboratory mutational scan says nothing about any person's variant.
- The 12 published models may themselves have been developed with ProteinGym data.

## Credits

- ProteinGym: Notin, Kollasch, Ritter, van Niekerk, Paul, Spinner, Rollins, Shaw, Orenbuch, Weitzman, Frazer, Dias,
  Franceschi, Gal and Marks, NeurIPS 2023 Datasets and Benchmarks (github.com/OATML-Markslab/ProteinGym,
  marks.hms.harvard.edu/proteingym).
- The assays: Matreyek et al., Genome Medicine 2021 (PTEN abundance); Mighell et al., AJHG 2018 (PTEN phosphatase);
  Kotler et al., Molecular Cell 2018 (TP53); Findlay et al., Nature 2018 (BRCA1).
- The 12 combined models, as distributed in ProteinGym (primary references in ProteinGym's README): VenusREM; ProSST
  (K = 128, 512, 1024, 2048, 4096); S3F and S3F-MSA; S2F-MSA; ESCOTT; ESM3 open; RSALOR.
- Target definition: the V3R1T4S bank (github.com/elder-plinius/V3R1T4S).
