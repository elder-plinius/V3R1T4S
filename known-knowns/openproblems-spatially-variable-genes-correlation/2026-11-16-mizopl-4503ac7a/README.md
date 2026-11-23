# Open Problems Spatially Variable Genes (`openproblems-spatially-variable-genes-correlation`): Variance-Stabilized Adaptive Multi-Scale Spatial Autocorrelation (`AMS-SVG`)

## What

Variance-stabilized adaptive multi-scale spatial autocorrelation in object/method.py (sha256 4503ac7a6e97aa6816353b486e8c87f7b64f5caeba32c6ae3f486eb6f44a7336), developed on 4 datasets and evaluated once zero-shot across 46 blind holdout datasets (object/benchmark_50_datasets.json, sha256 db67ac4b9c4a99dac1da6b915c5235263bd65a23cdd8a8bdac87a68f1e412df1), achieves 50-dataset mean gene-wise Kendall tau-b 0.945981 (46-holdout mean 0.953362 vs Zenodo 18193366 leader SPARK-X 0.884811), exceeds every non-control method by at least 0.02 on 37 of 50 Zenodo datasets and 30 of 50 datasets against both Zenodo 18193366 and Seqera v1.0.0 across 7 spatial technologies (Main Goal), scores 0.797905 on 42_slide_tag_human_skin_melanoma (+0.093668 over Zenodo SPARK-X 0.704236 and +0.099705 over Seqera spark_x 0.698200) while remaining within 0.007976 of Seqera leaders on all 20 10x Visium datasets (p1), stays within 0.02 of the best listed non-control method on all 50 of 50 datasets on CPU (p2), and provides controlled single-factor confounder ablations plus a dual-regime capture-dropout benchmark with companion operator object/ams_svg_eb_v2.py (sha256 4c27e2538339e69f18061879d5418afd2a1ea1de14355b649860ae5cd097b05f) in object/ablation_p3.json and object/depth_paradox_benchmark.json (p3), scoped strictly to scDesign3 Negative Binomial Gaussian-process simulations without claiming biological specificity or wet-lab superiority on primary tissue.

- **Central Operator Files:** [`object/method.py`](./object/method.py) (`sha256: 4503ac7a6e97aa6816353b486e8c87f7b64f5caeba32c6ae3f486eb6f44a7336`) and [`object/ams_svg_eb_v2.py`](./object/ams_svg_eb_v2.py) (`sha256: 4c27e2538339e69f18061879d5418afd2a1ea1de14355b649860ae5cd097b05f`)
- **Evaluation Certificates:** [`object/benchmark_50_datasets.json`](./object/benchmark_50_datasets.json) (`sha256: db67ac4b9c4a99dac1da6b915c5235263bd65a23cdd8a8bdac87a68f1e412df1`), [`object/ablation_p3.json`](./object/ablation_p3.json) (`sha256: 8b2b6667995ded2828927780989332ced5691e5947ee789dff33c7d0175d60cc`), [`object/depth_paradox_benchmark.json`](./object/depth_paradox_benchmark.json) (`sha256: 0dd042297449f2ad6927342ad49e79b2216e607ddf1a687aa555614a6c6980f3`), [`object/wave2_eb_v2_benchmark_50.json`](./object/wave2_eb_v2_benchmark_50.json) (`sha256: dd71e591abc468ef605e478acbb90faf39867e30bc4e1f638664852b30d1c39c`), [`object/bayes_ceiling_dev4.json`](./object/bayes_ceiling_dev4.json) (`sha256: 5550fa4f68a9dcf45795dd72a28b41cf5a9fbaba8a34e476683da124e2cfb1a0`), and [`object/verification_certificate.json`](./object/verification_certificate.json) (`sha256: 2585c5fdb2daee04730e5c0341537a69f208215bca83758eff6b69f98ac0bc7c`).

