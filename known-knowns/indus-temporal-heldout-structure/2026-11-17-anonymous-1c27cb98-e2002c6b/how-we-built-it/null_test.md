# Null test (PREREG null_test: required — category undeciphered-scripts)

Pre-registered design (PREREG.md 2026-11-17T02:50Z, pool rules corrected in PREREG.v2.md
2026-11-17T03:25Z): the claim model (class-conditional positional template, n<=3, add-one,
wildcard OOV, M77-only fit, seed 20261117) must beat BOTH baselines — (i) the tuned per-class
Kneser-Ney 3-gram (same M77 data, discount grid-tuned on the 10% M77 object split) and (ii) the
SIGIL-style class-conditional position-unigram control (matched on unigram + length distribution) —
on the pooled and per-site held-out sets.

"Controls" are the 10,000 paired-bootstrap resamples (seed 20261117) per site: each resample
recomputes all three accuracies on the resampled held-out set. best_control is the maximum, over
the 10,000 resamples, of max(KN accuracy, synthetic accuracy) at that site. "real beats all
controls" additionally requires the real claim accuracy to exceed the real (non-resampled) KN and
synthetic accuracies. This satisfies the >= 400-controls rule with 3 x 10,000 = 30,000 control
comparisons (plus the 400-draw synthetic pool per object used to build baseline (ii)).

Results (from `code/nulltest.py`, seed 20261117, B=10,000; output
`code/output_nulltest.json`):
- pooled: real 0.5846 vs KN 0.2808, synth 0.1872, best_control 0.3255, p=0.0, gap 0.2591
- Mohenjo-daro: real 0.7098 vs KN 0.3293, synth 0.1173, best_control 0.3970, p=0.0, gap 0.3128
- Harappa: real 0.4017 vs KN 0.2153, synth 0.2441, best_control 0.3136, p=0.0, gap 0.0881

- controls: 30000
- best_control: 0.397 (Mohenjo-daro; the maximum of the 10,000-resample max(KN,synth) distribution at that site; pooled 0.3255, Harappa 0.3136 — all < real)
- real: 0.5846 (pooled) / 0.7098 (Mohenjo-daro) / 0.4017 (Harappa) — all > their site's best_control and > the real KN and synth accuracies
- real_beats_all_controls: yes
- command: cd runs/2026-11-17-0212 && python3 code/nulltest.py  # reruns the 3x10,000 paired bootstrap (seed 20261117) and prints the per-site real / best_control / p
