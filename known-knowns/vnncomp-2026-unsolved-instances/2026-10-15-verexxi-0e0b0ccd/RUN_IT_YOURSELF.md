# Run it yourself

From this folder, in a fresh shell with Python 3 and `pip install numpy onnxruntime` (optionally `onnx vnnlib==1.0.2`):

    sh verify-it-yourself/run_checks.sh          # last line: PASS
    python3 verify-it-yourself/official_validate.py   # ('correct', ...) at abs_tol 0.0 and 1e-4

Expected output: verify-it-yourself/RECEIPTS.md. To rebuild the object from its search checkpoint, see
how-we-built-it/README.md step 5 (the witness is x = v + off + m*d with the pixel map described there).
