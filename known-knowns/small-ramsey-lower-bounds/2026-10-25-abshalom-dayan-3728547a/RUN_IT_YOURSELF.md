# Run it yourself

From this folder, in a fresh shell (Python 3, standard library only):
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output (verify-it-yourself/RECEIPTS.md has the real one):
```
sha256 3728547aec5e9b0b5779c21b5bf06cee6dfb90a01230c42389b821fcfa351976
colour 1: degree 52, no K_3 (no K_2 among the neighbours of 0, exhaustive)
colour 2: degree 84, no K_5 (no K_4 among the neighbours of 0, exhaustive)
colour 3: degree 114, no K_7 (no K_6 among the neighbours of 0, exhaustive)
N 251 colours 3 forbidden 3,5,7
proves R(3,5,7) >= 252
PASS
PASS
```
The object, object/R_3_5_7.txt, is a circulant 3-colouring of K_251: first line "circulant 251 3", then one line "c: d d d ..." per colour listing its distances. Vertices are 0..250; edge {i, j} gets the colour of the distance (j - i) mod 251, and d and 251 - d name the same distance. The claim: colour 1 has no K_3, colour 2 no K_5, colour 3 no K_7, so R(3,5,7) >= 252.

## Rebuild the object
Needs Python 3 with python-sat (how-we-built-it/requirements.txt):
```sh
cd how-we-built-it
python3 code/split_circ.py source/kuz_7_9_251.circ 2 3 5 rebuilt.circ
python3 ../verify-it-yourself/verify_circ.py rebuilt.circ 3 5 7
```
The construction: take the (7,9) circulant on Z_251 of Kuznetsov (source/kuz_7_9_251.circ) and split its colour 2 into a K3-free part and a K5-free part, both circulant (SAT over distance classes). The third colour is the other source colour. how-we-built-it/README.md records what the rebuild gave on the run's machine.
