# Run it yourself

From this folder, in a fresh shell (Python 3, standard library only):
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output (verify-it-yourself/RECEIPTS.md has the real one):
```
sha256 26a206db2dafae4a7f2c6f7478738acf5550af13998da2d4d0dff610ba83f82e
checker A: CAP - cap of size 1104 (pairs checked: 608856)
checker B: CAP - 0 lines inside S (lines meeting S twice or more: 608856)
VERDICT: CAP size 1104 n 9
PASS
```
The object, object/cap_1104_n9.txt, has one point per line: 9 digits from {0,1,2}. A cap means no three distinct
points x, y, z with x + y + z = 0 (mod 3), equivalently no three points on an affine line.

## Rebuild the object
Needs Python 3 with the pinned packages in how-we-built-it/requirements.txt (OR-Tools CP-SAT, numpy):
```sh
cd how-we-built-it
python3 fetch_512.py                                    # downloads the FunSearch 512-cap -> checker/record_512_n8.txt
python3 code/build_n9_frame.py diag22222111 rebuilt.txt # K = 92 points, exact max cap 80 (OPTIMAL), 1104 points
python3 ../verify-it-yourself/capcheck.py rebuilt.txt 9
```
The construction: S = {0} x B0 u {1} x C u {2} x D C in F_3 x F_3^8, where C is the FunSearch 512-cap,
D = diag(2,2,2,2,2,1,1,1), and B0 is a maximum cap (80 points) inside the 92 points of F_3^8 that are not of the form
-(c + D c') with c, c' in C. Every line of F_3^9 lies in one slice or meets all three, so S is a cap exactly when each
slice is a cap and B0 avoids -(C + D C). On the run's machine the rebuild gave a set identical to object/ (CP-SAT with
2 workers; another solver version may return a different 80-point slice, which gives another 1104-cap).
