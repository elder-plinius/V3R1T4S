# Run it yourself

From this folder, in a fresh shell (Python 3, standard library only):
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output (verify-it-yourself/RECEIPTS.md has the real one):
```
sha256 4e457e7ee1232a6b4c5ea299b7616c6e4329f04ba11531cadacd4a0d715e9ca7
colour 1: 5724 edges, no triangle (every edge checked)
colour 2: 6655 edges, no triangle (every edge checked)
colour 3 on vertices 0..265 (circulant, verified): clique number 13 (exhaustive through vertex 0)
vertices 266..270: no colour-3 edge among them, so a colour-3 clique holds at most one of them
colour 3 clique number = 14; witness of size 14: [0, 264, 261, 246, 242, 249, 189, 186, 83, 86, 33, 30, 2, 266]
N 271: no K_3 in colour 1, no K_3 in colour 2, no K_15 in colour 3
proves R(3,3,15) >= 272
PASS
PASS
```
The object, object/R_3_3_15.txt, is a 3-colouring of K_271 as a matrix: a "#" comment line, then "matrix 271 3", then 271 rows of 271 digits; digit j of row i is the colour of edge {i, j} (0 on the diagonal). The claim: colours 1 and 2 have no triangle and colour 3 has no K_15, so R(3,3,15) >= 272.

Structure used by the checker: vertices 0..265 form a circulant (the colour of {i, j} depends only on (j - i) mod 266) whose colour-3 clique number is 13; vertices 266..270 have no colour-3 edge among themselves and colour-3 edges to every old vertex; so the colour-3 clique number is 14.

## Rebuild the object
```sh
cd how-we-built-it
python3 code/join_k5.py source/R_3_3_14.txt rebuilt.txt
python3 ../verify-it-yourself/verify_join.py rebuilt.txt 266
```
how-we-built-it/README.md records what the rebuild gave on the run's machine.
