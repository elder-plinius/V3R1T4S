# Run it yourself

## Standard-library check (no installs)
From this folder, in a fresh shell:
```
sh verify-it-yourself/run_checks.sh
```
Expected output (also in verify-it-yourself/RECEIPTS.md):
```
gen0: population 160, 32 components, all gliders
rewind T=8004: ok
rewind T=10916: ok
forward: exact repeat from generation 4332, period 1, population 27
final object: matches xs27_0ca1ugmicz651346 exactly, nothing else live
cost: 32 gliders < table cost 66
...
PASS
```
Controls (about 18 minutes): `python3 verify-it-yourself/life_check.py --rle object/xs27_0ca1ugmicz651346.rle --target xs27_0ca1ugmicz651346 --table-cost 66 --controls --controls-skip-rewind --control-positive xs27_8ehf8bbgz6430321`
drops each glider in turn (none of the 32 sub-patterns builds the target; leaving out the glider at (0,1998) builds
xs27_8ehf8bbgz6430321, the published 31-glider route).

## Live cost
Open https://catagolue.hatsya.com/object/xs27_0ca1ugmicz651346/b3s23 and read the `#CSYNTH xs27_0ca1ugmicz651346 costs N gliders` line. The p1 claim
holds while N is greater than 32 and at least 60.

## lifelib route (as the finder ran it)
Needs python-lifelib 2.5.6 and a Shinjuku checkout (https://gitlab.com/parclytaxel/Shinjuku, commit
3615babf001146507a1e9ec901cb3eabba9f5fd0, 2026-10-27) at `data/Shinjuku` beside `code/`:
```
python how-we-built-it/code/verify_synthesis.py --rle object/xs27_0ca1ugmicz651346.rle --target xs27_0ca1ugmicz651346
```
Expected: JSON with "ok": true, "n_gliders": 32, "rewind_ok": true, "final_apgcode": "xs27_0ca1ugmicz651346", "period": 1 and the live
cost (66 on 2026-11-06; see how-we-built-it/data/verify_xs27_rerun.json).

## Rebuild the object
how-we-built-it/COMMANDS.md lists the exact commands of the sweep, lookup, stitching and verification steps.
