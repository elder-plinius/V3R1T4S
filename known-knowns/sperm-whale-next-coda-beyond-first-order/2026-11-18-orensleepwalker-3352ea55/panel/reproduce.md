# Fresh REPRODUCE review: frozen whale p4

context: fresh subagent

pass: true

This is a fresh numerical reproduction review of the frozen `claim/` bundle. I did not use the interrupted reviewer's partial results or read other panel material. The pass is for the literal p4 numerical benchmark, subject to the limitations below; it does not establish novelty, independent prospective confirmation, or communicative meaning. Nothing was published.

## Independent checks

Before reading author source, I wrote and ran `independent.py` from target/preregistration definitions. It reads the CSV with Python's standard CSV reader, groups by REC, sorts numeric TsTo with file-row tie breaks, assigns lexically sorted RECs modulo five, and independently constructs adjacent-speaker equality labels. It finds 3,840 rows, 219 REC streams, and 3,418 eligible targets from 188 streams. Eligible targets per fold are 514, 1,305, 508, 692, and 399. Every saved row index, REC, and target label matches. Training-only duration quintiles also match all five saved edge vectors.

I independently fit the binary first-order transition table, including pooled inner-fold selection over alpha = .01/.03/.1/.3/1. Selected alphas are 1/.01/1/.01/1. Every R1 probability matches within 1e-14. R1 loss is **0.8503173539892255 bits**.

After reading the frozen author's exact model formulas, I wrote a separate dictionary/Counter-style fitting implementation and a position-by-position feature implementation in `models.py`; it does not call author fitting, preparation, or prediction functions. It independently refits both widths, every named family, all strengths, and all inner and outer folds. Every saved family/twin probability matches exactly, as do the selected strengths and repetition-family selection in all five folds. This is an independent implementation of the disclosed algorithm, not a source-blind derivation of the candidate: the preregistration alone does not completely specify every feature boundary and hierarchical smoothing detail.

All saved binary probability vectors are finite, positive and normalized. Recomputed selected-model loss is **0.7802677275878882 bits**, giving **0.07004962640133727 bits** improvement over R1, above p4's 0.05 requirement. Using fresh seed 573921 and 10,000 whole-REC resamples, independently recomputed size-weighted paired 95% percentile interval is **[0.0533958639308128, 0.09081421590379664]**, excluding zero. The original reported interval is consistent with a different bootstrap seed.

## Controls and leakage

I audited every one of the 800 saved null records: exactly 400 distinct seeds 310000–310399 in each mode, valid task/count metadata and finite scores, baseline-minus-model arithmetic, and positive changed-field counts. All first-order-control baseline scores equal the real baseline, as expected from the preserved transition counts.

| Control | Maximum selected gain over R1 | Seed | Maximum selected gain over twin |
| --- | ---: | ---: | ---: |
| Payload | 0.047148187345422365 | 310233 | 0.04715398907119041 |
| First-order preserving | 0.03334803918937286 | 310158 | 0.03336200631476981 |

The maxima over every named family are the same as the selected-pipeline maxima. The real gains exceed both modes' maxima. No null even reaches p4's 0.05 point-estimate gate, so omitting per-null bootstrap intervals cannot change whether any saved null meets p4's complete rule.

I replayed payload seeds 310000, 310199, 310233, 310399 and first-order seeds 310000, 310158, 310199, 310399, including both maxima. Each replay reruns feature generation, inner selection, fitting and outer scoring, with exactly zero discrepancy in saved gains for every family and comparison. These replays use the author's pipeline and surrogate generator rather than a second independent null implementation. At the first seed of each mode, the slow and vectorized preparation pipelines give identical full summaries. I separately verified replayed payloads preserve within-REC joint count/duration/speaker multisets and fixed onsets; first-order replays preserve the initial binary bit and directed binary transition multiset, stream lengths and fixed onsets.

For **every one of 3,418 eligible targets**, I jointly altered all represented fields of that target and its future (count, duration, speaker, onset, row metadata) and checked every feature of every named family at both widths. No prediction input at the tested target changed. Training and stream ordering are held fixed for this causal-input test. ICI fields are absent from the predictor implementation. Source inspection confirms held-out data are excluded from fits and inner selection, and REC streams never split across folds.

## Limits and artifacts

- The independent baseline/labels/edges/bootstrap implementation preceded reading author code; the exact independent candidate refit followed reading its formulas. This is not a fully source-blind candidate reconstruction.
- All 800 records were audited, but only eight complete null pipelines were replayed; I did not regenerate all 800 controls or their probabilities.
- The so-called one-coda twin retains the previous binary same/switch outcome, which itself summarizes two earlier raw whale labels. I make no strict single-raw-coda interpretation or p2 claim from that twin. Literal p4 uses the explicitly specified first-order same/switch reference, which was independently reconstructed.
- The first-order surrogate is a diagnostic randomized Euler-trail procedure, not a uniform exact randomization test. It abstracts individual speaker identity. Predictability can reflect stream composition or turn persistence; the numerical benchmark establishes no mechanism.
- I used only the frozen source/data/output bundle, not a fresh upstream download. All 18 frozen SHA256SUMS entries verify. Prior score inspection disclosed in CLAIM.md prevents treating this as a new prospective experiment.

Scripts and JSON results in `panel/reproduce-artifacts/` are retained in the local workspace, not included in the public package. Additional internal temporary scratch is also not included. Reviewer scratch files are not required to run the package checker. The frozen claim's checked files were unchanged. Run with Python 3 with NumPy 2.5.4 and `OPENBLAS_NUM_THREADS=1` (set `PYTHONDONTWRITEBYTECODE=1` when importing author code to avoid transient cache files).

Editorial note (2026-11-18): local interpreter and scratch paths were redacted for portable packaging; findings, independence limits, replay scope, and verdict are unchanged.

Final verdict: **pass: true** for reproduction of the literal frozen p4 numerical result, with the scope and independence limits above.

pass: true
