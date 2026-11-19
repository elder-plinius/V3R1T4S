# Run it yourself

## Standard-library check (no installs)
From this folder, in a fresh shell:
```
sh verify-it-yourself/run_checks.sh
```
Expected output (also in verify-it-yourself/RECEIPTS.md):
```
gen0: population 105, 21 components, all gliders
rewind T=7016: ok
rewind T=9892: ok
forward: exact repeat from generation 3840, period 1, population 25
final object: matches xs25_69ar1mkiczx643 exactly, nothing else live
cost: 21 gliders < table cost 49
result: {'ok': True, 'target': 'xs25_69ar1mkiczx643', 'n_gliders': 21, 'rewind_ok': True, 'periodic_from': 3840, 'period': 1, 'final_population': 25, 'final_matches_target': True, 'table_cost': 49}
PASS
```
The `result:` line is the checker's summary; the last line is PASS.

Controls: `python3 verify-it-yourself/life_check.py --rle object/xs25_69ar1mkiczx643.rle --target xs25_69ar1mkiczx643 --table-cost 49 --controls --controls-skip-rewind --control-positive xs27_cikm1da4ozxd8711`
drops each glider in turn (none of the 21 sub-patterns should build the target; leaving out the one added glider
should build xs27_cikm1da4ozxd8711, the published 20-glider route). Output from this run is in verify-it-yourself/RECEIPTS.md.

## Live cost
Open https://catagolue.hatsya.com/object/xs25_69ar1mkiczx643/b3s23 and read the `#CSYNTH xs25_69ar1mkiczx643 costs N gliders` line. The claim
holds while N is greater than 21.

## lifelib route (as the finder ran it)
Needs python-lifelib 2.5.6 and a Shinjuku checkout (https://gitlab.com/parclytaxel/Shinjuku, commit
3615babf001146507a1e9ec901cb3eabba9f5fd0, 2026-10-27) at `data/Shinjuku` beside `code/`:
```
python how-we-built-it/code/verify_synthesis.py --rle object/xs25_69ar1mkiczx643.rle --target xs25_69ar1mkiczx643
```
Expected: JSON with "ok": true, "n_gliders": 21, "rewind_ok": true, "final_apgcode": "xs25_69ar1mkiczx643", "period": 1 and the live
cost (49 on 2026-11-19; see how-we-built-it/data/verify_xs25_69ar1mkiczx643_rerun.json).

## Rebuild the object
how-we-built-it/COMMANDS.md lists the exact commands of the sweep, lookup, stitching and verification steps.
