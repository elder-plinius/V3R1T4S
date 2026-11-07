# Run it yourself

From this package folder, in a fresh shell (needs python3 and cc, no network):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (about 17 seconds on one core):

```
claimed n=31 k=17 d=11; computed rank(G)=17
k=17 n=31 rank=17
W=1: no nonzero codeword of weight <= 1 (all 31 subsets)
...
W=10: no nonzero codeword of weight <= 10 (all 44352165 subsets)
W=11 complete for all W'<11; first nonzero codeword supported in a 11-set after 229 subsets
d=11 witness_weight=11 witness=1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0
m3_mindist: W=10: no nonzero codeword of weight <= 10 (all 44352165 subsets); d=11
witness: weight 11, nonzero codeword of the row space: True
computed n=31 k=17 d=11; claimed n=31 k=17 d=11
PASS
```

Why this is exact: every nonzero codeword of weight at most 10 is supported inside some 10-subset T of the 31
coordinates. With G in systematic form on an information set I, such a codeword exists for T iff the submatrix of
the redundancy part with rows I∩T and columns outside T has a nonzero left-kernel vector. The program examines all
C(31,10) = 44352165 subsets exactly over GF(9) and finds none, then prints a codeword of weight 11, which the Python
part checks is a combination of the rows of G.

Rebuild the object from its construction:

```sh
python3 how-we-built-it/build_code.py rebuilt.json
shasum -a 256 rebuilt.json object/code_q9_n31_k17_d11.json   # both f08aa6475f164ffa1ed1f41f5c63eb0f5516b74c34c1b198da8c83ae1a7da5dd
```

A second independent exact check, from the dual side:

```sh
python3 -c "import json;o=json.load(open('object/code_q9_n31_k17_d11.json'));print(o['k'],o['n']);[print(*r) for r in o['G']]" > code.txt
# smallest set of linearly dependent parity-check columns (a few seconds)
cc -O2 -o hdep how-we-built-it/hdep.c && ./hdep 11 < code.txt
# expected: rank=17 (k=17 n=31) / nodes=75973418 / dependent_min=11 d=11
```

How the tail was found: `how-we-built-it/gen_tail.py` computes the exact coset table (minimum weight of each coset of
C(D,16P) in C(D,19P), capped at 11) with hdep, and `how-we-built-it/tailg.c` searches 4-point multisets of PG(2,9) such
that every hyperplane c-perp holds at most 4 - max(0, 11 - mu(c)) of them. Its output line for this code was
`16,19,4,31,17 nodes=15 sols=1 0 1 2 13`; `build_tail.py 16 19 0,1,2,13 OUT` turns it into the matrix.

Named but not shipped: some files name run-workspace items that are not in this package and are not needed to check
the claim: three run folders named by their date and time (panel/gate.md, how-we-built-it/PREREG.md), the run's dossier and NEXT_RUN.md (how-we-built-it/PREREG.md), out/candidates.txt (gen_tail.py's CAND input), constructor/code/tailc.c (the earlier tail search that tailg.c generalizes), the self-break step (how-we-built-it/PREREG.md, panel/gate.md), and the skeptics' working folders (panel/).
