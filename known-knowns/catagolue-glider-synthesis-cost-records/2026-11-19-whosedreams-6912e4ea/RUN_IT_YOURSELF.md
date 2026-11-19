# Run it yourself

## Standard-library check (no installs)
From this folder, in a fresh shell:
```
sh verify-it-yourself/run_checks.sh
```
Expected output (also in verify-it-yourself/RECEIPTS.md):
```
gen0: population 65, 13 components, all gliders
rewind T=2880: ok
rewind T=4012: ok
forward: exact repeat from generation 1786, period 1, population 26
final object: matches xs26_8kk69ba952zw3453 exactly, nothing else live
cost: 13 gliders < table cost 32
result: {'ok': True, 'target': 'xs26_8kk69ba952zw3453', 'n_gliders': 13, 'rewind_ok': True, 'periodic_from': 1786, 'period': 1, 'final_population': 26, 'final_matches_target': True, 'table_cost': 32}
PASS
```
The `result:` line is the checker's summary; the last line is PASS.

Controls: `python3 verify-it-yourself/life_check.py --rle object/xs26_8kk69ba952zw3453.rle --target xs26_8kk69ba952zw3453 --table-cost 32 --controls --controls-skip-rewind --control-positive xs27_g88ehmkia4z0178a6`
drops each glider in turn (none of the 13 sub-patterns should build the target; leaving out the one added glider
should build xs27_g88ehmkia4z0178a6, the published 12-glider route). Output from this run is in verify-it-yourself/RECEIPTS.md.

## Live cost
Open https://catagolue.hatsya.com/object/xs26_8kk69ba952zw3453/b3s23 and read the `#CSYNTH xs26_8kk69ba952zw3453 costs N gliders` line. The claim
holds while N is greater than 13.

## lifelib route (as the finder ran it)
Needs python-lifelib 2.5.6 and a Shinjuku checkout (https://gitlab.com/parclytaxel/Shinjuku, commit
3615babf001146507a1e9ec901cb3eabba9f5fd0, 2026-10-27) at `data/Shinjuku` beside `code/`:
```
python how-we-built-it/code/verify_synthesis.py --rle object/xs26_8kk69ba952zw3453.rle --target xs26_8kk69ba952zw3453
```
Expected: JSON with "ok": true, "n_gliders": 13, "rewind_ok": true, "final_apgcode": "xs26_8kk69ba952zw3453", "period": 1 and the live
cost (32 on 2026-11-19; see how-we-built-it/data/verify_xs26_8kk69ba952zw3453_rerun.json).

## Rebuild the object
how-we-built-it/COMMANDS.md lists the exact commands of the sweep, lookup, stitching and verification steps.
