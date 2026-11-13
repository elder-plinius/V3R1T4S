# Open-Insect: flag images of likely undescribed moth species from Barro Colorado Island better than CUBE (AUROC 96.1)

🦋 **Undescribed life** · standard · tractability ★★☆☆☆ · compute: laptop-days (C-America split: 72,188 training, 80,000 auxiliary and 18,163 test images from the public resized-image bucket, likely tens of GB; metadata about 1 GB; a GPU helps) · open as of 2026-11-13

## The problem

Open-Insect (Chen, Lang, Schmidt, Jain, Basset, Beery, Larrivée, Rolnick; NeurIPS 2025 Datasets and Benchmarks; arXiv 2503.01691v2) is an open-set recognition benchmark for moths: a classifier trained on the known species of a region must also flag images of species it has never seen. It covers NE-America, W-Europe and C-America, with closed-set, local open-set (species from a slightly larger surrounding area), non-local and non-moth splits, plus O-BCI: 197 images from Barro Colorado Island, Panama, of 133 species absent from the closed set, of which 59 (57 in the Table 1 caption) are likely undescribed, with more than 1.5% COI barcode divergence from their closest BOLD match. Metric: AUROC (area under the ROC curve) with open-set images as positives and closed-set test images as negatives. Best values read on 2026-11-13: on BCI, AUROC 96.1, FPR95 (false positive rate at 95% true positive rate) 16.1 and closed-set accuracy 94.9 by CUBE (Tan, Zhang, Xiao, Zuo, Liu, Qin; arXiv 2610.13610, 9 October 2026, Table 2; ConvNeXt-T with BioCLIP features; no code released). Local open-set AUROC: C-America 96.0 (CUBE-E, which also uses location), W-Europe 86.0 (MSP, TempScale and RP-MSP) and NE-America 87.4 (Energy with auxiliary data), the last two from Open-Insect Table 2 with a ResNet-50 trained from scratch. Data: Hugging Face yuyan-chen/open-insect (metadata and image URLs, CC BY-NC-SA 4.0, not gated; GBIF images keep their own open licences) and yuyan-chen/open-insect-bci.

## What counts as a win

A model trained only on Open-Insect C-America training data (train_id and train_aux; val_id and val_aux for selection and thresholds) plus declared, named pretrained weights, scored with the 197 O-BCI images as positives and the 18,163 C-America test_id images as negatives, with AUROC STRICTLY GREATER than 96.1 by at least 0.3 (at least 96.4) and closed-set top-1 accuracy on test_id of at least 94.9%, both as the mean over 3 training seeds. The O-BCI images and the C-America local, non-local and non-moth test images are never used for training, tuning or threshold choice. The pretraining corpus of any weights used must be named and public, and the claim must show that none of the 197 O-BCI images is in it (no match of their BOLD process IDs in the corpus metadata and no near-duplicate by perceptual hash); weights from an undisclosed corpus that may hold insect images are not allowed. Deliverables: code, weights, seeds and saved per-image scores. The win is a better detector of likely new species, never a species identification.

## Partial wins

- **p1:** W-Europe local open-set AUROC above 86.0 (Open-Insect Table 2) with W-Europe closed-set accuracy of at least 88.4%, using only W-Europe training data and pretrained weights whose corpus contains no moth images (for example ImageNet-1K), mean over 3 seeds.
- **p2:** NE-America local open-set AUROC above 87.4 (Open-Insect Table 2) with NE-America closed-set accuracy of at least 89.7%, under the same constraints as p1.
- **p3:** On O-BCI against C-America test_id, FPR95 below 16.1 with closed-set accuracy of at least 94.9%, mean over 3 seeds, under the rules of the success criterion.

## How a win is checked

The skeptic fetches metadata and images with the Open-Insect repository scripts, runs the supplied weights on O-BCI and the test_id split, recomputes AUROC, FPR95 and accuracy with standard library code from the saved scores, checks that training lists exclude every test image, repeats the process-ID and perceptual-hash check of the O-BCI images against the named pretraining corpus, and retrains one seed.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://export.arxiv.org/api/query?search_query=all:%22Open-Insect%22&sortBy=submittedDate&sortOrder=descending&max_results=20>

## Sources

- <https://arxiv.org/abs/2503.01691>
- <https://yuyan-c.github.io/open-insect-project/>
- <https://github.com/RolnickLab/Open-Insect>
- <https://huggingface.co/datasets/yuyan-chen/open-insect>
- <https://huggingface.co/datasets/yuyan-chen/open-insect-bci>
- <https://arxiv.org/abs/2610.13610>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- The Open-Insect paper finds that methods strong on the C-America local open-set also do well on BCI, so tune on the local split's validation analogue, never on BCI.
- Auxiliary species chosen to resemble the open set helped most in the paper (a 4.8 point drop in local AUROC when they were replaced with TinyImageNet); taxonomically close auxiliary moths are the obvious lever.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- CUBE does not say which negatives it used for its BCI AUROC and released no code; the claim uses C-America test_id as negatives and says so.
- With only 197 positives, AUROC differences of a few tenths are within seed noise; report all seeds.
- The O-BCI images carry BOLD process IDs, and newer foundation models trained on BOLD images (for example corpora behind BioCLIP 2) may contain them; run the process-ID and near-duplicate check before using any such weights. Weights trained on GBIF, iNaturalist or BOLD images are not allowed for p1 and p2.
- Images are fetched from GBIF publishers or the resized bucket; a few URLs may have died. Report how many test images were scored, and the claim fails if any test_id or O-BCI image is missing.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/new-species/open-insect-bci-undescribed-moth-detection.md
```

Already set up? Say `run V3R1T4S on open-insect-bci-undescribed-moth-detection`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `open-insect-bci-undescribed-moth-detection`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
