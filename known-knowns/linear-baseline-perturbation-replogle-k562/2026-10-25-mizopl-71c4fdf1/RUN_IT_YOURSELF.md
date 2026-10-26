# Run It Yourself (`2026-10-25-mizopl-71c4fdf1`)

1. Ensure `python3` (`>= 3.9`) is installed.
2. From the root of this package directory, execute:
   ```sh
   sh verify-it-yourself/run_checks.sh
   ```
3. The script runs `verify-it-yourself/verify.py`, performing in **`~0.01` seconds** (or **`14.37` seconds** with `--recompute` on the local pseudobulk cache):
   - **SHA-256 & Provenance Check:** verifies the SHA-256 digest of `object/certificate_replogle_k562.json` (`71c4fdf154e6f8cccfe44f18817dfa78f0863a5cadd8f964026e2a4670bf6c7e`) and all 8 benchmark dataset and Source Data SHA-256 hashes (`single_perturbation_prediction.xlsx`, `suppl-pearson_delta_performance_single_pert.xlsx`, `suppl-k562_rpe1_transfer.xlsx`, `perturbation_prediction.xlsx`, `go_essential_all.csv`, and the three GEARS `perturb_processed.h5ad` files).
   - **Partial Win `p3` Reproduction of Record (`seeds = 1:2` and `seeds = 1:5`):** verifies agreement (`abs_diff <= 7e-6` for all deterministic baselines) of `mean`, `lpm_selftrained`, `lpm_k562PertEmb`, `lpm_rpe1PertEmb`, and `lpm_gearsPertEmb` across `replogle_k562_essential`, `replogle_rpe1_essential`, and `adamson`.
   - **Full Win on `replogle_k562_essential` (`Panel A`, `n = 262`):** verifies that `hollow_loo_dual_lens` achieves **Mean $L_2 = 3.320307$** (`-18.96%` vs `lpm_selftrained = 4.097028`, `-18.59%` vs `gears = 4.078658`, `57.47x` `lpm_selftrained` SD / `31.25x` own SD), **Median $L_2 = 3.044310$** (`-20.00%` vs `lpm_selftrained = 3.805564`, `63.87x` SD), **Mean Pearson $\Delta = 0.620623$** (`+42.49%` vs `lpm_selftrained = 0.435544`, `7.70x` SD), and **Median Pearson $\Delta = 0.644965$** (`+51.23%` vs `0.426484`).
   - **Partial Win `p1` (`replogle_rpe1_essential`, `Panel A`, `n = 413`):** verifies **Mean $L_2 = 4.777953$** (`-11.36%` vs `lpm_selftrained = 5.390179`, `2.65x` SD), **Median $L_2 = 4.514809$** (`-12.38%`, `2.48x` SD), and **Mean Pearson $\Delta = 0.719286$** (`+5.72%` vs `0.680388`).
   - **Partial Win `p2` (Functional Distance Stratification):** verifies monotonic concentration of gain in `Q1_closest` (`-32.33%` $L_2$ reduction on K562, Spearman $r_s = +0.345058$, $p = 9.7126 \times 10^{-9}$; `-17.39%` on RPE1, $p = 0.027768$).
   - **Null / Permutation Control Battery (`300` split-level evaluations):** verifies $Z = 24.55\sigma$ separation on K562 (`200` split runs) and $Z = 22.44\sigma$ separation on RPE1 (`100` split runs), printing `PASS` as its final line.
