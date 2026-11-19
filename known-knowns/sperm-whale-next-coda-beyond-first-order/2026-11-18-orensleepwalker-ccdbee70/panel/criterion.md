# Criterion skeptic

context: fresh subagent

confirmed_scope: On the pinned sperm-whale-dialogues.csv benchmark, the preregistered training-fold-selected categorical pipeline scored 2.564371 bits per coda over 3,418 positions versus 2.794781 for R1 and 2.850952 for its retrained one-coda twin, with a fresh paired recording-bootstrap 95% interval of 0.241386 to 0.345250 bits for the gain over the twin.

I verified every frozen checksum. My independent evaluation rebuilt the sorted REC folds, file-order tie handling, training-only bin edges, scored row and token IDs, R1's inner-selected smoothing, the four full-history families' inner selection, and the matching order-3 full and cut forecasts. All selected probability vectors were positive, normalized, and matched the independent arrays. Order-3 won inner selection in all five folds. Across 188 scored recording groups, a fresh 10,000-draw paired resample also put the R1 gain of 0.230410 bits in an interval of 0.183686 to 0.289804. Both point margins exceed the bank's 0.10 and 0.05 requirements. Altering the predicted coda's available fields at each of the 3,418 fixed scored positions left all same-position feature inputs unchanged. REC and onset establish stream assignment and ordering upstream.

The cut twin is the same hierarchy retrained with only the prior token and two constant inputs, using separately inner-selected smoothing. The repeated constant levels apply the same previous-token counts three times, which changes effective shrinkage relative to a collapsed one-level model. An independently fitted single-level sensitivity scored 2.786314 bits, with a gain of 0.221943 and interval of 0.180039 to 0.280799. I did not replay matched nulls for that sensitivity.

I recomputed the maxima from both complete 400-seed logs and exactly replayed three seeds from each using the frozen implementation. For the same prespecified nested selector, the payload control maxima were 0.200664 against R1 and 0.256013 against the twin. The first-order control maxima were 0.095298 and 0.160038. Both observed gains beat all controls for the frozen selector. Picking whichever named family has the largest outer-score gain on each surrogate is a different decision rule. Under that sensitivity, five payload controls exceed the observed twin gain and the maximum reaches 0.318323. The verdict applies to the fold-selected pipeline. The transition-preserving surrogates preserve adjacency in each recording under its held-out edges and are diagnostic rather than uniform exact randomization tests.

pass: true