**In plain language:** Spatial transcriptomics measures gene activity together with `(x, y)` coordinates across thousands of cells or capture spots in a tissue slice, and a foundational task is ranking genes by how coherently their expression forms spatial patterns rather than spatially random shot noise. Existing detectors split into two incompatible camps: global library-size-normalized methods (`MoranI`, `SpatialDE2`, `nnSVG`, `SPARK`, `SpaGFT`) that divide each spot's counts by total spot counts $L_s = \sum_g Y_{s,g}$ — accurate on uniform grids when $L_s$ reflects technical depth, but degraded on irregular single-nucleus `slide-tags`, `MERFISH`, `Stereo-seq`, and compartmented solid tumors where $L_s$ carries biological compartment structure — versus unnormalized projection tests (`SPARK-X`), which avoid $1 / L_s$ contamination on clean simulated counts but lose sensitivity to localized domains, tie at IEEE-754 float64 `p < 1e-300`, and degrade when wet-lab spots suffer technical capture dropout. `object/method.py` combines gene-marginal `log1p` + Freeman-Tukey variance stabilization, locally density-adapted biweight kNN + `O(2)`-invariant low-rank Mercer operators, and unbounded Cliff & Ord analytical permutation $Z$-scores; `object/ams_svg_eb_v2.py` adds Hilbert-sphere geodesic arc-length quadrature (`arccos(R_{s,s+1})`) and a scale-separated Wiener + deflated-spectral Empirical-Bayes high-pass capture gate.

## Check it yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
sh verify-it-yourself/run_checks.sh --corrupt   # negative control: exits 1 with final line FAIL
```

- **Dependencies:** Python 3.9+ with `numpy`, `scipy`, `pandas`, and `anndata` (`0` GPU required). On first run without cached `.h5ad.gz` slices in `~/.cache/openproblems_svg_zenodo_18193366/`, `verify-it-yourself/verify.py` fetches only the `12` panel `.h5ad` entries via HTTP Range from `Zenodo 18193366` and verifies each file's CRC32 and SHA-256 before blind scrambling.
- **Runtime:** ~25–45 seconds on a laptop CPU (`0` `.pyc` bytecode side effects).
- **Expected final line:** `PASS` (and `sh verify-it-yourself/run_checks.sh --corrupt` exits `1` with final line `FAIL`).

## Compared to

Full URL, UTC fetch timestamp, HTTP status, and `sha256` snapshot metadata for both `openproblems.bio` `v1.0.0` (`run_2024-09-26_08-24-11`) and Pinello Lab `Zenodo 18193366` are recorded in [`the-record-we-beat/README.md`](./the-record-we-beat/README.md).

### 1. Milestone Evaluation Summary (`50` Datasets: `4` Dev + `46` Blind Holdout)

| Milestone | Quantitative Criterion | Verified Result (`AMS-SVG`, Frozen `object/method.py`) |
| :--- | :--- | :--- |
| **`Main Goal`** | Exceed `#1` non-control method by `>= +0.02` Kendall's $\tau$ across diverse technologies (`>= 5` datasets, `>= 3` technologies) | **`37 / 50` datasets** (`34 / 46` blind holdout) exceed `Zenodo 18193366` `#1` by `>= +0.02`, and **`30 / 50` datasets** (`27 / 46` blind holdout) simultaneously exceed **both** `Zenodo 18193366` `#1` and `Seqera v1.0.0` `#1` by `>= +0.02` across **`7` technologies** (`slide-tags`, `MERFISH`, `Stereo-seq`, `DBiT-seq`, `Slide-seqV2`, `STARmap`, `10x Visium`). `50 / 50` strictly exceed `Zenodo 18193366` `#1` (`mean = 0.945981` vs `#1 SPARK-X = 0.884811`, `+0.061170`). |
| **`p1`** | `>= +0.02` over `#1` on `42_slide_tag_human_skin_melanoma` while within `<= 0.02` of `#1` on `10x Visium` | **`0.797905`** on `42_slide_tag_human_skin_melanoma` (**`+0.093668`** vs `Zenodo #1 SPARK-X = 0.704236`; **`+0.099705`** vs `Seqera #1 spark_x = 0.698200`; `AMS-SVG-EB v2 = 0.799619`), while **`20 / 20`** `10x Visium` datasets are within `<= 0.007976` of `Seqera #1` and **`20 / 20`** strictly exceed `Zenodo #1` (`Visium mean = 0.982610` vs `Zenodo #1 oracle = 0.952533`). |
| **`p2`** | Within `0.02` of `#1` on all `50 / 50` datasets + pure CPU `O(N k G)` (`0` GPU) | **`50 / 50` datasets** within `0.02` of `#1` on **both** `Zenodo 18193366` (`min delta = +0.001524`) and `Seqera v1.0.0` (`min delta = -0.007976`; prior `#1` `SPARK-X` reaches `27 / 50`). Pure CPU runtime across all `50` datasets has `mean = 2.0778s` (`max = 7.9113s`); linear `10,000 / N` rate has `mean = 3.2708s` (`max = 6.3909s` on `1,050`-gene datasets), and `max(10,000, N)`-normalized rate is `<= 6.3909s` (`< 5.0s` on `48 / 50` datasets and `12 / 12` panel datasets, `0` GPU). |
| **`p3`** | Controlled mechanistic diagnosis isolating failure modes + Depth-Paradox & finite-UMI ceiling | Verified in [`how-we-built-it/ablation_p3.py`](./how-we-built-it/ablation_p3.py) $\to$ [`object/ablation_p3.json`](./object/ablation_p3.json), [`how-we-built-it/stress_test_depth_paradox.py`](./how-we-built-it/stress_test_depth_paradox.py) $\to$ [`object/depth_paradox_benchmark.json`](./object/depth_paradox_benchmark.json), and [`object/bayes_ceiling_dev4.json`](./object/bayes_ceiling_dev4.json). |

