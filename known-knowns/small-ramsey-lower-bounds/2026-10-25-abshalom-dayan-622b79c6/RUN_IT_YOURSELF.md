# Run it yourself

From this folder, in a fresh shell (Python 3, standard library only):
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output (verify-it-yourself/RECEIPTS.md has the real one):
```
sha256 622b79c6646d2617cd7f0b74c224ad3d5bd6cb856c6824ace5a5e30664461270
colour 1: degree 37, no K_3 (no K_2 among the neighbours of 0, exhaustive)
colour 2: degree 30, no K_3 (no K_2 among the neighbours of 0, exhaustive)
colour 3: degree 114, no K_11 (no K_10 among the neighbours of 0, exhaustive)
N 182 colours 3 forbidden 3,3,11
proves R(3,3,11) >= 183
PASS
PASS
```
The object, object/R_3_3_11.txt, is a circulant 3-colouring of K_182: first line "circulant 182 3", then one line "c: d d d ..." per colour listing its distances. Vertices are 0..181; edge {i, j} gets the colour of the distance (j - i) mod 182, and d and 182 - d name the same distance. The claim: colour 1 has no K_3, colour 2 no K_3, colour 3 no K_11, so R(3,3,11) >= 183.

## Rebuild the object
Needs Python 3 with python-sat (how-we-built-it/requirements.txt):
```sh
cd how-we-built-it
python3 code/split_circ.py source/kuz_5_11_182.circ 1 3 3 rebuilt.circ
python3 ../verify-it-yourself/verify_circ.py rebuilt.circ 3 3 11
```
The construction: take the (5,11) circulant on Z_182 of Kuznetsov (source/kuz_5_11_182.circ) and split its colour 1 into a K3-free part and a K3-free part, both circulant (SAT over distance classes). The third colour is the other source colour. how-we-built-it/README.md records what the rebuild gave on the run's machine.
