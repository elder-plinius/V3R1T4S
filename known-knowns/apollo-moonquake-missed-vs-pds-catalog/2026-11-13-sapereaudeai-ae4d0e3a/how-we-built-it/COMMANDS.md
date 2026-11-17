# Commands (from a working folder laid out as described in RUN_IT_YOURSELF.md)


From the working folder, Python 3 with numpy, scipy and pandas (no other packages; no programs downloaded). Create an
out/ folder first. Waveforms: waveforms/ (S14 and S16 MH1/MH2 for all of 1973 plus 1974-001, the ATT timing files used,
and S12 MH1/MH2/MHZ for 1973 days 303, 304, 330, 331); sha256 list waveforms/SHA256SUMS_waveforms.txt; URLs
data/urls_s14_s16_1973_mh12.txt and data/urls_att_and_s12.txt (PDS Geosciences, Nunn et al. 2022 restoration).
V3_WORKERS caps FFT threads (code/scripts/run_capped.py). Expected outputs to compare are in results/.

1. `cd waveforms && sha256sum -c SHA256SUMS_waveforms.txt && cd ..`
2. N0, the bank null (all 12 nest stacks, all 365 days of 1973, C0 time-reversed + C1..C400 S16 rolled by
   3600 + 180 k s; about 30-40 min at one thread, peak memory about 390 MB):
   `python -I code/scripts/run_capped.py code/scripts/lagtol_scan_1416.py frozen/nets25_1973.npz 1973 1 365 out/scan12_1973.jsonl 400`
   (compare with results/scan12_1973.jsonl). Analysis (null, multiplicity M1/M2, specificity A6, A3b forward part,
   determinism against the earlier lens scan data/lens_scan_1973.jsonl):
   `python -I -B code/c1030/n0_analyse.py code/tools out/scan12_1973.jsonl data/lens_scan_1973.jsonl data/catalog/levent.1008weber.csv 55,26 out/n0`
   (compare results/n0_stdout.txt, results/n0.json, results/n0_A100_control_maxima.csv). 55 and 26 are the numbers of
   two-station template-year scans of the parent run (all years; 1973), counted from its lens build logs.
3. Candidates of the rerun (per-nest nulls, R6, R7, R9, gap, thermal):
   `python -I code/scripts/run_capped.py code/tools/lagtol_candidates.py frozen/nets25_1973.npz out/scan12_1973.jsonl data/catalog data/lit out/cand12`
   then `python -I -B code/c1030/m4_list.py out/cand12.json data/lit code/tools` (compare results/cand12_stdout.txt, results/m4_list.txt).
4. R8 (ATT): `python -I code/scripts/att_check_1416.py out/cand12.json out/scan12_1973.jsonl 100 1973-10-30T02:25:51.509Z`
   (compare results/r8_att_A100_1030.txt; the printed label "S14-S12" is inherited, the code computes S16 minus S14).
5. Frozen glitch rule: `python -I code/scripts/glitch_check_1416.py frozen/nets25_1973.npz out/cand12.json 100 1973-10-30T02:25:51.509Z` (compare results/glitch_rule_A100_1030.txt).
6. Glitch-catalogue gates G1/G2 (Liu, Xiao and Li 2025): `cd data/lit_acc && sha256sum -c SHA256SUMS.txt && cd ../..`, then
   `python -I -B code/c1030/glitch_gates_1030.py code/tools frozen/nets25_1973_A100.npz data/lit_acc out/glitch_gates_A100_1030.json <N0 best control>`
   and the base rate `python -I -B code/c1030/g3_base_rate.py data/lit_acc data/catalog/levent.1008weber.csv`
   (compare results/glitch_gates_A100_1030.json, results/glitch_gates_stdout.txt, results/g3_base_rate.txt).
7. A1 (all 12 stacks) and A2 (lags, moveout): `python -I -B code/c1030/attrib_a1a2_1030.py code/tools frozen/nets25_1973.npz out/cand12_stdout.txt data/catalog/nakamura_2005_dm_arrivals.csv out/a1a2_1030.json` (compare results/a1a2_1030.json).
8. A3 (S16 MH2 response, about 5 min): `python -I -B code/c1030/s16_mh2_response_1030.py code/tools data/catalog/levent.1008weber.csv out/s16_response_1973_1030.jsonl`, then
   `python -I -B code/c1030/a3_decide_1030.py out/s16_response_1973_1030.jsonl` (compare results/a3_decision_1030.txt).
9. A4 (phase): `python -I -B code/fullwin/a4_phase.py code/tools data/catalog/levent.1008weber.csv` (compare results/a4_phase.txt).
10. A5 reverse search (about 15-20 min): `python -I -B code/c1030/reverse_scan_1030.py code/tools 1 365 out/reverse_scan_1973_1030.jsonl`, then
   `python -I -B code/c1030/a5_analyse_1030.py out/reverse_scan_1973_1030.jsonl data/catalog/levent.1008weber.csv b` (and `a`)
   (compare results/a5_variant_b_1030.txt, results/a5_variant_a_1030.txt).
11. D1 other decimation phase (stack rebuilt on that grid): `python -I -B code/c1030/decphase_1030.py code/tools data/catalog/levent.1008weber.csv frozen/nets25_1973_A100.npz out/decphase_1030.json` (compare results/decphase_stdout.txt).
12. S12 as a third station: `python -I -B code/c1030/s12_third_1030.py code/tools frozen/nets25_1973_s12s14.npz out/s12_third_1030.json data/lens_s12s14_candidates_stdout.txt` (compare results/s12_third_stdout.txt).
13. R6 and published lists: `python -I -B code/c1030/r6_check_1030.py code/tools data/catalog data/lit`;
   `python -I -X utf8 code/c1030/xls_dump.py data/lit/knapmeyer2015/<each .xls> out/kn_tsv`, then
   `python -I -X utf8 code/c1030/kn_check_1030.py out/kn_tsv data/lit/knapmeyer2015`;
   `python -I -X utf8 code/c1030/pdftxt.py data/lit/bulow2005/bulow_jgr05.pdf 400000 > out/bulow.txt`, then
   `python -I -X utf8 code/c1030/bulow_check_1030.py out/bulow.txt` (compare results/r6_check_1030.txt, kn_check_1030.txt, bulow_check_1030.txt).