### 2. Aggregate Comparison Against All `14` Official Benchmark Methods (`Zenodo 18193366`, `50` Datasets)

| Rank | Method | Succeeded | `50`-Dataset Mean $\tau$ | Datasets Within `0.02` of `#1` (`p2`) | Primary Limitation / Failure Mode |
| ---: | :--- | ---: | ---: | ---: | :--- |
| **—** | **`AMS-SVG` (`object/method.py`, frozen default)** | **`50 / 50`** | **`0.945981`** *(Holdout `46`: `0.953362`)* | **`50 / 50`** | `scDesign3` simulator scope; unnormalized under severe spot capture dropout; `-0.007976` vs cross-RNG `Seqera` `nnsvg` on `01_Visium` |
| — | *`AMS-SVG-EB v2` (`object/ams_svg_eb_v2.py`, frozen capture-deconfounded)* | *`50 / 50`* | *`0.945966`* *(Holdout `46`: `0.953130`)* | *`50 / 50`* | *Deconfounds spot capture dropout (`+0.0004..+0.0025` over `v1`), but `-0.0198` on `11_Cerebellum` (`1`-spot anatomical ribbon)* |
| — | *14-Method Per-Dataset Oracle* | *`50 / 50`* | *`0.910614`* | *`50 / 50`* | *Post-hoc maximum across all 14 methods per dataset* |
| 1 | `SPARK-X` | `50 / 50` | `0.884811` | `27 / 50` | Rank-2 axis kernels, raw NB outliers, `-log10(p)` underflow |
| 2 | `SpatialDE2` | `50 / 50` | `0.811916` | `8 / 50` | `1 / L_s` normalization contamination + Bayesian zone step |
| 3 | `nnSVG` | `49 / 50` | `0.800109` | `12 / 50` | `logcounts` (`1 / L_s`) contamination on compartment tissues (`1` failed) |
| 4 | `MoranI` | `50 / 50` | `0.779516` | `10 / 50` | `normalized` (`1 / L_s`) + unpruned Delaunay cavity edges |
| 5 | `Spanve` | `50 / 50` | `0.773444` | `13 / 50` | Degradation on sparse `Stereo-seq` / `slide-tags` |
| 6 | `SpatialDE` | `50 / 50` | `0.710133` | `3 / 50` | `normalized` (`1 / L_s`) + stationary Euclidean GP |
| 7 | `GPcounts` | `46 / 50` | `0.704757` | `5 / 50` | `1 / L_s` offset + stationary kernel + `O(N^3)` runtime (`4` failed) |
| 8 | `SpaGFT` | `50 / 50` | `0.696583` | `1 / 50` | `normalized` (`1 / L_s`) + fixed graph Fourier cutoff |
| 9 | `SOMDE` | `44 / 50` | `0.590445` | `0 / 50` | SOM node aggregation blurs sparse single-cell patterns (`6` failed) |
| 10 | `scGCO` | `50 / 50` | `0.520796` | `0 / 50` | Discrete graph-cut discretization + FDR step-function ties |
| 11 | `SPARK` | `50 / 50` | `0.385448` | `2 / 50` | `L_s` library-size offset endogeneity (`-0.2508` on melanoma) |
| 12 | `SpaGCN` | `43 / 50` | `0.079557` | `0 / 50` | Domain-clustering p-value ties (`7` failed) |
| 13 | `Sepal` | `45 / 50` | `0.055207` | `0 / 50` | Regular grid diffusion assumption fails on irregular coordinates (`5` failed) |
| 14 | `BOOST-GP` | `31 / 50` | `0.008017` | `0 / 50` | MCMC convergence / timeout failures (`19` failed) |

