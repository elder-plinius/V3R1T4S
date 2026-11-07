# How the object was built

Python 3 with python-sat (requirements.txt; CaDiCaL inside). From this folder:
```sh
python3 code/split_circ.py source/kuz_5_14_266.circ 1 3 3 rebuilt.circ
python3 ../verify-it-yourself/verify_circ.py rebuilt.circ 3 3 14
```
- source/kuz_5_14_266.circ: the (5,14) circulant on Z_266 of Eugene Kuznetsov (arXiv:1505.07186v5, Table 2), transcribed by the run from the paper's table as a two-colour circulant file (colour 1 = the printed distance set, colour 2 = the other distances).
- code/split_circ.py: splits colour 1 of the source into a K3-free part (new colour 1) and a K3-free part (new colour 2), both circulant: one SAT variable per distance class, complete triangle clauses, lazy clique clauses from an exact search through vertex 0, and an exact final check. Colour 3 of the object is the other source colour, unchanged. code/circ.py: file reader and adjacency output.
- code/check_fast.py with code/alpha.c (compile: `cc -O3 -o alpha alpha.c`): the run's second exact checker (bitset branch and bound plus CaDiCaL via pysat returning UNSAT for each colour (no DRAT/LRAT certificate); it uses code/mcheck.py, the run's reference checker, for parsing only, and this copy imports it from its own folder instead of the run's checker folder); usage `python3 code/check_fast.py ../object/R_3_3_14.txt 3 3 14`.
- PREREG.md: the run's preregistration, frozen before the object existed. null_test: not needed (an explicit object judged by deterministic exact checkers against a table value).

On the run's machine (2026-10-25T08:43:04Z) the rebuild printed "RESULT SAT" and gave colour classes identical to those of object/R_3_3_14.txt (python-sat 1.9.dev17). The object file itself is the split output rewritten in a clean format (first line `circulant N 3`, then one line per colour).
