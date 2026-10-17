# E. coli/Shigella genotype-to-phenotype, gentamicin: F1 96.28% vs the published rule's 92.4%

## What
On the single pre-fixed hash split of NCBI export PDG000000004.6366 (1623 gentamicin R/S comparisons in 1192 groups, of which 357 are PDS SNP clusters and 835 are isolates with no PDS accession treated as singletons), the saved LightGBM gentamicin predictor scores F1 96.28% and accuracy 98.64% (TP 285, FP 9, TN 1316, FN 13) against 92.41% and 97.17% (TP 280, FP 28, TN 1297, FN 18) for the reimplemented published genotype rule on the identical rows, which is 3.88 F1 points above the published 92.4% and 3.87 above the recomputed rule, with the model F1 above the rule's 95% percentile cluster-bootstrap interval (88.09% to 95.31%) and accuracy above the published 97.6%; this is a database-concordance result for gentamicin on that one partition only, carries no clinical interpretation, and rests on a published-figure re-read and NCBI file hashes that this review could not re-check.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (Python 3 standard library only). It downloads the sha256-pinned NCBI export
(551 MB) and cluster list, recomputes eligibility, phenotypes, the cluster split and the published rule, scores object/test_predictions_gentamicin.csv, runs a
2,000-replicate cluster bootstrap and checks every threshold. Expected last line: `PASS`. About 1-3 minutes plus the download.
NCBI first served these files under latest_snps/ and moved them to the versioned folder PDG000000004.6366/ when it published a newer version (same files, same sha256).

## Compared to
| bar | F1 | accuracy | source |
|---|---|---|---|
| published genotype rule (paper, 2026-06-11 export) | 92.4% | 97.6% | Table 3, PMC13513162, fetched 2026-10-17T00:27:32Z |
| same rule recomputed on our TEST rows | 92.41% | 97.17% | verify-it-yourself |
| this predictor (TEST clusters) | 96.28% (95% cluster CI 93.68%-98.00%) | 98.64% | object/ |

Confusion matrices on 1623 TEST comparisons (1192 clusters): model TP 285 FP 9 TN 1316 FN 13;
rule TP 280 FP 28 TN 1297 FN 18.

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
