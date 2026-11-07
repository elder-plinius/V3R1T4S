# IHTC-2024 Instance `m28` Feasible Schedule with Objective `45037` (Was `45873` in Live Benchmark Table; `-836` Improvement)

## What
A feasible solution JSON file in object/sol_m28_45037.json for the IHTC-2024 competition instance m28 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 45037 (RoomAgeMix 52, RoomSkillLevel 1345, ContinuityOfCare 13495, ExcessiveNurseWorkload 165, OpenOperatingTheater 4880, SurgeonTransfer 410, PatientDelay 16290, ElectiveUnscheduledPatients 8400), verified both by our standalone Python port (verify-it-yourself/check_ihtp.py) and by the organisers' compiled C++ IHTP_Validator (IHTP_Validator.cc), strictly below the table upper bound of 45873 listed on https://ihtc2024.github.io/ihtp/index.html by 836 points.

## Check It Yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output line: `PASS` (`verify-it-yourself/run_checks.sh` runs `verify-it-yourself/check_ihtp.py`, our standalone Python 3 standard-library port of `IHTP_Validator.cc`, automatically downloading and caching the official `m28.json` instance from `https://ihtc2024.github.io/assets/files/ihtc2024_final_instances.zip`).

We also compiled and ran the organisers' official C++ validator (`https://ihtc2024.github.io/assets/files/IHTP_Validator.cc` linked with `nlohmann/json.hpp`) directly on `m28.json` and `object/sol_m28_45037.json`:
```text
VIOLATIONS: 
RoomGenderMix.....................0
PatientRoomCompatibility..........0
SurgeonOvertime...................0
OperatingTheaterOvertime..........0
MandatoryUnscheduledPatients......0
AdmissionDay......................0
RoomCapacity......................0
NursePresence.....................0
UncoveredRoom.....................0
Total violations = 0

COSTS (weight X cost): 
RoomAgeMix............................52 (  1 X  52)
RoomSkillLevel......................1345 (  5 X 269)
ContinuityOfCare...................13495 (  5 X 2699)
ExcessiveNurseWorkload...............165 (  5 X  33)
OpenOperatingTheater................4880 ( 40 X 122)
SurgeonTransfer......................410 ( 10 X  41)
PatientDelay.......................16290 ( 10 X 1629)
ElectiveUnscheduledPatients.........8400 (350 X  24)
Total cost = 45037
```

## Compared To
All comparisons are against the official IHTC-2024 benchmark status table at `https://ihtc2024.github.io/ihtp/index.html` (fetched on `2026-10-27T19:43:31Z`, HTTP `200`, SHA-256 `2b69fe2e2b6e0a978472aa3916c8c53a774e223e666f20966156802f9ce2f363`, recorded in `the-record-we-beat/table_snapshot.txt`, and re-verified on `2026-11-07T05:10:33Z`, HTTP `200`, SHA-256 `351d0dcb75edfe3d9c250ed6af1abcd71d9e14a947ae076df783972d283b39de`):

| Instance | Live Table BKS (`sol_m28.json`) | Our Objective (`object/sol_m28_45037.json`) | Improvement Margin | Hard Violations |
|:---:|---:|---:|---:|:---:|
| **`m28`** | `45873` | **`45037`** | **`-836` (`-1.8224%`)** | **`0`** |

### Soft-Cost Penalty Breakdown (`m28`)
- `RoomAgeMix`: 52
- `RoomSkillLevel`: 1345
- `ContinuityOfCare`: 13495
- `ExcessiveNurseWorkload`: 165
- `OpenOperatingTheater`: 4880
- `SurgeonTransfer`: 410
- `PatientDelay`: 16290
- `ElectiveUnscheduledPatients`: 8400
- **Total violations = 0**, **Total cost = 45037**

## Not Claimed
- We do not claim a mathematical proof of optimality (lower bound) for `m28`; `45037` is a certified feasible upper bound with zero hard-constraint violations.
- Per `kit/SUBMIT.md`, third-party benchmark instance input files are not bundled directly in the package; `verify-it-yourself/check_ihtp.py` retrieves the official archive on demand.

## Credits
- Contributor: `@HindsightWise` (`Zerbytheboss`).
- Sara Ceschia, Roberto Maria Rosati, Andrea Schaerf, and Eugenia Zanazzo (University of Udine) with Pieter Smet and Greet Vanden Berghe (KU Leuven) — IHTC-2024 competition organisers (`https://ihtc2024.github.io/`) for the problem formulation, benchmark instances, reference C++ validator (`IHTP_Validator.cc`), and the published best-known solution `sol_m28.json` (`https://ihtc2024.github.io/assets/files/ihtp/solutions/sol_m28.json`, cost `45873`), which served as the starting solution for our polisher run.
- Alfonso Gippini Requeijo (`arXiv:2610.00044`, *"Improved upper bounds for five IHTC-2024 benchmark instances via exact reoptimization of the nurse-to-room layer"*, 2026) for nurse-to-room reoptimization results on instances `i02`, `i05`, `m01`, `m03`, and `m04` (does not cover `m28`).
