# Verification Receipts — `(3, 34)` Complex Line Packing

## 1. Live Leaderboard & Open PR Verification (`2026-11-17T00:12:14.359235+00:00`)

- **README URL:** `https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md`
- **README HTTP Status:** `200`
- **README SHA-256:** `699dbe7157363e568d11e019a0ea98178ec9f52f8834e900587c162801b0502d`
- **Open PRs Endpoint:** `https://api.github.com/repos/gnikylime/GameofSloanes/pulls?state=open&per_page=100`
- **Open PR Count / Claimed Cells:** `10` open PRs (`#11..#20`), `71` claimed cells
- **`(3, 34)` Status:** `IS_CLAIMED_IN_OPEN_PR: False`, `IS_PROVABLY_OPTIMAL: False`, `IS_CONJECTURALLY_OPTIMAL: False`
- **Live Table Values:** `TABLE_MU = 0.75683480`, `TABLE_LB = 0.67202151`, `TABLE_FILEPATH = CurrentBestPackings/3x34_jrr.txt`
- **Upstream Baseline File:** [`CurrentBestPackings/3x34_jrr.txt`](https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/3x34_jrr.txt) (`SHA-256: 159cb51fdd209252b1b4c2a190b8fccefed7415e5254a3226160d4218082cf1e`)

## 2. Independent Measurements (`float64` Snapshot vs True 60-Digit Precision)

- **Recorded Colab Snapshot (`float64` expansions from intermediate IEEE-754 float64 values):**
  - `BASELINE_MU_FLOAT64_EXPANSION` (upstream `3x34_jrr.txt`): `0.7568347972536282330935364370816387236118316650390625` (`129` active pairs within `1e-8`)
  - `CANDIDATE_MU_FLOAT64_EXPANSION` (`object/3x34_new.txt`): `0.75649479818227172156497317700996063649654388427734375` (`129` active pairs within `1e-8`)
  - `IMP_VS_TABLE_FLOAT64`: `0.0003400018177283081755` (`VERIFICATION_SUCCESS_IS_WIN: True`, `ABOVE_LOWER_BOUND: True`)

- **True 60-Digit Precision Measurements (parsed directly from decimal coordinate strings via `decimal.Decimal` `prec = 60` and `mpmath.mp.dps = 60`):**
  - **Candidate `object/3x34_new.txt`** (`SHA-256: 7b0745355c9f502a7eb731c0ec7541db1d21edfabe543f6274eacda06f2b0597`):
    - `Decimal` (`prec = 60`): `0.756494798182271705164224601239675096749550724764985832115081`, `worst = (1, 21)`
    - `mpmath` (`dps = 60`): `0.756494798182271705164224601239675096749550724764985832115081`, `worst = (1, 21)`
    - `imp_vs_table`: `+0.000340001817728294835775398760324903250449275235014167884919`
  - **Upstream Baseline `CurrentBestPackings/3x34_jrr.txt`** (`SHA-256: 159cb51fdd209252b1b4c2a190b8fccefed7415e5254a3226160d4218082cf1e`):
    - `Decimal` (`prec = 60`): `0.756834797253628206097823785778147954374744559786819000003653`, `worst = (2, 27)`
    - `mpmath` (`dps = 60`): `0.75683479725362820609782378577814795437474455978681900000366`, `worst = (2, 27)`
    - `imp_vs_baseline`: `+0.000339999071356500933599184538472857625193835021833167888572`

- **Verbatim Output of `sh verify-it-yourself/run_checks.sh`:**

```text
candidate=object/3x34_new.txt mu=0.756494798182271705164224601239675096749550724764985832115081 worst=(1, 21) imp_vs_table=0.000340001817728294835775398760324903250449275235014167884919
upstream_baseline_url=https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/3x34_jrr.txt upstream_baseline_sha256=159cb51fdd209252b1b4c2a190b8fccefed7415e5254a3226160d4218082cf1e recorded_baseline_mu_60=0.756834797253628206097823785778147954374744559786819000003653 imp_vs_recorded_baseline=0.000339999071356500933599184538472857625193835021833167888572
PASS
```

- **Self-Break Rejection:** Mutating a single digit in `object/3x34_new.txt` causes `verify-it-yourself/run_checks.sh` to print `FAIL` and exit with status `1`.
