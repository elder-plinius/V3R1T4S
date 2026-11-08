# VarBench J1J2/square_100_P_0.9.md: a neural variational state below every known energy

## What

For VarBench J1J2/square_100_P_0.9.md (10 x 10, periodic in x and y, J1 = 1, J2 = 0.9, Sz = 0, Pauli convention; file re-fetched unchanged at 2026-10-23T17:32:29Z), the fixed state object/r10_J0.9_B1.pt has a fresh-sample Monte Carlo energy below every row of that file (best -250.78657331066935) and below the lowest published variational value I found, -253.668 (arXiv:2606.04558 v1 and v2, Table I, 10 x 10 J2 = 0.90 ViT -0.634170 per site times 400), by more than the success margin, as shown by the claimant's bounded-weight DIS estimate -253.7473816594384 +- 0.0032485374695990594 and by my own independent plain estimate -253.74398860968137 +- 0.011353681212836501 (41984 samples, 39745 effective), the >= 10^5-effective-sample skeptic re-estimate itself being the REPRODUCE skeptic's to supply.

Status (panel/gate.md): CONFIRMED_SOLUTION. Energy in VarBench's Pauli convention (E = 400 e, e per site in S.S units):
E = -253.753424311 +- 0.003999231 (plain Monte Carlo, seed 4242, 102400 samples), E_DIS = -253.747381659 +- 0.003248537
(tail-safe defensive-mixture estimate, seed 2718), E = -253.748446817 +- 0.003746765 (seed 31337).

Object (since 2026-11-08, as the maintainers asked): object/r10_J0.9_B1.onnx (sha256
51918b654d3417330e96f5118f25b72f3aa6a737547c0c848bd14477ace1d9e0), an ONNX export of the PyTorch checkpoint the panel
reviewed (r10_J0.9_B1.pt, sha256 e68644979db4d9764ac1787d1c064fe18c4750cb4cb47ee573e40588bcd9c485, no longer shipped).
The panel's sentence above names that checkpoint; the export is the same state (see "The exported state"). The
submission id e6864497 is the checkpoint's hash prefix and predates the export.

## Check it yourself

    sh verify-it-yourself/run_checks.sh          # PYTHON=<python with numpy and onnxruntime> if python3 lacks them

Expected last line: `PASS` (verify-it-yourself/RECEIPTS.md). About one minute on two CPU threads: the object hashes,
the ONNX signature, the 100-row reference table, the symmetries built into the state, and the local energies of 256 of
the 2048 saved configurations (`NREF=2048` for all of them, about 8 minutes). The >= 1e5-sample energy estimates
above were made with the PyTorch checkpoint before the export (RUN_IT_YOURSELF.md).

## The exported state

- File: object/r10_J0.9_B1.onnx, 97834 bytes, ONNX IR version 8, opset 17, default operator domain only (Add, Atan,
  Concat, Constant, Conv, Cos, Div, Erf, Exp, Gather, Greater, Less, Log, MatMul, Mul, ReduceMax, ReduceSum, Reshape,
  Sin, Slice, Sub, Where); all weights inside the file, no external data; float32 throughout, as in training.
- Input `spins`: float32, shape [batch, 100], one configuration per row, +1 = up, -1 = down. Site k = 10 r + c for the
  lattice coordinates r, c = 0..9 (row-major). The nearest neighbours of (r, c) are (r, c +- 1) and (r +- 1, c), the
  next-nearest (r +- 1, c +- 1), all modulo 10: VarBench's square_100_P lattice, periodic in both directions.
