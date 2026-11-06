# How the object was built

Python 3.14 with the pinned requirements.txt (OR-Tools CP-SAT for the exact 80-point slice, numpy). From this folder:
```sh
python3 fetch_512.py                                    # one download of the FunSearch 512-cap -> checker/record_512_n8.txt
python3 code/build_n9_frame.py diag22222111 rebuilt.txt # prints "K 92 B0 OPTIMAL 80 80.0" and "wrote rebuilt.txt size 1104"
```
- code/framelib.py: point encoding, K = F_3^n minus -(B1 + B2), and the exact max-cap CP-SAT model (one clause per line
  inside the candidate set).
- code/h1_monomial.py: the search that found D (scores sign diagonals and random signed permutations M by |K(C, M C)|).
  Its n = 7 mode also needs checker/record_236_n7.txt (the 236-cap, not included here).
- code/h1_solveK.py: exact max cap inside K for given M, e.g. `python3 code/h1_solveK.py 8 diag22222111`.
- code/build_n9_frame.py: builds the 9-digit file (first digit = slice index).
- PREREG.md: the run's preregistration, frozen 2026-10-24T17:46:24Z before any lens ran. null_test: not needed
  (an explicit object judged by a deterministic exhaustive checker).
On the run's machine the rebuild returned a set identical to object/cap_1104_n9.txt.
