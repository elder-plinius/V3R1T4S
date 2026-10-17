# How we found it (contributor text, unverified)
First reproduced the paper exactly: eligibility, phenotype parsing and the genotype rule match its supplementary tables row for row.
Then one gradient-boosted model per antibiotic over the same exported annotations (gene and point-mutation calls with their status, a few
counts, the rule outputs, year, species and isolation type), trained on whole SNP clusters with the threshold chosen by grouped
cross-validation inside training. All eight antibiotics went through the same pre-registered job; README lists every TEST result.

For amoxicillin-clavulanic acid: The rule calls resistance whenever a mapped beta-lactamase is present, which over-calls (for example TEM-1 alone): on TEST it has 395 false positives against the model's 7. The model's main inputs are blaCMY-2, the ceftriaxone rule call and ampC promoter mutations.
Top features by gain in the released model: blaCMY-2 (33.8%); the published rule's own call for ceftriaxone (18.5%); the number of acquired beta-lactamase genes (10.0%); ampC_T-32A (7.3%); blaCMY (partial hit) (7.1%); ampC_C-42T (5.6%).
