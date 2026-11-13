# Open-Canopy: beat PVTv2's 2.52 m test MAE for 1.5 m canopy height from SPOT 6-7 images against LiDAR HD over France

🌍 **Earth and sky** · standard · tractability ★★☆☆☆ · compute: needs cluster (or one GPU workstation for several days; about 360 GB of SPOT imagery and lidar canopy heights, 423 GB with all files) · open as of 2026-11-13

## The problem

Open-Canopy (Fogel, Perron, Besic, Saint-André, Pellissier-Tanon, Schwartz, Boudras, Fayad, d'Aspremont, Landrieu and Ciais; CVPR 2025; arXiv 2407.09392 version 4, 2024-12-11) is a country-scale benchmark: predict canopy height at 1.5 m from SPOT 6-7 satellite images, scored against canopy height models from the IGN LiDAR HD aerial lidar survey, over more than 87,000 km^2 of France, with test tiles kept 1 km away from training tiles. It is open on Hugging Face (AI4Forest/Open-Canopy, Etalab Open Licence 2.0) with the evaluation scripts, the pretrained models and the test predictions. Best published test values in Table 2, read on 2026-11-13: PVTv2 MAE 2.52 m (nMAE 22.9%, bias 0.00 m, tree cover IoU 90.5%); SWIN with ImageNet-21k pretraining nMAE 22.8%; SWIN with Satlas pretraining tree cover IoU 90.6%. On the change-detection extension Open-Canopy-Delta, PVTv2 has F1 54.1%. A second lidar reference (lidar_v2, January 2025) gives about 0.05 m lower MAE, but the benchmark uses version 1. No later paper beating these values was found.

## What counts as a win

A model trained only on the Open-Canopy train split (validation split for selection; declared pretraining allowed, but no data derived from LiDAR HD or from canopy maps covering the test tiles) whose test MAE, computed with the repository's src/metrics/compute_metrics.py against the version 1 lidar reference (vegetation mask, heights below 60 m), is at most 2.47 m (direction: min; 0.05 m below 2.52 m) and at least 0.05 m below the MAE that the same script gives for the released PVTv2 test predictions, with nMAE no worse than 22.9% and tree cover IoU no worse than 90.5%. Deliverables: code, weights, saved test predictions and the metric output files.

## Partial wins

- **p1:** Test tree cover IoU of at least 91.0% with the repository script, with MAE no worse than 2.60 m.
- **p2:** On Open-Canopy-Delta, a change-detection F1 above 54.1% with the repository's compute_change_detection_metrics.py, using a model trained only on the train split.
- **p3:** Test MAE strictly below 2.52 m (version 1 reference, repository script) but above 2.47 m, with the other conditions of the full criterion.

## How a win is checked

The skeptic downloads the test tiles and the claimant's predictions, runs the repository's metric scripts on them and on the released PVTv2 predictions, and checks the training data list for test-tile leakage. Recomputing the metrics takes hours; retraining is optional.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://github.com/fajwel/Open-Canopy>

## Sources

- <https://arxiv.org/abs/2407.09392>
- <https://github.com/fajwel/Open-Canopy>
- <https://huggingface.co/datasets/AI4Forest/Open-Canopy>
- <https://openaccess.thecvf.com/content/CVPR2025/papers/Fogel_Open-Canopy_Towards_Very_High_Resolution_Forest_Monitoring_CVPR_2025_paper.pdf>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Fine-tune from the released PVTv2 weights with a height-weighted loss for tall trees, where errors dominate the MAE.
- Cross-domain import (monocular depth estimation): scale-aware depth heads and multi-scale decoders transfer to height regression.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Scoring against lidar_v2 lowers MAE by about 0.05 m on its own; only the version 1 reference counts.
- The CVPR supplement lists other MAE values under other settings; compare only with Table 2 and the released PVTv2 predictions.
- Public global canopy maps trained on GEDI are allowed as inputs only if they were not trained on LiDAR HD over the test tiles; declare every input.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/earth-and-sky/open-canopy-france-canopy-height-test-mae.md
```

Already set up? Say `run V3R1T4S on open-canopy-france-canopy-height-test-mae`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `open-canopy-france-canopy-height-test-mae`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
