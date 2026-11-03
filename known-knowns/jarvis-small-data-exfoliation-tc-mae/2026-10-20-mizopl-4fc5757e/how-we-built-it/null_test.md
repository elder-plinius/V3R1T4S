# Null Model & 400-Permutation Control Report (`jarvis-small-data-exfoliation-tc-mae`)

controls: 400
best_control: 53.342778 meV/atom on dft_3d_exfoliation_energy (null mean 62.359896 +/- 4.092869 meV/atom, z = -8.35); 0.454085 eV on tinnet_N_ead (null mean 0.675969 +/- 0.081043 eV, z = -7.49)
real: 28.195924 meV/atom on dft_3d_exfoliation_energy (-31.04% vs 40.887 meV/atom, h90 = 11.132579 meV/atom); 0.068908 eV on tinnet_N_ead (-20.89% vs 0.0871 eV, h90 = 0.017247 eV)
command: python3 -B verify-it-yourself/check_jarvis_clss_package.py
real_beats_all_controls: yes
