# null_test - sperm-whale-next-coda-beyond-first-order (run 2026-11-19-0936)

Main claim (full criterion), condition (2): design N2 of PREREG.md (first-order Markov bootstrap of coda records; statistic = pooled gain of the frozen model over its single-previous-coda twin).

controls: 400
best_control: 0.010642581202370468
real: 0.5310621359536837
real_beats_all_controls: yes
command: python -I attempts/evaluator/code/nulls.py N2 data/csv/sperm-whale-dialogues.csv <first> <last> attempts/evaluator/nulls/N2_<worker>.csv  (then python -I attempts/evaluator/code/make_null_test.py ...)

N2 control gains (full vs twin): mean 0.00040, sd 0.00258, min -0.00617, max 0.01064, indices 0..399, distinct 400
N2 context only (not a gate): gain full vs R1 under the null: mean 0.02919, max 0.05904 (real full vs R1 = 0.6563064778564619)
N2 duplicated indices (same seed computed twice across worker restarts; first kept): [(2, -8.8287715e-05, -8.8287719e-05)]

## p4 claim: design N4 (labels resimulated from the pooled first-order same/switch chain)

p4_controls: 400
p4_best_control: 0.000946956774339432
p4_real: 0.08720554077302466
p4_real_beats_all_controls: yes
p4 control gains: mean -0.00592, sd 0.00257, min -0.01557, max 0.00095
p4_command: python -I attempts/evaluator/code/nulls.py N4 data/csv/sperm-whale-dialogues.csv 0 400 attempts/evaluator/nulls/N4_<worker>.csv

## p3 claim: design N3 (CodaType sequences resimulated from the pooled first-order transitions)

p3_controls: 400
p3_best_control: 0.0011542479820425993
p3_real: 0.1284227460626554
p3_real_beats_all_controls: yes
p3 control gains: mean -0.00469, sd 0.00208, min -0.01019, max 0.00115
p3_command: python -I attempts/evaluator/code/nulls.py N3 data/csv/DominicaCodas.csv <first> <last> attempts/evaluator/nulls/N3_<worker>.csv

## Post-hoc diagnostic, NOT a gate: designs N5 and N6 (composition-preserving shuffle)

Designed after the three gates were written; frozen in PREREG.N5.md (2026-11-19T13:53:43Z) with the statistic
corrected in PREREG.N5.v2.md (14:00:12Z). Completed 16:37:08Z. Full result and integrity checks in
attempts/evaluator/nulls5/RESULT.md. Under the operator's "fair, not strictest" rule these numbers do not move any
threshold above and do not alter the three gates; they decide how the result is described.

The real values below are the exact ones from the frozen summaries. PREREG.N5.v2.md mis-transcribes them as
0.211240 and 0.025500 (errors of 2e-6 and 3.5e-5, both mine, both in transcription only). The frozen file is left
unedited and RESULT.md tabulates the difference; no verdict depends on it, since the largest control is 0.039591
against 0.2112 and 0.016931 against 0.0255.

n5_controls: 400 (indices 0..399, no duplicates, no gaps)
n5_statistic: pooled gain of full over a stream-local reference (both refit on the shuffled data)
n5_best_control: 0.039591049036179021
n5_real: 0.211238
n5_real_beats_all_controls: yes   (control mean 0.023049, sd 0.005585; real is +33.70 sd)

n6_controls: 400 (indices 0..399, no duplicates, no gaps)
n6_best_control: 0.016930587044015767
n6_real: 0.025465
n6_real_beats_all_controls: yes   (control mean 0.009387, sd 0.002052; real is +7.85 sd; margin 1.50x, the
narrowest of this run - state it wherever p3 is described)

n5_command: python -I attempts/evaluator/code/nulls_n5.py N5 data/csv/sperm-whale-dialogues.csv <first> <last> attempts/evaluator/nulls5/N5_<worker>.csv
n6_command: python -I attempts/evaluator/code/nulls_n5.py N6 data/csv/DominicaCodas.csv <first> <last> attempts/evaluator/nulls5/N6_<worker>.csv

Statistics declared INVALID as nulls by PREREG.N5.v2.md before 798 of the 800 controls ran, reported here because
their behaviour is the evidence for that declaration: the shuffle destroys the twin's and the bigram's real
token-to-token transitions, so the gain over them inflates instead of collapsing.
- N5 full vs twin: real 0.531062, controls mean 0.496911, max 0.536340, 4 of 400 at or above real (61, 67, 114, 376).
- N6 full vs bigram: real 0.128423, controls mean 0.574094, max 0.605964, 400 of 400 at or above real (real is 40.95 sd BELOW the control mean).

## Null-runner speed shims (null runs only; the frozen files were not modified)

- scipy.special.ndtr in place of scipy.stats.norm.cdf, and the vectorised feature code attempts/evaluator/code/fastfeats.py: both checked bit-identical (np.array_equal) to the frozen feats on all 3,418 real positions at each N2 worker start (attempts/evaluator/nulls/N2_w*.log) and on all 17,090 position x fold-edge combinations (attempts/evaluator/nulls/verify_fastfeats.txt).
- einsum gradient in place of the broadcast-and-sum gradient (same objective): on real fold 0 it reproduces the frozen probabilities within 3.1e-9 (full), 2.7e-14 (twin), R1 identical (attempts/evaluator/nulls/verify_fastgrad_N2.txt) and 7.4e-12 for the p3 model (verify_fastgrad_N3.txt). The first N2 controls (indices 0-2) ran with the ndtr shim only and a few more (about 3-9, 134-141, 267-274) with ndtr + einsum before fastfeats existed; N4 ran with no shim; N3 ran with the einsum gradient. Control 2 was computed twice (ndtr only, then ndtr + einsum): the two values agree to about 3e-12 bits (see the duplicated-indices line).