### 3. `12`-Dataset, `9`-Technology Verification Panel (`verify-it-yourself/verify.py`)

| Dataset ID | Technology | Split | Spots $\times$ Genes | `AMS-SVG` $\tau$ | `AMS-EB v2` $\tau$ | `Zenodo #1` (`Method`: $\tau$) | $\Delta_{\text{Zen}}$ | `Seqera v1 #1` (`Method`: $\tau$) | $\Delta_{\text{Seq}}$ | CPU Time |
| :--- | :--- | :--- | ---: | ---: | ---: | :--- | ---: | :--- | ---: | ---: |
| `42_slide_tag_human_skin_melanoma` | `slide-tags` | `dev` | `4,804 x 1,050` | **`0.797905`** | `0.799619` | `SPARK-X`: `0.704236` | `+0.093668` | `spark_x`: `0.698200` | `+0.099705` | `2.47s` |
| `41_slide_tag_human_cortex` | `slide-tags` | `blind_holdout` | `4,065 x 1,050` | **`0.912571`** | `0.909714` | `SPARK-X`: `0.879080` | `+0.033491` | `spark_x`: `0.872700` | `+0.039871` | `1.91s` |
| `44_stereo_seq_Drosophila_embryo_E7` | `Stereo-seq` | `dev` | `1,039 x 1,050` | **`0.807619`** | `0.810476` | `SPARK-X`: `0.770441` | `+0.037179` | `spark_x`: `0.774900` | `+0.032719` | `0.15s` |
| `47_stereo_seq_Drosophila_embryo_E10.5` | `Stereo-seq` | `blind_holdout` | `1,110 x 1,050` | **`0.829333`** | `0.832571` | `SPARK-X`: `0.779218` | `+0.050115` | `spark_x`: `0.769300` | `+0.060033` | `0.13s` |
| `34_MERFISH_Human_cortex` | `MERFISH` | `dev` | `9,259 x 525` | **`0.869333`** | `0.874286` | `SPARK-X`: `0.805983` | `+0.063350` | `spark_x`: `0.800100` | `+0.069233` | `1.79s` |
| `26_DBiT_seq_E10_brain` | `DBiT-seq` | `blind_holdout` | `1,789 x 1,050` | **`0.831619`** | `0.830286` | `GPcounts`: `0.829365` | `+0.002254` | `gpcounts`: `0.810500` | `+0.021119` | `0.32s` |
| `21_slide_seqv2_Mouse_Olfactory_Bulb` | `Slide-seqV2` | `blind_holdout` | `21,624 x 210` | **`0.985714`** | `0.983810` | `SPARK-X`: `0.924164` | `+0.061550` | `nnsvg`: `0.939000` | `+0.046714` | `5.34s` |
| `49_STARmap_Wang2018_2D_zstep10_0` | `STARmap` | `blind_holdout` | `2,764 x 525` | **`0.987810`** | `0.987810` | `SPARK-X`: `0.941338` | `+0.046472` | `spark_x`: `0.929000` | `+0.058810` | `0.46s` |
| `32_10x_Xenium_Human_Colon_Cancer` | `10x Xenium` | `blind_holdout` | `5,561 x 1,050` | **`0.999238`** | `0.999238` | `Spanve`: `0.995238` | `+0.004000` | `spanve`: `0.994100` | `+0.005138` | `2.98s` |
| `39_seqFISH_Mouse_Organogenesis` | `seqFISH` | `blind_holdout` | `19,402 x 525` | **`0.996952`** | `0.997333` | `nnSVG`: `0.992381` | `+0.004571` | `nnsvg`: `0.992000` | `+0.004952` | `4.14s` |
| `04_10x_Visium_Human_Heart` | `10x Visium` | `blind_holdout` | `4,224 x 1,050` | **`0.900762`** | `0.903429` | `SpatialDE2`: `0.849905` | `+0.050857` | `spark_x`: `0.777400` | `+0.123362` | `2.09s` |
| `01_10x_Visium_mouse_brain` | `10x Visium` | `dev` | `2,688 x 1,050` | **`0.969524`** | `0.969905` | `GPcounts`: `0.964670` | `+0.004854` | `nnsvg`: `0.977500` | `-0.007976` | `0.77s` |

