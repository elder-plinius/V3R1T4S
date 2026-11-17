# Skeptic 1 — Reproducibility, Live Upstream Join & Mutation Audit (`reproduce.md`)

- `context`: `fresh independent skeptic review initialized from clean package directory`
- `target_id`: `phenopacket-store-rare-disease-gene-prioritization`
- `command_checked`: `sh verify-it-yourself/run_checks.sh`
- `corrupt_checked`: `sh verify-it-yourself/run_checks.sh --corrupt`

## Audit Findings

1. **Zero Ground-Truth Labels or Third-Party Archives in `object/`:** `object/` holds only `00_p2_benchmark_certificate.json` (`sha256: 4bc37f92cb3bd7040e4d66807c4b4d95053f1a1d19caa04f53ae6dfce855da9e`), `marg_p2_ranker.py` (`sha256: 8c9a1b001a6de22406675281c04de5eb20f9c4bd1a4660f45536cb0b3de5176d`), `candidate_genes_19296.tsv` (`gene_idx\thgnc_id`, `sha256: 56254d6163b7ce356543f049a540d61dea69f72bbe38f5be0f7fb3bde03d70fe`), `p2_raw_full_rankings_part01..11.tsv.gz` (`case_index\tcase_sha256\tcase_id\tranked_19296_gidxs_csv`), and `p2_holdout_top100_predictions.tsv.gz` (`sha256: e795dd68d2d691ea4b3ccc6bf29ec0592fe0a24c157fbbf446b5ac14b7e15307`). `verify-it-yourself/verify.py` joins `case_sha256` directly against upstream `all_phenopackets_0.1.27.zip` (`sha256: d0c70005bb09b87035087516252b6b539fbc0415be7c664b73c9cde7eedf205a`) + `HPO v2026-06-06` and live-runs `MARGP2Ranker` across all `127` `P2-Raw` cases (`2,450,592` entries, `0` mismatches), all `988` `P2-Holdout` cases (`98,800` top-100 entries, `0` mismatches), and all `40` `Pos-40` cases.
2. **Invariance & Three-Control Separation Analysis:** `verify.py` checks `rank(Q) == rank(reversed(Q))`, `LIRICAL 2.4.1` (`jar sha256: 3cad929d98b6d56c4dd4046d999f5688c952a6abf3ee92093f7dd3f61481fe55`) blind-vs-raw parity (`max_diff = 0.0`), and all three negative controls: (a) analytical uniform `19,296` null (`MRR = 0.000541`, `Median = 9648.5`), (b) `P2-Holdout` shuffled-gene control (`MRR = 0.000991`, 95% case CI `[0.000436, 0.001750]`, disjoint from `MARG-P2` `[0.004710, 0.013741]`), and (c) within-`P2-Raw` shuffled-gene control (`case MRR = 0.000366`, 95% case CI `[0.000169, 0.000705]`, where permuting labels inside a cohort that is `68.5%` `U2AF2`/`MAPK8IP3`/`EZH1` neurodevelopmental presentations yields partially overlapping `case MRR` CIs while `macro-gene MRR` drops `22.1x` from `0.004329` to `0.000196` and median rank worsens from `8957.0` to `11021.0`).
3. **Semantic & Hash-Transparent Mutation Rejection:** Both `sh verify-it-yourself/run_checks.sh --corrupt` and single-digit/vector perturbations to `object/00_p2_benchmark_certificate.json` or any `.tsv.gz` ranking file exit `1` with final line `FAIL`.

pass: true
