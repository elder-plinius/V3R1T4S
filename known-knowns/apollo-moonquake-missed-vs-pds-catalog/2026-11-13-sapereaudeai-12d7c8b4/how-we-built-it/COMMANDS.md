# REPRODUCE (p1 claim, nest A39)

From the claim/ folder, Python 3 with numpy, scipy, pandas (no other packages, no programs downloaded). Waveforms in
waveforms/ (sha256 list waveforms/SHA256SUMS_waveforms.txt; URLs data/urls_s14_1971_mh12.txt, NASA PDS Geosciences
Node). Create an out/ folder first. V3_WORKERS caps FFT threads (code/scripts/run_capped.py).

1. `cd waveforms && sha256sum -c SHA256SUMS_waveforms.txt && cd ..`
2. Rebuild the 25 S14 stacks (about 5 min) and compare with frozen/s14_multinest_1971_templates.npz (the A39 entry and
   frozen/s14_A39_1971_templates.npz):
   `python -I code/scripts/run_capped.py code/scripts/s14_multinest_build.py 18,10,9,6,218,14,204,39,23,36,7,26,16,20,201,100,210,29,25,216,86,38,257,22,319 out/templates.npz`
   (one nest: `... s14_multinest_build.py 39 out/a39.npz`)
3. Forward scan (about 2-3 s per day):
   `python -I code/scripts/run_capped.py code/scripts/multinest_scan.py frozen/s14_multinest_1971_templates.npz 1971 36 365 out/scan.jsonl`
4. Seeds: `python -I code/scripts/multinest_seeds.py frozen/s14_multinest_1971_templates.npz results/s14_multinest_scan_1971.jsonl data/catalog data/lit out/seeds`
5. Null for A39 (about 6 s per day):
   `python -I code/scripts/run_capped.py code/tools/fast_null.py frozen/s14_A39_1971_templates.npz 1971 36 365 out/null_A39.jsonl 400 20261112`
   (equals results/null_A39_1971.jsonl; code/scripts/score_scan.py gives the same controls on any single day, e.g.
   `... code/scripts/score_scan.py frozen/s14_A39_1971_templates.npz 1971 248 248 out/ss248.jsonl 400 20261112`).
6. Checks: results/seed_checks_A39_A201.json (key "39", the seed with onset 1971-09-05T01:26:14.150Z) was made with
   code/tools/seed_checks.py with null maxima {"39": 0.3180, "201": 0.2751}; it reads frozen/s14_A<nest>_1971_templates.npz.
7. Glitch gates G1-G3: `python -I code/scripts/glitch_gates.py code/tools frozen/s14_A39_1971_templates.npz data/catalog/levent.1008weber.csv data/lit/S14_ACC-Spike_MH1_all.csv data/lit/S14_ACC-Spike_MH2_all.csv out/glitch_gates.json`
   (equals results/glitch_gates_A39.json).
8. Decimation phase: `python -I code/scripts/phase1_check.py out/phase1.json` (rebuilds the A201 and A39 stacks on the
   other grid; A39 entry).
