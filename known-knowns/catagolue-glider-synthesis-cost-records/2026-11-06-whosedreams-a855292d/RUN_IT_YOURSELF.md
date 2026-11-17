# Run it yourself

## Standard-library check (no installs)
From this folder, in a fresh shell:
```
sh verify-it-yourself/run_checks.sh
```
Expected output (also in verify-it-yourself/RECEIPTS.md):
```
gen0: population 60, 12 components, all gliders
rewind T=2860: ok
rewind T=4040: ok
forward: exact repeat from generation 1774, period 1, population 26
final object: matches xs26_08ehmkk8z6a87066 exactly, nothing else live
cost: 12 gliders < table cost 58
...
PASS
```
Controls (about 2.5 minutes): `python3 verify-it-yourself/life_check.py --rle object/xs26_08ehmkk8z6a87066.rle --target xs26_08ehmkk8z6a87066 --table-cost 58 --controls --control-positive xs28_651ugmmz69706221`
drops each glider in turn (none of the 12 sub-patterns builds the target; leaving out the last-arriving glider builds
xs28_651ugmmz69706221, the published 11-glider route).

## Live cost
Open https://catagolue.hatsya.com/object/xs26_08ehmkk8z6a87066/b3s23 and read the `#CSYNTH xs26_08ehmkk8z6a87066 costs N gliders` line. The claim
holds while N is greater than 12.

## lifelib route (as the finder ran it)
Needs python-lifelib 2.5.6 and a Shinjuku checkout (https://gitlab.com/parclytaxel/Shinjuku, commit
3615babf001146507a1e9ec901cb3eabba9f5fd0, 2026-10-27) at `data/Shinjuku` beside `code/`:
```
python how-we-built-it/code/verify_synthesis.py --rle object/xs26_08ehmkk8z6a87066.rle --target xs26_08ehmkk8z6a87066
```
Expected: JSON with "ok": true, "n_gliders": 12, "rewind_ok": true, "final_apgcode": "xs26_08ehmkk8z6a87066", "period": 1 and the live
cost (58 on 2026-11-06; see how-we-built-it/data/verify_xs26_rerun.json).

## Rebuild the object
how-we-built-it/COMMANDS.md lists the exact commands of the sweep, lookup, stitching and verification steps.
