# How the object was built

Python 3, standard library only. From this folder:
```sh
python3 code/join_k5.py source/R_3_3_14.txt rebuilt.txt
python3 ../verify-it-yourself/verify_join.py rebuilt.txt 266
```
- source/R_3_3_14.txt: a circulant 3-colouring of K_266 with no K_3, K_3, K_14 (first line "circulant 266 3", then one line of distances per colour). It is the object of a separate package of the same weekend, R(3,3,14) >= 267 (submission 2026-10-25-abshalom-dayan-d46e9b16), which splits the K5-free colour of Kuznetsov's (5,14) circulant on Z_266 (arXiv:1505.07186v5, Table 2) into two triangle-free colours by the Exoo-Tatarevic method; that package shows how to rebuild it.
- code/join_k5.py: the colour-3 join. Vertices 0..265 keep the circulant colouring; five new vertices 266..270 are coloured 1 on the pentagon and 2 on the pentagram; every edge between them and the old vertices gets colour 3.
- code/check_rot.py (needs python-sat): a second exact check that does not use the block argument. It checks that rotating 0..265 (fixing 266..270) is an automorphism, so every clique meeting 0..265 can be moved to contain vertex 0; then a bitset branch and bound and CaDiCaL search the neighbourhoods of 0, and brute force covers cliques inside 266..270. Usage `python3 code/check_rot.py ../object/R_3_3_15.txt 266`. Its output on the run's machine:
```
== start 09:21:19Z
automorphism check of the rotation of 0..265 (extra vertices fixed): 0 mismatching pairs
colour 1: degree of 0 = 43; clique number through 0 = 2 (B&B, 0.0 s); K_2 in the neighbourhood of 0: UNSAT (CaDiCaL, 0.0 s); largest clique inside the extra vertices: 2
colour 2: degree of 0 = 50; clique number through 0 = 2 (B&B, 0.0 s); K_2 in the neighbourhood of 0: UNSAT (CaDiCaL, 0.0 s); largest clique inside the extra vertices: 2
colour 3: degree of 0 = 177; clique number through 0 = 14 (B&B, 30.1 s); K_14 in the neighbourhood of 0: UNSAT (CaDiCaL, 304.4 s); largest clique inside the extra vertices: 1
N 271: forbidden 3, 3, 15 absent
proves R(3,3,15) >= 272
PASS
== end 09:26:53Z
```
- code/check_fast.py with code/alpha.c (compile: `cc -O3 -o alpha alpha.c`) and code/mcheck.py: the run's general exact checkers (bitset branch and bound on the complement of each colour, and a CaDiCaL SAT search; needs python-sat). They use no structure of the object. This copy imports mcheck.py from its own folder. Their saved output on the run's machine (a colour with no line is a search that did not finish within its time cap):
```
file result/R_3_3_15.txt kind matrix N 271 colours 3 matrix sha256 051067223c60530f20b0b5dbf7206d7cca66e4a45902eeab31a76ecb0e429125
colour 1: edges 5724 degrees [2, 43] | K_3 alpha.c: RESULT NONE (exact: search completed) (0.2s) | SAT: UNSAT (no K) (0.3s)
colour 2: edges 6655 degrees [2, 50] | K_3 alpha.c: RESULT NONE (exact: search completed) (0.0s) | SAT: UNSAT (no K) (0.3s)
== end 09:46:27Z
```
(result/ was the run's own folder. The `matrix sha256` printed here is the hash of the matrix rows as the checker reads them, not of the object file.)
- PREREG.md: the run's preregistration, frozen before the object existed. null_test: not needed (an explicit object judged by deterministic exact checkers against a table value).

On the run's machine (2026-10-25T11:52:09Z) the rebuild printed "wrote rebuilt.txt N 271" and the rebuilt file was byte-identical to object/R_3_3_15.txt.
