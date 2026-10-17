# How we found it (contributor text, unverified)
First reproduced the paper exactly: eligibility, phenotype parsing and the genotype rule match its supplementary tables row for row.
Then one gradient-boosted model per antibiotic over the same exported annotations (gene and point-mutation calls with their status, a few
counts, the rule outputs, year, species and isolation type), trained on whole SNP clusters with the threshold chosen by grouped
cross-validation inside training. All eight antibiotics went through the same pre-registered job; README lists every TEST result.

For ampicillin: The rule misses resistant isolates: on TEST it has 88 false negatives against the model's 13. Most of the model's weight is on the number of acquired beta-lactamase genes.
Top features by gain in the released model: the number of acquired beta-lactamase genes (70.2%); the published rule's own call for ampicillin (6.9%); blaHER-3 (6.5%); ampC_C-42T (2.7%); blaCMY (partial hit) (2.5%); the published rule's own call for amoxicillin-clavulanic acid (2.3%).
