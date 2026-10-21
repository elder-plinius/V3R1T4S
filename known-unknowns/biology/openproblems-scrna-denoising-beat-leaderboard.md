# Open Problems single-cell denoising: beat every listed method on the molecular-cross-validation leaderboard

🦠 **Biology** · harvest (many cells or partial wins within reach) · tractability ★★★★☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

Open Problems in Single-Cell Analysis (openproblems.bio, maintained by Wesley Lewis, Scott Gigante, Robrecht Cannoodt and co-authors) benchmarks scRNA-seq denoising with molecular cross-validation (Batson et al. 2019): each dataset's UMI molecules are binomially split into a training and a held-out test count matrix, a method denoises the training matrix, and it is scored by MSE in log-normalised space and by Poisson loss against the held-out counts (both lower is better). The latest public run (S3 results run_2025-08-11_16-45-36, shown as pre-release v1.1.0-rc1 at https://openproblems.bio/benchmarks/denoising/v1.1.0-rc1; on 2026-10-20 the default page shows the older v1.0.0 release (5 methods, 3 datasets) and hides pre-releases) covers 17 datasets. Best MSE values in that run are close together and well above the 'perfect denoising' control: e.g. tabula_sapiens 0.0760 (CellMapper), immune_cell_atlas 0.1241 (CellMapper), openproblems_v1 pancreas 0.2309 (CellMapper), tenx_5k_pbmc 0.1443 (MAGIC). On Poisson loss, no listed method beats the 'no denoising' control on most datasets. Separately, Yuksekgonul et al. (TTT-Discover, arXiv:2601.16175, 2026) reported a MAGIC-derived algorithm improving MSE on PBMC and Tabula Muris lung under the legacy openproblems v1.0 harness (MSE 0.15 / 0.14 vs MAGIC 0.19 / 0.18), with code released; it is not on the live leaderboard. The open question: a method that lowers MSE below every listed method AND the released TTT-Discover algorithm on the v2 datasets, without breaking the Poisson metric.

## What counts as a win

On at least three of the denoising datasets of the latest Open Problems run (live page https://openproblems.bio/benchmarks/denoising/v1.1.0-rc1, or any newer release, and the newest score file under resources/task_denoising/results/ on the openproblems-data S3 bucket, both re-fetched live immediately before claiming), a single frozen method produces denoised matrices whose MSE, recomputed by the skeptic with the official task_denoising metric component on the official train/test split files, is STRICTLY LOWER (direction: min) than every non-control method listed for that dataset by at least 2% relative, AND lower than TTT-Discover's released denoise_ttt.py run by the skeptic on the same files, AND whose Poisson loss is no worse than the best listed non-control method on that dataset. The method may read only the training matrix (never test.h5ad), must finish within the task's resource limits, and the configuration must be frozen before any test-set scoring.

## Partial wins

- **p1:** On one dataset, beat every listed non-control method on MSE by >= 2% relative while keeping Poisson loss no worse than the best listed method, with the skeptic re-running the official metric.
- **p2:** Beat the 'no_denoising' control on Poisson loss on at least three datasets where no listed method currently does, without increasing MSE above the best listed method on those datasets (a method that improves both metrics at once is what the leaderboard lacks).
- **p3:** Port TTT-Discover's released algorithm to the v2 task API and publish its official v2 scores on all datasets, with an honest table showing where it does and does not beat the live leaderboard.

## How a win is checked

Skeptic downloads train.h5ad and test.h5ad for each claimed dataset from the public openproblems-data S3 bucket (plain HTTPS), runs the attacker's frozen method on train.h5ad alone, then runs the official MSE and Poisson metric components from github.com/openproblems-bio/task_denoising against test.h5ad. Compare with the live page and the newest score_uns.yaml. Re-run TTT-Discover's denoise_ttt.py on the same inputs as an extra baseline. Grep the method code for any read of test.h5ad. Laptop-minutes to an hour per dataset.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://openproblems.bio/benchmarks/denoising/v1.1.0-rc1>

## Sources

- <https://openproblems.bio/benchmarks/denoising/>
- <https://github.com/openproblems-bio/task_denoising>
- <https://openproblems-data.s3.amazonaws.com/?list-type=2&prefix=resources/task_denoising/>
- <https://arxiv.org/abs/2601.16175>
- <https://github.com/test-time-training/discover/tree/main/results/denoising>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Start from the strongest listed methods (CellMapper, MAGIC, DCA) and tune the diffusion / neighbourhood human per dataset only via internal molecular cross-validation on a further binomial split of the TRAINING matrix (the same trick the benchmark uses, applied recursively), never the test file.
- Exploit the known structure of the metric: binomial thinning means the held-out counts are an independent Poisson draw with known sampling fraction, so the MSE-optimal estimator is a shrinkage estimator of the underlying rate; derive it analytically (James-Stein / empirical Bayes per gene) and use smoothing only to estimate the prior.
- Cross-domain import (image denoising): Noise2Self / Noise2Noise-style self-supervised training is exactly molecular cross-validation; borrow BM3D-style 'collaborative filtering' by grouping similar cells and doing low-rank shrinkage within each group rather than one global diffusion.
- Cross-domain import (recommender systems / matrix completion): treat the count matrix as implicit-feedback ratings and use Poisson matrix factorisation with optimal hard-thresholding of singular values (Gavish-Donoho), which is cheap and principled.
- Cross-domain import (geostatistics): kriging on the cell-cell kNN graph with a variogram estimated from training-split residuals gives a principled gene-specific smoothing bandwidth instead of MAGIC's single diffusion time.
- Treat the Poisson-loss failure separately: most smoothers overshrink low counts; a final calibration step that matches each gene's denoised mean and dispersion to the training counts may fix Poisson loss without hurting MSE.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Reading test.h5ad (or the original un-split counts from cellxgene) during fitting is direct leakage; the held-out molecules are the label. The skeptic must run the method in a sandbox with only train.h5ad present.
- Scoring a method on the legacy openproblems v1.0 harness (as TTT-Discover did) and comparing to v2 leaderboard numbers is not like-for-like: datasets, normalisation and metric code differ. Only the v2 metric components on v2 files count.
- Optimising MSE alone can wreck the Poisson metric (and vice versa); a claim must report both and satisfy the Poisson clause.
- Per-dataset hyperparameter search against the test split, even 'just to pick the diffusion time', is overfitting to the scorer. Hyperparameters must come from internal splits of the training matrix only.
- The leaderboard moves: new methods are added between runs. Re-fetch the S3 results listing and the live page immediately before claiming.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/biology/openproblems-scrna-denoising-beat-leaderboard.md
```

Already set up? Say `run V3R1T4S on openproblems-scrna-denoising-beat-leaderboard`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `openproblems-scrna-denoising-beat-leaderboard`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
