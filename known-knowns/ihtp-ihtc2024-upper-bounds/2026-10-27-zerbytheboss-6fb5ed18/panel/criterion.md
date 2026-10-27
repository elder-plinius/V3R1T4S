# CRITERION Skeptic Audit — `ihtp-ihtc2024-upper-bounds` (`i23`)

context: subagent (fresh invocation)
target_id: ihtp-ihtc2024-upper-bounds
package: 2026-10-27-zerbytheboss-6fb5ed18
audit_utc: 2026-10-27T19:50:00Z

## Literal Success Criterion Audit

1. **Instance Membership**:
   - Instance `i23` is an official benchmark instance of the Integrated Healthcare Timetabling Competition 2024.
2. **Zero Hard-Constraint Violations**:
   - Verified against the official `IHTP_Validator.cc` specification across all 9 hard constraint categories (`RoomGenderMix`, `PatientRoomCompatibility`, `SurgeonOvertime`, `OperatingTheaterOvertime`, `MandatoryUnscheduledPatients`, `AdmissionDay`, `RoomCapacity`, `NursePresence`, `UncoveredRoom`): `Total violations = 0`.
3. **Strict Improvement Over Live Listed Bound (`direction: min`)**:
   - Official live benchmark table lists `37542` as Best Known Solution.
   - Candidate solution `object/sol_i23_37231.json` achieves `Total cost = 37231` (RoomAgeMix 150, RoomSkillLevel 50, ContinuityOfCare 7675, ExcessiveNurseWorkload 883, OpenOperatingTheater 650, SurgeonTransfer 18, PatientDelay 6405, ElectiveUnscheduledPatients 21400), strictly lower by 311 points vs live BKS.
   - Satisfies the full `success_criterion` (`CONFIRMED_SOLUTION`).
4. **Soft-Cost Summation Reconciliation**:
   - The exact integer sum of the 8 weighted soft components equals the objective:
     150 + 50 + 7675 + 883 + 650 + 18 + 6405 + 21400 = 37231.

confirmed_scope: A feasible solution JSON file in object/sol_i23_37231.json for the IHTC-2024 competition instance i23 achieves Total violations = 0 across all 9 hard constraint categories and Total cost = 37231 (RoomAgeMix 150, RoomSkillLevel 50, ContinuityOfCare 7675, ExcessiveNurseWorkload 883, OpenOperatingTheater 650, SurgeonTransfer 18, PatientDelay 6405, ElectiveUnscheduledPatients 21400), verified by the official IHTP_Validator specification, strictly below the table upper bound of 37542 listed on https://ihtc2024.github.io/ihtp/index.html by 311 points.

pass: true
