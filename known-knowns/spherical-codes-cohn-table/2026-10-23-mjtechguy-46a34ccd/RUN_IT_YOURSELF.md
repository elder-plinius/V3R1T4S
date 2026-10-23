From this folder, in a fresh shell:

sh verify-it-yourself/run_checks.sh

The last line is PASS. The script runs python3 verify-it-yourself/check_one.py, which uses only the Python standard library. It normalizes the 650 vectors in object/650.txt at 50 decimal digits, computes every pairwise inner product, and checks that the maximum is at least 1e-10 below the cosine in the-record-we-beat/table_rows.tsv, that the star and needs-more-optimization columns are 0, that every coordinate has at least 20 digits, that the coordinate sum matches verify-it-yourself/expected_sum.txt, and that the maximum agrees with verify-it-yourself/expected_c.txt to 1e-48.

expected_c.txt holds the mpmath value at 50 digits. Both are 0.000337297950824 below the table cosine 0.242872702057.

To rebuild the object you need object/651.txt from package 2026-10-23-mjtechguy-23ad10a0 and the steps in how-we-built-it/COMMANDS.md (numpy, scipy, mpmath). Rebuilding is not required for the check.
