# How We Found It

_Note: contributor text, unverified._

## Brief

We sought a principled self-improvement on `darkmachines-unsupervised-median-total-improvement` (`p1`) over our initial global 27-invariant Peaks-Over-Threshold (POT) submission (`chaneut_cha300_neut100 TI = 1.60`, `chaneut_cha400_neut200 TI = 1.70`, `Median_TI = 2.80`). In Channel `2a` (`>= 3` leptons), Standard Model background is a mixture of `0`-jet $WZ \to 3\ell\nu$ events (`~75%`) and multi-jet $t\bar{t}Z$ / $t\bar{t}W$ events (`~25%`). Pooling hadronic scalar sums ($H_T$, $N_{\text{jet}}$, $N_b$) globally across all multiplicities allows `6`-jet $t\bar{t}Z$ background events to dominate the $\epsilon_B = 10^{-4}$ global threshold, masking `0`-jet electroweakino production ($\tilde{\chi}_1^\pm \tilde{\chi}_2^0 \to WZ \tilde{\chi}_1^0 \tilde{\chi}_1^0$).

## What Failed First

1. Adding conditional Gaussian copula log-det covariance terms inside each stratum (`dm_bsp_v2`) inflated heavy-tailed non-Gaussian SM fluctuations at $\epsilon_B = 10^{-4}$ and degraded `cha300` to `0.30`.
2. Adding jet/b-jet multiplicity directly as a 5th kinematic sector inside `max_sec_glob` (`dm_bsp_eval_v4`) re-introduced `6`-jet $t\bar{t}Z$ background inflation in Channel `2a`, pulling `cha300` back down to `1.10 - 1.89`.
3. Unclipping the discrete multiplicity grid from `60` to `192` strata (`n_b <= 5, n_jet <= 7`) fragmented rare multi-b SM tails below `MIN_STRATUM_N = 250`, lowering `cha300` from `6.00` to `4.00` without raising `Min_TI`.

## What Worked

1. Factoring the SM background model by exact Bayes' rule over discrete multiplicity topology $S = (\min(N_\ell, 3), \min(N_b, 2), \min(N_{\text{jet}}, 4))$ (`60` strata with `12`-stratum coarse fallback) and `4` physical LHC kinematic sectors (MET/recoil, hadronic transverse $M_T/M_{T2}/M_{CT}$, calorimetric jet mass, and electroweak leptonic $M_T/M_{T2}(Z, \ell_W)$) kept `6`-jet $t\bar{t}Z$ jet sums out of `0`-jet `chaneut` strata, raising `chaneut_cha300_neut100` to **`TI = 6.0000`** (`0.06 / sqrt(1e-4)`) and `chaneut_cha400_neut200` to **`TI = 7.0000`** (`0.07 / sqrt(1e-4)`), with **`Median_TI = 5.3759`** (`BSPOT_MaxSec`).
2. Calibrating both `BSPOT_MaxSec` and the multiplicity-inclusive 27-invariant POT statistic onto a common odd-SM $\text{Exp}(1)$ upper-tail survival scale (`BSPOT_Union_OR` and `BSPOT_FloorGuard`) restored sensitivity to soft high-multiplicity signals (`pp23mt_50`), achieving `cha300 = 3.0000, cha400 = 5.0000, Median_TI = 5.0000, Min_TI = 0.8000` (`BSPOT_Union_OR`) and `cha300 = 1.8000, cha400 = 2.2136, Median_TI = 3.1000, Min_TI = 0.9000` (`BSPOT_FloorGuard`).
