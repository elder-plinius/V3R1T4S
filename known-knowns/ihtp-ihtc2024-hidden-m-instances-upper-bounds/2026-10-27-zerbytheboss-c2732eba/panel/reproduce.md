# Panel Audit — REPRODUCE Skeptic (`ihtp-ihtc2024-hidden-m-instances-upper-bounds` / `m30`)

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
Before inspecting author tooling, `object/sol_m30_31102.json` was independently evaluated by both verification engines:
1. **Official C++ `IHTP_Validator.cc` Specification**:
   - Compiled from upstream source with clang++ and executed on the official instance `m30.json` and `object/sol_m30_31102.json`.
   - Reports `Total violations = 0` across all 9 hard constraint categories.
   - Exact soft-cost breakdown: `RoomAgeMix 130, RoomSkillLevel 320, ContinuityOfCare 2830, ExcessiveNurseWorkload 1252, OpenOperatingTheater 6000, SurgeonTransfer 350, PatientDelay 11420, ElectiveUnscheduledPatients 8800`.
   - Total cost = `31102`.
2. **Standalone Python Port (`verify-it-yourself/check_ihtp.py`)**:
   - Executed independently with zero external dependencies.
   - Yields bit-for-bit identical results: `Total violations = 0`, `Total cost = 31102`.
3. **Integrity and Bounds Check**:
   - File SHA-256 matches `INDEX.csv`: `c2732eba40078864ed09070ebc758aef2c5542a0d70c015244a54f81509bfa53`.
   - Objective cost `31102` strictly beats the published table bound `31649` (margin `-547`) and current live BKS `31641` (margin `-539`).

pass: true
