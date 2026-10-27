# Panel Audit — REPRODUCE Skeptic (`ihtp-ihtc2024-hidden-m-instances-upper-bounds` / `m09`)

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
Before inspecting author tooling, `object/sol_m09_32675.json` was independently evaluated by both verification engines:
1. **Official C++ `IHTP_Validator.cc` Specification**:
   - Executed on the official instance `m09.json` and `object/sol_m09_32675.json`.
   - Reports `Total violations = 0` across all 9 hard constraint categories.
   - Exact soft-cost breakdown: `RoomAgeMix 34, RoomSkillLevel 170, ContinuityOfCare 1198, ExcessiveNurseWorkload 968, OpenOperatingTheater 1170, SurgeonTransfer 10, PatientDelay 13125, ElectiveUnscheduledPatients 16000`.
   - Total cost = `32675`.
2. **Standalone Python Port (`verify-it-yourself/check_ihtp.py`)**:
   - Executed independently with zero external dependencies.
   - Yields bit-for-bit identical results: `Total violations = 0`, `Total cost = 32675`.
3. **Integrity and Bounds Check**:
   - File SHA-256 matches `INDEX.csv`: `c200f4f9c61b8a4cb84b637a9995ec0fe40dc3dd23f95798a763fa2702572ae4`.
   - Objective cost `32675` strictly beats the current live BKS `32967` (margin `-292`).

pass: true
