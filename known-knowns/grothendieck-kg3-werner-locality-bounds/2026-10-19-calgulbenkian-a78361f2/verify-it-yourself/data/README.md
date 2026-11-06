# Data files made by the builder

- `dual_certificates.txt`: 18454 lines, one for each dominant vector c (8 integers), followed by 8 integers M and one integer q. mu is given by m_k = M_k / q (see `../UPPER_BOUND.md`). The lines were produced with floating-point linear programs (`../optional/e8_gen_dual.py`, numpy and scipy) and are re-checked in exact integer arithmetic by `../e8_check.py`.
- `lower_bound_witness.txt`: 120 lines, the 8 simple-root coordinates of a positive root and the sign b for it. Produced by integer programming (`../optional/e8_gen_witness.py`, pulp with CBC); `../e8_check.py` evaluates ||A b||_1 directly on the matrix of the MATLAB file.
