# How the object was built

Python 3 with python-sat (requirements.txt; CaDiCaL inside). From this folder:
```sh
# first create source/kuz_5_11_182.circ from Table 2 (see below)
python3 code/split_circ.py source/kuz_5_11_182.circ 1 3 3 rebuilt.circ
python3 ../verify-it-yourself/verify_circ.py rebuilt.circ 3 3 11
```
- source/kuz_5_11_182.circ (not shipped): the (5,11) circulant on Z_182 of Eugene Kuznetsov, arXiv:1505.07186 (https://arxiv.org/abs/1505.07186), v5, Table 2. The run transcribed the printed set from the table into a two-colour circulant file; that file is not part of this package. To rebuild, re-type the set from Table 2 into how-we-built-it/source/kuz_5_11_182.circ (create the folder) and compare `shasum -a 256 source/kuz_5_11_182.circ` with the transcription's sha256, 29393c1bea81a0d78a2980ef7a401b77ba42bcf2ca679457ed80d269ab7f1643. If the hashes differ, the script still works on your copy, but check your typing against Table 2 first.

Format of the re-typed file (the sha256 above is of exactly these bytes):
The file is plain ASCII text with Unix line endings (LF), 4 lines, each ending in LF (including the last), no trailing spaces, no blank lines, exactly as follows:

```
# Kuznetsov arXiv:1505.07186v5 Table 2, (5,11) on 182: colour 1 = printed set S, colour 2 = the other distances
circulant 182 2
1: 4 5 7 13 21 22 29 30 31 36 39 40 43 48 50 54 61 63 64 65 66 68 70 74 75 77 80 81 82 83 84 87 88 91
2: 1 2 3 6 8 9 10 11 12 14 15 16 17 18 19 20 23 24 25 26 27 28 32 33 34 35 37 38 41 42 44 45 46 47 49 51 52 53 55 56 57 58 59 60 62 67 69 71 72 73 76 78 79 85 86 89 90
```
Line 1 is a comment (the scripts ignore lines starting with #). Line 2 is the header `circulant 182 2`. Line 3 lists the distances of the printed set S in Table 2, in increasing order, separated by single spaces. Line 4 lists, in increasing order, every distance in 1..91 that is not in S. A distance d and 182 - d name the same distance, so only 1..91 are listed. The scripts read any spacing and comment text, but the sha256 above is only reproduced by this exact byte layout.
- code/split_circ.py: splits colour 1 of the source into a K3-free part (new colour 1) and a K3-free part (new colour 2), both circulant: one SAT variable per distance class, complete triangle clauses, lazy clique clauses from an exact search through vertex 0, and an exact final check. Colour 3 of the object is the other source colour, unchanged. code/circ.py: file reader and adjacency output.
- code/check_fast.py with code/alpha.c (compile: `cc -O3 -o alpha alpha.c`): the run's second exact checker (bitset branch and bound plus CaDiCaL via pysat returning UNSAT for each colour (no DRAT/LRAT certificate); it uses code/mcheck.py, the run's reference checker, for parsing only, and this copy imports it from its own folder instead of the run's checker folder); usage `python3 code/check_fast.py ../object/R_3_3_11.txt 3 3 11`.
- PREREG.md: the run's preregistration, frozen before the object existed. null_test: not needed (an explicit object judged by deterministic exact checkers against a table value).

On the run's machine (2026-10-25T08:51:25Z) the rebuild printed "RESULT SAT" and gave colour classes identical to those of object/R_3_3_11.txt (python-sat 1.9.dev17). The object file itself is the split output rewritten in a clean format (first line `circulant N 3`, then one line per colour).
