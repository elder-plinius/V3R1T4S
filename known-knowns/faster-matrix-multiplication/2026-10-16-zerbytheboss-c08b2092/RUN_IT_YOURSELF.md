# Run it yourself

From this package folder, in a fresh shell (python3 3.8 or later, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected: sha256 matches `INDEX.csv`; `check_slp.py` prints JSON with `"VALID": true`, `"rank": 47`, `"adds_total": 177`; `brent_check.py` prints `brent_bad 0` and `BRENT_OK` (all 3600 Brent equations over Z, entries in -1,0,1); a copy with one sign flipped is rejected by both; last line `ALL CHECKS PASS`.

Individually:

```sh
python3 verify-it-yourself/check_slp.py object/2x5x6_m47_cr177_ZT_reduced.json
python3 verify-it-yourself/brent_check.py object/2x5x6_m47_cr177_ZT_reduced.json 177 47
```

To recount the reference, download Perminov's file named in `the-record-we-beat/README.md` and run `check_slp.py` on it; it reports 181 (`adds_U: 40, adds_V: 65, adds_W: 76`).
