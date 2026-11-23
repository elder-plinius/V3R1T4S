# The record we beat (table snapshot)

Benchmark: `polaris/pkis2-lok-slk-c-1` — multi-task classification (CLASS_LOK, CLASS_SLK;
threshold > 80% inhibition) on the PKIS2 LOK/SLK wild-type panel, dataset `polaris/kinase-pkis2-1`
(640 compounds, official scaffold split 508 train / 132 test).

| what | value |
|---|---|
| URL | https://polarishub.io/benchmarks/polaris/pkis2-lok-slk-c-1 |
| fetch 1 (scout) | 2026-11-18T13:5xZ, HTTP 200, page sha256 recorded in the producing run |
| fetch 2 (pre-claim) | 2026-11-18T16:04:25Z, HTTP 200, 186443 bytes, page sha256 5671da872b25a3afad11552ace4f0301c3f5afa3db0ac23f45868c9cddb58fbc |
| entries | 6 (board NOT empty) |
| best listed pr_auc | **0.2553191489361702** (`pkis2-lok-slk-c-1_DGLGraphTransformer_PNAModel`, Polaris "baseline null model", submitted 2023-12-08, CLASS_LOK ROC 0.6759259259259259) |
| other listed pr_auc | 0.18181818181818182 x4, 0.17394416607015034 |
| our value | CLASS_LOK pr_auc **0.634333770922** (ROC 0.880208333333) |

The listed values, the per-entry result pages, and the evidence that every listed value equals the
entry's CLASS_LOK row (the first target's metric):

| result id | entry | CLASS_LOK pr_auc (listed) | CLASS_SLK pr_auc |
|---|---|---|---|
| zqdl6nC4UmLpdpKi0p9a3 | DGLGraphTransformer_PNAModel | 0.2553191489361702 | 0.10317460317460317 |
| MbxXf91ywqASbWKZ3tB7t | DGLGraphTransformer_MPNNModel | 0.18181818181818182 | 0.1148018648018648 |
| VeyE6vondB8jpuLcwvHY1 | DGLGraphTransformer_GCNModel | 0.18181818181818182 | 0.09848484848484848 |
| fFUrA0qLVjU45bZr9cbGk | DGLGraphTransformer_GATModel | 0.18181818181818182 | 0.09848484848484848 |
| nx1cYFuvUNDjKv4vn25F3 | DGLGraphTransformer_AttentiveFPModel | 0.17394416607015034 | 0.09848484848484848 |
| 1PyKyhtqjixSkDxwsSpES | pharm2D_FCModel | 0.18181818181818182 | 0.1 |

All six entries are Polaris "baseline null model" submissions with "No references provided" and no
code or prediction links; four are constant all-positive predictors (CLASS_LOK pr_auc = test
prevalence 24/132), which is why their values are exactly reproducible and serve as the harness
calibration for this cell. Never the pages themselves; the extracted values and fetch facts only.
