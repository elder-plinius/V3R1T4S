# REPRODUCE skeptic verdict: m19 (IHTC-2024)

context: subagent (Claude Code Agent tool, fresh context)

Scope: read only claim/ (CLAIM.md, REPRODUCE.md, IHTP_Validator.cc, SHA256SUMS, ihtp_table.html, m19.json, both solution files). Worked in a scratch copy of claim/.

## Claim under test
claim/sol_m19.json: 0 hard violations, total cost 21752 under the official IHTP_Validator, strictly below the 21776 listed for m19 (claim/ihtp_table.html).

## 1. SHA256SUMS (claim/SHA256SUMS, `shasum -a 256 -c`)
```
CLAIM.md: OK
IHTP_Validator.cc: OK
REPRODUCE.md: OK
ihtp_table.html: OK
json.hpp: OK
m19.json: OK
published_sol_m19.json: OK
sol_m19.json: OK
```
IHTP_Validator.cc sha256 0b56fa75...a8afa matches the hash stated in CLAIM.md. ihtp_table.html row: `<td>m19</td> <td class="text-right">21776</td>`, so the listed value is 21776.

## 2. Independent checker (written from the definitions in claim/IHTP_Validator.cc)
I wrote it before reading any author code. No author code ships in claim/ apart from the solution files. Definitions used, quoted or paraphrased from IHTP_Validator.cc:
- Hard constraints, `PrintCosts` violations list: RoomGenderMix `cost += min(room_day_a_patients[r][d], room_day_b_patients[r][d])`; PatientRoomCompatibility `room[p] != -1 && in.IncompatibleRoom(p,room[p])`; SurgeonOvertime `surgeon_day_load[s][d] - in.SurgeonMaxSurgeryTime(s,d)`; OperatingTheaterOvertime `time - in.OperatingTheaterAvailability(t,d)`; MandatoryUnscheduledPatients `admission_day[p] == -1 && in.PatientMandatory(p)`; AdmissionDay `admission_day[p] < in.PatientSurgeryReleaseDay(p) || admission_day[p] > in.PatientLastPossibleDay(p)`, with `PatientLastPossibleDay = PatientMandatory(p) ? surgery_due_day : days-1`; RoomCapacity `size() - in.RoomCapacity(r)`; NursePresence `n != -1 && !in.IsNurseWorkingInShift(n,s)`; UncoveredRoom `room_shift_nurse[r][s] == -1 && room_day_patient_list[r][s/ShiftsPerDay].size()>0`.
- Soft costs, with weights in the order `weights[0..7] = room_mixed_age, room_nurse_skill, continuity_of_care, nurse_eccessive_workload, open_operating_theater, surgeon_transfer, patient_delay, unscheduled_optional`: RoomAgeMix `cost += max - min` age group per room-day; RoomSkillLevel `PatientSkillLevelRequired(p,s1) - NurseSkillLevel(n)` with `s1 = s - admission_day[p]*ShiftsPerDay` (occupants use absolute s); ContinuityOfCare is the number of distinct nurses per patient/occupant over its stay within the horizon; ExcessiveNurseWorkload `load - in.NurseMaxLoad(n,s)` over each nurse's working shifts; OpenOperatingTheater counts (t,d) with at least one patient; SurgeonTransfer `count - 1` distinct theatres per surgeon-day; PatientDelay `admission_day[p] - PatientSurgeryReleaseDay(p)`; ElectiveUnscheduledPatients counts unscheduled non-mandatory patients.
- Stays are truncated at the horizon (`d < min(Days, ad + LOS)`). Occupants count from day 0.

Structural checks in the same script: no duplicate or unknown patient ids, no duplicate or unknown nurse ids, admission days are integers in [0,14), rooms and OTs are known ids, each nurse-shift is listed once and is one of that nurse's working shifts, and **at most one nurse per (room, day, shift)**. The last check matters because the official validator silently overwrites `room_shift_nurse[r][s] = n`.

Output on claim/published_sol_m19.json:
```
structural issues: 0 []
Total violations = 0
  RoomAgeMix                         260 (5 X 52)
  RoomSkillLevel                     216 (1 X 216)
  ContinuityOfCare                  1003 (1 X 1003)
  ExcessiveNurseWorkload             177 (1 X 177)
  OpenOperatingTheater              1320 (30 X 44)
  SurgeonTransfer                     60 (10 X 6)
  PatientDelay                      7490 (10 X 749)
  ElectiveUnscheduledPatients      11250 (450 X 25)
Total cost = 21776
scheduled 188/213 patients, solution lists 213 patients, 38 nurses
```
This is 21776, the table value, so the checker is calibrated against the listed value.

Output on claim/sol_m19.json:
```
structural issues: 0 []
  (all 9 hard-constraint lines = 0)
Total violations = 0
  RoomAgeMix                         260 (5 X 52)
  RoomSkillLevel                     177 (1 X 177)
  ContinuityOfCare                   979 (1 X 979)
  ExcessiveNurseWorkload             176 (1 X 176)
  OpenOperatingTheater              1350 (30 X 45)
  SurgeonTransfer                     70 (10 X 7)
  PatientDelay                      7490 (10 X 749)
  ElectiveUnscheduledPatients      11250 (450 X 25)
Total cost = 21752
scheduled 188/213 patients, solution lists 213 patients, 38 nurses
```
Arithmetic check: 260+177+979+176+1350+70+7490+11250 = 21752.

## 3. Official validator (per claim/REPRODUCE.md, in a copy of claim/)
`g++ -O2 -std=c++17 -o IHTP_Validator IHTP_Validator.cc` compiled cleanly (rc=0).

`./IHTP_Validator m19.json published_sol_m19.json` gave all 9 hard-constraint lines = 0 and `Total violations = 0`. Costs per term: 260, 216, 1003, 177, 1320, 60, 7490, 11250. `Total cost = 21776` (rc=0).

`./IHTP_Validator m19.json sol_m19.json`:
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
RoomAgeMix...........................260 (  5 X  52)
RoomSkillLevel.......................177 (  1 X 177)
ContinuityOfCare.....................979 (  1 X 979)
ExcessiveNurseWorkload...............176 (  1 X 176)
OpenOperatingTheater................1350 ( 30 X  45)
SurgeonTransfer.......................70 ( 10 X   7)
PatientDelay........................7490 ( 10 X 749)
ElectiveUnscheduledPatients........11250 (450 X  25)
Total cost = 21752
```
Every term matches my checker exactly, for both files.

## 4. Determinism
Running the validator and my checker 3 times each on sol_m19.json gave identical output hashes every time (3x 293a6691..., 3x 7d3db261...).

## Verdict
Both independent checks give 0 violations and 21752 for claim/sol_m19.json. 21752 < 21776 (the listed m19 value), so the solution is 24 cheaper. The published solution reproduces 21776. Hashes match and the structural checks are clean. The claim reproduces.

Out of scope for this panel seat (not verified here): whether the live table still lists 21776 (I used only the saved claim/ihtp_table.html, fetched 2026-10-31T00:02:47Z) and the literature NOVELTY check in the success criterion.

pass: true
