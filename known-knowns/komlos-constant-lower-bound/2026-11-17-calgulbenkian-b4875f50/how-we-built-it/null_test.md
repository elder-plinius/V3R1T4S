# Null Model Benchmark — Random Unit-Column Gaussian Matrices

controls: 1000
best_control: 0.920607
real: 2.059565086610
command: python3 verify-it-yourself/check_komlos_py.py object/komlos_15x15_p2.txt
real_beats_all_controls: yes

## Details
- **Null family:** `1000` independent $15 \times 15$ matrices with standard Gaussian entries $G_{ij} \sim \mathcal{N}(0, 1)$, each column normalized to unit Euclidean length on $S^{14}$, evaluated by exhaustive Gray-code enumeration over all $2^{14} = 16,384$ antipodal sign classes (plus `40` controls at $24 \times 24$ with mean `0.695069` and max `0.761420`).
- **15x15 null distribution:** mean `0.703720`, maximum (`best_control`) `0.920607`.
- **Claimed object (`real`):** `205956508661 / 100000000000 = 2.059565086610`, exceeding all 1,000 controls by more than `+1.1389` (empirical $p < 1 / 1001$).
