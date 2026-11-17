# How we found it (contributor text, unverified)

The brief: the bank's partial win p1 asks for a beat of the reference tool by >= 10% in MRR on cases with <= 3 HPO
terms. An earlier run had evaluated a frozen classic ranker (asymmetric Resnik best-match average, from an earlier
leakage audit) against LIRICAL 2.4.1 on all 10,189 included cases, with both tools given the same HPOA from which every
row citing a corpus publication was removed. That full comparison was judged not new against a published table.

What we did: before computing any p1 statistic we froze the subset (the earlier run's definition: distinct observed
HPO terms mapped under Phenotypic abnormality), the gate (point ratio >= 1.10, paired case-bootstrap interval of the
difference above 0, 400-control label-swap null) and the sensitivity checks, and searched the literature for a
published few-terms split of the same comparison (none found). We then computed p1 from the existing per-case rows,
re-derived the subset with an independent parser, and tried to break the result (other term counts, single
publications, clusters). A three-skeptic panel reviewed it.

What failed or is weak: 1-term cases and the observed-plus-excluded count show no win; the gain is concentrated in a
few large cohorts.