- Why these two conventions cannot change the result: the state is symmetric under global spin flip (character +1),
  so reading +1 as down instead of up gives the same psi; and numbering the sites column-major instead (k = 10 c + r)
  is the diagonal reflection, under which this B1 state only changes sign, psi -> -psi for every configuration, so
  every ratio psi(s')/psi(s), every local energy and the energy are unchanged. Translations are symmetries too, so
  the choice of site 0 does not matter either.
- Outputs: `log_abs_psi` [batch] = log|psi(s)| and `phase` [batch] = arg psi(s) in radians, in (-pi, pi];
  psi(s) = exp(log_abs_psi + i phase), not normalised. The amplitudes are real up to a nearly constant phase: modulo
  pi, the phases of the reference rows lie between pi - 0.00318 and pi - 0.00315 (between pi - 0.0033 and pi - 0.0029
  on 1000 random configurations).
- Sector: Sz = 0. Evaluate and sample only configurations with exactly 50 up and 50 down spins.
- Energy convention: Pauli, as in VarBench. H = J1 sum_<ij> sigma_i.sigma_j + J2 sum_<<ij>> sigma_i.sigma_j with
  J1 = 1, J2 = 0.9 and Pauli matrices sigma, each of the 200 nearest-neighbour and 200 next-nearest-neighbour bonds
  counted once; sigma_i.sigma_j = sigma^z_i sigma^z_j + 2 (sigma^+_i sigma^-_j + sigma^-_i sigma^+_j). This is 4 times
  the energy written with S = sigma/2, so E = 400 e for e per site in S.S units. Every energy in this package uses it.
- Built into the network, nothing to add on the sampler side:
  1. the stripe sign rule, a factor (-1)^(number of up spins on odd columns c), added to the phase as pi per such spin;
  2. projection on the B1 representation of C4v about site 0, psi(s) = sum_g chi(g) psi0(g s), with chi = +1 for the
     identity, the 180-degree rotation and the two axis reflections, and chi = -1 for the 90- and 270-degree rotations
     and the two diagonal reflections;
  3. global spin flip with character +1 (the sum also runs over -g s: 16 images in all);
  4. translation invariance, by construction: periodic convolutions whose per-site outputs are summed over the sites
     (the stripe sign is translation invariant in the Sz = 0 sector).
  Step 4 of verify-it-yourself/verify.py checks 2, 3 and 4 on the ONNX file itself.
- Reference values: object/r10_J0.9_B1.reference_values.csv, 100 random Sz = 0 configurations (numpy
  default_rng(20261108)); `spins` is 100 characters, character k for site k, u = up (+1), d = down (-1); `log_abs_psi`
  and `phase` come from the trained model's own forward pass (nqs.NQS.forward, PyTorch, GPU, float32), the function
  the ONNX graph encodes. The ONNX file under onnxruntime 1.26 on the CPU reproduces them within 7.7e-6 in log|psi| and
  1e-9 rad in phase. On 1000 random configurations the largest log|psi| difference was 5.4e-4, at a configuration
  where the 16 image terms cancel to 0.23% of their summed magnitude (median 99.6%), which magnifies float32 rounding.
  The energy measurements evaluated the same network but summed the 16 images in float64
  (how-we-built-it/estimator2.py); on the same 1000 configurations that sum differs from the ONNX file by at most
  5.4e-4 in log|psi| and 3.8e-4 rad in phase (how-we-built-it/export_report.json).
- Energy check of the export: the local energies of the 2048 saved configurations (final chain states of measurement
  S2), recomputed from the ONNX file with a Hamiltonian written from the definition, match the values the measurement
  code recorded: mean difference 1.0e-5, largest 1.0e-3, mean local energy -253.803492 against -253.803502
  (verify-it-yourself/RECEIPTS.md).
- How it was made: how-we-built-it/export_onnx.py (torch 2.9, TorchScript exporter, the model's own forward pass with
  the batch size left free); its output is how-we-built-it/export_report.json.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| VarBench J1J2/square_100_P_0.9.md | best row (DMRG, bond dimension 1024) | -250.78657331066935 | https://raw.githubusercontent.com/varbench/varbench/main/J1J2/square_100_P_0.9.md | 2026-10-23T15:08:00Z |
| arXiv:2606.04558v2, Table I | 10 x 10, J2 = 0.90, ViT | -0.634170 per site = -253.668 | https://arxiv.org/abs/2606.04558 | 2026-10-22T16:49:41Z |

Margin below -253.668: 0.085424 (required max(3 sigma, 1e-6 |E|) = 0.011998).

## Corrections of the claim text (from the panel; panel/gate.md)

- how-we-built-it/measurements/S2_plain_4242.json and S3_dis_2718.json give N_eff = 113495 and 172011, and the claim
  text repeated them; those numbers divide the DIS estimate of Var(H) by each run's
  sigma^2 and are not sample counts. Counted as raw samples / autocorrelation time: S1 101824, S2 83176; S3's Kish
  effective sample size is 97096 before autocorrelation. The criterion's re-estimate with >= 1e5 effective samples is
  the REPRODUCE skeptic's: 219136 samples, N/2tau = 208462, E = -253.749891 +- 0.003879 (plain) and
  -253.752519 +- 0.002064 (its own bounded-weight estimator), panel/reproduce.md.
- The plain error bars (S1, S2) are optimistic under the heavy, upward-skewed local-energy tail; rely on the
  bounded-weight estimates (S3 and the REPRODUCE skeptic's), which clear the bar by 24 and 41 of their sigma.
- The claimant's table fetch (15:08Z) was not immediately before claiming; the skeptics' fetches between 17:28Z and
  18:58Z (2026-10-23) found the file unchanged.
- Only the .json summaries of the three measurements are included (how-we-built-it/measurements/), plus the 2048
  final chain states of S2 (verify-it-yourself/ref_configs.npz); the per-run .npz and .log files are not.
- how-we-built-it/nqs.py stores the B1 character phase as float32(pi), 8.7e-8 rad from pi, and the ONNX file carries the
  same constant; the state is a valid variational state either way and the energy effect is negligible (panel/reproduce.md).

## Not claimed

- Not an exact, extrapolated or ground-state energy; not a V-score result (partial win p1); nothing about any other
  VarBench file, size or J2.
- The bar prints no error bar; it is used as exact (sigma_best = 0). The authors' own later re-measurement of their
  final state (-253.6416(60) via an aggregator, not in the paper) is higher and does not change the comparison.
- The panel reviewed the PyTorch checkpoint, not the ONNX file; the export is tied to it by the reference table and
  the local energies above. The >= 1e5-effective-sample re-estimate with the maintainers' own sampler is theirs.
- how-we-built-it/nqs.py differs from the run's copy only in two machine-specific lines (the CUDA runtime location and an
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
