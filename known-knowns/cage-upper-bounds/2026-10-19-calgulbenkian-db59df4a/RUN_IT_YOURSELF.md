# Run it yourself

From this folder, in a fresh shell (python3 3.8 or later, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. The checker alone:

```sh
python3 -I verify-it-yourself/check_mixed.py object/mixed_z2_r9_g6_N294.json
```

It rebuilds the graph from the generators, compares with the stored lists, checks regularity, finds the shortest cycle up to length 5 under the forward-arc convention (expected: none), and prints the direction-blind girth (expected: 4). Run time: seconds to about a minute.

## Rebuilding the object

The search code that produced the object is in `how-we-built-it/`; its README says which commands are recorded and which are not. The object itself is shipped in `object/`, so checking it does not need a rebuild.
