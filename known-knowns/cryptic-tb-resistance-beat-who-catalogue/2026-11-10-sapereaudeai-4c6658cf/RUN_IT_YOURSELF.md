# Run it yourself (from this folder, fresh shell)

1. Quick check (standard library only, a few seconds):

       sh verify-it-yourself/run_checks.sh

   Expected last line: `PASS` (the real output is in verify-it-yourself/RECEIPTS.md).

2. Full recompute of the 10-NN values (numpy; about 10 s on the run machine, memory-mapped, row blocks). Download the public inputs:
   - https://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/reproducibility/data_tables/cryptic-analysis-group/GPI_SNP_DISTANCES_VALUES.npy
     (463,784,096 bytes, sha256 02d7cd4602a0bc900448f0fb290cf958a3b2c834f0bd878ca880af91eedef5dd)
   - GPI_SNP_DISTANCES_LABELS.npy from the same folder (sha256 611512d71d066bb71ff1dd289950b63abf5538af94654884d9c8b8c0dce25e61)
   - https://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/reuse/CRyPTIC_reuse_table_20240917.csv
     (5,393,811 bytes, sha256 f785ae87f2bfb7f39f08d2ca2618a1925a290c39bfdfd5a535995b1827541c1b)

   Then:

       CRYPTIC_GPI_DISTANCES=GPI_SNP_DISTANCES_VALUES.npy CRYPTIC_GPI_LABELS=GPI_SNP_DISTANCES_LABELS.npy \
       CRYPTIC_REUSE_TABLE=CRyPTIC_reuse_table_20240917.csv python3 verify-it-yourself/check_p2.py

   Expected: `ok   full recompute, split v2: 0.349624 vs 0.349624` and the same for random seeds 1-3, then `PASS`.

3. Rebuild the objects (numpy, pandas, scikit-learn as in how-we-built-it/requirements.txt). Make a run folder
   holding data/CRyPTIC_reuse_table_20240917.csv and data/tables/GPI_SNP_DISTANCES_LABELS.npy, then from it:

       python3 -I code/make_split_v2.py VALUES.npy data/tables/GPI_SNP_DISTANCES_LABELS.npy data/CRyPTIC_reuse_table_20240917.csv split/split.csv
       python3 -I code/p2_knn.py VALUES.npy data/tables/GPI_SNP_DISTANCES_LABELS.npy . ETH 400 100 p2_knn_ETH.csv
       python3 -I code/export_p2_artifacts.py VALUES.npy data/tables/GPI_SNP_DISTANCES_LABELS.npy . result/

   (code/ = how-we-built-it/code/). split/split.csv must have sha256 3b4ed122...0a56, p2_knn_ETH.csv must equal
   object/p2_knn_ETH_metrics.csv (about 4 minutes). The run's logs are in how-we-built-it/logs/.
