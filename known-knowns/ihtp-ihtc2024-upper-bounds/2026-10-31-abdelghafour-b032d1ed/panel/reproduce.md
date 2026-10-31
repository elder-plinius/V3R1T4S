# REPRODUCE skeptic report: i20 (claim: 0 violations, cost 28812 < listed 29042)

context: subagent (Claude Code Agent tool, fresh context)

Scope: only the claim/ folder was read. All files were treated as data. Work was done in a scratch copy of claim/.

## 1. Independent checker (my own, written from the definitions in claim/IHTP_Validator.cc)

Definitions used, quoted from claim/IHTP_Validator.cc:
- Hard constraints (summed into "Total violations"): `{"RoomGenderMix", ...}, {"PatientRoomCompatibility", ...}, {"SurgeonOvertime", ...}, {"OperatingTheaterOvertime", ...}, {"MandatoryUnscheduledPatients", ...}, {"AdmissionDay", ...}, {"RoomCapacity", ...}, {"NursePresence", ...}, {"UncoveredRoom", ...}`
- Gender mix: `cost += min(room_day_a_patients[r][d], room_day_b_patients[r][d]);`
- Admission day: `admission_day[p] < in.PatientSurgeryReleaseDay(p) || (admission_day[p] > in.PatientLastPossibleDay(p))`, with `PatientLastPossibleDay(p) ... PatientMandatory(p) ? surgery_due_day : days-1`
- Stay truncated at the horizon: `for (d = ad; d < min(in.Days(), ad + in.PatientLengthOfStay(p)); d++)`; occupants are present on days 0..length_of_stay-1 in their fixed room.
- Uncovered room: `room_shift_nurse[r][s] == -1 && room_day_patient_list[r][s/in.ShiftsPerDay()].size()>0`
- Age mix: max age-group index minus min, per non-empty room-day.
- Skill: `PatientSkillLevelRequired(p,s1) - NurseSkillLevel(n)` when positive, with `s1 = s - admission_day[p] * in.ShiftsPerDay()`. For occupants the absolute shift is used.
- Continuity of care: the number of distinct nurses per occupant, plus per scheduled patient, over in-horizon shifts.
- Excessive workload: for each nurse working shift, `load > in.NurseMaxLoad(n,s)`. Load is the sum of `workload_produced` over the patients in the nurse's rooms.
- Open OT: count of (theater, day) pairs with at least one surgery. Surgeon transfer: `cost += (count - 1)` for distinct theaters per surgeon-day.
- Delay: `admission_day[p] - PatientSurgeryReleaseDay(p)`. Elective unscheduled: count. Weights are read from the instance `weights` in the order room_mixed_age, room_nurse_skill, continuity_of_care, nurse_eccessive_workload, open_operating_theater, surgeon_transfer, patient_delay, unscheduled_optional.

Output on claim/published_sol_i20.json:
```
H RoomGenderMix 0 | PatientRoomCompatibility 0 | SurgeonOvertime 0 | OperatingTheaterOvertime 0
H MandatoryUnscheduledPatients 0 | AdmissionDay 0 | RoomCapacity 0 | NursePresence 0 | UncoveredRoom 0
Total violations = 0
C RoomAgeMix 80 (1 x 80); RoomSkillLevel 2040 (10 x 204); ContinuityOfCare 965 (1 x 965)
C ExcessiveNurseWorkload 560 (10 x 56); OpenOperatingTheater 1400 (40 x 35); SurgeonTransfer 17 (1 x 17)
C PatientDelay 3480 (15 x 232); ElectiveUnscheduledPatients 20500 (500 x 41)
Total cost = 29042
structural issues: 0 [] | patients absent from solution file: 0 ; scheduled 147 of 188
```
This matches the table value 29042 for i20 in claim/ihtp_table.html (`<td>i20</td> <td class="text-right">29042</td>`).

Output on claim/sol_i20.json:
```
H all nine hard constraints = 0
Total violations = 0
C RoomAgeMix 79 (1 x 79); RoomSkillLevel 1890 (10 x 189); ContinuityOfCare 981 (1 x 981)
C ExcessiveNurseWorkload 460 (10 x 46); OpenOperatingTheater 1400 (40 x 35); SurgeonTransfer 22 (1 x 22)
C PatientDelay 3480 (15 x 232); ElectiveUnscheduledPatients 20500 (500 x 41)
Total cost = 28812
structural issues: 0 [] | patients absent from solution file: 0 ; scheduled 147 of 188
```

## 2. Official validator (claim/IHTP_Validator.cc, built in a copy of claim/)
`g++ -O2 -std=c++17 -o IHTP_Validator IHTP_Validator.cc` built cleanly. Here `g++` is Apple clang version 16.0.0 (clang-1600.0.26.6).

`./IHTP_Validator i20.json published_sol_i20.json`: every violation line is 0, `Total violations = 0`, then RoomAgeMix 80, RoomSkillLevel 2040 (10 X 204), ContinuityOfCare 965, ExcessiveNurseWorkload 560 (10 X 56), OpenOperatingTheater 1400 (40 X 35), SurgeonTransfer 17, PatientDelay 3480 (15 X 232), ElectiveUnscheduledPatients 20500 (500 X 41), `Total cost = 29042`, exit 0.

`./IHTP_Validator i20.json sol_i20.json`: every violation line is 0, `Total violations = 0`, then RoomAgeMix 79, RoomSkillLevel 1890 (10 X 189), ContinuityOfCare 981, ExcessiveNurseWorkload 460 (10 X 46), OpenOperatingTheater 1400 (40 X 35), SurgeonTransfer 22, PatientDelay 3480 (15 X 232), ElectiveUnscheduledPatients 20500 (500 X 41), `Total cost = 28812`, exit 0.

Every component matches my checker exactly, for both files.

Determinism: two repeated runs gave identical output hashes. Validator on sol_i20.json: 237ccf2a…af25 both times. Validator on published_sol_i20.json: 31be6479…4822 both times. My checker on sol_i20.json: b5d6f4cf…a630 both times.

## 3. claim/SHA256SUMS
`shasum -a 256 -c SHA256SUMS` reports OK for CLAIM.md, IHTP_Validator.cc, REPRODUCE.md, i20.json, ihtp_table.html, json.hpp, published_sol_i20.json and sol_i20.json.

The validator hash 0b56fa75…a8afa and the json.hpp hash 9bea4c80…3ea6 match the values stated in CLAIM.md. This panel did not fetch anything, so it did not check these files against upstream.

## 4. Structural checks on claim/sol_i20.json (my checker)
- No duplicate or unknown patient ids. All 188 patients are listed: 147 are scheduled and 41 are "none", all of them elective.
- Every admission day is an integer in [0, 13]. All rooms and operating theaters are known ids.
- No unknown or duplicate nurse ids, and no duplicate (day, shift) entries for a nurse.
- No duplicate room within an assignment.
- Every nurse assignment falls in one of that nurse's working shifts.
- At most one nurse per room-shift. This matters because the official validator would silently overwrite a second nurse on the same room-shift; none occurs here.
- Result: 0 structural issues. claim/published_sol_i20.json also has 0 structural issues.

## Not verified here
- I did not re-fetch the live table. The value used is the saved claim/ihtp_table.html (29042), which matches its recorded sha256.
- I did not check the NOVELTY part of the success criterion (other published values).

## Verdict
My checker and the official validator agree: 0 violations, total cost 28812 for claim/sol_i20.json. That is strictly below the listed 29042, which both tools also reproduce for claim/published_sol_i20.json.
pass: true
