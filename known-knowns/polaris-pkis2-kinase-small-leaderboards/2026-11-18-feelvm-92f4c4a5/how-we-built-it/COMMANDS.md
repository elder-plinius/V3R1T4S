# How we built it — exact commands and pinned requirements

Pinned stack of the producing run: Windows, python 3.15.2, scikit-learn 1.9.1, lightgbm 4.x,
rdkit 2026.09.2, pandas 3.1.1, pyarrow 26.0.1, numpy 2.5.5. Paths are relative to the V3R1T4S workspace
folder of the producing run; every path below is relative to the workspace folder.

## Commands, in order

```sh
# 1. official inputs (one plain curl each, honest UA)
curl -sS -A "V3R1T4S/1.0 (open research; github.com/elder-plinius/V3R1T4S)" \
     -o data/bench_pkis2-lok-slk-c-1.json \
     https://polarishub.io/api/v1/benchmark/polaris/pkis2-lok-slk-c-1
curl -sS -A "V3R1T4S/1.0 (open research; github.com/elder-plinius/V3R1T4S)" \
     -o data/table_v1.parquet \
     https://data.polarishub.io/dataset/polaris/kinase-pkis2-1/table.parquet
#    sha256: table_v1.parquet 653d2b6f3013c7c6b54b15ee8093fa2ac7380319bf6525c47dd182f4b75c4306
#            bench json        b7a58de2d71d5266... (recorded in object/official_inputs.json)

# 2. the live leaderboard pages (scout + immediately before the claim)
curl -sS -A "V3R1T4S/1.0 ..." -o data/page_pkis2-lok-slk-c-1.html \
     https://polarishub.io/benchmarks/polaris/pkis2-lok-slk-c-1
#    pre-claim re-fetch 2026-11-18T16:04:25Z, page sha256 5671da872b25a3afad11552ace4f0301...

# 3. model selection: train-only scaffold-grouped CV over 10 stable partitions
#    (fold groups by Murcko scaffold hashed with sha256 for reproducibility)
the workspace venv python (.venv-mace/Scripts/python.exe) code/lokslk_feasibility.py
the workspace venv python (.venv-mace/Scripts/python.exe) code/lokslk_select.py
#    selected: rank-blend(ET-regressor on the continuous label, LGBM classifier on CLASS)
#    CLASS_LOK OOF PR-AUC 0.6744 +- 0.0298; see selection.md

# 4. the frozen prediction (one read; PREREG.v3.md was written first)
the workspace venv python (.venv-mace/Scripts/python.exe) code/lokslk_oofs.py       # OOF arrays for the Platt maps
the workspace venv python (.venv-mace/Scripts/python.exe) code/final_predict_lokslk.py
the workspace venv python (.venv-mace/Scripts/python.exe) code/score_lokslk.py \
     --pred attempts/lokslk-cls/preds.csv \
     --bench data/bench_pkis2-lok-slk-c-1.json --table data/table_v1.parquet \
     --bar 0.2553191489361702 --bootstrap 10000
#    CLASS_LOK pr_auc 0.634333770922; bootstrap fraction above the bar 1.000000

# 5. harness calibration on this cell (published null-model values reproduced exactly)
the workspace venv python (.venv-mace/Scripts/python.exe) baseline/lokslk_null_model.py
#    BASELINE CALIBRATION: PASS

# 6. 400 label-permutation controls through the same pipeline
the workspace venv python (.venv-mace/Scripts/python.exe) code/null_test_lokslk.py
#    see null_test.md in this folder

# 7. InChIKey audit + independent recomputation (self-break)
the workspace venv python (.venv-mace/Scripts/python.exe) code/verify_lokslk.py
#    SELF_BREAK: SURVIVES
```

`lokslk_pipeline.py` in this folder is the same recipe in portable form (features computed directly
from the official parquet; the producing run computed them from the same molecules and mapped rows by
canonical SMILES — the canonical sets are identical, 640/640, so the feature matrices are identical).

## What the recipe uses and does not use

- Train data: the 508 official train indices only. Auxiliary: the continuous LOK/SLK
  percent-inhibition columns of those same rows (declared). No test-row value of any column, and no
  external PKIS or ChEMBL record, enters any fit, the Platt map, the blend, or feature building.
- Features: RDKit Morgan ECFP4 counts (2048) + 18 RDKit physchem descriptors from SMILES.
- InChIKey audit: 640 unique keys, 0 train/test overlap, 0 test-key skeletons across every
  auxiliary file fetched in the run.



