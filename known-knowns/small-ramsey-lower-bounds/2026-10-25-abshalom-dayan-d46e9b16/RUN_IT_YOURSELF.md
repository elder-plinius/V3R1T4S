# Run it yourself

From this folder, in a fresh shell (Python 3, standard library only):
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output (verify-it-yourself/RECEIPTS.md has the real one):
```
sha256 d46e9b167a93492eb02cabc1d2d9f81c975ea68698cb55944a4afac2463034ba
colour 1: degree 43, no K_3 (no K_2 among the neighbours of 0, exhaustive)
colour 2: degree 50, no K_3 (no K_2 among the neighbours of 0, exhaustive)
colour 3: degree 172, no K_14 (no K_13 among the neighbours of 0, exhaustive)
N 266 colours 3 forbidden 3,3,14
proves R(3,3,14) >= 267
PASS
PASS
```
The object, object/R_3_3_14.txt, is a circulant 3-colouring of K_266: first line "circulant 266 3", then one line "c: d d d ..." per colour listing its distances. Vertices are 0..265; edge {i, j} gets the colour of the distance (j - i) mod 266, and d and 266 - d name the same distance. The claim: colour 1 has no K_3, colour 2 no K_3, colour 3 no K_14, so R(3,3,14) >= 267.

## Rebuild the object
Needs Python 3 with python-sat (how-we-built-it/requirements.txt):
```sh
cd how-we-built-it
python3 code/split_circ.py source/kuz_5_14_266.circ 1 3 3 rebuilt.circ
python3 ../verify-it-yourself/verify_circ.py rebuilt.circ 3 3 14
```
The construction: take the (5,14) circulant on Z_266 of Kuznetsov (source/kuz_5_14_266.circ) and split its colour 1 into a K3-free part and a K3-free part, both circulant (SAT over distance classes). The third colour is the other source colour. how-we-built-it/README.md records what the rebuild gave on the run's machine.
