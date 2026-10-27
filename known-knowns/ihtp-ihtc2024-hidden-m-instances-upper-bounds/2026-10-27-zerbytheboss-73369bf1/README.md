# IHTC-2024 Instance `m29` Feasible Schedule with Objective `47253` (Was `48079` in Live Benchmark Table; `-826` Improvement)

## What
A feasible solution JSON file in object/sol_m29_47253.json for the IHTC-2024 competition instance m29 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 47253 (RoomAgeMix 55, RoomSkillLevel 1090, ContinuityOfCare 2453, ExcessiveNurseWorkload 80, OpenOperatingTheater 3600, SurgeonTransfer 120, PatientDelay 7305, ElectiveUnscheduledPatients 32550), verified by the official IHTP_Validator specification, strictly below the table upper bound of 48079 listed on https://ihtc2024.github.io/ihtp/index.html by 826 points (and strictly below hunt baseline 48082 by 829 points).

## Check It Yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output line: `PASS` (verifies in < 0.5 seconds on a standard CPU using the standalone Python 3 standard library port of `IHTP_Validator.cc`, automatically caching the official `m29.json` instance archive from `https://ihtc2024.github.io/assets/files/`).

## Compared To
All comparisons are against the official IHTC-2024 benchmark status table at `https://ihtc2024.github.io/ihtp/index.html` fetched on `2026-10-27T19:43:31Z` (HTTP `200`, SHA-256 `2b69fe2e2b6e0a978472aa3916c8c53a774e223e666f20966156802f9ce2f363`, recorded in `the-record-we-beat/table_snapshot.txt`):

| Instance | Official Table Baseline | Live Table BKS | Our Objective (`object/sol_m29_47253.json`) | Margin vs Baseline | Margin vs Live | Hard Violations |
|:---:|---:|---:|---:|---:|---:|:---:|
| **`m29`** | `48082` | `48079` | **`47253`** | **`-829`** | **`-826`** | **`0`** |

### Soft-Cost Penalty Breakdown (`m29`)
- `RoomAgeMix`: 55
- `RoomSkillLevel`: 1090
- `ContinuityOfCare`: 2453
- `ExcessiveNurseWorkload`: 80
- `OpenOperatingTheater`: 3600
- `SurgeonTransfer`: 120
- `PatientDelay`: 7305
- `ElectiveUnscheduledPatients`: 32550
- **Total violations = 0**, **Total cost = 47253**

## Not Claimed
- We do not claim a mathematical proof of optimality (lower bound) for `m29`; `47253` is a certified feasible upper bound with zero hard-constraint violations.
- Per `kit/SUBMIT.md`, third-party benchmark instance input files are not bundled directly in the package; `verify-it-yourself/check_ihtp.py` retrieves the official archive on demand.

## Credits
- Contributor: `zerbytheboss` (GitHub account `HindsightWise` operated by `zerbytheboss`).
- S. Ceschia, N. Thiessen, A. Schaerf et al. (IHTC-2024 Organizers) (https://ihtc2024.github.io/) for the problem formulation, benchmark instances, and reference C++ validator.
- D. Sylejmani et al. (arXiv:2610.00044) for nurse-to-room reoptimization baselines reflected on the live IHTC-2024 page.
