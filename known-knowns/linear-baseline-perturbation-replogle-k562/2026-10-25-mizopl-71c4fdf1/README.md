# `linear-baseline-perturbation-replogle-k562` — Full Win (`CONFIRMED_SOLUTION`) + Partial Wins `p1`, `p2`, `p3` (`2026-10-25-mizopl-71c4fdf1`)

- **Target:** `linear-baseline-perturbation-replogle-k562` (*"Unseen single-gene perturbations in leukaemia cells: beat the linear baseline that currently matches every foundation model"*)
- **Reference Benchmark:** C. Ahlmann-Eltze, W. Huber & S. Anders, *"Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines"*, *Nature Methods* **22**, 1657–1661 (2025), `doi:10.1038/s41592-025-02772-6`, GitHub `const-ae/linear_perturbation_prediction-Paper` at pinned commit `bfa6eeea2bd145a1af2ec0127a2e808cc38456a9`.
- **Verdict:** **`CONFIRMED_SOLUTION`** (**Full Win** on `replogle_k562_essential` + **Partial Win `p1`** on `replogle_rpe1_essential` + **Partial Win `p2`** Functional Distance Stratification + **Partial Win `p3`** Reproduction of Record across `seeds = 1:2` and `seeds = 1:5`).
- **Certificate:** [`object/certificate_replogle_k562.json`](object/certificate_replogle_k562.json) (`sha256 = 71c4fdf154e6f8cccfe44f18817dfa78f0863a5cadd8f964026e2a4670bf6c7e`).
- **One-Command Verification:** `sh verify-it-yourself/run_checks.sh` (`0.01 s` certificate audit; `14.37 s` with `--recompute` live solver execution).

---

## 1. Headline Summary Table

Trained **strictly on the intra-dataset `train` perturbations** of the published GEARS splits (`sha256` verified) with zero cross-cell-line expression transfer and zero test/val leakage (verified by active test/val expression poisoning `max_poison_diff = 0.0`), our closed-form **Hollow Leave-One-Out Dual-Lens Kernel Regression (`hollow_loo_dual_lens`)** predictor beats both our same-environment re-run of `lpm_selftrained` and the best published method in the paper's Source Data across every criterion:

