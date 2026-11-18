# Model selection (train rows only; 10 scaffold-grouped CV partitions, stable sha256 fold groups)

Cell: `polaris/pkis2-lok-slk-c-1`, primary target CLASS_LOK (the metric the live leaderboard lists),
secondary CLASS_SLK. No test value was read at selection time.

| ranker (per target) | CLASS_LOK PR-AUC | CLASS_SLK PR-AUC | mean |
|---|---|---|---|
| ExtraTrees classifier | 0.550 | 0.326 | 0.438 |
| ExtraTrees classifier (balanced) | 0.634 | 0.346 | 0.490 |
| RandomForest classifier | 0.645 | 0.359 | 0.502 |
| LightGBM classifier | 0.661 | 0.293 | 0.477 |
| ET regressor on the continuous label | 0.623 | 0.380 | 0.502 |
| rank-blend(reg, RandomForest) | 0.642 | 0.389 | 0.516 |
| **rank-blend(reg, LightGBM)** | **0.674 +- 0.030** | 0.352 | 0.513 |

The frozen recipe is the CLASS_LOK winner: per target, rank-average of
(ExtraTreesRegressor(800, mf=0.1, random_state=0) on the continuous percent-inhibition label,
LGBMClassifier(400, lr=0.05) on the class label). Train-only OOF of the exact frozen blend:
CLASS_LOK 0.6744 +- 0.0298, CLASS_SLK 0.3519 +- 0.0393; CLASS_LOK ROC 0.87.

Note on a caught bug: the first feasibility run indexed a full-table feature matrix with positional
fold indices, so features and labels were misaligned and every model looked chance-level (ROC
0.47-0.50 under both scaffold and random CV). That contradicted the train correlation
corr(LOKc, CLASS_LOK) = 0.854, the bug was found and fixed, and every number in the table above is
from the fixed pipeline (the broken run's output is retained in the producing run's folder as the
record of what was seen first).

Test-fold reads on this cell: exactly one (the frozen prediction). Baseline and null reads are
separate and disclosed in null_test.md and baseline/.
