# Run it yourself (from this folder, in a fresh shell)

Python 3 with torch (CUDA), numpy and scipy. object/model/nqs.py and verify-it-yourself/estimator2.py find the CUDA
runtime through the installed `nvidia` pip package (or V3R1T4S_SITE_PACKAGES) and set blocking sync before torch
starts; V3R1T4S_LOCK (optional) names a lock file for one-job-at-a-time machines.

1. Quick check (about 5 minutes): `sh verify-it-yourself/run_checks.sh`; expected last line `PASS`.
2. Load the state: `python object/model/load_example.py object/r10_J0.9_B1.pt 0.9`.
3. The three measurements (20-40 minutes of GPU each; numbers in how-we-built-it/measurements/):

       cd verify-it-yourself
       python estimator2.py ../object/r10_J0.9_B1.pt --nqs_dir ../object/model --mode plain --seed 31337 \
           --chains 2048 --therm 50 --gap 2 --min_rounds 50 --max_rounds 400 --neff 100000 --out S1_plain_31337
       python estimator2.py ../object/r10_J0.9_B1.pt --nqs_dir ../object/model --mode dis --seed 2718 \
           --chains 2048 --therm 50 --gap 2 --min_rounds 50 --max_rounds 400 --neff 100000 --out S3_dis_2718
       python estimator2.py ../object/r10_J0.9_B1.pt --nqs_dir ../object/model --mode plain --seed 4242 \
           --chains 2048 --therm 50 --gap 2 --min_rounds 50 --max_rounds 400 --neff 100000 \
           --varH 1.8152283827002975 --out S2_plain_4242

   Expected (Pauli units): S1 -253.748447 +- 0.003747; S3 -253.747382 +- 0.003249;
   S2 -253.753424 +- 0.003999; GPU results agree within the error bars, not bit for bit.
4. Instrument checks: how-we-built-it/checks.py (I1, I2v2, I3v2) and tail_sign.py, with outputs in
   how-we-built-it/instrument_checks/ (their paths point at the run's folders; edit the constants at the top).
5. Rebuild the state: how-we-built-it/train.py (night 1: 4x4 -> 6x6 -> 10x10 kernel transfer, MinSR); the 10x10 run's
   log is how-we-built-it/training_log_r10_J0.9_B1.txt (648 steps).
