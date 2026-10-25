# Commands

The fast check is pure Python and does not compile these files. They are
the search programs from the research record.

```
gcc -O2 -o search search.c
gcc -O2 -o vf2 vf2.c
g++ -O2 -o verify_fixed verify_fixed.cpp
```

`search` and `vf2` take the largest odd magnitude and the target length.
The historical non-existence runs (length 16 up to magnitude 75, length 18
up to 93, and lengths 20 through 48 up to 95) are what the saved logs
record. They are not repeated by `sh verify-it-yourself/run_checks.sh`.

There is no PREREG file in the research record. A term was kept only after
an independent program reproduced the published a(5), a(6), and a(7) and
the exhaustive runs for the new index came back NONE below the witness.
