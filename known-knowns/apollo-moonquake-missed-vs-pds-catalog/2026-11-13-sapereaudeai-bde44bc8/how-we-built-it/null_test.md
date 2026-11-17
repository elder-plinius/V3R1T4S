# null_test (p1 candidate A38 1971-05-13 18:39:34 UTC window start, S14 MH1/MH2; PREREG.md R5 = run 2026-11-12-1842 PREREG.v12)

controls: 401
best_control: 0.2868
real: 0.7417
real_beats_all_controls: yes
command: python -I tools/fast_null.py frozen/per_nest/s14_A38_1971_templates.npz 1971 36 365 out/nulls/null_A38_1971.jsonl 400 20261112 (run from attempts/s14-multinest-1971 with the run-1 tools; exact equality with score_scan.py checked in out/fast_null_equality_check.txt)

Controls: C0 = the A38 S14 templates on time-reversed 1971 data (full-span maximum 0.2124); C1..C400 = phase-randomised A38 templates (seeds 20261112 + k) on forward data (best full-span maximum 0.2868). Span: 1971 days 36-365 (330 days), the full searched span of the seed scan.
real = D14 of the candidate (mean of the single-channel NCC on S14 MH1 0.7268 and MH2 0.7567).
