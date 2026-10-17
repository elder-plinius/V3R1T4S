# How we found it (contributor text, unverified)
First reproduced the paper exactly: eligibility, phenotype parsing and the genotype rule match its supplementary tables row for row.
Then one gradient-boosted model per antibiotic over the same exported annotations (gene and point-mutation calls with their status, a few
counts, the rule outputs, year, species and isolation type), trained on whole SNP clusters with the threshold chosen by grouped
cross-validation inside training. All eight antibiotics went through the same pre-registered job; README lists every TEST result.

For ceftriaxone: The rule misses resistant isolates: on TEST it has 35 false negatives against the model's 9. Beyond the rule's own call, the model uses the number of acquired beta-lactamases and partial blaCMY hits.
Top features by gain in the released model: the published rule's own call for ceftriaxone (79.0%); the number of acquired beta-lactamase genes (5.7%); blaCMY (partial hit) (5.5%); collection year (2.3%); the total number of AMR calls (1.2%); blaTEM-1 (1.0%).
