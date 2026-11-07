# IHTC-2024 Instance `m26` Feasible Schedule with Objective `68496` (Was `69715` in Live BKS Table; `-1219` Improvement)

## What
A feasible solution JSON file in object/sol_m26_68496.json for the IHTC-2024 competition instance m26 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 68496 (RoomAgeMix 72, RoomSkillLevel 2470, ContinuityOfCare 2974, ExcessiveNurseWorkload 130, OpenOperatingTheater 2580, SurgeonTransfer 200, PatientDelay 12370, ElectiveUnscheduledPatients 47700), verified by both the official compiled C++ IHTP_Validator and its standalone Python port, strictly below the best-known upper bound of 69715 listed on https://ihtc2024.github.io/ihtp/index.html by 1219 points.

## Check It Yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last output line: `PASS` (runs in ~0.3 seconds on a laptop using `verify-it-yourself/check_ihtp.py`, our standalone Python 3 standard library port of `IHTP_Validator.cc`, automatically fetching the official `m26.json` instance from `https://ihtc2024.github.io/assets/files/ihtc2024_final_instances.zip` if not already cached in `$TMPDIR`).

We also compiled and ran the organisers' official C++ validator (`https://ihtc2024.github.io/assets/files/IHTP_Validator.cc`, compiled with `clang++ -O3 -std=c++17 IHTP_Validator.cc -o IHTP_Validator`) directly on `m26.json` and `object/sol_m26_68496.json`; its verbatim output is:
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
RoomAgeMix............................72 (  1 X  72)
RoomSkillLevel......................2470 ( 10 X 247)
ContinuityOfCare....................2974 (  1 X 2974)
ExcessiveNurseWorkload...............130 ( 10 X  13)
OpenOperatingTheater................2580 ( 30 X  86)
SurgeonTransfer......................200 ( 10 X  20)
PatientDelay.......................12370 ( 10 X 1237)
ElectiveUnscheduledPatients........47700 (450 X 106)
Total cost = 68496
```

## Compared To
All comparisons are against the official IHTC-2024 benchmark status table at `https://ihtc2024.github.io/ihtp/index.html` fetched on `2026-11-07T05:10:33Z` (HTTP `200`, SHA-256 `351d0dcb75edfe3d9c250ed6af1abcd71d9e14a947ae076df783972d283b39de`, recorded in `the-record-we-beat/snapshot_2026-10-17.md`; Internal verification notes are in `panel/`):

| Instance | Official BKS (`ihtc2024.github.io`, `sol_m26.json`) | Our Objective (`object/sol_m26_68496.json`) | Margin | Hard Constraint Violations |
|---|---:|---:|---:|---:|
| **`m26`** | `69715` | **`68496`** | **`-1219`** | **`0`** (across all 9 hard constraint categories) |

### Full Objective Component Breakdown (`m26`)
- `RoomAgeMix 72, RoomSkillLevel 2470, ContinuityOfCare 2974, ExcessiveNurseWorkload 130, OpenOperatingTheater 2580, SurgeonTransfer 200, PatientDelay 12370, ElectiveUnscheduledPatients 47700`
- **`Total violations = 0`**, **`Total cost = 68496`**

## Not Claimed
- We do not claim a proof of optimality (lower bound) for `m26`; `68496` is a verified feasible upper bound with `0` hard-constraint violations obtained by polishing the published `sol_m26.json` schedule with `how-we-built-it/IHTP_Polisher.cpp`.
- Per `kit/SUBMIT.md`, the third-party benchmark input file `m26.json` is not copied into this package; `verify-it-yourself/check_ihtp.py` loads it from local cache or fetches the official `ihtc2024_final_instances.zip` archive on demand.

## Credits
- **Contributor**: `Zerbytheboss` (GitHub account `HindsightWise` is operated by `Zerbytheboss`).
- **Sara Ceschia, Roberto Maria Rosati, Andrea Schaerf, and Eugenia Zanazzo (University of Udine), and Pieter Smet and Greet Vanden Berghe (KU Leuven)** — the IHTC-2024 organisers ([`https://ihtc2024.github.io/`](https://ihtc2024.github.io/)) — for the problem formulation, instances, published `sol_m26.json` starting solution, BKS table, and official C++ `IHTP_Validator.cc`.
- **Alfonso Gippini Requeijo** (*"Improved upper bounds for five IHTC-2024 benchmark instances via exact reoptimization of the nurse-to-room layer"*, `arXiv:2610.00044`, 2026) for the exact nurse-to-room reoptimization study on `i02`, `i05`, `m01`, `m03`, and `m04`.
