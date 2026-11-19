# Run it yourself

## Standard-library check (no installs)
From this folder, in a fresh shell:
```
sh verify-it-yourself/run_checks.sh
```
Expected output (also in verify-it-yourself/RECEIPTS.md):
```
gen0: population 75, 15 components, all gliders
rewind T=3748: ok
rewind T=4768: ok
forward: exact repeat from generation 1880, period 1, population 28
final object: matches xs28_08ehlmggoz6a87066 exactly, nothing else live
cost: 15 gliders < table cost 61
result: {'ok': True, 'target': 'xs28_08ehlmggoz6a87066', 'n_gliders': 15, 'rewind_ok': True, 'periodic_from': 1880, 'period': 1, 'final_population': 28, 'final_matches_target': True, 'table_cost': 61}
PASS
```
(The `result:` line is the checker's summary dictionary; the last line is PASS.) About a minute or less on a laptop.

Optional drop-one controls (not part of run_checks.sh): `python3 verify-it-yourself/life_check.py --rle object/xs28_08ehlmggoz6a87066.rle --target xs28_08ehlmggoz6a87066 --table-cost 61 --controls`

## Live cost
Open https://catagolue.hatsya.com/object/xs28_08ehlmggoz6a87066/b3s23 and read the `#CSYNTH xs28_08ehlmggoz6a87066 costs N gliders` line. The claim
holds while N is greater than 15 and at least 60.

## lifelib route (as the finder ran it)
Needs python-lifelib 2.5.6 and a Shinjuku checkout (https://gitlab.com/parclytaxel/Shinjuku, commit
3615babf001146507a1e9ec901cb3eabba9f5fd0, 2026-10-27) importable as the `shinjuku` package:
```
python3 how-we-built-it/code/verify_synthesis.py --rle object/xs28_08ehlmggoz6a87066.rle --target xs28_08ehlmggoz6a87066
```
Expected: JSON with "ok": true, "n_gliders": 15, "rewind_ok": true, "final_apgcode": "xs28_08ehlmggoz6a87066", "period": 1.
That script also fetches the object page (it does not have to match the packaged 61; re-read the cost yourself).
The original harvest verification from 2026-11-15 is in how-we-built-it/data/harvest_verify.json.

## Rebuild the object
how-we-built-it/COMMANDS.md lists the harvest commands (Shinjuku Dijkstra with the cheaper seed injected, then compose and verify).
