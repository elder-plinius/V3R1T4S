# Run it yourself

From this folder, in a fresh shell (Python 3, standard library only):
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output (verify-it-yourself/RECEIPTS.md has the real one):
```
sha256 e9fa8b95605e0f8e8d7b020855f7905ff9c02269c9d49a48abd725e7858d6a40
colour 1: degree 36, no K_3 (no K_2 among the neighbours of 0, exhaustive)
colour 2: degree 42, no K_4 (no K_3 among the neighbours of 0, exhaustive)
colour 3: degree 74, no K_7 (no K_6 among the neighbours of 0, exhaustive)
N 153 colours 3 forbidden 3,4,7
proves R(3,4,7) >= 154
PASS
PASS
```
The object, object/R_3_4_7.txt, is a circulant 3-colouring of K_153: first line "circulant 153 3", then one line "c: d d d ..." per colour listing its distances. Vertices are 0..152; edge {i, j} gets the colour of the distance (j - i) mod 153, and d and 153 - d name the same distance. The claim: colour 1 has no K_3, colour 2 no K_4, colour 3 no K_7, so R(3,4,7) >= 154.

## Rebuild the object
Needs Python 3 with python-sat (how-we-built-it/requirements.txt):
```sh
cd how-we-built-it
python3 code/split_circ.py source/kuz_7_7_153.circ 2 3 4 rebuilt.circ
python3 ../verify-it-yourself/verify_circ.py rebuilt.circ 3 4 7
```
The construction: take the (7,7) circulant on Z_153 of Kuznetsov (source/kuz_7_7_153.circ) and split its colour 2 into a K3-free part and a K4-free part, both circulant (SAT over distance classes). The third colour is the other source colour. how-we-built-it/README.md records what the rebuild gave on the run's machine.
