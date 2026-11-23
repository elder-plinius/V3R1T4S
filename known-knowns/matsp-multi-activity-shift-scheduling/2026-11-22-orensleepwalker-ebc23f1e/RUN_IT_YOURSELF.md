# Run it yourself

1. `sh verify-it-yourself/run_checks.sh` (expect PASS). It downloads https://www.schedulingbenchmarks.org/matsp/data/instances1_225.zip (sha256 202ddbc48da844a404298f24edecc00f717c21e334e1dfe510e9b20d081cd556) and https://www.schedulingbenchmarks.org/matsp/data/8_7_20_2.Solution.889.xml (sha256 ee1af323a538aa10af486ce87bb5d77d842fd01ebf3f571d85aae4222e31c27f) to a temporary folder.
2. To re-solve: install how-we-built-it/requirements.txt (Python 3.12), make a folder with code/ (how-we-built-it/code/*.py) and raw/instances1_225.zip, and run `python3 code/cpsat_matsp.py 155_28_10_2 1800 4 24` from it; it writes out/155_28_10_2.cpsat.xml (create out/ first) and checks it with code/matsp.py.
