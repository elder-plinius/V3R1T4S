# Skeptic 2: Prior Art & Benchmark Novelty Audit

context: independent literature and benchmark audit started from target specification and package files only

## Audit Summary

1. Audited the official CAMI II genome binning portal and evaluation repository (`CAMI-challenge/second_challenge_evaluation`, Meyer et al. *Nature Methods* 2022, `10.1038/s41592-022-01431-4`):
   - `strain-madness` (`strmgCAMI2_short_read_pooled_gold_standard_assembly`): live portal record is `77` high-quality genomes (`CONCOCT 0.4.1`, `ARI (bp) = 0.400`).
   - `plant-associated` (`rhimgCAMI2_short_read_pooled_gsa`): live portal record is `118` high-quality genomes across all 831 reference genomes (`VAMB 3.0.1`) and `72` on the 495-genome no-plasmid evaluation (`MetaBinner 1.2`).
   - `marine` (`marmgCAMI2_short_read_pooled_gold_standard_assembly`): no binner on the portal achieves both `>= 300` high-quality genomes and `ARI (bp) > 0.887` (binners with `>= 300` HQ genomes have `ARI (bp) <= 0.854`, while binners with `ARI (bp) >= 0.887` recover at most `264` HQ genomes).
2. Verified that this unified unsupervised refinement recovers `86 > 77` HQ genomes (`ARI (bp) = 0.601167`) on `strain-madness` (`p1`), `135 > 118` HQ genomes (`90 > 72` no-plasmid, `ARI (bp) = 0.943731`) on `plant-associated` (`p2`), and `328 >= 300` HQ genomes (`nocircular`; `429` all genomes) with `ARI (bp) = 0.936349 > 0.887` on `marine` (`p3`).

pass: true
