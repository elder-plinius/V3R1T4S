# E. coli/Shigella genotype-to-phenotype, ampicillin: F1 98.80% vs the published rule's 93.9%

## What
Recomputed from the saved per-isolate file, on the hash-selected 20 percent test partition of NCBI Pathogen Detection export PDG000000004.6366 (1715 ampicillin R/S rows, one per isolate, in 1257 groups made of 365 whole PDS SNP clusters holding 823 rows plus 892 isolates with no PDS accession each kept as its own group), the saved LightGBM predictor scores F1 98.80% and accuracy 98.78% (TP 867, FP 8, TN 827, FN 13) against 94.40% F1 and 94.52% accuracy (TP 792, FP 6, TN 829, FN 88) for the reimplemented published genotype rule on the same rows and the 93.9% F1 and 94.5% accuracy in Table 3 of the saved status-source copy, with a paired 95% cluster-bootstrap interval of 3.06 to 5.88 F1 points for model minus rule, as a database-concordance result for ampicillin only (no other antibiotic, no other export, no clinical or treatment meaning).

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (Python 3 standard library only). It downloads the sha256-pinned NCBI export
(551 MB) and cluster list, recomputes eligibility, phenotypes, the cluster split and the published rule, scores object/test_predictions_ampicillin.csv, runs a
2,000-replicate cluster bootstrap and checks every threshold. Expected last line: `PASS`. About 1-3 minutes plus the download.
NCBI first served these files under latest_snps/ and moved them to the versioned folder PDG000000004.6366/ when it published a newer version (same files, same sha256).

## Compared to
| bar | F1 | accuracy | source |
|---|---|---|---|
| published genotype rule (paper, 2026-06-11 export) | 93.9% | 94.5% | Table 3, PMC13513162, fetched 2026-10-17T00:27:32Z |
| same rule recomputed on our TEST rows | 94.40% | 94.52% | verify-it-yourself |
| this predictor (TEST clusters) | 98.80% (95% cluster CI 98.25%-99.28%) | 98.78% | object/ |

Confusion matrices on 1715 TEST comparisons (1257 clusters): model TP 867 FP 8 TN 827 FN 13;
rule TP 792 FP 6 TN 829 FN 88.

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
