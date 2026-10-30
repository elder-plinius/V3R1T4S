# Run it yourself

From this package folder, in a fresh shell (needs python3 and cc, no network):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (about 1 second on one core):

```
claimed n=29 k=19 d=8; computed rank(G)=19
k=19 n=29 rank=19
W=1: no nonzero codeword of weight <= 1 (all 29 subsets)
...
W=7: no nonzero codeword of weight <= 7 (all 1560780 subsets)
W=8 complete for all W'<8; first nonzero codeword supported in a 8-set after 253 subsets
d=8 witness_weight=8 witness=2 2 2 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2
m3_mindist: W=7: no nonzero codeword of weight <= 7 (all 1560780 subsets); d=8
witness: weight 8, nonzero codeword of the row space: True
computed n=29 k=19 d=8; claimed n=29 k=19 d=8
PASS
```

Why this is exact: every nonzero codeword of weight at most 7 is supported inside some 7-subset T of the 29
coordinates. With G in systematic form on an information set I, such a codeword exists for T iff the submatrix of
the redundancy part with rows I∩T and columns outside T has a nonzero left-kernel vector. The program examines all
C(29,7) = 1560780 subsets exactly over GF(9) and finds none, then prints a codeword of weight 8, which the Python
part checks is a combination of the rows of G.

Rebuild the object from its construction:

```sh
python3 how-we-built-it/build_code.py rebuilt.json
shasum -a 256 rebuilt.json object/code_q9_n29_k19_d8.json   # both 912c80c8ee946bc6021522350a436fb9510b39e1565175a0a0fc380d0216f9e7
```

Two more independent exact checks, from the dual side:

```sh
python3 -c "import json;o=json.load(open('object/code_q9_n29_k19_d8.json'));print(o['k'],o['n']);[print(*r) for r in o['G']]" > code.txt
# smallest set of linearly dependent parity-check columns (under a second)
cc -O2 -o hdep how-we-built-it/hdep.c && ./hdep 8 < code.txt
# expected: rank=19 (k=19 n=29) / nodes=2182648 / dependent_min=8 d=8
# all 9^10 dual codewords, then the MacWilliams identities (about 10 seconds)
cc -O2 -o dualenum how-we-built-it/dualenum.c && ./dualenum < code.txt > dual.txt && python3 how-we-built-it/macwilliams.py dual.txt 9
# expected first lines:
#   k=19 n=29 m=10 dual_words=3486784401
#   sum A = 1350851717672992089 = 9^k
#   A_1..A_7 = 0; A_8 = 12456; minimum distance d = 8
```

Named but not shipped: some files name run-workspace items that are not in this package and are not needed to check the
claim: the Brouwer-Zimmermann program bz9t (the fourth method in panel/gate.md and how-we-built-it/PREREG.v2.md),
fetch_cells.sh and started_reproduce.txt (panel/gate.md), constructor/out/plain_d*.txt (how-we-built-it/candidates.py),
out/candidates.txt (gen_tail.py), data/ (parse_range.py, PREREG.v2.md), constructor/code/tailc.c (tailg.c), target.md
and scout.md (the two PREREG files), attempts/, NEXT_RUN.md and data/prs_0151_*.json (PREREG.v2.md), and the run folder
named by its date and time (panel/gate.md, the PREREG files). The PREREG files say "verbatim" but quote the criterion
in shortened form; the exact text is codetables-binary-linear's success_criterion in bank/targets.json of the V3R1T4S
repository.
