# AI4Shipwrecks side-scan sonar benchmark: beat the best published site-averaged shipwreck IoU (0.445) on the official site-disjoint test split

⚓ **Wrecks and ancient sites** · standard · tractability ★★★☆☆ · compute: laptop-hours (one consumer GPU helps; 286 labelled sonar images with masks, total size not stated on the project page) · open as of 2026-11-13

## The problem

AI4Shipwrecks (Sethuraman, Sheppard, Bagoren, Pinnow, Anderson, Havens and Skinner, University of Michigan Field Robotics Group with Michigan Tech and NOAA Thunder Bay National Marine Sanctuary; arXiv 2401.14546 v2 of 2024-08-27; International Journal of Robotics Research 2024) is a set of 286 high-resolution side-scan sonar images of 28 wrecks in Lake Huron, with pixel masks for two classes, shipwreck and other. Side-scan sonar is a sonar on a vehicle that images the seabed to each side of its track. The official split is 50/50 and site-disjoint: Table 4 of the paper lists 14 training and 15 test sites, so no wreck appears in both. The score is the intersection over union (IoU, overlap divided by union of predicted and true wreck pixels) of the shipwreck class, computed per test site and then averaged over sites. Best published value read on 2026-11-13: 0.445 (SOD, the InSPyReNet salient-object network, Table 5; F1 0.594, true positive rate 0.652), then U-Net 0.411. Later work has not beaten it: BenthicDINO (Hamoda, Rajani and Gracias, arXiv 2608.23215 v2, 2026-10-16) reports 0.423 with a frozen self-supervised encoder and a U-Net decoder over 13 wreck-bearing test sites, second of seven; the weakly supervised method of Baker, Emigh and Brockmeier (arXiv 2506.22505 v2, 2025-11-04) reports 0.36 over 12 sites. The data are on the University of Michigan Deep Blue repository, released 2024-01-25.

## What counts as a win

A model trained only on the 14 official training sites (any validation set carved from those sites only; declared public pretraining allowed) whose shipwreck-class IoU, computed per test site in pixel space on the full official test images and averaged over the test sites that contain shipwreck pixels in the released labels (the list of sites used is part of the claim), is STRICTLY GREATER than 0.465 (direction: max; the published best 0.445 plus a 0.02 margin) as the mean over at least 3 training seeds. The same evaluation code must reproduce a plain U-Net baseline at 0.411 plus or minus 0.03 on the same site list, which shows the protocol matches the paper. No test image may be used for training, self-supervised pretraining, model selection or threshold tuning, and no pretraining corpus may contain Thunder Bay side-scan surveys of the test sites. The claim must also beat every value on this split in any paper or preprint dated before the claim, found by an arXiv search for AI4Shipwrecks re-run on the claim date. Deliverables: code, seeds, per-site IoU table, saved test masks and logs.

## Partial wins

- **p1:** With the encoder fully frozen (a public pretrained encoder, only a decoder trained on the training sites), a site-averaged test IoU above 0.433, which beats the BenthicDINO frozen-encoder value 0.423 by at least 0.01, mean over 3 seeds, on the same site list as the full criterion.
- **p2:** Using only image-level labels (wreck present or absent) from the training sites, a site-averaged test IoU above 0.38, which beats the 0.36 of Baker, Emigh and Brockmeier by at least 0.02, mean over 3 seeds.
- **p3:** A model whose site-averaged test F1 for the shipwreck class exceeds 0.614 (the SOD value 0.594 plus 0.02) while its site-averaged true negative rate stays at or above 0.995, mean over 3 seeds.

## How a win is checked

The skeptic downloads the dataset from Deep Blue, checks the train and test site lists against Table 4 of the benchmark paper, recomputes per-site IoU from the saved test masks with their own code, compares the U-Net reproduction, re-runs the arXiv search for later results, and retrains one seed from the released code. Under a day on one GPU.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://export.arxiv.org/api/query?search_query=all:AI4Shipwrecks&sortBy=submittedDate&sortOrder=descending&max_results=25>

## Sources

- <https://arxiv.org/abs/2401.14546>
- <https://umfieldrobotics.github.io/ai4shipwrecks/>
- <https://deepblue.lib.umich.edu/data/concern/data_sets/8623hz41x>
- <https://github.com/umfieldrobotics/ai4shipwrecks-scripts>
- <https://arxiv.org/abs/2608.23215>
- <https://arxiv.org/abs/2506.22505>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Use the shadow geometry: side-scan wrecks cast acoustic shadows whose length follows the sonar grazing angle, a physical cue that augmentations can preserve.
- Self-supervised pretraining on public side-scan surveys that exclude the Thunder Bay test sites, then fine-tune the whole network rather than freezing it.
- Cross-domain import (medical imaging): small-lesion segmentation losses such as Tversky or boundary losses for a class that covers about 3% of test pixels.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The dataset licence is shown on the Deep Blue record, which returned HTTP 403 to automated fetches on 2026-11-13 and is unread; the project page and paper call the data open source but name no licence, so the human reads the record terms before download.
- Papers average over different site sets (the benchmark says all test sites, BenthicDINO uses 13 wreck-bearing sites, Baker and colleagues 12); only a run that also reproduces U-Net at about 0.411 on its own site list is comparable with 0.445.
- Site-averaged and pixel-pooled IoU differ a lot on this set; never compare a pooled value with 0.445.
- Strided crops of one image overlap; never let crops of a test site leak into training or validation.
- The BenthicDINO abstract says its frozen features beat supervised baselines, but its own Table IV ranks it second behind SOD; read the tables, not the abstracts.
- Detection scores such as mAP50 from box detectors are a different task and are not comparable.
- Files named NellieGardner in the paper were renamed Exploratory2 in the dataset, as the project Overview page says.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/lost-and-hidden/ai4shipwrecks-sidescan-segmentation-iou.md
```

Already set up? Say `run V3R1T4S on ai4shipwrecks-sidescan-segmentation-iou`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `ai4shipwrecks-sidescan-segmentation-iou`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