### 4. Three-Confounder Single-Factor Ablation (`how-we-built-it/ablation_p3.py` $\to$ `object/ablation_p3.json`)

| Dataset (`Technology`) | `L_s` Moran's $I$ | **Confounder #1:** Delaunay `normalized` $\to$ Unnormalized `log1p(counts)` | **Confounder #2:** Unpruned Delaunay VST $\to$ Multi-Scale Adaptive `AMS-SVG` *(Raw Counts)* | **Confounder #3 (`alpha >= 0.5`):** Float64 `-log10(max(p, 1e-300))` $\to$ Unbounded `Z` *(Genes `Z >= 37.17`)* |
| :--- | ---: | :--- | :--- | :--- |
| `42_slide_tag_human_skin_melanoma` (`slide-tags`) | `0.293064` | `0.196000 -> 0.450857` (`+0.254857`) | `0.467429 -> 0.797905` (`+0.330476`; *raw `0.792000`*) | `0.721455 -> 0.721455` (`+0.000000`; *`0.1%`*) |
| `41_slide_tag_human_cortex` (`slide-tags`) | `0.300338` | `0.585143 -> 0.751048` (`+0.165905`) | `0.759810 -> 0.912571` (`+0.152762`; *raw `0.900000`*) | `0.792418 -> 0.862545` (`+0.070128`; *`18.4%`*) |
| `44_stereo_seq_Drosophila_embryo_E7` (`Stereo-seq`) | `0.374727` | `0.710667 -> 0.737333` (`+0.026667`) | `0.736762 -> 0.807619` (`+0.070857`; *raw `0.811238`*) | `0.735516 -> 0.744727` (`+0.009211`; *`3.7%`*) |
| `47_stereo_seq_Drosophila_embryo_E10.5` (`Stereo-seq`) | `0.436640` | `0.693905 -> 0.732571` (`+0.038667`) | `0.732190 -> 0.829333` (`+0.097143`; *raw `0.828571`*) | `0.727176 -> 0.725818` (`-0.001358`; *`3.3%`*) |
| `34_MERFISH_Human_cortex` (`MERFISH`) | `0.189145` | `0.567238 -> 0.635429` (`+0.068190`) | `0.657143 -> 0.869333` (`+0.212190`; *raw `0.878857`*) | `0.741042 -> 0.838545` (`+0.097503`; *`16.6%`*) |
| `21_slide_seqv2_Mouse_Olfactory_Bulb` (`Slide-seqV2`) | `0.384929` | `0.908571 -> 0.955238` (`+0.046667`) | `0.956190 -> 0.985714` (`+0.029524`; *raw `0.950476`*) | `0.123650 -> 0.970909` (`+0.847259`; *`61.9%`*) |
| `32_10x_Xenium_Human_Colon_Cancer` (`10x Xenium`) | `0.430468` | `0.943810 -> 0.999429` (`+0.055619`) | `0.999048 -> 0.999238` (`+0.000190`; *raw `0.977714`*) | `0.000000 -> 0.997818` (`+0.997818`; *`81.6%`*) |
| `04_10x_Visium_Human_Heart` (`10x Visium`) | `0.414547` | `0.503619 -> 0.827810` (`+0.324190`) | `0.826857 -> 0.900762` (`+0.073905`; *raw `0.880000`*) | `0.602459 -> 0.874909` (`+0.272450`; *`27.6%`*) |
| `01_10x_Visium_mouse_brain` (`10x Visium`) | `0.463640` | `0.946857 -> 0.958095` (`+0.011238`) | `0.956571 -> 0.969524` (`+0.012952`; *raw `0.925333`*) | `0.120594 -> 0.932364` (`+0.811770`; *`62.3%`*) |

