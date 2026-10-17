# E. coli/Shigella genotype-to-phenotype, ciprofloxacin: F1 96.13% vs the published rule's 77.2%

## What
On the 10,836 eligible isolates of NCBI Pathogen Detection export PDG000000004.6366 (hash-pinned in CLAIM.md) with the whole-PDS-cluster split in result/split.csv (sha256 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca), a LightGBM predictor over exported AMR-genotype tokens plus collection year, species label and epi_type scores ciprofloxacin resistant-class F1 96.13% (95% cluster-bootstrap interval 93.65% to 97.84%) and accuracy 98.35% (TP 348, FP 12, TN 1317, FN 16) on 1693 isolate comparisons in 1246 held-out clusters, against 80.36% F1 and 89.72% accuracy (TP 356, FP 166, TN 1163, FN 8) for the reimplemented published genotype-field rule on the same rows (paired F1 difference 95% interval 11.09 to 21.88 points) and 77.2% F1 and 89.9% accuracy published in Table 3 of PMC13513162, as a single-split database-concordance result for ciprofloxacin only with no clinical or treatment meaning.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (Python 3 standard library only). It downloads the sha256-pinned NCBI export
(551 MB) and cluster list, recomputes eligibility, phenotypes, the cluster split and the published rule, scores object/test_predictions_ciprofloxacin.csv, runs a
2,000-replicate cluster bootstrap and checks every threshold. Expected last line: `PASS`. About 1-3 minutes plus the download.
NCBI first served these files under latest_snps/ and moved them to the versioned folder PDG000000004.6366/ when it published a newer version (same files, same sha256).

## Compared to
| bar | F1 | accuracy | source |
|---|---|---|---|
| published genotype rule (paper, 2026-06-11 export) | 77.2% | 89.9% | Table 3, PMC13513162, fetched 2026-10-17T00:27:32Z |
| same rule recomputed on our TEST rows | 80.36% | 89.72% | verify-it-yourself |
| this predictor (TEST clusters) | 96.13% (95% cluster CI 93.65%-97.84%) | 98.35% | object/ |

Confusion matrices on 1693 TEST comparisons (1246 clusters): model TP 348 FP 12 TN 1317 FN 16;
rule TP 356 FP 166 TN 1163 FN 8.

## Not claimed
- No clinical or treatment interpretation: this is a database-concordance benchmark for surveillance, not diagnostic validation.
- Not a claim about other antibiotics (one antibiotic per package) or about the paper's June export (a secondary run on the paper's own
  records gives a similar picture but is not this claim).
- Test-label history: TEST labels were read once by the pre-registered job, then by contrarian checks and pre-registered secondaries
  that did not change the model (details in how-we-built-it/ and the workspace).
- The published rule was reimplemented from its summaries and calibrated to reproduce the paper's per-comparison table exactly; for
  alleles absent from the paper's data the regexes are our reading of the summaries.

## Credits
- Abdullateef Abdullah Alshehri, "Antibiotic-Specific Genotype-Phenotype Concordance and Cross-Database Interoperability in Public
  Escherichia coli/Shigella WGS-AMR Metadata", Int J Mol Sci 2026, 27:7157 (https://doi.org/10.3390/ijms27167157), rule and supplement.
- NCBI Pathogen Detection (https://www.ncbi.nlm.nih.gov/pathogens/) and AMRFinderPlus (M. Feldgarden et al.).
- T. J. Davies et al., Antimicrob Agents Chemother 2020 (PMC7269502), amoxicillin-clavulanate genotype prediction.
- LightGBM (G. Ke et al.), scikit-learn, pandas, numpy.
