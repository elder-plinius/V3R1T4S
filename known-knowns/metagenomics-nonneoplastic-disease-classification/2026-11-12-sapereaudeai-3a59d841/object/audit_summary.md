
### W1: T2D (Qin 2012) within-cohort, 170 T2D / 174 control (published RF species AUC 0.744)

| quantity | model | AUC | interval | fraction of published signal |
|---|---|---|---|---|
| species RF (paper baseline), reproduced | RF500 species | 0.7442 | 0.686-0.802 | 1.001 (0.76 to 1.24) |
| covariates only: depth | LR covariates | 0.5910 | 0.523-0.659 | 0.373 (0.09 to 0.65) |
| covariates only: age | LR covariates | 0.7345 | 0.676-0.793 | 0.961 (0.72 to 1.20) |
| covariates only: bmi | LR covariates | 0.5549 | 0.488-0.621 | 0.225 (-0.05 to 0.50) |
| covariates only: age+bmi | LR covariates | 0.7303 | 0.672-0.789 | 0.944 (0.70 to 1.18) |
| covariates only: country | LR covariates | 0.5000 | 0.500-0.500 | 0.000 (0.00 to 0.00) |
| covariates only: study | LR covariates | 0.5000 | 0.500-0.500 | 0.000 (0.00 to 0.00) |
| covariates only: ALL | LR covariates | 0.7301 | 0.671-0.790 | 0.943 (0.70 to 1.19) |
| covariates only: ALL+sex | LR covariates | 0.7517 | 0.693-0.811 | 1.032 (0.79 to 1.27) |
| covariates only: study | RF covariates | 0.5000 | 0.500-0.500 | 0.000 (0.00 to 0.00) |
| covariates only: ALL | RF covariates | 0.7677 | 0.715-0.820 | 1.097 (0.88 to 1.31) |
| within-study label permutation (mean of 400) | RF100 species, repeat-0 folds | 0.5000 | 0.422-0.575 | -0.000 (-0.32 to 0.31) |
| within-study permutation: max control | RF100 species, repeat-0 folds | 0.6127 |  | 0.462 |
| real labels, same reduced pipeline | RF100 species, repeat-0 folds | 0.7382 |  | 0.976 |

### W2: WT2D (Karlsson 2013) within-cohort, 53 T2D / 43 NGT (published RF species AUC 0.762)

| quantity | model | AUC | interval | fraction of published signal |
|---|---|---|---|---|
| species RF (paper baseline), reproduced | RF500 species | 0.7684 | 0.645-0.892 | 1.024 (0.55 to 1.50) |
| covariates only: depth | LR covariates | 0.6606 | 0.527-0.794 | 0.613 (0.10 to 1.12) |
| covariates only: age | LR covariates | 0.5654 | 0.425-0.706 | 0.250 (-0.29 to 0.79) |
| covariates only: bmi | LR covariates | 0.6724 | 0.540-0.805 | 0.658 (0.15 to 1.16) |
| covariates only: age+bmi | LR covariates | 0.6624 | 0.539-0.786 | 0.620 (0.15 to 1.09) |
| covariates only: country | LR covariates | 0.5046 | 0.435-0.574 | 0.018 (-0.25 to 0.28) |
| covariates only: study | LR covariates | 0.5000 | 0.500-0.500 | 0.000 (0.00 to 0.00) |
| covariates only: ALL | LR covariates | 0.6828 | 0.553-0.812 | 0.698 (0.20 to 1.19) |
| covariates only: ALL+sex | LR covariates | 0.6830 | 0.554-0.812 | 0.699 (0.20 to 1.19) |
| covariates only: study | RF covariates | 0.5000 | 0.500-0.500 | 0.000 (0.00 to 0.00) |
| covariates only: ALL | RF covariates | 0.5736 | 0.449-0.698 | 0.281 (-0.20 to 0.76) |
| within-study label permutation (mean of 400) | RF100 species, repeat-0 folds | 0.5024 | 0.360-0.655 | 0.009 (-0.54 to 0.59) |
| within-study permutation: max control | RF100 species, repeat-0 folds | 0.7372 |  | 0.905 |
| real labels, same reduced pipeline | RF100 species, repeat-0 folds | 0.7759 |  | 1.053 |

### P1: T2D + WT2D merged, 223 / 217 (published RF species AUC 0.743)

