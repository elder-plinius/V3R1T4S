# Run it yourself

From this folder, in a fresh shell (python3 3.8 or later, standard library only, no network):

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`; the line before it begins with `RESULT` and gives the degree, the number of digits of M, the 50-digit bound, and the exact margin over the best record. The run takes about 0.1s plus the negative controls.

The checker alone:

```sh
python3 -I verify-it-yourself/shannon_check.py object table-record
```

What it does, in order: (1) compares the separation relation in object/rules.json with Definition 4 of Tandon's paper; (2) checks Definition 6 (conditions (i) and (ii)) for every substitution table the schedule uses and the pairwise separation of every terminal code; (3) recomputes the integer M and the degree d from object/schedule.json using Tandon's Lemma 1, Theorem 1 and the map Phi, after first reproducing Tandon's own d=500 integer as a known answer; (4) compares M and d with the contributor's file; (5) computes the certified integer floor of 10^50 times M^(1/d) (two exact integer powers certify it) and compares with every record in table-record/records.json, requiring a strict exceedance by exact integers (and, when affordable, the direct test that M^(d of record) is greater than (M of record)^d).

The two negative controls in run_checks.sh (a duplicated table word; one input changed by 1) must be rejected.

## The further checkers (C7 only)

`sh verify-it-yourself/run_checks.sh` also runs these (python3, standard library only, about 2 to 3 minutes in total, single thread):

```sh
python3 -I verify-it-yourself/check_g5.py object                      # Definition 2 for the 367-word base gadget G5, exhaustive
python3 -I verify-it-yourself/bpz_lean_c7_check.py object table-record  # the BPZ Lean C7 schedule: known answer
python3 -I verify-it-yourself/set_level_test.py object                 # Lemma 1, Theorem 1, sigma, Phi, S3b, K4a on real vertex sets
python3 -I verify-it-yourself/check_box_axioms.py object              # I15, I30++ independent; dimension-15 private pairs; condition (33) for Xhat30 at dimension 30
python3 -I verify-it-yourself/derive_certificates.py object --brute    # C1 to C4 from their definitions; --brute adds the word-by-word C2 enumeration
```

Each prints a line beginning with RESULT. The last line of run_checks.sh is ALL CHECKS PASS; the RESULT lines of these checkers and the one of shannon_check.py are printed just before it. Four negative controls must be rejected: a duplicated table word, a changed input (C4 plus 1), a corrupted G5 set, and a wrong ledger value for C1.
