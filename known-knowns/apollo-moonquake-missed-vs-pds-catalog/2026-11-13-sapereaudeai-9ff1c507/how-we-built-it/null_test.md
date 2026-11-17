# null_test (full-criterion candidate, nest A100, S14+S16, onset 1973-11-26 07:46:28.6 UTC; PREREG.md = run 2026-11-12-1842 PREREG.v15)

controls: 401
best_control: 0.1906
real: 0.3433
real_beats_all_controls: yes
command: python -I code/lagtol_scan_1416.py frozen/nets25_1973.npz 1973 1 365 out/scan.jsonl 400 (run with code/run_capped.py; then the A100 entries of every day give rev_max and shift_max)

Controls: C0 = the A100 S14+S16 templates on time-reversed 1973 data (full-span maximum 0.1574); C1..C400 = S16 channels circularly rolled by 3600 + 180 k s relative to S14 (best full-span maximum 0.1906). Span: all 365 days of 1973, the full searched span. real = Dt of the candidate (min of the S14 and S16 station means, each at its best lag within 7 samples).
Other nests searched with the same design in this lens (12 in total) have their own nulls (0.176-0.625); see attempts/lagtol-s14s16-1973/out/lagtol_candidates_1973_stdout.txt.
