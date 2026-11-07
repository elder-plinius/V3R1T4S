# The Record We Beat

- **Source URL**: https://github.com/CAMI-challenge/second_challenge_evaluation/tree/master/binning/genome_binning
- **Target Specification**: `known-unknowns/genomics/cami2-genome-binning-recovered-genomes.md` (`bank/targets.json`)
- **Fetched UTC**: 2026-11-07T06:30:00Z
- **Reference Snapshot SHA-256**: `e817761a192a49bf80ca70fa62d42989e89012ffde2fb4089e3c6b532f7a0b42`
- **Published Records Beaten**:
  - `p1` (`strain-madness` pooled GSA): `86 > 77` HQ genomes (beating `CONCOCT 0.4.1` at `77`, `ARI = 0.601167` vs `0.400`).
  - `p2` (`plant-associated` pooled GSA): `135 > 118` HQ genomes across all 831 reference genomes (beating `VAMB 3.0.1` at `118`) and `90 > 72` on the 495-genome no-plasmid evaluation (beating `MetaBinner 1.2` at `72`), with `ARI (bp) = 0.943731`.
  - `p3` (`marine` pooled GSA): `328 >= 300` HQ genomes (`nocircular`; `429` all genomes) AND `ARI (bp) = 0.936349 > 0.887` in a single binning.
