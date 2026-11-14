# Null Model & 400-Permutation Control Report (`jarvis-small-data-exfoliation-tc-mae`)

controls: 400
best_control: 53.342778 meV/atom on dft_3d_exfoliation_energy (null mean 62.359896 +/- 4.092869 meV/atom, z = -8.35); 0.454085 eV on tinnet_N_ead (null mean 0.675969 +/- 0.081043 eV, z = -7.49)
real: 28.195924 meV/atom on dft_3d_exfoliation_energy (-31.04% vs 40.887 meV/atom, h90 = 11.132579 meV/atom); 0.068908 eV on tinnet_N_ead (-20.89% vs 0.0871 eV, h90 = 0.017247 eV, uncredited supplementary)
command: python3 -B verify-it-yourself/check_jarvis_clss_package.py
real_beats_all_controls: yes

## Summary of 400 Training-Label Permutation Controls & Dummy Predictors

Across both NIST JARVIS-Leaderboard benchmarks (`dft_3d_exfoliation_energy` and uncredited supplementary `tinnet_N_ead`), `400` independent random permutations of the training labels `y_tv` (`np.random.default_rng(0)`) were evaluated through the exact same kernel pipeline (`how-we-built-it/train_and_predict_jarvis_clss.py`, verified by `verify-it-yourself/check_jarvis_clss_package.py`):

| Benchmark | Frozen CLSS Test MAE (`real`) | 400-Permutation Null Mean $\pm$ SD | Best Control (`min` across 400 permutations) | $z$-Score | Controls Reaching `real` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`dft_3d_exfoliation_energy`** (meV/atom, claimed primary) | **`28.195924`** | `62.359896 +/- 4.092869` | `53.342778` | `-8.35` | `0 / 400` (`p = 0.00249`) |
| **`tinnet_N_ead`** (eV, uncredited supplementary; `p1` dropped) | **`0.068908`** | `0.675969 +/- 0.081043` | `0.454085` | `-7.49` | `0 / 400` (`p = 0.00249`) |
