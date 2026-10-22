# How We Built It (`polaris-moleculeace-activity-cliff-mse`)

All training and audit scripts used to produce the saved predictions in `object/` are included in this folder:

1. `how-we-built-it/run_clss_moleculeace.py`: Standalone, deterministic, single-threaded CPU (`OMP_NUM_THREADS=1`, `deterministic=True`) 3-stage CLSS training and prediction script across all 30 MoleculeACE benchmarks (`--dataset CHEMBL287_Ki` runs the primary headline benchmark in ~45 seconds on CPU).
2. `how-we-built-it/audit_inchikey_and_baselines.py`: Initial Lens 1 audit verifying `sha256` checksums, Polaris train/test split counts, stereo-stripped `InChIKey[:14]` disjointness, and exact reproduction of `SVM_ECFP`, `RF_ECFP`, `GBM_ECFP`, and `KNN_ECFP`.
3. `how-we-built-it/run_lens1_multiscale_ruzicka.py`: Lens 1 Multi-Scale Chiral + Achiral Generalized Tanimoto/Ruzicka Mercer kernel evaluation.
4. `how-we-built-it/run_lens2_clss_fast.py`: Lens 2 30-benchmark sweep script combining Stage 1 Multi-Scale LOO KRR + OOF ensemble, Stage 2 CLSS Directional MMP Substituent-Difference Seam Surgery, and Stage 3 Thermometer-BLAS Exact Ruzicka + `ErG` Pharmacophore + 215-Descriptor RankGauss LOO KRR.
