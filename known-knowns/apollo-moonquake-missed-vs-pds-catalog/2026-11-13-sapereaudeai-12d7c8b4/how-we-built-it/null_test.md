# null_test (p1 candidate A39, S14 MH1/MH2, window start 1971-09-05 01:25:44.150 UTC; PREREG.v12 of run 2026-11-12-1842)

controls: 401
best_control: 0.3180
real: 0.6439
real_beats_all_controls: yes
command: python -I code/scripts/run_capped.py code/tools/fast_null.py frozen/s14_A39_1971_templates.npz 1971 36 365 out/null_A39.jsonl 400 20261112

Controls: C0 = the A39 S14 templates on time-reversed 1971 data (full-span maximum 0.2205); C1..C400 = phase-randomised templates (seeds 20261112 + k) on forward data (best 0.3180). Span: 1971 days 36-365 (330 days), the full span of the seed scan. real = D14 (mean of MH1 0.5952 and MH2 0.6925). Computed in run 2026-11-12-1842's lens (results/null_A39_1971.jsonl), before this run's prereg (disclosed there).
