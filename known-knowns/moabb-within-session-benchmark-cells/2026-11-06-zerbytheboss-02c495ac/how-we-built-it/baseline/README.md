# Published Baseline Reference & Local Reproduction (`moabb-within-session-benchmark-cells`)

- **Live MOABB Results Page**: `https://moabb.neurotechx.com/docs/paper_results.html` (`SSVEP (All classes)` paradigm table, fetched `2026-11-07T00:36:49Z`, SHA-256 `acba9cb52cf71de26d84b1ff00bd8a7a0a61b845ee2a017cb5531e25a2c76d4c`).
- **`Kalunga2016` (12 subjects, 4 classes)**:
  - Live page: `SSVEP_MDM = 70.89±13.44` (best), `SSVEP_TS+LR = 70.86±11.64`.
  - Our local reproduction (`WithinSessionEvaluation(paradigm=FilterBankSSVEP(n_classes=None), datasets=[Kalunga2016()], random_state=42)`): `SSVEP_MDM = 70.89±13.44` (exact match), `SSVEP_TS+LR = 70.86±11.64` (exact match).
- **`Nakanishi2015` (9 subjects, 12 classes)**:
  - Live page: `SSVEP_TS+LR = 87.22±15.96` (best), `SSVEP_MDM = 78.77±19.06`.
  - Our local reproduction (`WithinSessionEvaluation(paradigm=FilterBankSSVEP(n_classes=None), datasets=[Nakanishi2015()], random_state=42)`): `SSVEP_TS+LR = 87.22±15.96` (exact match; `87.28±15.90` in batch export, 1/1,620 trial L-BFGS tie difference), `SSVEP_MDM = 78.77±19.06` (exact match).
- **`MAMEM3` (5 classes)**:
  - Live page (`moabb v1.1.2`): `SSVEP_TS+LR = 42.10±14.33` (best), `SSVEP_MDM = 34.40±9.96`.
  - Our local rerun in `moabb-1.5.0`: `SSVEP_TS+LR = 38.62±15.01` (`11` subjects) / `39.92±15.14` (`10` subjects `1..10`); `SSVEP_MDM = 31.56±11.98` (`11` subjects).
