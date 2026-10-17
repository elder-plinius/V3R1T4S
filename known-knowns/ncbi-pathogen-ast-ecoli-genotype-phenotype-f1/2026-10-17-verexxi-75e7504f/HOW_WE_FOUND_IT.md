# How we found it (contributor text, unverified)
First reproduced the paper exactly: eligibility, phenotype parsing and the genotype rule match its supplementary tables row for row.
Then one gradient-boosted model per antibiotic over the same exported annotations (gene and point-mutation calls with their status, a few
counts, the rule outputs, year, species and isolation type), trained on whole SNP clusters with the threshold chosen by grouped
cross-validation inside training. All eight antibiotics went through the same pre-registered job; README lists every TEST result.

For gentamicin: The rule is already close for gentamicin; the gain is mostly fewer false positives (28 for the rule against 9 for the model). Beyond the rule's own call, the model's main inputs are aac(3) variants and sul1.
Top features by gain in the released model: the published rule's own call for gentamicin (69.2%); aac(3)-IId (4.2%); sul1 (3.7%); aac(3)-IIe (3.5%); aac(3)-VIa (3.2%); the total number of AMR calls (3.0%).
