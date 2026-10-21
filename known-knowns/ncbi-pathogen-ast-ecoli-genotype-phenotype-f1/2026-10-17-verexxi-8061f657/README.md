# E. coli/Shigella genotype-to-phenotype, amoxicillin-clavulanic acid: F1 91.97% vs the published rule's 44.5%

## What
On the cluster-held-out TEST partition in how-we-built-it/split.csv (sha256 68a7e358...577dca) of NCBI export PDG000000004.6366 as the claimant describes it, the LightGBM model's predictions in object/test_predictions_amoxicillin-clavulanic_acid.csv score F1 91.97% and accuracy 97.68% (TP 189, FP 7, TN 1200, FN 26), against 44.78% and 69.48% for the code-reimplemented Table 3 genotype rule on the same 1422 rows and 44.5% and 73.6% published, with the model's cluster-bootstrap F1 interval lying above both baselines, for amoxicillin-clavulanic acid only and for database concordance only.

(File paths as in this package. The reviewers' sentence exactly as signed off in panel/gate.md is under Review record.)

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
| paper's post hoc alternative rule (Section 2.4, Supplementary Table S5; paper's export) | 62.7% | 88.2% | PMC13513162 text |
| this predictor (TEST clusters) | 91.97% (95% cluster CI 86.91%-95.42%) | 97.68% | object/ |

Confusion matrices on 1422 TEST comparisons (1045 clusters): model TP 189 FP 7 TN 1200 FN 26;
rule TP 176 FP 395 TN 812 FN 39.

## All eight antibiotics we attempted
One pre-registered job trained and scored all eight antibiotics on the same cluster split (TEST results below, nothing else was run on
TEST before the claims were chosen). Five meet every pre-registered threshold and are claimed, one package each; three are not.

| antibiotic | TEST comparisons | model F1 (95% cluster CI) | model accuracy | rule F1, same rows | published F1 / accuracy | paired F1 difference, 95% CI (points) | status |
|---|---|---|---|---|---|---|---|
| ciprofloxacin | 1693 | 96.13% (93.65%-97.84%) | 98.35% | 80.36% | 77.2% / 89.9% | 11.09 to 21.88 | claimed (one package each) |
| ampicillin | 1715 | 98.80% (98.25%-99.28%) | 98.78% | 94.40% | 93.9% / 94.5% | 3.06 to 5.88 | claimed (one package each) |
| gentamicin | 1623 | 96.28% (93.68%-98.00%) | 98.64% | 92.41% | 92.4% / 97.6% | 1.81 to 6.95 | claimed (one package each) |
| tetracycline | 1545 | 98.19% (97.47%-98.85%) | 98.38% | 98.26% | 98.1% / 98.4% | -0.41 to 0.22 | not claimed |
| trimethoprim-sulfamethoxazole | 1588 | 94.51% (92.31%-96.47%) | 97.61% | 94.29% | 94.2% / 97.9% | -0.84 to 1.32 | not claimed |
| ceftriaxone | 1531 | 97.66% (96.32%-98.69%) | 98.76% | 94.51% | 94.6% / 97.9% | 1.21 to 5.44 | claimed (one package each) |
| amoxicillin-clavulanic acid | 1422 | 91.97% (86.91%-95.42%) | 97.68% | 44.78% | 44.5% / 73.6% | 39.72 to 54.60 | claimed (one package each) |
| meropenem | 1333 | 88.89% (75.00%-97.67%) | 99.70% | 78.95% | 81.2% / 99.6% | 0.00 to 23.49 | not claimed |

Tetracycline and trimethoprim-sulfamethoxazole: the model is within noise of the rule. Meropenem: only 18 resistant TEST isolates, and
the interval's lower end is below the published F1.

## Not claimed
- No clinical or treatment interpretation: this is a database-concordance benchmark for surveillance, not diagnostic validation.
- Not a claim about other antibiotics (one antibiotic per package) or about the paper's June export (a secondary run on the paper's own
  records gives a similar picture but is not this claim).
- Test-label history: TEST labels were read once by the pre-registered job, then by contrarian checks and pre-registered secondaries
  that did not change the model (details in how-we-built-it/).
- The published rule was reimplemented from its summaries and calibrated to reproduce the paper's per-comparison table exactly; for
  alleles absent from the paper's data the regexes are our reading of the summaries.

## Credits
- Abdullateef Abdullah Alshehri, "Antibiotic-Specific Genotype-Phenotype Concordance and Cross-Database Interoperability in Public
  Escherichia coli/Shigella WGS-AMR Metadata", Int J Mol Sci 2026, 27:7157 (https://doi.org/10.3390/ijms27167157), rule and supplement.
- NCBI Pathogen Detection (https://www.ncbi.nlm.nih.gov/pathogens/) and AMRFinderPlus (M. Feldgarden et al.).
- T. J. Davies et al., Antimicrob Agents Chemother 2020 (PMC7269502), amoxicillin-clavulanate genotype prediction.
- LightGBM (G. Ke et al.), scikit-learn, pandas, numpy.
- Found by verexxi; code written with help from Claude (Anthropic).

## Who reviewed this
The "signed off" reviewers named above, and the CONFIRMED_SOLUTION status in panel/gate.md, are our own internal review panel: three separate reviewer runs that each saw only the claim folder, plus the submitter's own gate over their verdicts. They are not this repository's maintainers, and nothing here has been reviewed or endorsed by them.

## Review record
The reviewers' scope sentence exactly as signed off in panel/gate.md:

Path note: the quote below uses the claim-folder paths the panel reviewed. In this package, result/split.csv is how-we-built-it/split.csv and result/test_predictions_amoxicillin-clavulanic_acid.csv is object/test_predictions_amoxicillin-clavulanic_acid.csv.

> On the cluster-held-out TEST partition in result/split.csv (sha256 68a7e358...577dca) of NCBI export PDG000000004.6366 as the claimant describes it, the LightGBM model's predictions in result/test_predictions_amoxicillin-clavulanic_acid.csv score F1 91.97% and accuracy 97.68% (TP 189, FP 7, TN 1200, FN 26), against 44.78% and 69.48% for the code-reimplemented Table 3 genotype rule on the same 1422 rows and 44.5% and 73.6% published, with the model's cluster-bootstrap F1 interval lying above both baselines, for amoxicillin-clavulanic acid only and for database concordance only.
