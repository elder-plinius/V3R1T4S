# How the object was built

Requirements: Python 3.13 with pandas 3.0.6, numpy 2.5.4, scipy 1.18.1 (requirements.txt). About 6 GB of disk for the
unzipped ProteinGym files. Laptop time is about 20 minutes, mostly reading CSVs.

Inputs (public, ProteinGym v1.3, Marks lab / OATML):
- https://marks.hms.harvard.edu/proteingym/ProteinGym_v1.3/zero_shot_substitutions_scores.zip
  (1,911,045,703 bytes, sha256 3fd7cdb5e78f1d43cabfabfeb6578c252b63af23ba2ab44db0094dc3a42de36d)
- https://marks.hms.harvard.edu/proteingym/ProteinGym_v1.3/DMS_ProteinGym_substitutions.zip
  (sha256 3a83766254ac9ac9984ec25cb73c6e010ea4418f5e35f143933e6b6e6473b921)
- https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/main/benchmarks/DMS_zero_shot/substitutions/Spearman/DMS_substitutions_Spearman_DMS_level.csv
  (the copy used: sha256 f432423b87f79ac9778dfac86e3d95be041d246bc618dc0a406b35b0b7466437, fetched 2026-10-18T18:46:05Z)

Commands, from this folder:
```
mkdir -p pg && cd pg && unzip -q ../zero_shot_substitutions_scores.zip && unzip -q ../DMS_ProteinGym_substitutions.zip && cd ..
python build_cache.py      # score cache (no sequences) + split.json (must equal the packaged split.json, sha256 bf163ae6...)
python m1_score.py         # method M1: selects 12 columns on the 187 fitting assays, writes result/<assay>.M1.csv for the 13 targets
sha256sum result/*.M1.csv   # must equal the sha256 values in verify-it-yourself/check_p1.py
python label_invariance.py # leakage check: target labels replaced by noise, so selection and predictions are bit-identical
```
explore_fit.py and explore_fit3.py are the leave-protein-out explorations on the fitting assays that chose K = 12 and
z-scoring before PREREG.md was frozen.

PREREG.md is the run's pre-registration, frozen 2026-10-18T19:11:52Z before any target assay was scored. It names its own
checker as attempts/checker/code/pg_checker.py (run-folder path); the packaged equivalent is
verify-it-yourself/check_spearman.py. No null test was required (PREREG: deterministic checker against a table value).
