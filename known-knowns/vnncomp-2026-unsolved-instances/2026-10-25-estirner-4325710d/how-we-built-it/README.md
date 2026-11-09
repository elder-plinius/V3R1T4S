# How we built it

Code (code/; Python 3.12, torch 2.9 with CUDA, onnx 1.21.0, onnxruntime 1.26.0, numpy 2.2.6). Paths: the scripts read
the benchmark files from `$LENS/in/bench/` (LENS defaults to the folder above code/) and import `vnnspec.py` and
`cuda_blocking.py` from code/.
- `bnnx.py`: exact integer model of the binarized 48x48 and 64x64 traffic-sign networks on the GPU (or the CPU with
  BNNX_CPU=1), checked layer by layer against onnxruntime; strict-interior pixel grid.
- `relax1.py`, `mf_relax.py`, `mf1.py`: the relaxed first-layer search and the moment-propagation helpers that `mf4.py`
  imports.
- `mf4.py`: iterated target propagation with a continuous first-layer realisation step (the search that crossed).
  `job7.sh` is the job that crossed: `mf4.py 64 6371 110 9 4 1.0 20 0 2` started from the tie point
  (checkpoints/checkpoint_mf4_tie_x_64_6371.npy), giving checkpoints/checkpoint_mf4_cross_x_64_6371.npy (logit gap +8;
  outputs/mf4_continuation_crossing.log).
- `polish.py`: exact single-pixel polish (outputs/polish.log); `robust_polish.py`: moves the pixel that keeps the
  closest first-layer neuron away from its threshold; `replay_x.py`: onnxruntime CPU replay and float32 witness writer
  (outputs/replay_candidate.log).
- Judge outputs from the run (outputs/finalize.out, own_check.out, official_v2.out): the run's own checker and the
  unmodified official validator on the final witness.
- PREREG.md and PREREG.v2.md: the run's frozen rule (null test not needed: an explicit object judged by deterministic
  checkers); v2 added these six rows to the pool before any attack on them.
