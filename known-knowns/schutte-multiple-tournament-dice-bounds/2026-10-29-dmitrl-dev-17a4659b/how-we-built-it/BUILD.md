# How this was built: commands

Tools: CaDiCaL 3.0.1 (github.com/arminbiere/cadical c60730422e758ef1cebe7aeddf2dda31c996bf04, `./configure && make`),
kissat 4.0.4 (github.com/arminbiere/kissat 8af8e56f174b778aef3aa45af9f739b2a5f492c2), cake_lpr
(github.com/tanyongkiam/cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, `cc -O2 -o cake_lpr basis_ffi.c cake_lpr_arm8.S`
on ARMv8 or `cake_lpr.S` on x86-64), python-sat 1.9.dev17 (only for sb_audit.py and test scripts that use it).

1. Base encoding on the starred cells of Figure 7 (m < k+1), SAT at f(m,k) and UNSAT at f(m,k) - 1:
   `python3 calibrate.py 300` (needs encode_schutte.py, check_schutte.py and a cadical binary at the path in the script).
2. Maximum-degree cubes: `python3 cubes.py m k n seconds cadical [D-list]`, e.g. `cubes.py 2 5 13 3000 cadical 12,11,10,9,8,7,6,5`.
3. Certificate CNF: `python3 encode_schutte.py 2 5 13 --sb global3 -o m2k5n13_global3.cnf`; solve with
   `sh solve_lrat_zstd.sh <dir> m2k5n13_global3 3600` (CaDiCaL `--lrat --no-binary`, proof streamed into zstd) and
   check with `sh check_lrat_zstd.sh <dir> m2k5n13_global3 1500` (proof streamed into cake_lpr).
4. Other variants and tests: `encode_schutte.py ... --sb none|dom0|maxdeg --D d|global|gsort|global2|global3`;
   `test_global2.py`, `test_global3.py` (variants on known cells); `encode_alt.py` + `test_alt.py` (a second,
   separately written encoding, run with kissat); `sb_audit.py cnf m k n trials seed` (randomised test of the added
   clauses); `make_tests.py` (checker test inputs, including the 14-vertex composition).
