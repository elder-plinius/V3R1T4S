# Run it yourself

All commands run from this folder in a fresh shell.

## 1. Check the object (seconds, Python standard library only)

    sh verify-it-yourself/run_checks.sh

Expected output (verify-it-yourself/RECEIPTS.md has the real one):

    annual: RMSE 0.996243 n=1065 | published 1.00 n=1065 | |diff| 0.0038 <= 0.01: True | count ok: True | equals printed 0.9962432770: True
    winter: RMSE 0.588143 n=999 | published 0.59 n=999 | |diff| 0.0019 <= 0.01: True | count ok: True | equals printed 0.5881431289: True
    summer: RMSE 0.700051 n=1028 | published 0.70 n=1028 | |diff| 0.0001 <= 0.01: True | count ok: True | equals printed 0.7000514609: True
    object sha256 a44c189b3573a67eb555cc473444fb7c09e6a87d719d986de96c38a0d3db1164 equals the recorded a44c189b3573a67eb555cc473444fb7c09e6a87d719d986de96c38a0d3db1164: True
    PASS

## 2. Rebuild the object from the shipped data (about 1 minute plus a 27 MB download)

    cd how-we-built-it
    sh get_data.sh                                  # fetches 3 files from ML_MB_Norway @ 32d8175 and checks sha256
    pip install -r requirements.txt                 # xgboost 3.2.0, numpy, pandas (in a virtual environment)
    python -I -B code/reimpl_p3.py data rebuild     # about 5 s on 4 threads, under 1 GB of memory
    diff rebuild/test_record_predictions_primary.csv ../object/test_record_predictions_primary.csv && echo identical

Expected last lines of the rebuild (how-we-built-it/output/primary_output.txt):

    OUR MODEL on OUR test records: annual 0.9962 (n=1065) / winter 0.5881 (n=999) / summer 0.7001 (n=1028)
    ...
    P3_PASS: yes

The rebuild also writes the retrained booster rebuild/model_primary.json (1095898 bytes, sha256
8eb005e47d3fe65ee2510cb7df464dcc79567df2efbd029b953381405626581f in our run; not shipped because it is over 1 MB).
The record-predictions file was bit-identical on a second fit in our run; across machines, CPUs or library builds
the last float digits may differ, which moves the RMSEs far less than the 0.01 tolerance.

## 3. Optional checks

    python -I -B code/lens2.py code data lens2     # seeds, threads, tree methods, the 9.99 rule, MBM's own grid (about 15 s)
    python -I -B code/deleted_test_rows.py code data   # training with every test-glacier row deleted from the input
