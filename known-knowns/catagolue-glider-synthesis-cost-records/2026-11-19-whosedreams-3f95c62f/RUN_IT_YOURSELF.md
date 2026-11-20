# Run it yourself

## Standard-library check (no installs)
From this folder, in a fresh shell:
```
sh verify-it-yourself/run_checks.sh
```
Expected output (also in verify-it-yourself/RECEIPTS.md):
```
gen0: population 145, 29 components, all gliders
rewind T=4920: ok
rewind T=6284: ok
forward: exact repeat from generation 2810, period 1, population 27
final object: matches xs27_08e1ugmicz651346 exactly, nothing else live
cost: 29 gliders < table cost 62
result: {'ok': True, 'target': 'xs27_08e1ugmicz651346', 'n_gliders': 29, 'rewind_ok': True, 'periodic_from': 2810, 'period': 1, 'final_population': 27, 'final_matches_target': True, 'table_cost': 62}
PASS
```
The `result:` line is the checker's summary; the last line is PASS.

Controls: `python3 verify-it-yourself/life_check.py --rle object/xs27_08e1ugmicz651346.rle --target xs27_08e1ugmicz651346 --table-cost 62 --controls --controls-skip-rewind --control-positive xs27_caar4kl3z330343`
drops each glider in turn (none of the 29 sub-patterns should build the target; leaving out the one added glider
should build xs27_caar4kl3z330343, the published 28-glider route). Output from this run is in verify-it-yourself/RECEIPTS.md.

## Live cost
Open https://catagolue.hatsya.com/object/xs27_08e1ugmicz651346/b3s23 and read the `#CSYNTH xs27_08e1ugmicz651346 costs N gliders` line. The claim
holds while N is greater than 29 and at least 60.

## lifelib route (as the finder ran it)
Needs python-lifelib 2.5.6 and a Shinjuku checkout (https://gitlab.com/parclytaxel/Shinjuku, commit
3615babf001146507a1e9ec901cb3eabba9f5fd0, 2026-10-27) at `data/Shinjuku` beside `code/`:
```
python how-we-built-it/code/verify_synthesis.py --rle object/xs27_08e1ugmicz651346.rle --target xs27_08e1ugmicz651346
```
Expected: JSON with "ok": true, "n_gliders": 29, "rewind_ok": true, "final_apgcode": "xs27_08e1ugmicz651346", "period": 1 and the live
cost (62 on 2026-11-19; see how-we-built-it/data/verify_xs27_08e1ugmicz651346_rerun.json).

## Rebuild the object
how-we-built-it/COMMANDS.md lists the exact commands of the sweep, lookup, stitching and verification steps.
