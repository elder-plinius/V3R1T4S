# How We Found It (`immrep22-tcr-epitope-microauc`)

*Note: contributor text, unverified.*

## 1. Reproducing the Published `tcrex` Family & Auditing Negative Provenance (Lens 1)

We began by cloning `MortimerLab/immrep22` (`commit 8942484a902a4694628f0e4f828012884f76382e`) and reproducing the top published baseline family (`tcrexab = 0.847347`, `tcrexb = 0.833841`, `tcrexa = 0.784839`) from its published physicochemical CDR3 descriptors + one-hot V/J gene random forest architecture (`how-we-built-it/reproduce_tcrex_and_audit.py`), obtaining `0.846619`, `0.831443`, and `0.785032` (`|diff| <= 0.0024`).

Next, we audited the provenance of the negative TCRs in `training_data/` and `true_set/` (`how-we-built-it/audit_immrep22_p3_and_leakage.py`):
- Each epitope's 5:1 negative pool consists of ~60% **swapped positives** (TCRs binding one of the other 16 epitopes) and ~40% **control-repertoire negatives** (healthy donor background TCRs).
- Zero (`0 / 17`) control-repertoire negatives overlap between `training_data/{ep}.txt` and `true_set/{ep}.txt`.
- Evaluating all baselines separately on swapped-only negatives (`51.9%` of test negatives) vs control-only negatives (`35.2%` of test negatives) revealed a universal `-0.05` to `-0.06` MicroAUC drop on control-repertoire negatives (`tcrexab`: `0.8707` on swapped vs `0.8130` on control), caused by two distinct failure modes:
  1. **Single-view fragility**: sequence alignment methods (`tcrmatch`, `TCRbase`, `tcrdist3`) miss global physicochemical and V/J gene context, whereas random forests on global physicochemical averages (`tcrex`) miss localized gapped $k$-mer binding motifs in the central contact loop (`CDR3[3:-3]`).
  2. **Metric hubness in sequence space**: canonical germline stems (`CASS...` / `...QYF`) turn generic TCRs into nearest-neighbor hubs under standard cosine/RBF kernels.

## 2. Multi-Chain ($\alpha/\beta/\alpha\beta$) OOB + Analytical LOO + CSLS Hubness-Corrected CLSS Ensemble (Lens 2)

To overcome both failure modes strictly from `training_data/{epitope}.txt` (`how-we-built-it/run_clss_immrep22.py`), we constructed a 3-view ($\alpha$-chain, $\beta$-chain, and synergistic $\alpha\beta$ product) composite representation combining:
- Exact + gapped (`d=1,2`) + central-loop (`CDR3[3:-3]`) + reduced-alphabet (`8`-group physicochemical) TF-IDF $L_2$-normalized string kernels,
- Exact + family-level V/J gene similarity kernels, and
- Standardized physicochemical + position-binned Atchley/Kidera + dipeptide descriptors.

Across the three chain views ($\alpha, \beta, \alpha\beta$), we trained 9 strictly out-of-fold / leave-one-out experts per epitope:
1. **Analytical Leave-One-Out (LOO) Dual Kernel Ridge Regression (3 experts)**: closed-form LOO hat-matrix diagonal $r_i = (y_i - \hat{y}_i)/(1 - H_{ii}) = \alpha_i / (K + \lambda I)^{-1}_{ii}$ over $\lambda \in \{0.05, 0.15, 0.4, 1.0, 2.5, 6.0\}$.
2. **Cross-Domain Similarity Local Scaling (CSLS) Hubness-Corrected $k$-NN (3 experts)**: cubic kernel sharpening $K_{ij}^3$ minus half the background $k$-nearest-neighbor mean similarity $\frac{1}{2}(\mu_k(x_i) + \mu_k(x_j))$, suppressing germline hub TCRs.
3. **Out-of-Bag (`oob_decision_function_`) Balanced Random Forest + ExtraTrees (3 experts)** on the `tcrex` + dipeptide + Atchley/Kidera + V/J dictionary view.

Finally, each expert's predictions are calibrated using the training-only OOF mean and standard deviation via the smooth, strictly monotone pointwise map $g(z_j) = 0.5\,z_j + 0.5\,\tanh(0.6\,z_j)\sqrt{3}$ and weighted by $\max(0, \text{AUC}_{\text{OOF}, j} - 0.52)^4$, then centered by the training OOF negative mean and scaled by the training OOF standard deviation for cross-epitope comparability in Task 2 (`testSet_Global.txt`). Every test TCR prediction is 100% pointwise inductive (`|diff| <= 4.66e-15` between single-row and batch evaluation) and lifts `_Average` MicroAUC to `0.882173` (`+0.034826` over `tcrexab`), `SPRWYFYYL` MicroAUC to `0.877874` (`+0.040050` over all 22 methods, `p1`), and Task 2 `_Average` Rank to `2.859120` (`-0.425169`, `p2`).
