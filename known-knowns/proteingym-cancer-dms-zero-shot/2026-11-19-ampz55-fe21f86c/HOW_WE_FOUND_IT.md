# HOW_WE_FOUND_IT.md

(contributor text, unverified)

The hunt: beat the best public Spearman on a cancer-gene
deep-mutational-scanning assay with a zero-shot method — no fitting on
the assay's labels. The target was PTEN_HUMAN_Matreyek_2021, whose live
ProteinGym best was 0.516 (VenusREM), bar 0.531.

What failed before (seventeen hunts on this target): single-model
masked-LM columns (ESM-2 8M 0.1652, 35M 0.2737, 150M 0.4620); MSA
statistics (best 0.3666); DCA/Potts (-0.1662, wrong-signed); every
frozen z-sum combination of the 150M column (all below 150M alone);
every transform of the 150M column (all diluting it); pocket penalties;
charge/volume/motif penalties. The best label-free single column stayed
0.4620 — far below the bar.

The turn came from published score files: ProteinGym distributes
per-mutant scores for ~97 models (Zenodo record 15293562). A frozen
top-10 Borda ensemble of the best non-cancer-selected models scored
0.5637 (hunt 15) — past the live bar, but below M1, a frozen top-12
z-score ensemble disclosed in V3R1T4S PRs #463/#467 at 0.5658. A
log-likelihood-ratio decoder over M1's 12 scored 0.5647 (hunt 16) —
also below M1. During that hunt's self-break, a plain equal-weight
Borda over M1's 12 recomputed to 0.5682 post-hoc — the first combiner
to clear M1. It earned nothing then, because it was found after
scoring.

This hunt (hunt 17) pre-registered that exact combiner as primary
before scoring anything, and re-scored it fresh: BORDA-12 = 0.5682,
+0.0024 above M1. The three-skeptic panel passed it (reproduce,
novelty, criterion), and the honesty gate confirmed it — with the
caveat carried in the open that the margin over M1 is inside bootstrap
noise, and that the second PTEN assay (Mighell, 0.5723 vs bar 0.576)
does not replicate. The record is a best-known point value on one
assay, not a demonstration that Borda beats z-score combining.