| quantity | model | AUC | interval | fraction of published signal |
|---|---|---|---|---|
| species RF (paper baseline), reproduced | RF500 species | 0.7426 | 0.691-0.795 | 0.998 (0.78 to 1.21) |
| covariates only: depth | LR covariates | 0.5940 | 0.533-0.655 | 0.387 (0.13 to 0.64) |
| covariates only: age | LR covariates | 0.6852 | 0.630-0.740 | 0.762 (0.54 to 0.99) |
| covariates only: bmi | LR covariates | 0.5789 | 0.518-0.640 | 0.325 (0.07 to 0.58) |
| covariates only: age+bmi | LR covariates | 0.6817 | 0.627-0.736 | 0.748 (0.52 to 0.97) |
| covariates only: country | LR covariates | 0.5105 | 0.467-0.554 | 0.043 (-0.14 to 0.22) |
| covariates only: study | LR covariates | 0.5175 | 0.473-0.562 | 0.072 (-0.11 to 0.26) |
| covariates only: ALL | LR covariates | 0.7112 | 0.660-0.763 | 0.869 (0.66 to 1.08) |
| covariates only: ALL+sex | LR covariates | 0.7271 | 0.677-0.778 | 0.934 (0.73 to 1.14) |
| covariates only: study | RF covariates | 0.5175 | 0.473-0.562 | 0.072 (-0.11 to 0.26) |
| covariates only: ALL | RF covariates | 0.7311 | 0.680-0.782 | 0.951 (0.74 to 1.16) |
| pair decomposition same-study pairs (31859 pairs) | species_rf | 0.7420 | 0.731-0.752 | 0.996 |
| pair decomposition diff-study pairs (16532 pairs) | species_rf | 0.7326 | 0.709-0.747 | 0.957 |
| pair decomposition same-study pairs (31859 pairs) | cov_lr_study | 0.4488 | 0.426-0.464 | -0.211 |
| pair decomposition diff-study pairs (16532 pairs) | cov_lr_study | 0.5565 | 0.544-0.558 | 0.233 |
| pair decomposition same-study pairs (31859 pairs) | cov_lr_ALL | 0.7181 | 0.712-0.722 | 0.897 |
| pair decomposition diff-study pairs (16532 pairs) | cov_lr_ALL | 0.6851 | 0.675-0.691 | 0.762 |
| within-study label permutation (mean of 400) | RF100 species, repeat-0 folds | 0.4997 | 0.430-0.568 | -0.001 (-0.29 to 0.28) |
| within-study permutation: max control | RF100 species, repeat-0 folds | 0.5964 |  | 0.397 |
| real labels, same reduced pipeline | RF100 species, repeat-0 folds | 0.7434 |  | 1.002 |

### P2: T2D + WT2D + healthy stool controls of cirrhosis, colorectal, HMP, IBD datasets, 223 / 659 (published RF species AUC 0.837)

| quantity | model | AUC | interval | fraction of published signal |
|---|---|---|---|---|
| species RF (paper baseline), reproduced | RF500 species | 0.8560 | 0.825-0.887 | 1.056 (0.96 to 1.15) |
| covariates only: depth | LR covariates | 0.6612 | 0.624-0.698 | 0.478 (0.37 to 0.59) |
| covariates only: age | LR covariates | 0.7758 | 0.741-0.810 | 0.818 (0.72 to 0.92) |
| covariates only: bmi | LR covariates | 0.6985 | 0.659-0.738 | 0.589 (0.47 to 0.71) |
| covariates only: age+bmi | LR covariates | 0.7733 | 0.739-0.808 | 0.811 (0.71 to 0.91) |
| covariates only: country | LR covariates | 0.7634 | 0.738-0.789 | 0.782 (0.71 to 0.86) |
| covariates only: study | LR covariates | 0.8404 | 0.817-0.864 | 1.010 (0.94 to 1.08) |
| covariates only: ALL | LR covariates | 0.9030 | 0.881-0.925 | 1.196 (1.13 to 1.26) |
| covariates only: ALL+sex | LR covariates | 0.9098 | 0.888-0.932 | 1.216 (1.15 to 1.28) |
| covariates only: study | RF covariates | 0.8420 | 0.819-0.865 | 1.015 (0.95 to 1.08) |
| covariates only: ALL | RF covariates | 0.9105 | 0.890-0.931 | 1.218 (1.16 to 1.28) |
| pair decomposition same-study pairs (31859 pairs) | species_rf | 0.7351 | 0.727-0.741 | 0.698 |
| pair decomposition diff-study pairs (115098 pairs) | species_rf | 0.8882 | 0.885-0.892 | 1.152 |
| pair decomposition same-study pairs (31859 pairs) | cov_lr_study | 0.4389 | 0.422-0.456 | -0.181 |
| pair decomposition diff-study pairs (115098 pairs) | cov_lr_study | 0.9351 | 0.931-0.936 | 1.291 |
| pair decomposition same-study pairs (31859 pairs) | cov_lr_ALL | 0.7172 | 0.711-0.721 | 0.644 |
| pair decomposition diff-study pairs (115098 pairs) | cov_lr_ALL | 0.9529 | 0.952-0.954 | 1.344 |
| within-study label permutation (mean of 400) | RF100 species, repeat-0 folds | 0.7595 | 0.734-0.785 | 0.770 (0.70 to 0.84) |
| within-study permutation: max control | RF100 species, repeat-0 folds | 0.7970 |  | 0.881 |
| real labels, same reduced pipeline | RF100 species, repeat-0 folds | 0.8434 |  | 1.019 |
| null N1: study-only LR, repeat-0 folds (real) | LR study | 0.8305 |  | 0.981 |
| null N1: best of 400 study-permuted controls | LR study | 0.5752 |  | 0.223 |
