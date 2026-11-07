# Run it yourself

From this folder, in a fresh shell (Python 3, standard library only):
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output (verify-it-yourself/RECEIPTS.md has the real one):
```
sha256 eeb47c398be7c450cadf8d9b5939d4996761911a1ddba276e6d820b87fd0db1b
colour 1: degree 35, no K_3 (no K_2 among the neighbours of 0, exhaustive)
colour 2: degree 40, no K_3 (no K_2 among the neighbours of 0, exhaustive)
colour 3: degree 126, no K_12 (no K_11 among the neighbours of 0, exhaustive)
N 202 colours 3 forbidden 3,3,12
proves R(3,3,12) >= 203
PASS
PASS
```
The object, object/R_3_3_12.txt, is a circulant 3-colouring of K_202: first line "circulant 202 3", then one line "c: d d d ..." per colour listing its distances. Vertices are 0..201; edge {i, j} gets the colour of the distance (j - i) mod 202, and d and 202 - d name the same distance. The claim: colour 1 has no K_3, colour 2 no K_3, colour 3 no K_12, so R(3,3,12) >= 203.

## Rebuild the object
Needs Python 3 with python-sat (how-we-built-it/requirements.txt) and the source set, which is not shipped: re-type the (5,12) set on Z_202 from Table 2 of Kuznetsov, arXiv:1505.07186v5 (https://arxiv.org/abs/1505.07186), into how-we-built-it/source/kuz_5_12_202.circ, in the exact format given in how-we-built-it/README.md, and check `shasum -a 256 how-we-built-it/source/kuz_5_12_202.circ` against f7c231e0cc93c1a070e694146c2f801b3946a0129c48a145ff24d6dd965ca582 (the sha256 of the transcription used for this object). Then:
```sh
cd how-we-built-it
python3 code/split_circ.py source/kuz_5_12_202.circ 1 3 3 rebuilt.circ
python3 ../verify-it-yourself/verify_circ.py rebuilt.circ 3 3 12
```
The construction: take the (5,12) circulant on Z_202 of Kuznetsov (your re-typed source/kuz_5_12_202.circ; the rebuild runs on your copy, not on a shipped file) and split its colour 1 into a K3-free part and a K3-free part, both circulant (SAT over distance classes). The third colour is the other source colour. how-we-built-it/README.md records what the rebuild gave on the run's machine.
