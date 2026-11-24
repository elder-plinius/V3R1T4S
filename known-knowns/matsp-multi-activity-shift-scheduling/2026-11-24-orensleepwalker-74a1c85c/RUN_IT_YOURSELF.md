# Run it yourself

1. `sh verify-it-yourself/run_checks.sh` (expect PASS). It downloads https://www.schedulingbenchmarks.org/matsp/data/instances1_225.zip (sha256 202ddbc48da844a404298f24edecc00f717c21e334e1dfe510e9b20d081cd556) and https://www.schedulingbenchmarks.org/matsp/data/8_7_20_2.Solution.889.xml (sha256 ee1af323a538aa10af486ce87bb5d77d842fd01ebf3f571d85aae4222e31c27f) to a temporary folder.
2. One roster by hand: extract instances1_225/txt/<stem>.txt from the archive, then `python3 verify-it-yourself/verify.py <stem>.txt object/<file> <best known>` prints the violations, the penalty and PASS.
3. The search code is in how-we-built-it/code/ as provenance (paths replaced by WORKSPACE/HOME; it needs HiGHS, OR-Tools, NumPy and Numba and is not deterministic); how-we-built-it/rows.csv names each row's script and wave.
