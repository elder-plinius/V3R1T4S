# Run it yourself

From this folder, in a fresh shell (python3, git, make, a C compiler and network access to github.com):

```
sh verify-it-yourself/run_checks.sh
```

Expected output (about 5 minutes on an Apple M-series laptop; 161 s without the builds): step 1 prints
`matches object/cnf_spec.json`, step 2 `m=2 k=5 n=14: 2002 k-subsets checked, 0 undominated -> PASS`, step 3 `AUDIT OK`,
step 5 `s UNSATISFIABLE` and `s VERIFIED UNSAT`, and the last line is `PASS`. With tools already built:

```
CADICAL=/path/to/cadical CAKE_LPR=/path/to/cake_lpr sh verify-it-yourself/run_checks.sh
```

By hand:

```
python3 verify-it-yourself/encode_schutte.py 2 5 13 --sb global3 -o m2k5n13.cnf   # sha256 247ca74489c8144e2eca1fa1b7bfdd6c2f7f826e7deac2c46e4b3748c7069626
cadical --lrat --no-binary m2k5n13.cnf m2k5n13.lrat                                 # CaDiCaL 3.0.1: s UNSATISFIABLE
cake_lpr --CML_HEAP_SIZE=1500 --CML_STACK_SIZE=512 m2k5n13.cnf m2k5n13.lrat         # s VERIFIED UNSAT
```

cake_lpr: https://github.com/tanyongkiam/cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa
(`cc -O2 -o cake_lpr basis_ffi.c cake_lpr.S` on x86-64, `cake_lpr_arm8.S` on ARMv8). CaDiCaL:
https://github.com/arminbiere/cadical at c60730422e758ef1cebe7aeddf2dda31c996bf04 (`./configure && make`). Any proof
that cake_lpr accepts for this CNF is a certificate; a different CaDiCaL build may produce a different proof.
To rebuild the 14-vertex object: how-we-built-it/make_tests.py (function compose applied to two Paley QR7 tournaments).
