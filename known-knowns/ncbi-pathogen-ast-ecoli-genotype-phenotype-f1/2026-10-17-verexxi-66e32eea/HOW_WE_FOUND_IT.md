# How we found it (contributor text, unverified)
First reproduced the paper exactly: eligibility, phenotype parsing and the genotype rule match its supplementary tables row for row.
Then one gradient-boosted model per antibiotic over the same exported annotations (gene and point-mutation calls with their status, a few
counts, the rule outputs, year, species and isolation type), trained on whole SNP clusters with the threshold chosen by grouped
cross-validation inside training. All eight antibiotics went through the same pre-registered job; README lists every TEST result.

For ciprofloxacin: The rule calls ciprofloxacin resistance on any QRDR mutation or PMQR gene, which over-calls: on TEST it has 166 false positives against the model's 12. The model's main inputs are parC S80I, the rule's own call and the number of quinolone-target point mutations, so it separates isolates with several target mutations from those with one.
Top features by gain in the released model: parC_S80I (33.2%); the published rule's own call for ciprofloxacin (31.9%); collection year (7.3%); the number of quinolone-target point mutations (6.9%); gyrA_S83L (5.2%); qnrS1 (4.6%).
