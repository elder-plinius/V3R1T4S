# How the object was built (exact commands, from the package folder)

Requirements: python3 (standard library only) and a C compiler (cc). No pinned packages.

1. The code. `hermitian.py m` prints the extended one-point code E_m on the Hermitian curve y^3 + y = x^4 over GF(9)
   (GF(9) = GF(3)[w]/(w^2 - w - 1), a + b*w stored as a + 3b): one row per monomial x^i y^j with j <= 2 and
   3i + 4j <= m, evaluated at the 27 affine points (ordered by x, then y, in that encoding), plus a 28th coordinate
   equal to 1 for the monomial of pole order m and 0 otherwise.

       python3 how-we-built-it/hermitian.py 13

2. Distance and hull (exact Brouwer-Zimmermann minimum distance and Hermitian hull dimension; about 25 s):

       cc -O3 -o analyze how-we-built-it/analyze.c
       python3 how-we-built-it/hermitian.py 13 | ./analyze noeps
       # code 0 K=11 n=28 rank=11 d=15 hull=6

3. The EA code (Hermitian construction: an [n, kappa, d]_9 code with hull dimension l gives [[n, kappa - l, >= d;
   n - kappa - l]]_3, here [[28, 5, >= 15; 11]]_3) as a JSON object with G9, D9 = C^perp_H and S = phi(D9):

       python3 how-we-built-it/build_claim.py 13 rebuilt.json 15
       shasum -a 256 rebuilt.json object/eaqecc_28_5_15_11.json   # identical:
       # 83602b9ae21bd9ab3d1872f4bb244f452a689cb88254e0cc398a75df2e9fd434

4. How the cell was chosen: `for m in $(seq 6 16); do python3 how-we-built-it/hermitian.py $m; done | ./analyze noeps
   > analysis.txt`, then `python3 how-we-built-it/cells_from_codes.py cells.csv analysis.txt`, where cells.csv is
   the live table parsed into rows n,k,c,d_lower,d_upper,color,title (the page itself is not included here).
   For m = 6..16 the run found [28, m-2, 28-m] with hulls 3,4,6,5,6,5,5,6,6,6,8.

PREREG.md is the frozen success rule of the run that found the object (written before any search output existed).
That run was cut off before its panel; PREREG_panel_run.md is the rule of the follow-up run that rebuilt the object
byte for byte and produced the skeptic reports in panel/.
