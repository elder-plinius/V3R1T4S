# REPRODUCE (full-criterion claim)

From the claim/ folder, Python 3 with numpy, scipy, pandas (no other packages, no programs downloaded). Create an out/
folder first. Waveforms: waveforms/ (sha256 list waveforms/SHA256SUMS_waveforms.txt; URLs data/urls_s14_s16_1973_mh12.txt
and the ATT files' PDS URLs follow the same pattern with channel "att" and an empty location). Set V3_WORKERS to cap
FFT threads (code/scripts/run_capped.py).

1. `cd waveforms && sha256sum -c SHA256SUMS_waveforms.txt && cd ..`
2. Rebuild the stacks (about 15 min) and compare with frozen/nets25_1973.npz:
   `python -I code/scripts/run_capped.py code/scripts/net25_build_1416.py 18,10,9,6,218,14,204,39,23,36,7,26,16,20,201,100,210,29,25,216,86,38,257,22,319 out/nets.npz`
3. Scan 1973 for nest A100 alone (about 2-4 s per day at one thread; equals the A100 entries of the full scan):
   `python -I code/scripts/run_capped.py code/scripts/lagtol_scan_1416.py frozen/nets25_1973_A100.npz 1973 1 365 out/scan_A100.jsonl 400`
   and compare with results/lagtol_scan_1973_A100.jsonl (fwd_peaks, rev_max, shift_max per day).
4. Candidates: `python -I code/scripts/run_capped.py code/tools/lagtol_candidates.py frozen/nets25_1973_A100.npz results/lagtol_scan_1973_A100.jsonl data/catalog data/lit out/cand`
5. R8: `python -I code/scripts/att_check_1416.py results/lagtol_candidates_1973_A100.json results/lagtol_scan_1973_A100.jsonl 100 1973-11-26T07:46:28.641Z`
6. Glitch: `python -I code/scripts/glitch_check_1416.py frozen/nets25_1973.npz results/lagtol_candidates_1973_A100.json 100 1973-11-26T07:46:28.641Z`

Added in this continuation (code/fullwin/, prereg/PREREG_fullwin.md; outputs to compare in results/fullwin/):

7. Every stacked nest and moveout (A1, A2; seconds):
   `python -I -B code/fullwin/attrib_a1a2.py code/tools frozen/nets25_1973.npz results/lagtol_candidates_1973_stdout.txt data/catalog/nakamura_2005_dm_arrivals.csv out/a1a2.json` (compare results/fullwin/a1a2.json)
8. Reverse search over 1973 (A5; about 2 s per day, 13 min):
   `python -I -B code/fullwin/reverse_scan.py code/tools 1 365 out/reverse_scan_1973.jsonl`, then
   `python -I -B code/fullwin/a5_analyse.py out/reverse_scan_1973.jsonl data/catalog/levent.1008weber.csv b` (and `a`)
   (compare results/fullwin/a5_variant_b.txt, a5_variant_a.txt)
9. S16 MH2 response (A3; about 4 min):
   `python -I -B code/fullwin/s16_mh2_response.py code/tools data/catalog/levent.1008weber.csv out/s16_response_1973.jsonl`, then
   `python -I -B code/fullwin/a3_decide.py out/s16_response_1973.jsonl` (compare results/fullwin/a3_decision.txt)
10. Phase (A4): `python -I -B code/fullwin/a4_phase.py code/tools data/catalog/levent.1008weber.csv` (compare results/fullwin/a4_phase.txt)
11. Glitch catalogue gates (G1, G2; about 1 min): `cd data/lit_acc && sha256sum -c SHA256SUMS.txt && cd ../..`, then
   `python -I -B code/fullwin/glitch_gates_1416.py code/tools frozen/nets25_1973_A100.npz data/lit_acc out/glitch_gates_A100.json`
   (compare results/fullwin/glitch_gates_A100.json)
12. Knapmeyer-Endrun and Hammer 2015 tables: `python -I -X utf8 code/fullwin/xls_dump.py data/lit/knapmeyer2015/<each .xls> out/kn_tsv`, then
   `python -I -X utf8 code/fullwin/kn_check.py out/kn_tsv data/lit/knapmeyer2015` (compare results/fullwin/kn_check.txt)
13. Bulow 2005 Table 2: `python -I -X utf8 code/fullwin/pdftxt.py data/lit/bulow2005/bulow_jgr05.pdf 400000 > out/bulow.txt`, then
   `python -I -X utf8 code/fullwin/bulow_check.py out/bulow.txt` (compare results/fullwin/bulow_check.txt)
