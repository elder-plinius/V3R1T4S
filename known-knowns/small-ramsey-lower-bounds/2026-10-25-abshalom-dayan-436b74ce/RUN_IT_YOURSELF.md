# Run it yourself

From this folder, in a fresh shell (Python 3, standard library only):
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output (verify-it-yourself/RECEIPTS.md has the real one):
```
sha256 436b74cecb10c8263ed5c3413d66993ce1f9d34993718f7b5bb4b31890896826
colour 1: degree 39, no K_3 (no K_2 among the neighbours of 0, exhaustive)
colour 2: degree 68, no K_5 (no K_4 among the neighbours of 0, exhaustive)
colour 3: degree 74, no K_6 (no K_5 among the neighbours of 0, exhaustive)
N 182 colours 3 forbidden 3,5,6
proves R(3,5,6) >= 183
PASS
PASS
```
The object, object/R_3_5_6.txt, is a circulant 3-colouring of K_182: first line "circulant 182 3", then one line "c: d d d ..." per colour listing its distances. Vertices are 0..181; edge {i, j} gets the colour of the distance (j - i) mod 182, and d and 182 - d name the same distance. The claim: colour 1 has no K_3, colour 2 no K_5, colour 3 no K_6, so R(3,5,6) >= 183.

## Rebuild the object
Needs Python 3 with python-sat (how-we-built-it/requirements.txt):
```sh
cd how-we-built-it
python3 code/split_circ.py source/kuz_6_9_182.circ 2 3 5 rebuilt.circ
python3 ../verify-it-yourself/verify_circ.py rebuilt.circ 3 5 6
```
The construction: take the (6,9) circulant on Z_182 of Kuznetsov (source/kuz_6_9_182.circ) and split its colour 2 into a K3-free part and a K5-free part, both circulant (SAT over distance classes). The third colour is the other source colour. how-we-built-it/README.md records what the rebuild gave on the run's machine.
