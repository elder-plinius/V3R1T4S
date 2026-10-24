# Run it yourself

All commands run from this package folder in a fresh shell.

## 1. The standalone check (Python 3 standard library)
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output (verify-it-yourself/RECEIPTS.md has the real one), last line `PASS`:
```
integrity: 48 files listed, 0 bad
variables: scored 80, recovered (independent agree) 77
controls: scored 400 (VSX CST 67), max control S 21.103453, S > 54.0: 0/400 overall, 0/67 CST
recovered AND S above every control: 77 (rule: >= 50)
light curves: not checked offline (run fetch_lightcurves.py DIR, then this script with --lc-dir DIR)
PASS
```
The light curves are public ZTF data and are not copied into this package; how-we-built-it/data/lc_manifest.csv
lists, for all 524 stars, the exact SNAD URL, the byte count and the sha256 of the response that was scored.
Fold test with the light curves (network, about 2 minutes):
```sh
python3 -I verify-it-yourself/fetch_lightcurves.py lc
python3 -I -B verify-it-yourself/check_gate.py --lc-dir lc
```
Expected: `light curves: 77 recovered periods folded; worst PDM ratio to random median 0.733 (limit 0.8)` and
`PASS` if SNAD still serves the same release (the fetch script reports how many responses are byte-identical).

## 2. Re-run the frozen pipeline on the light curves (rebuilds object/)
Needs Python 3.9+ with how-we-built-it/requirements.txt (numpy 1.26.4, scipy 1.13.1, astropy 6.0.1, pandas 2.3.3).
A few minutes on 3 cores.
```sh
python3 -I verify-it-yourself/fetch_lightcurves.py lcall --all      # about 15 minutes, 524 GETs
W=$(mktemp -d); cp -R how-we-built-it/code $W/code; mkdir -p $W/data $W/out $W/results
cp how-we-built-it/data/*.csv how-we-built-it/data/*.tsv $W/data/
for s in var cst gaia; do mkdir -p $W/data/lc_$s; for f in lcall/${s}_*.json; do
  b=$(basename "$f"); cp "$f" $W/data/lc_$s/${b#${s}_}; done; done
cd $W
OMP_NUM_THREADS=1 python3 -I code/run_many.py out/var.jsonl 3 data/lc_var/*.json
OMP_NUM_THREADS=1 python3 -I code/run_many.py out/cst.jsonl 3 data/lc_cst/*.json
OMP_NUM_THREADS=1 python3 -I code/run_many.py out/gaia.jsonl 3 data/lc_gaia/*.json
python3 -I code/decide.py
```
Expected: decide.py prints `recovered: 77/80; recovered AND detected (S > best_control): 77`, `FAR at T=54.0: 0/400`,
`PREREG decision: real_count=77 -> PASS` (full text in how-we-built-it/decide_output.txt), and writes
results/vsx_reproduce_known_table.csv and results/controls_table.csv byte-identical to object/ (`cmp` them).
decide.py imports agree() from code/period_check.py (its first sys.path entry is a placeholder path, then its own
folder). The `command:` line it prints is a hard-coded string.

## 3. Re-draw and re-fetch (optional, network)
`code/draw_v3.py var|cst|gaia|order` re-queries VizieR B/vsx and the Gaia DR3 TAP and rebuilds the pools and the
seeded draw orders (B/vsx changes over time; the saved pools in how-we-built-it/data are the ones used).
`code/fetch_lcs_v3.py var 80`, `cst 1000000`, `gaia 400` re-fetch the light curves, one GET per star, from
https://db.ztf.snad.space/api/v3/data/latest/circle/full/json?ra=<ra>&dec=<dec>&radius_arcsec=1.5 (SNAD's "latest"
release can change; the saved JSON is the scored evidence). Use an honest User-Agent and >= 1 s between requests.

## 4. The frozen rules
how-we-built-it/PREREG.v2_run1643_frozen_statistic.md (statistic S, period pick, usable-LC rule, T = 54.0; frozen
2026-10-15T17:14:05Z) and how-we-built-it/PREREG.md (draws and decision rule, Line A2; frozen 2026-10-15T17:48:06Z),
both written before these light curves were fetched (first fetch 2026-10-15T18:01:26Z, last 18:30:57Z).
how-we-built-it/null_test.md holds the null-test lines.
