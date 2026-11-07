# Run it yourself

From this folder, with Python, numpy and python-flint, and clang.

1. Short check: `sh verify-it-yourself/run_checks.sh`, last line PASS.

2. Table: `cat object/V_b_parts/V_b.npy.xz.part* | xz -d > V_b.npy; cp object/V_b.json .` gives the table used for the certificate (the joined V_b.npy.xz has sha256 3511d3527f799d504c0db8ef8707ea63a2d50d2ff1da8137c25b7564dc9af7a9; the part hashes are in SHA256SUMS). To rebuild it instead: `python3 -I how-we-built-it/build_V.py V_b .501 .0035 1600 .0042 .5 .015` writes V_b.npy and V_b.json in the current folder, about 1 minute. The table used for the certificate has sha256 b1712e642ea9a80c1731556369451bb7afb4dcfab14fa71a218c3351440def0c. A rebuilt table on another machine may differ in the last bits; any table that passes the checks gives the theorem, with (LATE), (GAP) rerun on it.

3. Full check, about 40 minutes on two cores: `python3 -I verify-it-yourself/check_hjb.py V_b 1e-6 0 300` and `python3 -I verify-it-yourself/check_hjb.py V_b 1e-6 300 1600`. Each ends with PASS.

4. Interval check: `clang -O2 -ffp-contract=off -o check2 verify-it-yourself/check2.c -lm`, then `./check2 --npy V_b.npy --json V_b.json --rows 0 1600 --maxboxes 300000 --maxdepth 64 --log full.log`.

5. Constants: `python3 -I verify-it-yourself/late_gap.py V_b` ends with `GAP OK` and prints the INIT slack.
