# Run it yourself

From this folder, in a fresh shell with Python 3 and `pip install numpy onnxruntime onnx` (and `vnnlib==1.0.2` for the
official validator):

    sh verify-it-yourself/run_checks.sh               # last line: PASS (downloads 0.5 MB once; VNN_CACHE=<dir> to reuse)
    python3 verify-it-yourself/official_validate.py   # ('correct', ...) at abs_tol 0.0 and 1e-4

Expected output: verify-it-yourself/RECEIPTS.md.

To rebuild the object from the saved crossing point (CPU, seconds; see how-we-built-it/README.md):

    mkdir -p in/bench out && cp <the two benchmark files> in/bench/     # same files and sha256 as above
    BNNX_CPU=1 LENS=. python3 how-we-built-it/code/robust_polish.py 64 6371 how-we-built-it/checkpoints/checkpoint_mf4_cross_x_64_6371.npy robust_x.npy 0.05
    BNNX_CPU=1 LENS=. python3 how-we-built-it/code/replay_x.py 64 6371 robust_x.npy repro
    # expected: softmax_margin 0.9993293141305912 logit_gap 8.0 argmax 9 true 17; out/candidate_model_64_idx_6371_eps_1_repro.npy
    # has sha256 af1c32281af6f48bcfc93125e21f0fb0e6bf4aa6a712daa6f7ff4cc72441c430 and the same 12288 values as object/*.npy

The GPU search itself (how-we-built-it/code/mf4.py) is not bit-reproducible across hardware; the object is the claim,
and the checkers above judge it.
