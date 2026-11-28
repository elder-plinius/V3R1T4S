# Baseline record (kit step 3c)

No published *peer-reviewed* baseline exists for this exact setup, but this section as first written was wrong on
two points, corrected here after the NOVELTY skeptic checked it:

1. **A public in-cell value does now exist.** V3R1T4S draft PR #1159 (another contributor, 2026-11-18) reports
   2.564371 bits per coda on this exact setup, with R1 2.794781 and twin 2.850952, and is the first public
   clearance of the full criterion. It is an unmerged draft, not a publication, but it is the number this claim
   has to beat, and it does: 2.1238 against 2.564371. PR #1175 (2026-11-19) is the comparable public value for
   p4: 0.780268 against this claim's 0.7631118.
2. **WhaleLM does report absolute perplexities.** WhaleLM (bioRxiv 2024.10.31.621071) plots absolute perplexity
   values under its own tokenisation, not only relative changes. Its numbers are still not comparable with this
   claim's, because the token set, the scored rows and the data split all differ, and no code was released; but
   the earlier wording ("reports only relative perplexity changes") misstated what that paper contains. The
   bank's own entry carries the same misstatement, which is worth reporting upstream.

Sinha and Chavan (arXiv 2606.16084, 2609.16612, 2610.33974) use other corpora (1,483 to 1,952 audio codas) and
other tokens, and the bank calls their numbers context, not baselines.

The criterion itself defines the baseline: reference R1, a bigram over the 50 tokens with additive smoothing chosen
from {0.01, 0.03, 0.1, 0.3, 1} by inner cross-validation on the training folds. It is computed here from that
definition (code/swlib.py: r1_select_alpha, r1_fit), with the same data, folds, bins, scored set and metric as the
model. The data file is the one named by the bank (sha256 above, size equal to the bank's 500,380 bytes).

R1 as computed (result/content_summary.json): alpha chosen 0.3 in every outer fold; held-out bits per coda by fold
2.8708, 3.0440, 2.9201, 2.3700, 2.3335; pooled 2.7802 over 3,418 codas. There is no published R1 value to compare
with; a skeptic recomputes R1 independently from the definition.
