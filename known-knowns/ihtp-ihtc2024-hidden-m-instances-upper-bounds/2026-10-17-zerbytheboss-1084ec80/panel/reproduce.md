# Panel Audit — REPRODUCE Skeptic (`ihtp-ihtc2024-hidden-m-instances-upper-bounds` / `m26`)

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

## 2. Independent Verification Against Official `IHTP_Validator` and `INDEX.csv`
Before inspecting `verify-it-yourself/` or `how-we-built-it/`, `object/sol_m26_68496.json` was verified directly against `INDEX.csv` and both the official C++ `IHTP_Validator` compiled from the IHTC-2024 specification and its standalone Python port (`verify-it-yourself/check_ihtp.py`):
1. **File Integrity (`INDEX.csv`)**: Verified `object/sol_m26_68496.json` has SHA-256 `1084ec80f011bba03680556ecb38881cda80ea415228860a3757359fb4709e9a`, matching `INDEX.csv` (`target_id = ihtp-ihtc2024-hidden-m-instances-upper-bounds`, `cell = m26`, `value = 68496`, `table_value = 69730`).
2. **Official C++ `IHTP_Validator` Output**:
   - `RoomGenderMix = 0`, `PatientRoomCompatibility = 0`, `SurgeonOvertime = 0`, `OperatingTheaterOvertime = 0`, `MandatoryUnscheduledPatients = 0`, `AdmissionDay = 0`, `RoomCapacity = 0`, `NursePresence = 0`, `UncoveredRoom = 0` : **`Total violations = 0`**.
   - Soft cost breakdown:
     - `RoomAgeMix = 72` (`1 X 72`)
     - `RoomSkillLevel = 2470` (`10 X 247`)
     - `ContinuityOfCare = 2974` (`1 X 2974`)
     - `ExcessiveNurseWorkload = 130` (`10 X 13`)
     - `OpenOperatingTheater = 2580` (`30 X 86`)
     - `SurgeonTransfer = 200` (`10 X 20`)
     - `PatientDelay = 12370` (`10 X 1237`)
     - `ElectiveUnscheduledPatients = 47700` (`450 X 106`)
     - **`Total cost = 68496`** (strictly improving the published BKS of `69730` by `-1234`).

## 3. Verification of Package Check Script
Executed `sh verify-it-yourself/run_checks.sh` from the package root:
- Output: `VERIFIED: instance=m26 total_violations=0 total_cost=68496 bks=69730 delta=-1234` with identical component breakdown, followed by `PASS` (exit code `0`).
- Determinism confirmed across repeated runs.

pass: true
