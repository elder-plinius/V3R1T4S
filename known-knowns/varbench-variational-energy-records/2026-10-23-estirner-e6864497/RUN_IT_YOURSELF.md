# Run it yourself (from this folder, in a fresh shell)

1. Quick check, Python 3 with numpy and onnxruntime, CPU only (about one minute):
   `sh verify-it-yourself/run_checks.sh`; expected last line `PASS`. `NREF=2048 sh verify-it-yourself/run_checks.sh`
   re-evaluates all 2048 saved configurations (about 8 minutes on two threads).
2. Evaluate the state: load object/r10_J0.9_B1.onnx in any ONNX runtime. Input `spins`, float32 [batch, 100]
   (+1 = up, -1 = down, site k = 10 r + c); outputs `log_abs_psi` and `phase` (README.md, "The exported state").

       python3 -c "import numpy as np, onnxruntime as ort; s = ort.InferenceSession('object/r10_J0.9_B1.onnx'); \
       x = np.repeat([[1.0], [-1.0]], 50, axis=0).T.astype(np.float32); print(s.run(None, {'spins': x}))"

3. Energy: sample |psi|^2 in the Sz = 0 sector (for example with exchange moves of an up and a down spin) and average
   the local energy of the Hamiltonian in README.md; verify-it-yourself/verify.py (function `eloc`) is a plain
   implementation of the local energy. The package's three measurements (how-we-built-it/measurements/) were made
   before the export, with how-we-built-it/estimator2.py and how-we-built-it/nqs.py on the PyTorch checkpoint
   r10_J0.9_B1.pt (sha256 e68644979db4d9764ac1787d1c064fe18c4750cb4cb47ee573e40588bcd9c485, not shipped), 20-40
   minutes of GPU each:

       python estimator2.py r10_J0.9_B1.pt --nqs_dir . --mode plain --seed 31337 \
           --chains 2048 --therm 50 --gap 2 --min_rounds 50 --max_rounds 400 --neff 100000 --out S1_plain_31337
       python estimator2.py r10_J0.9_B1.pt --nqs_dir . --mode dis --seed 2718 \
           --chains 2048 --therm 50 --gap 2 --min_rounds 50 --max_rounds 400 --neff 100000 --out S3_dis_2718
       python estimator2.py r10_J0.9_B1.pt --nqs_dir . --mode plain --seed 4242 \
           --chains 2048 --therm 50 --gap 2 --min_rounds 50 --max_rounds 400 --neff 100000 \
           --varH 1.8152283827002975 --out S2_plain_4242

   Results (Pauli units): S1 -253.748447 +- 0.003747; S3 -253.747382 +- 0.003249; S2 -253.753424 +- 0.003999.
4. Instrument checks: how-we-built-it/checks.py (I1, I2v2, I3v2) and tail_sign.py, with outputs in
   how-we-built-it/instrument_checks/ (their paths point at the run's folders; edit the constants at the top).
5. Rebuild the state: how-we-built-it/train.py (night 1: 4x4 -> 6x6 -> 10x10 kernel transfer, MinSR); the 10x10 run's
   log is how-we-built-it/training_log_r10_J0.9_B1.txt (648 steps). Export: `python how-we-built-it/export_onnx.py
   r10_J0.9_B1.pt how-we-built-it OUT_DIR` (torch with CUDA, onnx, onnxruntime) writes the ONNX file, the reference
   table and how-we-built-it/export_report.json.
