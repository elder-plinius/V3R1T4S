# How we built it

- search/: the GPU engine thomson_bb.cu, the chain scripts and the full chain log of run 2026-10-21-2021.
- certify/: the judge certify.py (30-digit mpmath energy, tangent Newton, Hessian), verify_stdlib.py and the
  negative-control generator perturb.py.
- expected/: the judge's outputs on the object and on the two posted configurations (run 2026-10-22-0154).
- PREREG.md (run 2026-10-21-2021, written before the search) and PREREG.v2.md (run 2026-10-22-0154, written before the
  re-panel). null_test: not needed (an explicit object judged by a deterministic checker).
Requirements: Python 3.8+, numpy, scipy, mpmath (gmpy2 optional); CUDA 12+ for the search only.
