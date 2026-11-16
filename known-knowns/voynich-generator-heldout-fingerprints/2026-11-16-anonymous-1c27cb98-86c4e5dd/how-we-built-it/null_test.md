# Null test (PREREG null_test: required — category undeciphered-scripts)

The falsifying statistic H1 (edit-1 adjacency-similarity ratio) is judged against
Voynich quire-bootstrap envelopes. The "controls" are the Voynich bootstrap
resamples themselves: B=4000 per (d,T) cell, 16,000 total, each a
quire-resampled recomputation of H1 on the frozen ZL3b/IT2a corpora
(preload files, seed 20261116; 95% and 99.9% percentile envelopes in
output/env_H1_{d}_{T}.json). The real object is the pooled unmodified-Naibbe
output (200 runs: 20 plaintexts x 10 seeds, 10 A-mode + 10 B-mode per cell,
3,049,192 tokens per mode). A falsification "beats" a control when the real
H1 lies OUTSIDE the control distribution — here below its minimum (the real
object is lower than EVERY Voynich bootstrap resample in all four cells),
which is stronger than the pre-registered 99.9%-envelope rule.

- controls: 16000
- best_control: 0.8990 (minimum H1 over all 16,000 Voynich quire-bootstrap resamples; per-cell minima: A/ZL3b 1.0650, A/IT2a 1.0255, B/ZL3b 0.9037, B/IT2a 0.8990; output/null_H1_bootstraps.json)
- real: 0.7981 (pooled Naibbe A-mode H1) / 0.7917 (pooled Naibbe B-mode H1); attempts/falsifier/output/naibbe_batch.json
- real_beats_all_controls: yes
- detail: 0.7981 < min(A cells) 1.0255; 0.7917 < min(B cells) 0.8990; also below the 0.05-quantile 99.9% bounds of every cell (A/ZL3b 1.0690, A/IT2a 1.0271, B/ZL3b 0.9053, B/IT2a 0.9012)
- command: cd runs/2026-11-16-1141 && python3 code/null_recheck.py   # reruns the 4000x4 quire-bootstrap controls and the pooled-Naibbe comparison; prints PASS when the real H1 beats all 16,000 controls
