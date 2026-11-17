# Leakage audit of LIRICAL on phenopacket-store 0.1.27 (bank target phenopacket-store-rare-disease-gene-prioritization, partial win p3)

## What
With LIRICAL 2.4.1 in phenotype-only mode (pinned data, HPO ontology v2026-06-06 held fixed), on a seeded random sample of 500 of the 4,247 run-1-included phenopacket-store 0.1.27 cases (211 PMIDs) for which an HPO release predates the case's earliest PubMed date, replacing the contemporary HPOA v2026-06-06 by the last HPOA release published before each case's paper (ids mapped to the v2026-06-06 ontology) lowers the MRR of gene ranks over 19,274 protein-coding genes (derived from LIRICAL's disease post-test probabilities via mim2gene_medgen) from 0.5567 to 0.0798 (paired drop 0.4769, 95% bootstrap over cases [0.4325, 0.5181], over publications [0.3422, 0.6230]; 85.7% of the contemporary MRR) and top-1 recall from 0.5005 to 0.0490 (drop 0.4515, cases [0.4050, 0.4965], publications [0.3297, 0.5864]), a drop that beats all 400 paired label-swap controls (best 0.1063) and that measures the effect of all HPOA annotations added after each case's pre-publication release, not of the case's own publication alone.

These are retrospective ranking statistics on published case reports. They are not clinical advice, and they say
nothing about LIRICAL's performance on a real patient.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: `PASS`. Laptop time: a few seconds, Python 3 standard library only (set PYTHON if python3 is not
on PATH). To rebuild the object from the corpus with LIRICAL itself, see RUN_IT_YOURSELF.md (about 35 minutes of JVM
time).

## Compared to
| what | value | source | fetched (UTC) |
|---|---|---|---|
| status source (corpus release pinned) | 0.1.27, all_phenopackets.zip sha256 d0c70005...205a | https://github.com/monarch-initiative/phenopacket-store/releases | 2026-11-11T10:34:08Z |
| p3 is an audit, so no table value is beaten | the comparison is within the tool: the same 500 cases under HPOA v2026-06-06 vs the last HPOA release before each paper | object/summary.json | - |
| related design, not the same quantity | LIRICAL 2.4.1, exact leave-one-publication-out on one contemporary HPOA, Recall@1 0.4868 -> 0.1724 on 2,227 cases (the cleaner own-publication audit) | https://arxiv.org/abs/2609.02473 | read 2026-11-11 |
| related, reported by the panel (panel/novelty.md), not opened by the run | dataset-level scores of an LR model against annual HPO snapshots; overlap flag against HPOA v2026-02-16 without tool numbers | https://arxiv.org/abs/2610.33592 ; https://www.biorxiv.org/content/10.64898/2026.08.30.748028v1 | 2026-11-11 |

## Not claimed
- Nothing about all 10,189 cases or all 4,247 cases with a pre-publication release. Only the seeded 500-case sample was run.
- No split of the drop into own-paper and other later curation. The pre-publication release lacks ALL annotations
  added after it, and the bank names this design as its example. For 299 of the 500 cases the disease had no
  annotation at all before the paper (how-we-built-it/logs/decomposition.json).
- No Exomiser result; no claim on the main criterion, p1 or p2.
- The date-permutation placebo of the earlier run (N2) was not run with LIRICAL. The null reported is a paired
  label-swap with 400 controls.
- Term ids of older HPOA releases were mapped onto the v2026-06-06 ontology, and 4 malformed frequency cells were
  blanked (how-we-built-it/PREREG.v2.md, v4). A run with release-specific ontologies was not done.

## Credits
- phenopacket-store (Danis et al., Monarch Initiative): https://github.com/monarch-initiative/phenopacket-store
- Human Phenotype Ontology and its disease annotations (HPO team, Jackson Laboratory and Monarch):
  https://hpo.jax.org/ and https://github.com/obophenotype/human-phenotype-ontology
- LIRICAL (Robinson et al., Am J Hum Genet 2020; The Jackson Laboratory): https://github.com/TheJacksonLaboratory/LIRICAL
- Jannovar transcript data (Zenodo record 5410367): https://zenodo.org/records/5410367
- HGNC gene nomenclature: https://www.genenames.org/ ; NCBI mim2gene_medgen: https://ftp.ncbi.nlm.nih.gov/gene/DATA/
- OMIM disease identifiers: https://www.omim.org/ ; PubMed E-utilities for publication dates: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- The leave-one-publication-out LIRICAL audit this complements: arXiv 2609.02473, https://arxiv.org/abs/2609.02473 ; related leakage work found by the panel: arXiv 2610.33592 and bioRxiv 10.64898/2026.08.30.748028.
- This is not the first leakage audit of LIRICAL on this corpus; it is, as far as the panel found, the first with per-case pre-publication HPOA releases.
- Phenomizer (Koehler et al., Am J Hum Genet 2009), the method behind the earlier run's context baseline.
