# How We Built It (`vnncomp-2026-unsolved-instance-counterexample`)

## Scripts in `how-we-built-it/`

- `triage_cifar100_and_tiny.py`: Multi-rival top-$K$ PGD + Adam + CosineAnnealing screening across unsolved `challenging_certified_training_2026` instances, discovering the violating basin for rival class $y_{\text{adv}} = 179$ ($y_{\text{true}} = 153$) on `tinyimagenet_eps1_wide_cnn7_idx7687_sample8`.
- `polish_and_attack_cct.py`: Strict interior box contraction ($\delta = 2 \times 10^{-6}$) and margin maximization inside the open `float32` box $(\text{lb}_i, \text{ub}_i)$.
- `certify_counterexample_lens2.py`: Four-runtime forward-pass verifier (`onnxruntime` CPU `float32`, `onnx.reference.ReferenceEvaluator` `float32`, PyTorch `float32`, and PyTorch `float64`), local linear-region affine functional extractor (`object/linear_region_certificate_idx7687_sample8.npz`), VNN-LIB 1.0 and 2.0 `.counterexample` emitter, and official VNN-COMP 2026 `counterexamples.py` / `counterexamples_v2.py` / `cex_checks.py` harness.
- Additional exploratory triage scripts from Lens 1: `ibp_tsr_triage.py`, `solve_tsr_seam.py`, `attack_cora_img78.py`, `attack_resnet_top.py`, `triage_relu_and_acopf.py`.
