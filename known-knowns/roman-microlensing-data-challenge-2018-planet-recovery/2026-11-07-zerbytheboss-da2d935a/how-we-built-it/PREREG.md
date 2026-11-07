# Pre-Registration & Protocol Lock

- **Target ID**: `roman-microlensing-data-challenge-2018-planet-recovery` (`planetary-science`)
- **Zero-Leakage Unsupervised Invariant**: `how-we-built-it/solve_roman_dc18.py` and `how-we-built-it/binary_lens_kernel.c` operate strictly on the two-band light curves (`W149` and `Z087`) and never read `master_file.txt`, `Answers/`, or team entries during classification or `(s, q)` parameter estimation.
- **Single Frozen Pipeline**: Every event `1..293` is processed through the exact same three-stage physical cascade (`CV` achromaticity/outburst test -> unregularized `PSPL+FSPL+parallax` residual test -> 4-regime physical binary-lens `(s, q)` solver).
