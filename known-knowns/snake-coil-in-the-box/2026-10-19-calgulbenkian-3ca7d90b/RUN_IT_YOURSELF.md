# Run it yourself

From this folder, in a fresh shell (python3 3.8 or later, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. The checker alone:

```sh
python3 -I verify-it-yourself/check_snake.py object/p3_co11_drifted_r0_Q11_740.txt 11 coil the-record-we-beat/published.json
```

It checks the induced cycle by two independent methods, prints the length, the table page's own symmetry test, the canonical class hash (when published classes are listed), and runs the same checker on the published sample records of the-record-we-beat/published.json to calibrate the length convention. The literal O(L^2) test takes up to about a minute for the Q14 objects; the canonical hash takes a few seconds to a minute.

## Rebuilding the object

The search code that produced the object is in `how-we-built-it/`; its README says which commands are recorded and which are not. The object itself is shipped in `object/`, so checking it does not need a rebuild.
