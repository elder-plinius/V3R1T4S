# Verification Receipts — `(3, 34)` Complex Line Packing

## 1. Live Leaderboard & Open PR Verification (Google Colab, `2026-11-17T00:12:14.359235+00:00`)

- **README URL:** `https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md`
- **README HTTP Status:** `200`
- **README SHA-256:** `699dbe7157363e568d11e019a0ea98178ec9f52f8834e900587c162801b0502d`
- **Open PRs Endpoint:** `https://api.github.com/repos/gnikylime/GameofSloanes/pulls?state=open&per_page=100`
- **Open PR Count / Claimed Cells:** `10` open PRs (`#11..#20`), `71` claimed cells
- **`(3, 34)` Status:** `IS_CLAIMED_IN_OPEN_PR: False`, `IS_PROVABLY_OPTIMAL: False`, `IS_CONJECTURALLY_OPTIMAL: False`
- **Live Table Values:** `TABLE_MU = 0.75683480`, `TABLE_LB = 0.67202151`, `TABLE_FILEPATH = CurrentBestPackings/3x34_jrr.txt`

## 2. Independent 60-Digit Precision Measurements

- **Colab `mpmath` (`mp.dps = 60`):**
  - `BASELINE_MU_MP60` (`3x34_jrr.txt`): `0.7568347972536282330935364370816387236118316650390625` (`129` active pairs within `1e-8`)
  - `CANDIDATE_MU_MP60` (`object/3x34_new.txt`): `0.75649479818227172156497317700996063649654388427734375` (`129` active pairs within `1e-8`)
  - `IMP_VS_TABLE`: `0.0003400018177283081755` (`VERIFICATION_SUCCESS_IS_WIN: True`, `ABOVE_LOWER_BOUND: True`)
- **Local Python 3 `decimal.Decimal` (`prec = 60`, `verify-it-yourself/check_submission.py`):**
  - `object/3x34_new.txt` (`SHA-256: 7b0745355c9f502a7eb731c0ec7541db1d21edfabe543f6274eacda06f2b0597`): `mu = 0.756494798182271705164224601239675096749550724764985832115081`, `worst = (1, 21)`, `imp_vs_table = +0.000340001817728295`, `PASS`.
  - `the-record-we-beat/3x34_jrr.txt`: `mu = 0.756834797253628206097823785778147954374744559786819000003653`, `imp_vs_baseline = +0.000339999071356501`.
- **Self-Break Rejection:** Mutating a single digit in `object/3x34_new.txt` causes `verify-it-yourself/run_checks.sh` to print `FAIL` and exit with status `1`.
