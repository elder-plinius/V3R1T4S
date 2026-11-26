# Skeptic 3 — Milestone `p2` Criterion, Candidate Symmetry & Bootstrap Audit (`criterion.md`)

- `context`: `fresh independent skeptic verification of p2 rules, candidate space, and statistical intervals`
- `target_id`: `phenopacket-store-rare-disease-gene-prioritization`
- `milestone_checked`: `p2 (>= 50 unannotated causal gene cases, fixed candidate space, full ranked lists)`

## Audit Findings

1. **Fixed `19,296`-Gene Candidate Space & Candidate Symmetry:** Both `LIRICAL 2.4.1` and `MARG-P2` are scored identically over all `19,296` HGNC protein-coding genes (`object/candidate_genes_19296.tsv`, `sha256: 56254d6163b7ce356543f049a540d61dea69f72bbe38f5be0f7fb3bde03d70fe`) using exact mid-rank tie handling. `MARG-P2` applies zero target-gene HPOA-membership indicators or penalties (`Pos-40` leave-self-HPOA-out control reaches `MRR = 0.050084`, `Median Rank = 621.5`).
2. **Sample Size `>= 50` & Complete Label-Free Ranked Lists:** `P2-Raw` contains `127 >= 50` single-gene cases (`10` genes with zero HPO annotations even in untouched `HPOA v2026-06-06`), with complete `127 x 19,296` ranked lists archived across `object/p2_raw_full_rankings_part01.tsv.gz`..`part11.tsv.gz` (every file `< 560 KB`, zero `y_true` columns). `P2-Holdout` provides `988` additional blind cases across `112` independent corpus-only genes.
3. **All-Three-CI Dominance & Limitations Honesty:** `MARG-P2` exceeds `LIRICAL 2.4.1` outside all three `95%` bootstrap CIs (`case`, `gene_cluster`, and `pub_cluster`) on both `P2-Raw` (`MRR = 0.001089` vs `0.000083`) and `P2-Holdout` (`MRR = 0.008803` vs `0.000089`), and the inclusive `6/6` equal-weight baseline (`u6`) also clears `LIRICAL 2.4.1` outside all `95%` CIs (`P2-Raw` `0.001057`, `P2-Holdout` `0.008274`). `Top-1 = 0/127` on `P2-Raw` and `Top-1 = 5/988` (`0.0051`) on `P2-Holdout` are stated upfront under `## Not claimed`.

pass: true
