# VarBench J1J2/square_100_P_0.9.md: a neural variational state below every known energy

## What

For VarBench J1J2/square_100_P_0.9.md (10 x 10, periodic in x and y, J1 = 1, J2 = 0.9, Sz = 0, Pauli convention; file re-fetched unchanged at 2026-10-23T17:32:29Z), the fixed state object/r10_J0.9_B1.pt has a fresh-sample Monte Carlo energy below every row of that file (best -250.78657331066935) and below the lowest published variational value I found, -253.668 (arXiv:2606.04558 v1 and v2, Table I, 10 x 10 J2 = 0.90 ViT -0.634170 per site times 400), by more than the success margin, as shown by the claimant's bounded-weight DIS estimate -253.7473816594384 +- 0.0032485374695990594 and by my own independent plain estimate -253.74398860968137 +- 0.011353681212836501 (41984 samples, 39745 effective), the >= 10^5-effective-sample skeptic re-estimate itself being the REPRODUCE skeptic's to supply.

Status (panel/gate.md): CONFIRMED_SOLUTION. Energy in VarBench's Pauli convention (E = 400 e, e per site in S.S units):
E = -253.753424311 +- 0.003999231 (plain Monte Carlo, seed 4242, 102400 samples), E_DIS = -253.747381659 +- 0.003248537
(tail-safe defensive-mixture estimate, seed 2718), E = -253.748446817 +- 0.003746765 (seed 31337).

## Check it yourself

    sh verify-it-yourself/run_checks.sh          # PYTHON=<python with torch> if python3 lacks torch

Expected last line: `PASS` (verify-it-yourself/RECEIPTS.md). About 5 minutes on one consumer GPU: object hashes, the
configuration, local energies of 2048 saved configurations, and a short fresh Monte Carlo spot check. The full
>= 1e5-sample re-estimates take about an hour of GPU (RUN_IT_YOURSELF.md).

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| VarBench J1J2/square_100_P_0.9.md | best row (DMRG, bond dimension 1024) | -250.78657331066935 | https://raw.githubusercontent.com/varbench/varbench/main/J1J2/square_100_P_0.9.md | 2026-10-23T15:08:00Z |
| arXiv:2606.04558v2, Table I | 10 x 10, J2 = 0.90, ViT | -0.634170 per site = -253.668 | https://arxiv.org/abs/2606.04558 | 2026-10-22T16:49:41Z |

Margin below -253.668: 0.085424 (required max(3 sigma, 1e-6 |E|) = 0.011998).

## Corrections of the claim text (from the panel; panel/gate.md)

- claim/CLAIM.md gave N_eff = 113495 (S2) and 172011 (S3); those numbers divide the DIS estimate of Var(H) by each run's
  sigma^2 and are not sample counts. Counted as raw samples / autocorrelation time: S1 101824, S2 83176; S3's Kish
  effective sample size is 97096 before autocorrelation. The criterion's re-estimate with >= 1e5 effective samples is
  the REPRODUCE skeptic's: 219136 samples, N/2tau = 208462, E = -253.749891 +- 0.003879 (plain) and
  -253.752519 +- 0.002064 (its own bounded-weight estimator), panel/reproduce.md.
- The plain error bars (S1, S2) are optimistic under the heavy, upward-skewed local-energy tail; rely on the
  bounded-weight estimates (S3 and the REPRODUCE skeptic's), which clear the bar by 24 and 41 of their sigma.
- The claimant's table fetch (15:08Z) was not immediately before claiming; the skeptics' fetches between 17:28Z and
  18:58Z (2026-10-23) found the file unchanged.
- The claim folder's REPRODUCE.md said per-run .npz and .log files were included; only the .json summaries are (this
  package: how-we-built-it/measurements/), plus the 2048 final chain states of S2 (verify-it-yourself/ref_configs.npz).
- object/model/nqs.py stores the B1 character phase as float32(pi), 8.7e-8 rad from pi; the state is a valid variational
  state either way and the energy effect is negligible (panel/reproduce.md).

## Not claimed

- Not an exact, extrapolated or ground-state energy; not a V-score result (partial win p1); nothing about any other
  VarBench file, size or J2.
- The bar prints no error bar; it is used as exact (sigma_best = 0). The authors' own later re-measurement of their
  final state (-253.6416(60) via an aggregator, not in the paper) is higher and does not change the comparison.
- object/model/nqs.py differs from the run's copy only in two machine-specific lines (the CUDA runtime location and an
  optional lock file are read from the environment); the network and the state definition are unchanged.

## Credits

- VarBench: D. Wu, R. Rossi, F. Vicentini et al., Variational benchmarks for quantum many-body problems, Science 386,
  296 (2024), https://arxiv.org/abs/2302.04919, https://github.com/varbench/varbench (the Hamiltonian file and table).
- The bar: V. Golubev, A. Iakovlev, M. Mazurenko, arXiv:2606.04558 (ViT energies for the 10 x 10 J1-J2 model).
- MinSR: A. Chen and M. Heyl, Empowering deep neural quantum states through efficient optimization,
  https://arxiv.org/abs/2302.01941; the linear-algebra identity of R. Rende, L. L. Viteritti, L. Bardone, F. Becca,
  https://arxiv.org/abs/2310.05715 (the training used the stacked real-parameter MinSR form).
- Neural quantum states: G. Carleo and M. Troyer, Science 355, 602 (2017); convolutional states for the J1-J2 model,
  K. Choo, T. Neupert, G. Carleo, https://arxiv.org/abs/1903.06713; exact 6x6 references from Chen, Hendry, Weinberg and
  Feiguin, https://arxiv.org/abs/2206.14307.
- Defensive importance sampling: T. Hesterberg, Technometrics 37, 185 (1995).
- Software: PyTorch, NumPy, SciPy.
