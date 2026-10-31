# REPRODUCE skeptic: IHTC-2024 i18, claimed cost 37625

context: subagent (Claude Code Agent tool, fresh context)

Scope: only the files in claim/. Every file was treated as data. I did not re-fetch the live table and did not run the novelty or literature check; that is outside this role.

## 1. Integrity (claim/SHA256SUMS)
`shasum -a 256 -c SHA256SUMS` printed OK for all 8 entries: CLAIM.md, IHTP_Validator.cc, REPRODUCE.md, i18.json, ihtp_table.html, json.hpp, published_sol_i18.json, sol_i18.json.
The IHTP_Validator.cc hash (0b56fa75...afa) and the ihtp_table.html hash (2b69fe2e...363) match the values stated in CLAIM.md.
The i18 row in claim/ihtp_table.html reads `<td>i18</td> <td class="text-right">37650</td>`.

## 2. My own checker, written from the definitions in claim/IHTP_Validator.cc
I wrote the checker myself in Python, without using the validator's data structures. The definitions I used, quoted from IHTP_Validator.cc:
- Gender mix: `cost += min(room_day_a_patients[r][d], room_day_b_patients[r][d]);`
- Capacity: `room_day_patient_list[r][d].size() > in.RoomCapacity(r)` adds the excess.
- Admission window: `admission_day[p] < in.PatientSurgeryReleaseDay(p) || admission_day[p] > in.PatientLastPossibleDay(p)`, with `PatientLastPossibleDay = PatientMandatory(p) ? surgery_due_day : days-1`.
- Theater overtime and surgeon overtime: the excess of the summed surgery_duration over `availability[d]` or `max_surgery_time[d]`.
- Uncovered room: `room_shift_nurse[r][s] == -1 && room_day_patient_list[r][s/ShiftsPerDay].size()>0`.
- Nurse presence: a nurse assigned in a shift that is not in working_shifts. The validator also throws an error for this when it reads the solution.
- Age mix: `cost += max - min` of age-group indices per room-day.
- Skill level: `PatientSkillLevelRequired(p,s1) > NurseSkillLevel(n)` adds the difference. `s1 = s - admission_day[p]*ShiftsPerDay`, and occupants use the absolute shift.
- Continuity of care: the number of distinct nurses per occupant and per scheduled patient, counted within the horizon.
- Excessive workload: over each nurse's working shifts, the excess of the summed workload_produced of the patients in the nurse's rooms over max_load.
- Open theater: the count of (t,d) pairs with at least one surgery.
- Surgeon transfer: `count-1` per surgeon-day, where count is the number of distinct theaters used.
- Patient delay: `admission_day - surgery_release_day` when the admission is later than the release day.
- Unscheduled elective: the count of elective patients with no admission.
- Weights, in the order the validator reads them: room_mixed_age, room_nurse_skill, continuity_of_care, nurse_eccessive_workload, open_operating_theater, surgeon_transfer, patient_delay, unscheduled_optional.

Output of my checker:

claim/published_sol_i18.json:
```
structural issues: none
Total violations = 0   (all 9 hard terms 0)
  RoomAgeMix 5 (5x1)  RoomSkillLevel 148 (1x148)  ContinuityOfCare 795 (1x795)
  ExcessiveNurseWorkload 0 (10x0)  OpenOperatingTheater 750 (30x25)  SurgeonTransfer 2 (1x2)
  PatientDelay 2650 (10x265)  ElectiveUnscheduledPatients 33300 (300x111)
Total cost = 37650   scheduled patients: 146 of 257
```
claim/sol_i18.json:
```
structural issues: none
Total violations = 0   (all 9 hard terms 0)
  RoomAgeMix 5 (5x1)  RoomSkillLevel 121 (1x121)  ContinuityOfCare 792 (1x792)
  ExcessiveNurseWorkload 0 (10x0)  OpenOperatingTheater 750 (30x25)  SurgeonTransfer 7 (1x7)
  PatientDelay 2650 (10x265)  ElectiveUnscheduledPatients 33300 (300x111)
Total cost = 37625   scheduled patients: 146 of 257
```
The published solution gives exactly the listed table value, 37650.

Recomputing the difference: skill level -27, continuity -3 and surgeon transfer +5 sum to -25, and 37650 - 25 = 37625. All other terms are unchanged.

## 3. Structural checks (done inside my checker)
Both files passed every structural check:
- Patient ids: no duplicates, none unknown, and all 257 present.
- Admission days are integers in [0, 21).
- Every room and theater id exists.
- Nurse ids: no duplicates and none unknown.
- No nurse is assigned to a non-working shift.
- No nurse lists the same shift twice or the same room twice within a shift.
- At most one nurse covers each room-shift: zero room-shifts have more than one nurse.

## 4. Official validator (compiled in a copy of claim/)
`g++ -O2 -std=c++17 -o IHTP_Validator IHTP_Validator.cc` built with exit code 0 and no output.

`./IHTP_Validator i18.json sol_i18.json`:
```
RoomGenderMix 0, PatientRoomCompatibility 0, SurgeonOvertime 0, OperatingTheaterOvertime 0,
MandatoryUnscheduledPatients 0, AdmissionDay 0, RoomCapacity 0, NursePresence 0, UncoveredRoom 0
Total violations = 0
RoomAgeMix 5 (5 X 1)  RoomSkillLevel 121 (1 X 121)  ContinuityOfCare 792 (1 X 792)
ExcessiveNurseWorkload 0 (10 X 0)  OpenOperatingTheater 750 (30 X 25)  SurgeonTransfer 7 (1 X 7)
PatientDelay 2650 (10 X 265)  ElectiveUnscheduledPatients 33300 (300 X 111)
Total cost = 37625
```
`./IHTP_Validator i18.json published_sol_i18.json` reported Total violations = 0 and Total cost = 37650. Its breakdown is the same as my checker's.

Determinism: I ran each file a second time and compared the output byte for byte with `cmp`. Both reruns were identical.

## Verdict
My checker and the official validator agree on every term for both files. sol_i18.json has 0 violations and cost exactly 37625. That is strictly below the 37650 for i18 in the saved claim/ihtp_table.html, and the published solution reproduces 37650. I found no mismatches, no missing objects and no non-determinism. The live re-fetch of the table and the novelty check were not part of this check.

pass: true
