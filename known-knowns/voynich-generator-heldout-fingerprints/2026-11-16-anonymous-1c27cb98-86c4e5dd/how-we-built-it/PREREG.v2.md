# PREREG.v2 — refinement of PREREG.md (timestamped; the original PREREG.md is unchanged)

Frozen: 2026-11-16 ~12:4x UTC (`date -u` at write), AFTER the precompute step (which
produced no scored lens output) and BEFORE the first lens report is scored. Changes:

1. S1 and H1 shuffle nulls use their EXACT within-line expectation instead of a 100-shuffle
   noisy estimate (the two are the same null; the expectation removes sampling noise and
   makes the pooled observed value and the bootstrap envelopes use ONE consistent
   pipeline):
   - S1_null = MI of the pooled token-level joint distribution
     (P(last-char, first-char) over all tokens of the pool); S1_bits =
     MI(observed boundary pairs) - S1_null; S1_share = S1_bits / H(marginal of the
     next-token first char). (The paper's 100-within-line-shuffle estimate is an
     unbiased estimator of exactly this quantity.)
   - H1_null = expected adjacent edit-1 count under within-line shuffling =
     (2/n_line) * sum_{i<j} [edit1(t_i,t_j)] per line, summed over the pool
     (adjacency probability 2/n for a random permutation of n distinct items).
2. S9: per-page (folio proxy) r_cho computed only on pages with >=5 classifiable
   cho/che words (the paper's Table-7 n=197 filter "folios with >=5 classifiable
   words"; a page with <5 is excluded, matching "folios with >=5").
3. Reproduction-gate tolerances (PREREG §3) refined, because two of the published
   references are computed on a DIFFERENT corpus than the criterion's envelope
   corpora (ZL3b-n.txt / IT2a-n.txt fetched 2026-11-16):
   - 2608.17096 references (S1 0.137/0.248; S2 ~0.70; S3 2.69; H1 1.20/1.07) are
     for their ZL3b build (bundle file, plain separators). Gate: S1 A/B within
     +/-0.02 of 0.137/0.248; S2 within +/-0.05 of 0.70; S3 pooled (A+B, ZL3b)
     within +/-0.40 of 2.69 (corpus-version difference, both "low ~2.2-2.7");
     H1 A/B within +/-0.05 of 1.20/1.07.
   - 2604.19762 references (S5 71.0/64.3%, S7 0.5856/0.4980, S8 shapes) are the
     paper's calibration on ITS RF1b-e corpus + ITS grapheme inventory. For this
     run the criterion mandates envelopes from ZL3b-n/IT2a-n, so S5-S8 are gated as
     CROSS-CORPUS CONSISTENCY checks only (direction and order: A vs B as
     published; absolute values recorded, not matched). The scored comparison is
     always generator-vs-Voynich on the SAME fetched corpus, so this does not
     weaken the claim.
   - S9 references (p1=0.682, p0=0.160 are binomial-mixture POSTERIOR means, not
     raw means): gate = raw per-folio quantities with the >=5 filter: ambiguous
     share [0.3,0.5] within +/-0.06 of 0.068 (published "6.8%"), and the
     cho-state/che-state raw means recorded (expected above/below the mixture
     p1/p0 respectively, by shrinkage).
Everything else in PREREG.md (cells, statistics S2/S3/S4/S5/S6/S7/S8/S9/H2/H3/H4
definitions, the generator design space E1-E4, the falsifier design, hand-
executability limits, the novelty gate) is unchanged.
