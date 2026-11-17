# Null test: p2 leakage, ETH (PREREG.md, "p2 (leakage) and the null_test.md record")

Model: genome-wide 10-nearest-neighbour on the released CRyPTIC SNP distances (GPI_SNP_DISTANCES_VALUES.npy),
weights 1/(1+d), among isolates with a HIGH-filter R/S ETH phenotype. Metric: sensitivity at >= 95% specificity on
the test part. Real = the frozen cluster-aware split v2 (split/split.csv). Controls = 400 random isolate-level splits
with the same TEST size (3,073 of 12,287), numpy default_rng seeds 1..400. Per PREREG.md, "real beats all controls"
here means the cluster-aware value lies below every random-split value (leakage shown).
Output (repair round 1, integer form of the frozen <= 5% rule; attempts/leakage-knn-repair/REPAIR.md):
attempts/leakage-knn-repair/p2_knn_ETH_output.txt and attempts/leakage-knn-repair/p2_knn_ETH.csv. The round-1 run
(attempts/leakage-knn/) differed in one control only (seed 333: 0.584375 there, 0.5875 here); every line below is from the repaired run.

controls: 400
best_control: 0.5135 (lowest random-split sensitivity at 95% specificity; random mean 0.6003, max 0.6678)
real: 0.3496 (split v2; AP 0.4170 vs random AP 0.5965-0.7395)
real_beats_all_controls: yes
margin: mean(controls) - real = 0.2507; min(controls) - real = 0.1639
secondary: 100 alternative cluster-aware splits (same rule, other salts): sensitivity 0.1799-0.4662 (mean 0.3259), all below the lowest random split (0.5135)
command: python3 -I attempts/leakage-knn-repair/code/p2_knn.py <GPI_SNP_DISTANCES_VALUES.npy> data/tables/GPI_SNP_DISTANCES_LABELS.npy . ETH 400 100 attempts/leakage-knn-repair/p2_knn_ETH.csv
