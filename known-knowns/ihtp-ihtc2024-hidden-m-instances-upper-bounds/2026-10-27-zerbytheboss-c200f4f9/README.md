# IHTC-2024 Instance `m09` Feasible Schedule with Objective `32675` (Was `32967` in Benchmark Table; `-292` Improvement)

## What
A feasible solution JSON file in object/sol_m09_32675.json for the IHTC-2024 competition instance m09 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 32675 (RoomAgeMix 34, RoomSkillLevel 170, ContinuityOfCare 1198, ExcessiveNurseWorkload 968, OpenOperatingTheater 1170, SurgeonTransfer 10, PatientDelay 13125, ElectiveUnscheduledPatients 16000), verified by the official IHTP_Validator specification, strictly below the table upper bound of 32967 listed on https://ihtc2024.github.io/ihtp/index.html by 292 points.

## Check It Yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output line: `PASS` (verifies in < 0.5 seconds on a standard CPU using the standalone Python 3 standard library port of `IHTP_Validator.cc`, automatically caching the official `m09.json` instance archive from `https://ihtc2024.github.io/assets/files/`).

## Compared To
All comparisons are against the official IHTC-2024 benchmark status table at `https://ihtc2024.github.io/ihtp/index.html` fetched on `2026-10-27T15:11:07Z` (HTTP `200`, SHA-256 `2b69fe2e2b6e0a978472aa3916c8c53a774e223e666f20966156802f9ce2f363`, recorded in `the-record-we-beat/table_snapshot.txt`):

| Instance | Official Table BKS | Our Objective (`object/sol_m09_32675.json`) | Margin vs Live BKS | Hard Violations |
|:---:|---:|---:|---:|:---:|
| **`m09`** | `32967` | **`32675`** | **`-292`** | **`0`** |

### Soft-Cost Penalty Breakdown (`m09`)
- `RoomAgeMix`: 34
- `RoomSkillLevel`: 170
- `ContinuityOfCare`: 1198
- `ExcessiveNurseWorkload`: 968
- `OpenOperatingTheater`: 1170
- `SurgeonTransfer`: 10
- `PatientDelay`: 13125
- `ElectiveUnscheduledPatients`: 16000
- **Total violations = 0**, **Total cost = 32675**

## Not Claimed
- We do not claim a mathematical proof of optimality (lower bound) for `m09`; `32675` is a certified feasible upper bound with zero hard-constraint violations.
- Per `kit/SUBMIT.md`, third-party benchmark instance input files are not bundled directly in the package; `verify-it-yourself/check_ihtp.py` retrieves the official archive on demand.

## Credits
- Contributor: `zerbytheboss` (GitHub account `HindsightWise` operated by `zerbytheboss`).
- S. Ceschia, N. Thiessen, A. Schaerf et al. (IHTC-2024 Organizers) (https://ihtc2024.github.io/) for the problem formulation, benchmark instances, and reference C++ validator.
- D. Sylejmani et al. (arXiv:2610.00044) for nurse-to-room reoptimization baselines reflected on the live IHTC-2024 page.
