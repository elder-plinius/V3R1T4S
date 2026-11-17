# Baseline (step 3c)

This run audits the reference tool itself (LIRICAL 2.4.1); no score of ours is compared against it and no
improvement is claimed. So there is no published baseline to beat. What is recorded here:
- The reference tool is run by us: command in work/run_lirical_group.sh, data hashes in data/lirical_data_sha256.txt.
- Published context: arXiv 2609.02473 reports LIRICAL 2.4.1 on 0.1.27 with Recall@1 0.4868 (uncorrected) on its
  2,227 ranking-eligible cases. Different case set, different unit; not reproduced and not compared.
- Our condition-C numbers on the 500-case sample are in attempts/lirical-temporal/output/summary.json (copied into
  the report next to that context value).
