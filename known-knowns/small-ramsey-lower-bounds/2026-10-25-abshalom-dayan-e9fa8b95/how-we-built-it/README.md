# How the object was built

Python 3 with python-sat (requirements.txt; CaDiCaL inside). From this folder:
```sh
python3 code/split_circ.py source/kuz_7_7_153.circ 2 3 4 rebuilt.circ
python3 ../verify-it-yourself/verify_circ.py rebuilt.circ 3 4 7
```
- source/kuz_7_7_153.circ: the (7,7) circulant on Z_153 of Eugene Kuznetsov (arXiv:1505.07186v5, Table 2), transcribed by the run from the paper's table as a two-colour circulant file (colour 1 = the printed distance set, colour 2 = the other distances).
- code/split_circ.py: splits colour 2 of the source into a K3-free part (new colour 1) and a K4-free part (new colour 2), both circulant: one SAT variable per distance class, complete triangle clauses, lazy clique clauses from an exact search through vertex 0, and an exact final check. Colour 3 of the object is the other source colour, unchanged. code/circ.py: file reader and adjacency output.
- code/check_fast.py with code/alpha.c (compile: `cc -O3 -o alpha alpha.c`): the run's second exact checker (bitset branch and bound plus a CaDiCaL UNSAT answer for each colour, with no proof certificate saved; it uses code/mcheck.py, the run's reference checker, for parsing only, and this copy imports it from its own folder instead of the run's checker folder); usage `python3 code/check_fast.py ../object/R_3_4_7.txt 3 4 7`.
- PREREG.md: the run's preregistration, frozen before the object existed. null_test: not needed (an explicit object judged by deterministic exact checkers against a table value).

On the run's machine (2026-10-25T11:16:52Z) the rebuild printed "RESULT SAT" and gave colour classes identical to those of object/R_3_4_7.txt (python-sat 1.9.dev17). The object file itself is the split output rewritten in a clean format (first line `circulant 153 3`, then one line of distances per colour).
