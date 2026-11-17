# The record compared against (p1)

p1 compares with the reference tool run by the claimant on the same cases, not with a published table value.

| item | value |
|---|---|
| status source | https://github.com/monarch-initiative/phenopacket-store/releases (read via https://api.github.com/repos/monarch-initiative/phenopacket-store/releases?per_page=5) |
| fetched (UTC) | 2026-11-11T19:03:25Z |
| HTTP status | 200 |
| sha256 of the saved API response (not included) | daeee02f505a61765be0ce16c7eb90b124ccf8c06c562cec3b700780a82040e1 |
| extracted cell | latest release 0.1.27 (published 2026-06-09T16:47:04Z), all_phenopackets.zip 19,431,098 bytes, sha256 d0c70005bb09b87035087516252b6b539fbc0415be7c664b73c9cde7eedf205a |
| reference value beaten | LIRICAL 2.4.1 (phenotype-only, same cleaned HPOA, same 19,274 genes) gene-level MRR 0.1047 on the 2,038 cases with <= 3 observed HPO terms (object/p1_summary.json) |
| published evaluations on 0.1.27 split by term count | none found before computing (how-we-built-it/PREREG.md, novelty section); the closest, arXiv 2609.02473 Table 1, compares Resnik and LIRICAL 2.4.1 on all 2,227 test cases at disease level under leave-one-publication-out, with no term-count split |
