# E. coli/Shigella genotype-to-phenotype, amoxicillin-clavulanic acid: F1 91.97% vs the published rule's 44.5%

## What
On the cluster-held-out TEST partition in result/split.csv (sha256 68a7e358...577dca) of NCBI export PDG000000004.6366 as the claimant describes it, the LightGBM model's predictions in result/test_predictions_amoxicillin-clavulanic_acid.csv score F1 91.97% and accuracy 97.68% (TP 189, FP 7, TN 1200, FN 26), against 44.78% and 69.48% for the code-reimplemented Table 3 genotype rule on the same 1422 rows and 44.5% and 73.6% published, with the model's cluster-bootstrap F1 interval lying above both baselines, for amoxicillin-clavulanic acid only and for database concordance only.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (Python 3 standard library only). It downloads the sha256-pinned NCBI export
(551 MB) and cluster list, recomputes eligibility, phenotypes, the cluster split and the published rule, scores object/test_predictions_amoxicillin-clavulanic_acid.csv, runs a
2,000-replicate cluster bootstrap and checks every threshold. Expected last line: `PASS`. About 1-3 minutes plus the download.
NCBI first served these files under latest_snps/ and moved them to the versioned folder PDG000000004.6366/ when it published a newer version (same files, same sha256).

## Compared to
| bar | F1 | accuracy | source |
|---|---|---|---|
| published genotype rule (paper, 2026-06-11 export) | 44.5% | 73.6% | Table 3, PMC13513162, fetched 2026-10-17T00:27:32Z |
| same rule recomputed on our TEST rows | 44.78% | 69.48% | verify-it-yourself |
| this predictor (TEST clusters) | 91.97% (95% cluster CI 86.91%-95.42%) | 97.68% | object/ |

Confusion matrices on 1422 TEST comparisons (1045 clusters): model TP 189 FP 7 TN 1200 FN 26;
rule TP 176 FP 395 TN 812 FN 39.

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
