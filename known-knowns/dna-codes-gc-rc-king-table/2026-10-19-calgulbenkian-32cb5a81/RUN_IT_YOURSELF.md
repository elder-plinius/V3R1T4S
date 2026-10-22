# Run it yourself

From this package folder, in a fresh shell (python3 3.8 or later, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. The checker alone:

```sh
python3 -I verify-it-yourself/check_dna.py object/gc_rc_10_7_5.txt 10 7 gcrc
```

Expected: every condition line reads PASS and the last line is a JSON record with VALID true and size 20.

How to rebuild the object: the object is a plain list of 20 words, one per line. It was produced by the contributor's search program (how-we-built-it/dna_search.c, see how-we-built-it/README.md); the exact command line that produced it was not recorded in the snapshot, so a rebuild is not promised to give the same file. The check above does not depend on how the file was found.