- **Confounder #1 (`1 / L_s` Endogeneity):** Total spot counts $L_s = \sum_g Y_{s,g}$ are strongly spatially autocorrelated on compartmented tissues (`MoranI(log1p(L_s)) = 0.293064` on `42_melanoma`, `0.414547` on `04_Visium_Heart`); dividing by $L_s$ injects spurious autocorrelation into `alpha = 0` null genes (`+0.007362` vs `+0.004588` unnormalized on `42_melanoma`; `+0.037722` vs `+0.000392` on `04_Visium_Heart`; `+0.053297` vs `+0.004390` on `32_Xenium`) and cancels compartment-aligned SVGs (`mean drop = -0.154900` when injected into `AMS-SVG`).
- **Confounder #2 (Irregular Point-Cloud Geometry, Cavity Bridging & NB Heavy Tails):** Replacing unpruned Delaunay edges (`p99 / median = 3.9565x` on melanoma) with the 6-scale locally density-adapted biweight kNN + `O(2)`-invariant Mercer bank adds `mean = +0.108889` across the 9-dataset panel (`+0.330476` on `42_melanoma`), while dual VST adds `mean = +0.014201` over raw counts.
- **Confounder #3 (IEEE-754 Binary64 P-Value Underflow):** Mapping spatial statistics through `-log10(max(p, 1e-300))` clips identically at `300.0` for $Z \ge 37.17$, tying up to `81.6%` of genes on `32_Xenium` and reducing high-SNR (`alpha >= 0.5`) Kendall's $\tau$ (`mean recovery = +0.344976` via unbounded analytical permutation $Z$-scores).

### 5. Offline Finite-UMI Template Ceiling & Dual-Regime Depth-Paradox Benchmark

| Dev Dataset | Spots $\times$ Genes | `AMS-SVG v1` $\tau$ | `AMS-SVG-EB v2` $\tau$ | Best Single Scale (`v1`) | Offline 20-Column LOAO Template Ceiling $\tau$ | Scale Dilution (`alpha >= 0.3`) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| `42_slide_tag_human_skin_melanoma` | `4,804 x 1,050` | `0.797905` | `0.799619` (`+0.001714`) | `mercer_0.26`: `0.803048` | `0.835238` | `12.3%` |
| `44_stereo_seq_Drosophila_embryo_E7` | `1,039 x 1,050` | `0.807619` | `0.810476` (`+0.002857`) | `mercer_0.14`: `0.805905` | `0.847238` | `2.3%` |
| `34_MERFISH_Human_cortex` | `9,259 x 525` | `0.869333` | `0.874286` (`+0.004953`) | `mercer_0.14`: `0.868571` | `0.891048` | `7.7%` |
| `01_10x_Visium_mouse_brain` | `2,688 x 1,050` | `0.969524` | `0.969905` (`+0.000381`) | `knn_2`: `0.970476` | `0.972381` | `0.0%` |

- **Kac–Murdock–Szegő Boundary Trap (`No-Go #1`):** Inverting the multi-scale $H_0$ correlation matrix $R$ concentrates `~78%` of weight onto the two extreme boundary scales (`0.797905 -> 0.780190` on `42_melanoma`), whereas Hilbert-sphere geodesic arc-length weights $\Delta\theta_{s,s+1} = \arccos(R_{s,s+1})$ avoid matrix inversion and lift all `4 / 4` Dev datasets (`0.861095 -> 0.863571`).
- **Spatial-Mixture Variance-Dip Shift (`No-Go #2`):** Because `scDesign3`'s spatial mean variance scales as $(1 - 2\alpha(1-\alpha))\operatorname{Var}_s(\mu_g)$, estimating per-column NB dispersion $\hat{\theta}_g$ shifts the Anscombe curve across $\alpha$ (`0.797905 -> 0.776000` on `42_melanoma`), whereas fixed-curve `log1p` + Freeman-Tukey transforms preserve $\alpha$-comparability.