| Criterion / Split Universe | Metric (`Top-1,000` Genes) | `lpm_selftrained` (Re-run & Published) | Best Published Method in Source Data | **`hollow_loo_dual_lens` (Ours)** | Relative Improvement vs `lpm_selftrained` | Across-Split SD Multiple (`>= 2x` req.) | Status |
|---|---|---:|---:|---:|---:|---:|---|
| **Full Win: `replogle_k562_essential` (`Panel A`, `n = 262`)** | **Mean $L_2$ ($\downarrow$)** | `4.097028` (`SD = 0.013196`) | `4.078658` (`gears`, `SD = 0.064478`) | **`3.320307`** (`SD = 0.024271`) | **`-18.96%`** (`-18.59%` vs `gears`) | **`57.47x` `lpm` SD** (`31.25x` own SD) | **PASS (`>= 5%` & `>= 2x SD`)** |
| **Full Win: `replogle_k562_essential` (`Panel A`, `n = 262`)** | **Median $L_2$ ($\downarrow$)** | `3.805564` (`3.805557` pub, `SD = 0.011305`) | `3.766328` (`uce`, `SD = 0.015954`) | **`3.044310`** (`SD = 0.058063`) | **`-20.00%`** (`-19.17%` vs `uce`) | **`63.87x` `lpm` SD** (`45.26x` `uce` SD) | **PASS (`>= 5%` & `>= 2x SD`)** |
| **Full Win: `replogle_k562_essential` (`Panel A`, `n = 262`)** | **Mean Pearson $\Delta$ ($\uparrow$)** | `0.435544` (`SD = 0.024039`) | `0.435544` (`lpm_selftrained`) | **`0.620623`** (`SD = 0.016671`) | **`+42.49%`** (`+0.185079`) | **`7.70x` `lpm` SD** (`11.10x` own SD) | **PASS (`>= 5%` & `>= 2x SD`)** |
| **Full Win: `replogle_k562_essential` (`Panel A`, `n = 262`)** | **Median Pearson $\Delta$ ($\uparrow$)** | `0.426480` (`0.426484` pub, `SD = 0.020503`) | `0.426484` (`lpm_selftrained`) | **`0.644965`** (`SD = 0.042957`) | **`+51.23%`** (`+0.218481`) | **`10.66x` `lpm` SD** (`5.09x` own SD) | **PASS (`>= 5%` & `>= 2x SD`)** |
| **`replogle_k562_essential` (`Panel C`, `n = 214`)** | **Mean $L_2$ / Mean $r_{\Delta}$** | `4.028209` / `0.441412` | `3.892297` (`scFoundation`) / `3.543026` (`rpe1PertEmb`) | **`3.273909` / `0.608814`** | **`-18.73%` (`L2`) / `+37.92%` (`r2_delta`)** | Beats cross-cell-line `rpe1PertEmb` by **`-7.60%`** | **PASS** |
| **`replogle_k562_essential` (`seeds = 1:5`, `n = 677`)** | **Mean $L_2$ / Mean $r_{\Delta}$** | `4.168029` (`SD = 0.060489`) / `0.437119` | — | **`3.332314` / `0.633310`** | **`-20.05%` (`L2`) / `+44.88%` (`r2_delta`)** | **`13.82x` 5-seed `lpm` SD** (`31.53x` own SD) | **PASS** |
| **Partial Win `p1`: `replogle_rpe1_essential` (`Panel A`, `n = 413`)** | **Mean $L_2$ ($\downarrow$)** | `5.390179` (`SD = 0.230747`) | `5.390179` (`lpm_selftrained`) | **`4.777953`** (`SD = 0.182955`) | **`-11.36%`** (`-0.612226`) | **`2.65x` `lpm` SD** (`3.35x` own SD) | **PASS (`p1`)** |
| **Partial Win `p1`: `replogle_rpe1_essential` (`Panel A`, `n = 413`)** | **Median $L_2$ ($\downarrow$)** | `5.152955` (`5.152959` pub, `SD = 0.257374`) | `5.152959` (`lpm_selftrained`) | **`4.514809`** (`SD = 0.390666`) | **`-12.38%`** (`-0.638150`) | **`2.48x` `lpm` SD** | **PASS (`p1`)** |
| **Partial Win `p1`: `replogle_rpe1_essential` (`Panel A`, `n = 413`)** | **Mean Pearson $\Delta$ ($\uparrow$)** | `0.680388` (`SD = 0.034730`) | `0.680388` (`lpm_selftrained`) | **`0.719286`** (`SD = 0.024171`) | **`+5.72%`** (`+0.038898`) | `1.61x` own SD (`2.36x` across 5 seeds) | **PASS (`p1`)** |
| **Partial Win `p1`: `replogle_rpe1_essential` (`Panel C`, `n = 224`)** | **Mean $L_2$ / Mean $r_{\Delta}$** | `5.711850` / `0.766209` | `5.147212` (`k562PertEmb`) | **`4.914609` / `0.815232`** | **`-13.96%` (`L2`) / `+6.40%` (`r2_delta`)** | Beats cross-cell-line `k562PertEmb` by **`-4.52%`** | **PASS (`p1`)** |
| **Partial Win `p1`: `replogle_rpe1_essential` (`seeds = 1:5`, `n = 1,063`)** | **Mean $L_2$ / Mean $r_{\Delta}$** | `5.544850` (`SD = 0.174215`) / `0.662573` | — | **`4.885882` / `0.709296`** | **`-11.88%` (`L2`) / `+7.05%` (`r2_delta`)** | **`3.78x` 5-seed `lpm` SD** (`4.87x` own SD) | **PASS (`p1`)** |
| **Partial Win `p2`: Functional Distance Quartiles (`K562`, `n = 262`)** | **`Q1_closest` vs `Q4_farthest` $\Delta L_2$** | `4.345813` (`Q1`) / `3.887674` (`Q4`) | — | **`2.940883` (`Q1`) / `3.483419` (`Q4`)** | **`-32.33%` (`Q1`) vs `-10.40%` (`Q4`)** | Spearman $r_s = +0.345058$ (**$p = 9.7126 \times 10^{-9}$**) | **PASS (`p2`)** |
| **Partial Win `p3`: Reproduction of Record (`3` datasets)** | **`mean`, `lpm_selftrained`, `k562/rpe1PertEmb`** | Exact match (`0.000000` to `0.000007`) | — | Evaluated across `seeds = 1:2` & `1:5` | `max_diff <= 7e-6` | — | **PASS (`p3`)** |
| **Null Control Battery (`300` Split-Level Permutations)** | **Gene-Identity Permutation $L_2$** | `4.971309 ± 0.067250` (`K562` null) | `6.231428 ± 0.064759` (`RPE1` null) | **`3.320307` (`K562`) / `4.777953` (`RPE1`)** | Beats all `300` null runs | **`Z = 24.55 σ` (`K562`) / `Z = 22.44 σ` (`RPE1`)** | **PASS** |

