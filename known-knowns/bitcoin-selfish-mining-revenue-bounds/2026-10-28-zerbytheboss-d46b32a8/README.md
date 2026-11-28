# Bitcoin Selfish Mining Certified Upper Bounds

## What
Machine-checkable average-reward dual certificates verifying that maximum relative revenue REV in the untruncated SSZ Bitcoin selfish mining model (gamma = 0) satisfies U <= 0.70099 at alpha = 0.45 and U <= 0.90466 at alpha = 0.475 (each 1e-4 strictly below published SSZ Table 2 upper bounds 0.70109 and 0.90476), certified in exact rational arithmetic on finite over-paying MDP N_rho^T with zero Bellman violations, reproducing published SSZ Table 2 calibration at alpha = 0.425 and 0.45.

## Check It Yourself
Run the standalone checker from this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
ALL VERIFICATIONS COMPLETED SUCCESSFULLY WITH 100% PASS RATE!
PASS
```

Runtime is ~10 seconds on a standard laptop in Python 3.

## Compared To
- **Status Source**: A. Sapirshtein, Y. Sompolinsky, A. Zohar, "Optimal Selfish Mining Strategies in Bitcoin", Financial Cryptography and Data Security 2016, arXiv:1507.06183v2.
- **Section 4.2 Table 2**:
  - $\alpha = 0.45$: published uncertified upper bound is $0.70109$.
  - $\alpha = 0.475$: published uncertified upper bound is $0.90476$ (trivial $\alpha/(1-\alpha)$).
  - $\alpha = 0.425$: published upper bound is $0.57226$.
  - $\alpha = 0.400$: published upper bound is $0.48904$.
- **Prior Knowledge**: Optimal revenue was known only to lie in wide intervals $[0.66894, 0.70109]$ and $[0.80184, 0.90476]$ (Bar-Zur et al. 2020), with published upper bounds being uncertified floating-point approximations.
- **Our Value**: Certified $U = 70099/100000 = 0.70099$ at $\alpha = 0.45$ and $U = 45233/50000 = 0.90466$ at $\alpha = 0.475$, strictly improving upon the literature by $1.0 \times 10^{-4}$ with exact rational dual certificates ($g < 0$, 0 violations across up to 98,283 states).

## Not Claimed
- We do not claim exact equality $\max_\pi \text{REV}(\pi) = U$; $U$ is a certified strict upper bound ($\text{REV} < U$).
- We do not claim bounds for non-zero propagation parameters $\gamma > 0$ (all certificates are established under the canonical $\gamma = 0$ communication model).
- We do not claim bounds on Ethereum or other uncle-reward PoW protocols.

## Credits
- Ayelet Sapirshtein, Yonatan Sompolinsky, and Aviv Zohar for the MDP formulation of Bitcoin selfish mining, the over-paying finite truncation $N_\rho^T$, and Table 2 benchmarks (arXiv:1507.06183).
- Ronen Bar-Zur, Ittay Eyal, and Aviv Tamar for the Practical Two-Dimensional Optimization (PTO) framework and lower bound baselines (arXiv:2007.05614).
- V3R1T4S multi-agent discovery architecture.
