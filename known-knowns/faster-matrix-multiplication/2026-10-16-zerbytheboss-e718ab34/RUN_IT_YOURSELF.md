# Run it yourself

From this package folder, in a fresh shell (python3 3.8 or later, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected: sha256 matches `INDEX.csv`; `check_slp.py` prints JSON with `"VALID": true`, `"rank": 45`, `"adds_total": 161`; `brent_check.py` prints `brent_bad 0` and `BRENT_OK` (all 3136 Brent equations over Z, entries in -1,0,1); a copy with one sign flipped is rejected by both; last line `ALL CHECKS PASS`.

Individually:

```sh
python3 verify-it-yourself/check_slp.py object/2x4x7_m45_cr161_ZT_reduced.json
python3 verify-it-yourself/brent_check.py object/2x4x7_m45_cr161_ZT_reduced.json 161 45
```

To recount the reference, download Perminov's file named in `the-record-we-beat/README.md` and run `check_slp.py` on it; it reports 174 (`adds_U: 35, adds_V: 69, adds_W: 70`).

Rebuilding: `how-we-built-it/` has the scripts that walked the scheme space (`flip4.py`) and applied the canonical binary DAG exclusive-cone reduction (`dag_cone_collapse.py`); the walk is randomized, so a rerun gives a program of similar cost, while `dag_cone_collapse.py` is deterministic.
