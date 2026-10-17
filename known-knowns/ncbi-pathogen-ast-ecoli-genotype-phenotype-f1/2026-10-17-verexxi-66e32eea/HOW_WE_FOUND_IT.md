# How we found it (contributor text, unverified)
First reproduced the paper exactly: eligibility, phenotype parsing and the genotype rule match its supplementary tables row for row.
The rule calls resistance whenever a mapped determinant is present; for beta-lactam/inhibitor and fluoroquinolone phenotypes that
over-calls (TEM-1 alone, single QRDR mutations). A gradient-boosted model over the same exported annotations (gene and point-mutation
calls with their status, a few counts, the rule outputs, year, species and isolation type), trained on whole SNP clusters with the
threshold chosen by grouped cross-validation inside training, learns which determinants matter (for amoxicillin-clavulanic acid:
blaCMY-2, ampC promoter mutations, blaOXA-1). A random split gives almost the same numbers, as does the paper's own June snapshot.
