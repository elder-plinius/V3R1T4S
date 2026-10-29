# Pre-Registered Null Test — `tdc-dti-dg-bindingdb-patent-pcc`

- **Target ID:** `tdc-dti-dg-bindingdb-patent-pcc`
- `controls`: 1000
- `best_control`: 0.014612 (`TrackF1_5seed_ens` max null PCC across $B=1,000$ within-year test label permutations; `0.014585` for `TrackF2_5seed_ens`, `0.014252` for `TrackF2_seed1`, `0.014352` for `TrackA_5seed_ens`, `0.013647` for `TrackA_seed1`, `0.013774` for `ERM_5seed_ens`)
- `real`: 0.600184 (`Track F2` 5-seed mean PCC; `0.603907` for `Track F2` 5-seed ensemble; `0.599960` for `Track F1` 5-seed mean; `0.579422` for CPU-only `Track A` 5-seed mean)
- `command`: `sh verify-it-yourself/run_checks.sh`
- `real_beats_all_controls`: yes

## 1. Within-Year Permutation Null Protocol

We executed $B = 1,000$ independent **within-patent-year label permutations** (`seed = 20261029`) across all $N = 49,028$ official `BindingDB_Patent` test pairs (`2019`: $N = 42,009$; `2020`: $N = 6,947$; `2021`: $N = 72$). Permuting $Y$ strictly within each patent year preserves the exact marginal affinity distribution and year-specific mean/variance shifts across `2019`, `2020`, and `2021` while breaking the pairing between `(Drug, Target)` and `Y`.

## 2. Empirical Null Distribution ($B = 1,000$ Permutations, $N = 49,028$)

| Model / Track | Observed `PCC` | Null Mean | Null SD | Null 95th %ile | Null 99th %ile | Null Max | $Z$-Score | Empirical $p$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`Track F2` (`trackC_fullwin`, Seed 1)** | **`0.599820`** | `0.000092` | `0.004560` | `0.007871` | `0.011317` | `0.014252` | **`+131.51`** | **`0.000999`** |
| **`Track F2` (`trackC_fullwin`, 5-Seed Ensemble)** | **`0.603907`** | `0.000089` | `0.004588` | `0.008072` | `0.011699` | `0.014585` | **`+131.62`** | **`0.000999`** |
| **`Track F1` ($\beta_{\text{Ex}}=0.72$, 5-Seed Ensemble)** | **`0.603944`** | `0.000089` | `0.004588` | `0.008058` | `0.011596` | `0.014612` | **`+131.62`** | **`0.000999`** |
| **`Track A` (CPU-Only `p1`, Seed 1)** | **`0.578556`** | `0.000097` | `0.004559` | `0.007762` | `0.011180` | `0.013647` | **`+126.88`** | **`0.000999`** |
| **`Track A` (CPU-Only `p1`, 5-Seed Ensemble)** | **`0.582504`** | `0.000083` | `0.004558` | `0.007623` | `0.011295` | `0.014352` | **`+127.77`** | **`0.000999`** |
| **Reproduced `ERM` Baseline (5-Seed Ensemble)** | **`0.516357`** | `0.000109` | `0.004634` | `0.007924` | `0.011769` | `0.013774` | **`+111.41`** | **`0.000999`** |

## 3. Conclusion

Under within-year label permutation, all models collapse to theoretical finite-sample noise ($\text{SD} \approx 1/\sqrt{49028} = 0.004516$, max null $< 0.0147$), with observed correlations exceeding the null by $+126.88\sigma$ to $+131.62\sigma$ ($p = 0.000999$ across all $1,000$ permutations).
