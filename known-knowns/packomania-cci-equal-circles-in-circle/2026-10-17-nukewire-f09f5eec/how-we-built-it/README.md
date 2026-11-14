# How we built it

- lens1_gap_sweep.py — the finding program (numpy only; deterministic, no randomness): quick
  12-window pass over all 135 gap rows, full 601-orientation x 36-offset grid on flagged rows,
  spacing in closed form (lattice-window scale invariance: s* = 2/(1 + 2 rho_N), r = 1/(1 +
  2 rho_N)). Found this cell (N=3307) and the sibling N=4141 in the same run. Adjust the
  radius.txt path constant or run it beside a fresh copy of the table.
- verify_N3307.py — exact verification (numpy + scipy + decimal): binding pairs/norms located
  with a KD-tree in double, recomputed at decimal 60 from the coordinate strings; posted-config
  integrity and sorted-distance-multiset non-isometry. Saved output: verify_output.txt.
- PREREG.md — the frozen pre-registration for this claim (criterion verbatim, statistic,
  thresholds, null-test exemption), timestamped before the panel scored anything.
- Pinned requirements: python 3.11; numpy 2.4.6; scipy 1.17.1 (the packaged standalone checker
  uses the standard library only).
