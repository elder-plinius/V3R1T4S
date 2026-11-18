# Run it yourself

1. Check the package: `sh verify-it-yourself/run_checks.sh` (expect PASS). Standard library only.
2. Rebuild the predictions: download the Dryad deposit doi 10.5061/dryad.hmgqnk9nj (version 16) in a browser (Dryad refuses scripted downloads) and check the spectral and cepstral n469 files against Dryad's sha-256 digests. Make a folder with `code/` (copy how-we-built-it/code/*.py) and `data/` (the two n469 CSV files). Install how-we-built-it/requirements.txt (Python 3.12). Then, with OMP_NUM_THREADS=1:
   `WORKERS=4 python3 code/run_real.py && python3 code/context_check.py && python3 code/null_pa.py && python3 code/null_rf.py && python3 code/summarize.py`
   (about 2.5 hours on 4 cores). output/summary.json must equal object/summary.json, and output/real/draw_SSS.json must equal object/real-draws/draw_SSS.json byte for byte. A single file can be replayed in seconds with `python3 code/replay.py real <s>` or `python3 code/replay.py null_rf <j>` once output/ holds the saved files.
3. The call list: object/calls.csv equals the rows with Cert_ID_Bin == 1 of the spectral n469 file, columns soundID, CallerID, Elicitor1_ID, in file order.
