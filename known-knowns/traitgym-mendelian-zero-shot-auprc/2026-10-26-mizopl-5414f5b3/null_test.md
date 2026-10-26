# Pre-Registered Null Test — `traitgym-mendelian-zero-shot-auprc`

- **Target ID:** `traitgym-mendelian-zero-shot-auprc`
- `controls`: 1000
- `best_control`: 0.154438 (`AF_Closed_4` max null across $B=1,000$ within-chromosome label permutations; `0.147438` for `ZS_7_cadd_free`, `0.151593` for `CI_6_multimodal`, `0.149629` for `M2_supervised_chrom`, `0.123316` for `ZS_7_cadd_free` on Complex traits)
- `real`: 0.789624 (`ZS_7_cadd_free` on Mendelian; `0.807396` for `CI_6_multimodal`; `0.754022` for `AF_Closed_4`; `0.793262` for `AF_4P`; `0.904124` for `M2_supervised_chrom`; `0.281541` for `ZS_7_cadd_free` on Complex traits)
- `command`: `python3 claim/verify.py`
- `real_beats_all_controls`: yes

## 1. Null-Test Protocol (`PREREG.md`)
As frozen in `PREREG.md` (`null_test: required`), we executed $B = 1,000$ independent **within-chromosome label permutations** (`seed = 20261026` in `claim/verify.py`) on both `mendelian_traits_matched_9` ($N = 3,380$, $338$ positives across $19$ chromosomes, $10.0\%$ positive prevalence per chromosome) and `complex_traits_matched_9` ($N = 11,400$, $1,140$ positives across $22$ chromosomes, $10.0\%$ positive prevalence per chromosome).

In each permutation $b \in \{1, \dots, 1000\}$:
1. For every chromosome $c$, the binary causal label vector $y_c$ is randomly permuted without replacement (`rng.permutation(y_c)`), preserving the exact sample size $n_c$ and exact positive count $n_{c,+}$ on every chromosome.
2. The official TraitGym evaluation metric (`AUPRC_by_chrom_weighted_average`) is computed against the fixed variant scores.
3. The empirical one-sided $p$-value is $p_{\text{emp}} = \frac{1 + \#\{b : \text{AUPRC}_{\text{null}}^{(b)} \ge \text{AUPRC}_{\text{obs}}\}}{B + 1}$.

## 2. Results (`claim/certificate.json`)

### A. `mendelian_traits_matched_9` ($N = 3,380$, $19$ Chromosomes, $B = 1,000$)

| Model / Track | Observed `AUPRC` | Null Mean | Null SD | Null 95th %ile | Null 99th %ile | Null Max | $Z$-Score | Empirical $p$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`ZS_7_cadd_free`** (Track A Full Win, 100% CADD-free) | **`0.789624`** | `0.122174` | `0.007793` | `0.135616` | `0.141809` | `0.147438` | **`+85.65`** | **`0.000999`** |
| **`CI_6_multimodal`** (Track A Full Win, 6-pillar) | **`0.807396`** | `0.122115` | `0.007757` | `0.135244` | `0.141885` | `0.151593` | **`+88.34`** | **`0.000999`** |
| **`AF_Closed_4`** (Track B `p1`, Closed-Family Alignment-Free) | **`0.754022`** | `0.122085` | `0.007783` | `0.135763` | `0.140068` | `0.154438` | **`+81.19`** | **`0.000999`** |
| **`AF_4P`** (Track B `p1`, 4-Pillar Alignment-Free) | **`0.793262`** | `0.122126` | `0.007754` | `0.135704` | `0.140583` | `0.152092` | **`+86.56`** | **`0.000999`** |
| **`M2_supervised_chrom`** (Track C `p2`, By-Chromosome Probing) | **`0.904124`** | `0.121268` | `0.007656` | `0.134126` | `0.141191` | `0.149629` | **`+102.26`** | **`0.000999`** |

### B. `complex_traits_matched_9` ($N = 11,400$, $22$ Chromosomes, $B = 1,000$)

| Model / Track | Observed `AUPRC` | Null Mean | Null SD | Null 95th %ile | Null 99th %ile | Null Max | $Z$-Score | Empirical $p$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`ZS_7_cadd_free`** (Track A Transfer / Complex `p1`) | **`0.281541`** | `0.109935` | `0.003740` | `0.116223` | `0.119237` | `0.123316` | **`+45.89`** | **`0.000999`** |
| **`ZS_8_standalone`** (Track A Transfer / Complex `p1`) | **`0.284569`** | `0.109947` | `0.003734` | `0.116400` | `0.119113` | `0.123219` | **`+46.76`** | **`0.000999`** |
| **`CI_6_multimodal`** (Track A Transfer / Complex `p1`) | **`0.283768`** | `0.109856` | `0.003702` | `0.116260` | `0.118744` | `0.123232` | **`+46.98`** | **`0.000999`** |

## 3. Conclusion
All models collapse to the theoretical finite-sample baseline ($\approx 0.122$ on Mendelian and $\approx 0.110$ on Complex for a $10\%$ positive rate) under within-chromosome label permutation, with zero null realizations approaching the observed scores ($Z = +45.89$ to $+102.26$, $p = 0.000999$ across all $1,000$ permutations).