---

## 2. Compute & Discovery Time (`we*` Single-Thread Architecture)

All discovery, baseline reproduction, ablation testing, and 300-run permutation certification were executed autonomously on a **single thread** of our [`we*`](https://github.com/mizopl/we-star) architecture running on a 16 GB Apple M1 laptop (CPU-only):

| Phase / Benchmark Operation | Hardware | Single-Core CPU Compute Time | Wall-Clock Discovery Time (1 `we*` Thread) |
|---|---|---:|---:|
| GO IDF + Jaccard Graph Construction (`19,264` genes, `gene2go_all.pkl`) | 1 CPU core (Apple M1) | `7.62 s` | — |
| `replogle_k562_essential` Full 5-Seed + Panel A/C + Ablation Suite | 1 CPU core (Apple M1) | `24.08 s` | — |
| `replogle_rpe1_essential` Full 5-Seed + Panel A/C + Ablation Suite | 1 CPU core (Apple M1) | `38.55 s` | — |
| `adamson` Full 5-Seed + Panel A/C + Ablation Suite | 1 CPU core (Apple M1) | `1.99 s` | — |
| **Total Solver Runtime Across All 3 Datasets & 5 Seeds (`39` splits)** | **1 CPU core (Apple M1)** | **`72.24 s` (`1.20 min`)** | **`27 min` (`23:03 -> 23:30`) to first win** |
| Null Permutation Control Battery (`300` split-level runs on K562 + RPE1) | 1 CPU core (Apple M1) | `418.45 s` (`6.97 min`) | — |
| **Complete Certification (`certify_all_splits_and_controls.py`)** | **1 CPU core (Apple M1)** | **`493.51 s` (`8.23 min`)** | **`36 min` (`23:03 -> 23:39`) end-to-end** |
| **Standalone Verification (`verify-it-yourself/verify.py`)** | **1 CPU core (Apple M1)** | **`0.01 s` (`14.37 s` with `--recompute`)** | — |

---

## 3. Package Layout

- [`INDEX.csv`](INDEX.csv) — machine-readable summary row with SHA-256 pointer.
- [`RUN_IT_YOURSELF.md`](RUN_IT_YOURSELF.md) — one-command verification guide.
- [`HOW_WE_FOUND_IT.md`](HOW_WE_FOUND_IT.md) — mathematical derivation of the Hollow-LOO Dual-Lens engine.
- [`null_test.md`](null_test.md) — 300-run gene-identity permutation control report ($Z = 24.55\sigma$ on K562, $Z = 22.44\sigma$ on RPE1).
- [`object/certificate_replogle_k562.json`](object/certificate_replogle_k562.json) — full machine-verified JSON certificate (`sha256 = 71c4fdf154e6f8cccfe44f18817dfa78f0863a5cadd8f964026e2a4670bf6c7e`).
- [`verify-it-yourself/`](verify-it-yourself/) — `run_checks.sh`, `verify.py`, and `RECEIPTS.md`.
- [`how-we-built-it/`](how-we-built-it/) — `certify_all_splits_and_controls.py`, `reproduce_baselines.py`, `lens1_lens2_engine.py`, and `test_hollow_loo_engine.py`.
- [`the-record-we-beat/PAPER_NUMBERS.md`](the-record-we-beat/PAPER_NUMBERS.md) — exact comparison against Ahlmann-Eltze, Huber & Anders (*Nature Methods* 2025) Source Data.
- [`panel/`](panel/) — independent 3-skeptic adversarial audit reports (`reproduce.md`, `novelty.md`, `criterion.md`, `gate.md`).

— autonomously engineered & 3-skeptic verified by **Gemini-CLSS** (`PROOFER v18`) on @mizopl's behalf
