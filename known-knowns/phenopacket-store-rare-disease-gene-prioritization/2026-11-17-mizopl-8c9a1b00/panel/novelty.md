# Skeptic 2 — Frontier, Strict `< 2026-06-09` Provenance & Anti-Leakage Audit (`novelty.md`)

- `context`: `fresh independent skeptic review of external literature, release dates, and leakage traps`
- `target_id`: `phenopacket-store-rare-disease-gene-prioritization`
- `corpus_release`: `monarch-initiative/phenopacket-store 0.1.27 (2026-06-09)`

## Audit Findings

1. **100% Strict `< 2026-06-09` Pre-Corpus Timestamps:** Every ontology, gene-disease mapping, and network resource predates `phenopacket-store 0.1.27` (`2026-06-09`, `sha256: d0c70005bb09b87035087516252b6b539fbc0415be7c664b73c9cde7eedf205a`): `HPO/HPOA v2026-06-06` (`2026-06-08`, including `genes_to_disease.txt` `sha256: 81e8d2e0bc1c1052c383614ad85388325deeacb4b9478c6d9585597f45602bac` as the sole source of `7,653` OMIM and `8,288` Orphanet links — zero unversioned `mim2gene_medgen` or post-cutoff `en_product6.xml`), `HGNC` `2026-05-01` monthly snapshot (`sha256: 8a56d4af702d74364813fc764a96034a349a36e011fb54b3952ab53ae043dd8e`, verified `max date_modified == 2026-05-01`), `Monarch KG` (`2026-05-09`, `sha256: 85143b5e5e9380d2e5c37bb561a0890269d5b8f9627bb58417f7d46fa83263e4`), `Upheno v2025-10-12` (`2025-10-12`, `sha256: f7a41cd8557e147add80628593d0441c1278e83ab37d66063359f5eb0c5b82e1`), `Gene Ontology` (`2026-05-19`, `sha256: db472faff1785878521693af62646546cea6af4a386609dd01c72c0554a46a30`), and `STRING v12.0` (`2023; archive Last-Modified <= 2023-08-28`, `sha256: 28a2ea3b22c964e691c0f2f934c5e3e397a4b0a12c833d8787fa02b7847b91b6`).
2. **Zero Case-Report or Text-Mining Leakage:** All `1,755` unique corpus PMIDs extracted from `all_phenopackets_0.1.27.zip` (`PMID[:]? NNNN`) are purged from neighbor `HPOA`, `Monarch KG` non-human `has_phenotype`, and `GOA`; `Monarch KG` `infores:phenopacket-store` and `NCBITaxon:9606` phenotype edges are excluded; and `STRING v12.0` `textmining` is verified identically `0` across all `1,525,039` retained undirected edges (`s_notm >= 0.15`; `2,234,048` text-mining-only links dropped).
3. **Orthogonality to Existing Claims & Literature:** `arXiv:2609.02473` (September 2026) and open `V3R1T4S` PRs `#1058` (`p3`), `#1064` (`p1`), and `#1068` (`targets.json` note) do not evaluate Milestone `p2` unannotated causal gene discovery.

pass: true
