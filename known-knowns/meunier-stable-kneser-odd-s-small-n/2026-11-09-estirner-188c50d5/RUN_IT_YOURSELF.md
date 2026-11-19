# Run it yourself

Tools: Python 3; drat-trim (one C file: `gcc -O2 -o drat-trim drat-trim.c` from https://github.com/marijnheule/drat-trim);
CaDiCaL 3.0.1 (https://github.com/arminbiere/cadical/archive/refs/tags/rel-3.0.1.tar.gz, sha256
0a8ea563b5a25f5aa064634814edab45cc0e45111ea0f5d412a565f806fd7e11; `./configure && make`).

From this folder:

    DRAT_TRIM=/path/to/drat-trim CADICAL=/path/to/cadical sh verify-it-yourself/run_checks.sh

Expected (10-12 minutes, almost all n = 22): one line per n = 17..22 ending 'proof s VERIFIED' (n = 22: 'regenerated
(exit 20, sha256 d24a47fc195dbc48 as recorded), s VERIFIED'), then PASS. See verify-it-yourself/RECEIPTS.md.

By hand, for one n: python3 verify-it-yourself/gen_cnf.py 17 3 5 6 n17.cnf; xz -dc object/proof_n17_c6.drat.xz > p;
drat-trim n17.cnf p   ->  s VERIFIED.

Rebuild everything: TOOLS_BIN=<folder with cadical and drat-trim> sh how-we-built-it/code/run_all_sat.sh (run from
how-we-built-it/code; minutes, n = 22 about 5 minutes).
