# Receipts (real output)

## sh verify-it-yourself/run_checks.sh (quick)
```
PASS
```
## python3 verify-it-yourself/check_c3.py
```
0. object sha256 matches INDEX.csv
1. A^T J A - J contains 0: True
2. c_0..c_7 contain 0: True
   q coefficients l^0..l^4: ['[1.000000000 +/- 1e-14]', '[0.9152926480 +/- 3.71e-11]', '[-0.1613963447 +/- 4.47e-11]', '[0.9152926480 +/- 3.71e-11]', '1.000000000']
3. via a3: disc [9.4833460 +/- 1.02e-8], s [-1.99739841527964 +/- 4.62e-15] [1.08210576724262 +/- 2.52e-15], in (-2,2): True; omega ['[0.159012938903764251 +/- 1.90e-19]', '[0.491881305365955760 +/- 2.83e-19]']; encloses source: True
3. via a1: disc [9.4833460 +/- 1.02e-8], s [-1.99739841527964 +/- 4.62e-15] [1.08210576724262 +/- 2.52e-15], in (-2,2): True; omega ['[0.159012938903764251 +/- 1.90e-19]', '[0.491881305365955760 +/- 2.83e-19]']; encloses source: True
PASS
```
## FULL=1 (certify.py rerun): not run inside this folder; the same command was rerun independently by the self-break verifier and the REPRODUCE panelist, both printing "CERT ROW 2: PASS" with a byte-identical A enclosure; reference output object/certify_row2.txt.
