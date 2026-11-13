# African elephant name-like rumbles: predict who a call is addressed to better than Pardo et al. (27.5%) and better than the caller's own habits, or across callers

🐋 **Animal communication** · standard · tractability ★★☆☆☆ · compute: laptop-minutes to laptop-hours (Dryad deposit of 42.3 MB: acoustic feature tables and contours for 469 calls, no audio) · open as of 2026-11-13

## The problem

Pardo, Fristrup, Lolchuragi, Poole, Granli, Moss, Douglas-Hamilton and Wittemyer (Nature Ecology and Evolution 8:1353-1364, 2024) studied rumbles of wild African savanna elephants recorded in Samburu, Buffalo Springs and Amboseli, Kenya. A rumble is a low-frequency call. Their data have 469 calls from 101 callers to 117 receivers. The 437 calls whose caller is known went into a random forest that predicts the receiver from acoustic features. The forest used 500 trees and 7-fold cross-validation, with folds stratified by caller and receiver, averaged over 2,000 runs. With spectral features it named the right receiver for 27.5% of calls. The null was 10,000 models trained on permuted features, which scored 8.0% (SD 0.66%). Calls unlike the receiver's own calls scored 32.6% (null 17.9%). Calls like them scored 20.1% (null 7.7%). A second model kept all calls of each caller-receiver pair in one fold, so it had to predict receivers across callers. It scored 1.1% against a null of 1.4% (SD 0.33%, P = 0.896), so there is no evidence yet that different callers use the same label for a receiver. Permuting features also removes cues to the caller's identity. So the 27.5% alone does not separate receiver-specific structure from the caller's habits. The paper handles this with random-forest proximity scores, not with a stronger null. The data are on Dryad (doi 10.5061/dryad.hmgqnk9nj, latest version 2025-09-27, 42.31 MB, CC0). They contain spectral and cepstral feature CSVs, an observational CSV with caller, receiver and context, and acoustic contours (.rds), but no audio. The authors' R code is Zenodo record 10576772 (version 4, 2024-01-28, LGPL-3.0). On 2026-11-13 none of the 31 papers that Europe PMC lists as citing it was a reanalysis by title.

## What counts as a win

Use only the Dryad deposit (n469 revision files) and the 437 calls with a known caller. Freeze a pipeline and evaluate it with the paper's scheme: 7-fold cross-validation with folds stratified by caller ID and receiver ID, mean accuracy over at least 100 fold draws with fresh seeds. The model may take the true caller ID as an input. Its mean receiver accuracy must meet three conditions. (1) It is STRICTLY GREATER (direction: max) than 0.295, which is the paper's 0.275 plus 0.02. (2) It beats by at least 0.02 the caller-habit baseline on the same folds. That baseline predicts, for each test call, the receiver most often addressed by that call's true caller in the training folds, with ties broken at random and the overall most frequent receiver as the fallback. (3) It is above the 99.9th percentile of 1,000 reruns of the same pipeline in which receiver labels are shuffled among calls of the same caller, which keeps each caller's receiver frequencies. Features and hyperparameters must be chosen by nested cross-validation inside the training folds only. Deliverables: code, seeds, per-call predictions for every draw, and the baseline and null outputs.

## Partial wins

- **p1:** Across callers: under folds that keep all calls of each caller-receiver pair together (the paper's hypothesis-3 design), a frozen pipeline reaches a mean receiver accuracy of at least 0.03. It must also beat the 99th percentile of 1,000 feature-permuted reruns of the same pipeline (the paper had 0.011 against a null of 0.014).
- **p2:** Under the paper's 7-fold scheme and its permuted-feature null (1,000 permutations, one-tailed p below 0.001), a mean receiver accuracy strictly above 0.295. The caller-habit condition is not required.
- **p3:** A reproducibility result: re-implement the paper's random forest and land within 0.02 of 27.5%. Then report the caller-habit baseline and the 99.9th percentile of 1,000 within-caller label shuffles on the same folds, and state whether 27.5% exceeds them, with code a skeptic can rerun.

## How a win is checked

The skeptic downloads the Dryad deposit (42 MB) and reruns the claimant's code with new seeds. Using their own script, they rebuild the caller- and receiver-stratified folds and compute the caller-habit baseline and the within-caller shuffle null. They check that no feature or hyperparameter choice used the test folds, and that only the 437 calls with a known caller were scored. This takes minutes to an hour on a laptop.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.ebi.ac.uk/europepmc/webservices/rest/MED/38858512/citations?format=json&pageSize=100>

## Sources

- <https://datadryad.org/dataset/doi:10.5061/dryad.hmgqnk9nj>
- <https://doi.org/10.1038/s41559-024-02420-w>
- <https://savetheelephants.org/wp-content/uploads/2024/06/Nature-Ecology-Evolution-Article.pdf>
- <https://www.biorxiv.org/content/10.1101/2023.08.25.554872v1.full>
- <https://zenodo.org/records/10576772>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Use the raw acoustic contours rather than the derived features: time-series classifiers such as dynamic time warping nearest neighbours or random convolutional kernels, run within each caller.
- Hierarchical models that first remove caller-specific voice structure (for example, residuals after regressing features on caller ID), then classify the receiver from what is left.
- Cross-domain import (speaker verification): treat the receiver as the class and the caller as the nuisance channel, with within-caller cosine scoring.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Caller and receiver are partly aliased: many callers address only one or two receivers, so a model that only recognises the caller can beat chance and even beat 27.5%. That is why the within-caller shuffle null and the caller-habit baseline are required.
- The data are tiny: the median is 2 calls per receiver. Differences of 1 to 2 points between single runs are noise, so average over many fold draws.
- The Dryad record has several versions. The paper's final analysis uses the n469 revision files of 2023-12-25 and 2024-01-06, not the larger 2023 files behind the 2023 bioRxiv preprint. The older Zenodo record 8340196 holds the pre-revision script.
- Context is a confound: caregiving rumbles mostly go to calves. Report whether gains survive stratifying folds by context.
- Any work is computational only, on the deposited data. Playback to wild elephants is outside this target.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/animal-communication/elephant-rumble-receiver-identity-beyond-caller.md
```

Already set up? Say `run V3R1T4S on elephant-rumble-receiver-identity-beyond-caller`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `elephant-rumble-receiver-identity-beyond-caller`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
