# REPRODUCE (p1 claim)

From the claim/ folder, Python 3 with numpy, scipy, pandas (no other packages, no programs downloaded). Waveforms are
in waveforms/ (sha256 list waveforms/SHA256SUMS_waveforms.txt; URLs in data/urls_s14_1971_mh12.txt, NASA PDS
Geosciences Node, bundle urn:nasa:pds:apollo_pse; EarthScope FDSN was not reachable from the claimant's network).
Create an out/ folder first. Set V3_WORKERS to cap FFT threads (code/scripts/run_capped.py).

1. `cd waveforms && sha256sum -c SHA256SUMS_waveforms.txt && cd ..`
2. Rebuild the 25 S14 templates (about 5 min) and compare with frozen/s14_multinest_1971_templates.npz:
   `python -I code/scripts/run_capped.py code/scripts/s14_multinest_build.py 18,10,9,6,218,14,204,39,23,36,7,26,16,20,201,100,210,29,25,216,86,38,257,22,319 out/templates.npz`
3. Forward scan of 1971 days 36-365 for all 25 nests (about 2-3 s per day):
   `python -I code/scripts/run_capped.py code/scripts/multinest_scan.py frozen/s14_multinest_1971_templates.npz 1971 36 365 out/scan.jsonl`
   (equals results/s14_multinest_scan_1971.jsonl).
4. Seeds: `python -I code/scripts/multinest_seeds.py frozen/s14_multinest_1971_templates.npz results/s14_multinest_scan_1971.jsonl data/catalog data/lit out/seeds`
5. Null for A38 over the same span (C0 + 400 phase-randomised controls; about 6 s per day):
   `python -I code/scripts/run_capped.py code/tools/fast_null.py frozen/s14_A38_1971_templates.npz 1971 36 365 out/null_A38.jsonl 400 20261112`
   (equals results/null_A38_1971.jsonl; fast_null.py reproduces score_scan.py's controls exactly, which
   `python -I code/scripts/run_capped.py code/scripts/score_scan.py frozen/s14_A38_1971_templates.npz 1971 133 133 out/ss.jsonl 400 20261112`
   lets you check on any day).
6. Checks: write {"38": <best control>} to out/nullmax.json, then
   `python -I code/scripts/run_capped.py code/tools/seed_checks.py out/seeds/seeds_summary.json frozen data/catalog data/lit out/checks.json out/nullmax.json`
   (seed_checks.py looks for frozen/s14_A<nest>_1971_templates.npz; only A38 has one here, so restrict the seeds file
   to nest 38 first).

## Added for the glitch-catalogue gates (package rebuild, 2026-11-13)

The glitch-catalogue gates G1 and G2 were not part of this claim's original pre-registration: they were pre-registered at the lens level at 2026-11-13T05:59:12Z, after the claim's own three-skeptic panel (run 2026-11-12-2317), with G1 already seen (a post-panel check, run 2026-11-13-0514) and G2 not yet computed at the time of the freeze. G2's outcome was already implied before its freeze, by G1 and by the claim's original glitch check (no raw sample above 8 x MAD in the window), so there was nothing to mute and G2 adds no independent evidence. Put the two S14 ACC-Spike files of https://doi.org/10.5281/zenodo.15715187 (catalogs/ folder of
lunar_ACC-v1.0.1.zip) in data/lit/ and copy code/scripts/glitch_gates_a38.py, code/scripts/rebuild_object_extracts.py
and code/scripts/extract_spike_subset.py from how-we-built-it/code/scripts.

7. Glitch gates G1, G2 and the descriptive G3 (numpy, scipy, pandas; reads the day-133 waveforms):
   `python -I code/scripts/glitch_gates_a38.py code/tools frozen/s14_A38_1971_templates.npz data/catalog/levent.1008weber.csv data/lit/S14_ACC-Spike_MH1_all.csv data/lit/S14_ACC-Spike_MH2_all.csv out/glitch_gates_A38.json`
   (equals how-we-built-it/glitch_gates_A38.json: byte for byte on Windows, where the script writes CRLF line endings;
   elsewhere the same text with LF endings).
8. Object extracts, rebuilt from the waveforms with the package builder's own code and compared with object/:
   `python -I code/scripts/rebuild_object_extracts.py code/tools frozen/s14_A38_1971_templates.npz out/null_A38.jsonl OBJECT_DIR out/extracts`
   (OBJECT_DIR = this package's object folder)
   (out/extracts/compare.txt: window_and_template.csv, null_full_span_maxima.csv, null_daily_maxima.csv,
   g2_raw_window.csv and g2_prepped_window_pm10s.csv IDENTICAL; NCC 0.726768 / 0.756719, D 0.741743; the frozen glitch
   rule flags no raw sample in the window).
9. Glitch-catalogue extracts (standard library): `python -I code/scripts/extract_spike_subset.py data/lit out/subset window`
   (or the archive itself as the first argument); both files equal object/glitch_catalogue_*_onset_pm24h.csv. Mode
   `year` writes the full scanned-span extract (not shipped; see RUN_IT_YOURSELF.md for its sha256).
