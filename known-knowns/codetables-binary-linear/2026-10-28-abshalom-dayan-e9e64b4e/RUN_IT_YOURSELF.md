# Run it yourself

From this package folder, in a fresh shell (needs python3 and cc, no network):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (about 8 seconds on one core):

```
claimed n=32 k=19 d=10; computed rank(G)=19
k=19 n=32 rank=19
W=1: no nonzero codeword of weight <= 1 (all 32 subsets)
...
W=9: no nonzero codeword of weight <= 9 (all 28048800 subsets)
W=10 complete for all W'<10; first nonzero codeword supported in a 10-set after 23 subsets
d=10 witness_weight=10 witness=1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
m3_mindist: W=9: no nonzero codeword of weight <= 9 (all 28048800 subsets); d=10
witness: weight 10, nonzero codeword of the row space: True
computed n=32 k=19 d=10; claimed n=32 k=19 d=10
PASS
```

Why this is exact: every nonzero codeword of weight at most 9 is supported inside some 9-subset T of the 32
coordinates. With G in systematic form on an information set I, such a codeword exists for T iff the submatrix of
the redundancy part with rows I∩T and columns outside T has a nonzero left-kernel vector. The program examines all
C(32,9) = 28048800 subsets exactly over GF(9) and finds none, then prints a codeword of weight 10, which the Python
part checks is a combination of the rows of G.

Rebuild the object from its construction:

```sh
python3 how-we-built-it/build_code.py rebuilt.json
shasum -a 256 rebuilt.json object/code_q9_n32_k19_d10.json   # both e9e64b4eef94a2fc783bf8e027b849d0d931a3641607aa98121561a77cb77965
```

A second independent exact check, from the dual side:

```sh
python3 -c "import json;o=json.load(open('object/code_q9_n32_k19_d10.json'));print(o['k'],o['n']);[print(*r) for r in o['G']]" > code.txt
# smallest set of linearly dependent parity-check columns (a few seconds)
cc -O2 -o hdep how-we-built-it/hdep.c && ./hdep 10 < code.txt
# expected: rank=19 (k=19 n=32) / nodes=43081995 / dependent_min=10 d=10
```

How the tail was found: `how-we-built-it/gen_tail.py` computes the exact coset table (minimum weight of each coset of
C(D,17P) in C(D,21P), capped at 10) with hdep, and `how-we-built-it/tailg.c` searches 5-point multisets of PG(3,9) such
that every hyperplane c-perp holds at most 5 - max(0, 10 - mu(c)) of them. Its output line for this code was
`17,21,5,32,19 nodes=1882 sols=1 0 2 11 22 588` (point indices in lexicographic order, first nonzero coordinate 1);
`build_tail.py 17 21 0,2,11,22,588 OUT` turns them into the matrix.

Named but not shipped: some files name run-workspace items that are not in this package and are not needed to check the claim: the run folder named by its date and time (panel/gate.md, how-we-built-it/PREREG.md), NEXT_RUN.md (PREREG.md), out/candidates.txt (the earlier run's candidate list, gen_tail.py's CAND input), constructor/code/tailc.c (the earlier tail search that tailg.c generalises), the self-break step (PREREG.md), and the skeptics' working folders (panel/).
