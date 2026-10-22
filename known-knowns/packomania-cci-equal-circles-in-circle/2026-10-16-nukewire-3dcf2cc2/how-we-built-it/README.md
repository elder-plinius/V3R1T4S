# How we built it

- lens1_gap_sweep.py — the finding program (numpy only). Loads the live radius.txt (path
  ../../data/radius.txt relative to its run layout; place a copy next to it and adjust the one
  path constant, or run it from the original run folder). Quick pass: 12 windows per gap row;
  full grid for flagged rows: 601 orientations x 36 fractional offsets, spacing in closed form
  (scale invariance of the lattice window: s* = 2/(1 + 2 rho_N), r = 1/(1 + 2 rho_N), rho_N =
  N-th smallest norm of the unit-spacing offset lattice). Deterministic: no randomness, no
  seeds. Runtime ~110 s for the full 135-row sweep.
- verify_candidates.py — exact verification (numpy + scipy + mpmath): locates binding pairs and
  norms with a KD-tree in double precision, recomputes them at mpmath dps=50; also checks the
  posted configuration's integrity and the sorted-distance-multiset non-isometry. In the
  packaged claim the load-bearing number is the string-exact decimal-60 value produced by the
  claim's standalone checker (see ../verify-it-yourself/); this script's float64 input pass
  gives the same value to 1e-16.
- PREREG.md — the frozen pre-registration (criterion verbatim, statistic, thresholds, null-test
  exemption), written before any search output was scored.
- Pinned requirements: python 3.11; numpy 2.4.6; scipy 1.17.1; mpmath 1.4.1 (only for
  verify_candidates.py; the sweep itself needs numpy alone, and the packaged checker needs
  nothing beyond the standard library).
