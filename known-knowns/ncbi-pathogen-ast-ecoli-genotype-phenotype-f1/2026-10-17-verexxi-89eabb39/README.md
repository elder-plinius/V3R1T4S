# E. coli/Shigella genotype-to-phenotype, ceftriaxone: F1 97.66% vs the published rule's 94.6%

## What
On the hash-defined test partition of NCBI Pathogen Detection export PDG000000004.6366 (1531 ceftriaxone comparisons in 1114 groups, of which 337 are PDS SNP clusters holding 754 rows and 777 are unclustered isolates treated as one-isolate groups), the LightGBM predictions saved in object/test_predictions_ceftriaxone.csv score F1 97.66% (95% cluster-bootstrap CI 96.32% to 98.69%) and accuracy 98.76% with TP 396, FP 10, TN 1116, FN 9, which is 3.06 points above the published 94.6% F1 (published accuracy 97.9%) and 3.15 points above the published genotype rule recomputed on the same rows (F1 94.51%, accuracy 97.19%, paired-difference CI 1.21 to 5.44 points), for ceftriaxone only, as a database-concordance result with no clinical interpretation, and with the margin over the 3-point bar only 0.06 points (one more test error would put it below the bar).

(File paths as in this package. The reviewers' sentence exactly as signed off in panel/gate.md is under Review record.)

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (Python 3 standard library only). It downloads the sha256-pinned NCBI export
(551 MB) and cluster list, recomputes eligibility, phenotypes, the cluster split and the published rule, scores object/test_predictions_ceftriaxone.csv, runs a
2,000-replicate cluster bootstrap and checks every threshold. Expected last line: `PASS`. About 1-3 minutes plus the download.
NCBI first served these files under latest_snps/ and moved them to the versioned folder PDG000000004.6366/ when it published a newer version (same files, same sha256).

## Compared to
| bar | F1 | accuracy | source |
|---|---|---|---|
| published genotype rule (paper, 2026-06-11 export) | 94.6% | 97.9% | Table 3, PMC13513162, fetched 2026-10-17T00:27:32Z |
| same rule recomputed on our TEST rows | 94.51% | 97.19% | verify-it-yourself |
| this predictor (TEST clusters) | 97.66% (95% cluster CI 96.32%-98.69%) | 98.76% | object/ |

Confusion matrices on 1531 TEST comparisons (1114 clusters): model TP 396 FP 10 TN 1116 FN 9;
rule TP 370 FP 8 TN 1118 FN 35.

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
- LightGBM (G. Ke et al.), scikit-learn, pandas, numpy.
- Found by verexxi; code written with help from Claude (Anthropic).

## Review record
The reviewers' scope sentence exactly as signed off in panel/gate.md:

Path note: the quote below uses the claim-folder paths the panel reviewed. In this package, result/test_predictions_ceftriaxone.csv is object/test_predictions_ceftriaxone.csv.

> On the hash-defined test partition of NCBI Pathogen Detection export PDG000000004.6366 (1531 ceftriaxone comparisons in 1114 groups, of which 337 are PDS SNP clusters holding 754 rows and 777 are unclustered isolates treated as one-isolate groups), the LightGBM predictions saved in result/test_predictions_ceftriaxone.csv score F1 97.66% (95% cluster-bootstrap CI 96.32% to 98.69%) and accuracy 98.76% with TP 396, FP 10, TN 1116, FN 9, which is 3.06 points above the published 94.6% F1 (published accuracy 97.9%) and 3.15 points above the published genotype rule recomputed on the same rows (F1 94.51%, accuracy 97.19%, paired-difference CI 1.21 to 5.44 points), for ceftriaxone only, as a database-concordance result with no clinical interpretation, and with the margin over the 3-point bar only 0.06 points (one more test error would put it below the bar).
