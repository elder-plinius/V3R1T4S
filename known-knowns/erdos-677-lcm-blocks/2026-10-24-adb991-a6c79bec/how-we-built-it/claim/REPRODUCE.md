# Reproduce

Requirements: Python 3 (standard library only; tested with the machine's python3), one core, about 0.2 GB of memory.
Expected time: a few minutes. The computation is deterministic and makes no network access.

```sh
cd <this claim folder>
python3 -I object/range_nCk.py 5871 > my_range_nCk_C5871.txt
cmp my_range_nCk_C5871.txt object/out/range_nCk_C5871.txt && echo IDENTICAL
tail -n 1 my_range_nCk_C5871.txt
```

Expected: `IDENTICAL`, and the last line `RESULT: no counterexample with n <= 5871 k`.

The saved output (object/out/range_nCk_C5871.txt, sha256 84b1d82fb5d2474686c60663817c5fb49709d7372987c4e044157aac61008d14)
reports: 1449175 prime-free (m, k) pairs examined (largest k 147); 7567449 candidate N after pinning; 7567420 exact
lcm comparisons; counterexamples found: [].

The mathematical reduction that makes the enumeration complete (no cap on m) is object/PROOF.md (Steps 0, S0, S1, S2,
S3). It cites two KNOWN explicit results: Rosser–Schoenfeld (1962), ψ(x) < 1.03883·x for x > 0; and Schoenfeld (1976),
a prime in (x, x(1 + 1/16597)) for x > 2010759.9.

To judge a single triple in exact integers: `python3 -I checker/check677.py n m k` (arguments in the order n, m, k; see the file header).
