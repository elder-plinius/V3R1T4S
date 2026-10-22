# Run it yourself

From this folder, in a fresh shell (python3 3.8 or later, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. The checker alone:

```sh
python3 -I verify-it-yourself/check_gram.py object/G49_p2.json 635974777627126753067532288 the-record-we-beat/records.json
```

Run time: about a minute (exact rational elimination of an 49 x 49 matrix and 18424 triple congruences).

## Rebuilding the object

The search code that produced the object is in `how-we-built-it/`; its README says which commands are recorded and which are not. The object itself is shipped in `object/`, so checking it does not need a rebuild.
