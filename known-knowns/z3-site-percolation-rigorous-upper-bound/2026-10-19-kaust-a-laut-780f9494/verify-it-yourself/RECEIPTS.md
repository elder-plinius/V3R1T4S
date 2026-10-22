# Receipts (real output, copied from the runs on this machine)

## Default: sh verify-it-yourself/run_checks.sh
```
1. integrity: 8 object files checked
2. census: 6 faces x 28 values of k sum to the binomial coefficients; minimum size respected
3. chain: 7 links, q_1 = 501/1000, q_j = p_(j-1), last p = 4427/10000
4. root: r_f(full face) - q_j >= 0.259948 in every link (link 1, face 0)
PASS (fast exact checks; FULL=1 reruns the exhaustive certificate with the Go engine)
PASS
```

## Full: PYTHON=<python with numpy> FULL=1 sh verify-it-yourself/run_checks.sh (start and end times from date -u)
```
Mon Oct 19 00:49:35 UTC 2026
1. integrity: 8 object files checked
2. census: 6 faces x 28 values of k sum to the binomial coefficients; minimum size respected
3. chain: 7 links, q_1 = 501/1000, q_j = p_(j-1), last p = 4427/10000
4. root: r_f(full face) - q_j >= 0.259948 in every link (link 1, face 0)
PASS (fast exact checks; FULL=1 reruns the exhaustive certificate with the Go engine)
link 1: p = 2317/5000, q = 501/1000: CERTIFICATE: PASS (p = 2317/5000, q = 501/1000)
checked 3066 entry laws x 7579 up-sets; worst margin 1.939266e-04 at entry face 0 U=0b1 up-set (1, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
link 2: p = 9/20, q = 2317/5000: CERTIFICATE: PASS (p = 9/20, q = 2317/5000)
checked 3066 entry laws x 7579 up-sets; worst margin 1.116371e-04 at entry face 4 U=0b1 up-set (2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
link 3: p = 1781/4000, q = 9/20: CERTIFICATE: PASS (p = 1781/4000, q = 9/20)
checked 3066 entry laws x 7579 up-sets; worst margin 1.136700e-04 at entry face 0 U=0b1 up-set (1, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
chain complete: p_c^site(Z^3) <= 1781/4000 (given Campanino-Russo's p_c < 1/2 for link 1)
link 1: p = 1109/2500, q = 1781/4000: CERTIFICATE: PASS (p = 1109/2500, q = 1781/4000)
checked 3066 entry laws x 7579 up-sets; worst margin 2.035065e-04 at entry face 0 U=0b1 up-set (1, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
link 2: p = 443/1000, q = 1109/2500: CERTIFICATE: PASS (p = 443/1000, q = 1109/2500)
checked 3066 entry laws x 7579 up-sets; worst margin 1.655116e-04 at entry face 0 U=0b1 up-set (1, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
link 3: p = 1107/2500, q = 443/1000: CERTIFICATE: PASS (p = 1107/2500, q = 443/1000)
checked 3066 entry laws x 7579 up-sets; worst margin 1.993285e-04 at entry face 0 U=0b1 up-set (1, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
link 4: p = 4427/10000, q = 1107/2500: CERTIFICATE: PASS (p = 4427/10000, q = 1107/2500)
checked 3066 entry laws x 7579 up-sets; worst margin 1.231418e-04 at entry face 0 U=0b1 up-set (1, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
chain complete: p_c^site(Z^3) <= 4427/10000 (given Campanino-Russo's p_c < 1/2 for link 1)
PASS (full: counts reproduced byte for byte, 7 of 7 links certified)
Mon Oct 19 01:00:22 UTC 2026
```

(Each link also printed its worst up-set margin; see how-we-built-it/outputs/*_summary.txt. The closing "given Campanino-Russo's p_c < 1/2" text is cosmetic: ERRATA.md item 2.)
