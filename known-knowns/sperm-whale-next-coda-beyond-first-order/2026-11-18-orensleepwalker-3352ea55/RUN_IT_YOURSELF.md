# Reproduce

Use Python 3, NumPy 2.5.4, POSIX shell, curl and sha256sum. Run sh verify-it-yourself/run_checks.sh from this folder. For a full control replay, make a scratch folder with code/, data/ and output/. Copy the included source programs into code/, fetch the pinned CSV to data/sperm-whale-dialogues.csv, and run python3 code/controls.py turns payload then python3 code/controls.py turns first_order with OPENBLAS_NUM_THREADS=1. The default is 400 seeds per command. Existing control logs cause completed seeds to be skipped.
