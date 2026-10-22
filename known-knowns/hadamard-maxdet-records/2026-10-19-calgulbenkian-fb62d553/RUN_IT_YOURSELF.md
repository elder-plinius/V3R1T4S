# Run it yourself

From this folder, in a fresh shell (python3 3.8 or later, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. The checker alone:

```sh
python3 -I verify-it-yourself/check_det.py object/M117_73887205478246242985652874268409752933911041846892660492861670872395821475850942725425.txt 73887205478246242985652874268409752933911041846892660492861670872395821475850942725425 the-record-we-beat/records.json
```

It computes the determinant three independent ways (Bareiss, 14-prime CRT, Fraction elimination) and prints the normalised value, the Barba ratio and the comparison with the records. Run time: a few seconds to about a minute.

## Rebuilding the object

The search code that produced the object is in `how-we-built-it/`; its README says which commands are recorded and which are not. The object itself is shipped in `object/`, so checking it does not need a rebuild.
