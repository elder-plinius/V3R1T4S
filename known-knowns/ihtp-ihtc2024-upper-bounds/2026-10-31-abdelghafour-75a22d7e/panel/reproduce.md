# REPRODUCE skeptic: m08 (claim/sol_m08.json)

context: subagent (Claude Code Agent tool, fresh context)

Scope: I read only the files in claim/. Everything ran on a scratch copy of claim/. My checker is saved next to this report as reproduce_mycheck.py.

## Claim under test
claim/CLAIM.md says claim/sol_m08.json has 0 hard violations and total cost 14877 under IHTP_Validator, which is strictly below the listed value of 14976 for m08.
claim/ihtp_table.html, row m08: `<td>m08</td> <td class="text-right">14976</td>`. This matches the claimed listed value.

## (3) SHA256SUMS
`shasum -a 256 -c SHA256SUMS`: CLAIM.md, IHTP_Validator.cc, REPRODUCE.md, ihtp_table.html, json.hpp, m08.json, published_sol_m08.json and sol_m08.json are all **OK** (8/8).
Limitation: this only shows the files match their own checksum list. I could not check the validator or table hash against upstream, because I was limited to claim/.

## (1) Independent checker (written from the definitions in claim/IHTP_Validator.cc)
These are the definitions I implemented, quoted or paraphrased from IHTP_Validator.cc:
- Hard constraints. The PrintCosts `violations` list has RoomGenderMix, PatientRoomCompatibility, SurgeonOvertime, OperatingTheaterOvertime, MandatoryUnscheduledPatients, AdmissionDay, RoomCapacity, NursePresence and UncoveredRoom.
  - RoomGenderMix: `cost += min(room_day_a_patients[r][d], room_day_b_patients[r][d])` (occupants are included).
  - AdmissionDay: `admission_day[p] < PatientSurgeryReleaseDay(p) || admission_day[p] > PatientLastPossibleDay(p)`, where LastPossibleDay is `mandatory ? surgery_due_day : days-1`.
  - RoomCapacity: `size() - RoomCapacity(r)` when the room is over capacity.
  - Overtime: `load - availability` for OTs and `load - max_surgery_time` for surgeons, per day.
  - UncoveredRoom: `room_shift_nurse[r][s] == -1 && room_day_patient_list[r][s/ShiftsPerDay()].size()>0`.
- Soft costs, weighted by `costs[i].second * in.Weight(i)`:
  - RoomAgeMix is max-min of the age-group index.
  - RoomSkillLevel is `SkillLevelRequired(p,s1) - NurseSkillLevel(n)` when positive, with `s1 = s - admission_day[p]*ShiftsPerDay()`.
  - ContinuityOfCare is the number of distinct nurses per person over the shifts of their stay that fall inside the horizon.
  - ExcessiveNurseWorkload is `load - NurseMaxLoad(n,s)`.
  - OpenOperatingTheater counts (t,d) with at least one surgery.
  - SurgeonTransfer is `count - 1` distinct theaters per surgeon-day.
  - PatientDelay is `admission_day - release_day`.
  - ElectiveUnscheduledPatients is a count of unscheduled elective patients.
  - Patient stays are clipped at the horizon: `min(in.Days(), ad + LOS)`.

My checker also runs structural checks:
- every patient, room, OT and nurse id must be known, with no duplicates;
- all 200 patients must appear in the solution;
- admission days must be integers in [0,28), and nurse days and shifts must be in range;
- each room-shift may have at most one nurse assignment.

Output of `python3 -I reproduce_mycheck.py m08.json published_sol_m08.json`:
```
structural issues: none
  (all 9 hard constraints = 0)
Total violations = 0
  RoomAgeMix                          11 (1 x 11)
  RoomSkillLevel                     435 (5 x 87)
  ContinuityOfCare                  4400 (5 x 880)
  ExcessiveNurseWorkload              20 (10 x 2)
  OpenOperatingTheater               490 (10 x 49)
  SurgeonTransfer                     30 (10 x 3)
  PatientDelay                      1340 (5 x 268)
  ElectiveUnscheduledPatients       8250 (250 x 33)
Total cost = 14976
```
This equals the listed table value of 14976.

Output of `python3 -I reproduce_mycheck.py m08.json sol_m08.json`:
```
structural issues: none
  (all 9 hard constraints = 0)
Total violations = 0
  RoomAgeMix                         117 (1 x 117)
  RoomSkillLevel                     445 (5 x 89)
  ContinuityOfCare                  4195 (5 x 839)
  ExcessiveNurseWorkload               0 (10 x 0)
  OpenOperatingTheater               500 (10 x 50)
  SurgeonTransfer                     30 (10 x 3)
  PatientDelay                      1340 (5 x 268)
  ElectiveUnscheduledPatients       8250 (250 x 33)
Total cost = 14877
```

Sanity check: I mutated sol_m08.json by removing one nurse room and shifting one admission by +1. My checker and the official validator gave the same result on the mutant: UncoveredRoom 1, Total violations 361, PatientDelay 5 x 269, Total cost 14917. So my checker is not just agreeing trivially.

## (2) Official validator
I ran `g++ -O2 -std=c++17 -o IHTP_Validator IHTP_Validator.cc` in the copy of claim/. The build succeeded. Here g++ is Apple clang 16.0.0.

`./IHTP_Validator m08.json published_sol_m08.json` gave identical output on both runs (cmp equal):
```
Total violations = 0   (all 9 lines = 0)
RoomAgeMix............................11 (  1 X  11)
RoomSkillLevel.......................435 (  5 X  87)
ContinuityOfCare....................4400 (  5 X 880)
ExcessiveNurseWorkload................20 ( 10 X   2)
OpenOperatingTheater.................490 ( 10 X  49)
SurgeonTransfer.......................30 ( 10 X   3)
PatientDelay........................1340 (  5 X 268)
ElectiveUnscheduledPatients.........8250 (250 X  33)
Total cost = 14976
```

`./IHTP_Validator m08.json sol_m08.json` gave identical output on both runs (cmp equal):
```
Total violations = 0   (all 9 lines = 0)
RoomAgeMix...........................117 (  1 X 117)
RoomSkillLevel.......................445 (  5 X  89)
ContinuityOfCare....................4195 (  5 X 839)
ExcessiveNurseWorkload.................0 ( 10 X   0)
OpenOperatingTheater.................500 ( 10 X  50)
SurgeonTransfer.......................30 ( 10 X   3)
PatientDelay........................1340 (  5 X 268)
ElectiveUnscheduledPatients.........8250 (250 X  33)
Total cost = 14877
```

## (4) Structure
Both solutions passed the structural checks:
- no duplicate or unknown patient or nurse ids, and all 200 patients are listed;
- days are in range, and all rooms and OTs are known;
- no room-shift has more than one nurse;
- no nurse is assigned outside their working shifts (NursePresence = 0, and the validator did not throw on a non-working assignment).

## Verdict
My checker and the official validator agree on every component for both files.
- sol_m08.json: 0 violations and total cost 14877. This is exactly the claimed value and is strictly below the listed 14976.
- published_sol_m08.json: reproduces the listed value of 14976.
- Results were deterministic over 2 runs each, and SHA256SUMS is 8/8 OK.

Out of scope for this role: the live re-fetch of the table and the novelty or literature check.

pass: true
