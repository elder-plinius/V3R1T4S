# Few-terms head-to-head on phenopacket-store 0.1.27: a frozen Resnik ranker vs LIRICAL 2.4.1 on cleaned annotations (bank target phenopacket-store-rare-disease-gene-prioritization, partial win p1)

## What
On the 2,038 of the 10,189 included phenopacket-store 0.1.27 cases with at most 3 distinct observed (non-excluded) HPO terms (hp.obo v2026-06-06, under HP:0000118), with both tools using the same HPOA v2026-06-06 cleaned of every row citing a corpus PMID (sha256 5e1a2fcf77d3ddf7d5d00f54ce8975ecabff3277749359f1e0636a8c6a7caa14) and the same 19,274-gene protein-coding candidate space, the frozen asymmetric-Resnik ranker reaches gene-level MRR 0.1384 against 0.1047 for LIRICAL 2.4.1 phenotype-only on the unmodified phenopackets (ratio 1.32, paired case-bootstrap 95% intervals [0.0257, 0.0420] for the difference and [1.239, 1.420] for the ratio, real difference above all 400 paired label-swap controls), a margin that does not survive counting excluded terms (493 cases, ratio 0.98) and whose publication-cluster ratio interval [1.024, 1.672] does not exclude ratios below 1.10.

These are retrospective ranking statistics on published case reports. They are not clinical advice, and they say
nothing about either tool's performance on a real patient.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: `PASS`. Laptop time: about 10 seconds, Python 3 standard library only (set PYTHON if python3 is
not on PATH). To rebuild the per-case rows from the corpus with both tools, see RUN_IT_YOURSELF.md (about 4 hours of
LIRICAL JVM time for all cases).

## Compared to
| what | value | source | fetched (UTC) |
|---|---|---|---|
| status source (corpus release pinned) | 0.1.27, all_phenopackets.zip sha256 d0c70005...205a | https://github.com/monarch-initiative/phenopacket-store/releases | 2026-11-11T19:03:25Z |
| the reference tool, run by us on the same cases, data and candidate space | LIRICAL 2.4.1 gene-level MRR 0.1047 on the 2,038 cases with <= 3 observed HPO terms | object/p1_summary.json | - |
| closest published comparison (not split by term count) | Resnik vs LIRICAL 2.4.1 on 0.1.27, leave-one-publication-out for both, Recall@1 0.2591 vs 0.1724 (disease level, 2,227 test cases) | arXiv 2609.02473 Table 1, https://arxiv.org/abs/2609.02473 | read 2026-11-11 |

## Not claimed
- Nothing about the full success criterion. On all 10,189 cases the same comparison (MRR 0.1091 vs 0.0870) was judged
  not new against arXiv 2609.02473 Table 1 and the bank's published-bar clause; it is not part of this package.
- No new ranking method: the ranker is the classic asymmetric Resnik best-match average (Phenomizer's similarity),
  frozen before any evaluation.
- Not robust to every term count: on 1-term cases (520) LIRICAL is level or ahead (ratio 0.9167 [0.8037, 1.0523]);
  counting excluded terms too (493 cases with <= 3 observed + excluded terms) gives ratio 0.9816 [0.8742, 1.1141]
  (how-we-built-it/logs/audit.out). The subset counts observed terms only, as fixed before the p1 statistics.
- The gain is concentrated: NF1 cohorts (277 subset cases) carry about 41% of the summed per-case difference, and
  the publication-cluster interval of the ratio is [1.0236, 1.6718] (its lower end is below 1.10; the difference
  interval [0.0021, 0.0659] stays above 0).
- Both tools use the same HPOA v2026-06-06 with every row citing a corpus PMID removed; rows citing only OMIM, Orphanet
  or DECIPHER, and the gene-disease maps, are kept for both. Unmodified LIRICAL with the original HPOA is a different
  (leakier) comparison and is not claimed against.
- Point values of this subset were seen descriptively in the earlier full evaluation before the p1 rules were frozen
  (declared in how-we-built-it/PREREG.md); the intervals, null and sensitivity results were not.

## Credits
- phenopacket-store (Monarch Initiative): https://github.com/monarch-initiative/phenopacket-store
- Human Phenotype Ontology and its disease annotations (HPO team, The Jackson Laboratory and Monarch Initiative):
  https://hpo.jax.org/ and https://github.com/obophenotype/human-phenotype-ontology
- LIRICAL (The Jackson Laboratory; Am J Hum Genet 2020): https://github.com/TheJacksonLaboratory/LIRICAL
- The Phenomizer similarity score (Am J Hum Genet 2009), the method frozen here.
- HGNC gene nomenclature: https://www.genenames.org/ ; NCBI mim2gene_medgen: https://ftp.ncbi.nlm.nih.gov/gene/DATA/ ;
  OMIM identifiers: https://www.omim.org/
- The published Resnik vs LIRICAL comparison under leave-one-publication-out on this release: arXiv 2609.02473,
  https://arxiv.org/abs/2609.02473
- Authors are cited by organisation and paper identifier only in this package.
