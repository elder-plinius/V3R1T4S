# REPRODUCE skeptic: i16 claim (claim/sol_i16.json, cost 10054 vs listed 10139)
context: subagent (Claude Code Agent tool, fresh context)

Scope: read only claim/. No solver code was supplied or read. I wrote my own checker before looking at any author tooling.

## 1. Independent checker, written from the definitions in claim/IHTP_Validator.cc
Definitions used (quoted from the validator):
- Stay window: `for (d = ad; d < min(in.Days(), ad + in.PatientLengthOfStay(p)); d++)`. Occupants stay on days 0..length_of_stay-1 in `room_id`.
- Shift offset: `s1 = s - ad * in.ShiftsPerDay()` for patients; occupants use `s` directly.
- Hard constraints: RoomGenderMix `min(room_day_a_patients, room_day_b_patients)`; PatientRoomCompatibility; SurgeonOvertime `surgeon_day_load - SurgeonMaxSurgeryTime`; OperatingTheaterOvertime `time - OperatingTheaterAvailability`; MandatoryUnscheduledPatients; AdmissionDay `admission_day < SurgeryReleaseDay || > PatientLastPossibleDay` with `PatientMandatory(p) ? surgery_due_day : days-1`; RoomCapacity; NursePresence; UncoveredRoom `room_shift_nurse == -1 && room_day_patient_list[r][d].size()>0`.
- Soft costs: RoomAgeMix `max - min` age group per room-day; RoomSkillLevel `SkillLevelRequired - NurseSkillLevel(n)` when positive; ContinuityOfCare = distinct nurses per patient/occupant within the horizon; ExcessiveNurseWorkload `load - NurseMaxLoad(n,s)` over each nurse's working shifts; OpenOperatingTheater = (theater, day) pairs with at least one patient; SurgeonTransfer `count - 1`; PatientDelay `admission_day - SurgeryReleaseDay`; ElectiveUnscheduledPatients. Weights come from the instance in validator order: room_mixed_age, room_nurse_skill, continuity_of_care, nurse_eccessive_workload, open_operating_theater, surgeon_transfer, patient_delay, unscheduled_optional (1, 10, 1, 1, 40, 5, 15, 450).
- Structural checks (on top of the validator): unknown or duplicate patient/nurse/room/theater ids; admission day and nurse days within 0..13; known shift names; at most one nurse per room-shift; no room listed twice for a nurse in a shift.

My checker's output (`python3 -I mycheck.py claim/i16.json <sol>`):

claim/published_sol_i16.json: STRUCTURAL issues: 0. 146 of 154 patients listed (8 absent, which counts as unscheduled), 146 scheduled.
All 9 hard constraints = 0, Total violations = 0.
RoomAgeMix 120 (1x120), RoomSkillLevel 370 (10x37), ContinuityOfCare 885, ExcessiveNurseWorkload 899, OpenOperatingTheater 1400 (40x35), SurgeonTransfer 30 (5x6), PatientDelay 2835 (15x189), ElectiveUnscheduledPatients 3600 (450x8).
**Total cost = 10139**, which equals the listed table value.

claim/sol_i16.json: STRUCTURAL issues: 0. 154 of 154 patients listed, 146 scheduled.
All 9 hard constraints = 0, Total violations = 0.
RoomAgeMix 104 (1x104), RoomSkillLevel 360 (10x36), ContinuityOfCare 892, ExcessiveNurseWorkload 808, OpenOperatingTheater 1400 (40x35), SurgeonTransfer 55 (5x11), PatientDelay 2835 (15x189), ElectiveUnscheduledPatients 3600 (450x8).
**Total cost = 10054**

## 2. Official validator (built in a copy of claim/ with `g++ -O2 -std=c++17 -o IHTP_Validator IHTP_Validator.cc`)
The build finished with no errors. I ran each file twice: exit code 0 both times, and the two outputs were byte-identical (`cmp`), so the result is deterministic.

./IHTP_Validator i16.json sol_i16.json:
```
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
RoomAgeMix...........................104 (  1 X 104)
RoomSkillLevel.......................360 ( 10 X  36)
ContinuityOfCare.....................892 (  1 X 892)
ExcessiveNurseWorkload...............808 (  1 X 808)
OpenOperatingTheater................1400 ( 40 X  35)
SurgeonTransfer.......................55 (  5 X  11)
PatientDelay........................2835 ( 15 X 189)
ElectiveUnscheduledPatients.........3600 (450 X   8)
Total cost = 10054
```
./IHTP_Validator i16.json published_sol_i16.json: Total violations = 0. Components are 120 / 370 / 885 / 899 / 1400 / 30 / 2835 / 3600. **Total cost = 10139**

Every component matches my checker exactly, for both files.

## 3. claim/SHA256SUMS
`shasum -a 256 -c SHA256SUMS`: all 8 files OK (CLAIM.md, IHTP_Validator.cc, REPRODUCE.md, i16.json, ihtp_table.html, json.hpp, published_sol_i16.json, sol_i16.json). The hashes for IHTP_Validator.cc (0b56fa75...) and json.hpp (9bea4c80...) match the ones stated in CLAIM.md. In claim/ihtp_table.html, the i16 row lists 10139.

## 4. Structural check of claim/sol_i16.json
No unknown or duplicate ids. Every day is within range. No room-shift has more than one nurse, and no room is repeated within a nurse's shift.

## Verdict
My checker and the official validator agree: 0 violations, Total cost = 10054. This is strictly below the listed 10139, and the published solution reproduces 10139 exactly. Not checked here (outside the REPRODUCE scope): a live re-fetch of the table and the literature NOVELTY check.
pass: true
