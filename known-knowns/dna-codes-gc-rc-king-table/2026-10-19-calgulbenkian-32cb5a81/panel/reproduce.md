context: Claude Code subagent, fresh context [Sonnet 5.5]

# reproduce: dna-gcrc-n10-d7-w5

Definition (from README.md): a list of 20 quaternary words, each of length 10 over {A,C,G,T}, exactly 5 letters from {C,G}, all distinct, pairwise Hamming distance >= 7, and Hamming(x, rc(y)) >= 7 for all x, y in the list including x = y (rc = reverse, then swap A/T and C/G).

## Method
- Folder check: The contributor's hash list verified from inside the package folder (all entries OK).
- Worked in a private copy of the package. Wrote my own checker (not shipped in this package; run with python -I) from the definition above BEFORE opening verify-it-yourself/. The checker reads object/ as raw bytes, splits on newline, and tests: line count equals the claimed 20; all words distinct; each word has length 10, only letters A,C,G,T, exactly 5 letters in {C,G}; minimum pairwise Hamming distance over all pairs i<j (full enumeration, not a sample); minimum over ALL ordered pairs (i,j), including i=j, of Hamming(x_i, rc(x_j)).
- Only then ran the author's verify-it-yourself/run_checks.sh .

## My checker output (shown below)
```
== dna-gcrc-n10-d7-w5 params n=10 d=7 w=5 rc=1 size=20
bytes 220 ends_newline True CR False
lines 20 claimed 20
min Hamming 7 min RC dist (incl x=y) 7
RESULT OK
```

## Author's run_checks.sh
Output ended with: checker verdict PASS (VALID=True, size=20, w=5); both negative controls rejected; ALL CHECKS PASS. It agrees with my checker on every property.

## Mismatches
None. Not judged here: whether the value is current or new (other skeptics).

Open questions for the panel concerning reproduction: the question in the claim record (not shipped) on whether an independent re-implementation agrees on all conditions (GC count w = floor(n/2), pairwise distance, RC distance incl. x = y) is answered: yes, agrees, all conditions hold exactly with the claimed size 20.

pass: true
