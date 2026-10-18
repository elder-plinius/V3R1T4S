# Verification Receipts (`2026-10-18-mizopl-900443ab`)

## 1. Standalone Pure-Python Checker (`verify-it-yourself/run_checks.sh`)

Command:
```bash
sh verify-it-yourself/run_checks.sh
```

Real command output:
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

## 2. Official Competition Validator (`verify-it-yourself/IHTP_Validator.cc`)

Command:
```bash
./IHTP_Validator verify-it-yourself/i27.json object/sol_i27.json
```

Real command output:
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
RoomAgeMix...........................298 (  1 X 298)
RoomSkillLevel......................3610 ( 10 X 361)
ContinuityOfCare....................3045 (  1 X 3045)
ExcessiveNurseWorkload...............620 ( 10 X  62)
OpenOperatingTheater................3210 ( 30 X 107)
SurgeonTransfer......................290 ( 10 X  29)
PatientDelay.......................16490 (  5 X 3298)
ElectiveUnscheduledPatients........22500 (500 X  45)
Total cost = 50063
```
