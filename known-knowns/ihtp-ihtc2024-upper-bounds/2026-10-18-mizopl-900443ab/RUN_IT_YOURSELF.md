# Run It Yourself (`2026-10-18-mizopl-900443ab`)

## 1. Quick Verification (< 0.1 seconds, Python 3.8+ standard library only)

From the root of this package directory:

```bash
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
File: object/sol_i27.json (209120 bytes, sha256=900443ab5205ab28d6ad4713b0023593f931007812ecf0e3410a4e49e1006cf7)
Total violations = 0
Costs breakdown:
  RoomAgeMix                    : 298
  RoomSkillLevel                : 3610
  ContinuityOfCare              : 3045
  ExcessiveNurseWorkload        : 620
  OpenOperatingTheater          : 3210
  SurgeonTransfer               : 290
  PatientDelay                  : 16490
  ElectiveUnscheduledPatients   : 22500
Total cost = 50063
IHTP_CHECK: PASS
PASS
```

## 2. Verification with the Official C++ Validator (`IHTP_Validator.cc`)

With `nlohmann/json.hpp` on the compiler include path:

```bash
clang++ -O3 -std=c++17 verify-it-yourself/IHTP_Validator.cc -o IHTP_Validator
./IHTP_Validator verify-it-yourself/i27.json object/sol_i27.json
```

Expected output:
```text
Total violations = 0
Costs: RoomAgeMix = 298, RoomSkillLevel = 3610, ContinuityOfCare = 3045, ExcessiveNurseWorkload = 620, OpenOperatingTheater = 3210, SurgeonTransfer = 290, PatientDelay = 16490, ElectiveUnscheduledPatients = 22500, 
Total cost = 50063
```

## 3. Baseline Comparison (`published_sol_i27.json`, Cost `50,976`)

```bash
python3 verify-it-yourself/author_checker_ihtp_check.py verify-it-yourself/i27.json the-record-we-beat/published_sol_i27.json 50976
```
