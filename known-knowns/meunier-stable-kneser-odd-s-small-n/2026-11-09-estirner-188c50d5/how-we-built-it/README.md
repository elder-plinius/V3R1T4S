# How it was built

- code/gen_cnf.py: the CNF generator (also shipped as verify-it-yourself/gen_cnf.py). Vertices are the 5-stable
  3-subsets of [n] in lexicographic order; x(v,c) = v*C + c + 1; at-least-one-colour clauses, one clause per edge and
  colour, then units fixing colour j-1 on Q_j = {j, j+t, j+2t}, t = floor(n/3), j = 1..min(t, C).
- code/run_all_sat.sh: calibration on (k,s) = (3,3), n = 9..14 (the cases arXiv 2607.12912 proves), then (3,5),
  n = 17..22: CaDiCaL 3.0.1 with DRAT output for C = n - 11, drat-trim, and a SAT run for C + 1 = n - 10 colours.
  outputs/sat_drat_v2_run_all.txt (n = 9..21) and outputs/n22.txt.
- Shipping the proofs (n = 17..21): drat-trim -l (core lemmas) twice, code/drat_to_binary.py, xz -9e; each shipped file
  re-verified by drat-trim after decompression. The n = 22 proof (752 MB) is not shipped; CaDiCaL regenerates it
  identically (object/proof_n22_c11_not_shipped.txt).
- code/exact_colour.py and code/run_all_exact.sh: an independent exact colouring search (DSATUR branch and bound, no
  SAT solver). outputs/own_exact_run_all.txt: agrees on every calibration case and on n = 17..21.
- PREREG.md, PREREG.v2.md (larger allowed clique, so the n = 21 proof fits under 1 MB) and PREREG.v3.md (n = 22 added
  after the first panel's novelty check showed which n are open).
Tools: CaDiCaL 3.0.1 (https://github.com/arminbiere/cadical, tag rel-3.0.1), drat-trim (https://github.com/marijnheule/drat-trim,
commit 2e3b2dc0ecf9), Python 3 standard library.
