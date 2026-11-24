# Receipts for verify-it-yourself/run_checks.sh

Run from the package folder with python3 (standard library only). Real output:

    T1 r1 printed 0.991  rounding=MATCH  truncation=MATCH  3dp 0.991 / 0.991
    T1 r2 printed -0.993  rounding=MATCH  truncation=MATCH  3dp -0.993 / -0.993
    T1 r3 printed -1.012  rounding=MATCH  truncation=MATCH  3dp -1.012 / -1.012
    T1 r4 printed 1.0019  rounding=MATCH  truncation=MISMATCH  3dp 1.002 / 1.001
    T1 r5 printed 1.0004  rounding=MATCH  truncation=MATCH  3dp 1.000 / 1.000
    T2 r1 printed -0.974798  rounding=MISMATCH  truncation=MISMATCH  3dp -0.975 / -0.974
    T2 r2 printed -0.9949  rounding=MISMATCH  truncation=MATCH  3dp -0.995 / -0.994
    T2 r3 printed -1.007  rounding=MATCH  truncation=MATCH  3dp -1.007 / -1.007
    T2 r4 printed -0.9949  rounding=MISMATCH  truncation=MISMATCH  3dp -0.995 / -0.995
    T2 r5 printed -1.02  rounding=MATCH  truncation=MATCH  3dp -1.021 / -1.020
    T2 r6 printed -0.9998977  rounding=MATCH  truncation=MISMATCH  3dp -1.000 / -0.999
    T2 r7 printed 1.025  rounding=MISMATCH  truncation=MATCH  3dp 1.026 / 1.025
    T2 r8 printed -0.997  rounding=MATCH  truncation=MATCH  3dp -0.997 / -0.997
    T2 r9 printed 0.997  rounding=MISMATCH  truncation=MATCH  3dp 0.998 / 0.997
    T2 r10 printed 1.0017  rounding=MISMATCH  truncation=MATCH  3dp 1.002 / 1.001
    T2 r11 printed -1.0002  rounding=MATCH  truncation=MATCH  3dp -1.000 / -1.000
    T2 r12 printed 1.00057  rounding=MISMATCH  truncation=MISMATCH  3dp 1.001 / 1.000
    T2 r13 printed 1.0079  rounding=MATCH  truncation=MATCH  3dp 1.008 / 1.007
    T2 r14 printed -1.00004  rounding=MISMATCH  truncation=MISMATCH  3dp -1.000 / -1.000
    rounding {'MATCH': 11, 'MISMATCH': 8, 'AMBIGUOUS': 0}
    truncation {'MATCH': 13, 'MISMATCH': 6, 'AMBIGUOUS': 0}
    corrections at printed precision (either convention): ['T2 r1', 'T2 r4', 'T2 r12', 'T2 r14']
    convention-dependent (rounding only): ['T2 r2', 'T2 r7', 'T2 r9', 'T2 r10']
    mismatch under truncation only: ['T1 r4', 'T2 r6']
    PASS
