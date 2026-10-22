# How We Found It (`vnncomp-2026-unsolved-instance-counterexample`)

> Contributor text, unverified.

## 1. Auditing the Unsolved Frontier in VNN-COMP 2026 (`SCORING/results.txt`)

Parsing `VNN-COMP/vnncomp2026_results/SCORING/results.txt` (`sha256: ec1b6fcbdef79539ffee17adbda2e99add137ba963a5306b87904035289eb26f`) across all 22 competition categories (`excluding soundnessbench_2026 and test`) revealed `242` undecided instances (`True Result: -`). In `2026_challenging_certified_training_2026` (`8` participating tools: `agate`, `alpha_beta_crown`, `n2v`, `neuralsat`, `nnv`, `pyrat`, `super_simple_vnn_comp`, `vibecheck`), `29 / 60` instances remained completely unsolved, including `15` instances on the 7-layer wide convolutional network `onnx/tinyimagenet_eps1_wide_cnn7.onnx` (`141,147,418` bytes, input shape `(1, 3, 64, 64)` = `12,288` coordinates, `200` output classes).

## 2. Why Standard Falsifiers Failed on `tinyimagenet_eps1_wide_cnn7_idx7687_sample8`

On instance 58 (`tinyimagenet_eps1_wide_cnn7_idx7687_sample8`, ground-truth class $y_{\text{true}} = 153$), all 8 competition tools scored `0` (`timeout` for `n2v` and `neuralsat`, `error` for `nnv` and `pyrat`, `-` for the remaining tools), and the benchmark authors' own 1,000-second `abCROWN` baseline also timed out at `1001.67s`. At the box center $x_0 = (\text{lb} + \text{ub})/2$, the network is safely classified as class `153` with worst-case margin $-0.723220$ (and rival `179` margin $Y_{179} - Y_{153} = -0.876775$). Standard single-target PGD with small step schedules or boundary clamping either gets trapped in suboptimal ReLU orthants or places coordinates on the box boundary $\text{lb}_i, \text{ub}_i$.

## 3. Top-$K$ Rival Screening + Exact Linear-Region Seam Surgery + Strict Interior Contraction

1. **Multi-Rival Screening:** We screened the top rival classes $k \neq 153$ on `tinyimagenet_eps1_wide_cnn7_idx7687_sample8` using momentum-PGD + Adam + CosineAnnealing restarts (`how-we-built-it/triage_cifar100_and_tiny.py`), identifying rival class $y_{\text{adv}} = 179$ (disjunct `#178`, $Y_{153} \le Y_{179}$) as crossing zero with a positive violation margin.
2. **Exact Linear-Region Extraction & Strictly Interior Polishing (`how-we-built-it/polish_and_attack_cct.py`, `how-we-built-it/certify_counterexample_lens2.py`):** Once inside the violating basin for $Y_{179} - Y_{153} > 0$, we pulled every coordinate strictly into the open `float32` box $[\text{lb}_i + \delta, \text{ub}_i - \delta]$ with $\delta = 2 \times 10^{-6}$, Achieving minimum `float32` boundary clearance $1.668930 \times 10^{-6} > 0$ across all `12,288` coordinates (`0` boundary coordinates).
3. **Four-Runtime & Official Validator Certification:** At the polished point $x$, all `1,638,912` ReLU units across all 6 ReLU layers are strictly away from the `0` kink in `float64`, so the network is locally an exact affine linear functional $f(x') = W_{\text{eff}} x' + b_{\text{eff}}$. Evaluating $x$ across four independent runtimes yields $Y_{179} - Y_{153} = +0.04230213$ (`onnxruntime` CPU `float32`), $+0.04230690$ (`onnx.reference.ReferenceEvaluator`), $+0.04228902$ (PyTorch `float32`), and $+0.04230902$ (PyTorch `float64`), and both official VNN-COMP 2026 validators (`counterexamples.py` and `counterexamples_v2.py`) return `'correct'` at `abs_tol=0.0, rel_tol=0.0`.
