# SRBench 2025 Black-Box Symbolic Regression Pareto Dominance (`579_fri_c0_250_5`, `1028_SWD`, `650_fri_c0_500_50`)

## What

Strict 2D Pareto dominance on SRBench 2025 black-box dataset 579_fri_c0_250_5 across all 30 official seeds (median sympy-evaluated test R2 = 0.948589 vs #1 leader GPZGD = 0.947561, and median symbolic_utils.complexity model_size = 38.0 vs GPZGD = 40.5, full win and partial win p1), together with compact model_size <= 20 records (partial win p2) on 579_fri_c0_250_5 (median test R2 = 0.780392 at size 18.0 vs BSR = 0.529910), 1028_SWD (median test R2 = 0.358744 at size 18.0 vs gplearn = 0.243018), and 650_fri_c0_500_50 (median test R2 = 0.826157 at size 18.0 vs PYSR = 0.774987).

## Check It Yourself

Run the standalone verification script from the package root:

```bash
sh verify-it-yourself/run_checks.sh
```

This executes `verify-it-yourself/check_srbench2025.py` (standard library Python 3 only, < 2 seconds runtime), which:
1. Parses all 120 closed-form symbolic expressions in `object/srbench2025_verified_splits.csv` across the 30 official SRBench `random_state` seeds per dataset.
2. Independently recomputes the SymPy-equivalent preorder traversal AST node count (`model_size`) from each symbolic expression and evaluates each expression directly on the held-out 25% test split of the PMLB dataset (`579_fri_c0_250_5.tsv.gz`, `1028_SWD.tsv.gz`, `650_fri_c0_500_50.tsv.gz`), verifying exact agreement with `r2_test_sympy` and `model_size`.
3. Verifies that on `579_fri_c0_250_5` (`win_and_p1`), the 30-split median test $R^2$ is `0.948589` (strictly exceeding the highest median `r2_test` of any algorithm in `results.feather`, `GPZGD = 0.947561`) while the 30-split median `model_size` is `38.0` (strictly smaller than `GPZGD = 40.5`), and verifies the `model_size <= 20` (`p2`) records on `579_fri_c0_250_5`, `1028_SWD`, and `650_fri_c0_500_50`.

## Compared To

- **Published Record (SRBench 2025, `cavalab/srbench` `srbench_2025` branch, `results/black-box-tuning/results.feather`)**:
  - On `579_fri_c0_250_5`: #1 median `r2_test` across all 28 evaluated algorithms is `GPZGD` at `0.947561` with median `model_size = 40.5` (`TIR` is #2 at `0.945587` with median `model_size = 59.5`). Best algorithm with median `model_size <= 20` is `BSR` at `r2_test = 0.529910` (`model_size = 18.0`).
  - On `1028_SWD`: Best algorithm with median `model_size <= 20` is `gplearn` at `r2_test = 0.243018` (`model_size = 13.5`).
  - On `650_fri_c0_500_50`: Best algorithm with median `model_size <= 20` is `PYSR` at `r2_test = 0.774987` (`model_size = 14.0`).
- **This Submission**:
  - `579_fri_c0_250_5` (`win_and_p1`, full `win` + `p1`): median `r2_test = 0.948589` (`+0.001028` over `GPZGD`) at median `model_size = 38.0` (`-2.5` nodes smaller than `GPZGD`).
  - `579_fri_c0_250_5` (`p2_size20`, partial win `p2`): median `r2_test = 0.780392` (`+0.250482` over `BSR`) at median `model_size = 18.0 <= 20`.
  - `1028_SWD` (`p2_size20`, partial win `p2`): median `r2_test = 0.358744` (`+0.115726` over `gplearn`) at median `model_size = 18.0 <= 20`.
  - `650_fri_c0_500_50` (`p2_size20`, partial win `p2`): median `r2_test = 0.826157` (`+0.051170` over `PYSR`) at median `model_size = 18.0 <= 20`.

## Not Claimed

- No claim is made on synthetic track datasets (`feynman_*` or `strogatz_*`) or on the other 9 black-box datasets in the 12-dataset SRBench 2025 subset.

## Credits

- Contributor: `@HindsightWise`
- Prior work:
  - Fabricio Olivetti de Franca, Bogdan Burlacu, Marco Virgolin, Michael Kommenda, Conrado S. Miranda, William G. La Cava et al., "SRBench 2.0: A Living Benchmark for Symbolic Regression," `arXiv:2505.03977` (2025) (`https://github.com/cavalab/srbench/tree/srbench_2025/results/black-box-tuning`).
