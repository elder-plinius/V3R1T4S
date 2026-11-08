# How we built it

Code (code/; Python 3.12, torch 2.9 with CUDA, onnx2torch 1.5.15, onnx 1.21.0, onnxruntime 1.26.0, numpy 2.2.6):
- `vnnspec.py` reads a VNN-LIB 2.0 file into an input box and a disjunction of linear output atoms; `netload.py` loads
  the ONNX into onnxruntime (CPU) and onnx2torch; `cuda_blocking.py` sets blocking sync before torch uses the GPU.
- `attack.py`: multi-disjunct margin attack (sign-PGD with momentum, cosine steps, uniform / vertex / centre starts,
  then Adam on a sigmoid reparametrisation), every improvement replayed on CPU onnxruntime. Run on this instance:
  `attack.py --onnx <net>.onnx.gz --vnnlib <prop>.vnnlib.gz --out <dir> --budget 300 --seed 0`
  (outputs/plain_attack_summary.json: best +0.002304911613 on the disjunct for rival 8).
- `finalize.py`: snaps a point into the strict box in float32, writes exact-decimal witness files, replays in torch
  float32/float64 (outputs/finalize.out). `vnncheck_own.py`: the claimant's own checker (outputs/own_check.out).
  `official_validate_run.py`: the official validator wrapper (outputs/official_v2.out). `attack_focus.py`,
  `provenance_replay.py`: used for the sibling instances of the same run.
- PREREG.md: the run's frozen rule (null test not needed: an explicit object judged by deterministic checkers).
