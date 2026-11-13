# null_test (claim run a100_1030: second A100-like candidate, S14 + S16, onset 1973-10-30 02:25:51.509 UTC; PREREG.md N0)

controls: 401
best_control: 0.1906
real: 0.2981
real_beats_all_controls: yes
command: python -I tools/code/scripts/run_capped.py tools/code/scripts/lagtol_scan_1416.py tools/frozen/nets25_1973.npz 1973 1 365 attempts/null-multiplicity/out/scan12_1973.jsonl 400 (attempts/null-multiplicity/code/run_n0.sh), then python -I -B attempts/null-multiplicity/code/n0_analyse.py tools/code/tools attempts/null-multiplicity/out/scan12_1973.jsonl ../out/lagtol_scan_1973.jsonl tools/data/catalog/levent.1008weber.csv 55,26 attempts/null-multiplicity/out/n0

Controls, computed in this run (2026-11-13T16:23-16:58Z) over all 365 days of 1973 for the A100 stack: C0 = all
channels time-reversed (full-span maximum 0.15744); C1..C400 = S16 circularly rolled by 3600 + 180 k s (best full-span
maximum 0.19062). real = Dt of the A100 forward peak at window start 1973-10-30T02:25:21.509 (0.29806). The rerun is
identical to the lens scan in every science field (fwd_peaks, rev_max, shift_max; the files differ only by a
run-time field) on all 365 days for all 12 nests (attempts/null-multiplicity/out/n0_stdout.txt).
Multiplicity (PREREG M1/M2): max-T family-wise over the 12 templates p = 1/402 (candidate z 17.47 > every family-wise
control maximum, largest 14.36); Bonferroni 12/402 = 0.030; over the 26 two-station template-year scans of 1973 in
the parent run 26/402 = 0.065, over all 55: 0.137 (empirical bounds); GEV tail 4.7e-10 per template (model-based).