| Stress Regime (`9`-Dataset Multi-Tech Panel) | Mean $\hat{\kappa}_{\text{EB}}$ | `MoranI` (`normalized`) | `AMS + Global 1/L_s` | `Py-SPARK-X` (`counts`) | `AMS-SVG v1` (`counts`) | `AMS-SVG-EB v2` (`counts`) | $\Delta(\text{v2} - \text{v1})$ | $\Delta(\text{v2} - \text{SPARK-X})$ |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Regime I: Intact Compartment (`sigma_tech = 0.00`) | `0.0574` | `0.672868` | `0.741989` | `0.845045` | `0.896889` | **`0.898116`** | `+0.001228` | `+0.053072` |
| Regime II-A: Moderate Bead Capture Dropout (`sigma_tech = 0.35`) | `0.2437` | `0.665566` | `0.740127` | `0.823824` | `0.889587` | **`0.889968`** | `+0.000381` | `+0.066144` |
| Regime II-B: Strong Bead Capture Dropout (`sigma_tech = 0.70`) | `0.5732` | `0.649185` | `0.734963` | `0.765778` | `0.875111` | **`0.875958`** | `+0.000846` | `+0.110180` |
| Regime II-C: Severe Bead Capture Dropout (`sigma_tech = 0.85`) | `0.6509` | `0.644148` | `0.732656` | `0.738349` | `0.864444` | **`0.866942`** | `+0.002497` | `+0.128593` |
| Regime II-D: Microfluidic Channel Striping (`sigma_tech = 0.70`) | `0.4515` | `0.647069` | `0.733841` | `0.670116` | `0.838624` | **`0.840931`** | `+0.002307` | `+0.170815` |

## Not claimed

1. **Simulator Scope Only:** All `50` datasets come from `scDesign3` (`simulate_svg/script.R`, rank-`50` Gaussian-process spatial marginal mixed across `21` levels `alpha in {0.00, ..., 1.00}` under a Negative Binomial copula). High rank correlation on `scDesign3` simulations does **not** establish biological specificity, cell-type deconvolution separation, or wet-lab superiority on primary tissue.
2. **S3 Bucket Outage & Cross-RNG Comparison:** Because `s3://openproblems-data` began returning `403 AllAccessDisabled` globally on `2026-11-05` (`openproblems-bio/task_predict_modality#85`), `.h5ad` verification uses lead author Zhijian Li's official Pinello Lab `Zenodo 18193366` archive alongside published `Seqera Cloud v1.0.0` (`run_2024-09-26_08-24-11`, an independent container RNG realization). On matched `Zenodo 18193366` `.h5ad` files, `object/method.py` exceeds all `14` methods on `50 / 50` datasets; across independent RNG realizations against `Seqera v1.0.0`, `nnsvg` has a higher score on `1 / 50` datasets (`01_10x_Visium_mouse_brain`: `0.969524` vs `0.977500`, `delta = -0.007976`).
3. **Coordinate-Multiplicity & Single-Spot Ribbon Identifiability Scope:** Exact tie-free equivalence of `cKDTree(k=k_eff+1)` biweight kNN holds whenever exact coordinate multiplicity satisfies $m(x) \le k_{\text{eff}} + 1$ (`max = 2` across all `50` datasets). Unnormalized `object/method.py` assumes absence of severe unmodeled spot capture dropout, while capture-deconfounded `object/ams_svg_eb_v2.py` trades `-0.019809` on `11_10x_Visium_Human_Cerebellum` (`49 / 50` strict `Zenodo` wins, `50 / 50` within `0.02`) where `1`-spot-wide anatomical layers are rank-1 collinear with sub-meso capture shifts without negative-control probes.
4. **Peer Review:** Not peer-reviewed; verified mechanically by `verify-it-yourself/verify.py` and audited by our local three-skeptic panel (`panel/`).

## Credits

- **Benchmark & `scDesign3` Simulation Suite:** Zhijian Li, Zain M. Patel, Dongyuan Song, Guanao Yan, Jingyi Jessica Li, and Luca Pinello, *Benchmarking computational methods to identify spatially variable genes and peaks*, `bioRxiv 2023.12.02.569717` (`10.1101/2023.12.02.569717`); OpenProblems `task_spatially_variable_genes` (`https://github.com/openproblems-bio/task_spatially_variable_genes`) and Pinello Lab `Zenodo Record 18193366` (`https://zenodo.org/records/18193366`).
- **Analytical Spatial Autocorrelation & Variance Stabilization:** P. A. P. Moran, *Biometrika* 37:17–23 (`10.1093/biomet/37.1-2.17`, 1950); M. F. Freeman and J. W. Tukey, *Ann. Math. Statist.* 21:607–611 (`10.1214/aoms/1177729756`, 1950); A. D. Cliff and J. K. Ord, *Spatial Processes: Models & Applications* (Pion, 1981); L. Zelnik-Manor and P. Perona, *Self-Tuning Spectral Clustering* (NeurIPS 2004).
- **Method Engineering & Verification:** **we\*** (`PROOFER` powered by Gemini + `@mizopl`).
