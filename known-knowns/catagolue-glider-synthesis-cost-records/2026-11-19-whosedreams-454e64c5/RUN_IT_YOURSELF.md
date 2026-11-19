# Run it yourself

## Standard-library check (no installs)
From this folder, in a fresh shell:
```
sh verify-it-yourself/run_checks.sh
```
Expected output (also in verify-it-yourself/RECEIPTS.md):
```
gen0: population 70, 14 components, all gliders
rewind T=3612: ok
rewind T=4624: ok
forward: exact repeat from generation 1819, period 1, population 31
final object: matches xs31_g8e1ugmmzd553w643 exactly, nothing else live
cost: 14 gliders < table cost 60
result: {'ok': True, 'target': 'xs31_g8e1ugmmzd553w643', 'n_gliders': 14, 'rewind_ok': True, 'periodic_from': 1819, 'period': 1, 'final_population': 31, 'final_matches_target': True, 'table_cost': 60}
PASS
```
(The `result:` line is the checker's summary dictionary; the last line is PASS.) About a minute or less on a laptop.

Optional drop-one controls (not part of run_checks.sh): `python3 verify-it-yourself/life_check.py --rle object/xs31_g8e1ugmmzd553w643.rle --target xs31_g8e1ugmmzd553w643 --table-cost 60 --controls`

## Live cost
Open https://catagolue.hatsya.com/object/xs31_g8e1ugmmzd553w643/b3s23 and read the `#CSYNTH xs31_g8e1ugmmzd553w643 costs N gliders` line. The claim
holds while N is greater than 14 and at least 60.

## lifelib route (as the finder ran it)
Needs python-lifelib 2.5.6 and a Shinjuku checkout (https://gitlab.com/parclytaxel/Shinjuku, commit
3615babf001146507a1e9ec901cb3eabba9f5fd0, 2026-10-27) importable as the `shinjuku` package:
```
python3 how-we-built-it/code/verify_synthesis.py --rle object/xs31_g8e1ugmmzd553w643.rle --target xs31_g8e1ugmmzd553w643
```
Expected: JSON with "ok": true, "n_gliders": 14, "rewind_ok": true, "final_apgcode": "xs31_g8e1ugmmzd553w643", "period": 1.
That script also fetches the object page (it does not have to match the packaged 60; re-read the cost yourself).
The original harvest verification from 2026-11-15 is in how-we-built-it/data/harvest_verify.json.

## Rebuild the object
how-we-built-it/COMMANDS.md lists the harvest commands (Shinjuku Dijkstra with the cheaper seed injected, then compose and verify).
