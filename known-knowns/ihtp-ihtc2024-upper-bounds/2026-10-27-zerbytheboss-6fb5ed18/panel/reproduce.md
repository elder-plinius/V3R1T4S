# Panel Audit — REPRODUCE Skeptic (`ihtp-ihtc2024-upper-bounds` / `i23`)

context: subagent (fresh invocation)

## 1. Mathematical Definition Quoted Before Inspecting Author Code
In the Integrated Healthcare Timetabling Competition 2024 (IHTC-2024) formulation (Ceschia et al., 2024), a schedule assigns each mandatory and scheduled elective patient an admission day, room, and operating theater, and assigns each working nurse-shift a subset of rooms over the planning horizon $D$. A schedule is feasible if and only if all 9 hard constraint categories equal zero:
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
Before inspecting author tooling, `object/sol_i23_37231.json` was independently evaluated by both verification engines:
1. **Official C++ `IHTP_Validator.cc` Specification**:
   - Executed on the official instance `i23.json` and `object/sol_i23_37231.json`.
   - Reports `Total violations = 0` across all 9 hard constraint categories.
   - Exact soft-cost breakdown: `RoomAgeMix 150, RoomSkillLevel 50, ContinuityOfCare 7675, ExcessiveNurseWorkload 883, OpenOperatingTheater 650, SurgeonTransfer 18, PatientDelay 6405, ElectiveUnscheduledPatients 21400`.
   - Total cost = `37231`.
2. **Standalone Python Port (`verify-it-yourself/check_ihtp.py`)**:
   - Executed independently with zero external dependencies.
   - Yields bit-for-bit identical results: `Total violations = 0`, `Total cost = 37231`.
3. **Integrity and Bounds Check**:
   - File SHA-256 matches `INDEX.csv`: `6fb5ed18e0ef8878449e688e6d14e8b1b8c60e9fe1e6cf12c225adb73022b7d1`.
   - Objective cost `37231` strictly beats the current live BKS `37542` (margin `-311`).

pass: true
