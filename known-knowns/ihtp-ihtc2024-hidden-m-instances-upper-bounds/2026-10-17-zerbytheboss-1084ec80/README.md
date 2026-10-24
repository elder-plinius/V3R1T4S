# IHTC-2024 Instance `m26` Feasible Schedule with Objective `68496` (Was `69730` in Live BKS Table; `-1234` Improvement)

## What
A feasible solution JSON file in object/sol_m26_68496.json for the IHTC-2024 competition instance m26 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 68496 (RoomAgeMix 72, RoomSkillLevel 2470, ContinuityOfCare 2974, ExcessiveNurseWorkload 130, OpenOperatingTheater 2580, SurgeonTransfer 200, PatientDelay 12370, ElectiveUnscheduledPatients 47700), verified by the official IHTP_Validator specification, strictly below the best-known upper bound of 69730 listed on https://ihtc2024.github.io/ihtp/index.html by 1234 points.

## Check It Yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last output line: `PASS` (runs in ~0.3 seconds on a laptop using the Python 3 standard library port of `IHTP_Validator.cc`, automatically fetching the official `m26.json` instance from `https://ihtc2024.github.io/assets/files/` if not already cached in `$TMPDIR`).

## Compared To
All comparisons are against the official IHTC-2024 benchmark status table at `https://ihtc2024.github.io/ihtp/index.html` fetched on `2026-10-17T16:46:37Z` (HTTP `200`, SHA-256 `7c09c272ce00ce581c8537a3316898c97f7cfcf9a3fc6cdbeaac00e08279b495`, recorded in `the-record-we-beat/snapshot_2026-10-17.md`):

| Instance | Official BKS (`ihtc2024.github.io`) | Our Objective (`object/sol_m26_68496.json`) | Margin | Hard Constraint Violations |
|---|---:|---:|---:|---:|
| **`m26`** | `69730` | **`68496`** | **`-1234`** | **`0`** ( across all 9 hard constraint categories) |

### Full Objective Component Breakdown (`m26`)
- `RoomAgeMix 72, RoomSkillLevel 2470, ContinuityOfCare 2974, ExcessiveNurseWorkload 130, OpenOperatingTheater 2580, SurgeonTransfer 200, PatientDelay 12370, ElectiveUnscheduledPatients 47700`
- **`Total violations = 0`**, **`Total cost = 68496`**

In the same coupled Simulated Annealing + Kempe-chain nurse/patient local search run (`how-we-built-it/IHTP_Polisher.cc`), we strictly improved **28 of the 30 `m`-instances** (including `m26: 69730 -> 68496 (-1234)`, `m29: 48082 -> 47368 (-714)`, `m28: 45913 -> 45274 (-639)`, `m24: 30873 -> 30363 (-510)`, `m27: 28028 -> 27533 (-495)`, `m30: 31649 -> 31181 (-468)`, `m09: 32967 -> 32675 (-292)`, `m21: 25170 -> 24934 (-236)`, `m23: 18301 -> 18091 (-210)`, `m14: 13368 -> 13177 (-191)`, `m11: 35030 -> 34866 (-164)`, and `m01: 3380 -> 3379 (-1 vs arXiv:2610.00044)`) and **28 of the 30 `i`-instances** (including `i27: 50976 -> 50192 (-784)`, `i19: 43857 -> 43410 (-447)`, `i26: 64352 -> 64003 (-349)`, `i23: 37550 -> 37268 (-282)`, `i20: 29098 -> 28851 (-247)`, `i30: 37387 -> 37201 (-186)`, and `i02: 1263 -> 1262 (-1 vs arXiv:2610.00044)`), all available for individual per-cell packages.

## Not Claimed
- We do not claim a proof of optimality (lower bound) for `m26`; `68496` is a verified feasible upper bound with `0` hard-constraint violations.
- Per `kit/SUBMIT.md`, the third-party benchmark input file `m26.json` is not copied into this package; `verify-it-yourself/check_ihtp.py` loads it from local cache or fetches the official `ihtc2024` zip archive on demand.

## Credits
- **Contributor**: `Zerbytheboss` (GitHub account `HindsightWise` is operated by `Zerbytheboss`).
- **S. Ceschia, N. Thiessen, A. Schaerf et al. (IHTC-2024 Organizers)** ([`https://ihtc2024.github.io/`](https://ihtc2024.github.io/)) for the problem formulation, instances, BKS table, and reference C++ `IHTP_Validator.cc`.
- **D. Sylejmani et al. (`arXiv:2610.00044`)** for recent nurse-to-room reoptimization baselines reflected on the live IHTC-2024 page.
