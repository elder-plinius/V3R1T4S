# Run it yourself

From this folder, in a fresh shell with Python 3 and `pip install numpy onnxruntime onnx` (and `vnnlib==1.0.2` for the
official validator):

    sh verify-it-yourself/run_checks.sh               # last line: PASS (downloads 65.2 MB once; VNN_CACHE=<dir> to reuse)
    python3 verify-it-yourself/official_validate.py   # ('correct', ...) at abs_tol 0.0 and 1e-4

Expected output: verify-it-yourself/RECEIPTS.md.

To rebuild the object (GPU with torch and onnx2torch; see how-we-built-it/README.md): run how-we-built-it/code/attack.py
on the instance (--budget 300 --seed 0), then how-we-built-it/code/finalize.py on that run's best_x.npy. GPU attacks are
not bit-reproducible across hardware; the object itself is the claim, and the checkers above judge it.
