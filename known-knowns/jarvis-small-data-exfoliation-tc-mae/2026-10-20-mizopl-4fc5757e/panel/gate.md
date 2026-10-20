# Skeptic Panel Gate (`jarvis-small-data-exfoliation-tc-mae`)

status: CONFIRMED_SOLUTION
target: jarvis-small-data-exfoliation-tc-mae
reproduce_pass: true
novelty_pass: true
criterion_pass: true
confirmed_scope: Structure-only physics-informed CLSS kernel models trained strictly on official train U val IDs with zero label leakage (claim/trained_models_jarvis_clss.npz, sha256 4fc5757ef96c86ab1361ac488a5ee376e5aeea57b29c03afa5befa1b54b21489) achieve official test MAE = 0.902806 K on dft_3d_Tc_supercon (claim/AI-SinglePropertyPrediction-Tc_supercon-dft_3d-test-mae.csv, -40.55% below live best atomgpt_model 1.5187 K and -54.83% below cfid 1.9989 K, gain +0.615894 K exceeding 1,000-sample bootstrap 90% CI half-width h90 = 0.367962 K), test MAE = 28.195924 meV/atom on dft_3d_exfoliation_energy (claim/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv, -31.04% below live best matminer_xgboost 40.887 meV/atom, gain +12.691076 meV/atom exceeding h90 = 11.132579 meV/atom), and test MAE = 0.068908 eV on the preregistered p1 task tinnet_N_ead (N = 327 materials, claim/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv, -20.89% below live best alignn 0.0871 eV, gain +0.018192 eV exceeding h90 = 0.017247 eV), together with 5-fold cross-validation paired superiority over reproduced matminer_xgboost on train U val across all three benchmarks (Wilcoxon p = 5.99e-09, 1.62e-18, and 5.86e-15, p2).
