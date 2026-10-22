context: Claude Code subagent, fresh context [Sonnet 5.5]

# reproduce: dna-gcrc-n12-d8-w6

Definition (from README.md): a list of 38 quaternary words, each of length 12 over {A,C,G,T}, exactly 6 letters from {C,G}, all distinct, pairwise Hamming distance >= 8, and Hamming(x, rc(y)) >= 8 for all x, y in the list including x = y (rc = reverse, then swap A/T and C/G).

## Method
- Folder check: The contributor's hash list verified from inside the package folder (all entries OK).
- Worked in a private copy of the package. Wrote my own checker (not shipped in this package; run with python -I) from the definition above BEFORE opening verify-it-yourself/. The checker reads object/ as raw bytes, splits on newline, and tests: line count equals the claimed 38; all words distinct; each word has length 12, only letters A,C,G,T, exactly 6 letters in {C,G}; minimum pairwise Hamming distance over all pairs i<j (full enumeration, not a sample); minimum over ALL ordered pairs (i,j), including i=j, of Hamming(x_i, rc(x_j)).
- Only then ran the author's verify-it-yourself/run_checks.sh .

## My checker output (shown below)
```
== dna-gcrc-n12-d8-w6 params n=12 d=8 w=6 rc=1 size=38
bytes 494 ends_newline True CR False
lines 38 claimed 38
min Hamming 8 min RC dist (incl x=y) 8
RESULT OK
```

## Author's run_checks.sh
Output ended with: checker verdict PASS (VALID=True, size=38, w=6); both negative controls rejected; ALL CHECKS PASS. It agrees with my checker on every property.

## Mismatches
None. Not judged here: whether the value is current or new (other skeptics).

Open questions for the panel concerning reproduction: the question in the claim record (not shipped) on whether an independent re-implementation agrees on all conditions (GC count w = floor(n/2), pairwise distance, RC distance incl. x = y) is answered: yes, agrees, all conditions hold exactly with the claimed size 38.

pass: true
