# Skeptic 1 — Reproduce Audit (`plmfit-trastuzumab-cdrh3-binding-mcc`)

context: fresh review session

## 1. Independent Execution & Cryptographic Verification

- **Target ID:** `plmfit-trastuzumab-cdrh3-binding-mcc`
- **Submission ID:** `2026-11-08-mizopl-465b77e7`
- **Command Executed:** `sh verify-it-yourself/run_checks.sh`
- **Negative Control Executed:** `python3 verify-it-yourself/verify.py --corrupt`

### Verified Certificate & Dataset Hashes
- `object/certificate.json`:
  `465b77e779fe37b92f9da4444bb53016a97449138ba4c28fb1d13a863e47908c`
- `object/manifest_sha256.json`:
  `96429fd22f9ecaedadc97e21506e19752e2f18e7a77216836ff535a347b27d6d`
- Official `LSSI-ETH/plmfit` Dataset & Scoreboard Commitments (zero sequences or `binary_score` labels copied inside `object/`):
  - `data/herH3/herH3_data_full.csv` (`36,560` rows, `17,149,024` bytes):
    `5137572eec7ce2689283854fefacd8bcd7c5cb2547d57f5ffc7c53c9fed4070f`
  - `https://raw.githubusercontent.com/LSSI-ETH/plmfit/main/README.md` (`14,780` bytes, fetched `2026-11-08T14:42:30Z`):
    `51b672d563c778ae40a435cad51424a5b8e0f82294211642d2bfff4983792f0b`
  - `test_row_keys_sha256` (`36,386` `(test_order_index, csv_row_index, no_mut)` keys):
    `0ace8e36377e1829550529d43341d4bd59b6fecbb2bdebdd40384cb67c92a05c`

## 2. Keyed Prediction CSV Verification (`36,386` Test Rows x 3 Seeds x 2 Tracks)

Every prediction CSV in `object/` is keyed by `(test_order_index, csv_row_index, no_mut, score_2body, pred_2body, score_1body, pred_1body)` covering all `36,386` `one_vs_rest == 'test'` rows in exact order (`0..36,385`), split into `_part1.csv` (`18,193` rows, `~637 KB < 1 MB`) and `_part2.csv` (`18,193` rows, `~662 KB < 1 MB`):

| Track (`object/seed_{42,43,44}_{track}_part{1,2}.csv`) | 3-Seed Test `MCC` (`mean +- SD`) | Bootstrap 95% CI | Test `AUROC` (`p2`) | Test `AP` (`p2`) | 1-Body `MCC` (`p3`) | 2-Body Epistatic Gain (`p3`) | Inductive `tau_CV` vs Oracle Gap (`p4`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`trackB_cv_learned` (Claimed Full Win + `p1..p4`)** | **`0.421004 +- 0.001735`** | **`[0.412067, 0.430182]`** | **`0.789510 +- 0.000669`** | **`0.624177 +- 0.000884`** | `0.410402 +- 0.001592` | **`+0.010601` MCC** | `0.001752` (`0.421004` vs `0.422756`) |
| **`trackA_canonical` (Parameter-Free Canonical Law)** | **`0.408391 +- 0.000411`** | **`[0.398892, 0.417982]`** | **`0.785602 +- 0.000461`** | **`0.622932 +- 0.000615`** | `0.401879 +- 0.000887` | **`+0.006512` MCC** | `0.001402` (`0.408391` vs `0.409793`) |

## 3. Adversarial Mutation & Negative Control Check

- Running `python3 verify-it-yourself/verify.py --corrupt` or mutating any matrix, vector, or digit in `object/*.json` or `object/seed_*.csv` is deterministically rejected by `verify.py` (`FAIL`, exit code `1`).

pass: true
