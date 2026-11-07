# Pre-Registration & Protocol Lock

- **Target ID**: `cami2-genome-binning-recovered-genomes` (`genomics`)
- **Zero-Leakage Unsupervised Invariant**: `how-we-built-it/solve_cami2_unsupervised.py` takes only the public candidate `.binning` files and intrinsic contig lengths `seq_len[sid]`. It never reads ground-truth `BINID` or `TAXID` mappings during lineage clustering, circular replicon extraction, fringe trimming, or bin selection.
- **Single Frozen Algorithm Across All 3 Datasets**: The exact same function `run_refined_unsupervised_cami2(binners, seq_len)` with identical thresholds is applied unchanged to `strain-madness` (`p1`), `plant-associated` (`p2`), and `marine` (`p3`).
- **Exact AMBER Evaluation**: High-quality genome recovery (`recall_bp = tp_length_bp / gs_length_bp > 0.90` and `precision_bp = tp_length_bp / total_length_bp > 0.95`) and base-pair Adjusted Rand Index (`ARI (bp)`) follow `CAMI-challenge/AMBER` and `second_challenge_evaluation/binning/genome_binning/scripts/recovered_g.py`.
