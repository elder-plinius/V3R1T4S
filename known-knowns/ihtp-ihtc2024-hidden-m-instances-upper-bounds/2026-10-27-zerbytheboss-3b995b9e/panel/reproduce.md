# Panel Audit — REPRODUCE Skeptic (`ihtp-ihtc2024-hidden-m-instances-upper-bounds` / `m28`)

- Context: Independent reproduction verification from `object/sol_m28_45037.json` and the official `m28.json` instance using both the organisers' compiled C++ `IHTP_Validator` and `verify-it-yourself/check_ihtp.py`

## 1. Mathematical Definition Quoted Before Inspecting Author Code
In the Integrated Healthcare Timetabling Competition 2024 (IHTC-2024) formulation (Sara Ceschia, Roberto Maria Rosati, Andrea Schaerf, and Eugenia Zanazzo with Pieter Smet and Greet Vanden Berghe), a schedule assigns each mandatory and scheduled elective patient an admission day, room, and operating theater, and assigns each working nurse-shift a subset of rooms over the planning horizon $D$. A schedule is feasible if and only if all 9 hard constraint categories equal zero:
- H1 (`RoomGenderMix`): no room on any day contains patients of different genders.
- H2 (`PatientRoomCompatibility`): no patient is assigned to an incompatible room.
- H3 (`SurgeonOvertime`): no surgeon exceeds maximum daily surgery time on any day.
- H4 (`OperatingTheaterOvertime`): no operating theater exceeds daily capacity on any day.
- H5 (`MandatoryUnscheduledPatients`): all mandatory patients are scheduled.
- H6 (`AdmissionDay`): every scheduled patient is admitted between `surgery_release_day` and `surgery_due_day` (for mandatory patients) or `D - 1` (for elective patients).
- H7 (`RoomCapacity`): room occupancy on any day does not exceed room capacity.
- H8 (`NursePresence`): every assigned room belongs to the rooms list of the instance and every nurse assignment matches an existing working shift.
- H9 (`UncoveredRoom`): every occupied room on every shift of every day is covered by a working nurse.

The total objective is the weighted sum of the 8 soft constraint penalties:
$$\text{Total cost} = \text{RoomAgeMix} + \text{RoomSkillLevel} + \text{ContinuityOfCare} + \text{ExcessiveNurseWorkload} + \text{OpenOperatingTheater} + \text{SurgeonTransfer} + \text{PatientDelay} + \text{ElectiveUnscheduledPatients}.$$

## 2. Independent Verification Against Official C++ Validator and Python Standalone Port
`object/sol_m28_45037.json` was evaluated by both the organisers' compiled C++ validator and our standalone Python port:
1. **Official C++ `IHTP_Validator.cc` (`https://ihtc2024.github.io/assets/files/IHTP_Validator.cc`)**:
   - Compiled with `g++ -O3 -std=c++17 IHTP_Validator.cc -o IHTP_Validator` and executed directly on `m28.json` and `object/sol_m28_45037.json`:
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
2. **Standalone Python Port (`verify-it-yourself/check_ihtp.py`)**:
   - Executed via `sh verify-it-yourself/run_checks.sh` (which runs `verify-it-yourself/check_ihtp.py` with Python 3 standard library only).
   - Yields identical results: `Total violations = 0`, `Total cost = 45037`.
3. **Integrity and Bounds Check**:
   - File SHA-256 matches `INDEX.csv`: `3b995b9e0d524a8a887bbda0d7f20efc5e67128d85a15baadae307078a4e9395`.
   - Objective cost `45037` strictly beats the live table bound `45873` (`sol_m28.json`, margin `-836`).

pass: true
