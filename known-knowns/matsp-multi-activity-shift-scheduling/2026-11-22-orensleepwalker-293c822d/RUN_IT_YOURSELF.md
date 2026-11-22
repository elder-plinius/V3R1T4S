# Run it yourself

1. `sh verify-it-yourself/run_checks.sh` (expect PASS); it downloads https://www.schedulingbenchmarks.org/matsp/data/instances1_225.zip and checks its sha256.
2. To recompute the bound for all 225 instances and see which ones are tight: `python3 how-we-built-it/code/screen.py` with the instance archive at ../raw/instances1_225.zip relative to a code/ folder holding the script (see its header).
3. To check the best known values against a saved copy of the table: `python3 how-we-built-it/code/check_table.py <matsp.html> object/certificates.csv`.
