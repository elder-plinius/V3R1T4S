# Skeptic 2: Prior Art & Benchmark Novelty Audit

context: independent literature and benchmark audit started from target specification and package files only

## Audit Summary

1. Audited `results/black-box-tuning/results.feather` (`sha256: 5b428264a346f6bbbeabded219f87454b9206afa70c19c012075c672533f342e`) from `cavalab/srbench` (`srbench_2025` branch, `arXiv:2505.03977`) across all 28 evaluated symbolic regression algorithms.
2. Verified that on `579_fri_c0_250_5`, the #1 algorithm by median `r2_test` is `GPZGD` (`0.947561`, median `model_size = 40.5`, followed by #2 `TIR` at `0.945587`, median `model_size = 59.5`), and that this submission's median `r2_test = 0.948589` at median `model_size = 38.0` strictly dominates `GPZGD` and every other algorithm in `results.feather`.
3. Verified that on `579_fri_c0_250_5` (`0.780392 > 0.529910` vs `BSR` at size `18.0`), `1028_SWD` (`0.358744 > 0.243018` vs `gplearn` at size `13.5`), and `650_fri_c0_500_50` (`0.826157 > 0.774987` vs `PYSR` at size `14.0`), the `p2_size20` models strictly beat the best `model_size <= 20` algorithms in `results.feather`.

pass: true
