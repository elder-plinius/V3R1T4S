From this folder, in a fresh shell:

sh verify-it-yourself/run_checks.sh

The last line is PASS. The script runs python3 verify-it-yourself/check_one.py, which uses only the Python standard library. It normalizes the 651 vectors in object/651.txt at 50 decimal digits, computes every pairwise inner product, and checks that the maximum is at least 1e-10 below the cosine in the-record-we-beat/table_rows.tsv, that the star and needs-more-optimization columns are 0, that every coordinate has at least 20 digits, that the coordinate sum matches verify-it-yourself/expected_sum.txt, and that the maximum agrees with verify-it-yourself/expected_c.txt to 1e-48.

expected_c.txt holds the mpmath value at 50 digits. A Decimal run at precision 50 prints the same digits. Both are 0.00279300505343786445429 below the table cosine 0.245484258816.

To rebuild the object you need the 2026-10-22 polish of the table's posted coordinates for this cell, then the LogSumExp steps in how-we-built-it/COMMANDS.md. Rebuilding is not required for the check.
