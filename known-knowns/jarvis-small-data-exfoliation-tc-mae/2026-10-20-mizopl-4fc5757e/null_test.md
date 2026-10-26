# Null Model & 400-Permutation Control Report (`jarvis-small-data-exfoliation-tc-mae`)

controls: 400
best_control: 1.447097 K on dft_3d_Tc_supercon (null mean 2.050390 +/- 0.281586 K, z = -4.08); 53.342778 meV/atom on dft_3d_exfoliation_energy (null mean 62.359896 +/- 4.092869 meV/atom, z = -8.35); 0.454085 eV on tinnet_N_ead (null mean 0.675969 +/- 0.081043 eV, z = -7.49)
real: 0.902806 K on dft_3d_Tc_supercon (-40.55% vs 1.5187 K, h90 = 0.367962 K); 28.195924 meV/atom on dft_3d_exfoliation_energy (-31.04% vs 40.887 meV/atom, h90 = 11.132579 meV/atom); 0.068908 eV on tinnet_N_ead (-20.89% vs 0.0871 eV, h90 = 0.017247 eV)
command: python3 -B claim/author_checker_jarvis_clss.py
real_beats_all_controls: yes

## Summary of 400 Training-Label Permutation Controls & Dummy Predictors

Across all three NIST JARVIS-Leaderboard benchmarks (`dft_3d_Tc_supercon`, `dft_3d_exfoliation_energy`, and `tinnet_N_ead`), `400` independent random permutations of the training labels `y_tv` (`np.random.default_rng(0)`) were evaluated through the exact same kernel pipeline (`claim/train_and_predict_jarvis_clss.py`, verified by `claim/author_checker_jarvis_clss.py`):

| Benchmark | Claimed CLSS Test MAE (`real`) | 400-Permutation Null Mean $\pm$ SD | Best Control (`min` across 400 permutations) | $z$-Score | Controls Reaching `real` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`dft_3d_Tc_supercon`** (K) | **`0.902806`** | `2.050390 +/- 0.281586` | `1.447097` | `-4.08` | `0 / 400` (`p = 0.00249`) |
| **`dft_3d_exfoliation_energy`** (meV/atom) | **`28.195924`** | `62.359896 +/- 4.092869` | `53.342778` | `-8.35` | `0 / 400` (`p = 0.00249`) |
| **`tinnet_N_ead` (`p1`)** (eV) | **`0.068908`** | `0.675969 +/- 0.081043` | `0.454085` | `-7.49` | `0 / 400` (`p = 0.00249`) |
