# REPRODUCE skeptic report: IHTC-2024 i08, claimed cost 6225 (listed 6243)

context: subagent (Claude Code Agent tool, fresh context)

Files read: only those in claim/ (CLAIM.md, REPRODUCE.md, SHA256SUMS, IHTP_Validator.cc, i08.json,
published_sol_i08.json, sol_i08.json, ihtp_table.html). No author code exists in claim/; none was read.

## 1. Independent checker (own Python, written from the definitions in claim/IHTP_Validator.cc)
Definitions used (quoted / paraphrased from IHTP_Validator.cc):
- Hard list in `PrintCosts`: "RoomGenderMix", "PatientRoomCompatibility", "SurgeonOvertime", "OperatingTheaterOvertime",
  "MandatoryUnscheduledPatients", "AdmissionDay", "RoomCapacity", "NursePresence", "UncoveredRoom".
- RoomGenderMix: `cost += min(room_day_a_patients[r][d], room_day_b_patients[r][d]);` (occupants included).
- AdmissionDay: `admission_day[p] < in.PatientSurgeryReleaseDay(p) || (admission_day[p] > in.PatientLastPossibleDay(p))`,
  with `PatientLastPossibleDay = PatientMandatory(p) ? surgery_due_day : days-1`.
- UncoveredRoom: `room_shift_nurse[r][s] == -1 && room_day_patient_list[r][s/in.ShiftsPerDay()].size()>0`.
- Soft list with weights `weights[0..7] = room_mixed_age, room_nurse_skill, continuity_of_care, nurse_eccessive_workload,
  open_operating_theater, surgeon_transfer, patient_delay, unscheduled_optional`, `total_cost += costs[i].second * in.Weight(i)`.
- RoomAgeMix: per room-day `cost += max - min` of age-group index; RoomSkillLevel: `PatientSkillLevelRequired(p,s1) - NurseSkillLevel(n)`
  with `s1 = s - admission_day[p] * ShiftsPerDay` (occupants use absolute s); ContinuityOfCare: distinct nurses per patient/occupant
  over in-horizon stay; ExcessiveNurseWorkload: `load - NurseMaxLoad(n,s)` over the nurse's working shifts;
  OpenOperatingTheater: (t,d) with >=1 patient; SurgeonTransfer: `count - 1` distinct theaters per surgeon-day;
  PatientDelay: `admission_day[p] - SurgeryReleaseDay(p)`; ElectiveUnscheduledPatients: count of unscheduled non-mandatory.
- Stays truncated at horizon: `d < min(in.Days(), ad + in.PatientLengthOfStay(p))`.

Own checker output (python3 -I mycheck.py i08.json <sol>):

| component | published_sol_i08.json | sol_i08.json |
|---|---|---|
| all 9 hard components | 0 each | 0 each |
| Total violations | 0 | 0 |
| RoomAgeMix | 105 (5 x 21) | 115 (5 x 23) |
| RoomSkillLevel | 0 (10 x 0) | 0 (10 x 0) |
| ContinuityOfCare | 1152 (1 x 1152) | 1144 (1 x 1144) |
| ExcessiveNurseWorkload | 616 (1 x 616) | 646 (1 x 646) |
| OpenOperatingTheater | 1600 (40 x 40) | 1600 (40 x 40) |
| SurgeonTransfer | 70 (10 x 7) | 90 (10 x 9) |
| PatientDelay | 2300 (10 x 230) | 2430 (10 x 243) |
| ElectiveUnscheduledPatients | 400 (200 x 2) | 200 (200 x 1) |
| **Total cost** | **6243** | **6225** |

published_sol_i08.json gives 6243 = listed table value (claim/ihtp_table.html row: `<td>i08</td> <td class="text-right">6243</td>`).

## 2. Official validator (copy of claim/, `g++ -O2 -std=c++17 -o IHTP_Validator IHTP_Validator.cc`, compiled clean)
- `./IHTP_Validator i08.json sol_i08.json`: all 9 violation lines 0, `Total violations = 0`, components identical to the table above,
  `Total cost = 6225`.
- `./IHTP_Validator i08.json published_sol_i08.json`: `Total violations = 0`, `Total cost = 6243`.
- Determinism: two runs each, identical output hashes (sol 9a3ba7bb...c0c8, published 842cf21c...843b); own checker also identical across runs.
- Per-component agreement between own checker and official validator: exact on all 17 components for both files.

## 3. SHA256SUMS
`shasum -a 256 -c SHA256SUMS`: all 8 entries OK (CLAIM.md, IHTP_Validator.cc, REPRODUCE.md, i08.json, ihtp_table.html,
json.hpp, published_sol_i08.json, sol_i08.json). Validator sha 0b56fa75...a8afa matches the hash quoted in CLAIM.md.

## 4. Structural checks (own checker)
STRUCTURE: OK for both files. Checked: patient ids unique, all known, set equals the instance's 174 patients;
nurse ids unique and known; admission days integers in [0,27]; rooms and theaters known; no nurse repeats a shift;
no duplicate rooms within an assignment; at most one nurse per room-shift (no overwrite of `room_shift_nurse`).
sol_i08.json has 1 unscheduled (elective) patient, consistent with ElectiveUnscheduledPatients = 1.

## Verdict
Own checker and official validator both give 0 violations and exactly 6225 for sol_i08.json (6225 < 6243 listed),
and reproduce the listed 6243 for published_sol_i08.json. Scope: this verifies the claimed value and feasibility only;
the live re-fetch of the table and the NOVELTY check of the literature are outside this role.

pass: true
