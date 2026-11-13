# Chactun Maya structures (ECML PKDD 2021 challenge): beat the winning average IoU of 0.8341 on the released 329-tile test set

⚓ **Wrecks and ancient sites** · standard · tractability ★★★☆☆ · compute: laptop-hours to laptop-days (about 2.2 GB on Figshare: lidar visualisations 1.13 GB, canopy height model 218 MB, Sentinel-1 507 MB, Sentinel-2 356 MB, masks 4.7 MB; 480 by 480 pixel lidar and mask tiles at 0.5 m (CHM 240 by 240, Sentinel 24 by 24), a small GPU helps) · open as of 2026-11-13

## The problem

The Discover the Mysteries of the Maya challenge (ECML PKDD 2021, 1 April to 1 July 2021; organisers Dragi Kocev, Nikola Simidjievski, Ana Kostovska, Ivica Dimitrovski and Žiga Kokalj) asked for pixel masks of three kinds of ancient Maya structure around Chactun, Campeche, Mexico: buildings, platforms and aguadas (artificial water basins). Inputs were airborne laser scanning (lidar) visualisations, a canopy height model, Sentinel-1 and Sentinel-2 tiles. Tiles 0 to 1764 were for training; tiles 1765 to 2093 (329 tiles) were the hidden test set. The final leaderboard, read on 2026-11-13, has Aksell first with an overall average IoU (intersection over union) of 0.8341, then ArchAI 0.8316, German Computer Archaeologists 0.8275, dmitrykonovalov 0.8262 and The Sentinels 0.8183. The organisers' DeepLabV3 baseline is given as 0.76787 in the challenge's Baseline section (buildings 0.66005, platforms 0.65877); its final-leaderboard row shows different values (0.7676 overall, buildings 0.6617, platforms 0.6662). Kokalj and colleagues (Scientific Data 10, 558, 2023) later released all 2,094 tiles with their masks, keeping the challenge numbering and including the 329 test tiles, on Figshare under CC BY 4.0. The papers citing that release that were checked on 2026-11-13 use their own splits or other data, and no result above 0.8341 on the official test tiles was found. Open task: a model trained only on the training tiles that beats 0.8341 on the official test tiles.

## What counts as a win

A model trained only on tiles 0 to 1764 (validation carved from those tiles; declared public pretraining allowed). No pretraining, self-supervision or pseudo-labelling on tiles 1765 to 2093, and no use of their masks for training, model selection or thresholds. Its 987 predicted masks for tiles 1765 to 2093 are scored with the challenge metric: for each class, the mean over the 329 tiles of the per-tile IoU, counting IoU = 1 when prediction and ground truth are both empty; the overall score is the mean of the three class averages. The challenge pages do not state the empty-mask rule, so the scoring code must first reproduce the score of all-empty masks on the 329 test tiles (overall 0.5876; aguadas 0.9574, buildings 0.3495, platforms 0.4559, equal to the final-leaderboard row of Valeriya_Mashkina; the comp page's empty-mask baseline of 0.5745 was scored on the public-leaderboard subset) to 4 decimals on the released masks, which fixes the conventions. The win: an overall score STRICTLY GREATER than 0.8341 (direction: max) by at least 0.003, as the mean over at least 3 training seeds, and above any higher official-split value published before the claim. Deliverables: code, seeds, saved test masks and scoring logs.

## Partial wins

- **p1:** A single model, with no ensembling and no test-time augmentation, whose mean overall score over 3 seeds exceeds 0.8275 (the third-place entry), scored as in the success criterion.
- **p2:** Hard classes: mean building-class and platform-class average IoUs over 3 seeds that both exceed the organisers' DeepLabV3 baseline values (buildings 0.66005, platforms 0.65877, read on 2026-11-13) by at least 0.05, scored as in the success criterion.
- **p3:** Data efficiency: a model trained on a random 25% of the training tiles, with the tile list committed before training, whose mean overall score over 3 seeds exceeds the DeepLabV3 baseline of 0.76787.

## How a win is checked

The verifier downloads the Figshare files, checks the tile numbering, runs the submitted scoring code on all-empty masks (it must give 0.5876 overall and the three stated class values) and then rescores the saved test masks. They re-train one seed from the logged configuration and check that its score is within 0.005 of the reported mean, and they read the training logs to confirm that no file of tiles 1765 to 2093 was opened before the final evaluation.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://biasvariancelabs.github.io/maya_challenge/about>

## Sources

- <https://biasvariancelabs.github.io/maya_challenge/about>
- <https://biasvariancelabs.github.io/maya_challenge/comp>
- <https://pmc.ncbi.nlm.nih.gov/articles/PMC10447422/>
- <https://doi.org/10.6084/m9.figshare.22202395>
- <https://api.figshare.com/v2/articles/22202395>
- <https://arxiv.org/abs/2208.03163>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Conventional: U-Net or SegFormer on several relief visualisations (sky-view factor, openness, local dominance) stacked as channels, as most top teams used lidar only.
- Cross-domain import (building-footprint extraction from SpaceNet): boundary-aware losses and instance separation for small adjacent buildings and platforms.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The test masks are public, so leakage is easy; anything tuned or selected on tiles 1765 to 2093 is void.
- Many papers re-split the 2,094 tiles or report IoU pooled over all pixels; those numbers are not comparable with the leaderboard.
- Aguadas are rare (95 in the whole study area), so all-empty masks already score 0.9574 on them and the top entries about 0.98; the race is in buildings and platforms.
- The challenge page describes 8-bit masks with 0 meaning structure and 255 empty, while submissions used boolean arrays with True for structure; check the polarity before scoring.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/lost-and-hidden/chactun-maya-structures-official-test-iou.md
```

Already set up? Say `run V3R1T4S on chactun-maya-structures-official-test-iou`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `chactun-maya-structures-official-test-iou`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
