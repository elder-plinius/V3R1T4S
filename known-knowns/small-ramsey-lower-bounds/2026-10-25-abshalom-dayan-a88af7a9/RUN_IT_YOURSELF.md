# Run it yourself

From this folder, in a fresh shell (Python 3, standard library only):
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output (verify-it-yourself/RECEIPTS.md has the real one):
```
sha256 a88af7a9fb8fc8eb0ddf226628db6f59df6c1fb8504ed3ec80d2eeaf972a64cd
colour 1: degree 26, no K_3 (no K_2 among the neighbours of 0, exhaustive)
colour 2: degree 27, no K_3 (no K_2 among the neighbours of 0, exhaustive)
colour 3: degree 78, no K_9 (no K_8 among the neighbours of 0, exhaustive)
N 132 colours 3 forbidden 3,3,9
proves R(3,3,9) >= 133
PASS
PASS
```
The object, object/R_3_3_9.txt, is a circulant 3-colouring of K_132: first line "circulant 132 3", then one line "c: d d d ..." per colour listing its distances. Vertices are 0..131; edge {i, j} gets the colour of the distance (j - i) mod 132, and d and 132 - d name the same distance. The claim: colour 1 has no K_3, colour 2 no K_3, colour 3 no K_9, so R(3,3,9) >= 133.

## Rebuild the object
Needs Python 3 with python-sat (how-we-built-it/requirements.txt):
```sh
cd how-we-built-it
python3 code/split_circ.py source/kuz_5_9_132.circ 1 3 3 rebuilt.circ
python3 ../verify-it-yourself/verify_circ.py rebuilt.circ 3 3 9
```
The construction: take the (5,9) circulant on Z_132 of Kuznetsov (source/kuz_5_9_132.circ) and split its colour 1 into a K3-free part and a K3-free part, both circulant (SAT over distance classes). The third colour is the other source colour. how-we-built-it/README.md records what the rebuild gave on the run's machine.
