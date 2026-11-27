# Commands (Python 3 with mpmath 1.3.0, numpy 2.0.2, scipy 1.13.1)
python3 check_bound.py   # u*, closed-form bound, E(sigma) at 8 sigma values, known-case tests -> check_bound_output.txt
python3 eval3d.py        # 3D Cartesian integration of Eq. (3) vs 1D quadrature; least |E| over sigma -> eval3d_output.txt
PREREG.md is the run's pre-registration, frozen 2026-11-25T19:11:58Z before any energy was computed
(null_test: not needed, deterministic bound).
