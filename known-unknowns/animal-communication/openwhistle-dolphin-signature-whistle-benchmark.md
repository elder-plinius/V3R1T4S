# OpenWhistle bottlenose dolphin whistles: beat the best published session-held-out macro-F1 for signature-whistle identity, or the best whistle-type detection mAP

🐋 **Animal communication** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours for frozen-encoder probes, laptop-days for end-to-end fine-tuning (a GPU helps); classification set 4.64 GB and detection set about 237 MB of Parquet audio on Hugging Face, optional 114-hour unlabelled pretraining corpus · open as of 2026-11-13

## The problem

OpenWhistle (Faadil Mustun, Chiara Semenzin, Roberto Dessì, Pablo Robin Guerrero, Pierre Orhan, Alexis Emanuelli, Emanuele Rossi, Yair Lakretz, Gonzalo de Polavieja, Germán Sumbre; arXiv 2609.34839, NeurIPS 2026 Datasets and Evaluations spotlight; code at github.com/sumbre-lab/OpenWhistle) is a public corpus of about 180,000 whistles (114 hours) recorded from November 2019 to March 2024 from a pod of five dolphins at Dolphin Reef, Eilat, a semi-natural open-sea enclosure. A signature whistle is a learned contour each dolphin uses as its own identity call, so classifying signature-whistle types is a caller-identity task. An expert-labelled subset of 8,354 whistles defines three tasks with fixed splits in which no recording session appears in more than one of train, validation and test: balanced classification (6 classes, five signature whistles and one non-signature type; 2,100, 450 and 450 clips), unbalanced classification (10 classes; 5,848, 1,253 and 1,253 clips), both scored by macro-F1, and multi-label detection of 7 whistle types plus background in 0.5 s windows (3,920, 840 and 840), scored by macro-averaged average precision (mAP). Best published test values, read on 2026-11-13 from the repository result tables (commit of 2026-11-07): balanced 85.55 percent macro-F1, unbalanced 64.79 percent and detection 81.44 percent mAP, all by AVES-bio pretrained from scratch on OpenWhistle and then fine-tuned end to end. Best frozen linear probes: balanced 81.40 and detection 79.59 (OpenWhistle wav2vec 2.0), unbalanced 64.75 (AVES-bio continued on OpenWhistle). All are single-seed values with test bootstrap standard deviations of about 1.6 to 3.5 points. Data and weights are CC BY 4.0 and ungated; code is MIT.

## What counts as a win

Pick one cell: balanced classification, unbalanced classification or detection, using dolphinteam/OpenWhistle-Classification-Finetuning at revision 1026daf811f1f134d98a977e0cdd1e1129692497 or dolphinteam/OpenWhistle-Detection-Finetuning at revision c2e89807b51142e106b76d486f4cf620ec63c1fb. The model is selected using only the train and validation splits (refitting on train plus validation is allowed, as in the published protocol). Declared pretraining is allowed, including self-supervised pretraining on dolphinteam/OpenWhistle-Pretraining as the published baselines did, but no test labels and no other labelled OpenWhistle clips. Its test metric, computed with the repository metric code (macro-F1, or macro-averaged AP over the 7 labels) and averaged over at least 3 training seeds, must be STRICTLY GREATER (direction: max) than the published best for that cell by at least 1.0 percentage point: above 86.55 balanced, above 65.79 unbalanced, above 82.44 detection. It must also beat any newer published value for that cell that the NOVELTY skeptic finds. Deliverables: code, weights, seeds, saved test predictions for every seed and the scorer output.

## Partial wins

- **p1:** Frozen-encoder cell: keeping the encoder frozen and using the repository logistic-regression probe protocol (C chosen on validation, final probe fit on train plus validation, seed 42), beat the best published probe value of one cell by at least 1.0 point: above 82.40 balanced, above 65.75 unbalanced or above 80.59 detection.
- **p2:** Off-the-shelf transfer: an encoder that has never seen OpenWhistle audio whose frozen probe exceeds AVES-bio's published balanced value of 75.13 by at least 2.0 points, or BioLingual's published detection value of 66.52 by at least 2.0 points.
- **p3:** A model with at most 10 million parameters whose 3-seed mean balanced macro-F1 exceeds 81.40, the best published frozen probe of any size.
- **p4:** One trained encoder (separate heads per cell allowed) that beats the published best of two of the three cells at once, each by at least 0.5 points as 3-seed means.

## How a win is checked

The skeptic downloads both datasets at the pinned revisions, confirms that the session lists of train, validation and test are disjoint, reruns the claimant's inference on the test split and recomputes the metric with the repository scorer from the saved predictions. They retrain one seed to confirm it falls within the reported spread, read the training logs to confirm that model selection used validation only, and check the declared pretraining data for labelled OpenWhistle clips.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://github.com/sumbre-lab/OpenWhistle>

## Sources

- <https://arxiv.org/abs/2609.34839>
- <https://github.com/sumbre-lab/OpenWhistle>
- <https://github.com/sumbre-lab/OpenWhistle/blob/main/experiments/benchmark/README.md>
- <https://github.com/sumbre-lab/OpenWhistle/blob/main/experiments/finetuning/README.md>
- <https://huggingface.co/datasets/dolphinteam/OpenWhistle-Classification-Finetuning>
- <https://huggingface.co/datasets/dolphinteam/OpenWhistle-Detection-Finetuning>
- <https://sumbre-lab.github.io/openwhistle/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Signature-whistle identity lives mostly in the contour shape: the classification dataset ships F0 tracks and F0 spectrograms, so a time-warping-tolerant contour classifier fused with audio embeddings is a cheap first try.
- Cross-domain import (speaker verification): margin losses such as additive angular margin softmax, built for identity, applied to whistle identity.
- Several band-limited views of the 44.1 kHz audio, as the continued AVES-bio model used, to keep harmonics above 8 kHz.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- The test sets are small (450 clips for balanced), so single-seed gains under about 2 points are within the bootstrap noise.
- Integer labels differ between the balanced and unbalanced configs; map classes by name.
- NSW_3, NSW_2 and SW_Shy have very few test clips in the unbalanced config, so its macro-F1 moves with a handful of clips.
- The OpenWhistle self-supervised models were pretrained on the whole five-year corpus, which may overlap the labelled sessions in time; this unlabelled use is allowed only because the published baselines did the same, and it must be declared.
- The arXiv tables and the project page carry older numbers (for example 81.67 balanced and 80.80 detection); compare only with the repository result tables.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/animal-communication/openwhistle-dolphin-signature-whistle-benchmark.md
```

Already set up? Say `run V3R1T4S on openwhistle-dolphin-signature-whistle-benchmark`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `openwhistle-dolphin-signature-whistle-benchmark`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
